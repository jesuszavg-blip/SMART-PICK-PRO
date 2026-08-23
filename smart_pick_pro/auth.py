import sqlite3
import hashlib
import os
from pathlib import Path
import config

DB_PATH = Path(__file__).parent / "users.db"

try:
    import bcrypt
    HAS_BCRYPT = True
except ImportError:
    HAS_BCRYPT = False

def _hash_password(password: str) -> str:
    if HAS_BCRYPT:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    else:
        # Fallback a SHA-256 con salt si bcrypt no está instalado
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
        # Comparación texto plano para compatibilidad de migración inicial
        return password == hashed

USER_BACKUP_PATH = Path(__file__).parent / "users_backup.json"

def _respaldar_usuarios_json():
    """Guarda un respaldo persistente de todos los usuarios en JSON"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT username, password, role, is_active FROM users")
        rows = cursor.fetchall()
        conn.close()
        
        users_list = []
        for u, p, r, a in rows:
            users_list.append({"username": u, "password": p, "role": r, "is_active": a})
            
        import json
        with open(USER_BACKUP_PATH, "w", encoding="utf-8") as f:
            json.dump(users_list, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error al respaldar usuarios: {e}")

def init_db():
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

    # Asegurar cuenta de Administrador por defecto
    cursor.execute("SELECT * FROM users WHERE username = ?", (config.ADMIN_INIT_USER.lower(),))
    admin_user = cursor.fetchone()
    if not admin_user:
        hashed_pw = _hash_password(config.ADMIN_INIT_PASS)
        cursor.execute(
            "INSERT INTO users (username, password, role, is_active) VALUES (?, ?, ?, 1)",
            (config.ADMIN_INIT_USER.lower(), hashed_pw, 'ADMIN')
        )
        conn.commit()

    # Auto-Restaurar usuarios del respaldo JSON si el servidor en la nube se reinició
    if USER_BACKUP_PATH.exists():
        try:
            import json
            with open(USER_BACKUP_PATH, "r", encoding="utf-8") as f:
                saved_users = json.load(f)
                for u_data in saved_users:
                    u_name = u_data.get("username", "").strip().lower()
                    u_pw = u_data.get("password", "")
                    u_role = u_data.get("role", "VIP")
                    u_active = u_data.get("is_active", 1)
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

# Inicializar DB al importar
init_db()
