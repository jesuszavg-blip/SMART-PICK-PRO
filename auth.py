import sqlite3
import hashlib
import json
import os
from pathlib import Path
import config

DB_PATH = Path(__file__).parent / "users.db"
USER_BACKUP_PATH = Path(__file__).parent / "users_backup.json"

try:
    import bcrypt
    HAS_BCRYPT = True
except ImportError:
    HAS_BCRYPT = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

def _hash_password(password: str) -> str:
    if HAS_BCRYPT:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    else:
        salt = "smart_pick_salt_2026"
        return f"sha256:{hashlib.sha256((password + salt).encode('utf-8')).hexdigest()}"

def _verify_password(password: str, hashed: str) -> bool:
    if hashed.startswith("$2b$") or hashed.startswith("$2a$"):
        if HAS_BCRYPT:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        return False
    elif hashed.startswith("sha256:"):
        salt = "smart_pick_salt_2026"
        expected = f"sha256:{hashlib.sha256((password + salt).encode('utf-8')).hexdigest()}"
        return expected == hashed
    else:
        return password == hashed

def _get_remote_sync_config():
    """Detecta si hay configuración remota en .env o Streamlit secrets"""
    remote_url = os.getenv("REMOTE_USERS_URL", "")
    remote_key = os.getenv("REMOTE_USERS_KEY", "")
    
    # Intentar leer desde streamlit.secrets si está disponible
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            if "REMOTE_USERS_URL" in st.secrets:
                remote_url = st.secrets["REMOTE_USERS_URL"]
            if "REMOTE_USERS_KEY" in st.secrets:
                remote_key = st.secrets["REMOTE_USERS_KEY"]
    except Exception:
        pass
        
    return remote_url, remote_key

def _sincronizar_remoto_push(users_list: list[dict]):
    """Envía la lista actualizada de usuarios al almacenamiento remoto si está configurado"""
    remote_url, remote_key = _get_remote_sync_config()
    if not remote_url or not HAS_REQUESTS:
        return False
    try:
        headers = {"Content-Type": "application/json"}
        if remote_key:
            headers["Authorization"] = f"Bearer {remote_key}"
            headers["X-Master-Key"] = remote_key
            headers["apikey"] = remote_key
        resp = requests.put(remote_url, json=users_list, headers=headers, timeout=5)
        return resp.status_code in [200, 201, 204]
    except Exception as e:
        print(f"Error al sincronizar usuarios con la nube: {e}")
        return False

def _sincronizar_remoto_pull() -> list[dict]:
    """Obtiene la lista de usuarios desde el almacenamiento remoto si está configurado"""
    remote_url, remote_key = _get_remote_sync_config()
    if not remote_url or not HAS_REQUESTS:
        return []
    try:
        headers = {}
        if remote_key:
            headers["Authorization"] = f"Bearer {remote_key}"
            headers["X-Master-Key"] = remote_key
            headers["apikey"] = remote_key
        resp = requests.get(remote_url, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, dict) and "record" in data:
                data = data["record"]
            if isinstance(data, list):
                return data
    except Exception as e:
        print(f"Error al descargar usuarios de la nube: {e}")
    return []

def _respaldar_usuarios_json():
    """Guarda un respaldo persistente de todos los usuarios en JSON local y remoto"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT username, password, role, is_active FROM users")
        rows = cursor.fetchall()
        conn.close()
        
        users_list = []
        for u, p, r, a in rows:
            users_list.append({"username": u, "password": p, "role": r, "is_active": a})
            
        with open(USER_BACKUP_PATH, "w", encoding="utf-8") as f:
            json.dump(users_list, f, ensure_ascii=False, indent=2)
            
        _sincronizar_remoto_push(users_list)
    except Exception as e:
        print(f"Error al respaldar usuarios: {e}")

def _cargar_usuarios_secrets() -> list[dict]:
    """Carga usuarios declarados como persistentes en Streamlit secrets o .env"""
    secrets_users = []
    
    # 1. Desde .env
    env_users = os.getenv("PERSISTENT_USERS", "")
    if env_users:
        try:
            data = json.loads(env_users)
            if isinstance(data, list):
                secrets_users.extend(data)
        except Exception:
            pass

    # 2. Desde st.secrets
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "PERSISTENT_USERS" in st.secrets:
            raw = st.secrets["PERSISTENT_USERS"]
            if isinstance(raw, list):
                secrets_users.extend(raw)
            elif isinstance(raw, str):
                try:
                    data = json.loads(raw)
                    if isinstance(data, list):
                        secrets_users.extend(data)
                except Exception:
                    pass
    except Exception:
        pass

    return secrets_users

def init_db():
    """Inicializa la base de datos y restaura usuarios desde todas las fuentes persistentes"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'VIP',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )
    ''')
    conn.commit()

    # 1. Asegurar cuenta de Administrador por defecto
    cursor.execute("SELECT * FROM users WHERE username = ?", (config.ADMIN_INIT_USER.lower(),))
    admin_user = cursor.fetchone()
    if not admin_user:
        hashed_pw = _hash_password(config.ADMIN_INIT_PASS)
        cursor.execute(
            "INSERT INTO users (username, password, role, is_active) VALUES (?, ?, ?, 1)",
            (config.ADMIN_INIT_USER.lower(), hashed_pw, 'ADMIN')
        )
        conn.commit()

    # 2. Restaurar desde Almacenamiento Remoto (Nube) si está activo
    cloud_users = _sincronizar_remoto_pull()
    if cloud_users:
        for u_data in cloud_users:
            u_name = str(u_data.get("username", "")).strip().lower()
            u_pw = str(u_data.get("password", ""))
            u_role = str(u_data.get("role", "VIP"))
            u_active = int(u_data.get("is_active", 1))
            if u_name and u_pw:
                cursor.execute("SELECT id FROM users WHERE username = ?", (u_name,))
                if not cursor.fetchone():
                    pw_to_insert = u_pw if (u_pw.startswith("$2") or u_pw.startswith("sha256:")) else _hash_password(u_pw)
                    cursor.execute(
                        "INSERT INTO users (username, password, role, is_active) VALUES (?, ?, ?, ?)",
                        (u_name, pw_to_insert, u_role, u_active)
                    )
        conn.commit()

    # 3. Restaurar desde Secrets de Streamlit / .env si están definidos
    secrets_users = _cargar_usuarios_secrets()
    if secrets_users:
        for u_data in secrets_users:
            u_name = str(u_data.get("username", "")).strip().lower()
            u_pw = str(u_data.get("password", ""))
            u_role = str(u_data.get("role", "VIP"))
            u_active = int(u_data.get("is_active", 1))
            if u_name and u_pw:
                cursor.execute("SELECT id FROM users WHERE username = ?", (u_name,))
                if not cursor.fetchone():
                    pw_to_insert = u_pw if (u_pw.startswith("$2") or u_pw.startswith("sha256:")) else _hash_password(u_pw)
                    cursor.execute(
                        "INSERT INTO users (username, password, role, is_active) VALUES (?, ?, ?, ?)",
                        (u_name, pw_to_insert, u_role, u_active)
                    )
        conn.commit()

    # 4. Restaurar desde respaldo JSON local si existe
    if USER_BACKUP_PATH.exists():
        try:
            with open(USER_BACKUP_PATH, "r", encoding="utf-8") as f:
                saved_users = json.load(f)
                for u_data in saved_users:
                    u_name = str(u_data.get("username", "")).strip().lower()
                    u_pw = str(u_data.get("password", ""))
                    u_role = str(u_data.get("role", "VIP"))
                    u_active = int(u_data.get("is_active", 1))
                    if u_name and u_pw:
                        cursor.execute("SELECT id FROM users WHERE username = ?", (u_name,))
                        if not cursor.fetchone():
                            cursor.execute(
                                "INSERT INTO users (username, password, role, is_active) VALUES (?, ?, ?, ?)",
                                (u_name, u_pw, u_role, u_active)
                            )
            conn.commit()
        except Exception as e:
            print(f"Error al restaurar respaldo de usuarios: {e}")

    conn.close()

def verificar_credenciales(username: str, password: str) -> tuple[bool, str]:
    if not username or not password:
        return False, "Usuario o contraseña requeridos"

    username_clean = username.strip().lower()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT password, role, is_active FROM users WHERE username = ?", (username_clean,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return False, "Usuario no encontrado"

    hashed_pw, role, is_active = user
    if not is_active:
        return False, "Esta cuenta ha sido desactivada"

    if _verify_password(password, hashed_pw):
        return True, role

    return False, "Contraseña incorrecta"

def registrar_usuario(username: str, password: str, role: str = 'VIP') -> tuple[bool, str]:
    username_clean = username.strip().lower()
    if len(username_clean) < 3:
        return False, "El nombre de usuario debe tener al menos 3 caracteres."
    if len(password) < 4:
        return False, "La contraseña debe tener al menos 4 caracteres."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        hashed_pw = _hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password, role, is_active) VALUES (?, ?, ?, 1)",
            (username_clean, hashed_pw, role)
        )
        conn.commit()
        conn.close()
        _respaldar_usuarios_json()
        return True, f"Usuario '{username_clean}' registrado exitosamente como {role}."
    except sqlite3.IntegrityError:
        conn.close()
        return False, "El nombre de usuario ya existe."

def listar_usuarios():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role, is_active, created_at FROM users ORDER BY id DESC")
    users = cursor.fetchall()
    conn.close()
    return users

def cambiar_estado_usuario(user_id: int, nuevo_estado: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_active = ? WHERE id = ?", (nuevo_estado, user_id))
    conn.commit()
    conn.close()
    _respaldar_usuarios_json()

def eliminar_usuario(user_id: int) -> bool:
    """Elimina permanentemente un usuario por ID (evitando eliminar al admin principal)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if not row or row[0].lower() == config.ADMIN_INIT_USER.lower():
        conn.close()
        return False
        
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    _respaldar_usuarios_json()
    return True

def exportar_usuarios_json() -> str:
    """Exporta todos los usuarios en formato JSON formateado listo para descarga/respaldo"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username, password, role, is_active FROM users")
    rows = cursor.fetchall()
    conn.close()
    
    users_list = []
    for u, p, r, a in rows:
        users_list.append({"username": u, "password": p, "role": r, "is_active": a})
        
    return json.dumps(users_list, ensure_ascii=False, indent=2)

def importar_usuarios_json(json_str: str) -> tuple[int, int, str]:
    """Importa usuarios desde un texto JSON, restaurándolos en la base de datos sin duplicar"""
    try:
        users_data = json.loads(json_str)
        if not isinstance(users_data, list):
            return 0, 0, "El archivo JSON debe contener una lista de usuarios."
            
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        insertados = 0
        actualizados = 0
        
        for u in users_data:
            u_name = str(u.get("username", "")).strip().lower()
            u_pw = str(u.get("password", ""))
            u_role = str(u.get("role", "VIP"))
            u_active = int(u.get("is_active", 1))
            
            if u_name and u_pw:
                pw_val = u_pw if (u_pw.startswith("$2") or u_pw.startswith("sha256:")) else _hash_password(u_pw)
                cursor.execute("SELECT id FROM users WHERE username = ?", (u_name,))
                existing = cursor.fetchone()
                if existing:
                    cursor.execute(
                        "UPDATE users SET password = ?, role = ?, is_active = ? WHERE id = ?",
                        (pw_val, u_role, u_active, existing[0])
                    )
                    actualizados += 1
                else:
                    cursor.execute(
                        "INSERT INTO users (username, password, role, is_active) VALUES (?, ?, ?, ?)",
                        (u_name, pw_val, u_role, u_active)
                    )
                    insertados += 1
                    
        conn.commit()
        conn.close()
        _respaldar_usuarios_json()
        return insertados, actualizados, f"Éxito: {insertados} usuarios añadidos, {actualizados} actualizados."
    except Exception as e:
        return 0, 0, f"Error al importar JSON: {e}"

def obtener_estado_persistencia() -> dict:
    """Devuelve el estado de las capas de persistencia activas"""
    remote_url, _ = _get_remote_sync_config()
    secrets_users = _cargar_usuarios_secrets()
    
    return {
        "nube_activa": bool(remote_url),
        "secrets_activos": len(secrets_users) > 0,
        "backup_local_existe": USER_BACKUP_PATH.exists(),
        "total_usuarios": len(listar_usuarios())
    }

# Inicializar DB al importar
init_db()
