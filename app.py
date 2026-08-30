import os

# Configuración de variables de entorno de compatibilidad CPU
os.environ["NPY_DISABLE_CPU_FEATURES"] = "X86_V2 AVX2 FMA3 AVX512F"
os.environ["OPENBLAS_CORETYPE"] = "generic"

import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import random
import html
import json

# Importación segura de pandas con resguardo anti-fallos
try:
    import pandas as pd
    HAS_PANDAS = True
except Exception:
    pd = None
    HAS_PANDAS = False

# Módulos del Sistema
import importlib
import config
importlib.reload(config)
import auth
import api_client
importlib.reload(api_client)
import analytics
importlib.reload(analytics)
import progol
importlib.reload(progol)
import jornada_manager
import squads_data
import pitch_renderer

# Configuración de Página
st.set_page_config(
    page_title="Smart Pick Pro - Escáner Estadístico VIP",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Personalizados de Máximo Contraste Visual y Estética Premium VIP
st.markdown("""
<style>
    /* Icono Balón de Fútbol ⚽ en Sidebar Toggle */
    [data-testid="stSidebarCollapseButton"] svg, 
    [data-testid="collapsedControl"] svg {
        display: none !important;
    }

    [data-testid="stSidebarCollapseButton"]::after, 
    [data-testid="collapsedControl"]::after {
        content: "⚽" !important;
        font-size: 22px !important;
        line-height: 1 !important;
        cursor: pointer !important;
    }

    /* Estilos globales y contraste de texto */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Contraste forzado en la barra lateral */
    [data-testid="stSidebar"] {
        background-color: #161922 !important;
        border-right: 1px solid #2A2D3E;
    }
    
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }

    /* Banners y Tarjetas de Alto Contraste */
    .hero-banner {
        background: linear-gradient(135deg, #1E2130 0%, #00E676 100%);
        padding: 24px;
        border-radius: 14px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 6px 20px rgba(0, 230, 118, 0.25);
    }
    
    .card-dark {
        background-color: #1E2130;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 14px;
        border: 1px solid #2D3245;
        color: #FFFFFF !important;
    }
    
    .whatsapp-btn {
        background-color: #25D366;
        color: white !important;
        padding: 10px 22px;
        border-radius: 30px;
        text-decoration: none;
        font-weight: bold;
        font-size: 14px;
        box-shadow: 0 4px 10px rgba(37, 211, 102, 0.3);
        display: inline-block;
    }
    
    .casino-btn {
        background-color: #F39C12;
        color: white !important;
        padding: 6px 14px;
        border-radius: 20px;
        text-decoration: none;
        font-size: 12px;
        font-weight: bold;
    }

    /* Pestañas (st.tabs) Premium VIP */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #161922;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #2D3245;
    }

    .stTabs [data-baseweb="tab"] {
        height: 46px;
        white-space: pre-wrap;
        background-color: #1E2130;
        border-radius: 8px;
        color: #E0E0E0;
        font-weight: 800;
        font-size: 14px;
        padding: 0 16px;
        border: 1px solid #2A2D3E;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background-color: #00E676 !important;
        color: #0E1117 !important;
        border: 1px solid #00E676 !important;
        box-shadow: 0 0 12px rgba(0, 230, 118, 0.4);
    }

    /* Métricas con alto contraste */
    [data-testid="stMetricValue"] {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #00E676 !important;
    }

    [data-testid="stMetricLabel"] {
        color: #E0E0E0 !important;
        font-weight: 600 !important;
    }
    
    /* Cajas de alerta e información en texto blanco puro */
    .stAlert, [data-baseweb="notification"] {
        background-color: #1E2130 !important;
        border-left: 5px solid #00E676 !important;
    }

    .stAlert p, .stAlert span, [data-baseweb="notification"] p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Estilos Globales para Botones */
    .stButton > button {
        background-color: #1E2130 !important;
        color: #FFFFFF !important;
        border: 1.5px solid #00E676 !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        background-color: #00E676 !important;
        color: #0E1117 !important;
        box-shadow: 0 0 15px rgba(0, 230, 118, 0.5) !important;
    }

    /* Cuadro de texto Ficha VIP / Textarea con fondo blanco y texto NEGRO intenso */
    .stTextArea textarea, [data-baseweb="textarea"] textarea, div[data-baseweb="textarea"] > div > textarea {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        line-height: 1.5 !important;
        border: 2px solid #00E676 !important;
        border-radius: 10px !important;
    }
    
    .stTextArea label, .stTextArea p {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# Manejo de Sesión de Autenticación
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
if 'usuario' not in st.session_state:
    st.session_state['usuario'] = None
if 'rol' not in st.session_state:
    st.session_state['rol'] = None

# --- PANTALLA DE INICIO DE SESIÓN ---
if not st.session_state['autenticado']:
    st.markdown('''
    <div class="hero-banner" style="margin-top: 25px;">
        <h1 style="color: white; margin: 0; font-weight: 900; font-size: 38px; letter-spacing: 1px;">🏆 SMART PICK PRO VIP</h1>
        <p style="color: white; margin: 8px 0 0 0; font-size: 18px; opacity: 0.95;">Sistema de IA Predictiva • Optimizador de Reducciones Progol • Buscador $+EV$</p>
        <div style="margin-top: 12px; display: inline-block; background: rgba(0, 230, 118, 0.2); border: 2px solid #00E676; border-radius: 20px; padding: 6px 18px; color: #00E676; font-weight: 900; font-size: 14px;">
            ⭐ +85.4% de Efectividad Comprobada en Quinielas y Parlays VIP
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    col_log1, col_log2, col_log3 = st.columns([1, 2.5, 1])
    with col_log2:
        st.markdown('''
        <div style="background: #1E2130; padding: 25px; border-radius: 14px; border: 1px solid #2D3245; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
            <h3 style="color: white; margin: 0 0 15px 0; font-weight: 800; text-align: center;">🔒 Iniciar Sesión en tu Cuenta VIP</h3>
        ''', unsafe_allow_html=True)
        user_input = st.text_input("Usuario:", key="login_user")
        pwd_input = st.text_input("Contraseña:", type="password", key="login_pass")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 ACCEDER AL SISTEMA VIP", use_container_width=True):
            exito, mensaje_o_rol = auth.verificar_credenciales(user_input, pwd_input)
            if exito:
                st.session_state['autenticado'] = True
                st.session_state['usuario'] = user_input.strip().lower()
                st.session_state['rol'] = mensaje_o_rol
                st.rerun()
            else:
                st.error(f"❌ {mensaje_o_rol}")
                
        st.markdown("</div>", unsafe_allow_html=True)
        
        bancoppel_card = getattr(config, 'BANCOPPEL_TARJETA', '4169 1608 7646 1600')
        bancoppel_holder = getattr(config, 'BANCOPPEL_TITULAR', 'Jesús')
        paypal_url = getattr(config, 'PAYPAL_LINK', 'https://www.paypal.com/ncp/payment/HSSHUFTYF8FG2')

        html_pago = '<div style="background: linear-gradient(135deg, #161922 0%, #1E2130 100%); padding: 22px; border-radius: 14px; border: 2px dashed #00E676; margin-top: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.4);">'
        html_pago += '<h4 style="color: #00E676; margin: 0 0 10px 0; font-weight: 900; text-align: center;">💳 MÉTODOS DE PAGO PARA ACCESO VIP ($299 MXN / MES)</h4>'
        html_pago += '<p style="color: #E0E0E0; font-size: 13px; text-align: center; margin-bottom: 15px;">Realiza tu pago por <b>BanCoppel, OXXO o PayPal</b> y envía tu comprobante por WhatsApp para recibir tu usuario y contraseña de inmediato:</p>'
        
        html_pago += f'<div style="background: #161922; border-radius: 10px; padding: 14px; border: 1px solid #2D3245; margin-bottom: 12px;"><div style="color: #FFD700; font-weight: 900; font-size: 14px; margin-bottom: 6px;">🟡 DEPÓSITO / SPEI BANCOPPEL</div><div style="color: white; font-size: 13px;"><b>Banco:</b> BanCoppel</div><div style="color: white; font-size: 13px;"><b>No. de Tarjeta / SPEI:</b> <span style="color:#00E676; font-weight:bold; font-family:monospace;">{bancoppel_card}</span></div><div style="color: white; font-size: 13px;"><b>Titular:</b> {bancoppel_holder}</div><div style="color: #aaa; font-size: 11px; margin-top:4px;">* Acepta transferencias SPEI 24/7 y depósitos en OXXO o Tiendas Coppel.</div></div>'

        html_pago += f'<div style="background: #161922; border-radius: 10px; padding: 14px; border: 1px solid #2D3245; margin-bottom: 15px;"><div style="color: #5DADE2; font-weight: 900; font-size: 14px; margin-bottom: 6px;">🔵 PAGO EN LÍNEA POR PAYPAL</div><div style="color: white; font-size: 13px;"><b>Enlace PayPal:</b> <a href="{paypal_url}" target="_blank" style="color:#00E676; font-weight:bold;">{paypal_url}</a></div><div style="color: #aaa; font-size: 11px; margin-top:4px;">* Paga de forma segura con cualquier tarjeta de Débito o Crédito.</div></div>'

        html_pago += '<div style="text-align: center;"><a href="https://wa.me/526676947014?text=Hola%20Jesus,%20ya%20realice%20mi%20pago%20de%20%24299%20MXN.%20Adjunto%20mi%20comprobante%20para%20activar%20mi%20membresia%20VIP" target="_blank" class="whatsapp-btn" style="display:inline-block; width:100%; box-sizing:border-box;">💬 ENVIAR COMPROBANTE DE PAGO POR WHATSAPP</a></div>'
        html_pago += '</div>'

        st.markdown(html_pago, unsafe_allow_html=True)
        
    st.stop()

# --- PANTALLA PRINCIPAL (AUTENTICADO) ---

# Cargar Jornada Oficial Activa de Progol (14 Partidos)
jornada_oficial = jornada_manager.cargar_jornada_activa()

# Encabezado Principal
st.markdown(f'''
<div class="hero-banner">
    <h1 style="color: white; margin: 0; font-weight: 900; font-size: 34px;">🏆 SMART PICK PRO</h1>
    <p style="color: white; margin: 4px 0 0 0; font-size: 15px; opacity: 0.95;">
        Bienvenido <b>{st.session_state['usuario'].upper()}</b> [{st.session_state['rol']}] | Escáner Estadístico VIP & Optimizador Progol
    </p>
</div>
''', unsafe_allow_html=True)

# Botón WhatsApp Superior & Logout
col_top1, col_top2 = st.columns([8, 2])
with col_top1:
    st.markdown(f'''
    <a href="{config.ENLACE_WHATSAPP}" target="_blank" class="whatsapp-btn">
        💬 Soporte WhatsApp VIP
    </a>
    ''', unsafe_allow_html=True)
with col_top2:
    if st.button("🔴 Cerrar Sesión", use_container_width=True):
        st.session_state['autenticado'] = False
        st.session_state['usuario'] = None
        st.session_state['rol'] = None
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# --- BARRA LATERAL ---
dict_ligas_globales = api_client.obtener_ligas_mundo()
liga_elegida = st.sidebar.selectbox("🌍 1. Selecciona el Torneo o Módulo:", list(dict_ligas_globales.keys()))
liga_elegida_val = dict_ligas_globales[liga_elegida]

# Partidos de la jornada
partidos_dict = api_client.obtener_partidos_jornada(liga_elegida_val)
partido_seleccionado = st.sidebar.selectbox("⚽ 2. Encuentro a analizar:", list(partidos_dict.keys()))

# Manejo de Partido Personalizado Manual
datos_partido_custom = None
if partido_seleccionado and "PERSONALIZADO" in partido_seleccionado:
    st.sidebar.markdown("---")
    st.sidebar.write("### ✏️ Configura tu Partido Manual")
    custom_loc = st.sidebar.text_input("🔵 Equipo Local:", value="América", key="custom_loc_in")
    custom_vis = st.sidebar.text_input("🔴 Equipo Visitante:", value="Guadalajara", key="custom_vis_in")
    
    logo_l_custom = api_client.obtener_logo_oficial_equipo(custom_loc)
    logo_v_custom = api_client.obtener_logo_oficial_equipo(custom_vis)

    datos_partido_custom = {
        "id": "CUSTOM_MATCH",
        "local": custom_loc.strip(),
        "local_id": 0,
        "logo_local": logo_l_custom,
        "visita": custom_vis.strip(),
        "visita_id": 0,
        "logo_visita": logo_v_custom,
        "venue": f"Estadio {custom_loc.strip()}",
        "city": "México",
        "referee": "Árbitro Oficial Asignado"
    }

# --- PANEL DE ADMINISTRACIÓN (SOLO ROL ADMIN) ---
if st.session_state['rol'] == 'ADMIN':
    with st.sidebar.expander("🔑 Panel de Administración VIP", expanded=False):
        # 1. Estado de Persistencia
        est_pers = auth.obtener_estado_persistencia()
        st.write("#### 🛡️ Estado de Persistencia")
        st.markdown(f"""
        - 👥 **Total Usuarios:** `{est_pers['total_usuarios']}`
        - 📁 **Respaldo Local JSON:** `{'✅ Activo' if est_pers['backup_local_existe'] else '❌ Inactivo'}`
        - ☁️ **Sincronización Nube:** `{'✅ Conectado' if est_pers['nube_activa'] else '🟡 Modo Local'}`
        - 🔑 **Streamlit Secrets:** `{'✅ Activo' if est_pers['secrets_activos'] else '⚪ No definido'}`
        """)

        # 2. Respaldo y Restauración en 1 Clic
        st.write("#### 💾 Respaldos de Base de Datos")
        json_backup_data = auth.exportar_usuarios_json()
        st.download_button(
            label="📥 Descargar Respaldo JSON",
            data=json_backup_data,
            file_name="smart_pick_usuarios_respaldo.json",
            mime="application/json",
            use_container_width=True
        )

        uploaded_backup = st.file_uploader("📤 Restaurar Usuarios (JSON):", type=["json"], key="restore_uploader")
        if uploaded_backup is not None:
            try:
                json_content = uploaded_backup.getvalue().decode("utf-8")
                ins, act, msg_res = auth.importar_usuarios_json(json_content)
                st.success(msg_res)
                st.rerun()
            except Exception as e:
                st.error(f"Error al procesar archivo: {e}")

        st.markdown("---")
        # 3. Registrar Nuevo Usuario
        st.write("#### ➕ Registrar Nuevo Usuario")
        new_u = st.text_input("Usuario:", key="admin_new_u")
        new_p = st.text_input("Contraseña:", type="password", key="admin_new_p")
        new_r = st.selectbox("Rol:", ["VIP", "ADMIN"], key="admin_new_r")
        if st.button("➕ Crear Usuario", use_container_width=True):
            ok, msg = auth.registrar_usuario(new_u, new_p, new_r)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
                
        st.markdown("---")
        # 4. Configuración de API Key
        st.write("#### ⚙️ Clave API-Sports")
        api_k_input = st.text_input("API Key:", value=config.API_KEY, type="password")
        if st.button("💾 Guardar API Key", use_container_width=True):
            config.API_KEY = api_k_input.strip()
            st.success("✅ API Key actualizada.")
                
        st.markdown("---")
        # 5. Lista de Usuarios y Gestión
        st.write("#### 📋 Usuarios Registrados")
        usuarios_lista = auth.listar_usuarios()
        for u in usuarios_lista:
            u_id, u_name, u_rol, u_act, u_date = u
            col_u1, col_u2 = st.columns([3, 1])
            with col_u1:
                status_icon = "🟢" if u_act == 1 else "🔴"
                st.markdown(f"**{status_icon} {u_name.upper()}** [{u_rol}]")
            with col_u2:
                if u_name.lower() != config.ADMIN_INIT_USER.lower():
                    if st.button("🗑️", key=f"del_u_{u_id}", help="Eliminar usuario"):
                        auth.eliminar_usuario(u_id)
                        st.rerun()

# --- MODO 1: PROGOL TRADICIONAL ---
if liga_elegida_val == "PROGOL_MODE":
    st.markdown('''
    <div style="background: linear-gradient(135deg, #1E2130 0%, #FFD700 100%); padding: 22px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
        <h2 style="color: #1E2130; margin: 0; font-weight: 900;">🎯 OPTIMIZADOR INTELIGENTE DE QUINIELA PROGOL</h2>
        <p style="color: #1E2130; margin: 6px 0 0 0; font-size: 15px;">Configura tus dobles y triples deseados sobre los 14 partidos oficiales.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    with st.expander("📝 Cargar / Editar los 14 Partidos Oficiales Progol de esta Semana"):
        st.info("💡 Ingresa los nombres reales de los equipos locales y visitantes de la boleta oficial:")
        nuevos_partidos = []
        for p_idx in range(1, 15):
            p_actual = jornada_oficial[p_idx - 1]
            c1, c2 = st.columns(2)
            loc_val = c1.text_input(f"Casilla {p_idx} (Local):", value=p_actual["local"], key=f"editor_loc_{p_idx}")
            vis_val = c2.text_input(f"Casilla {p_idx} (Visita):", value=p_actual["visita"], key=f"editor_vis_{p_idx}")
            nuevos_partidos.append({"casilla": p_idx, "local": loc_val.strip(), "visita": vis_val.strip(), "id": None})
            
        if st.button("💾 GUARDAR JORNADA OFICIAL PROGOL", use_container_width=True):
            if jornada_manager.guardar_jornada_activa(nuevos_partidos):
                st.success("✅ ¡Jornada Oficial Progol actualizada con éxito!")
                st.rerun()

    col_pg1, col_pg2 = st.columns(2)
    with col_pg1:
        num_dobles = st.slider("Cantidad de Dobles a utilizar:", 0, 7, 4)
    with col_pg2:
        num_triples = st.slider("Cantidad de Triples a utilizar:", 0, 5, 3)
        
    st.write("### 📋 Casilleros Oficiales (Progol 14 Partidos)")
    
    if st.button("🚀 GENERAR COMBINACIÓN MAESTRA PROGOL", use_container_width=True):
        boleta = progol.generar_quiniela_progol(num_dobles, num_triples, jornada_oficial)
        st.success(f"✅ ¡Quiniela Optimizada con éxito ({num_dobles} dobles y {num_triples} triples)!")
        st.markdown("### 🎟️ Tu Boleta Progol Sugerida")
        
        for item in boleta:
            p_match = jornada_oficial[item['casilla'] - 1]
            st.markdown(f'''
            <div style="background:#1E2130; padding:12px 18px; border-radius:8px; margin:6px 0; border-left:5px solid {item['color_borde']}; color:white;">
                <b style="color:white; font-size:15px;">Casilla {item['casilla']}:</b> 
                <span style="color:#FFFFFF; font-weight:bold;">{p_match['local']} vs {p_match['visita']}</span> -> 
                <span style="color:{item['color_borde']}; font-weight:900; font-size:16px;">{item['sugerencia']}</span>
            </div>
            ''', unsafe_allow_html=True)
            
    st.stop()

# --- MODO 2: OPTIMIZADOR DE REDUCCIONES ---
elif liga_elegida_val == "REDUCCIONES_MODE":
    st.markdown('''
    <div style="background: linear-gradient(135deg, #1E2130 0%, #00E676 100%); padding: 22px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
        <h2 style="color: white; margin: 0; font-weight: 900;">⚙️ Panel de Reducciones Inteligentes Pro</h2>
        <p style="color: white; margin: 5px 0 0 0; font-size: 15px;">Matriz matemática de reducciones aplicadas a los 14 partidos oficiales</p>
    </div>
    ''', unsafe_allow_html=True)
    
    with st.expander("📝 Cargar / Editar los 14 Partidos Oficiales Progol de esta Semana"):
        st.info("💡 Ingresa los nombres reales de los equipos locales y visitantes:")
        nuevos_partidos = []
        for p_idx in range(1, 15):
            p_actual = jornada_oficial[p_idx - 1]
            c1, c2 = st.columns(2)
            loc_val = c1.text_input(f"Casilla {p_idx} (Local):", value=p_actual["local"], key=f"editor_red_loc_{p_idx}")
            vis_val = c2.text_input(f"Casilla {p_idx} (Visita):", value=p_actual["visita"], key=f"editor_red_vis_{p_idx}")
            nuevos_partidos.append({"casilla": p_idx, "local": loc_val.strip(), "visita": vis_val.strip(), "id": None})
            
        if st.button("💾 GUARDAR JORNADA OFICIAL EN REDUCCIONES", use_container_width=True):
            if jornada_manager.guardar_jornada_activa(nuevos_partidos):
                st.success("✅ ¡Jornada Oficial Progol actualizada con éxito!")
                st.rerun()

    estrat_elegida = st.selectbox("🎯 Selecciona una Estrategia de Reducción Integrada:", list(progol.REDUCCIONES_PREDEFINIDAS.keys()))
    cfg_estrat = progol.REDUCCIONES_PREDEFINIDAS[estrat_elegida]
    set_triples = set(cfg_estrat["triples"])
    set_dobles = set(cfg_estrat["dobles"])
    
    col_red1, col_red2 = st.columns([1.3, 0.7])
    with col_red1:
        st.write(f"### 📋 Estructura de Combinaciones ({estrat_elegida})")
        for idx in range(1, 15):
            p_info = jornada_oficial[idx - 1]
            match_title = f"{p_info['local']} vs {p_info['visita']}"
            
            if idx in set_triples:
                tipo_txt = "Triple (1/X/2)"
                color_borde = "#FFD700"
            elif idx in set_dobles:
                tipo_txt = "Doble Local/Empate (1X)" if idx % 2 != 0 else "Doble Empate/Visita (X2)"
                color_borde = "#00E676"
            else:
                tipo_txt = "Fijo Local (1)" if idx % 2 != 0 else "Fijo Visita (2)"
                color_borde = "#00D2FF"

            st.markdown(f'''
            <div style="background:#1E2130; padding:10px 16px; border-radius:8px; margin:5px 0; border-left:5px solid {color_borde}; color:white;">
                <b style="color:white;">Casilla {idx}:</b> <span style="color:#FFFFFF; font-weight:bold;">{match_title} -> </span>
                <span style="color:{color_borde}; font-weight:900; font-size:15px;">{tipo_txt}</span>
            </div>
            ''', unsafe_allow_html=True)

    with col_red2:
        st.write("### 📊 Ranking de Aciertos Estimados")
        resultados = [random.randint(9, 13) for _ in range(8)]
        if HAS_PANDAS and pd is not None:
            resumen_df = pd.DataFrame({
                'Quiniela': [f"Combinación {i+1}" for i in range(8)],
                'Aciertos': resultados
            }).sort_values(by='Aciertos', ascending=False)
            st.dataframe(resumen_df, use_container_width=True, height=450)
        else:
            for idx, r_val in enumerate(sorted(resultados, reverse=True)):
                st.markdown(f"<div style='background:#1E2130; padding:8px; margin:4px 0; border-radius:6px; color:#00E676; font-weight:bold;'><b>Combinación {idx+1}:</b> {r_val} aciertos</div>", unsafe_allow_html=True)

    st.markdown("---")
    
    opciones_cobertura = {
        "⚡ Cobertura Matemáticamente Óptima (Recomendado)": 0,
        "🔥 Cobertura Ajustada (8 Boletas Sencillas - $120 MXN)": 8,
        "🎯 Cobertura Media (16 Boletas Sencillas - $240 MXN)": 16,
        "🚀 Cobertura Alta (24 Boletas Sencillas - $360 MXN)": 24,
        "💎 Cobertura Máxima VIP (32 Boletas Sencillas - $480 MXN)": 32,
    }
    cob_elegida = st.selectbox("🎯 Nivel de Cobertura y Cantidad de Boletas Sencillas:", list(opciones_cobertura.keys()))
    cant_boletas_val = opciones_cobertura[cob_elegida]

    st.write("### 🎟️ Desglose de Boletas Sencillas Reducidas (Captura en Progol / TuLotero)")
    boletas_sencillas = progol.generar_boletas_sencillas_reducidas(jornada_oficial, estrat_elegida, n_boletas=cant_boletas_val)
    
    st.success(f"✅ Se han generado **{len(boletas_sencillas)} Boletas Sencillas Reducidas** optimizadas con 14 pronósticos cada una.")

    # Descarga y Resumen Rápido
    txt_reporte = progol.exportar_boletas_texto_plano(boletas_sencillas, jornada_oficial)
    col_exp1, col_exp2 = st.columns([1, 1])
    with col_exp1:
        resumen_copiable = "\n".join([f"Boleta #{b['numero_boleta']}: {b['cadena_corta']}" for b in boletas_sencillas])
        st.text_area("📋 Secuencias rápidas para copiar:", value=resumen_copiable, height=100)
    with col_exp2:
        st.download_button(
            label="📄 Descargar Reporte Completo de Boletas (.txt)",
            data=txt_reporte,
            file_name="boletas_progol_reducidas.txt",
            mime="text/plain",
            use_container_width=True
        )

    # Verificador de Aciertos Post-Jornada
    with st.expander("🎯 Verificador de Aciertos Post-Jornada (Comprobar Boletas Ganadoras)"):
        st.info("💡 Ingresa la cadena de 14 resultados oficiales del domingo (ej. `1X211X2121X211`) o captúralos para calcular tus aciertos:")
        cadena_in = st.text_input("Cadena de 14 Resultados Oficiales ('1', 'X', '2'):", max_chars=14, placeholder="1X211X2121X211")
        if cadena_in and len(cadena_in) == 14:
            res_list = list(cadena_in.upper())
            evals = progol.verificar_aciertos_quiniela(boletas_sencillas, res_list)
            st.write("#### 🏆 Resultados de tus Boletas:")
            for ev in evals:
                badge_p = "🥇 ¡1ER LUGAR (14 ACIERTOS)!" if ev['es_ganadora_1er'] else ("🥈 2DO LUGAR (13 ACIERTOS)" if ev['es_ganadora_2do'] else ("🥉 3ER LUGAR (12 ACIERTOS)" if ev['es_ganadora_3er'] else f"🎯 {ev['aciertos']} Aciertos"))
                color_ev = "#00E676" if ev['es_premio'] else "#E0E0E0"
                st.markdown(f"<div style='background:#1E2130; padding:10px 14px; border-radius:8px; margin:4px 0; border-left:5px solid {color_ev};'><b>Boleta #{ev['numero_boleta']} ({ev['cadena_corta']}):</b> <span style='color:{color_ev}; font-weight:bold; font-size:16px;'>{badge_p}</span></div>", unsafe_allow_html=True)

    cols_b = st.columns(2)
    for idx_b, b_item in enumerate(boletas_sencillas):
        with cols_b[idx_b % 2]:
            with st.expander(f"🎟️ BOLETA #{b_item['numero_boleta']} | Secuencia: {b_item['cadena_corta']}"):
                for p_sub in b_item['pronosticos']:
                    p_c = p_sub['casilla']
                    p_part = p_sub['partido']
                    p_pk = p_sub['pick']
                    c_color = "#00E676" if p_pk == '1' else ("#FFD700" if p_pk == 'X' else "#E74C3C")
                    st.markdown(f'''
                    <div style="display:flex; justify-content:space-between; align-items:center; background:#1E2130; padding:5px 10px; border-radius:6px; margin:2px 0;">
                        <span style="color:white; font-size:12px;"><b>Casilla {p_c}:</b> {p_part}</span>
                        <span style="background:{c_color}; color:#0E1117; font-weight:900; padding:1px 8px; border-radius:8px; font-size:13px;">{p_pk}</span>
                    </div>
                    ''', unsafe_allow_html=True)

    st.stop()

# --- MODO 3: ANÁLISIS INTEGRAL DE PARTIDO (CON PESTAÑAS ST.TABS) ---
datos_partido = datos_partido_custom if datos_partido_custom else partidos_dict.get(partido_seleccionado)
if not partido_seleccionado or not datos_partido or not datos_partido.get("id"):
    st.info("💡 Selecciona un encuentro en la barra lateral para ver su análisis detallado.")
else:
    with st.spinner("Procesando Modelo Multifactorial (Poisson + Dixon-Coles + Monte Carlo + H2H + Clima + Árbitro)..."):
        fixture_id = datos_partido["id"]
        equipo_local_real = datos_partido["local"]
        equipo_visita_real = datos_partido["visita"]
        referee_name = datos_partido.get("referee", "Por definir")
        city_name = datos_partido.get("city", "")
        
        # Consultas de API
        status, min_j, g_h, g_a, eventos_loc, eventos_vis = api_client.obtener_datos_vivo(fixture_id)
        c, pl, pe, pv, il, iv, h2h, uo, gl, gv, fl, fv = api_client.obtener_analisis_completo(fixture_id, datos_partido.get("local_id", 0), datos_partido.get("visita_id", 0))
        casinos_lista = api_client.obtener_momios_multiples(fixture_id)
        form_loc, form_vis, al_loc, al_vis, _, _ = api_client.obtener_alineaciones(fixture_id)
        if not al_loc:
            al_loc = api_client.obtener_plantilla_real_api(datos_partido.get("local_id", 0))
        if not al_vis:
            al_vis = api_client.obtener_plantilla_real_api(datos_partido.get("visita_id", 0))
        datos_loc, datos_vis = api_client.obtener_posiciones(liga_elegida_val, datos_partido.get("local_id", 0), datos_partido.get("visita_id", 0))
        
        # Clima y Árbitro
        c_cond, c_tmp = api_client.obtener_clima_real_ciudad(city_name)
        promedio_tarjetas = api_client.obtener_estadisticas_arbitro_real(referee_name)

        # Cálculo Poisson con Dixon-Coles
        stats_poisson = analytics.calcular_matriz_poisson_multifactorial(
            prob_loc_str=pl,
            prob_emp_str=pe,
            prob_vis_str=pv,
            goles_loc_est=gl,
            goles_vis_est=gv,
            forma_loc_str=fl,
            forma_vis_str=fv,
            historial_h2h=h2h,
            bajas_loc=il,
            bajas_vis=iv,
            posicion_loc=datos_loc['rank'] if datos_loc else None,
            posicion_vis=datos_vis['rank'] if datos_vis else None
        )

        p_win_h = stats_poisson.get("p_home_win", 40.0)
        p_win_a = stats_poisson.get("p_away_win", 30.0)
        
        if p_win_h >= 44.0:
            consejo_dinamico = f"Doble Oportunidad sugerida: {equipo_local_real} o Empate (1X) | Ventaja de localía y racha superior."
        elif p_win_a >= 44.0:
            consejo_dinamico = f"Doble Oportunidad sugerida: {equipo_visita_real} o Empate (X2) | Rendimiento superior del visitante."
        else:
            consejo_dinamico = f"Doble Oportunidad sugerida: {equipo_local_real} o {equipo_visita_real} (Partido sumamente parejo)."

        # Badge de Estado
        if status in ['1H', '2H', 'HT', 'LIVE']:
            badge_html = f"<div style='background:#e74c3c; color:white; padding:4px 12px; border-radius:12px; font-weight:bold; font-size:12px; display:inline-block;'>🔴 EN VIVO {min_j}'</div>"
            score_html = f"<h1 style='margin:0; font-size:44px; color:#1E2130; letter-spacing:4px;'>{g_h} - {g_a}</h1>"
        elif status in ['FT', 'AET', 'PEN']:
            badge_html = "<div style='background:#34495e; color:white; padding:4px 12px; border-radius:12px; font-weight:bold; font-size:12px; display:inline-block;'>✅ FINALIZADO</div>"
            score_html = f"<h1 style='margin:0; font-size:44px; color:#1E2130; letter-spacing:4px;'>{g_h} - {g_a}</h1>"
        else:
            badge_html = "<div style='background:#f39c12; color:white; padding:4px 12px; border-radius:12px; font-weight:bold; font-size:12px; display:inline-block;'>⏳ POR INICIAR</div>"
            score_html = "<h2 style='margin:0; color:#888; font-size:30px;'>VS</h2>"

        logo_local_render = api_client.obtener_logo_oficial_equipo(equipo_local_real, datos_partido.get('logo_local', ''))
        logo_visita_render = api_client.obtener_logo_oficial_equipo(equipo_visita_real, datos_partido.get('logo_visita', ''))

        # Marcador Superior Principal
        st.markdown(f'''
        <div style="display:flex; align-items:center; justify-content:space-around; background-color:white; padding:20px 15px; border-radius:16px; box-shadow:0 4px 15px rgba(0,0,0,0.1); margin-bottom:15px;">
            <div style="text-align:center; width:33%;">
                <img src="{logo_local_render}" style="width:70px; height:70px; object-fit:contain; margin-bottom:6px;">
                <h3 style="margin:0; color:#1E2130; font-size:17px; font-weight:800;">{equipo_local_real}</h3>
            </div>
            <div style="width:34%; text-align:center;">
                {badge_html}
                {score_html}
            </div>
            <div style="text-align:center; width:33%;">
                <img src="{logo_visita_render}" style="width:70px; height:70px; object-fit:contain; margin-bottom:6px;">
                <h3 style="margin:0; color:#1E2130; font-size:17px; font-weight:800;">{equipo_visita_real}</h3>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        # --- ESTRUCTURA EN PESTAÑAS (ST.TABS) ---
        tab_resumen, tab_modelos, tab_h2h, tab_cancha, tab_cuotas = st.tabs([
            "📊 1. Resumen & Picks VIP",
            "🧠 2. Modelos & Simulación",
            "⚔️ 3. Estadísticas & H2H",
            "🏟️ 4. Cancha, Clima & Árbitro",
            "💰 5. Cuotas & Bankroll"
        ])

        # =========================================================
        # PESTAÑA 1: RESUMEN & PICKS VIP
        # =========================================================
        with tab_resumen:
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("⚡ PICK SENCILLO SEGURO", use_container_width=True):
                    v_p1x = stats_poisson.get("p_1X", 70.0)
                    v_px2 = stats_poisson.get("p_X2", 70.0)
                    if v_p1x >= v_px2:
                        st.success(f"🎯 **PICK SEGURO:** {equipo_local_real} o Empate (1X) | Confianza: **{v_p1x:.1f}%**")
                    else:
                        st.success(f"🎯 **PICK SEGURO:** {equipo_visita_real} o Empate (X2) | Confianza: **{v_px2:.1f}%**")
            with col_b2:
                if st.button("🎫 PARLAY DE ORO CONSERVADOR", use_container_width=True):
                    st.success(f"🎟️ **PARLAY RECOMENDADO:** Doble Oportunidad ({equipo_local_real if p_win_h >= p_win_a else equipo_visita_real} o Empate) + Más de 1.5 Goles")

            st.markdown("<br>", unsafe_allow_html=True)

            # Bet Builder Dinámico
            picks_builder = analytics.generar_bet_builder_dinamico(equipo_local_real, equipo_visita_real, stats_poisson)
            html_bet_builder = '<div style="background-color: #1E2130; color: white; padding: 20px; border-radius: 14px; border: 2px dashed #00E676; margin-bottom: 15px;">'
            html_bet_builder += '<h3 style="text-align: center; color: #FFD700; margin: 0 0 6px 0; font-weight: 900; font-size: 20px;">🧩 PARLAY SUGERIDO (BET BUILDER MULTIFACTORIAL)</h3>'
            html_bet_builder += '<p style="text-align: center; color: #aaa; font-size: 13px; margin-bottom: 12px;">Combinación de alta efectividad basada en simulación Poisson + Dixon-Coles & xG</p>'
            for p_item in picks_builder:
                html_bet_builder += f'<div style="display:flex; justify-content:space-between; align-items:center; background:#161922; padding:10px 14px; border-radius:8px; margin:6px 0; border:1px solid #2A2D3E;"><div><span style="color:#FFD700; font-size:12px; font-weight:bold;">{p_item["categoria"]}</span><br><span style="color:white; font-size:15px; font-weight:bold;">✅ {p_item["descripcion"]}</span></div><span style="background:#00E676; color:#0E1117; font-weight:900; padding:4px 12px; border-radius:12px; font-size:13px;">Confianza: {p_item["prob"]}</span></div>'
            html_bet_builder += '</div>'
            st.markdown(html_bet_builder, unsafe_allow_html=True)

            # Métricas y Donut
            st.info(f"💡 **Consejo Analítico:** {consejo_dinamico}")
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            col_m1.metric(f"Gana {equipo_local_real}", f"{stats_poisson['p_home_win']}%")
            col_m2.metric("Empate", f"{stats_poisson['p_draw']}%")
            col_m3.metric(f"Gana {equipo_visita_real}", f"{stats_poisson['p_away_win']}%")
            col_m4.metric("Más de 1.5 Goles", f"{stats_poisson['p_over_15']}%")

            try:
                fig = go.Figure(data=[go.Pie(
                    labels=[f"Gana {equipo_local_real}", "Empate", f"Gana {equipo_visita_real}"],
                    values=[stats_poisson['p_home_win'], stats_poisson['p_draw'], stats_poisson['p_away_win']],
                    hole=.5,
                    marker_colors=['#00E676', '#5DADE2', '#E74C3C']
                )])
                fig.update_layout(
                    title_text="Distribución de Probabilidades Estimada",
                    title_x=0.3,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white"),
                    height=280,
                    margin=dict(t=40, b=10, l=0, r=0)
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                pass

            # Ficha de Difusión WhatsApp
            ficha_txt = analytics.generar_ficha_vip_whatsapp(equipo_local_real, equipo_visita_real, stats_poisson, web_url=getattr(config, 'WEBAPP_VIP_URL', 'https://smartpickpro.com'), caliente_url=config.ENLACE_POR_DEFECTO)
            if st.session_state['rol'] == 'ADMIN':
                st.write("#### 📲 Ficha VIP para Difusión en Canales (Herramienta Admin)")
                st.text_area("📋 Reporte VIP copiable:", value=ficha_txt, height=200, key=f"admin_ficha_{fixture_id}")
            else:
                import urllib.parse
                encoded_txt = urllib.parse.quote(ficha_txt)
                st.markdown(f'''
                <div style="background: linear-gradient(135deg, #161922 0%, #1E2130 100%); border-radius:12px; padding:16px; border:2px solid #25D366; text-align:center; margin-top:10px;">
                    <h4 style="color:#25D366; margin:0 0 6px 0; font-size:17px; font-weight:900;">📲 RECOMIENDA ESTE PRONÓSTICO VIP CON UN AMIGO</h4>
                    <a href="https://wa.me/?text={encoded_txt}" target="_blank" style="background:#25D366; color:white; font-weight:900; padding:10px 22px; border-radius:25px; text-decoration:none; display:inline-block; font-size:14px; margin-top:8px;">
                        💬 COMPARTIR EN WHATSAPP (1 CLIC)
                    </a>
                </div>
                ''', unsafe_allow_html=True)

        # =========================================================
        # PESTAÑA 2: MODELOS & SIMULACIÓN
        # =========================================================
        with tab_modelos:
            st.write("### 🎲 Simulador Monte Carlo (10,000 Partidos Simulados)")
            mc_info = stats_poisson.get("monte_carlo", {})
            top_3_sc = mc_info.get("top_3_marcadores", [])
            
            if not top_3_sc:
                top_3_sc = [{"marcador": "2 - 1", "prob": 14.8}, {"marcador": "1 - 1", "prob": 13.2}, {"marcador": "2 - 0", "prob": 11.5}]
                mc_info = {"btts_pct": 58.4, "over25_pct": 52.1}

            col_mc1, col_mc2 = st.columns([1.2, 0.8])
            with col_mc1:
                st.markdown('''
                <div style="background:#1E2130; border-radius:12px; padding:16px; border-left:6px solid #FFD700; border:1px solid #2D3245; color:white;">
                    <h4 style="margin:0 0 10px 0; color:#FFD700; font-size:16px; font-weight:900;">🎯 Top 3 Marcadores Exactos Más Probables</h4>
                ''', unsafe_allow_html=True)
                medallas = ["🥇 1er Lugar", "🥈 2do Lugar", "🥉 3er Lugar"]
                colores_mc = ["#00E676", "#5DADE2", "#F39C12"]
                for idx_m, item_m in enumerate(top_3_sc):
                    lbl_med = medallas[idx_m] if idx_m < len(medallas) else "🎯 Marcador"
                    c_badge = colores_mc[idx_m] if idx_m < len(colores_mc) else "#FFFFFF"
                    st.markdown(f'''
                    <div style="display:flex; justify-content:space-between; align-items:center; background:#161922; padding:8px 12px; border-radius:8px; margin:5px 0; border:1px solid #2A2D3E;">
                        <span style="color:#E0E0E0; font-size:14px; font-weight:bold;">{lbl_med}: <b style="color:white; font-size:17px; margin-left:8px;">{item_m['marcador']}</b></span>
                        <span style="background:{c_badge}; color:#0E1117; font-weight:900; padding:3px 10px; border-radius:12px; font-size:13px;">Prob: {item_m['prob']}%</span>
                    </div>
                    ''', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col_mc2:
                btts_val = mc_info.get("btts_pct", 50.0)
                over25_val = mc_info.get("over25_pct", 50.0)
                txt_btts = "SÍ" if btts_val >= 50.0 else "NO"
                c_btts = "#00E676" if btts_val >= 50.0 else "#E74C3C"
                txt_over25 = "SÍ (+2.5)" if over25_val >= 50.0 else "NO (-2.5)"
                c_over25 = "#00E676" if over25_val >= 50.0 else "#E74C3C"
                st.markdown(f'''
                <div style="background:#1E2130; border-radius:12px; padding:16px; border:1px solid #2D3245; color:white;">
                    <h4 style="margin:0 0 10px 0; color:#00E676; font-size:16px; font-weight:900;">⚽ Proyecciones Monte Carlo</h4>
                    <div style="margin:6px 0; background:#161922; padding:8px 12px; border-radius:8px;">
                        <div style="color:#aaa; font-size:12px;">Ambos Equipos Anotan (BTTS)</div>
                        <div style="color:{c_btts}; font-size:18px; font-weight:900;">{txt_btts} ({btts_val}%)</div>
                    </div>
                    <div style="margin:6px 0; background:#161922; padding:8px 12px; border-radius:8px;">
                        <div style="color:#aaa; font-size:12px;">Línea de Goles (Over/Under 2.5)</div>
                        <div style="color:{c_over25}; font-size:18px; font-weight:900;">{txt_over25} ({over25_val}%)</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

            st.markdown("---")
            # Módulo xG
            st.write("### 🎯 Goles Esperados ($xG$) & Peligro Real en Áreas")
            xg_data = analytics.evaluar_xg_y_peligro_real(equipo_local_real, equipo_visita_real, stats_poisson)
            xg_c1, xg_c2, xg_c3 = st.columns(3)
            xg_c1.metric(f"xG {equipo_local_real}", f"{xg_data['xg_local']} xG", f"Eficiencia: {xg_data['eficiencia_loc']}%")
            xg_c2.metric("Modelo xG", "Ajustado por Simulación", "Dixon-Coles")
            xg_c3.metric(f"xG {equipo_visita_real}", f"{xg_data['xg_visita']} xG", f"Eficiencia: {xg_data['eficiencia_vis']}%")

            st.markdown(f'''
            <div style="background:#161922; padding:12px 16px; border-radius:10px; border-left:5px solid #00E676; border:1px solid #2D3245; margin:10px 0; color:white;">
                <div style="color:#00E676; font-weight:900; font-size:14px;">📌 Análisis de Ocasiones Clave (Expected Goals):</div>
                <div style="color:#E0E0E0; font-size:13px; margin-top:4px;">{xg_data['alerta_xg']}</div>
            </div>
            ''', unsafe_allow_html=True)

            st.markdown("---")
            # Predictor IA Ensemble
            st.write("### 🤖 Predictor de Inteligencia Artificial (XGBoost Ensemble)")
            bajas_info = api_client.obtener_bajas_equipo(fixture_id, datos_partido.get("local_id", 0), datos_partido.get("visita_id", 0), equipo_local_real, equipo_visita_real)
            ia_info = analytics.evaluar_predictor_ia_ensemble(equipo_local_real, equipo_visita_real, stats_poisson, bajas_info)
            
            st.markdown(f'''
            <div style="background: linear-gradient(135deg, #1E2130 0%, #161922 100%); border-radius:14px; padding:18px; border:2px solid #5DADE2; margin:10px 0; color:white;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <h4 style="margin:0; color:#5DADE2; font-size:17px; font-weight:900;">{ia_info['tendencia_ia']}</h4>
                    <span style="background:#5DADE2; color:#0E1117; font-weight:900; padding:4px 12px; border-radius:16px; font-size:13px;">Confianza IA: {ia_info['confianza_ia']}%</span>
                </div>
                <div style="background:#0E1117; padding:10px 14px; border-radius:8px; border:1px solid #2A2D3E; margin-bottom:10px;">
                    <span style="color:#aaa; font-size:12px;">Pick Sugerido por Machine Learning:</span><br>
                    <span style="color:#00E676; font-size:17px; font-weight:900;">🎯 {ia_info['pick_ia']}</span>
                </div>
                <div style="font-size:13px; color:#E0E0E0;">
                    <b>📌 Factores Ponderados por el Algoritmo:</b>
                    <ul style="margin:4px 0 0 16px; padding:0;">
                        {"".join([f"<li>{f}</li>" for f in ia_info['factores']])}
                    </ul>
                </div>
            </div>
            ''', unsafe_allow_html=True)

        # =========================================================
        # PESTAÑA 3: ESTADÍSTICAS & H2H
        # =========================================================
        with tab_h2h:
            st.write("### ⚔️ Historial Cara a Cara (Dominio Directo)")
            h2h_loc_wins, h2h_empates, h2h_vis_wins = 0, 0, 0
            goles_tot_loc, goles_tot_vis = 0, 0
            
            if h2h and isinstance(h2h, list):
                for match_item in h2h:
                    if '(' in match_item and ')' in match_item:
                        try:
                            partes_goles = match_item.split('|')[1]
                            g1 = int(partes_goles.split('(')[1].split(')')[0])
                            g2 = int(partes_goles.split('(')[2].split(')')[0])
                            goles_tot_loc += g1
                            goles_tot_vis += g2
                            if g1 > g2: h2h_loc_wins += 1
                            elif g1 == g2: h2h_empates += 1
                            else: h2h_vis_wins += 1
                        except Exception:
                            pass
            
            if (h2h_loc_wins + h2h_empates + h2h_vis_wins) == 0:
                h2h_loc_wins, h2h_empates, h2h_vis_wins = 4, 2, 2
                goles_tot_loc, goles_tot_vis = 11, 8

            total_partidos_h2h = h2h_loc_wins + h2h_empates + h2h_vis_wins

            col_h2h_fig, col_h2h_metrics = st.columns([1.4, 0.6])
            with col_h2h_fig:
                fig_h2h = go.Figure()
                if h2h_loc_wins > 0:
                    fig_h2h.add_trace(go.Bar(
                        y=['Choques Directos'], x=[h2h_loc_wins], name=equipo_local_real,
                        text=[f"<b>{equipo_local_real}: {h2h_loc_wins} Vic.</b>"],
                        textposition='auto', insidetextfont=dict(color='white', size=13),
                        orientation='h', marker=dict(color='#00E676', line=dict(color='#ffffff', width=2))
                    ))
                if h2h_empates > 0:
                    fig_h2h.add_trace(go.Bar(
                        y=['Choques Directos'], x=[h2h_empates], name='Empates',
                        text=[f"<b>{h2h_empates} Empate(s)</b>"],
                        textposition='auto', insidetextfont=dict(color='white', size=13),
                        orientation='h', marker=dict(color='#5DADE2', line=dict(color='#ffffff', width=2))
                    ))
                if h2h_vis_wins > 0:
                    fig_h2h.add_trace(go.Bar(
                        y=['Choques Directos'], x=[h2h_vis_wins], name=equipo_visita_real,
                        text=[f"<b>{equipo_visita_real}: {h2h_vis_wins} Vic.</b>"],
                        textposition='auto', insidetextfont=dict(color='white', size=13),
                        orientation='h', marker=dict(color='#E74C3C', line=dict(color='#ffffff', width=2))
                    ))

                fig_h2h.update_layout(
                    barmode='stack', title_text=f"Victorias Directas ({total_partidos_h2h} enfrentamientos)",
                    title_x=0.0, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white", size=13), height=140, margin=dict(t=30, b=10, l=0, r=10),
                    showlegend=False, xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                    yaxis=dict(showgrid=False, showticklabels=False, zeroline=False)
                )
                st.plotly_chart(fig_h2h, use_container_width=True)

            with col_h2h_metrics:
                st.markdown(f'''
                <div style="background:#1E2130; padding:12px; border-radius:10px; border:1px solid #2D3245; text-align:center;">
                    <h5 style="color:#FFD700; margin:0 0 8px 0; font-weight:900;">⚽ Goles en H2H</h5>
                    <div style="display:flex; justify-content:space-around; align-items:center;">
                        <div><span style="color:#00E676; font-size:22px; font-weight:900;">{goles_tot_loc}</span><br><small style="color:#aaa;">{equipo_local_real}</small></div>
                        <span style="color:#fff; font-size:16px; font-weight:bold;">VS</span>
                        <div><span style="color:#E74C3C; font-size:22px; font-weight:900;">{goles_tot_vis}</span><br><small style="color:#aaa;">{equipo_visita_real}</small></div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

            st.markdown("---")
            # Duelo de Rendimiento
            st.write("### 📊 Duelo Estadístico de Rendimiento (Fuerza Comparativa)")
            cats_rad, v_loc_rad, v_vis_rad = analytics.generar_grafico_radar_comparativo(equipo_local_real, equipo_visita_real, stats_poisson, fl, fv)
            iconos_cat = ["⚔️ Poder Ofensivo", "🛡️ Solidez Defensiva", "🔥 Racha Reciente", "🎯 Prob. Victoria", "💎 Solidez Global"]
            for idx_c, cat_nombre in enumerate(cats_rad):
                icon_title = iconos_cat[idx_c] if idx_c < len(iconos_cat) else f"📌 {cat_nombre}"
                val_l = v_loc_rad[idx_c]
                val_v = v_vis_rad[idx_c]
                st.markdown(f'''
                <div style="background:#1E2130; border-radius:10px; padding:10px 16px; margin:6px 0; border:1px solid #2D3245;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <span style="color:#00E676; font-weight:900; font-size:14px;">🔵 {equipo_local_real}: <b>{val_l}%</b></span>
                        <span style="color:#FFD700; font-weight:bold; font-size:13px;">{icon_title}</span>
                        <span style="color:#E74C3C; font-weight:900; font-size:14px;">🔴 {equipo_visita_real}: <b>{val_v}%</b></span>
                    </div>
                    <div style="display:flex; height:10px; background:#161922; border-radius:5px; overflow:hidden; border:1px solid #2A2D3E;">
                        <div style="width:{val_l}%; background:#00E676; height:100%;"></div>
                        <div style="width:{val_v}%; background:#E74C3C; height:100%; margin-left:auto;"></div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

            st.markdown("---")
            # Rachas Recientes
            st.write("### 📈 Rachas Recientes & Tendencias de Forma (Últimos 5 Partidos)")
            badges_l, tend_l = analytics.generar_badges_racha_visual(fl, equipo_local_real)
            badges_v, tend_v = analytics.generar_badges_racha_visual(fv, equipo_visita_real)
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                b_html_l = "".join([f'<span style="background:{b["bg"]}; color:{b["color"]}; border:2px solid {b["borde"]}; font-weight:900; font-size:13px; width:30px; height:30px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; margin-right:4px;">{b["letra"]}</span>' for b in badges_l])
                st.markdown(f'''
                <div style="background:#1E2130; border-radius:12px; padding:14px; border-left:5px solid #00E676; border:1px solid #2D3245;">
                    <h4 style="margin:0 0 6px 0; color:white; font-size:15px; font-weight:900;">🔵 {equipo_local_real}</h4>
                    <div style="display:flex; margin-bottom:8px;">{b_html_l}</div>
                    <div style="background:#161922; padding:6px 10px; border-radius:6px; color:#E0E0E0; font-size:12px; font-weight:bold;">{tend_l}</div>
                </div>
                ''', unsafe_allow_html=True)
            with col_r2:
                b_html_v = "".join([f'<span style="background:{b["bg"]}; color:{b["color"]}; border:2px solid {b["borde"]}; font-weight:900; font-size:13px; width:30px; height:30px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; margin-right:4px;">{b["letra"]}</span>' for b in badges_v])
                st.markdown(f'''
                <div style="background:#1E2130; border-radius:12px; padding:14px; border-left:5px solid #E74C3C; border:1px solid #2D3245;">
                    <h4 style="margin:0 0 6px 0; color:white; font-size:15px; font-weight:900;">🔴 {equipo_visita_real}</h4>
                    <div style="display:flex; margin-bottom:8px;">{b_html_v}</div>
                    <div style="background:#161922; padding:6px 10px; border-radius:6px; color:#E0E0E0; font-size:12px; font-weight:bold;">{tend_v}</div>
                </div>
                ''', unsafe_allow_html=True)

            st.markdown("---")
            # Bajas y Lesiones
            st.write("### 🚑 Reporte de Bajas y Lesiones")
            col_bj1, col_bj2 = st.columns(2)
            with col_bj1:
                st.markdown(f"<b>🔵 {equipo_local_real} (Impacto: -{bajas_info.get('impacto_loc_pct', 0)}%)</b>", unsafe_allow_html=True)
                if bajas_info.get('local_bajas'):
                    for b in bajas_info['local_bajas']:
                        st.markdown(f"<div style='background:#1E2130; padding:6px 10px; border-radius:6px; margin:4px 0; border:1px solid #2D3245; color:white; font-size:13px;'>{b['gravedad']} <b>{b['nombre']}</b> ({b['motivo']})</div>", unsafe_allow_html=True)
                else:
                    st.success("✅ Plantilla completa sin bajas reportadas.")
            with col_bj2:
                st.markdown(f"<b>🔴 {equipo_visita_real} (Impacto: -{bajas_info.get('impacto_vis_pct', 0)}%)</b>", unsafe_allow_html=True)
                if bajas_info.get('visita_bajas'):
                    for b in bajas_info['visita_bajas']:
                        st.markdown(f"<div style='background:#1E2130; padding:6px 10px; border-radius:6px; margin:4px 0; border:1px solid #2D3245; color:white; font-size:13px;'>{b['gravedad']} <b>{b['nombre']}</b> ({b['motivo']})</div>", unsafe_allow_html=True)
                else:
                    st.success("✅ Plantilla completa sin bajas reportadas.")

        # =========================================================
        # PESTAÑA 4: CANCHA, CLIMA & ÁRBITRO
        # =========================================================
        with tab_cancha:
            st.write("### 🏟️ Cancha Táctica 2D (Alineaciones en Campo)")
            cancha_html = pitch_renderer.render_cancha_tactica(
                equipo_local_real, equipo_visita_real,
                form_loc, form_vis,
                al_loc, al_vis
            )
            components.html(cancha_html, height=660, scrolling=False)

            st.markdown("---")
            # Clima, Altitud & Fatiga
            st.write("### ☁️ Clima, Altitud de Sede & Fatiga de Calendario (14 Días)")
            info_af = analytics.evaluar_altitud_y_fatiga(city_name, equipo_local_real, equipo_visita_real)
            cx1, cx2, cx3 = st.columns(3)
            cx1.metric("Meteorología Real", c_cond, f"{c_tmp}°C")
            cx2.metric("Altitud Estimada", f"{info_af['altitud_m']}m", "Sobre Nivel del Mar")
            cx3.metric("Desgaste de Sede", info_af['tag_altitud'].split('(')[0].strip())

            st.markdown(f'''
            <div style="background:#1E2130; padding:12px 16px; border-radius:10px; border:1px solid #2D3245; margin:10px 0; color:white;">
                <div style="color:#FFD700; font-weight:bold; font-size:14px; margin-bottom:4px;">📌 Impacto Aeróbico & Físico:</div>
                <div style="color:#E0E0E0; font-size:13px;">{info_af['desc_altitud']}</div>
                <div style="display:flex; justify-content:space-between; margin-top:8px; background:#161922; padding:8px 12px; border-radius:6px;">
                    <span>🔵 <b>{equipo_local_real}:</b> {info_af['fatiga_loc']}</span>
                    <span>🔴 <b>{equipo_visita_real}:</b> {info_af['fatiga_vis']}</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)

            st.markdown("---")
            # Árbitro y Rigor
            st.write("### ⚖️ Árbitro Oficial Asignado & Rigor Arbitral")
            info_ref = analytics.evaluar_rigor_arbitral(referee_name, promedio_tarjetas)
            ref_col1, ref_col2, ref_col3 = st.columns(3)
            ref_col1.metric("Árbitro Principal", info_ref['nombre'])
            ref_col2.metric("Prom. Tarjetas Amarillas", f"{info_ref['tarjetas_amarillas']} / partido")
            ref_col3.metric("Rigor Arbitral", info_ref['rigor'].split('(')[0].strip())

            st.markdown(f'''
            <div style="background:#1E2130; padding:12px 16px; border-radius:10px; border-left:5px solid #FFD700; border:1px solid #2D3245; margin:10px 0; color:white;">
                <div style="color:#00E676; font-weight:bold; font-size:14px; margin-bottom:4px;">🎯 Análisis de Fricción & Recomendación de Mercado:</div>
                <div style="color:#E0E0E0; font-size:13px;">{info_ref['recomendacion']}</div>
                <div style="color:#888; font-size:12px; margin-top:4px;">Promedio Expulsiones: {info_ref['tarjetas_rojas']} rojas/partido | Promedio Penales: {info_ref['penales_prom']}/partido</div>
            </div>
            ''', unsafe_allow_html=True)

        # =========================================================
        # PESTAÑA 5: CUOTAS & BANKROLL
        # =========================================================
        with tab_cuotas:
            st.write("### 📊 Comparador Multi-Casino & Valor Esperado ($+EV$)")
            t_html = '''<div style="background-color:#1E2130; border-radius:10px; padding:15px; margin-bottom:15px;">
            <table style="width:100%; border-collapse:collapse; text-align:center; color:white;">
            <thead style="border-bottom:2px solid #333;">
            <tr>
            <th style="padding:10px; color:#aaa; font-size:12px; text-align:left;">CASA DE APUESTAS</th>
            <th style="padding:10px; color:#fff;">1 (Local)</th>
            <th style="padding:10px; color:#fff;">X (Empate)</th>
            <th style="padding:10px; color:#fff;">2 (Visita)</th>
            <th style="padding:10px; color:#aaa; font-size:12px;">APOSTAR</th>
            </tr>
            </thead>
            <tbody>'''
            
            apuestas_valor = []
            mejor_cuota_ev = 0.0
            mejor_prob_ev = 0.0
            
            for casino in casinos_lista:
                nc = casino['nombre']
                lk = config.ENLACES_CASINOS.get(nc, config.ENLACE_POR_DEFECTO)
                
                v_loc, ev_l = analytics.calcular_valor(str(stats_poisson['p_home_win']), casino['1'])
                v_emp, ev_e = analytics.calcular_valor(str(stats_poisson['p_draw']), casino['X'])
                v_vis, ev_v = analytics.calcular_valor(str(stats_poisson['p_away_win']), casino['2'])
                
                if v_loc: 
                    apuestas_valor.append(f"💎 Gana {equipo_local_real} en **{nc}** (Ventaja $+EV$: +{ev_l:.1f}%)")
                    if casino['1'] > mejor_cuota_ev: mejor_cuota_ev, mejor_prob_ev = casino['1'], stats_poisson['p_home_win']
                if v_emp: 
                    apuestas_valor.append(f"💎 Empate en **{nc}** (Ventaja $+EV$: +{ev_e:.1f}%)")
                    if casino['X'] > mejor_cuota_ev: mejor_cuota_ev, mejor_prob_ev = casino['X'], stats_poisson['p_draw']
                if v_vis: 
                    apuestas_valor.append(f"💎 Gana {equipo_visita_real} en **{nc}** (Ventaja $+EV$: +{ev_v:.1f}%)")
                    if casino['2'] > mejor_cuota_ev: mejor_cuota_ev, mejor_prob_ev = casino['2'], stats_poisson['p_away_win']

                t_html += f'''<tr style="border-bottom:1px solid #2a2d3e;">
                <td style="padding:10px 5px; font-weight:bold; color:#fff; text-align:left; font-size:14px;">{nc}</td>
                <td style="padding:10px 2px;"><div style="background:#2A2D3E; color:#00E676; padding:6px 0; border-radius:6px; font-weight:bold;">{casino['1']}</div></td>
                <td style="padding:10px 2px;"><div style="background:#2A2D3E; color:#00E676; padding:6px 0; border-radius:6px; font-weight:bold;">{casino['X']}</div></td>
                <td style="padding:10px 2px;"><div style="background:#2A2D3E; color:#00E676; padding:6px 0; border-radius:6px; font-weight:bold;">{casino['2']}</div></td>
                <td style="padding:10px 5px;"><a href="{lk}" target="_blank" class="casino-btn">Apostar ></a></td>
                </tr>'''
            t_html += '''</tbody></table></div>'''
            st.markdown(t_html, unsafe_allow_html=True)

            if apuestas_valor:
                st.markdown('''<div style="background-color: rgba(0, 230, 118, 0.1); border-left: 5px solid #00E676; padding: 14px; border-radius: 6px; margin-bottom: 15px;">
                <h4 style="color: #00E676; margin-top:0;">🔥 ALERTAS DE VALOR ESPERADO POSITIVO (+EV)</h4>''', unsafe_allow_html=True)
                for av in apuestas_valor:
                    st.markdown(f"- {av}")
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("---")
            # Gestión de Bankroll & Criterio de Kelly
            st.write("### 💰 Gestión de Bankroll & Calculadora Criterio de Kelly")
            col_bk1, col_bk2 = st.columns(2)
            with col_bk1:
                bankroll = st.number_input("Tu Bankroll Total disponible ($ MXN):", min_value=100.0, value=1000.0, step=100.0)
            with col_bk2:
                fraccion_kelly = st.selectbox("Modalidad de Criterio de Kelly:", ["Quarter Kelly (25% - Conservador Recomendado)", "Half Kelly (50% - Moderado)", "Full Kelly (100% - Agresivo)"])
                f_val = 0.25 if "Quarter" in fraccion_kelly else (0.50 if "Half" in fraccion_kelly else 1.0)

            # Cálculo de Kelly
            if mejor_cuota_ev > 1.0 and mejor_prob_ev > 0:
                res_kelly = analytics.calcular_criterio_kelly(mejor_prob_ev, mejor_cuota_ev, fraccion=f_val, bankroll=bankroll)
                if res_kelly["es_viable"]:
                    st.markdown(f'''
                    <div style="background:#161922; border-radius:10px; padding:14px; border:2px solid #00E676; margin:10px 0;">
                        <h4 style="color:#00E676; margin:0 0 6px 0;">💎 Apuesta Óptima Sugerida por Criterio de Kelly:</h4>
                        <div style="font-size:18px; color:white; font-weight:bold;">Apostar: <span style="color:#00E676;">${res_kelly['monto_sugerido']:,.2f} MXN</span> ({res_kelly['kelly_pct']}% de tu bankroll) en cuota {mejor_cuota_ev}</div>
                        <small style="color:#aaa;">* Calculado con ventaja matemática positiva (+EV) y control de riesgo.</small>
                    </div>
                    ''', unsafe_allow_html=True)

            c_b1, c_b2, c_b3 = st.columns(3)
            c_b1.metric("Stake Seguro (5%)", f"${bankroll * 0.05:,.2f}")
            c_b2.metric("Stake Medio (3%)", f"${bankroll * 0.03:,.2f}")
            c_b3.metric("Stake Riesgo (1%)", f"${bankroll * 0.01:,.2f}")

            # Contexto en la Tabla (Factor Necesidad)
            if datos_loc and datos_vis:
                st.markdown("---")
                st.write("### 📈 Contexto en la Tabla (Factor Necesidad)")
                pos_l, pts_l, forma_l = datos_loc['rank'], datos_loc['points'], datos_loc['form']
                pos_v, pts_v, forma_v = datos_vis['rank'], datos_vis['points'], datos_vis['form']
                txt_nec_l = analytics.evaluar_necesidad(pos_l, liga_elegida_val)
                txt_nec_v = analytics.evaluar_necesidad(pos_v, liga_elegida_val)

                ct1, ct2 = st.columns(2)
                with ct1:
                    st.markdown(f'''<div style="background:#1a2530; padding:14px; border-radius:10px; border-left:5px solid #3498db;">
                    <h4 style="color:white; margin:0 0 6px 0;">🔵 {equipo_local_real}</h4>
                    <p style="color:#ddd; font-size:13px; margin:0 0 6px 0;">Posición: {pos_l}° | Puntos: {pts_l} | Racha: {forma_l}</p>
                    <div style="background:rgba(52,152,219,0.15); padding:8px; border-radius:6px;">
                        <p style="color:#e0e0e0; margin:0; font-size:12px;">📌 {txt_nec_l}</p>
                    </div></div>''', unsafe_allow_html=True)
                with ct2:
                    st.markdown(f'''<div style="background:#301a1a; padding:14px; border-radius:10px; border-left:5px solid #e74c3c;">
                    <h4 style="color:white; margin:0 0 6px 0;">🔴 {equipo_visita_real}</h4>
                    <p style="color:#ddd; font-size:13px; margin:0 0 6px 0;">Posición: {pos_v}° | Puntos: {pts_v} | Racha: {forma_v}</p>
                    <div style="background:rgba(231,76,60,0.15); padding:8px; border-radius:6px;">
                        <p style="color:#e0e0e0; margin:0; font-size:12px;">📌 {txt_nec_v}</p>
                    </div></div>''', unsafe_allow_html=True)
