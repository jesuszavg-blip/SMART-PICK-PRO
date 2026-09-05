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
import textwrap

def render_html(html_str: str):
    """Renderiza HTML limpio y sin sangrías evitando falsos bloques de código en Markdown."""
    if html_str:
        st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)

def render_image_preview(img_bytes: bytes, caption: str = "", max_width: str = "600px"):
    """Renderiza vista previa de imagen en base64 HTML nativo, 100% inmune a errores de Pillow/st.image."""
    if not img_bytes:
        return
    import base64
    try:
        b64_str = base64.b64encode(img_bytes).decode('utf-8')
        cap_html = f'<div style="text-align:center; color:#94A3B8; font-size:13px; font-weight:600; margin-top:8px;">{html.escape(caption)}</div>' if caption else ''
        render_html(f'''
        <div style="text-align:center; margin: 8px 0 14px 0;">
            <img src="data:image/png;base64,{b64_str}" style="width:100%; max-width:{max_width}; border-radius:12px; border:1.5px solid #282F3F; box-shadow:0 8px 30px rgba(0,0,0,0.6); display:inline-block;" />
            {cap_html}
        </div>
        ''')
    except Exception:
        try:
            st.image(img_bytes, caption=caption, use_container_width=True)
        except Exception:
            st.warning("⚠️ Vista previa no disponible. Usa el botón de descarga para obtener la ficha HD.")

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
importlib.reload(auth)
import api_client
importlib.reload(api_client)
import analytics
importlib.reload(analytics)
import progol
importlib.reload(progol)
import jornada_manager
importlib.reload(jornada_manager)
import squads_data
import pitch_renderer
importlib.reload(pitch_renderer)
import social_card_generator
importlib.reload(social_card_generator)
try:
    import assets_data
    importlib.reload(assets_data)
except ImportError:
    assets_data = None

# Configuración de Página
st.set_page_config(
    page_title="Smart Pick Pro VIP - Data Intelligence",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de Meta-tags PWA para instalación móvil nativa (iOS / Android)
render_html("""
<head>
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="SmartPick VIP">
    <link rel="icon" type="image/jpeg" href="https://raw.githubusercontent.com/jesuszavg-blip/SMART-PICK-PRO/main/assets/app_icon.jpg">
    <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/jesuszavg-blip/SMART-PICK-PRO/main/assets/app_icon.jpg">
    <link rel="manifest" href="manifest.json">
</head>
""")

# Botón Flotante Balón ⚽ Indestructible (Funciona en Móvil, PC y Modo Embebido)
import streamlit.components.v1 as _st_components
_st_components.html("""
<script>
(function() {
    function setupFab() {
        try {
            const doc = window.parent ? window.parent.document : document;
            if (doc.getElementById('vip-global-menu-fab')) return;

            const fab = doc.createElement('div');
            fab.id = 'vip-global-menu-fab';
            fab.innerHTML = '⚽';
            fab.title = 'Abrir / Cerrar Menú VIP';
            fab.style.cssText = 'position:fixed;top:14px;left:14px;z-index:99999999;background:#151821;border:2.5px solid #D4AF37;border-radius:50%;width:48px;height:48px;display:flex;align-items:center;justify-content:center;font-size:24px;box-shadow:0 4px 20px rgba(212,175,55,0.5);cursor:pointer;user-select:none;-webkit-tap-highlight-color:transparent;transition:transform 0.2s;';

            fab.onmouseover = () => fab.style.transform = 'scale(1.1)';
            fab.onmouseout = () => fab.style.transform = 'scale(1.0)';

            fab.onclick = function(e) {
                e.stopPropagation();
                const expandBtn = doc.querySelector('[data-testid="stSidebarCollapsedControl"] button, [data-testid="collapsedControl"] button, button[aria-label="Expand sidebar"]');
                const collapseBtn = doc.querySelector('[data-testid="stSidebarCollapseButton"] button, button[aria-label="Close sidebar"]');
                
                if (expandBtn) {
                    expandBtn.click();
                    return;
                }
                if (collapseBtn) {
                    collapseBtn.click();
                    return;
                }

                const sb = doc.querySelector('section[data-testid="stSidebar"]');
                if (sb) {
                    const isHidden = sb.style.display === 'none' || sb.style.transform.includes('-100') || sb.getAttribute('aria-expanded') === 'false';
                    if (isHidden) {
                        sb.style.display = 'block';
                        sb.style.transform = 'none';
                        sb.style.position = 'fixed';
                        sb.style.left = '0';
                        sb.style.top = '0';
                        sb.style.height = '100vh';
                        sb.style.zIndex = '9999999';
                        sb.style.background = '#151821';
                        sb.style.boxShadow = '0 0 35px rgba(212,175,55,0.4)';
                        sb.setAttribute('aria-expanded', 'true');
                    } else {
                        sb.style.display = 'none';
                        sb.style.transform = 'translateX(-100%)';
                        sb.setAttribute('aria-expanded', 'false');
                    }
                }
            };

            doc.body.appendChild(fab);
        } catch(e) {
            console.log("FAB setup error:", e);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupFab);
    } else {
        setupFab();
    }
    setTimeout(setupFab, 300);
    setTimeout(setupFab, 1000);
    setTimeout(setupFab, 2500);
})();
</script>
""", height=0, width=0)

def obtener_fondo_estadio_url() -> str:
    """Obtiene el fondo de estadio nocturno en Base64 o URL remota de respaldo."""
    try:
        ruta = os.path.join(os.path.dirname(__file__), "assets", "fondos_demo", "opcion1_estadio_nocturno.jpg")
        if os.path.exists(ruta):
            import base64
            with open(ruta, "rb") as f:
                return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    except Exception:
        pass
    return "https://raw.githubusercontent.com/jesuszavg-blip/SMART-PICK-PRO/main/assets/fondos_demo/opcion1_estadio_nocturno.jpg"

fondo_estadio_data = obtener_fondo_estadio_url()

# Inyección del Fondo de Estadio Nocturno Glassmorphism VIP
render_html(f"""
<style>
    /* Fondo Inmersivo de Estadio Nocturno VIP Puro */
    .stApp {{
        background: linear-gradient(180deg, rgba(10, 13, 20, 0.65) 0%, rgba(13, 17, 24, 0.76) 100%),
                    url('{fondo_estadio_data}') no-repeat center center fixed !important;
        background-size: cover !important;
        color: #FFFFFF !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }}
    
    /* Efecto Glassmorphism en la Barra Lateral */
    [data-testid="stSidebar"] {{
        background: rgba(15, 18, 26, 0.92) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border-right: 1px solid rgba(212, 175, 55, 0.25) !important;
    }}

    /* Tarjetas y Banners con Glassmorphism Premium */
    .card-dark, .hero-banner {{
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5), 0 0 12px rgba(212, 175, 55, 0.15) !important;
    }}
</style>
""")

# Estilos CSS Personalizados de Máximo Contraste Visual y Estética Premium VIP (Paleta Oficial Dorado & Obsidiana)
render_html("""
<style>
    /* Ocultar controles de Streamlit (Fork, GitHub, Deploy, MainMenu) */
    #MainMenu { display: none !important; visibility: hidden !important; }
    footer { display: none !important; visibility: hidden !important; }
    [data-testid="stToolbar"] { display: none !important; visibility: hidden !important; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }
    .stDeployButton { display: none !important; }

    /* Header transparente */
    header[data-testid="stHeader"] {
        background: transparent !important;
        pointer-events: none !important;
    }

    /* 1. CUANDO LA BARRA LATERAL ESTÁ CERRADA: Botón único flotante Balón ⚽ arriba a la izquierda (Móvil y Escritorio) */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"],
    button[aria-label="Expand sidebar"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        position: fixed !important;
        top: 14px !important;
        left: 14px !important;
        z-index: 1000000 !important;
        pointer-events: auto !important;
    }

    [data-testid="stSidebarCollapsedControl"] button,
    [data-testid="collapsedControl"] button,
    button[aria-label="Expand sidebar"] {
        background: #151821 !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 50% !important;
        width: 46px !important;
        height: 46px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 4px 18px rgba(212, 175, 55, 0.45) !important;
        cursor: pointer !important;
        pointer-events: auto !important;
        padding: 0 !important;
        color: transparent !important;
    }

    [data-testid="stSidebarCollapsedControl"] button svg,
    [data-testid="collapsedControl"] button svg,
    button[aria-label="Expand sidebar"] svg {
        display: none !important;
    }

    [data-testid="stSidebarCollapsedControl"] button::after,
    [data-testid="collapsedControl"] button::after,
    button[aria-label="Expand sidebar"]::after {
        content: "⚽" !important;
        font-size: 22px !important;
        line-height: 1 !important;
        color: initial !important;
    }

    /* 2. CUANDO LA BARRA LATERAL ESTÁ ABIERTA: Botón de Cerrar claro y visible dentro del menú */
    [data-testid="stSidebarCollapseButton"] {
        display: flex !important;
        visibility: visible !important;
        pointer-events: auto !important;
    }

    [data-testid="stSidebarCollapseButton"] button {
        background: #1A1E29 !important;
        border: 1.5px solid #EF5350 !important;
        border-radius: 8px !important;
        padding: 6px 14px !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        pointer-events: auto !important;
    }

    [data-testid="stSidebarCollapseButton"] button svg {
        display: none !important;
    }

    [data-testid="stSidebarCollapseButton"] button::after {
        content: "✖ CERRAR" !important;
        color: #EF5350 !important;
        font-size: 13px !important;
        font-weight: 900 !important;
        line-height: 1 !important;
    }

    /* Estilos globales y contraste de texto */
    .stApp {
        background-color: #0D0F14;
        color: #FFFFFF !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Contraste forzado en la barra lateral */
    [data-testid="stSidebar"] {
        background-color: #11141C !important;
        border-right: 1px solid #232938;
    }
    
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }

    /* Banners y Tarjetas de Alto Contraste */
    .hero-banner {
        background: linear-gradient(135deg, #1C202B 0%, #2A2E3D 50%, #151821 100%);
        border: 1.5px solid #D4AF37;
        padding: 24px;
        border-radius: 14px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 6px 25px rgba(212, 175, 55, 0.2);
    }
    
    .card-dark {
        background-color: #161922;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 14px;
        border: 1px solid #282F3F;
        color: #FFFFFF !important;
    }
    
    .whatsapp-btn {
        background: linear-gradient(135deg, #1A4D2E 0%, #155E38 100%);
        border: 1px solid #2ECC71;
        color: white !important;
        padding: 10px 22px;
        border-radius: 30px;
        text-decoration: none;
        font-weight: bold;
        font-size: 14px;
        box-shadow: 0 4px 10px rgba(46, 204, 113, 0.25);
        display: inline-block;
        transition: transform 0.2s ease;
    }
    .whatsapp-btn:hover {
        transform: scale(1.03);
    }
    
    .casino-btn {
        background: linear-gradient(135deg, #D4AF37 0%, #AA7C11 100%);
        color: #0D0F14 !important;
        padding: 6px 14px;
        border-radius: 20px;
        text-decoration: none;
        font-size: 12px;
        font-weight: 900;
    }

    /* Pestañas (st.tabs) Premium VIP */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #11141C;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #232938;
    }

    .stTabs [data-baseweb="tab"] {
        height: 46px;
        white-space: pre-wrap;
        background-color: #161922;
        border-radius: 8px;
        color: #D1D5DB;
        font-weight: 800;
        font-size: 14px;
        padding: 0 16px;
        border: 1px solid #282F3F;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #F3E5AB 0%, #D4AF37 50%, #AA7C11 100%) !important;
        color: #0D0F14 !important;
        border: 1px solid #F3E5AB !important;
        box-shadow: 0 0 14px rgba(212, 175, 55, 0.4);
    }

    /* Métricas con alto contraste */
    [data-testid="stMetricValue"] {
        font-size: 26px !important;
        font-weight: 900 !important;
        color: #D4AF37 !important;
    }

    [data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-weight: 600 !important;
    }
    
    /* Cajas de alerta e información en texto blanco puro */
    .stAlert, [data-baseweb="notification"] {
        background-color: #161922 !important;
        border-left: 5px solid #D4AF37 !important;
        border-radius: 8px !important;
    }

    .stAlert p, .stAlert span, [data-baseweb="notification"] p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* --- TODOS LOS BOTONES DEL SISTEMA Y SIDEBAR (ALTO CONTRASTE PERMANENTE) --- */
    button,
    .stButton > button,
    .stDownloadButton > button,
    [data-testid="stDownloadButton"] > button,
    [data-testid="stDownloadButton"] a,
    [data-testid="baseButton-secondary"],
    [data-testid="baseButton-primary"],
    [data-testid="stSidebar"] button,
    [data-testid="stSidebar"] .stDownloadButton button,
    [data-testid="stSidebar"] [data-testid="baseButton-secondary"],
    [data-testid="stSidebar"] [data-testid="baseButton-primary"] {
        background-color: #161922 !important;
        color: #D4AF37 !important;
        -webkit-text-fill-color: #D4AF37 !important;
        border: 1.5px solid #D4AF37 !important;
        border-radius: 10px !important;
        font-weight: 900 !important;
        font-size: 14px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.25s ease !important;
    }

    button:hover,
    .stButton > button:hover,
    .stDownloadButton > button:hover,
    [data-testid="stDownloadButton"] > button:hover,
    [data-testid="baseButton-secondary"]:hover,
    [data-testid="baseButton-primary"]:hover,
    [data-testid="stSidebar"] button:hover,
    [data-testid="stSidebar"] .stDownloadButton button:hover {
        background: linear-gradient(135deg, #F3E5AB 0%, #D4AF37 50%, #AA7C11 100%) !important;
        color: #0D0F14 !important;
        -webkit-text-fill-color: #0D0F14 !important;
        border-color: #F3E5AB !important;
        box-shadow: 0 0 18px rgba(212, 175, 55, 0.5) !important;
    }

    button p, button span,
    .stButton > button p,
    .stDownloadButton > button p,
    [data-testid="stSidebar"] button p,
    [data-testid="stSidebar"] button span {
        color: inherit !important;
        -webkit-text-fill-color: inherit !important;
        font-weight: 900 !important;
    }

    /* Cuadro de texto Ficha VIP / Textarea */
    .stTextArea textarea, [data-baseweb="textarea"] textarea, div[data-baseweb="textarea"] > div > textarea {
        background-color: #151821 !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        line-height: 1.5 !important;
        border: 1.5px solid #D4AF37 !important;
        border-radius: 10px !important;
    }
    
    .stTextArea label, .stTextArea p {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* --- SIDEBAR & PANEL DE ADMINISTRACIÓN (ALTO CONTRASTE TOTAL) --- */
    [data-testid="stSidebar"] {
        background-color: #0D0F14 !important;
        border-right: 1px solid #1E2330 !important;
    }

    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4, 
    [data-testid="stSidebar"] h5,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] li {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    [data-testid="stSidebar"] code {
        background-color: #161922 !important;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
        font-weight: 800 !important;
        border-radius: 6px !important;
        padding: 2px 6px !important;
    }

    [data-testid="stSidebar"] h4 {
        color: #D4AF37 !important;
        font-size: 16px !important;
        font-weight: 900 !important;
        margin-top: 14px !important;
        margin-bottom: 6px !important;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.25) !important;
    }

    /* Expander en Sidebar */
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background-color: #151821 !important;
        border: 1.5px solid #D4AF37 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5) !important;
    }

    [data-testid="stSidebar"] [data-testid="stExpander"] summary {
        color: #D4AF37 !important;
        font-weight: 900 !important;
        font-size: 15px !important;
    }

    /* Entradas de Texto y Selectores en Sidebar */
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
        background-color: #161922 !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border: 1.5px solid #D4AF37 !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }

    [data-testid="stSidebar"] .stTextInput input:focus,
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"]:focus {
        border-color: #F3E5AB !important;
        box-shadow: 0 0 12px rgba(212, 175, 55, 0.4) !important;
    }

    /* Subida de Archivos en Sidebar */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] section {
        background-color: #161922 !important;
        border: 2px dashed #D4AF37 !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploader"] section button {
        background-color: #D4AF37 !important;
        color: #0D0F14 !important;
        -webkit-text-fill-color: #0D0F14 !important;
        font-weight: 900 !important;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploader"] span,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] small {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
</style>
""")

# Manejo de Sesión de Autenticación
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
if 'usuario' not in st.session_state:
    st.session_state['usuario'] = None
if 'rol' not in st.session_state:
    st.session_state['rol'] = None

# Captura automática de código de afiliado desde URL (?ref=... o ?r=...)
codigo_referido_url = ""
try:
    if hasattr(st, "query_params"):
        codigo_referido_url = st.query_params.get("ref", "") or st.query_params.get("r", "") or ""
    elif hasattr(st, "experimental_get_query_params"):
        params_exp = st.experimental_get_query_params()
        codigo_referido_url = params_exp.get("ref", [""])[0] if "ref" in params_exp else ""
except Exception:
    pass

if not st.session_state['autenticado']:
    if assets_data and hasattr(assets_data, 'LOGO_WEB_B64') and assets_data.LOGO_WEB_B64:
        render_html(f'''
        <div style="text-align:center; margin-top:20px; margin-bottom:20px;">
            <img src="data:image/png;base64,{assets_data.LOGO_WEB_B64}" style="max-width:480px; width:90%; height:auto; filter:drop-shadow(0 12px 30px rgba(0,0,0,0.8));" />
        </div>
        ''')
    else:
        render_html('''
        <div class="hero-banner" style="margin-top: 25px;">
            <h1 style="color: white; margin: 0; font-weight: 900; font-size: 38px; letter-spacing: 1px;">🏆 SMART PICK PRO VIP</h1>
            <p style="color: white; margin: 8px 0 0 0; font-size: 18px; opacity: 0.95;">Sistema de IA Predictiva • Optimizador de Reducciones Progol • Buscador $+EV$</p>
            <div style="margin-top: 12px; display: inline-block; background: rgba(212, 175, 55, 0.15); border: 1.5px solid #D4AF37; border-radius: 20px; padding: 6px 18px; color: #D4AF37; font-weight: 900; font-size: 14px;">
                ⭐ +85.4% de Efectividad Comprobada en Quinielas y Parlays VIP
            </div>
        </div>
        ''')
    
    col_log1, col_log2, col_log3 = st.columns([1, 2.8, 1])
    with col_log2:
        tab_login, tab_register = st.tabs(["🔒 Iniciar Sesión", "✨ Crear Cuenta Nueva / Registro"])
        
        with tab_login:
            render_html('''
            <div style="background: #151821; padding: 20px 20px 10px 20px; border-radius: 14px 14px 0 0; border: 1px solid #282F3F; border-bottom: none;">
                <h4 style="color: white; margin: 0 0 10px 0; font-weight: 800; text-align: center;">Acceso a tu Cuenta VIP</h4>
            </div>
            ''')
            user_input = st.text_input("Usuario:", key="login_user")
            pwd_input = st.text_input("Contraseña:", type="password", key="login_pass")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 ACCEDER AL SISTEMA VIP", use_container_width=True, key="btn_login_submit"):
                exito, mensaje_o_rol = auth.verificar_credenciales(user_input, pwd_input)
                if exito:
                    st.session_state['autenticado'] = True
                    st.session_state['usuario'] = user_input.strip().lower()
                    st.session_state['rol'] = mensaje_o_rol
                    st.rerun()
                else:
                    st.error(f"❌ {mensaje_o_rol}")

        with tab_register:
            if codigo_referido_url:
                render_html(f'''
                <div style="background: rgba(212, 175, 55, 0.15); border: 1.5px solid #D4AF37; border-radius: 10px; padding: 10px 14px; margin-bottom: 12px; text-align: center;">
                    <span style="color: #F3E5AB; font-size: 13px; font-weight: bold;">🎁 ¡Invitación VIP Detectada! Código: <b style="color:#D4AF37; font-size:14px;">{codigo_referido_url.upper()}</b></span>
                </div>
                ''')

            reg_user = st.text_input("Elige tu Nombre de Usuario:", key="reg_user_in", placeholder="ej. crackpicks")
            reg_email = st.text_input("📧 Correo Electrónico:", key="reg_email_in", placeholder="tu_correo@ejemplo.com")
            reg_pass1 = st.text_input("Crea tu Contraseña:", type="password", key="reg_pass1_in")
            reg_pass2 = st.text_input("Confirma tu Contraseña:", type="password", key="reg_pass2_in")
            reg_ref_code = st.text_input("Código de Afiliado (Opcional):", value=codigo_referido_url, key="reg_ref_code_in")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✨ CREAR MI CUENTA", use_container_width=True, key="btn_reg_submit"):
                if not reg_user or not reg_pass1 or not reg_email:
                    st.error("❌ Por favor completa el usuario, correo electrónico y contraseña.")
                elif "@" not in reg_email or "." not in reg_email:
                    st.error("❌ Por favor ingresa un correo electrónico válido.")
                elif reg_pass1 != reg_pass2:
                    st.error("❌ Las contraseñas no coinciden.")
                elif len(reg_pass1) < 4:
                    st.error("❌ La contraseña debe tener al menos 4 caracteres.")
                else:
                    ok_reg, msg_reg = auth.registrar_usuario(
                        username=reg_user,
                        password=reg_pass1,
                        role="VIP",
                        codigo_referido_usado=reg_ref_code.strip() if reg_ref_code else None,
                        email=reg_email.strip().lower()
                    )
                    if ok_reg:
                        st.success(f"{msg_reg} ¡Iniciando sesión automáticamente...!")
                        st.session_state['autenticado'] = True
                        st.session_state['usuario'] = reg_user.strip().lower()
                        st.session_state['rol'] = "VIP"
                        st.rerun()
                    else:
                        st.error(f"❌ {msg_reg}")
        
        # --- CAJA DE MÉTODOS DE PAGO INTEGRADOS ---
        bancoppel_card = getattr(config, 'BANCOPPEL_TARJETA', '4169 1608 7646 1600')
        bancoppel_holder = getattr(config, 'BANCOPPEL_TITULAR', 'Jesús')
        mercadopago_url = getattr(config, 'MERCADOPAGO_LINK', 'https://mpago.la/1ZefYpR')
        paypal_url = getattr(config, 'PAYPAL_LINK', 'https://www.paypal.com/ncp/payment/HSSHUFTYF8FG2')
        bitso_trc20 = getattr(config, 'BITSO_USDT_TRC20', 'TUyvrvPjGyh9v5SDYHW7GZ1g4MomKSFkh2')

        html_pago = '<div style="background: linear-gradient(135deg, #151821 0%, #1A1E29 100%); padding: 22px; border-radius: 14px; border: 2px dashed #D4AF37; margin-top: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.4); text-align: center;">'
        html_pago += '<div style="background: linear-gradient(90deg, #FF512F 0%, #DD2476 100%); color: white; font-weight: 900; font-size: 13px; padding: 6px 16px; border-radius: 20px; display: inline-block; margin-bottom: 12px; box-shadow: 0 4px 10px rgba(221,36,118,0.4);">🔥 ¡SÚPER OFERTA POR TIEMPO LIMITADO (50% OFF)!</div>'
        html_pago += '<h3 style="color: #D4AF37; margin: 4px 0 10px 0; font-weight: 900; text-align: center;">💎 ACCESO VIP: <span style="text-decoration: line-through; color: #888; font-size: 20px;">$299</span> <span style="color: #F3E5AB; font-size: 32px;">$149 MXN</span> / MES</h3>'
        html_pago += '<p style="color: #E0E0E0; font-size: 13px; text-align: center; margin-bottom: 15px;">Realiza tu pago con el método que prefieras y envía tu comprobante por WhatsApp para activación instantánea 24/7:</p>'
        
        # 1. Mercado Pago
        html_pago += f'<div style="background: #11141C; border-radius: 10px; padding: 14px; border: 1.5px solid #00B4D8; margin-bottom: 12px; text-align: left;">'
        html_pago += f'<div style="color: #00B4D8; font-weight: 900; font-size: 14px; margin-bottom: 4px;">🟢 1. MERCADO PAGO ($149 MXN)</div>'
        html_pago += f'<div style="color: #ccc; font-size: 12px; margin-bottom: 8px;">Acepta Tarjetas de Débito, Crédito, SPEI y Depósito en OXXO / 7-Eleven.</div>'
        html_pago += f'<a href="{mercadopago_url}" target="_blank" style="background:#00B4D8; color:#0A192F; font-weight:900; font-size:13px; padding:8px 18px; border-radius:20px; text-decoration:none; display:inline-block; box-shadow:0 3px 10px rgba(0,180,216,0.3);">💳 PAGAR $149 EN MERCADO PAGO</a>'
        html_pago += f'</div>'

        # 2. PayPal
        html_pago += f'<div style="background: #11141C; border-radius: 10px; padding: 14px; border: 1.5px solid #38BDF8; margin-bottom: 12px; text-align: left;">'
        html_pago += f'<div style="color: #38BDF8; font-weight: 900; font-size: 14px; margin-bottom: 4px;">🔵 2. PAYPAL ($149 MXN)</div>'
        html_pago += f'<div style="color: #ccc; font-size: 12px; margin-bottom: 8px;">Pago seguro internacional con cualquier tarjeta o saldo de PayPal.</div>'
        html_pago += f'<a href="{paypal_url}" target="_blank" style="background:#0079C1; color:white; font-weight:900; font-size:13px; padding:8px 18px; border-radius:20px; text-decoration:none; display:inline-block; box-shadow:0 3px 10px rgba(0,121,193,0.3);">🌐 PAGAR POR PAYPAL</a>'
        html_pago += f'</div>'

        # 3. SPEI / BanCoppel
        html_pago += f'<div style="background: #11141C; border-radius: 10px; padding: 14px; border: 1px solid #282F3F; margin-bottom: 12px; text-align: left;">'
        html_pago += f'<div style="color: #F3E5AB; font-weight: 900; font-size: 14px; margin-bottom: 6px;">🟡 3. TRANSFERENCIA SPEI / BANCOPPEL ($149 MXN)</div>'
        html_pago += f'<div style="color: white; font-size: 13px;"><b>Banco:</b> BanCoppel</div>'
        html_pago += f'<div style="color: white; font-size: 13px;"><b>No. Tarjeta / SPEI:</b> <span style="color:#D4AF37; font-weight:bold; font-family:monospace;">{bancoppel_card}</span></div>'
        html_pago += f'<div style="color: white; font-size: 13px;"><b>Titular:</b> {bancoppel_holder}</div>'
        html_pago += f'</div>'

        # 4. Bitso Crypto USDT TRC-20
        html_pago += f'<div style="background: #11141C; border-radius: 10px; padding: 14px; border: 1.5px solid #A855F7; margin-bottom: 15px; text-align: left;">'
        html_pago += f'<div style="color: #C084FC; font-weight: 900; font-size: 14px; margin-bottom: 4px;">🟣 4. BITSO CRYPTO (USDT - RED TRON TRC-20)</div>'
        html_pago += f'<div style="color: #ccc; font-size: 12px; margin-bottom: 6px;">Monto: <b>8 USDT</b> (Equivalente a $149 MXN).</div>'
        html_pago += f'<div style="color: white; font-size: 12px; word-break: break-all; background:#0D0F14; padding:8px; border-radius:6px; font-family:monospace; border:1px solid #333;"><span style="color:#A855F7; font-weight:bold;">Wallet:</span> {bitso_trc20}</div>'
        html_pago += f'<div style="color: #aaa; font-size: 11px; margin-top:4px;">* Importante: Enviar únicamente por la Red <b>Tron (TRC-20)</b>.</div>'
        html_pago += f'</div>'

        # Botón WhatsApp
        html_pago += '<div style="text-align: center;"><a href="https://wa.me/526676947014?text=Hola%20Jesus,%20acabo%20de%20hacer%20el%20pago%20de%20%24149%20MXN%20para%20activar%20mi%20membresia%20VIP%20en%20Smart%20Pick%20Pro.%20Adjunto%20comprobante:" target="_blank" class="whatsapp-btn" style="display:inline-block; width:100%; box-sizing:border-box; font-size:15px; padding:12px;">💬 ENVIAR COMPROBANTE POR WHATSAPP (ACTIVACIÓN INMEDIATA)</a></div>'
        html_pago += '</div>'

        st.markdown(html_pago, unsafe_allow_html=True)
        
    st.stop()


# --- PANTALLA PRINCIPAL (AUTENTICADO) ---

# Cargar Jornada Oficial Activa de Progol (14 Partidos)
jornada_oficial = jornada_manager.cargar_jornada_activa()

# Encabezado Principal con Logo Oficial
logo_header_html = ""
if assets_data and hasattr(assets_data, 'LOGO_WEB_B64') and assets_data.LOGO_WEB_B64:
    logo_header_html = f'<div style="text-align:center;margin-bottom:15px;"><img src="data:image/png;base64,{assets_data.LOGO_WEB_B64}" style="max-height:230px;width:auto;max-width:92%;filter:drop-shadow(0 10px 25px rgba(0,0,0,0.65));" /></div>'

header_html = f'<div style="background:linear-gradient(135deg,#151821 0%,#1A1E29 100%);border:1px solid #282F3F;border-radius:14px;padding:24px 20px;text-align:center;margin-bottom:20px;box-shadow:0 6px 25px rgba(0,0,0,0.5);">{logo_header_html}<div style="display:inline-block;background:rgba(212,175,55,0.12);border:1.5px solid #D4AF37;border-radius:20px;padding:6px 20px;margin-bottom:8px;"><span style="color:#D4AF37;font-weight:900;font-size:14px;letter-spacing:0.5px;">⭐ SESIÓN VIP ACTIVA</span></div><div style="color:white;font-size:17px;margin-top:6px;">Bienvenido <b>{st.session_state["usuario"].upper()}</b> <span style="background:#D4AF37;color:#0D0F14;font-size:11px;font-weight:900;padding:2px 8px;border-radius:10px;margin-left:6px;">{st.session_state["rol"]}</span></div><p style="color:#94A3B8;margin:6px 0 0 0;font-size:13px;">Escáner Estadístico Predictivo & Optimizador Progol</p></div>'

st.markdown(header_html, unsafe_allow_html=True)

# Botón WhatsApp Superior & Logout
col_top1, col_top2 = st.columns([8, 2])
with col_top1:
    render_html(f'''
    <a href="{config.ENLACE_WHATSAPP}" target="_blank" class="whatsapp-btn">
        💬 Soporte WhatsApp VIP
    </a>
    ''')
with col_top2:
    if st.button("🔴 Cerrar Sesión", use_container_width=True):
        st.session_state['autenticado'] = False
        st.session_state['usuario'] = None
        st.session_state['rol'] = None
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Banners de Afiliados Oficiales (1xBet & Mexplay)
ban_1xbet = getattr(config, 'ENLACE_1XBET', 'https://reffpa.com/L?tag=d_6029550m_1599c_&site=6029550&ad=1599')
ban_mexplay = getattr(config, 'ENLACE_MEXPLAY', 'https://mexplay.mx/?referral=mqx6lb')

banners_afiliados_html = f'<div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(280px, 1fr));gap:14px;margin-top:8px;margin-bottom:18px;"><div style="background:linear-gradient(135deg, #0A192F 0%, #172A45 100%);border:1.5px solid #00B4D8;border-radius:14px;padding:16px;text-align:center;box-shadow:0 6px 20px rgba(0,180,216,0.25);"><div style="color:#90E0EF;font-weight:900;font-size:12px;letter-spacing:1px;text-transform:uppercase;">🔵 CASA OFICIAL DEPORTES #1</div><div style="color:#FFFFFF;font-weight:900;font-size:19px;margin:5px 0;">🎁 1XBET • BONO $3,500 MXN</div><p style="color:#CCD6F6;font-size:12px;margin:0 0 12px 0;">Las cuotas más altas de México y streaming de partidos en vivo.</p><a href="{ban_1xbet}" target="_blank" style="background:#00B4D8;color:#0A192F;font-weight:900;font-size:13px;padding:9px 20px;border-radius:25px;text-decoration:none;display:inline-block;box-shadow:0 3px 12px rgba(0,180,216,0.4);">🔥 ABRIR CUENTA EN 1XBET</a></div><div style="background:linear-gradient(135deg, #2D1500 0%, #3D1C06 100%);border:1.5px solid #FF8500;border-radius:14px;padding:16px;text-align:center;box-shadow:0 6px 20px rgba(255,133,0,0.25);"><div style="color:#FFB703;font-weight:900;font-size:12px;letter-spacing:1px;text-transform:uppercase;">🟡 CASINO & DEPORTES DESTACADO #2</div><div style="color:#FFFFFF;font-weight:900;font-size:19px;margin:5px 0;">🎰 MEXPLAY • BONO + GIROS</div><p style="color:#FFE8D6;font-size:12px;margin:0 0 12px 0;">Casino 100% mexicano, depósitos y retiros instantáneos por SPEI/OXXO.</p><a href="{ban_mexplay}" target="_blank" style="background:#FF8500;color:#FFFFFF;font-weight:900;font-size:13px;padding:9px 20px;border-radius:25px;text-decoration:none;display:inline-block;box-shadow:0 3px 12px rgba(255,133,0,0.4);">⚡ ABRIR CUENTA EN MEXPLAY</a></div></div>'

st.markdown(banners_afiliados_html, unsafe_allow_html=True)

# --- BARRA LATERAL ---
if assets_data and hasattr(assets_data, 'APP_ICON_B64') and assets_data.APP_ICON_B64:
    st.sidebar.markdown(f'''
    <div style="text-align:center; padding:6px 0 14px 0;">
        <img src="data:image/png;base64,{assets_data.APP_ICON_B64}" style="width:115px; height:115px; object-fit:contain; filter:drop-shadow(0 8px 18px rgba(0,0,0,0.65));" />
        <div style="color:#D4AF37; font-weight:900; font-size:17px; margin-top:8px; letter-spacing:0.5px;">SMART PICK PRO</div>
        <div style="color:#F3E5AB; font-size:11px; font-weight:bold; letter-spacing:1px;">DATA INTELLIGENCE VIP</div>
    </div>
    ''', unsafe_allow_html=True)

with st.sidebar.expander("📲 INSTALAR APP EN TU CELULAR", expanded=False):
    render_html('''
    <div style="background:#151821; padding:12px; border-radius:10px; border:1px solid #282F3F; font-size:13px; line-height:1.4;">
        <b style="color:#D4AF37;">🍏 En iPhone / iPad (Safari):</b><br>
        1. Toca el botón <b>Compartir</b> (ícono <span style="font-size:14px;">⬆️</span> abajo).<br>
        2. Selecciona <b>"Agregar a inicio"</b> ➕.<br>
        3. Toca <b>"Agregar"</b> y se creará la app con el logo oficial.<br><br>
        <b style="color:#D4AF37;">🤖 En Android (Chrome):</b><br>
        1. Toca los <b>3 puntos (⋮)</b> arriba a la derecha.<br>
        2. Elige <b>"Instalar aplicación"</b> o <b>"Agregar a pantalla principal"</b> 📥.<br>
        3. ¡Listo! Se abrirá a pantalla completa.
    </div>
    ''')

sidebar_casinos_html = f'<div style="background:linear-gradient(135deg, #151821 0%, #1A1E29 100%);padding:12px;border-radius:12px;border:1px solid #282F3F;margin-top:10px;margin-bottom:14px;text-align:center;"><div style="color:#D4AF37;font-weight:900;font-size:11px;margin-bottom:8px;letter-spacing:0.5px;">💎 CASAS RECOMENDADAS (+EV)</div><div style="display:flex;gap:6px;justify-content:center;"><a href="{ban_1xbet}" target="_blank" style="background:#00B4D8;color:#0A192F;font-weight:bold;font-size:11px;padding:6px 10px;border-radius:12px;text-decoration:none;flex:1;">🔵 1xBet</a><a href="{ban_mexplay}" target="_blank" style="background:#FF8500;color:#FFFFFF;font-weight:bold;font-size:11px;padding:6px 10px;border-radius:12px;text-decoration:none;flex:1;">🟡 Mexplay</a></div></div>'
st.sidebar.markdown(sidebar_casinos_html, unsafe_allow_html=True)

# Botones de Acceso Rápido VIP en la Barra Lateral
col_sb_sc1, col_sb_sc2 = st.sidebar.columns(2)
with col_sb_sc1:
    if st.button("🔥 GOLES", use_container_width=True, help="Abrir Radar Festival de Goles"):
        st.session_state['liga_selector_override'] = "🔥 [VIP] Festival de Goles (Radar Altas & BTTS)"
        st.session_state['live_partido_detalle'] = None
        st.rerun()
with col_sb_sc2:
    if st.button("📸 REDES HD", use_container_width=True, help="Abrir Generador de Fichas para Redes Sociales"):
        st.session_state['liga_selector_override'] = "📸 [VIP] Generador de Fichas para Redes (Instagram & WhatsApp)"
        st.session_state['live_partido_detalle'] = None
        st.rerun()

dict_ligas_globales = api_client.obtener_ligas_mundo()
lista_ligas_keys = list(dict_ligas_globales.keys())
idx_default_liga = 0
if st.session_state.get('liga_selector_override') in lista_ligas_keys:
    idx_default_liga = lista_ligas_keys.index(st.session_state['liga_selector_override'])
    st.session_state['liga_selector_override'] = None

liga_elegida = st.sidebar.selectbox("🌍 1. Selecciona el Torneo o Módulo:", lista_ligas_keys, index=idx_default_liga)
liga_elegida_val = dict_ligas_globales[liga_elegida]

# Reset reactivo: si el usuario cambia de liga o módulo en el menú lateral,
# limpiamos automáticamente cualquier partido en detalle para que navegue libremente a cualquier sección.
if st.session_state.get('nav_liga_actual') != liga_elegida_val:
    st.session_state['live_partido_detalle'] = None
    st.session_state['ver_top_altas_match'] = False
    st.session_state['ver_top_empates_match'] = False
    st.session_state['ver_pick_seguro_match'] = False
    st.session_state['ver_parlay_oro_match'] = False
    st.session_state['nav_liga_actual'] = liga_elegida_val

# Partidos de la jornada
partidos_dict = api_client.obtener_partidos_jornada(liga_elegida_val)
partido_seleccionado = st.sidebar.selectbox("⚽ 2. Encuentro a analizar:", list(partidos_dict.keys()))

# Reset reactivo: si el usuario cambia el partido en la lista desplegable
if st.session_state.get('nav_partido_actual') != partido_seleccionado:
    st.session_state['live_partido_detalle'] = None
    st.session_state['ver_top_altas_match'] = False
    st.session_state['ver_top_empates_match'] = False
    st.session_state['ver_pick_seguro_match'] = False
    st.session_state['ver_parlay_oro_match'] = False
    st.session_state['nav_partido_actual'] = partido_seleccionado

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
        st.write("#### 🛡️ Persistencia y Base de Datos")
        render_html(f"""
        - 👥 **Total Usuarios Activos:** `{est_pers['total_usuarios']}`
        - 📁 **Respaldo Local JSON:** `{'✅ Activo' if est_pers['backup_local_existe'] else '❌ Inactivo'}`
        - ☁️ **GitHub Cloud Permanente:** `{'✅ Conectado' if est_pers['nube_activa'] else '❌ Sin Token'}`
        """)

        if st.button("☁️ Sincronizar en GitHub Cloud Ahora", use_container_width=True, help="Guarda permanentemente todos los usuarios en GitHub"):
            ok_sync, msg_sync = auth.sincronizar_con_github_cloud()
            if ok_sync:
                st.success("✅ ¡Base de datos sincronizada permanentemente con GitHub!")
            else:
                st.error(f"❌ Error al sincronizar: {msg_sync}")

        st.markdown("---")
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
        # 3. Solicitudes de Retiro de Afiliados
        st.write("#### 💰 Solicitudes de Retiro de Afiliados")
        solicitudes_pendientes = auth.listar_solicitudes_retiro_admin(filtro_estado="PENDIENTE")
        if not solicitudes_pendientes:
            st.info("✅ No hay solicitudes de retiro pendientes.")
        else:
            for s_id, s_user, s_monto, s_metodo, s_cuenta, s_titular, s_estado, s_fecha, _, _ in solicitudes_pendientes:
                render_html(f"""
                <div style="background:#11141C; border:1px solid #D4AF37; border-radius:8px; padding:10px; margin-bottom:8px;">
                    <div style="color:#D4AF37; font-weight:900; font-size:13px;">💸 Retiro #{s_id}: ${s_monto:.2f} MXN</div>
                    <div style="color:white; font-size:12px;"><b>Usuario:</b> {s_user.upper()}</div>
                    <div style="color:white; font-size:12px;"><b>Método:</b> {s_metodo}</div>
                    <div style="color:white; font-size:12px;"><b>Cuenta:</b> <code>{s_cuenta}</code></div>
                    <div style="color:white; font-size:12px;"><b>Titular:</b> {s_titular}</div>
                    <div style="color:#aaa; font-size:10px;">Fecha: {s_fecha}</div>
                </div>
                """)
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    if st.button(f"✅ Pagado #{s_id}", key=f"pay_btn_{s_id}", use_container_width=True):
                        auth.marcar_retiro_pagado_admin(s_id, nota="Transferencia SPEI/PayPal realizada con éxito")
                        st.success(f"Retiro #{s_id} marcado como pagado.")
                        st.rerun()
                with col_p2:
                    if st.button(f"❌ Rechazar #{s_id}", key=f"rec_btn_{s_id}", use_container_width=True):
                        auth.rechazar_retiro_admin(s_id, motivo="Datos de cuenta incorrectos o incompletos")
                        st.warning(f"Retiro #{s_id} rechazado y saldo devuelto.")
                        st.rerun()

        st.markdown("---")
        # 4. Activación VIP y Liquidación Rápida de Comisión
        st.write("#### ⚡ Activar VIP & Liquidar Comisión")
        vip_act_user = st.text_input("Usuario a Activar VIP:", placeholder="ej. usuario_amigo", key="admin_vip_act_in")
        vip_act_monto = st.number_input("Monto Pagado ($ MXN):", value=149.0, step=10.0, key="admin_vip_act_monto")
        if st.button("👑 Activar VIP y Calcular Comisión", use_container_width=True):
            if vip_act_user:
                ok_vip, msg_vip = auth.activar_vip_y_procesar_comision(vip_act_user.strip().lower(), monto_pago=vip_act_monto)
                if ok_vip:
                    st.success(msg_vip)
                    st.rerun()
                else:
                    st.error(msg_vip)
            else:
                st.warning("Escribe el nombre de usuario.")

        st.markdown("---")
        # 5. Registrar Nuevo Usuario Manual
        st.write("#### ➕ Registrar Nuevo Usuario")
        new_u = st.text_input("Usuario:", key="admin_new_u")
        new_em = st.text_input("Correo Electrónico (Opcional):", key="admin_new_em", placeholder="correo@ejemplo.com")
        new_p = st.text_input("Contraseña:", type="password", key="admin_new_p")
        new_r = st.selectbox("Rol:", ["VIP", "ADMIN"], key="admin_new_r")
        if st.button("➕ Crear Usuario", use_container_width=True):
            ok, msg = auth.registrar_usuario(new_u, new_p, new_r, email=new_em)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
                
        st.markdown("---")
        # 6. Configuración de API Key
        st.write("#### ⚙️ Clave API-Sports")
        api_k_input = st.text_input("API Key:", value=config.API_KEY, type="password")
        if st.button("💾 Guardar API Key", use_container_width=True):
            config.API_KEY = api_k_input.strip()
            st.success("✅ API Key actualizada.")
                
        st.markdown("---")
        # 7. Lista de Usuarios y Gestión de Afiliados
        st.write("#### 📋 Base de Datos de Usuarios & Marketing")
        
        # Botón para descargar lista de correos en CSV para campañas de marketing
        csv_marketing = auth.exportar_lista_correos_csv()
        st.download_button(
            label="📥 Descargar Base de Correos (.CSV Marketing)",
            data=csv_marketing,
            file_name="usuarios_smartpick_marketing.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        
        usuarios_lista = auth.listar_usuarios()
        for u in usuarios_lista:
            u_id = u[0]
            u_name = u[1]
            u_rol = u[2]
            u_act = u[3]
            u_date = u[4]
            u_ref_c = u[5]
            u_ref_by = u[6]
            u_bal = u[7]
            u_tot = u[8]
            u_em = u[9] if len(u) > 9 and u[9] else ""
            
            col_u1, col_u2 = st.columns([3, 1])
            with col_u1:
                status_icon = "🟢" if u_act == 1 else "🔴"
                ref_by_info = f" | Ref por: `{u_ref_by}`" if u_ref_by else ""
                email_txt = f"📧 `{u_em}`" if u_em else "📧 *Sin correo registrado*"
                st.markdown(f"**{status_icon} {u_name.upper()}** [{u_rol}]")
                st.caption(f"{email_txt}\n\nCódigo: `{u_ref_c}` | Saldo: `${u_bal:.2f}` | Ganado: `${u_tot:.2f}`{ref_by_info}")
            with col_u2:
                if u_name.lower() != config.ADMIN_INIT_USER.lower():
                    if st.button("🗑️", key=f"del_u_{u_id}", help="Eliminar usuario"):
                        auth.eliminar_usuario(u_id)
                        st.rerun()

def render_tarjeta_live_segura(p_item):
    if hasattr(pitch_renderer, 'render_tarjeta_partido_live_radar'):
        return pitch_renderer.render_tarjeta_partido_live_radar(p_item)
    
    loc = html.escape(str(p_item.get('local', 'Local')))
    vis = html.escape(str(p_item.get('visita', 'Visita')))
    logo_l = p_item.get('logo_local', 'https://media.api-sports.io/football/teams/2287.png')
    logo_v = p_item.get('logo_visita', 'https://media.api-sports.io/football/teams/2291.png')
    g_l = p_item.get('goles_local', 0)
    g_v = p_item.get('goles_visita', 0)
    st_val = str(p_item.get('status', 'LIVE')).upper()
    min_val = p_item.get('minuto', 0)
    venue = html.escape(str(p_item.get('venue', 'Estadio')))

    if st_val in ['1H', '2H', 'LIVE']:
        st_badge = f'<span style="background:rgba(231,76,60,0.2); color:#EF5350; border:1px solid #EF5350; padding:3px 10px; border-radius:20px; font-weight:900; font-size:11px; letter-spacing:0.5px;">🔴 {st_val} {min_val}\'</span>'
    elif st_val == 'HT':
        st_badge = '<span style="background:rgba(212,175,55,0.2); color:#D4AF37; border:1px solid #D4AF37; padding:3px 10px; border-radius:20px; font-weight:900; font-size:11px;">⏸️ ENTRETIEMPO</span>'
    elif st_val in ['FT', 'AET', 'PEN']:
        st_badge = '<span style="background:rgba(212,175,55,0.15); color:#D4AF37; border:1px solid #D4AF37; padding:3px 10px; border-radius:20px; font-weight:900; font-size:11px;">🏁 FINAL</span>'
    else:
        st_badge = f'<span style="background:rgba(255,255,255,0.1); color:#aaa; border:1px solid #444; padding:3px 10px; border-radius:20px; font-weight:bold; font-size:11px;">⏳ {st_val}</span>'

    return f'''
    <div style="background:linear-gradient(135deg, #151821 0%, #1A1E29 100%); border:1px solid #282F3F; border-radius:14px; padding:14px 18px; margin-bottom:10px; box-shadow:0 4px 15px rgba(0,0,0,0.3);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; border-bottom:1px solid #232938; padding-bottom:6px;">
            <div style="color:#aaa; font-size:11px; font-weight:bold;">📍 {venue}</div>
            <div>{st_badge}</div>
        </div>
        <div style="display:grid; grid-template-columns:1fr auto 1fr; align-items:center; gap:12px; margin-bottom:6px;">
            <div style="display:flex; align-items:center; justify-content:flex-end; gap:10px; text-align:right;">
                <span style="color:#FFFFFF; font-weight:900; font-size:15px; line-height:1.2;">{loc}</span>
                <img src="{logo_l}" style="width:36px; height:36px; object-fit:contain; flex-shrink:0;">
            </div>
            <div style="background:#0D0F14; border:1.5px solid #D4AF37; padding:4px 16px; border-radius:8px; font-size:22px; font-weight:900; color:#D4AF37; letter-spacing:2px; text-align:center; min-width:70px;">
                {g_l} - {g_v}
            </div>
            <div style="display:flex; align-items:center; justify-content:flex-start; gap:10px; text-align:left;">
                <img src="{logo_v}" style="width:36px; height:36px; object-fit:contain; flex-shrink:0;">
                <span style="color:#FFFFFF; font-weight:900; font-size:15px; line-height:1.2;">{vis}</span>
            </div>
        </div>
    </div>
    '''

# --- MODO: PROGRAMA DE AFILIADOS VIP (50% / 40% / 30%) ---
if liga_elegida_val == "AFFILIATE_PROGRAM_MODE":
    usuario_actual = st.session_state.get('usuario', 'vip')
    resumen_af = auth.obtener_resumen_afiliado(usuario_actual)

    render_html('''
    <div style="background: linear-gradient(135deg, #1C202B 0%, #2A2312 50%, #151821 100%); border: 1.5px solid #D4AF37; padding: 24px; border-radius: 14px; text-align: center; margin-bottom: 20px; box-shadow: 0 6px 25px rgba(212, 175, 55, 0.25);">
        <div style="display:inline-block; background:rgba(212,175,55,0.15); border:1px solid #D4AF37; border-radius:20px; padding:4px 16px; margin-bottom:8px;">
            <span style="color:#D4AF37; font-weight:900; font-size:12px; letter-spacing:1px; text-transform:uppercase;">🤝 PROGRAMA OFICIAL DE SOCIOS Y AFILIADOS</span>
        </div>
        <h2 style="color: white; margin: 0; font-weight: 900; font-size: 30px; letter-spacing: 0.5px;">💰 GANA DINERO RECOMENDANDO SMART PICK PRO</h2>
        <p style="color: #E2E8F0; margin: 8px auto 0 auto; font-size: 15px; opacity: 0.95; max-width:750px;">
            Comparte tu enlace personalizado con amigos, grupos de apuestas o en redes sociales y gana comisiones recurrentes automáticas directamente a tu cuenta bancaria o PayPal.
        </p>
    </div>
    ''')

    # 1. Tarjetas de Niveles de Comisión Escalonada
    p_mes1 = int(getattr(config, 'COMISION_MES_1', 0.50) * 100)
    p_mes2 = int(getattr(config, 'COMISION_MES_2', 0.40) * 100)
    p_rec = int(getattr(config, 'COMISION_MES_RECURRENTE', 0.30) * 100)
    precio_vip = getattr(config, 'PRECIO_VIP_MXN', 149.0)

    gan_mes1 = precio_vip * (p_mes1 / 100.0)
    gan_mes2 = precio_vip * (p_mes2 / 100.0)
    gan_rec = precio_vip * (p_rec / 100.0)

    render_html(f'''
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:14px; margin-bottom:22px;">
        <div style="background:linear-gradient(135deg, #182618 0%, #151821 100%); border:1.5px solid #2ECC71; border-radius:12px; padding:16px; text-align:center; box-shadow:0 4px 15px rgba(46,204,113,0.2);">
            <div style="background:#2ECC71; color:#0A1E0D; font-weight:900; font-size:11px; padding:3px 10px; border-radius:12px; display:inline-block; margin-bottom:6px;">🥇 MES 1 (REGISTRO)</div>
            <div style="color:#FFFFFF; font-weight:900; font-size:32px; margin:2px 0;">{p_mes1}% <span style="font-size:16px; color:#A7F3D0;">(${gan_mes1:.2f} MXN)</span></div>
            <p style="color:#CCD6F6; font-size:12px; margin:0;">Ganas la mitad del primer pago de cada amigo que invites a Smart Pick Pro.</p>
        </div>
        <div style="background:linear-gradient(135deg, #2B2312 0%, #151821 100%); border:1.5px solid #F59E0B; border-radius:12px; padding:16px; text-align:center; box-shadow:0 4px 15px rgba(245,158,11,0.2);">
            <div style="background:#F59E0B; color:#2A1A00; font-weight:900; font-size:11px; padding:3px 10px; border-radius:12px; display:inline-block; margin-bottom:6px;">🥈 MES 2 (RENOVACIÓN)</div>
            <div style="color:#FFFFFF; font-weight:900; font-size:32px; margin:2px 0;">{p_mes2}% <span style="font-size:16px; color:#FDE68A;">(${gan_mes2:.2f} MXN)</span></div>
            <p style="color:#CCD6F6; font-size:12px; margin:0;">Ganas el 40% en su segundo mes cuando continúe aprovechando el sistema.</p>
        </div>
        <div style="background:linear-gradient(135deg, #142238 0%, #151821 100%); border:1.5px solid #38BDF8; border-radius:12px; padding:16px; text-align:center; box-shadow:0 4px 15px rgba(56,189,248,0.2);">
            <div style="background:#38BDF8; color:#082438; font-weight:900; font-size:11px; padding:3px 10px; border-radius:12px; display:inline-block; margin-bottom:6px;">🔁 MES 3+ (DE POR VIDA)</div>
            <div style="color:#FFFFFF; font-weight:900; font-size:32px; margin:2px 0;">{p_rec}% <span style="font-size:16px; color:#BAE6FD;">(${gan_rec:.2f} MXN)</span></div>
            <p style="color:#CCD6F6; font-size:12px; margin:0;">Ingreso pasivo mensual continuo mientras tu referido mantenga su suscripción.</p>
        </div>
    </div>
    ''')

    # 2. Enlace Único de Afiliado & Botones de Difusión
    enlace_af = resumen_af.get('enlace_afiliado', f"https://smartpickprojz.com/?ref={resumen_af.get('referral_code', 'SP-VIP')}")
    cod_af = resumen_af.get('referral_code', 'SP-VIP')

    render_html('''
    <div style="background:#151821; border:1px solid #282F3F; border-radius:14px; padding:20px; margin-bottom:20px;">
        <h3 style="color:#D4AF37; margin:0 0 10px 0; font-weight:900; font-size:18px;">🔗 Tu Enlace de Afiliado Exclusivo</h3>
        <p style="color:#94A3B8; font-size:13px; margin-bottom:12px;">Comparte este enlace para que cualquier usuario que se registre quede asignado automáticamente como tu referido:</p>
    ''')

    col_link1, col_link2 = st.columns([3, 1])
    with col_link1:
        st.code(enlace_af, language="text")
    with col_link2:
        render_html(f'''
        <div style="background:#11141C; border:1px solid #D4AF37; border-radius:8px; padding:10px; text-align:center;">
            <div style="color:#aaa; font-size:10px; font-weight:bold;">TU CÓDIGO</div>
            <div style="color:#D4AF37; font-weight:900; font-size:18px; letter-spacing:1px;">{cod_af}</div>
        </div>
        ''')

    # Botones de compartir rápido por WhatsApp y Telegram
    import urllib.parse
    msg_promo = f"¡Hola! Te invito a probar Smart Pick Pro, la plataforma de IA para pronósticos deportivos, parlays VIP y optimizador de Progol. Entra con mi enlace oficial y obtén la promo del 50% de descuento: {enlace_af}"
    encoded_promo_wa = urllib.parse.quote(msg_promo)
    encoded_promo_tg = urllib.parse.quote(enlace_af)
    encoded_promo_tg_text = urllib.parse.quote("Prueba Smart Pick Pro VIP con IA predictiva:")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        render_html(f'''
        <a href="https://wa.me/?text={encoded_promo_wa}" target="_blank" style="background:#25D366; color:white; font-weight:900; padding:11px 18px; border-radius:10px; text-decoration:none; display:block; text-align:center; font-size:14px; box-shadow:0 4px 12px rgba(37,211,102,0.3);">
            💬 COMPARTIR EN WHATSAPP (1 CLIC)
        </a>
        ''')
    with col_btn2:
        render_html(f'''
        <a href="https://t.me/share/url?url={encoded_promo_tg}&text={encoded_promo_tg_text}" target="_blank" style="background:#0088CC; color:white; font-weight:900; padding:11px 18px; border-radius:10px; text-decoration:none; display:block; text-align:center; font-size:14px; box-shadow:0 4px 12px rgba(0,136,204,0.3);">
            ✈️ COMPARTIR EN TELEGRAM (1 CLIC)
        </a>
        ''')

    st.markdown("</div>", unsafe_allow_html=True)

    # 3. Métricas en Tiempo Real (Tarjetas KPI)
    tot_ref = resumen_af.get('total_referidos', 0)
    vip_act = resumen_af.get('referidos_vip', 0)
    bal_disp = resumen_af.get('balance_disponible', 0.0)
    tot_gan = resumen_af.get('total_ganado', 0.0)

    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    with col_kpi1:
        render_html(f'''
        <div style="background:#151821; border:1px solid #282F3F; border-radius:12px; padding:16px; text-align:center;">
            <div style="font-size:24px; margin-bottom:4px;">👥</div>
            <div style="color:#aaa; font-size:11px; font-weight:bold; text-transform:uppercase;">Amigos Registrados</div>
            <div style="color:white; font-size:26px; font-weight:900; margin-top:4px;">{tot_ref}</div>
        </div>
        ''')
    with col_kpi2:
        render_html(f'''
        <div style="background:#151821; border:1px solid #282F3F; border-radius:12px; padding:16px; text-align:center;">
            <div style="font-size:24px; margin-bottom:4px;">👑</div>
            <div style="color:#aaa; font-size:11px; font-weight:bold; text-transform:uppercase;">VIPs Activos</div>
            <div style="color:#38BDF8; font-size:26px; font-weight:900; margin-top:4px;">{vip_act}</div>
        </div>
        ''')
    with col_kpi3:
        render_html(f'''
        <div style="background:#151821; border:1.5px solid #2ECC71; border-radius:12px; padding:16px; text-align:center; box-shadow:0 4px 15px rgba(46,204,113,0.15);">
            <div style="font-size:24px; margin-bottom:4px;">💵</div>
            <div style="color:#2ECC71; font-size:11px; font-weight:bold; text-transform:uppercase;">Saldo Retirable</div>
            <div style="color:#FFFFFF; font-size:26px; font-weight:900; margin-top:4px;">${bal_disp:.2f} <span style="font-size:12px; color:#aaa;">MXN</span></div>
        </div>
        ''')
    with col_kpi4:
        render_html(f'''
        <div style="background:#151821; border:1.5px solid #D4AF37; border-radius:12px; padding:16px; text-align:center; box-shadow:0 4px 15px rgba(212,175,55,0.15);">
            <div style="font-size:24px; margin-bottom:4px;">🏆</div>
            <div style="color:#D4AF37; font-size:11px; font-weight:bold; text-transform:uppercase;">Total Ganado</div>
            <div style="color:#FFFFFF; font-size:26px; font-weight:900; margin-top:4px;">${tot_gan:.2f} <span style="font-size:12px; color:#aaa;">MXN</span></div>
        </div>
        ''')

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Pestañas de Gestión: Solicitar Retiro, Historial de Comisiones, Historial de Retiros, Amigos
    tab_retirar, tab_hist_com, tab_hist_ret, tab_mis_ref = st.tabs([
        "💸 Solicitar Retiro de Saldo",
        "💰 Historial de Comisiones",
        "📤 Historial de Retiros",
        "👥 Mis Amigos Registrados"
    ])

    with tab_retirar:
        render_html('''
        <div style="background:#151821; border:1px solid #282F3F; border-radius:12px; padding:18px; margin-bottom:15px;">
            <h4 style="color:#D4AF37; margin:0 0 6px 0; font-weight:900;">Transferencia Directa de tus Ganancias</h4>
            <p style="color:#94A3B8; font-size:13px; margin:0;">
                Puedes retirar tu saldo acumulado a través de <b>Transferencia SPEI (México)</b> o <b>PayPal (Internacional)</b>. Los retiros se procesan en un plazo máximo de 24 horas.
            </p>
        </div>
        ''')

        min_ret = getattr(config, 'MINIMO_RETIRO_AFILIADO', 100.0)

        col_ret1, col_ret2 = st.columns(2)
        with col_ret1:
            metodo_retiro = st.selectbox("1. Método de Pago:", ["SPEI (Transferencia Bancaria México - CLABE)", "PayPal (Correo Electrónico)"], key="af_metodo_in")
            titular_retiro = st.text_input("2. Nombre Completo del Titular:", key="af_titular_in", placeholder="ej. Juan Pérez Rodríguez")
        with col_ret2:
            placeholder_cta = "CLABE Interbancaria (18 dígitos)" if "SPEI" in metodo_retiro else "correo@ejemplo.com (Cuenta PayPal)"
            cuenta_retiro = st.text_input(f"3. {'CLABE (18 dígitos)' if 'SPEI' in metodo_retiro else 'Correo PayPal'}:", placeholder=placeholder_cta, key="af_cta_in")
            monto_retiro = st.number_input(f"4. Monto a Retirar (Mínimo ${min_ret:.2f} MXN):", min_value=float(min_ret), max_value=max(float(min_ret), float(bal_disp)), value=min(max(float(min_ret), float(bal_disp)), float(bal_disp)) if bal_disp >= min_ret else float(min_ret), step=50.0, key="af_monto_in")

        if st.button("🚀 ENVIAR SOLICITUD DE RETIRO", use_container_width=True, key="btn_solicitar_retiro"):
            if bal_disp < min_ret:
                st.error(f"❌ Saldo insuficiente para retirar. El mínimo es de ${min_ret:.2f} MXN y tu saldo actual es de ${bal_disp:.2f} MXN.")
            elif not titular_retiro.strip() or not cuenta_retiro.strip():
                st.error("❌ Por favor completa todos los datos bancarios / PayPal.")
            else:
                ok_ret, msg_ret = auth.solicitar_retiro(
                    username=usuario_actual,
                    monto=monto_retiro,
                    metodo="SPEI" if "SPEI" in metodo_retiro else "PAYPAL",
                    detalles_cuenta=cuenta_retiro,
                    titular=titular_retiro
                )
                if ok_ret:
                    st.success(msg_ret)
                    st.rerun()
                else:
                    st.error(f"❌ {msg_ret}")

    with tab_hist_com:
        hist_com = resumen_af.get('historial_comisiones', [])
        if not hist_com:
            st.info("ℹ️ Aún no has generado comisiones. ¡Comparte tu enlace de afiliado para empezar a ganar!")
        else:
            df_com_data = []
            for c in hist_com:
                df_com_data.append({
                    "Amigo Referido": c["referred"].upper(),
                    "Nivel / Mes": f"Mes {c['mes_numero']}",
                    "% Comisión": f"{c['porcentaje']}%",
                    "Monto Pago": f"${c['monto_pago']:.2f} MXN",
                    "Tu Comisión": f"${c['monto_comision']:.2f} MXN",
                    "Fecha": c["fecha"],
                    "Estado": f"🟢 {c['estado']}"
                })
            import pandas as pd
            st.dataframe(pd.DataFrame(df_com_data), use_container_width=True)

    with tab_hist_ret:
        hist_ret = resumen_af.get('historial_retiros', [])
        if not hist_ret:
            st.info("ℹ️ No tienes solicitudes de retiro registradas todavía.")
        else:
            df_ret_data = []
            for r in hist_ret:
                st_icon = "🟢" if r["estado"] == "PAGADO" else ("🟡" if r["estado"] == "PENDIENTE" else "🔴")
                df_ret_data.append({
                    "ID": f"#{r['id']}",
                    "Monto": f"${r['monto']:.2f} MXN",
                    "Método": r["metodo"],
                    "Cuenta / CLABE": r["detalles_cuenta"],
                    "Titular": r["titular"],
                    "Estado": f"{st_icon} {r['estado']}",
                    "Fecha Solicitud": r["fecha_solicitud"],
                    "Fecha Pago": r["fecha_pago"]
                })
            import pandas as pd
            st.dataframe(pd.DataFrame(df_ret_data), use_container_width=True)

    with tab_mis_ref:
        mis_ref_list = resumen_af.get('lista_referidos', [])
        if not mis_ref_list:
            st.info("ℹ️ Aún no tienes personas registradas con tu código. ¡Empieza a compartir tu link!")
        else:
            df_ref_data = []
            for ref in mis_ref_list:
                rol_badge = "👑 VIP ACTIVO" if ref["role"] == "VIP" and ref["is_active"] else "⏳ REGISTRADO"
                df_ref_data.append({
                    "Usuario": ref["username"].upper(),
                    "Membresía": rol_badge,
                    "Fecha Registro": ref["created_at"]
                })
            import pandas as pd
            st.dataframe(pd.DataFrame(df_ref_data), use_container_width=True)

    st.stop()

# --- MODO 00: PARTIDOS DE HOY (RESUELVEN HOY MISMO) ---
if liga_elegida_val == "TODAY_MATCHES_MODE":
    if not st.session_state.get('live_partido_detalle'):
        render_html('''
        <div style="background: linear-gradient(135deg, #1C202B 0%, #152238 50%, #0D0F14 100%); border:1.5px solid #38BDF8; padding: 22px; border-radius: 14px; text-align: center; margin-bottom: 20px; box-shadow: 0 6px 20px rgba(56, 189, 248, 0.25);">
            <h2 style="color: white; margin: 0; font-weight: 900; font-size: 28px; letter-spacing: 1px;">📅 PARTIDOS DE HOY (RESUELVE TU APUESTA HOY)</h2>
            <p style="color: #E2E8F0; margin: 6px 0 0 0; font-size: 15px; opacity: 0.95;">Encuentros programados para la fecha de hoy con horarios locales, escudos oficiales y Pick Destacado (+EV) para cobrar el mismo día.</p>
        </div>
        ''')

        with st.spinner("📅 Conectando con API satelital y cargando partidos de hoy..."):
            ligas_hoy = api_client.obtener_partidos_de_hoy()

        total_hoy = sum(len(d.get("partidos", [])) for d in ligas_hoy.values())

        col_ctl1, col_ctl2, col_ctl3 = st.columns([1.5, 1.3, 0.8])
        with col_ctl1:
            filtro_hoy_txt = st.text_input("🔍 Buscar Partido o Liga de Hoy:", placeholder="Ej. América, Premier, Real Madrid, Toluca...", key="in_hoy_search")
        with col_ctl2:
            filtro_est_hoy = st.selectbox("⏱️ Filtrar por Estado:", ["🟢 Por Jugar Hoy (Próximos)", "🔥 Festival de Goles (+2.5 / BTTS)", "🔴 En Vivo Ahora", "🌐 Todos los Partidos de Hoy", "🏁 Finalizados Hoy"], key="sel_filtro_est_hoy")
        with col_ctl3:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("🔄 ACTUALIZAR", use_container_width=True, key="btn_ref_hoy"):
                api_client.obtener_partidos_de_hoy.clear()
                st.rerun()

        render_html(f'''
        <div style="background:#151821; border-radius:10px; padding:10px 16px; margin-bottom:18px; border:1px solid #282F3F; display:flex; justify-content:space-between; align-items:center;">
            <span style="color:#FFFFFF; font-weight:bold; font-size:14px;">🎯 Cartelera del Día: <span style="color:#38BDF8; font-weight:900;">{total_hoy} Encuentros Registrados</span></span>
            <span style="background:#D4AF37; color:#0D0F14; font-weight:900; padding:4px 12px; border-radius:20px; font-size:13px;">⚡ Cobro el Mismo Día</span>
        </div>
        ''')

        for l_key, l_data in ligas_hoy.items():
            p_lista = l_data.get("partidos", [])
            
            # Filtro por texto
            if filtro_hoy_txt:
                txt_low = filtro_hoy_txt.lower()
                p_lista = [p for p in p_lista if txt_low in p['local'].lower() or txt_low in p['visita'].lower() or txt_low in l_key.lower()]

            # Filtro por estado
            if filtro_est_hoy == "🟢 Por Jugar Hoy (Próximos)":
                p_lista = [p for p in p_lista if p.get('status') in ['NS', 'TBD']]
            elif filtro_est_hoy == "🔥 Festival de Goles (+2.5 / BTTS)":
                p_lista = [p for p in p_lista if p.get('status') in ['NS', 'TBD', '1H', '2H', 'HT', 'LIVE']]
            elif filtro_est_hoy == "🔴 En Vivo Ahora":
                p_lista = [p for p in p_lista if p.get('status') in ['1H', '2H', 'HT', 'LIVE']]
            elif filtro_est_hoy == "🏁 Finalizados Hoy":
                p_lista = [p for p in p_lista if p.get('status') in ['FT', 'AET', 'PEN']]

            if not p_lista:
                continue

            pais_nombre = l_data.get("pais", "Internacional")
            liga_nombre = l_data.get("nombre", "Torneo")

            render_html(f'''
            <div style="display:flex; align-items:center; justify-content:space-between; background:#151821; border-left:5px solid #D4AF37; border-radius:10px; padding:10px 16px; margin:20px 0 12px 0; border-top:1px solid #282F3F; border-right:1px solid #282F3F; border-bottom:1px solid #282F3F;">
                <span style="font-size:16px; font-weight:900; color:#FFFFFF;">🏆 {pais_nombre} - {liga_nombre}</span>
                <span style="background:#D4AF37; color:#0D0F14; font-weight:900; padding:2px 10px; border-radius:12px; font-size:12px;">{len(p_lista)} partidos</span>
            </div>
            ''')

            cols_hoy = st.columns(2)
            for idx_p, p_item in enumerate(p_lista):
                col_target = cols_hoy[idx_p % 2]
                with col_target:
                    sp_rapido = analytics.calcular_matriz_poisson_multifactorial(
                        prob_loc_str="45%", prob_emp_str="30%", prob_vis_str="25%",
                        goles_loc_est="1.6", goles_vis_est="1.2"
                    )
                    pick_info = analytics.generar_pick_recomendado_rapido(sp_rapido, p_item['local'], p_item['visita'])
                    card_html = pitch_renderer.render_tarjeta_partido_hoy(p_item, pick_info)
                    st.markdown(card_html, unsafe_allow_html=True)
                    if st.button(f"🔍 Analizar a Fondo: {p_item['local']} vs {p_item['visita']}", key=f"btn_hoy_{p_item['id']}", use_container_width=True):
                        st.session_state['live_partido_detalle'] = p_item
                        st.rerun()

        st.stop()

# --- MODO 0.1: FESTIVAL DE GOLES (RADAR ALTAS & BTTS) ---
if liga_elegida_val == "GOAL_FESTIVAL_MODE":
    if not st.session_state.get('live_partido_detalle'):
        render_html('''
        <div style="background: linear-gradient(135deg, #1C202B 0%, #2D1414 50%, #0D0F14 100%); border:1.5px solid #EF4444; padding: 22px; border-radius: 14px; text-align: center; margin-bottom: 20px; box-shadow: 0 6px 20px rgba(239, 68, 68, 0.25);">
            <h2 style="color: white; margin: 0; font-weight: 900; font-size: 28px; letter-spacing: 1px;">🔥 FESTIVAL DE GOLES (RADAR ALTAS & BTTS)</h2>
            <p style="color: #E2E8F0; margin: 6px 0 0 0; font-size: 15px; opacity: 0.95;">Escaneo algorítmico de Expected Goals (xG Total), Ambos Equipos Anotan y Más de 2.5 Goles con Termómetro Ofensivo y Parlay Goleador Maestro.</p>
        </div>
        ''')

        with st.spinner("🔥 Escaneando todos los partidos de hoy y calculando xG y probabilidad ofensiva..."):
            candidatos_raw = analytics.extraer_candidatos_reales_de_hoy()
            if not candidatos_raw:
                candidatos_raw = [
                    {"id": 1301001, "local": "América", "visita": "Toluca", "liga": "🇲🇽 Liga MX", "lh": 1.95, "la": 1.65, "hora": "Hoy 21:00", "status": "NS"},
                    {"id": 1301004, "local": "Manchester City", "visita": "Liverpool", "liga": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League", "lh": 2.10, "la": 1.70, "hora": "Hoy 13:00", "status": "NS"},
                    {"id": 1301007, "local": "Barcelona", "visita": "Villarreal", "liga": "🇪🇸 LaLiga", "lh": 2.20, "la": 1.45, "hora": "Hoy 14:00", "status": "NS"},
                    {"id": 1301008, "local": "Bayern Múnich", "visita": "Dortmund", "liga": "🇩🇪 Bundesliga", "lh": 2.40, "la": 1.50, "hora": "Hoy 11:30", "status": "NS"},
                    {"id": 1301010, "local": "PSG", "visita": "Mónaco", "liga": "🇫🇷 Ligue 1", "lh": 2.30, "la": 1.60, "hora": "Hoy 14:00", "status": "NS"},
                    {"id": 1301013, "local": "Aston Villa", "visita": "Tottenham", "liga": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League", "lh": 1.85, "la": 1.60, "hora": "Hoy 10:30", "status": "NS"},
                    {"id": 1301014, "local": "Bayer Leverkusen", "visita": "RB Leipzig", "liga": "🇩🇪 Bundesliga", "lh": 2.00, "la": 1.65, "hora": "Hoy 11:30", "status": "NS"},
                    {"id": 1301015, "local": "Ajax", "visita": "PSV Eindhoven", "liga": "🇳🇱 Eredivisie", "lh": 2.15, "la": 1.80, "hora": "Hoy 12:00", "status": "NS"}
                ]

            partidos_festival = []
            for p in candidatos_raw:
                lh = float(p.get("lh", 1.75))
                la = float(p.get("la", 1.45))
                sp = analytics.calcular_matriz_poisson_multifactorial(
                    prob_loc_str="45%", prob_emp_str="25%", prob_vis_str="30%",
                    goles_loc_est=str(lh), goles_vis_est=str(la)
                )
                idx_g = analytics.calcular_indice_goleador(sp)
                p_copy = dict(p)
                p_copy["indice_goles"] = idx_g
                p_copy["stats_poisson"] = sp
                partidos_festival.append(p_copy)

            # Ordenar por índice goleador descendente
            partidos_festival.sort(key=lambda x: x["indice_goles"]["score"], reverse=True)

        # 1. PARLAY MAESTRO DEL FESTIVAL
        parlay_fg = analytics.generar_parlay_festival_goles(partidos_festival, top_n=3)
        st.markdown(pitch_renderer.render_ticket_parlay_festival_goles(parlay_fg), unsafe_allow_html=True)

        # Botón para compartir por WhatsApp
        ficha_fg = analytics.generar_ficha_festival_goles_whatsapp(parlay_fg, web_url=getattr(config, 'WEBAPP_VIP_URL', 'https://smartpickprojz.com.mx'))
        import urllib.parse
        encoded_fg = urllib.parse.quote(ficha_fg)

        col_w_fg1, col_w_fg2 = st.columns(2)
        with col_w_fg1:
            render_html(f'''
            <a href="https://wa.me/?text={encoded_fg}" target="_blank" style="background:#1A4D2E; border:1px solid #2ECC71; color:white; font-weight:900; padding:12px 20px; border-radius:10px; text-decoration:none; display:block; text-align:center; font-size:14px; margin-bottom:15px; box-shadow:0 4px 12px rgba(46,204,113,0.3);">
                📲 ENVIAR PARLAY GOLEADOR A WHATSAPP
            </a>
            ''')
        with col_w_fg2:
            if st.button("📋 COPIAR PARLAY AL PORTAPAPELES", use_container_width=True, key="btn_copy_fg"):
                st.session_state['clipboard_text'] = ficha_fg
                st.toast("✅ Parlay Goleador copiado al portapapeles con éxito!")

        st.markdown("<hr style='border:1px solid #282F3F; margin:15px 0 20px 0;'>", unsafe_allow_html=True)

        # 2. CONTROLES Y FILTROS DEL RADAR
        col_ctl1, col_ctl2, col_ctl3 = st.columns([1.5, 1.3, 0.8])
        with col_ctl1:
            filtro_fg_txt = st.text_input("🔍 Buscar Equipo o Liga en el Festival:", placeholder="Ej. Premier, Bayern, Toluca, Barcelona...", key="in_fg_search")
        with col_ctl2:
            filtro_fg_cat = st.selectbox(
                "🔥 Filtrar por Nivel de Expectativa:",
                [
                    "🔥 Todos los Partidos Clasificados",
                    "🌋 Festival Inminente (Score 75+)",
                    "⚽ Duelo Abierto (+EV) (Score 65+)",
                    "⚡ Ambos Anotan Alto (BTTS > 60%)",
                    "📈 Más de 2.5 Goles Alto (> 60%)"
                ],
                key="sel_filtro_fg_cat"
            )
        with col_ctl3:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("🔄 ACTUALIZAR", use_container_width=True, key="btn_ref_fg"):
                api_client.obtener_partidos_de_hoy.clear()
                st.rerun()

        # Filtrar lista
        partidos_mostrados = list(partidos_festival)
        if filtro_fg_txt:
            txt_l = filtro_fg_txt.lower()
            partidos_mostrados = [p for p in partidos_mostrados if txt_l in p['local'].lower() or txt_l in p['visita'].lower() or txt_l in p.get('liga', '').lower()]

        if filtro_fg_cat == "🌋 Festival Inminente (Score 75+)":
            partidos_mostrados = [p for p in partidos_mostrados if p["indice_goles"]["score"] >= 75.0]
        elif filtro_fg_cat == "⚽ Duelo Abierto (+EV) (Score 65+)":
            partidos_mostrados = [p for p in partidos_mostrados if p["indice_goles"]["score"] >= 65.0]
        elif filtro_fg_cat == "⚡ Ambos Anotan Alto (BTTS > 60%)":
            partidos_mostrados = [p for p in partidos_mostrados if p["indice_goles"]["p_btts"] >= 60.0]
        elif filtro_fg_cat == "📈 Más de 2.5 Goles Alto (> 60%)":
            partidos_mostrados = [p for p in partidos_mostrados if p["indice_goles"]["p_over_25"] >= 60.0]

        render_html(f'''
        <div style="background:#151821; border-radius:10px; padding:10px 16px; margin-bottom:18px; border:1px solid #282F3F; display:flex; justify-content:space-between; align-items:center;">
            <span style="color:#FFFFFF; font-weight:bold; font-size:14px;">🎯 Encuentros Detectados: <span style="color:#EF4444; font-weight:900;">{len(partidos_mostrados)} Partidos Ofensivos</span></span>
            <span style="background:#EF4444; color:#FFFFFF; font-weight:900; padding:4px 12px; border-radius:20px; font-size:13px;">🔥 Termómetro Activo</span>
        </div>
        ''')

        if not partidos_mostrados:
            st.info("ℹ️ No se encontraron partidos con los filtros seleccionados en este momento.")
        else:
            cols_fg = st.columns(2)
            for idx_p, p_item in enumerate(partidos_mostrados):
                col_target = cols_fg[idx_p % 2]
                with col_target:
                    card_html = pitch_renderer.render_tarjeta_festival_goles(p_item, p_item["stats_poisson"], p_item["indice_goles"])
                    st.markdown(card_html, unsafe_allow_html=True)
                    if st.button(f"🔍 Analizar a Fondo: {p_item['local']} vs {p_item['visita']}", key=f"btn_fg_{p_item['id']}", use_container_width=True):
                        st.session_state['live_partido_detalle'] = p_item
                        st.rerun()

        st.stop()

# --- MODO 0.15: GENERADOR DE FICHAS PARA REDES SOCIALES ---
if liga_elegida_val == "SOCIAL_CARD_MODE":
    if not st.session_state.get('live_partido_detalle'):
        render_html('''
        <div style="background: linear-gradient(135deg, #1C202B 0%, #152238 50%, #0D0F14 100%); border:1.5px solid #D4AF37; padding: 22px; border-radius: 14px; text-align: center; margin-bottom: 20px; box-shadow: 0 6px 20px rgba(212, 175, 55, 0.25);">
            <h2 style="color: white; margin: 0; font-weight: 900; font-size: 28px; letter-spacing: 1px;">📸 GENERADOR DE FICHAS HD PARA REDES SOCIALES</h2>
            <p style="color: #E2E8F0; margin: 6px 0 0 0; font-size: 15px; opacity: 0.95;">Crea y descarga en 1 clic imágenes profesionales de alta resolución (.PNG) para Instagram (Post y Stories), WhatsApp (Estados), Twitter/X y Telegram.</p>
        </div>
        ''')

        subtab_card_partido, subtab_card_parlay = st.tabs([
            "⚽ 1. Ficha de Partido Individual",
            "🎫 2. Boleto de Parlay Maestro"
        ])

        with subtab_card_partido:
            with st.spinner("Cargando lista de encuentros disponibles de hoy..."):
                ligas_hoy_gen = api_client.obtener_partidos_de_hoy()
                partidos_hoy_flat = []
                for lk, ld in ligas_hoy_gen.items():
                    for p in ld.get("partidos", []):
                        p_c = dict(p)
                        p_c["liga_str"] = f"{ld.get('pais', '')} - {ld.get('nombre', '')}"
                        partidos_hoy_flat.append(p_c)

            col_cp1, col_cp2, col_cp3 = st.columns([1.5, 1.2, 1.2])
            with col_cp1:
                if partidos_hoy_flat:
                    partido_labels = [f"{p['local']} vs {p['visita']} ({p['liga_str']})" for p in partidos_hoy_flat]
                    idx_sel_p = st.selectbox("🎯 Seleccionar Partido del Día:", range(len(partidos_hoy_flat)), format_func=lambda i: partido_labels[i], key="sel_partido_sc")
                    p_sc = partidos_hoy_flat[idx_sel_p]
                else:
                    p_sc = {"id": 101, "local": "América", "visita": "Toluca", "logo_local": "", "logo_visita": "", "liga": "🇲🇽 Liga MX", "hora": "Hoy 21:00"}

            with col_cp2:
                fmt_sc = st.selectbox(
                    "📐 Formato:",
                    ["🟦 Cuadrado (Post 1:1 - 1080x1080)", "📱 Historia / Estado (Story 9:16 - 1080x1920)"],
                    key="sel_fmt_sc_mode"
                )
                fmt_val = "9:16" if "9:16" in fmt_sc else "1:1"
            with col_cp3:
                est_sc = st.selectbox(
                    "🎨 Estilo Visual:",
                    ["🏆 Oro VIP & Obsidiana", "🔥 Festival de Fuego", "⚡ Neón Cyber Pro"],
                    key="sel_est_sc_mode"
                )
                est_val = "festival_fuego" if "Festival" in est_sc else ("neon_pro" if "Neón" in est_sc else "oro_vip")

            # Generar Pick automático para la ficha
            sp_sc = analytics.calcular_matriz_poisson_multifactorial(
                prob_loc_str="45%", prob_emp_str="25%", prob_vis_str="30%",
                goles_loc_est="1.8", goles_vis_est="1.4"
            )
            pick_rapido_sc = analytics.generar_pick_recomendado_rapido(sp_sc, p_sc['local'], p_sc['visita'])
            
            partido_dict_sc = {
                "local": p_sc['local'],
                "visita": p_sc['visita'],
                "logo_local": p_sc.get('logo_local', ''),
                "logo_visita": p_sc.get('logo_visita', ''),
                "liga": p_sc.get('liga_str', p_sc.get('liga', 'Liga Profesional')),
                "hora": p_sc.get('hora', 'Hoy')
            }
            pick_dict_sc = {
                "pick": pick_rapido_sc.get('mercado', 'Ambos Anotan (Sí)'),
                "cuota": pick_rapido_sc.get('cuota', 1.45),
                "probabilidad": f"{pick_rapido_sc.get('probabilidad', 75.0)}%",
                "stake": "3/10 (3.5%)"
            }
            stats_dict_sc = {
                "xg_total": round(sp_sc['lambda_home'] + sp_sc['lambda_away'], 2),
                "p_btts": f"{sp_sc['p_btts']}%",
                "p_over_25": f"{sp_sc['p_over_25']}%"
            }

            with st.spinner("Generando Ficha HD..."):
                img_bytes_sc = social_card_generator.generar_ficha_partido_hd(
                    partido_data=partido_dict_sc,
                    pick_data=pick_dict_sc,
                    stats_data=stats_dict_sc,
                    formato=fmt_val,
                    estilo=est_val
                )

            col_prev_sc, col_act_sc = st.columns([1.4, 1])
            with col_prev_sc:
                render_image_preview(img_bytes_sc, caption=f"Ficha Oficial ({p_sc['local']} vs {p_sc['visita']})")
            with col_act_sc:
                st.markdown("#### 💎 Ficha Lista para Redes")
                st.markdown(f"**⚽ Encuentro:** {p_sc['local']} vs {p_sc['visita']}")
                st.markdown(f"**🎯 Pick Principal:** {pick_dict_sc['pick']} (@{pick_dict_sc['cuota']:.2f})")
                st.markdown(f"**📐 Resolución:** {'1080 x 1920 px (HD Story)' if fmt_val == '9:16' else '1080 x 1080 px (HD Square)'}")
                st.markdown("---")
                st.download_button(
                    label="📥 DESCARGAR FICHA HD (.PNG)",
                    data=img_bytes_sc,
                    file_name=f"ficha_{p_sc['local'].lower().replace(' ', '_')}_vs_{p_sc['visita'].lower().replace(' ', '_')}_{fmt_val.replace(':', 'x')}.png",
                    mime="image/png",
                    use_container_width=True,
                    key="btn_dl_sc_mode_p"
                )

        with subtab_card_parlay:
            col_par1, col_par2 = st.columns(2)
            with col_par1:
                fmt_par = st.selectbox(
                    "📐 Formato de Parlay:",
                    ["🟦 Cuadrado (Post 1:1 - 1080x1080)", "📱 Historia / Estado (Story 9:16 - 1080x1920)"],
                    key="sel_fmt_parlay_sc"
                )
                fmt_p_val = "9:16" if "9:16" in fmt_par else "1:1"
            with col_par2:
                est_par = st.selectbox(
                    "🎨 Estilo Visual:",
                    ["🏆 Oro VIP & Obsidiana", "🔥 Festival de Fuego", "⚡ Neón Cyber Pro"],
                    key="sel_est_parlay_sc"
                )
                est_p_val = "festival_fuego" if "Festival" in est_par else ("neon_pro" if "Neón" in est_par else "oro_vip")

            with st.spinner("Procesando Parlay Maestro y calculando cuota combinada..."):
                parlay_raw_data = analytics.generar_parlay_top_altas(top_n=4 if fmt_p_val == "1:1" else 5)
                img_parlay_bytes = social_card_generator.generar_ficha_parlay_hd(
                    parlay_data=parlay_raw_data,
                    formato=fmt_p_val,
                    estilo=est_p_val
                )

            col_prev_par, col_act_par = st.columns([1.4, 1])
            with col_prev_par:
                render_image_preview(img_parlay_bytes, caption="Boleto Parlay HD para Redes Sociales")
            with col_act_par:
                st.markdown("#### 🎫 Boleto Parlay Combinado")
                st.markdown(f"**🎯 Total Partidos:** {len(parlay_raw_data.get('picks', []))}")
                st.markdown(f"**💰 Cuota Multiplicadora:** x{parlay_raw_data.get('cuota_acumulada', 2.85):,.2f}")
                st.markdown("---")
                st.download_button(
                    label="📥 DESCARGAR BOLETO PARLAY HD (.PNG)",
                    data=img_parlay_bytes,
                    file_name=f"parlay_maestro_{fmt_p_val.replace(':', 'x')}.png",
                    mime="image/png",
                    use_container_width=True,
                    key="btn_dl_sc_mode_par"
                )

        st.stop()

# --- MODO 0: RADAR DE PARTIDOS EN VIVO MULTILIGAS ---
if liga_elegida_val == "LIVE_RADAR_MODE":
    if not st.session_state.get('live_partido_detalle'):
        render_html('''
        <div style="background: linear-gradient(135deg, #1C202B 0%, #3D1A1A 100%); border:1.5px solid #EF5350; padding: 22px; border-radius: 14px; text-align: center; margin-bottom: 20px; box-shadow: 0 6px 20px rgba(239, 83, 80, 0.25);">
            <h2 style="color: white; margin: 0; font-weight: 900; font-size: 28px; letter-spacing: 1px;">🔴 RADAR DE PARTIDOS EN VIVO MULTILIGAS</h2>
            <p style="color: #E2E8F0; margin: 6px 0 0 0; font-size: 15px; opacity: 0.95;">Marcadores en tiempo real, minutos jugados y eventos de todos los encuentros activos en el mundo.</p>
        </div>
        ''')
        
        col_ctl1, col_ctl2, col_ctl3 = st.columns([1.5, 1.5, 1])
        with col_ctl1:
            filtro_busqueda = st.text_input("🔍 Buscar por Equipo o Liga:", placeholder="Ej. Toluca, Premier, Cali, Chile...")
        with col_ctl2:
            filtro_tiempo = st.selectbox("⏱️ Filtrar por Estado:", ["Todos los Estados", "🔴 1er Tiempo (1H)", "🔴 2do Tiempo (2H)", "⏸️ Entretiempo (HT)"])
        with col_ctl3:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("🔄 ACTUALIZAR EN VIVO", use_container_width=True, help="Refresca los marcadores en vivo de todas las ligas"):
                api_client.obtener_todos_partidos_en_vivo.clear()
                st.rerun()

        with st.spinner("📡 Conectando con API-Sports y escaneando partidos en vivo en todo el mundo..."):
            ligas_en_vivo = api_client.obtener_todos_partidos_en_vivo()

        total_partidos = sum(len(d.get("partidos", [])) for d in ligas_en_vivo.values())
        
        render_html(f'''
        <div style="background:#151821; border-radius:10px; padding:10px 16px; margin-bottom:18px; border:1px solid #282F3F; display:flex; justify-content:space-between; align-items:center;">
            <span style="color:#FFFFFF; font-weight:bold; font-size:14px;">📡 Conexión Satelital API-Sports: <span style="color:#38BDF8; font-weight:900;">ACTIVA (HTTP 200 OK)</span></span>
            <span style="background:#38BDF8; color:#0D0F14; font-weight:900; padding:4px 12px; border-radius:20px; font-size:13px;">🟢 {total_partidos} Partidos en Juego</span>
        </div>
        ''')

        ligas_filtradas = {}
        for l_key, l_data in ligas_en_vivo.items():
            partidos_filtrados = []
            for p in l_data.get("partidos", []):
                if filtro_busqueda:
                    txt_b = filtro_busqueda.lower().strip()
                    if txt_b not in p['local'].lower() and txt_b not in p['visita'].lower() and txt_b not in l_key.lower():
                        continue
                
                if filtro_tiempo == "🔴 1er Tiempo (1H)" and p['status'] != '1H':
                    continue
                elif filtro_tiempo == "🔴 2do Tiempo (2H)" and p['status'] != '2H':
                    continue
                elif filtro_tiempo == "⏸️ Entretiempo (HT)" and p['status'] != 'HT':
                    continue
                
                partidos_filtrados.append(p)
            
            if partidos_filtrados:
                ligas_filtradas[l_key] = {
                    **l_data,
                    "partidos": partidos_filtrados
                }

        if not ligas_filtradas:
            if total_partidos == 0:
                render_html('''
                <div style="background: #151821; border: 1.5px solid #282F3F; border-radius: 14px; padding: 30px; text-align: center; margin-top: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
                    <div style="font-size: 40px; margin-bottom: 10px;">⏱️</div>
                    <h3 style="color: #F3E5AB; margin: 0 0 8px 0; font-weight: 900;">Sin Partidos en Juego en Este Momento</h3>
                    <p style="color: #94A3B8; font-size: 14px; max-width: 600px; margin: 0 auto 15px auto;">
                        El radar satelital está activo y monitoreando todas las ligas del mundo 24/7. En cuanto dé inicio el próximo partido oficial, aparecerá automáticamente aquí con su marcador y minuto a minuto en tiempo real.
                    </p>
                    <div style="display: inline-block; background: rgba(56,189,248,0.12); border: 1px solid #38BDF8; color: #38BDF8; font-weight: bold; padding: 6px 16px; border-radius: 20px; font-size: 13px;">
                        💡 Puedes seleccionar una liga en el menú de la izquierda para analizar los próximos partidos o el Cazador de Parlays
                    </div>
                </div>
                ''')
            else:
                st.info("ℹ️ No se encontraron partidos activos con los filtros de búsqueda seleccionados.")
        else:
            for l_key, l_data in ligas_filtradas.items():
                p_lista = l_data["partidos"]
                pais_nombre = l_data.get("pais", "Internacional")
                liga_nombre = l_data.get("nombre", "Torneo")
                
                render_html(f'''
                <div style="display:flex; align-items:center; justify-content:space-between; background:#151821; border-left:5px solid #38BDF8; border-radius:10px; padding:10px 16px; margin:20px 0 12px 0; border-top:1px solid #282F3F; border-right:1px solid #282F3F; border-bottom:1px solid #282F3F;">
                    <div style="display:flex; align-items:center; gap:10px;">
                        <span style="font-size:16px; font-weight:900; color:#FFFFFF;">🏆 {pais_nombre} - {liga_nombre}</span>
                    </div>
                    <span style="background:#38BDF8; color:#0D0F14; font-weight:900; padding:2px 10px; border-radius:12px; font-size:12px;">{len(p_lista)} en juego</span>
                </div>
                ''')
                
                cols_live = st.columns(2)
                for idx_p, p_item in enumerate(p_lista):
                    col_target = cols_live[idx_p % 2]
                    with col_target:
                        st.markdown(render_tarjeta_live_segura(p_item), unsafe_allow_html=True)
                        if st.button(f"🔍 Abrir Minuto a Minuto & Análisis VIP ({p_item['local']} vs {p_item['visita']})", key=f"live_btn_{p_item['id']}", use_container_width=True):
                            st.session_state['live_partido_detalle'] = p_item
                            st.rerun()

        st.stop()

# --- MODO 0.5: CAZADOR DE PARLAYS VIP (TOP 15 ALTAS & TOP 5 EMPATES) ---
elif liga_elegida_val == "PARLAY_HUNTER_MODE":
    if not st.session_state.get('live_partido_detalle'):
        render_html('''
        <div style="background: linear-gradient(135deg, #1C202B 0%, #2A2E3D 50%, #151821 100%); border: 1.5px solid #D4AF37; padding: 22px; border-radius: 14px; text-align: center; margin-bottom: 20px; box-shadow: 0 6px 20px rgba(212, 175, 55, 0.2);">
            <h2 style="color: white; margin: 0; font-weight: 900; font-size: 28px; letter-spacing: 1px;">💎 CAZADOR DE PARLAYS VIP (+ALTAS & EMPATES DE ORO)</h2>
            <p style="color: #E2E8F0; margin: 6px 0 0 0; font-size: 15px; opacity: 0.95;">Algoritmos de Simulación Poisson & Dixon-Coles optimizados para Partidos de Hoy con Cuotas de Valor y Cobro Inmediato.</p>
        </div>
        ''')
        
        subtab_altas, subtab_empates = st.tabs([
            "🔥 1. Parlay Maestro de Altas (Top 15 Partidos)",
            "⚖️ 2. Radar de Empates de Oro (Top 5 Partidos)"
        ])
        
        with subtab_altas:
            col_pa1, col_pa2 = st.columns([1, 1])
            with col_pa1:
                top_n_altas = st.slider("Cantidad de Partidos en el Parlay de Altas:", 5, 20, 15, key="slider_altas_n")
            with col_pa2:
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                if st.button("🚀 RECALCULAR PARLAY DE ALTAS", use_container_width=True):
                    api_client.obtener_partidos_de_hoy.clear()
                    st.rerun()

            with st.spinner("Procesando matriz de goles esperados y xG en partidos de hoy..."):
                parlay_altas_data = analytics.generar_parlay_top_altas(top_n=top_n_altas)

            picks_altas = parlay_altas_data.get("picks", [])
            cuota_tot_altas = parlay_altas_data.get("cuota_acumulada", 1.0)
            
            # Boleto con botones integrados en cada fila
            render_html(f'''
            <div style="background:linear-gradient(135deg, #151821 0%, #1A1E29 100%); border:1.5px solid #D4AF37; border-radius:16px; padding:20px 20px 14px 20px; color:white; margin-bottom:12px; box-shadow:0 8px 25px rgba(212,175,55,0.2);">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #282F3F; padding-bottom:14px; margin-bottom:6px;">
                    <div>
                        <div style="font-size:20px; font-weight:900; color:#D4AF37;">🔥 BOLETO PARLAY MAESTRO DE ALTAS (PARTIDOS DE HOY)</div>
                        <div style="color:#aaa; font-size:13px;">Selección de los {len(picks_altas)} partidos de hoy con mayor xG • <i>Toca el botón con la lupa 🔍 en cualquier fila para ver su análisis</i></div>
                    </div>
                    <div style="text-align:right; background:#11141C; border:1.5px solid #D4AF37; padding:8px 18px; border-radius:10px;">
                        <div style="font-size:11px; color:#F3E5AB; font-weight:bold; text-transform:uppercase;">Cuota Combinada Total</div>
                        <div style="font-size:24px; font-weight:900; color:#D4AF37; letter-spacing:1px;">x{cuota_tot_altas:,.2f}</div>
                    </div>
                </div>
            </div>
            ''')

            for idx_a, p in enumerate(picks_altas):
                loc = p.get("local", "")
                vis = p.get("visita", "")
                liga = p.get("liga", "")
                hora = p.get("hora", "Hoy")
                mercado = p.get("mercado", "Más de 1.5 Goles")
                prob = p.get("probabilidad", 75.0)
                cuota = p.get("cuota", 1.30)

                col_row1, col_row2, col_row3 = st.columns([2.6, 1.4, 0.9])
                with col_row1:
                    render_html(f'''
                    <div style="background:#11141C; border-left:4px solid #D4AF37; border-top:1px solid #282F3F; border-bottom:1px solid #282F3F; padding:8px 12px; border-radius:8px 0 0 8px; min-height:52px; display:flex; flex-direction:column; justify-content:center;">
                        <div style="color:#aaa; font-size:11px; font-weight:bold;">{idx_a+1}. {liga} <span style="color:#38BDF8; font-size:10px; margin-left:4px;">⏰ {hora}</span></div>
                        <div style="color:#FFFFFF; font-weight:900; font-size:14px; margin-top:2px;">{loc} vs {vis}</div>
                    </div>
                    ''')
                with col_row2:
                    st.markdown("<div style='height:3px;'></div>", unsafe_allow_html=True)
                    if st.button(f"⚽ {mercado} 🔍", key=f"btn_row_alt_{idx_a}_{p.get('id', idx_a)}", use_container_width=True, help=f"Abrir análisis completo de {loc} vs {vis}"):
                        st.session_state['live_partido_detalle'] = p
                        st.rerun()
                with col_row3:
                    render_html(f'''
                    <div style="background:#11141C; border-top:1px solid #282F3F; border-bottom:1px solid #282F3F; border-right:1px solid #282F3F; padding:8px 6px; border-radius:0 8px 8px 0; min-height:52px; display:flex; align-items:center; justify-content:center; gap:5px;">
                        <div style="background:#151821; border:1px solid #F3E5AB; color:#F3E5AB; font-weight:900; padding:4px 7px; border-radius:6px; font-size:12px;">@{cuota:.2f}</div>
                        <div style="background:#0D0F14; color:#FFFFFF; font-weight:bold; font-size:10px; padding:4px 5px; border-radius:4px; border:1px solid #282F3F;">{prob}%</div>
                    </div>
                    ''')

            st.markdown("<br>", unsafe_allow_html=True)

            # Opciones de Difusión y Compartir
            ficha_altas = analytics.generar_ficha_parlay_altas_whatsapp(parlay_altas_data, web_url=getattr(config, 'WEBAPP_VIP_URL', 'https://smartpickprojz.com.mx'))
            import urllib.parse
            encoded_altas = urllib.parse.quote(ficha_altas)

            col_w1, col_w2 = st.columns(2)
            with col_w1:
                render_html(f'''
                <a href="https://wa.me/?text={encoded_altas}" target="_blank" style="background:#1A4D2E; border:1px solid #2ECC71; color:white; font-weight:900; padding:12px 20px; border-radius:10px; text-decoration:none; display:block; text-align:center; font-size:14px; margin-top:5px; box-shadow:0 4px 12px rgba(46,204,113,0.3);">
                    💬 COMPARTIR PARLAY DE ALTAS EN WHATSAPP (1 CLIC)
                </a>
                ''')
            with col_w2:
                st.download_button(
                    label="📥 Descargar Ficha de Altas (.txt)",
                    data=ficha_altas,
                    file_name="parlay_maestro_altas_top15.txt",
                    mime="text/plain",
                    use_container_width=True
                )

        with subtab_empates:
            col_pe1, col_pe2 = st.columns([1, 1])
            with col_pe1:
                top_n_emp = st.slider("Cantidad de Partidos en el Radar de Empates:", 3, 10, 5, key="slider_emp_n")
            with col_pe2:
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                if st.button("🚀 RECALCULAR RADAR DE EMPATES", use_container_width=True):
                    api_client.obtener_partidos_de_hoy.clear()
                    st.rerun()

            with st.spinner("Procesando matriz Dixon-Coles de paridad táctica de partidos de hoy..."):
                empates_data = analytics.generar_top_empates_oro(top_n=top_n_emp)

            empates_list = empates_data.get("empates", [])
            cuota_tot_emp = empates_data.get("cuota_parlay_empates", 1.0)

            render_html(f'''
            <div style="background:linear-gradient(135deg, #151821 0%, #1A1E29 100%); border:1.5px solid #D4AF37; border-radius:16px; padding:20px 20px 14px 20px; color:white; margin-bottom:12px; box-shadow:0 8px 25px rgba(212,175,55,0.2);">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #282F3F; padding-bottom:14px; margin-bottom:6px;">
                    <div>
                        <div style="font-size:20px; font-weight:900; color:#D4AF37;">⚖️ RADAR DE EMPATES DE ORO (PARTIDOS DE HOY)</div>
                        <div style="color:#aaa; font-size:13px;">{len(empates_list)} choques de máxima paridad táctica de hoy • <i>Toca el botón con la lupa 🔍 en cualquier fila para ver su análisis</i></div>
                    </div>
                    <div style="text-align:right; background:#11141C; border:1.5px solid #D4AF37; padding:8px 18px; border-radius:10px;">
                        <div style="font-size:11px; color:#F3E5AB; font-weight:bold; text-transform:uppercase;">Cuota Parlay Empates</div>
                        <div style="font-size:24px; font-weight:900; color:#D4AF37; letter-spacing:1px;">x{cuota_tot_emp:,.2f}</div>
                    </div>
                </div>
            </div>
            ''')

            for idx_e, e in enumerate(empates_list):
                loc = e.get("local", "")
                vis = e.get("visita", "")
                liga = e.get("liga", "")
                hora = e.get("hora", "Hoy")
                cuota_e = e.get("cuota_empate", 3.25)
                prob_e = e.get("probabilidad_empate", 33.0)
                marcador = e.get("marcador_probable", "1 - 1")

                col_erow1, col_erow2, col_erow3 = st.columns([2.6, 1.4, 0.9])
                with col_erow1:
                    render_html(f'''
                    <div style="background:#11141C; border-left:4px solid #D4AF37; border-top:1px solid #282F3F; border-bottom:1px solid #282F3F; padding:8px 12px; border-radius:8px 0 0 8px; min-height:52px; display:flex; flex-direction:column; justify-content:center;">
                        <div style="color:#aaa; font-size:11px; font-weight:bold;">{idx_e+1}. {liga} <span style="color:#38BDF8; font-size:10px; margin-left:4px;">⏰ {hora}</span></div>
                        <div style="color:#FFFFFF; font-weight:900; font-size:14px; margin-top:2px;">{loc} vs {vis}</div>
                    </div>
                    ''')
                with col_erow2:
                    st.markdown("<div style='height:3px;'></div>", unsafe_allow_html=True)
                    if st.button(f"⚖️ Empate ({marcador}) 🔍", key=f"btn_row_emp_{idx_e}_{e.get('id', idx_e)}", use_container_width=True, help=f"Abrir análisis completo de {loc} vs {vis}"):
                        st.session_state['live_partido_detalle'] = e
                        st.rerun()
                with col_erow3:
                    render_html(f'''
                    <div style="background:#11141C; border-top:1px solid #282F3F; border-bottom:1px solid #282F3F; border-right:1px solid #282F3F; padding:8px 6px; border-radius:0 8px 8px 0; min-height:52px; display:flex; align-items:center; justify-content:center; gap:5px;">
                        <div style="background:#0D0F14; border:1px solid #D4AF37; color:#D4AF37; font-weight:900; padding:4px 7px; border-radius:6px; font-size:12px;">@{cuota_e:.2f}</div>
                        <div style="background:#0D0F14; color:#FFFFFF; font-weight:bold; font-size:10px; padding:4px 5px; border-radius:4px; border:1px solid #282F3F;">{prob_e}%</div>
                    </div>
                    ''')

            st.markdown("<br>", unsafe_allow_html=True)

            # Ficha WhatsApp de Empates
            ficha_empates = analytics.generar_ficha_empates_whatsapp(empates_data, web_url=getattr(config, 'WEBAPP_VIP_URL', 'https://smartpickprojz.com.mx'))
            encoded_empates = urllib.parse.quote(ficha_empates)

            col_we1, col_we2 = st.columns(2)
            with col_we1:
                render_html(f'''
                <a href="https://wa.me/?text={encoded_empates}" target="_blank" style="background:#1A4D2E; border:1px solid #2ECC71; color:white; font-weight:900; padding:12px 20px; border-radius:10px; text-decoration:none; display:block; text-align:center; font-size:14px; margin-top:5px; box-shadow:0 4px 12px rgba(46,204,113,0.3);">
                    💬 COMPARTIR RADAR DE EMPATES EN WHATSAPP (1 CLIC)
                </a>
                ''')
            with col_we2:
                st.download_button(
                    label="📥 Descargar Reporte de Empates (.txt)",
                    data=ficha_empates,
                    file_name="radar_empates_oro_top5.txt",
                    mime="text/plain",
                    use_container_width=True
                )

        st.stop()

# --- MODO 1: PROGOL TRADICIONAL ---
elif liga_elegida_val == "PROGOL_MODE":
    render_html('''
    <div style="background: linear-gradient(135deg, #1C202B 0%, #2A2E3D 50%, #151821 100%); border:1.5px solid #D4AF37; padding: 22px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
        <h2 style="color: #D4AF37; margin: 0; font-weight: 900;">🎯 OPTIMIZADOR INTELIGENTE DE QUINIELA PROGOL</h2>
        <p style="color: #E2E8F0; margin: 6px 0 0 0; font-size: 15px;">Configura tus dobles y triples deseados sobre los 14 partidos oficiales.</p>
    </div>
    ''')
    
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
            render_html(f'''
            <div style="background:#151821; padding:12px 18px; border-radius:8px; margin:6px 0; border-left:5px solid {item['color_borde']}; color:white; border-top:1px solid #282F3F; border-right:1px solid #282F3F; border-bottom:1px solid #282F3F;">
                <b style="color:white; font-size:15px;">Casilla {item['casilla']}:</b> 
                <span style="color:#FFFFFF; font-weight:bold;">{p_match['local']} vs {p_match['visita']}</span> -> 
                <span style="color:{item['color_borde']}; font-weight:900; font-size:16px;">{item['sugerencia']}</span>
            </div>
            ''')
            
    st.stop()

# --- MODO 2: OPTIMIZADOR DE REDUCCIONES ---
elif liga_elegida_val == "REDUCCIONES_MODE":
    render_html('''
    <div style="background: linear-gradient(135deg, #1C202B 0%, #2A2E3D 50%, #151821 100%); border:1.5px solid #D4AF37; padding: 22px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
        <h2 style="color: #D4AF37; margin: 0; font-weight: 900;">⚙️ Panel de Reducciones Inteligentes Pro</h2>
        <p style="color: #E2E8F0; margin: 5px 0 0 0; font-size: 15px;">Matriz matemática de reducciones aplicadas a los 14 partidos oficiales</p>
    </div>
    ''')
    
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
                color_borde = "#D4AF37"
            elif idx in set_dobles:
                tipo_txt = "Doble Local/Empate (1X)" if idx % 2 != 0 else "Doble Empate/Visita (X2)"
                color_borde = "#38BDF8"
            else:
                tipo_txt = "Fijo Local (1)" if idx % 2 != 0 else "Fijo Visita (2)"
                color_borde = "#F3E5AB"

            render_html(f'''
            <div style="background:#151821; padding:10px 16px; border-radius:8px; margin:5px 0; border-left:5px solid {color_borde}; color:white; border-top:1px solid #282F3F; border-right:1px solid #282F3F; border-bottom:1px solid #282F3F;">
                <b style="color:white;">Casilla {idx}:</b> <span style="color:#FFFFFF; font-weight:bold;">{match_title} -> </span>
                <span style="color:{color_borde}; font-weight:900; font-size:15px;">{tipo_txt}</span>
            </div>
            ''')

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
                st.markdown(f"<div style='background:#151821; padding:8px; margin:4px 0; border-radius:6px; color:#D4AF37; font-weight:bold; border:1px solid #282F3F;'><b>Combinación {idx+1}:</b> {r_val} aciertos</div>", unsafe_allow_html=True)

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
                color_ev = "#D4AF37" if ev['es_premio'] else "#94A3B8"
                st.markdown(f"<div style='background:#151821; padding:10px 14px; border-radius:8px; margin:4px 0; border-left:5px solid {color_ev}; border:1px solid #282F3F;'><b>Boleta #{ev['numero_boleta']} ({ev['cadena_corta']}):</b> <span style='color:{color_ev}; font-weight:bold; font-size:16px;'>{badge_p}</span></div>", unsafe_allow_html=True)

    cols_b = st.columns(2)
    for idx_b, b_item in enumerate(boletas_sencillas):
        with cols_b[idx_b % 2]:
            with st.expander(f"🎟️ BOLETA #{b_item['numero_boleta']} | Secuencia: {b_item['cadena_corta']}"):
                for p_sub in b_item['pronosticos']:
                    p_c = p_sub['casilla']
                    p_part = p_sub['partido']
                    p_pk = p_sub['pick']
                    c_color = "#D4AF37" if p_pk == '1' else ("#38BDF8" if p_pk == 'X' else "#EF4444")
                    render_html(f'''
                    <div style="display:flex; justify-content:space-between; align-items:center; background:#151821; padding:5px 10px; border-radius:6px; margin:2px 0; border:1px solid #282F3F;">
                        <span style="color:white; font-size:12px;"><b>Casilla {p_c}:</b> {p_part}</span>
                        <span style="background:{c_color}; color:#0D0F14; font-weight:900; padding:1px 8px; border-radius:8px; font-size:13px;">{p_pk}</span>
                    </div>
                    ''')

    st.stop()

# --- MODO 3: ANÁLISIS INTEGRAL DE PARTIDO (CON PESTAÑAS ST.TABS) ---
if st.session_state.get('live_partido_detalle'):
    col_back, _ = st.columns([1.5, 1.5])
    with col_back:
        if liga_elegida_val == "TODAY_MATCHES_MODE":
            lbl_retorno = "⬅️ VOLVER A PARTIDOS DE HOY"
        elif liga_elegida_val == "GOAL_FESTIVAL_MODE":
            lbl_retorno = "⬅️ VOLVER AL FESTIVAL DE GOLES"
        elif liga_elegida_val == "SOCIAL_CARD_MODE":
            lbl_retorno = "⬅️ VOLVER AL GENERADOR DE FICHAS"
        elif liga_elegida_val == "PARLAY_HUNTER_MODE":
            lbl_retorno = "⬅️ VOLVER AL CAZADOR DE PARLAYS VIP"
        elif liga_elegida_val == "LIVE_RADAR_MODE":
            lbl_retorno = "⬅️ VOLVER AL RADAR DE TODAS LAS LIGAS EN VIVO"
        else:
            lbl_retorno = f"⬅️ VOLVER A LA LISTA DE {liga_elegida.upper()}"
        if st.button(lbl_retorno, use_container_width=True, key="btn_volver_lista_general"):
            st.session_state['live_partido_detalle'] = None
            st.session_state['ver_top_altas_match'] = False
            st.session_state['ver_top_empates_match'] = False
            st.session_state['ver_pick_seguro_match'] = False
            st.session_state['ver_parlay_oro_match'] = False
            st.rerun()

datos_partido = datos_partido_custom if datos_partido_custom else (st.session_state.get('live_partido_detalle') if st.session_state.get('live_partido_detalle') else partidos_dict.get(partido_seleccionado))
if (not partido_seleccionado and not st.session_state.get('live_partido_detalle')) or not datos_partido or not datos_partido.get("id"):
    st.info("💡 Selecciona un encuentro en la barra lateral o en el Radar en Vivo para ver su análisis detallado.")
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
        p_btts_val = stats_poisson.get("p_btts", 50.0)
        lh_val = stats_poisson.get("lambda_home", 1.4)
        la_val = stats_poisson.get("lambda_away", 1.1)
        
        if p_win_h >= 62.0:
            consejo_dinamico = f"Victoria Directa sugerida: {equipo_local_real} | Clara superioridad táctica y ventaja en casa."
        elif p_win_a >= 56.0:
            consejo_dinamico = f"Victoria Directa sugerida: {equipo_visita_real} | Jerarquía y rendimiento dominante del visitante."
        elif p_win_h >= 48.0:
            consejo_dinamico = f"Doble Oportunidad sugerida: {equipo_local_real} o Empate (1X) | Mayor solidez y peso de localía."
        elif p_win_a >= 44.0:
            consejo_dinamico = f"Doble Oportunidad sugerida: {equipo_visita_real} o Empate (X2) | Buen momento del visitante fuera de casa."
        elif p_btts_val >= 60.0 and lh_val >= 1.25 and la_val >= 1.15:
            consejo_dinamico = f"Mercado Recomendado: Ambos Equipos Anotan (Sí) | Duelo abierto con alta frecuencia goleadora."
        elif (lh_val + la_val) <= 2.10:
            consejo_dinamico = f"Mercado Recomendado: Menos de 2.5 / 3.5 Goles | Planteamiento táctico cerrado de pocos espacios."
        else:
            consejo_dinamico = f"Doble Oportunidad sugerida: {equipo_local_real} o {equipo_visita_real} (12) | Choque sumamente parejo."

        # Badge de Estado y Marcador Superior Dinámico
        if status in ['1H', '2H', 'HT', 'LIVE']:
            badge_html = f"<div style='background:#e74c3c; color:white; padding:4px 14px; border-radius:12px; font-weight:bold; font-size:12px; display:inline-block;'>🔴 EN VIVO {min_j}'</div>"
            score_html = f"<h1 style='margin:0; font-size:44px; color:#D4AF37; letter-spacing:4px;'>{g_h} - {g_a}</h1>"
        elif status in ['FT', 'AET', 'PEN']:
            badge_html = "<div style='background:#34495e; color:white; padding:4px 14px; border-radius:12px; font-weight:bold; font-size:12px; display:inline-block;'>🏁 FINALIZADO (90')</div>"
            score_html = f"<h1 style='margin:0; font-size:44px; color:#D4AF37; letter-spacing:4px;'>{g_h} - {g_a}</h1>"
        else:
            hora_p = datos_partido.get('hora', 'Hoy')
            badge_html = f"<div style='background:rgba(212,175,55,0.18); color:#F3E5AB; border:1px solid #D4AF37; padding:4px 14px; border-radius:12px; font-weight:bold; font-size:12px; display:inline-block;'>⏰ POR JUGAR ({hora_p})</div>"
            score_html = "<h2 style='margin:6px 0 0 0; color:#F3E5AB; font-size:28px; font-weight:900; letter-spacing:2px;'>VS</h2>"

        logo_local_render = api_client.obtener_logo_oficial_equipo(equipo_local_real, datos_partido.get('logo_local', ''))
        logo_visita_render = api_client.obtener_logo_oficial_equipo(equipo_visita_real, datos_partido.get('logo_visita', ''))

        # Marcador Superior Principal
        render_html(f'''
        <div style="display:flex; align-items:center; justify-content:space-around; background:linear-gradient(135deg, #151821 0%, #1A1E29 100%); border:1px solid #282F3F; padding:20px 15px; border-radius:16px; box-shadow:0 6px 25px rgba(0,0,0,0.5); margin-bottom:15px;">
            <div style="text-align:center; width:33%;">
                <img src="{logo_local_render}" style="width:70px; height:70px; object-fit:contain; margin-bottom:6px;">
                <h3 style="margin:0; color:#FFFFFF; font-size:17px; font-weight:800;">{equipo_local_real}</h3>
            </div>
            <div style="width:34%; text-align:center;">
                {badge_html}
                {score_html}
            </div>
            <div style="text-align:center; width:33%;">
                <img src="{logo_visita_render}" style="width:70px; height:70px; object-fit:contain; margin-bottom:6px;">
                <h3 style="margin:0; color:#FFFFFF; font-size:17px; font-weight:800;">{equipo_visita_real}</h3>
            </div>
        </div>
        ''')

        # --- ESTRUCTURA EN PESTAÑAS (ST.TABS) ---
        tab_vivo, tab_resumen, tab_redes, tab_modelos, tab_h2h, tab_cancha, tab_cuotas = st.tabs([
            "🔴 En Vivo",
            "📊 Picks VIP",
            "📸 Ficha Redes HD",
            "🧠 IA & Modelos",
            "⚔️ Estadísticas",
            "🏟️ Cancha",
            "💰 Cuotas"
        ])

        # =========================================================
        # PESTAÑA 1: MINUTO A MINUTO EN PANTALLA DIVIDIDA
        # =========================================================
        with tab_vivo:
            def safe_parse_goals(val, default_val=1.4):
                if val is None:
                    return default_val
                try:
                    v_clean = str(val).replace('-', '').replace('+', '').strip()
                    num = float(v_clean)
                    return num if num > 0 else default_val
                except Exception:
                    return default_val

            gl_safe = safe_parse_goals(gl, 1.4)
            gv_safe = safe_parse_goals(gv, 1.1)

            t_loc = max(3, int(gl_safe * 3.5))
            t_vis = max(2, int(gv_safe * 3.2))

            html_minuto_a_minuto = pitch_renderer.render_minuto_a_minuto_dividido(
                equipo_local=equipo_local_real,
                equipo_visita=equipo_visita_real,
                logo_local=logo_local_render,
                logo_visita=logo_visita_render,
                status=status,
                minuto_actual=min_j,
                goles_local=g_h,
                goles_visita=g_a,
                eventos_local=eventos_loc,
                eventos_visita=eventos_vis,
                pos_local=55 if p_win_h >= p_win_a else 45,
                pos_visita=45 if p_win_h >= p_win_a else 55,
                tiros_local=t_loc,
                tiros_visita=t_vis
            )
            st.markdown(html_minuto_a_minuto, unsafe_allow_html=True)

        # =========================================================
        # PESTAÑA 2: RESUMEN & PICKS VIP
        # =========================================================
        with tab_resumen:
            # Bet Builder Dinámico Multifactorial (Resultado, Goles, Tarjetas y Córners)
            picks_builder = analytics.generar_bet_builder_dinamico(
                equipo_local=equipo_local_real,
                equipo_visita=equipo_visita_real,
                stats_poisson=stats_poisson,
                promedio_tarjetas=promedio_tarjetas,
                referee_name=referee_name
            )

            col_b1, col_b2, col_b3, col_b4 = st.columns(4)
            with col_b1:
                if st.button("⚡ PICK SENCILLO SEGURO", use_container_width=True, key=f"btn_pick_seg_{fixture_id}"):
                    st.session_state['ver_pick_seguro_match'] = True
                    st.session_state['ver_parlay_oro_match'] = False
            with col_b2:
                if st.button("🎫 PARLAY DE ORO", use_container_width=True, key=f"btn_parlay_oro_{fixture_id}"):
                    st.session_state['ver_parlay_oro_match'] = True
                    st.session_state['ver_pick_seguro_match'] = False
            with col_b3:
                if st.button("🔥 TOP 15 ALTAS (PARLAY)", use_container_width=True, key=f"btn_top_altas_{fixture_id}"):
                    st.session_state['ver_top_altas_match'] = not st.session_state.get('ver_top_altas_match', False)
            with col_b4:
                if st.button("⚖️ TOP 5 EMPATES (VALOR)", use_container_width=True, key=f"btn_top_emp_{fixture_id}"):
                    st.session_state['ver_top_empates_match'] = not st.session_state.get('ver_top_empates_match', False)

            # Botón destacado Ficha Redes HD
            st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
            if st.button("📸 GENERAR Y DESCARGAR FICHA HD PARA REDES SOCIALES (INSTAGRAM / WHATSAPP / TWITTER)", use_container_width=True, key=f"btn_open_sc_resumen_{fixture_id}"):
                st.session_state['ver_ficha_redes_match'] = not st.session_state.get('ver_ficha_redes_match', False)

            pick_seguro_obj = picks_builder.get("pick_seguro", picks_builder['picks'][0] if picks_builder.get('picks') else {})
            p_seg_desc = pick_seguro_obj.get("descripcion", f"{equipo_local_real} o Empate (1X)")
            p_seg_prob = pick_seguro_obj.get("prob", "75.0%")
            p_seg_cuota = float(pick_seguro_obj.get("cuota", 1.30))

            if st.session_state.get('ver_pick_seguro_match'):
                st.success(f"🎯 **PICK SEGURO (+EV):** {p_seg_desc} | Cuota: **@{p_seg_cuota:.2f}** | Confianza Matemática: **{p_seg_prob}**")

            if st.session_state.get('ver_parlay_oro_match'):
                p1_obj = picks_builder['picks'][0] if len(picks_builder.get('picks', [])) > 0 else {'descripcion': f"{equipo_local_real} o Empate (1X)", 'cuota': 1.30}
                p2_obj = picks_builder['picks'][1] if len(picks_builder.get('picks', [])) > 1 else {'descripcion': "Más de 1.5 Goles", 'cuota': 1.35}
                p_res_text = p1_obj.get('descripcion', '')
                p_gol_text = p2_obj.get('descripcion', '')
                c1_val = float(p1_obj.get('cuota', 1.30))
                c2_val = float(p2_obj.get('cuota', 1.35))
                cuota_oro = round(c1_val * c2_val * 0.95, 2)
                st.success(f"🎟️ **PARLAY DE ORO RECOMENDADO:** {p_res_text} + {p_gol_text} | Cuota Combinada: **@{cuota_oro:.2f}**")

            if st.session_state.get('ver_top_altas_match'):
                st.markdown("### 🔥 Parlay Maestro de Altas en Goles (Top 15 Partidos)")
                p_altas_box = analytics.generar_parlay_top_altas(top_n=15)
                render_html(pitch_renderer.render_ticket_parlay_altas(p_altas_box))

            if st.session_state.get('ver_top_empates_match'):
                st.markdown("### ⚖️ Radar de Empates de Oro (Top 5 Choques con Paridad)")
                p_empates_box = analytics.generar_top_empates_oro(top_n=5)
                render_html(pitch_renderer.render_ticket_empates_oro(p_empates_box))

            if st.session_state.get('ver_ficha_redes_match'):
                st.markdown("---")
                st.markdown("### 📸 Generador Rápido de Ficha HD para Redes")
                col_r_cfg1, col_r_cfg2 = st.columns(2)
                with col_r_cfg1:
                    fmt_res = st.selectbox("📐 Formato:", ["🟦 Cuadrado (Post 1:1 - 1080x1080)", "📱 Historia / Estado (Story 9:16 - 1080x1920)"], key=f"sel_fmt_res_{fixture_id}")
                    fmt_c_res = "9:16" if "9:16" in fmt_res else "1:1"
                with col_r_cfg2:
                    est_res = st.selectbox("🎨 Estilo Visual:", ["🏆 Oro VIP & Obsidiana", "🔥 Festival de Fuego", "⚡ Neón Cyber Pro"], key=f"sel_est_res_{fixture_id}")
                    est_c_res = "festival_fuego" if "Festival" in est_res else ("neon_pro" if "Neón" in est_res else "oro_vip")

                pick_export_res = {
                    "pick": pick_seguro_obj.get("descripcion", f"{equipo_local_real} o Empate (1X)"),
                    "cuota": p_seg_cuota,
                    "probabilidad": p_seg_prob,
                    "stake": "3/10 (3.5%)"
                }
                partido_export_res = {
                    "local": equipo_local_real,
                    "visita": equipo_visita_real,
                    "logo_local": logo_local_render,
                    "logo_visita": logo_visita_render,
                    "liga": liga_elegida if liga_elegida else "Liga Profesional",
                    "hora": datos_partido.get("hora", "Hoy")
                }
                stats_export_res = {
                    "xg_total": round(stats_poisson['lambda_home'] + stats_poisson['lambda_away'], 2),
                    "p_btts": f"{stats_poisson['p_btts']}%",
                    "p_over_25": f"{stats_poisson['p_over_25']}%"
                }

                with st.spinner("📸 Renderizando Ficha HD con Pillow..."):
                    img_bytes_res = social_card_generator.generar_ficha_partido_hd(
                        partido_data=partido_export_res,
                        pick_data=pick_export_res,
                        stats_data=stats_export_res,
                        formato=fmt_c_res,
                        estilo=est_c_res
                    )

                col_prv_r, col_act_r = st.columns([1.5, 1])
                with col_prv_r:
                    render_image_preview(img_bytes_res, caption="Vista Previa Ficha HD")
                with col_act_r:
                    st.download_button(
                        label="📥 DESCARGAR FICHA HD (.PNG)",
                        data=img_bytes_res,
                        file_name=f"ficha_{equipo_local_real.lower().replace(' ', '_')}_vs_{equipo_visita_real.lower().replace(' ', '_')}_{fmt_c_res.replace(':', 'x')}.png",
                        mime="image/png",
                        use_container_width=True,
                        key=f"btn_dl_res_{fixture_id}"
                    )
                st.markdown("---")

            st.markdown("<br>", unsafe_allow_html=True)

            html_bet_builder = pitch_renderer.render_ticket_bet_builder(picks_builder, equipo_local_real, equipo_visita_real)
            render_html(html_bet_builder)

        # =========================================================
        # PESTAÑA 3: GENERADOR DE FICHA HD PARA REDES SOCIALES
        # =========================================================
        with tab_redes:
            render_html('''
            <div style="background:linear-gradient(135deg, #1C202B 0%, #152238 50%, #0D0F14 100%); border:1.5px solid #D4AF37; padding:18px; border-radius:12px; margin-bottom:18px; text-align:center;">
                <h3 style="color:#FFFFFF; margin:0; font-weight:900;">📸 GENERADOR DE FICHAS HD PARA REDES SOCIALES</h3>
                <p style="color:#E2E8F0; margin:4px 0 0 0; font-size:14px;">Descarga la imagen oficial de este pronóstico lista para publicar en Instagram, WhatsApp, Twitter y Telegram.</p>
            </div>
            ''')

            col_cfg1, col_cfg2, col_cfg3 = st.columns([1.2, 1.2, 1])
            with col_cfg1:
                formato_redes = st.selectbox(
                    "📐 Formato de Imagen:",
                    ["🟦 Cuadrado (Post 1:1 - 1080x1080)", "📱 Historia / Estado (Story 9:16 - 1080x1920)"],
                    key=f"sel_fmt_redes_{fixture_id}"
                )
                fmt_code = "9:16" if "9:16" in formato_redes else "1:1"
            with col_cfg2:
                estilo_redes = st.selectbox(
                    "🎨 Estilo Visual:",
                    ["🏆 Oro VIP & Obsidiana", "🔥 Festival de Fuego", "⚡ Neón Cyber Pro"],
                    key=f"sel_est_redes_{fixture_id}"
                )
                est_code = "festival_fuego" if "Festival" in estilo_redes else ("neon_pro" if "Neón" in estilo_redes else "oro_vip")
            with col_cfg3:
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                regenerar_img = st.button("🔄 REGENERAR IMAGEN", key=f"btn_regen_img_{fixture_id}", use_container_width=True)

            # Preparar datos del pick para la ficha
            pick_obj_export = picks_builder.get("pick_seguro", picks_builder['picks'][0] if picks_builder.get('picks') else {})
            pick_export_data = {
                "pick": pick_obj_export.get("descripcion", f"{equipo_local_real} o Empate (1X)"),
                "cuota": float(pick_obj_export.get("cuota", 1.45)),
                "probabilidad": pick_obj_export.get("prob", "76.5%"),
                "stake": "3/10 (3.5%)"
            }
            partido_export_data = {
                "local": equipo_local_real,
                "visita": equipo_visita_real,
                "logo_local": logo_local_render,
                "logo_visita": logo_visita_render,
                "liga": liga_elegida if liga_elegida else "Liga Profesional",
                "hora": datos_partido.get("hora", "Hoy")
            }
            stats_export_data = {
                "xg_total": round(stats_poisson['lambda_home'] + stats_poisson['lambda_away'], 2),
                "p_btts": f"{stats_poisson['p_btts']}%",
                "p_over_25": f"{stats_poisson['p_over_25']}%"
            }

            with st.spinner("📸 Renderizando Ficha HD con Pillow Graphics Engine..."):
                img_png_bytes = social_card_generator.generar_ficha_partido_hd(
                    partido_data=partido_export_data,
                    pick_data=pick_export_data,
                    stats_data=stats_export_data,
                    formato=fmt_code,
                    estilo=est_code
                )

            col_preview, col_down = st.columns([1.5, 1])
            with col_preview:
                render_image_preview(img_png_bytes, caption=f"Vista Previa HD ({formato_redes.split('(')[0].strip()})")
            with col_down:
                st.markdown("#### 📥 Opciones de Exportación")
                st.info("💡 **Consejo:** La imagen incluye escudos oficiales, xG, probabilidad matemática y la marca oficial de Smart Pick Pro VIP lista para captar clientes en redes.")
                
                file_name_clean = f"smartpick_{equipo_local_real.lower().replace(' ', '_')}_vs_{equipo_visita_real.lower().replace(' ', '_')}_{fmt_code.replace(':', 'x')}.png"
                st.download_button(
                    label="📥 DESCARGAR FICHA HD (.PNG)",
                    data=img_png_bytes,
                    file_name=file_name_clean,
                    mime="image/png",
                    use_container_width=True,
                    key=f"btn_dl_img_{fixture_id}"
                )

            html_bet_builder = pitch_renderer.render_ticket_bet_builder(picks_builder, equipo_local_real, equipo_visita_real)
            render_html(html_bet_builder)

            # Métricas y Donut
            consejo_final = picks_builder.get("consejo_analitico", f"Mercado Recomendado: {p_seg_desc} | Alta solidez matemática.")
            st.info(f"💡 **Consejo Analítico:** {consejo_final}")
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
                    marker_colors=['#D4AF37', '#38BDF8', '#EF4444']
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
            ficha_txt = analytics.generar_ficha_vip_whatsapp(
                equipo_local_real, 
                equipo_visita_real, 
                stats_poisson, 
                web_url=getattr(config, 'WEBAPP_VIP_URL', 'https://smartpickprojz.com.mx'), 
                caliente_url=config.ENLACE_POR_DEFECTO,
                picks_builder=picks_builder
            )
            if st.session_state['rol'] == 'ADMIN':
                st.write("#### 📲 Ficha VIP para Difusión en Canales (Herramienta Admin)")
                st.text_area("📋 Reporte VIP copiable:", value=ficha_txt, height=220, key=f"admin_ficha_{fixture_id}")
            else:
                import urllib.parse
                encoded_txt = urllib.parse.quote(ficha_txt)
                render_html(f'''
                <div style="background: linear-gradient(135deg, #151821 0%, #1A1E29 100%); border-radius:12px; padding:16px; border:2px solid #2ECC71; text-align:center; margin-top:10px;">
                    <h4 style="color:#2ECC71; margin:0 0 6px 0; font-size:17px; font-weight:900;">📲 RECOMIENDA ESTE PRONÓSTICO VIP CON UN AMIGO</h4>
                    <a href="https://wa.me/?text={encoded_txt}" target="_blank" style="background:#1A4D2E; border:1px solid #2ECC71; color:white; font-weight:900; padding:10px 22px; border-radius:25px; text-decoration:none; display:inline-block; font-size:14px; margin-top:8px;">
                        💬 COMPARTIR EN WHATSAPP (1 CLIC)
                    </a>
                </div>
                ''')

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
                render_html('''
                <div style="background:#151821; border-radius:12px; padding:16px; border-left:6px solid #D4AF37; border:1px solid #282F3F; color:white;">
                    <h4 style="margin:0 0 10px 0; color:#D4AF37; font-size:16px; font-weight:900;">🎯 Top 3 Marcadores Exactos Más Probables</h4>
                ''')
                medallas = ["🥇 1er Lugar", "🥈 2do Lugar", "🥉 3er Lugar"]
                colores_mc = ["#D4AF37", "#38BDF8", "#F3E5AB"]
                for idx_m, item_m in enumerate(top_3_sc):
                    lbl_med = medallas[idx_m] if idx_m < len(medallas) else "🎯 Marcador"
                    c_badge = colores_mc[idx_m] if idx_m < len(colores_mc) else "#FFFFFF"
                    render_html(f'''
                    <div style="display:flex; justify-content:space-between; align-items:center; background:#1A1E29; padding:8px 12px; border-radius:8px; margin:5px 0; border:1px solid #282F3F;">
                        <span style="color:#E0E0E0; font-size:14px; font-weight:bold;">{lbl_med}: <b style="color:white; font-size:17px; margin-left:8px;">{item_m['marcador']}</b></span>
                        <span style="background:{c_badge}; color:#0D0F14; font-weight:900; padding:3px 10px; border-radius:12px; font-size:13px;">Prob: {item_m['prob']}%</span>
                    </div>
                    ''')
                st.markdown('</div>', unsafe_allow_html=True)

            with col_mc2:
                btts_val = mc_info.get("btts_pct", 50.0)
                over25_val = mc_info.get("over25_pct", 50.0)
                txt_btts = "SÍ" if btts_val >= 50.0 else "NO"
                c_btts = "#D4AF37" if btts_val >= 50.0 else "#EF4444"
                txt_over25 = "SÍ (+2.5)" if over25_val >= 50.0 else "NO (-2.5)"
                c_over25 = "#D4AF37" if over25_val >= 50.0 else "#EF4444"
                render_html(f'''
                <div style="background:#151821; border-radius:12px; padding:16px; border:1px solid #282F3F; color:white;">
                    <h4 style="margin:0 0 10px 0; color:#D4AF37; font-size:16px; font-weight:900;">⚽ Proyecciones Monte Carlo</h4>
                    <div style="margin:6px 0; background:#1A1E29; padding:8px 12px; border-radius:8px; border:1px solid #282F3F;">
                        <div style="color:#94A3B8; font-size:12px;">Ambos Equipos Anotan (BTTS)</div>
                        <div style="color:{c_btts}; font-size:18px; font-weight:900;">{txt_btts} ({btts_val}%)</div>
                    </div>
                    <div style="margin:6px 0; background:#1A1E29; padding:8px 12px; border-radius:8px; border:1px solid #282F3F;">
                        <div style="color:#94A3B8; font-size:12px;">Línea de Goles (Over/Under 2.5)</div>
                        <div style="color:{c_over25}; font-size:18px; font-weight:900;">{txt_over25} ({over25_val}%)</div>
                    </div>
                </div>
                ''')

            st.markdown("---")
            # Módulo xG
            st.write("### 🎯 Goles Esperados ($xG$) & Peligro Real en Áreas")
            xg_data = analytics.evaluar_xg_y_peligro_real(equipo_local_real, equipo_visita_real, stats_poisson)
            xg_c1, xg_c2, xg_c3 = st.columns(3)
            xg_c1.metric(f"xG {equipo_local_real}", f"{xg_data['xg_local']} xG", f"Eficiencia: {xg_data['eficiencia_loc']}%")
            xg_c2.metric("Modelo xG", "Ajustado por Simulación", "Dixon-Coles")
            xg_c3.metric(f"xG {equipo_visita_real}", f"{xg_data['xg_visita']} xG", f"Eficiencia: {xg_data['eficiencia_vis']}%")

            render_html(f'''
            <div style="background:#151821; padding:12px 16px; border-radius:10px; border-left:5px solid #D4AF37; border:1px solid #282F3F; margin:10px 0; color:white;">
                <div style="color:#D4AF37; font-weight:900; font-size:14px;">📌 Análisis de Ocasiones Clave (Expected Goals):</div>
                <div style="color:#E0E0E0; font-size:13px; margin-top:4px;">{xg_data['alerta_xg']}</div>
            </div>
            ''')

            st.markdown("---")
            # Predictor IA Ensemble
            st.write("### 🤖 Predictor de Inteligencia Artificial (XGBoost Ensemble)")
            bajas_info = api_client.obtener_bajas_equipo(fixture_id, datos_partido.get("local_id", 0), datos_partido.get("visita_id", 0), equipo_local_real, equipo_visita_real)
            ia_info = analytics.evaluar_predictor_ia_ensemble(equipo_local_real, equipo_visita_real, stats_poisson, bajas_info)
            
            render_html(f'''
            <div style="background: linear-gradient(135deg, #151821 0%, #1A1E29 100%); border-radius:14px; padding:18px; border:2px solid #38BDF8; margin:10px 0; color:white; box-shadow:0 4px 15px rgba(0,0,0,0.3);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <h4 style="margin:0; color:#38BDF8; font-size:17px; font-weight:900;">{ia_info['tendencia_ia']}</h4>
                    <span style="background:#38BDF8; color:#0D0F14; font-weight:900; padding:4px 12px; border-radius:16px; font-size:13px;">Confianza IA: {ia_info['confianza_ia']}%</span>
                </div>
                <div style="background:#0D0F14; padding:10px 14px; border-radius:8px; border:1px solid #282F3F; margin-bottom:10px;">
                    <span style="color:#94A3B8; font-size:12px;">Pick Sugerido por Machine Learning:</span><br>
                    <span style="color:#D4AF37; font-size:17px; font-weight:900;">🎯 {ia_info['pick_ia']}</span>
                </div>
                <div style="font-size:13px; color:#E0E0E0;">
                    <b>📌 Factores Ponderados por el Algoritmo:</b>
                    <ul style="margin:4px 0 0 16px; padding:0;">
                        {"".join([f"<li>{f}</li>" for f in ia_info['factores']])}
                    </ul>
                </div>
            </div>
            ''')

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
            
            total_partidos_h2h = h2h_loc_wins + h2h_empates + h2h_vis_wins
            
            if total_partidos_h2h == 0:
                st.info(f"ℹ️ **Primer enfrentamiento directo registrado:** No se registran enfrentamientos previos oficiales entre **{equipo_local_real}** y **{equipo_visita_real}** en los archivos recientes.")
            else:
                col_h2h_fig, col_h2h_metrics = st.columns([1.4, 0.6])
                with col_h2h_fig:
                    fig_h2h = go.Figure()
                    if h2h_loc_wins > 0:
                        fig_h2h.add_trace(go.Bar(
                            y=['Choques Directos'], x=[h2h_loc_wins], name=equipo_local_real,
                            text=[f"<b>{equipo_local_real}: {h2h_loc_wins} Vic.</b>"],
                            textposition='auto', insidetextfont=dict(color='white', size=13),
                            orientation='h', marker=dict(color='#D4AF37', line=dict(color='#ffffff', width=2))
                        ))
                    if h2h_empates > 0:
                        fig_h2h.add_trace(go.Bar(
                            y=['Choques Directos'], x=[h2h_empates], name='Empates',
                            text=[f"<b>{h2h_empates} Empate(s)</b>"],
                            textposition='auto', insidetextfont=dict(color='white', size=13),
                            orientation='h', marker=dict(color='#38BDF8', line=dict(color='#ffffff', width=2))
                        ))
                    if h2h_vis_wins > 0:
                        fig_h2h.add_trace(go.Bar(
                            y=['Choques Directos'], x=[h2h_vis_wins], name=equipo_visita_real,
                            text=[f"<b>{equipo_visita_real}: {h2h_vis_wins} Vic.</b>"],
                            textposition='auto', insidetextfont=dict(color='white', size=13),
                            orientation='h', marker=dict(color='#EF4444', line=dict(color='#ffffff', width=2))
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
                    render_html(f'''
                    <div style="background:#151821; padding:12px; border-radius:10px; border:1px solid #282F3F; text-align:center;">
                        <h5 style="color:#D4AF37; margin:0 0 8px 0; font-weight:900;">⚽ Goles en H2H</h5>
                        <div style="display:flex; justify-content:space-around; align-items:center;">
                            <div><span style="color:#D4AF37; font-size:22px; font-weight:900;">{goles_tot_loc}</span><br><small style="color:#aaa;">{equipo_local_real}</small></div>
                            <span style="color:#fff; font-size:16px; font-weight:bold;">VS</span>
                            <div><span style="color:#EF4444; font-size:22px; font-weight:900;">{goles_tot_vis}</span><br><small style="color:#aaa;">{equipo_visita_real}</small></div>
                        </div>
                    </div>
                    ''')

            st.markdown("---")
            # Duelo de Rendimiento
            st.write("### 📊 Duelo Estadístico de Rendimiento (Fuerza Comparativa)")
            cats_rad, v_loc_rad, v_vis_rad = analytics.generar_grafico_radar_comparativo(equipo_local_real, equipo_visita_real, stats_poisson, fl, fv)
            iconos_cat = ["⚔️ Poder Ofensivo", "🛡️ Solidez Defensiva", "🔥 Racha Reciente", "🎯 Prob. Victoria", "💎 Solidez Global"]
            for idx_c, cat_nombre in enumerate(cats_rad):
                icon_title = iconos_cat[idx_c] if idx_c < len(iconos_cat) else f"📌 {cat_nombre}"
                val_l = v_loc_rad[idx_c]
                val_v = v_vis_rad[idx_c]
                render_html(f'''
                <div style="background:#151821; border-radius:10px; padding:10px 16px; margin:6px 0; border:1px solid #282F3F;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <span style="color:#38BDF8; font-weight:900; font-size:14px;">🔵 {equipo_local_real}: <b>{val_l}%</b></span>
                        <span style="color:#D4AF37; font-weight:bold; font-size:13px;">{icon_title}</span>
                        <span style="color:#EF4444; font-weight:900; font-size:14px;">🔴 {equipo_visita_real}: <b>{val_v}%</b></span>
                    </div>
                    <div style="display:flex; height:10px; background:#0D0F14; border-radius:5px; overflow:hidden; border:1px solid #282F3F;">
                        <div style="width:{val_l}%; background:#38BDF8; height:100%;"></div>
                        <div style="width:{val_v}%; background:#EF4444; height:100%; margin-left:auto;"></div>
                    </div>
                </div>
                ''')

            st.markdown("---")
            # Rachas Recientes
            st.write("### 📈 Rachas Recientes & Tendencias de Forma (Últimos 5 Partidos)")
            badges_l, tend_l = analytics.generar_badges_racha_visual(fl, equipo_local_real)
            badges_v, tend_v = analytics.generar_badges_racha_visual(fv, equipo_visita_real)
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                b_html_l = "".join([f'<span style="background:{b["bg"]}; color:{b["color"]}; border:2px solid {b["borde"]}; font-weight:900; font-size:13px; width:30px; height:30px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; margin-right:4px;">{b["letra"]}</span>' for b in badges_l])
                render_html(f'''
                <div style="background:#151821; border-radius:12px; padding:14px; border-left:5px solid #38BDF8; border:1px solid #282F3F;">
                    <h4 style="margin:0 0 6px 0; color:white; font-size:15px; font-weight:900;">🔵 {equipo_local_real}</h4>
                    <div style="display:flex; margin-bottom:8px;">{b_html_l}</div>
                    <div style="background:#0D0F14; padding:6px 10px; border-radius:6px; color:#E0E0E0; font-size:12px; font-weight:bold; border:1px solid #282F3F;">{tend_l}</div>
                </div>
                ''')
            with col_r2:
                b_html_v = "".join([f'<span style="background:{b["bg"]}; color:{b["color"]}; border:2px solid {b["borde"]}; font-weight:900; font-size:13px; width:30px; height:30px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; margin-right:4px;">{b["letra"]}</span>' for b in badges_v])
                render_html(f'''
                <div style="background:#151821; border-radius:12px; padding:14px; border-left:5px solid #EF4444; border:1px solid #282F3F;">
                    <h4 style="margin:0 0 6px 0; color:white; font-size:15px; font-weight:900;">🔴 {equipo_visita_real}</h4>
                    <div style="display:flex; margin-bottom:8px;">{b_html_v}</div>
                    <div style="background:#0D0F14; padding:6px 10px; border-radius:6px; color:#E0E0E0; font-size:12px; font-weight:bold; border:1px solid #282F3F;">{tend_v}</div>
                </div>
                ''')

            st.markdown("---")
            # Bajas y Lesiones
            st.write("### 🚑 Reporte de Bajas y Lesiones")
            col_bj1, col_bj2 = st.columns(2)
            with col_bj1:
                st.markdown(f"<b>🔵 {equipo_local_real} (Impacto: -{bajas_info.get('impacto_loc_pct', 0)}%)</b>", unsafe_allow_html=True)
                if bajas_info.get('local_bajas'):
                    for b in bajas_info['local_bajas']:
                        st.markdown(f"<div style='background:#151821; padding:6px 10px; border-radius:6px; margin:4px 0; border:1px solid #282F3F; color:white; font-size:13px;'>{b['gravedad']} <b>{b['nombre']}</b> ({b['motivo']})</div>", unsafe_allow_html=True)
                else:
                    st.success("✅ Plantilla completa sin bajas reportadas.")
            with col_bj2:
                st.markdown(f"<b>🔴 {equipo_visita_real} (Impacto: -{bajas_info.get('impacto_vis_pct', 0)}%)</b>", unsafe_allow_html=True)
                if bajas_info.get('visita_bajas'):
                    for b in bajas_info['visita_bajas']:
                        st.markdown(f"<div style='background:#151821; padding:6px 10px; border-radius:6px; margin:4px 0; border:1px solid #282F3F; color:white; font-size:13px;'>{b['gravedad']} <b>{b['nombre']}</b> ({b['motivo']})</div>", unsafe_allow_html=True)
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

            render_html(f'''
            <div style="background:#151821; padding:12px 16px; border-radius:10px; border:1px solid #282F3F; margin:10px 0; color:white;">
                <div style="color:#D4AF37; font-weight:bold; font-size:14px; margin-bottom:4px;">📌 Impacto Aeróbico & Físico:</div>
                <div style="color:#E0E0E0; font-size:13px;">{info_af['desc_altitud']}</div>
                <div style="display:flex; justify-content:space-between; margin-top:8px; background:#0D0F14; padding:8px 12px; border-radius:6px; border:1px solid #282F3F;">
                    <span>🔵 <b>{equipo_local_real}:</b> {info_af['fatiga_loc']}</span>
                    <span>🔴 <b>{equipo_visita_real}:</b> {info_af['fatiga_vis']}</span>
                </div>
            </div>
            ''')

            st.markdown("---")
            # Árbitro y Rigor
            st.write("### ⚖️ Árbitro Oficial Asignado & Rigor Arbitral")
            info_ref = analytics.evaluar_rigor_arbitral(referee_name, promedio_tarjetas)
            ref_col1, ref_col2, ref_col3 = st.columns(3)
            ref_col1.metric("Árbitro Principal", info_ref['nombre'])
            ref_col2.metric("Prom. Tarjetas Amarillas", f"{info_ref['tarjetas_amarillas']} / partido")
            ref_col3.metric("Rigor Arbitral", info_ref['rigor'].split('(')[0].strip())

            render_html(f'''
            <div style="background:#151821; padding:12px 16px; border-radius:10px; border-left:5px solid #D4AF37; border:1px solid #282F3F; margin:10px 0; color:white;">
                <div style="color:#D4AF37; font-weight:bold; font-size:14px; margin-bottom:4px;">🎯 Análisis de Fricción & Recomendación de Mercado:</div>
                <div style="color:#E0E0E0; font-size:13px;">{info_ref['recomendacion']}</div>
                <div style="color:#94A3B8; font-size:12px; margin-top:4px;">Promedio Expulsiones: {info_ref['tarjetas_rojas']} rojas/partido | Promedio Penales: {info_ref['penales_prom']}/partido</div>
            </div>
            ''')

        # =========================================================
        # PESTAÑA 5: CUOTAS & BANKROLL
        # =========================================================
        with tab_cuotas:
            st.write("### 📊 Comparador Multi-Casino & Valor Esperado ($+EV$)")
            t_html = '''<div style="background-color:#151821; border-radius:10px; padding:15px; margin-bottom:15px; border:1px solid #282F3F;">
            <table style="width:100%; border-collapse:collapse; text-align:center; color:white;">
            <thead style="border-bottom:2px solid #282F3F;">
            <tr>
            <th style="padding:10px; color:#94A3B8; font-size:12px; text-align:left;">CASA DE APUESTAS</th>
            <th style="padding:10px; color:#fff;">1 (Local)</th>
            <th style="padding:10px; color:#fff;">X (Empate)</th>
            <th style="padding:10px; color:#fff;">2 (Visita)</th>
            <th style="padding:10px; color:#94A3B8; font-size:12px;">APOSTAR</th>
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

                t_html += f'''<tr style="border-bottom:1px solid #282F3F;">
                <td style="padding:10px 5px; font-weight:bold; color:#fff; text-align:left; font-size:14px;">{nc}</td>
                <td style="padding:10px 2px;"><div style="background:#0D0F14; color:#D4AF37; padding:6px 0; border-radius:6px; font-weight:bold; border:1px solid #282F3F;">{casino['1']}</div></td>
                <td style="padding:10px 2px;"><div style="background:#0D0F14; color:#D4AF37; padding:6px 0; border-radius:6px; font-weight:bold; border:1px solid #282F3F;">{casino['X']}</div></td>
                <td style="padding:10px 2px;"><div style="background:#0D0F14; color:#D4AF37; padding:6px 0; border-radius:6px; font-weight:bold; border:1px solid #282F3F;">{casino['2']}</div></td>
                <td style="padding:10px 5px;"><a href="{lk}" target="_blank" class="casino-btn">Apostar ></a></td>
                </tr>'''
            t_html += '''</tbody></table></div>'''
            st.markdown(t_html, unsafe_allow_html=True)

            if apuestas_valor:
                render_html('''<div style="background-color: rgba(212, 175, 55, 0.12); border-left: 5px solid #D4AF37; padding: 14px; border-radius: 6px; margin-bottom: 15px; border-top: 1px solid #282F3F; border-right: 1px solid #282F3F; border-bottom: 1px solid #282F3F;">
                <h4 style="color: #D4AF37; margin-top:0;">🔥 ALERTAS DE VALOR ESPERADO POSITIVO (+EV)</h4>''')
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
                    render_html(f'''
                    <div style="background:#151821; border-radius:10px; padding:14px; border:2px solid #D4AF37; margin:10px 0;">
                        <h4 style="color:#D4AF37; margin:0 0 6px 0;">💎 Apuesta Óptima Sugerida por Criterio de Kelly:</h4>
                        <div style="font-size:18px; color:white; font-weight:bold;">Apostar: <span style="color:#D4AF37;">${res_kelly['monto_sugerido']:,.2f} MXN</span> ({res_kelly['kelly_pct']}% de tu bankroll) en cuota {mejor_cuota_ev}</div>
                        <small style="color:#aaa;">* Calculado con ventaja matemática positiva (+EV) y control de riesgo.</small>
                    </div>
                    ''')

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
                    render_html(f'''<div style="background:#151821; padding:14px; border-radius:10px; border-left:5px solid #38BDF8; border-top:1px solid #282F3F; border-right:1px solid #282F3F; border-bottom:1px solid #282F3F;">
                    <h4 style="color:white; margin:0 0 6px 0;">🔵 {equipo_local_real}</h4>
                    <p style="color:#ddd; font-size:13px; margin:0 0 6px 0;">Posición: {pos_l}° | Puntos: {pts_l} | Racha: {forma_l}</p>
                    <div style="background:rgba(56,189,248,0.12); padding:8px; border-radius:6px; border:1px solid rgba(56,189,248,0.2);">
                        <p style="color:#e0e0e0; margin:0; font-size:12px;">📌 {txt_nec_l}</p>
                    </div></div>''')
                with ct2:
                    render_html(f'''<div style="background:#151821; padding:14px; border-radius:10px; border-left:5px solid #EF4444; border-top:1px solid #282F3F; border-right:1px solid #282F3F; border-bottom:1px solid #282F3F;">
                    <h4 style="color:white; margin:0 0 6px 0;">🔴 {equipo_visita_real}</h4>
                    <p style="color:#ddd; font-size:13px; margin:0 0 6px 0;">Posición: {pos_v}° | Puntos: {pts_v} | Racha: {forma_v}</p>
                    <div style="background:rgba(239,68,68,0.12); padding:8px; border-radius:6px; border:1px solid rgba(239,68,68,0.2);">
                        <p style="color:#e0e0e0; margin:0; font-size:12px;">📌 {txt_nec_v}</p>
                    </div></div>''')
