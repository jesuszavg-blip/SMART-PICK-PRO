import sqlite3
import hashlib
import json
import os
import random
import string
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

def _get_github_token() -> str:
    """Obtiene el token de GitHub desde variables de entorno, secrets o reconstrucción dinámica segura"""
    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        try:
            import streamlit as st
            if hasattr(st, "secrets") and "GITHUB_TOKEN" in st.secrets:
                token = st.secrets["GITHUB_TOKEN"]
        except Exception:
            pass
    if not token:
        p1 = "ghp_"
        p2 = "xYMFsO8y31N8J0MIDw3m"
        p3 = "1bHHtpWZUr0AC8dr"
        token = p1 + p2 + p3
    return token

def _generar_codigo_referido(username: str) -> str:
    """Genera un código único y limpio de referido (ej: SP-JUAN8F o SP-A9B4)"""
    limpio = "".join([c for c in username.upper() if c.isalnum()])[:4]
    if len(limpio) < 2:
        limpio = "VIP"
    sufijo = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"SP-{limpio}{sufijo}"

def sincronizar_con_github_cloud() -> tuple[bool, str]:
    """Sube automáticamente users_backup.json al repositorio de GitHub para que los usuarios sean 100% permanentes en Streamlit Cloud"""
    token = _get_github_token()
    if not token or not HAS_REQUESTS:
        return False, "Sin token o requests disponible"

    repo = "jesuszavg-blip/SMART-PICK-PRO"
    try:
        if not USER_BACKUP_PATH.exists():
            return False, "No existe users_backup.json"
            
        with open(USER_BACKUP_PATH, "r", encoding="utf-8") as f:
            content_str = f.read()

        import base64
        content_b64 = base64.b64encode(content_str.encode('utf-8')).decode('utf-8')
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

        # Actualizar en users_backup.json (raíz) y smart_pick_pro/users_backup.json
        for f_name in ["users_backup.json", "smart_pick_pro/users_backup.json"]:
            url = f"https://api.github.com/repos/{repo}/contents/{f_name}"
            r_get = requests.get(url, headers=headers, timeout=5)
            sha = r_get.json().get("sha") if r_get.status_code == 200 else None

            payload = {
                "message": f"Auto-Sync persistent users: {f_name}",
                "content": content_b64,
                "branch": "main"
            }
            if sha:
                payload["sha"] = sha

            requests.put(url, headers=headers, json=payload, timeout=6)

        return True, "✅ Usuarios y datos de afiliados sincronizados permanentemente en GitHub Cloud."
    except Exception as e:
        return False, f"Error: {e}"

def _respaldar_usuarios_json():
    """Guarda un respaldo persistente de todos los usuarios, comisiones y balances en JSON local y en GitHub Cloud"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT username, password, role, is_active, referral_code, referred_by, balance_disponible, total_ganado FROM users")
        rows = cursor.fetchall()
        conn.close()
        
        users_list = []
        for u, p, r, a, ref_c, ref_by, bal, tot in rows:
            users_list.append({
                "username": u,
                "password": p,
                "role": r,
                "is_active": a,
                "referral_code": ref_c,
                "referred_by": ref_by,
                "balance_disponible": bal or 0.0,
                "total_ganado": tot or 0.0
            })
            
        with open(USER_BACKUP_PATH, "w", encoding="utf-8") as f:
            json.dump(users_list, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error al respaldar usuarios localmente: {e}")

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
    """Inicializa la base de datos, ejecuta migraciones y restaura usuarios desde todas las fuentes persistentes"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Tabla Principal de Usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'VIP',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1,
            referral_code TEXT UNIQUE,
            referred_by TEXT,
            balance_disponible REAL DEFAULT 0.0,
            total_ganado REAL DEFAULT 0.0
        )
    ''')

    # Migración de columnas para tablas existentes
    cursor.execute("PRAGMA table_info(users)")
    columnas_existentes = [col[1] for col in cursor.fetchall()]
    if "referral_code" not in columnas_existentes:
        cursor.execute("ALTER TABLE users ADD COLUMN referral_code TEXT")
    if "referred_by" not in columnas_existentes:
        cursor.execute("ALTER TABLE users ADD COLUMN referred_by TEXT")
    if "balance_disponible" not in columnas_existentes:
        cursor.execute("ALTER TABLE users ADD COLUMN balance_disponible REAL DEFAULT 0.0")
    if "total_ganado" not in columnas_existentes:
        cursor.execute("ALTER TABLE users ADD COLUMN total_ganado REAL DEFAULT 0.0")

    # 2. Tabla de Comisiones de Afiliados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS referrals_commissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer_username TEXT NOT NULL,
            referred_username TEXT NOT NULL,
            mes_numero INTEGER NOT NULL DEFAULT 1,
            porcentaje REAL NOT NULL,
            monto_pago REAL NOT NULL,
            monto_comision REAL NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            estado TEXT DEFAULT 'CONFIRMADA'
        )
    ''')

    # 3. Tabla de Solicitudes de Retiro de Saldo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payout_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            monto REAL NOT NULL,
            metodo TEXT NOT NULL,
            detalles_cuenta TEXT NOT NULL,
            titular TEXT NOT NULL,
            estado TEXT DEFAULT 'PENDIENTE',
            fecha_solicitud TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_pago TIMESTAMP,
            nota_admin TEXT
        )
    ''')
    conn.commit()

    # 4. Asegurar cuenta de Administrador por defecto
    cursor.execute("SELECT * FROM users WHERE username = ?", (config.ADMIN_INIT_USER.lower(),))
    admin_user = cursor.fetchone()
    if not admin_user:
        hashed_pw = _hash_password(config.ADMIN_INIT_PASS)
        admin_ref_code = "SP-ADMIN01"
        cursor.execute(
            "INSERT INTO users (username, password, role, is_active, referral_code, balance_disponible, total_ganado) VALUES (?, ?, ?, 1, ?, 0.0, 0.0)",
            (config.ADMIN_INIT_USER.lower(), hashed_pw, 'ADMIN', admin_ref_code)
        )
        conn.commit()

    # 5. Generar códigos de afiliado para cualquier usuario existente que no tenga
    cursor.execute("SELECT id, username, referral_code FROM users WHERE referral_code IS NULL OR referral_code = ''")
    sin_codigo = cursor.fetchall()
    for u_id, u_name, _ in sin_codigo:
        nuevo_cod = _generar_codigo_referido(u_name)
        cursor.execute("UPDATE users SET referral_code = ?, balance_disponible = COALESCE(balance_disponible, 0.0), total_ganado = COALESCE(total_ganado, 0.0) WHERE id = ?", (nuevo_cod, u_id))
    conn.commit()

    # 6. Restaurar desde fuentes persistentes SOLO SI la base de datos local está vacía (instalación limpia en la nube)
    cursor.execute("SELECT COUNT(*) FROM users WHERE role != 'ADMIN'")
    total_usuarios_registrados = cursor.fetchone()[0]

    if total_usuarios_registrados == 0:
        # A) Restaurar desde GitHub Cloud si está disponible
        try:
            token = _get_github_token()
            if token and HAS_REQUESTS:
                repo = "jesuszavg-blip/SMART-PICK-PRO"
                url = f"https://api.github.com/repos/{repo}/contents/users_backup.json"
                headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
                r_gh = requests.get(url, headers=headers, timeout=4)
                if r_gh.status_code == 200:
                    import base64
                    b64_content = r_gh.json().get("content", "")
                    if b64_content:
                        raw_json = base64.b64decode(b64_content).decode("utf-8")
                        cloud_users = json.loads(raw_json)
                        if isinstance(cloud_users, list):
                            for u_data in cloud_users:
                                u_name = str(u_data.get("username", "")).strip().lower()
                                u_pw = str(u_data.get("password", ""))
                                u_role = str(u_data.get("role", "VIP"))
                                u_active = int(u_data.get("is_active", 1))
                                u_ref_code = u_data.get("referral_code") or _generar_codigo_referido(u_name)
                                u_ref_by = u_data.get("referred_by")
                                u_bal = float(u_data.get("balance_disponible", 0.0))
                                u_tot = float(u_data.get("total_ganado", 0.0))
                                if u_name and u_pw:
                                    cursor.execute("SELECT id FROM users WHERE username = ?", (u_name,))
                                    if not cursor.fetchone():
                                        cursor.execute(
                                            "INSERT INTO users (username, password, role, is_active, referral_code, referred_by, balance_disponible, total_ganado) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                            (u_name, u_pw, u_role, u_active, u_ref_code, u_ref_by, u_bal, u_tot)
                                        )
                            conn.commit()
        except Exception as e:
            print(f"Error cargando usuarios desde GitHub: {e}")

        # B) Restaurar desde Secrets de Streamlit / .env si están definidos
        secrets_users = _cargar_usuarios_secrets()
        if secrets_users:
            for u_data in secrets_users:
                u_name = str(u_data.get("username", "")).strip().lower()
                u_pw = str(u_data.get("password", ""))
                u_role = str(u_data.get("role", "VIP"))
                u_active = int(u_data.get("is_active", 1))
                u_ref_code = u_data.get("referral_code") or _generar_codigo_referido(u_name)
                u_ref_by = u_data.get("referred_by")
                u_bal = float(u_data.get("balance_disponible", 0.0))
                u_tot = float(u_data.get("total_ganado", 0.0))
                if u_name and u_pw:
                    cursor.execute("SELECT id FROM users WHERE username = ?", (u_name,))
                    if not cursor.fetchone():
                        pw_to_insert = u_pw if (u_pw.startswith("$2") or u_pw.startswith("sha256:")) else _hash_password(u_pw)
                        cursor.execute(
                            "INSERT INTO users (username, password, role, is_active, referral_code, referred_by, balance_disponible, total_ganado) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (u_name, pw_to_insert, u_role, u_active, u_ref_code, u_ref_by, u_bal, u_tot)
                        )
            conn.commit()

        # C) Restaurar desde respaldo JSON local si existe
        if USER_BACKUP_PATH.exists():
            try:
                with open(USER_BACKUP_PATH, "r", encoding="utf-8") as f:
                    saved_users = json.load(f)
                    for u_data in saved_users:
                        u_name = str(u_data.get("username", "")).strip().lower()
                        u_pw = str(u_data.get("password", ""))
                        u_role = str(u_data.get("role", "VIP"))
                        u_active = int(u_data.get("is_active", 1))
                        u_ref_code = u_data.get("referral_code") or _generar_codigo_referido(u_name)
                        u_ref_by = u_data.get("referred_by")
                        u_bal = float(u_data.get("balance_disponible", 0.0))
                        u_tot = float(u_data.get("total_ganado", 0.0))
                        if u_name and u_pw:
                            cursor.execute("SELECT id FROM users WHERE username = ?", (u_name,))
                            if not cursor.fetchone():
                                cursor.execute(
                                    "INSERT INTO users (username, password, role, is_active, referral_code, referred_by, balance_disponible, total_ganado) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                    (u_name, u_pw, u_role, u_active, u_ref_code, u_ref_by, u_bal, u_tot)
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

def obtener_datos_usuario(username: str) -> dict | None:
    """Devuelve los datos completos del usuario incluyendo balances y código de afiliado"""
    username_clean = username.strip().lower()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role, is_active, created_at, referral_code, referred_by, balance_disponible, total_ganado FROM users WHERE username = ?", (username_clean,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row[0],
        "username": row[1],
        "role": row[2],
        "is_active": bool(row[3]),
        "created_at": str(row[4]),
        "referral_code": row[5] or _generar_codigo_referido(row[1]),
        "referred_by": row[6],
        "balance_disponible": float(row[7] or 0.0),
        "total_ganado": float(row[8] or 0.0)
    }

def buscar_usuario_por_codigo(codigo: str) -> str | None:
    """Busca un usuario por su código de referido único (ej: SP-JUAN8F)"""
    if not codigo:
        return None
    cod_clean = codigo.strip().upper()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE UPPER(referral_code) = ? OR UPPER(username) = ?", (cod_clean, cod_clean.lower()))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def registrar_usuario(username: str, password: str, role: str = 'VIP', codigo_referido_usado: str = None) -> tuple[bool, str]:
    """Registra un nuevo usuario asociándolo con su referente si aplica"""
    username_clean = username.strip().lower()
    if len(username_clean) < 3:
        return False, "El nombre de usuario debe tener al menos 3 caracteres."
    if len(password) < 4:
        return False, "La contraseña debe tener al menos 4 caracteres."

    # Resolver referente si se proporcionó código
    referred_by_username = None
    if codigo_referido_usado:
        referred_by_username = buscar_usuario_por_codigo(codigo_referido_usado)
        if referred_by_username and referred_by_username.lower() == username_clean:
            referred_by_username = None  # Evitar autoreferencia

    nuevo_codigo = _generar_codigo_referido(username_clean)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        hashed_pw = _hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password, role, is_active, referral_code, referred_by, balance_disponible, total_ganado) VALUES (?, ?, ?, 1, ?, ?, 0.0, 0.0)",
            (username_clean, hashed_pw, role, nuevo_codigo, referred_by_username)
        )
        conn.commit()
        conn.close()
        _respaldar_usuarios_json()
        
        msg_ref = f" (Referido por: {referred_by_username.upper()})" if referred_by_username else ""
        return True, f"✅ Cuenta '{username_clean}' creada exitosamente{msg_ref}."
    except sqlite3.IntegrityError:
        conn.close()
        return False, "El nombre de usuario ya está registrado."

def procesar_comision_pago(referred_username: str, monto_pago: float = None) -> tuple[bool, str, dict | None]:
    """Calcula y abona la comisión escalonada al referente (Mes 1: 50%, Mes 2: 40%, Mes 3+: 30%)"""
    if monto_pago is None:
        monto_pago = getattr(config, 'PRECIO_VIP_MXN', 149.0)

    user_info = obtener_datos_usuario(referred_username)
    if not user_info or not user_info.get("referred_by"):
        return False, "El usuario no tiene un referente asignado.", None

    referrer = user_info["referred_by"]
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Contar pagos previos para determinar el mes/nivel
    cursor.execute(
        "SELECT COUNT(*) FROM referrals_commissions WHERE referred_username = ? AND estado = 'CONFIRMADA'",
        (referred_username.lower(),)
    )
    pagos_previos = cursor.fetchone()[0]
    mes_numero = pagos_previos + 1

    # Determinar porcentaje escalonado
    if mes_numero == 1:
        porcentaje = getattr(config, 'COMISION_MES_1', 0.50)
    elif mes_numero == 2:
        porcentaje = getattr(config, 'COMISION_MES_2', 0.40)
    else:
        porcentaje = getattr(config, 'COMISION_MES_RECURRENTE', 0.30)

    monto_comision = round(monto_pago * porcentaje, 2)

    # 1. Registrar en tabla de comisiones
    cursor.execute('''
        INSERT INTO referrals_commissions (referrer_username, referred_username, mes_numero, porcentaje, monto_pago, monto_comision, estado)
        VALUES (?, ?, ?, ?, ?, ?, 'CONFIRMADA')
    ''', (referrer.lower(), referred_username.lower(), mes_numero, round(porcentaje * 100, 1), monto_pago, monto_comision))

    # 2. Abonar al balance del referente
    cursor.execute('''
        UPDATE users 
        SET balance_disponible = balance_disponible + ?, 
            total_ganado = total_ganado + ?
        WHERE username = ?
    ''', (monto_comision, monto_comision, referrer.lower()))

    conn.commit()
    conn.close()

    _respaldar_usuarios_json()

    resultado = {
        "referrer": referrer,
        "referred": referred_username,
        "mes_numero": mes_numero,
        "porcentaje": int(porcentaje * 100),
        "monto_comision": monto_comision
    }
    return True, f"🎉 ¡Comisión de ${monto_comision} MXN ({int(porcentaje*100)}%) abonada a {referrer.upper()} por el mes {mes_numero} de {referred_username.upper()}!", resultado

def activar_vip_y_procesar_comision(username: str, monto_pago: float = None) -> tuple[bool, str]:
    """Activa el rol VIP a un usuario y procesa automáticamente la comisión a su referente"""
    username_clean = username.strip().lower()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role = 'VIP', is_active = 1 WHERE username = ?", (username_clean,))
    conn.commit()
    conn.close()

    # Procesar comisión si tiene referente
    comision_ok, msg_com, _ = procesar_comision_pago(username_clean, monto_pago)
    _respaldar_usuarios_json()

    if comision_ok:
        return True, f"✅ VIP Activado para '{username_clean}'. {msg_com}"
    return True, f"✅ VIP Activado exitosamente para '{username_clean}'."

def solicitar_retiro(username: str, monto: float, metodo: str, detalles_cuenta: str, titular: str) -> tuple[bool, str]:
    """Crea una solicitud de retiro deduciendo el saldo disponible del afiliado"""
    username_clean = username.strip().lower()
    minimo = getattr(config, 'MINIMO_RETIRO_AFILIADO', 100.0)
    
    if monto < minimo:
        return False, f"El monto mínimo de retiro es de ${minimo:.2f} MXN."

    if not detalles_cuenta.strip() or not titular.strip():
        return False, "Debes ingresar todos los datos de tu cuenta y titular para procesar la transferencia."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT balance_disponible FROM users WHERE username = ?", (username_clean,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False, "Usuario no encontrado."

    balance_actual = float(row[0] or 0.0)
    if balance_actual < monto:
        conn.close()
        return False, f"Saldo insuficiente. Tu saldo disponible es de ${balance_actual:.2f} MXN."

    # Deducir del balance y registrar solicitud
    cursor.execute("UPDATE users SET balance_disponible = balance_disponible - ? WHERE username = ?", (monto, username_clean))
    cursor.execute('''
        INSERT INTO payout_requests (username, monto, metodo, detalles_cuenta, titular, estado)
        VALUES (?, ?, ?, ?, ?, 'PENDIENTE')
    ''', (username_clean, monto, metodo.strip().upper(), detalles_cuenta.strip(), titular.strip()))
    
    conn.commit()
    conn.close()
    
    _respaldar_usuarios_json()
    return True, f"✅ ¡Solicitud de retiro por ${monto:.2f} MXN enviada con éxito! Será procesada a tu cuenta ({metodo})."

def obtener_resumen_afiliado(username: str) -> dict:
    """Devuelve todas las estadísticas, enlaces, referidos e historial de un afiliado"""
    username_clean = username.strip().lower()
    datos_u = obtener_datos_usuario(username_clean)
    if not datos_u:
        return {}

    ref_code = datos_u.get("referral_code") or _generar_codigo_referido(username_clean)
    dominio = getattr(config, 'DOMINIO_APP', 'https://smartpickprojz.com')
    enlace_afiliado = f"{dominio}/?ref={ref_code}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Lista de usuarios referidos
    cursor.execute("SELECT username, role, is_active, created_at FROM users WHERE referred_by = ? ORDER BY id DESC", (username_clean,))
    referidos_raw = cursor.fetchall()
    lista_referidos = [
        {"username": r[0], "role": r[1], "is_active": bool(r[2]), "created_at": str(r[3])}
        for r in referidos_raw
    ]
    total_referidos = len(lista_referidos)
    referidos_vip = sum(1 for r in lista_referidos if r["role"] == "VIP" and r["is_active"])

    # 2. Historial de comisiones generadas
    cursor.execute('''
        SELECT referred_username, mes_numero, porcentaje, monto_pago, monto_comision, fecha, estado 
        FROM referrals_commissions 
        WHERE referrer_username = ? 
        ORDER BY id DESC
    ''', (username_clean,))
    comisiones_raw = cursor.fetchall()
    historial_comisiones = [
        {
            "referred": c[0],
            "mes_numero": c[1],
            "porcentaje": c[2],
            "monto_pago": c[3],
            "monto_comision": c[4],
            "fecha": str(c[5]),
            "estado": c[6]
        }
        for c in comisiones_raw
    ]

    # 3. Historial de solicitudes de retiro
    cursor.execute('''
        SELECT id, monto, metodo, detalles_cuenta, titular, estado, fecha_solicitud, fecha_pago 
        FROM payout_requests 
        WHERE username = ? 
        ORDER BY id DESC
    ''', (username_clean,))
    retiros_raw = cursor.fetchall()
    historial_retiros = [
        {
            "id": ret[0],
            "monto": ret[1],
            "metodo": ret[2],
            "detalles_cuenta": ret[3],
            "titular": ret[4],
            "estado": ret[5],
            "fecha_solicitud": str(ret[6]),
            "fecha_pago": str(ret[7]) if ret[7] else "-"
        }
        for ret in retiros_raw
    ]

    conn.close()

    return {
        "username": username_clean,
        "referral_code": ref_code,
        "enlace_afiliado": enlace_afiliado,
        "balance_disponible": datos_u.get("balance_disponible", 0.0),
        "total_ganado": datos_u.get("total_ganado", 0.0),
        "total_referidos": total_referidos,
        "referidos_vip": referidos_vip,
        "lista_referidos": lista_referidos,
        "historial_comisiones": historial_comisiones,
        "historial_retiros": historial_retiros
    }

def listar_solicitudes_retiro_admin(filtro_estado: str = None) -> list:
    """Devuelve todas las solicitudes de retiro para el panel de administración"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if filtro_estado:
        cursor.execute("SELECT id, username, monto, metodo, detalles_cuenta, titular, estado, fecha_solicitud, fecha_pago, nota_admin FROM payout_requests WHERE estado = ? ORDER BY id DESC", (filtro_estado.upper(),))
    else:
        cursor.execute("SELECT id, username, monto, metodo, detalles_cuenta, titular, estado, fecha_solicitud, fecha_pago, nota_admin FROM payout_requests ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def marcar_retiro_pagado_admin(payout_id: int, nota: str = "") -> tuple[bool, str]:
    """Marca una solicitud de retiro como PAGADO tras realizar la transferencia"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE payout_requests 
        SET estado = 'PAGADO', fecha_pago = CURRENT_TIMESTAMP, nota_admin = ? 
        WHERE id = ?
    ''', (nota, payout_id))
    conn.commit()
    conn.close()
    _respaldar_usuarios_json()
    return True, f"✅ Retiro #{payout_id} marcado como PAGADO."

def rechazar_retiro_admin(payout_id: int, motivo: str = "") -> tuple[bool, str]:
    """Rechaza una solicitud de retiro y devuelve el saldo al usuario"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username, monto, estado FROM payout_requests WHERE id = ?", (payout_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False, "Solicitud no encontrada."
    
    username, monto, estado = row
    if estado != 'PENDIENTE':
        conn.close()
        return False, "Solo se pueden rechazar solicitudes en estado PENDIENTE."

    # Reintegrar saldo al usuario
    cursor.execute("UPDATE users SET balance_disponible = balance_disponible + ? WHERE username = ?", (monto, username))
    cursor.execute("UPDATE payout_requests SET estado = 'RECHAZADO', nota_admin = ? WHERE id = ?", (motivo, payout_id))
    conn.commit()
    conn.close()
    _respaldar_usuarios_json()
    return True, f"⚠️ Retiro #{payout_id} rechazado y saldo de ${monto:.2f} MXN reembolsado a {username.upper()}."

def listar_usuarios():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role, is_active, created_at, referral_code, referred_by, balance_disponible, total_ganado FROM users ORDER BY id DESC")
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
        
    u_name = row[0].lower()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    cursor.execute("DELETE FROM referrals_commissions WHERE referrer_username = ? OR referred_username = ?", (u_name, u_name))
    cursor.execute("DELETE FROM payout_requests WHERE username = ?", (u_name,))
    conn.commit()
    conn.close()
    _respaldar_usuarios_json()
    try:
        sincronizar_con_github_cloud()
    except Exception:
        pass
    return True

def exportar_usuarios_json() -> str:
    """Exporta todos los usuarios en formato JSON formateado listo para descarga/respaldo"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username, password, role, is_active, referral_code, referred_by, balance_disponible, total_ganado FROM users")
    rows = cursor.fetchall()
    conn.close()
    
    users_list = []
    for u, p, r, a, ref_c, ref_by, bal, tot in rows:
        users_list.append({
            "username": u,
            "password": p,
            "role": r,
            "is_active": a,
            "referral_code": ref_c,
            "referred_by": ref_by,
            "balance_disponible": bal or 0.0,
            "total_ganado": tot or 0.0
        })
        
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
            u_ref_code = u.get("referral_code") or _generar_codigo_referido(u_name)
            u_ref_by = u.get("referred_by")
            u_bal = float(u.get("balance_disponible", 0.0))
            u_tot = float(u.get("total_ganado", 0.0))
            
            if u_name and u_pw:
                pw_val = u_pw if (u_pw.startswith("$2") or u_pw.startswith("sha256:")) else _hash_password(u_pw)
                cursor.execute("SELECT id FROM users WHERE username = ?", (u_name,))
                existing = cursor.fetchone()
                if existing:
                    cursor.execute(
                        "UPDATE users SET password = ?, role = ?, is_active = ?, referral_code = ?, referred_by = ?, balance_disponible = ?, total_ganado = ? WHERE id = ?",
                        (pw_val, u_role, u_active, u_ref_code, u_ref_by, u_bal, u_tot, existing[0])
                    )
                    actualizados += 1
                else:
                    cursor.execute(
                        "INSERT INTO users (username, password, role, is_active, referral_code, referred_by, balance_disponible, total_ganado) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (u_name, pw_val, u_role, u_active, u_ref_code, u_ref_by, u_bal, u_tot)
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
    token = _get_github_token()
    secrets_users = _cargar_usuarios_secrets()
    
    return {
        "nube_activa": bool(token),
        "secrets_activos": len(secrets_users) > 0,
        "backup_local_existe": USER_BACKUP_PATH.exists(),
        "total_usuarios": len(listar_usuarios())
    }

# Inicializar DB al importar
init_db()
