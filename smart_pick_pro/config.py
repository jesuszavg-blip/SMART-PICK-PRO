import os
from pathlib import Path

# Intentar cargar python-dotenv si está disponible
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass

# Configuración Global
API_KEY = os.getenv("API_KEY", "eaa462feb62091195f0130bc4373796f")
SECRET_KEY = os.getenv("SECRET_KEY", "smart_pick_pro_super_secret_jwt_key_2026")
ADMIN_INIT_USER = os.getenv("ADMIN_INIT_USER", "admin")
ADMIN_INIT_PASS = os.getenv("ADMIN_INIT_PASS", "SmartVIP2026!")

# Enlaces de Casas de Apuestas (Afiliados / Referencia)
ENLACES_CASINOS = {
    "1xBet": "https://reffpa.com/L?tag=d_6029550m_1599c_&site=6029550&ad=1599",
    "Mexplay": "https://mexplay.mx/?referral=mqx6lb",
    "Caliente": "https://www.caliente.mx/ofertas/raf/?member=CALIRAF&var1=undefined",
    "Betmaster": "https://betmaster.net/?rsd=UmRoJ7BQ",
    "Winpot": "https://winpot.mx/r/5296706_0Socp8oK",
}

ENLACE_1XBET = ENLACES_CASINOS["1xBet"]
ENLACE_MEXPLAY = ENLACES_CASINOS["Mexplay"]
ENLACE_POR_DEFECTO = ENLACES_CASINOS["1xBet"]
ENLACE_WHATSAPP = "https://wa.me/526676947014?text=Hola%20Jesus,%20quiero%20obtener%20acceso%20a%20Smart%20Pick%20Pro"
# Datos de Pago Directo (BanCoppel, Mercado Pago, PayPal, Bitso USDT)
BANCOPPEL_TARJETA = os.getenv("BANCOPPEL_TARJETA", "4169 1608 7646 1600")
BANCOPPEL_TITULAR = os.getenv("BANCOPPEL_TITULAR", "Jesús")
MERCADOPAGO_LINK = os.getenv("MERCADOPAGO_LINK", "https://mpago.la/1ZefYpR")
PAYPAL_LINK = os.getenv("PAYPAL_LINK", "https://www.paypal.com/ncp/payment/HSSHUFTYF8FG2")
BITSO_USDT_TRC20 = os.getenv("BITSO_USDT_TRC20", "TUyvrvPjGyh9v5SDYHW7GZ1g4MomKSFkh2")

# Configuración del Programa de Afiliados y Membresía
DOMINIO_APP = os.getenv("DOMINIO_APP", "https://smartpickprojz.com")
PRECIO_VIP_MXN = float(os.getenv("PRECIO_VIP_MXN", "149.0"))
COMISION_MES_1 = float(os.getenv("COMISION_MES_1", "0.50"))  # 50%
COMISION_MES_2 = float(os.getenv("COMISION_MES_2", "0.40"))  # 40%
COMISION_MES_RECURRENTE = float(os.getenv("COMISION_MES_RECURRENTE", "0.30"))  # 30%
MINIMO_RETIRO_AFILIADO = float(os.getenv("MINIMO_RETIRO_AFILIADO", "100.0"))  # $100 MXN

# API Base URL
API_FOOTBALL_URL = "https://v3.football.api-sports.io"

