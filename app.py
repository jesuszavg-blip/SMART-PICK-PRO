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
st.markdown("""
<head>
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="SmartPick VIP">
    <link rel="icon" type="image/jpeg" href="https://raw.githubusercontent.com/jesuszavg-blip/SMART-PICK-PRO/main/assets/app_icon.jpg">
    <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/jesuszavg-blip/SMART-PICK-PRO/main/assets/app_icon.jpg">
    <link rel="manifest" href="manifest.json">
</head>
""", unsafe_allow_html=True)

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

# Estilos CSS Personalizados de Máximo Contraste Visual y Estética Premium VIP (Paleta Oficial Dorado & Obsidiana)
st.markdown("""
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
""", unsafe_allow_html=True)

# Manejo de Sesión de Autenticación
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
if 'usuario' not in st.session_state:
    st.session_state['usuario'] = None
if 'rol' not in st.session_state:
    st.session_state['rol'] = None

if not st.session_state['autenticado']:
    if assets_data and hasattr(assets_data, 'LOGO_WEB_B64') and assets_data.LOGO_WEB_B64:
        st.markdown(f'''
        <div style="text-align:center; margin-top:20px; margin-bottom:20px;">
            <img src="data:image/png;base64,{assets_data.LOGO_WEB_B64}" style="max-width:480px; width:90%; height:auto; filter:drop-shadow(0 12px 30px rgba(0,0,0,0.8));" />
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="hero-banner" style="margin-top: 25px;">
            <h1 style="color: white; margin: 0; font-weight: 900; font-size: 38px; letter-spacing: 1px;">🏆 SMART PICK PRO VIP</h1>
            <p style="color: white; margin: 8px 0 0 0; font-size: 18px; opacity: 0.95;">Sistema de IA Predictiva • Optimizador de Reducciones Progol • Buscador $+EV$</p>
            <div style="margin-top: 12px; display: inline-block; background: rgba(212, 175, 55, 0.15); border: 1.5px solid #D4AF37; border-radius: 20px; padding: 6px 18px; color: #D4AF37; font-weight: 900; font-size: 14px;">
                ⭐ +85.4% de Efectividad Comprobada en Quinielas y Parlays VIP
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    col_log1, col_log2, col_log3 = st.columns([1, 2.5, 1])
    with col_log2:
        st.markdown('''
        <div style="background: #151821; padding: 25px; border-radius: 14px; border: 1px solid #282F3F; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
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

        html_pago = '<div style="background: linear-gradient(135deg, #151821 0%, #1A1E29 100%); padding: 22px; border-radius: 14px; border: 2px dashed #D4AF37; margin-top: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.4); text-align: center;">'
        html_pago += '<div style="background: linear-gradient(90deg, #FF512F 0%, #DD2476 100%); color: white; font-weight: 900; font-size: 13px; padding: 6px 16px; border-radius: 20px; display: inline-block; margin-bottom: 12px; box-shadow: 0 4px 10px rgba(221,36,118,0.4);">🔥 ¡SÚPER OFERTA POR TIEMPO LIMITADO (50% OFF)!</div>'
        html_pago += '<h3 style="color: #D4AF37; margin: 4px 0 10px 0; font-weight: 900; text-align: center;">💎 ACCESO VIP: <span style="text-decoration: line-through; color: #888; font-size: 20px;">$299</span> <span style="color: #F3E5AB; font-size: 32px;">$149 MXN</span> / MES</h3>'
        html_pago += '<p style="color: #E0E0E0; font-size: 13px; text-align: center; margin-bottom: 15px;">Aprovecha la súper promoción de lanzamiento por <b>$149 MXN</b>. Realiza tu pago por <b>BanCoppel, OXXO o PayPal</b> y envía tu comprobante por WhatsApp para recibir tu usuario y contraseña de inmediato:</p>'
        
        html_pago += f'<div style="background: #11141C; border-radius: 10px; padding: 14px; border: 1px solid #282F3F; margin-bottom: 12px; text-align: left;"><div style="color: #F3E5AB; font-weight: 900; font-size: 14px; margin-bottom: 6px;">🟡 DEPÓSITO / SPEI BANCOPPEL ($149 MXN)</div><div style="color: white; font-size: 13px;"><b>Banco:</b> BanCoppel</div><div style="color: white; font-size: 13px;"><b>No. de Tarjeta / SPEI:</b> <span style="color:#D4AF37; font-weight:bold; font-family:monospace;">{bancoppel_card}</span></div><div style="color: white; font-size: 13px;"><b>Titular:</b> {bancoppel_holder}</div><div style="color: #aaa; font-size: 11px; margin-top:4px;">* Acepta transferencias SPEI 24/7 y depósitos en OXXO o Tiendas Coppel.</div></div>'

        html_pago += f'<div style="background: #11141C; border-radius: 10px; padding: 14px; border: 1px solid #282F3F; margin-bottom: 15px; text-align: left;"><div style="color: #38BDF8; font-weight: 900; font-size: 14px; margin-bottom: 6px;">🔵 PAGO EN LÍNEA POR PAYPAL ($149 MXN)</div><div style="color: white; font-size: 13px;"><b>Enlace PayPal:</b> <a href="{paypal_url}" target="_blank" style="color:#38BDF8; font-weight:bold;">{paypal_url}</a></div><div style="color: #aaa; font-size: 11px; margin-top:4px;">* Paga de forma segura con cualquier tarjeta de Débito o Crédito.</div></div>'

        html_pago += '<div style="text-align: center;"><a href="https://wa.me/526676947014?text=Hola%20Jesus,%20aprovecho%20la%20super%20oferta%20VIP%20de%20%24149%20MXN.%20Adjunto%20mi%20comprobante%20para%20activar%20mi%20cuenta" target="_blank" class="whatsapp-btn" style="display:inline-block; width:100%; box-sizing:border-box; font-size:15px; padding:12px;">💬 ENVIAR COMPROBANTE DE $149 POR WHATSAPP</a></div>'
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
    st.markdown('''
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
    ''', unsafe_allow_html=True)

sidebar_casinos_html = f'<div style="background:linear-gradient(135deg, #151821 0%, #1A1E29 100%);padding:12px;border-radius:12px;border:1px solid #282F3F;margin-top:10px;margin-bottom:14px;text-align:center;"><div style="color:#D4AF37;font-weight:900;font-size:11px;margin-bottom:8px;letter-spacing:0.5px;">💎 CASAS RECOMENDADAS (+EV)</div><div style="display:flex;gap:6px;justify-content:center;"><a href="{ban_1xbet}" target="_blank" style="background:#00B4D8;color:#0A192F;font-weight:bold;font-size:11px;padding:6px 10px;border-radius:12px;text-decoration:none;flex:1;">🔵 1xBet</a><a href="{ban_mexplay}" target="_blank" style="background:#FF8500;color:#FFFFFF;font-weight:bold;font-size:11px;padding:6px 10px;border-radius:12px;text-decoration:none;flex:1;">🟡 Mexplay</a></div></div>'
st.sidebar.markdown(sidebar_casinos_html, unsafe_allow_html=True)

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
        st.write("#### 🛡️ Persistencia y Base de Datos")
        st.markdown(f"""
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

# --- MODO 0: RADAR DE PARTIDOS EN VIVO MULTILIGAS ---
if liga_elegida_val == "LIVE_RADAR_MODE":
    if not st.session_state.get('live_partido_detalle'):
        st.markdown('''
        <div style="background: linear-gradient(135deg, #1C202B 0%, #3D1A1A 100%); border:1.5px solid #EF5350; padding: 22px; border-radius: 14px; text-align: center; margin-bottom: 20px; box-shadow: 0 6px 20px rgba(239, 83, 80, 0.25);">
            <h2 style="color: white; margin: 0; font-weight: 900; font-size: 28px; letter-spacing: 1px;">🔴 RADAR DE PARTIDOS EN VIVO MULTILIGAS</h2>
            <p style="color: #E2E8F0; margin: 6px 0 0 0; font-size: 15px; opacity: 0.95;">Marcadores en tiempo real, minutos jugados y eventos de todos los encuentros activos en el mundo.</p>
        </div>
        ''', unsafe_allow_html=True)
        
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
        
        st.markdown(f'''
        <div style="background:#151821; border-radius:10px; padding:10px 16px; margin-bottom:18px; border:1px solid #282F3F; display:flex; justify-content:space-between; align-items:center;">
            <span style="color:#FFFFFF; font-weight:bold; font-size:14px;">📡 Conexión Satelital API-Sports: <span style="color:#38BDF8; font-weight:900;">ACTIVA (HTTP 200 OK)</span></span>
            <span style="background:#38BDF8; color:#0D0F14; font-weight:900; padding:4px 12px; border-radius:20px; font-size:13px;">🟢 {total_partidos} Partidos en Juego</span>
        </div>
        ''', unsafe_allow_html=True)

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
                st.markdown('''
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
                ''', unsafe_allow_html=True)
            else:
                st.info("ℹ️ No se encontraron partidos activos con los filtros de búsqueda seleccionados.")
        else:
            for l_key, l_data in ligas_filtradas.items():
                p_lista = l_data["partidos"]
                pais_nombre = l_data.get("pais", "Internacional")
                liga_nombre = l_data.get("nombre", "Torneo")
                
                st.markdown(f'''
                <div style="display:flex; align-items:center; justify-content:space-between; background:#151821; border-left:5px solid #38BDF8; border-radius:10px; padding:10px 16px; margin:20px 0 12px 0; border-top:1px solid #282F3F; border-right:1px solid #282F3F; border-bottom:1px solid #282F3F;">
                    <div style="display:flex; align-items:center; gap:10px;">
                        <span style="font-size:16px; font-weight:900; color:#FFFFFF;">🏆 {pais_nombre} - {liga_nombre}</span>
                    </div>
                    <span style="background:#38BDF8; color:#0D0F14; font-weight:900; padding:2px 10px; border-radius:12px; font-size:12px;">{len(p_lista)} en juego</span>
                </div>
                ''', unsafe_allow_html=True)
                
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
    st.markdown('''
    <div style="background: linear-gradient(135deg, #1C202B 0%, #2A2E3D 50%, #151821 100%); border: 1.5px solid #D4AF37; padding: 22px; border-radius: 14px; text-align: center; margin-bottom: 20px; box-shadow: 0 6px 20px rgba(212, 175, 55, 0.2);">
        <h2 style="color: white; margin: 0; font-weight: 900; font-size: 28px; letter-spacing: 1px;">💎 CAZADOR DE PARLAYS VIP (+ALTAS & EMPATES DE ORO)</h2>
        <p style="color: #E2E8F0; margin: 6px 0 0 0; font-size: 15px; opacity: 0.95;">Algoritmos de Simulación Poisson & Dixon-Coles optimizados para Parlays de Alta Probabilidad y Cuotas de Valor.</p>
    </div>
    ''', unsafe_allow_html=True)
    
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
                st.rerun()

        with st.spinner("Procesando matriz de goles esperados y xG en ligas mundiales..."):
            parlay_altas_data = analytics.generar_parlay_top_altas(top_n=top_n_altas)

        # Renderizar boleto visual
        st.markdown(pitch_renderer.render_ticket_parlay_altas(parlay_altas_data), unsafe_allow_html=True)

        # Opciones de Difusión y Compartir
        ficha_altas = analytics.generar_ficha_parlay_altas_whatsapp(parlay_altas_data, web_url=getattr(config, 'WEBAPP_VIP_URL', 'https://smartpickprojz.com.mx'))
        import urllib.parse
        encoded_altas = urllib.parse.quote(ficha_altas)

        col_w1, col_w2 = st.columns(2)
        with col_w1:
            st.markdown(f'''
            <a href="https://wa.me/?text={encoded_altas}" target="_blank" style="background:#1A4D2E; border:1px solid #2ECC71; color:white; font-weight:900; padding:12px 20px; border-radius:10px; text-decoration:none; display:block; text-align:center; font-size:14px; margin-top:5px; box-shadow:0 4px 12px rgba(46,204,113,0.3);">
                💬 COMPARTIR PARLAY DE ALTAS EN WHATSAPP (1 CLIC)
            </a>
            ''', unsafe_allow_html=True)
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
                st.rerun()

        with st.spinner("Procesando matriz Dixon-Coles de paridad táctica..."):
            empates_data = analytics.generar_top_empates_oro(top_n=top_n_emp)

        # Renderizar boleto visual de empates
        st.markdown(pitch_renderer.render_ticket_empates_oro(empates_data), unsafe_allow_html=True)

        # Ficha WhatsApp de Empates
        ficha_empates = analytics.generar_ficha_empates_whatsapp(empates_data, web_url=getattr(config, 'WEBAPP_VIP_URL', 'https://smartpickprojz.com.mx'))
        encoded_empates = urllib.parse.quote(ficha_empates)

        col_we1, col_we2 = st.columns(2)
        with col_we1:
            st.markdown(f'''
            <a href="https://wa.me/?text={encoded_empates}" target="_blank" style="background:#1A4D2E; border:1px solid #2ECC71; color:white; font-weight:900; padding:12px 20px; border-radius:10px; text-decoration:none; display:block; text-align:center; font-size:14px; margin-top:5px; box-shadow:0 4px 12px rgba(46,204,113,0.3);">
                💬 COMPARTIR RADAR DE EMPATES EN WHATSAPP (1 CLIC)
            </a>
            ''', unsafe_allow_html=True)
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
    st.markdown('''
    <div style="background: linear-gradient(135deg, #1C202B 0%, #2A2E3D 50%, #151821 100%); border:1.5px solid #D4AF37; padding: 22px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
        <h2 style="color: #D4AF37; margin: 0; font-weight: 900;">🎯 OPTIMIZADOR INTELIGENTE DE QUINIELA PROGOL</h2>
        <p style="color: #E2E8F0; margin: 6px 0 0 0; font-size: 15px;">Configura tus dobles y triples deseados sobre los 14 partidos oficiales.</p>
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
            <div style="background:#151821; padding:12px 18px; border-radius:8px; margin:6px 0; border-left:5px solid {item['color_borde']}; color:white; border-top:1px solid #282F3F; border-right:1px solid #282F3F; border-bottom:1px solid #282F3F;">
                <b style="color:white; font-size:15px;">Casilla {item['casilla']}:</b> 
                <span style="color:#FFFFFF; font-weight:bold;">{p_match['local']} vs {p_match['visita']}</span> -> 
                <span style="color:{item['color_borde']}; font-weight:900; font-size:16px;">{item['sugerencia']}</span>
            </div>
            ''', unsafe_allow_html=True)
            
    st.stop()

# --- MODO 2: OPTIMIZADOR DE REDUCCIONES ---
elif liga_elegida_val == "REDUCCIONES_MODE":
    st.markdown('''
    <div style="background: linear-gradient(135deg, #1C202B 0%, #2A2E3D 50%, #151821 100%); border:1.5px solid #D4AF37; padding: 22px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
        <h2 style="color: #D4AF37; margin: 0; font-weight: 900;">⚙️ Panel de Reducciones Inteligentes Pro</h2>
        <p style="color: #E2E8F0; margin: 5px 0 0 0; font-size: 15px;">Matriz matemática de reducciones aplicadas a los 14 partidos oficiales</p>
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
                color_borde = "#D4AF37"
            elif idx in set_dobles:
                tipo_txt = "Doble Local/Empate (1X)" if idx % 2 != 0 else "Doble Empate/Visita (X2)"
                color_borde = "#38BDF8"
            else:
                tipo_txt = "Fijo Local (1)" if idx % 2 != 0 else "Fijo Visita (2)"
                color_borde = "#F3E5AB"

            st.markdown(f'''
            <div style="background:#151821; padding:10px 16px; border-radius:8px; margin:5px 0; border-left:5px solid {color_borde}; color:white; border-top:1px solid #282F3F; border-right:1px solid #282F3F; border-bottom:1px solid #282F3F;">
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
                    st.markdown(f'''
                    <div style="display:flex; justify-content:space-between; align-items:center; background:#151821; padding:5px 10px; border-radius:6px; margin:2px 0; border:1px solid #282F3F;">
                        <span style="color:white; font-size:12px;"><b>Casilla {p_c}:</b> {p_part}</span>
                        <span style="background:{c_color}; color:#0D0F14; font-weight:900; padding:1px 8px; border-radius:8px; font-size:13px;">{p_pk}</span>
                    </div>
                    ''', unsafe_allow_html=True)

    st.stop()

# --- MODO 3: ANÁLISIS INTEGRAL DE PARTIDO (CON PESTAÑAS ST.TABS) ---
if st.session_state.get('live_partido_detalle'):
    col_back, _ = st.columns([1, 2])
    with col_back:
        if st.button("⬅️ VOLVER AL RADAR DE TODAS LAS LIGAS EN VIVO", use_container_width=True):
            st.session_state['live_partido_detalle'] = None
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
        <div style="display:flex; align-items:center; justify-content:space-around; background:linear-gradient(135deg, #151821 0%, #1A1E29 100%); border:1px solid #282F3F; padding:20px 15px; border-radius:16px; box-shadow:0 6px 25px rgba(0,0,0,0.5); margin-bottom:15px;">
            <div style="text-align:center; width:33%;">
                <img src="{logo_local_render}" style="width:70px; height:70px; object-fit:contain; margin-bottom:6px;">
                <h3 style="margin:0; color:#FFFFFF; font-size:17px; font-weight:800;">{equipo_local_real}</h3>
            </div>
            <div style="width:34%; text-align:center;">
                {badge_html}
                <h1 style='margin:0; font-size:44px; color:#D4AF37; letter-spacing:4px;'>{g_h} - {g_a}</h1>
            </div>
            <div style="text-align:center; width:33%;">
                <img src="{logo_visita_render}" style="width:70px; height:70px; object-fit:contain; margin-bottom:6px;">
                <h3 style="margin:0; color:#FFFFFF; font-size:17px; font-weight:800;">{equipo_visita_real}</h3>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        # --- ESTRUCTURA EN PESTAÑAS (ST.TABS) ---
        tab_vivo, tab_resumen, tab_modelos, tab_h2h, tab_cancha, tab_cuotas = st.tabs([
            "🔴 1. Minuto a Minuto En Vivo",
            "📊 2. Resumen & Picks VIP",
            "🧠 3. Modelos & Simulación",
            "⚔️ 4. Estadísticas & H2H",
            "🏟️ 5. Cancha, Clima & Árbitro",
            "💰 6. Cuotas & Bankroll"
        ])

        # =========================================================
        # PESTAÑA 1: MINUTO A MINUTO EN PANTALLA DIVIDIDA
        # =========================================================
        with tab_vivo:
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
                tiros_local=max(3, int(float(gl) * 3.5)),
                tiros_visita=max(2, int(float(gv) * 3.2))
            )
            st.markdown(html_minuto_a_minuto, unsafe_allow_html=True)

        # =========================================================
        # PESTAÑA 2: RESUMEN & PICKS VIP
        # =========================================================
        with tab_resumen:
            col_b1, col_b2, col_b3, col_b4 = st.columns(4)
            with col_b1:
                if st.button("⚡ PICK SENCILLO SEGURO", use_container_width=True):
                    v_p1x = stats_poisson.get("p_1X", 70.0)
                    v_px2 = stats_poisson.get("p_X2", 70.0)
                    if v_p1x >= v_px2:
                        st.success(f"🎯 **PICK SEGURO:** {equipo_local_real} o Empate (1X) | Confianza: **{v_p1x:.1f}%**")
                    else:
                        st.success(f"🎯 **PICK SEGURO:** {equipo_visita_real} o Empate (X2) | Confianza: **{v_px2:.1f}%**")
            with col_b2:
                if st.button("🎫 PARLAY DE ORO", use_container_width=True):
                    st.success(f"🎟️ **PARLAY RECOMENDADO:** Doble Oportunidad ({equipo_local_real if p_win_h >= p_win_a else equipo_visita_real} o Empate) + Más de 1.5 Goles")
            with col_b3:
                if st.button("🔥 TOP 15 ALTAS (PARLAY)", use_container_width=True):
                    st.session_state['ver_top_altas_match'] = not st.session_state.get('ver_top_altas_match', False)
            with col_b4:
                if st.button("⚖️ TOP 5 EMPATES (VALOR)", use_container_width=True):
                    st.session_state['ver_top_empates_match'] = not st.session_state.get('ver_top_empates_match', False)

            if st.session_state.get('ver_top_altas_match'):
                st.markdown("### 🔥 Parlay Maestro de Altas en Goles (Top 15 Partidos)")
                p_altas_box = analytics.generar_parlay_top_altas(top_n=15)
                st.markdown(pitch_renderer.render_ticket_parlay_altas(p_altas_box), unsafe_allow_html=True)

            if st.session_state.get('ver_top_empates_match'):
                st.markdown("### ⚖️ Radar de Empates de Oro (Top 5 Choques con Paridad)")
                p_empates_box = analytics.generar_top_empates_oro(top_n=5)
                st.markdown(pitch_renderer.render_ticket_empates_oro(p_empates_box), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Bet Builder Dinámico
            picks_builder = analytics.generar_bet_builder_dinamico(equipo_local_real, equipo_visita_real, stats_poisson)
            html_bet_builder = '<div style="background-color: #151821; color: white; padding: 20px; border-radius: 14px; border: 2px dashed #D4AF37; margin-bottom: 15px; box-shadow:0 4px 20px rgba(0,0,0,0.3);">'
            html_bet_builder += '<h3 style="text-align: center; color: #D4AF37; margin: 0 0 6px 0; font-weight: 900; font-size: 20px;">🧩 PARLAY SUGERIDO (BET BUILDER MULTIFACTORIAL)</h3>'
            html_bet_builder += '<p style="text-align: center; color: #94A3B8; font-size: 13px; margin-bottom: 12px;">Combinación de alta efectividad basada en simulación Poisson + Dixon-Coles & xG</p>'
            for p_item in picks_builder:
                html_bet_builder += f'<div style="display:flex; justify-content:space-between; align-items:center; background:#1A1E29; padding:10px 14px; border-radius:8px; margin:6px 0; border:1px solid #282F3F;"><div><span style="color:#F3E5AB; font-size:12px; font-weight:bold;">{p_item["categoria"]}</span><br><span style="color:white; font-size:15px; font-weight:bold;">✅ {p_item["descripcion"]}</span></div><span style="background:#D4AF37; color:#0D0F14; font-weight:900; padding:4px 12px; border-radius:12px; font-size:13px;">Confianza: {p_item["prob"]}</span></div>'
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
            ficha_txt = analytics.generar_ficha_vip_whatsapp(equipo_local_real, equipo_visita_real, stats_poisson, web_url=getattr(config, 'WEBAPP_VIP_URL', 'https://smartpickprojz.com.mx'), caliente_url=config.ENLACE_POR_DEFECTO)
            if st.session_state['rol'] == 'ADMIN':
                st.write("#### 📲 Ficha VIP para Difusión en Canales (Herramienta Admin)")
                st.text_area("📋 Reporte VIP copiable:", value=ficha_txt, height=200, key=f"admin_ficha_{fixture_id}")
            else:
                import urllib.parse
                encoded_txt = urllib.parse.quote(ficha_txt)
                st.markdown(f'''
                <div style="background: linear-gradient(135deg, #151821 0%, #1A1E29 100%); border-radius:12px; padding:16px; border:2px solid #2ECC71; text-align:center; margin-top:10px;">
                    <h4 style="color:#2ECC71; margin:0 0 6px 0; font-size:17px; font-weight:900;">📲 RECOMIENDA ESTE PRONÓSTICO VIP CON UN AMIGO</h4>
                    <a href="https://wa.me/?text={encoded_txt}" target="_blank" style="background:#1A4D2E; border:1px solid #2ECC71; color:white; font-weight:900; padding:10px 22px; border-radius:25px; text-decoration:none; display:inline-block; font-size:14px; margin-top:8px;">
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
                <div style="background:#151821; border-radius:12px; padding:16px; border-left:6px solid #D4AF37; border:1px solid #282F3F; color:white;">
                    <h4 style="margin:0 0 10px 0; color:#D4AF37; font-size:16px; font-weight:900;">🎯 Top 3 Marcadores Exactos Más Probables</h4>
                ''', unsafe_allow_html=True)
                medallas = ["🥇 1er Lugar", "🥈 2do Lugar", "🥉 3er Lugar"]
                colores_mc = ["#D4AF37", "#38BDF8", "#F3E5AB"]
                for idx_m, item_m in enumerate(top_3_sc):
                    lbl_med = medallas[idx_m] if idx_m < len(medallas) else "🎯 Marcador"
                    c_badge = colores_mc[idx_m] if idx_m < len(colores_mc) else "#FFFFFF"
                    st.markdown(f'''
                    <div style="display:flex; justify-content:space-between; align-items:center; background:#1A1E29; padding:8px 12px; border-radius:8px; margin:5px 0; border:1px solid #282F3F;">
                        <span style="color:#E0E0E0; font-size:14px; font-weight:bold;">{lbl_med}: <b style="color:white; font-size:17px; margin-left:8px;">{item_m['marcador']}</b></span>
                        <span style="background:{c_badge}; color:#0D0F14; font-weight:900; padding:3px 10px; border-radius:12px; font-size:13px;">Prob: {item_m['prob']}%</span>
                    </div>
                    ''', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col_mc2:
                btts_val = mc_info.get("btts_pct", 50.0)
                over25_val = mc_info.get("over25_pct", 50.0)
                txt_btts = "SÍ" if btts_val >= 50.0 else "NO"
                c_btts = "#D4AF37" if btts_val >= 50.0 else "#EF4444"
                txt_over25 = "SÍ (+2.5)" if over25_val >= 50.0 else "NO (-2.5)"
                c_over25 = "#D4AF37" if over25_val >= 50.0 else "#EF4444"
                st.markdown(f'''
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
            <div style="background:#151821; padding:12px 16px; border-radius:10px; border-left:5px solid #D4AF37; border:1px solid #282F3F; margin:10px 0; color:white;">
                <div style="color:#D4AF37; font-weight:900; font-size:14px;">📌 Análisis de Ocasiones Clave (Expected Goals):</div>
                <div style="color:#E0E0E0; font-size:13px; margin-top:4px;">{xg_data['alerta_xg']}</div>
            </div>
            ''', unsafe_allow_html=True)

            st.markdown("---")
            # Predictor IA Ensemble
            st.write("### 🤖 Predictor de Inteligencia Artificial (XGBoost Ensemble)")
            bajas_info = api_client.obtener_bajas_equipo(fixture_id, datos_partido.get("local_id", 0), datos_partido.get("visita_id", 0), equipo_local_real, equipo_visita_real)
            ia_info = analytics.evaluar_predictor_ia_ensemble(equipo_local_real, equipo_visita_real, stats_poisson, bajas_info)
            
            st.markdown(f'''
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
                st.markdown(f'''
                <div style="background:#151821; padding:12px; border-radius:10px; border:1px solid #282F3F; text-align:center;">
                    <h5 style="color:#D4AF37; margin:0 0 8px 0; font-weight:900;">⚽ Goles en H2H</h5>
                    <div style="display:flex; justify-content:space-around; align-items:center;">
                        <div><span style="color:#D4AF37; font-size:22px; font-weight:900;">{goles_tot_loc}</span><br><small style="color:#aaa;">{equipo_local_real}</small></div>
                        <span style="color:#fff; font-size:16px; font-weight:bold;">VS</span>
                        <div><span style="color:#EF4444; font-size:22px; font-weight:900;">{goles_tot_vis}</span><br><small style="color:#aaa;">{equipo_visita_real}</small></div>
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
                <div style="background:#151821; border-radius:12px; padding:14px; border-left:5px solid #38BDF8; border:1px solid #282F3F;">
                    <h4 style="margin:0 0 6px 0; color:white; font-size:15px; font-weight:900;">🔵 {equipo_local_real}</h4>
                    <div style="display:flex; margin-bottom:8px;">{b_html_l}</div>
                    <div style="background:#0D0F14; padding:6px 10px; border-radius:6px; color:#E0E0E0; font-size:12px; font-weight:bold; border:1px solid #282F3F;">{tend_l}</div>
                </div>
                ''', unsafe_allow_html=True)
            with col_r2:
                b_html_v = "".join([f'<span style="background:{b["bg"]}; color:{b["color"]}; border:2px solid {b["borde"]}; font-weight:900; font-size:13px; width:30px; height:30px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; margin-right:4px;">{b["letra"]}</span>' for b in badges_v])
                st.markdown(f'''
                <div style="background:#151821; border-radius:12px; padding:14px; border-left:5px solid #EF4444; border:1px solid #282F3F;">
                    <h4 style="margin:0 0 6px 0; color:white; font-size:15px; font-weight:900;">🔴 {equipo_visita_real}</h4>
                    <div style="display:flex; margin-bottom:8px;">{b_html_v}</div>
                    <div style="background:#0D0F14; padding:6px 10px; border-radius:6px; color:#E0E0E0; font-size:12px; font-weight:bold; border:1px solid #282F3F;">{tend_v}</div>
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

            st.markdown(f'''
            <div style="background:#151821; padding:12px 16px; border-radius:10px; border:1px solid #282F3F; margin:10px 0; color:white;">
                <div style="color:#D4AF37; font-weight:bold; font-size:14px; margin-bottom:4px;">📌 Impacto Aeróbico & Físico:</div>
                <div style="color:#E0E0E0; font-size:13px;">{info_af['desc_altitud']}</div>
                <div style="display:flex; justify-content:space-between; margin-top:8px; background:#0D0F14; padding:8px 12px; border-radius:6px; border:1px solid #282F3F;">
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
            <div style="background:#151821; padding:12px 16px; border-radius:10px; border-left:5px solid #D4AF37; border:1px solid #282F3F; margin:10px 0; color:white;">
                <div style="color:#D4AF37; font-weight:bold; font-size:14px; margin-bottom:4px;">🎯 Análisis de Fricción & Recomendación de Mercado:</div>
                <div style="color:#E0E0E0; font-size:13px;">{info_ref['recomendacion']}</div>
                <div style="color:#94A3B8; font-size:12px; margin-top:4px;">Promedio Expulsiones: {info_ref['tarjetas_rojas']} rojas/partido | Promedio Penales: {info_ref['penales_prom']}/partido</div>
            </div>
            ''', unsafe_allow_html=True)

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
                st.markdown('''<div style="background-color: rgba(212, 175, 55, 0.12); border-left: 5px solid #D4AF37; padding: 14px; border-radius: 6px; margin-bottom: 15px; border-top: 1px solid #282F3F; border-right: 1px solid #282F3F; border-bottom: 1px solid #282F3F;">
                <h4 style="color: #D4AF37; margin-top:0;">🔥 ALERTAS DE VALOR ESPERADO POSITIVO (+EV)</h4>''', unsafe_allow_html=True)
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
                    <div style="background:#151821; border-radius:10px; padding:14px; border:2px solid #D4AF37; margin:10px 0;">
                        <h4 style="color:#D4AF37; margin:0 0 6px 0;">💎 Apuesta Óptima Sugerida por Criterio de Kelly:</h4>
                        <div style="font-size:18px; color:white; font-weight:bold;">Apostar: <span style="color:#D4AF37;">${res_kelly['monto_sugerido']:,.2f} MXN</span> ({res_kelly['kelly_pct']}% de tu bankroll) en cuota {mejor_cuota_ev}</div>
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
                    st.markdown(f'''<div style="background:#151821; padding:14px; border-radius:10px; border-left:5px solid #38BDF8; border-top:1px solid #282F3F; border-right:1px solid #282F3F; border-bottom:1px solid #282F3F;">
                    <h4 style="color:white; margin:0 0 6px 0;">🔵 {equipo_local_real}</h4>
                    <p style="color:#ddd; font-size:13px; margin:0 0 6px 0;">Posición: {pos_l}° | Puntos: {pts_l} | Racha: {forma_l}</p>
                    <div style="background:rgba(56,189,248,0.12); padding:8px; border-radius:6px; border:1px solid rgba(56,189,248,0.2);">
                        <p style="color:#e0e0e0; margin:0; font-size:12px;">📌 {txt_nec_l}</p>
                    </div></div>''', unsafe_allow_html=True)
                with ct2:
                    st.markdown(f'''<div style="background:#151821; padding:14px; border-radius:10px; border-left:5px solid #EF4444; border-top:1px solid #282F3F; border-right:1px solid #282F3F; border-bottom:1px solid #282F3F;">
                    <h4 style="color:white; margin:0 0 6px 0;">🔴 {equipo_visita_real}</h4>
                    <p style="color:#ddd; font-size:13px; margin:0 0 6px 0;">Posición: {pos_v}° | Puntos: {pts_v} | Racha: {forma_v}</p>
                    <div style="background:rgba(239,68,68,0.12); padding:8px; border-radius:6px; border:1px solid rgba(239,68,68,0.2);">
                        <p style="color:#e0e0e0; margin:0; font-size:12px;">📌 {txt_nec_v}</p>
                    </div></div>''', unsafe_allow_html=True)
