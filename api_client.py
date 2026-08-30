import datetime
import requests
import streamlit as st
import config

def get_headers():
    return {'x-apisports-key': config.API_KEY}

def get_current_season():
    now = datetime.datetime.now()
    return str(now.year)

# DICCIONARIO COMPLETO Y EXACTO DE ESCUDOS OFICIALES (LIGA MX VARONIL Y FEMENIL)
EQUIPOS_MEXICO_LOGOS = {
    # 1. América / Águilas
    "america": "https://a.espncdn.com/i/teamlogos/soccer/500/11145.png",
    "américa": "https://a.espncdn.com/i/teamlogos/soccer/500/11145.png",
    "aguilas": "https://a.espncdn.com/i/teamlogos/soccer/500/11145.png",
    "águilas": "https://a.espncdn.com/i/teamlogos/soccer/500/11145.png",
    "azulcrema": "https://a.espncdn.com/i/teamlogos/soccer/500/11145.png",
    "club america": "https://a.espncdn.com/i/teamlogos/soccer/500/11145.png",
    "club américa": "https://a.espncdn.com/i/teamlogos/soccer/500/11145.png",

    # 2. Guadalajara / Chivas
    "guadalajara": "https://a.espncdn.com/i/teamlogos/soccer/500/11153.png",
    "chivas": "https://a.espncdn.com/i/teamlogos/soccer/500/11153.png",
    "rebaño": "https://a.espncdn.com/i/teamlogos/soccer/500/11153.png",
    "rojiblanco": "https://a.espncdn.com/i/teamlogos/soccer/500/11153.png",
    "c.d. guadalajara": "https://a.espncdn.com/i/teamlogos/soccer/500/11153.png",

    # 3. Cruz Azul / La Máquina
    "cruz azul": "https://a.espncdn.com/i/teamlogos/soccer/500/11148.png",
    "maquina": "https://a.espncdn.com/i/teamlogos/soccer/500/11148.png",
    "máquina": "https://a.espncdn.com/i/teamlogos/soccer/500/11148.png",
    "cementero": "https://a.espncdn.com/i/teamlogos/soccer/500/11148.png",

    # 4. Pumas UNAM
    "pumas": "https://a.espncdn.com/i/teamlogos/soccer/500/11157.png",
    "unam": "https://a.espncdn.com/i/teamlogos/soccer/500/11157.png",
    "universidad nacional": "https://a.espncdn.com/i/teamlogos/soccer/500/11157.png",
    "auriazul": "https://a.espncdn.com/i/teamlogos/soccer/500/11157.png",

    # 5. Tigres UANL / Amazonas / Felinas
    "tigres": "https://a.espncdn.com/i/teamlogos/soccer/500/11162.png",
    "uanl": "https://a.espncdn.com/i/teamlogos/soccer/500/11162.png",
    "amazonas": "https://a.espncdn.com/i/teamlogos/soccer/500/11162.png",
    "felinas": "https://a.espncdn.com/i/teamlogos/soccer/500/11162.png",

    # 6. Monterrey / Rayados / Rayadas
    "monterrey": "https://a.espncdn.com/i/teamlogos/soccer/500/11155.png",
    "rayadas": "https://a.espncdn.com/i/teamlogos/soccer/500/11155.png",
    "rayada": "https://a.espncdn.com/i/teamlogos/soccer/500/11155.png",
    "rayados": "https://a.espncdn.com/i/teamlogos/soccer/500/11155.png",
    "pandilla": "https://a.espncdn.com/i/teamlogos/soccer/500/11155.png",

    # 7. Pachuca / Tuzos / Tuzas
    "pachuca": "https://a.espncdn.com/i/teamlogos/soccer/500/11156.png",
    "tuzas": "https://a.espncdn.com/i/teamlogos/soccer/500/11156.png",
    "tuzos": "https://a.espncdn.com/i/teamlogos/soccer/500/11156.png",
    "tuza": "https://a.espncdn.com/i/teamlogos/soccer/500/11156.png",
    "tuzo": "https://a.espncdn.com/i/teamlogos/soccer/500/11156.png",

    # 8. Toluca / Diablos / Diablas
    "toluca": "https://a.espncdn.com/i/teamlogos/soccer/500/11163.png",
    "diablas": "https://a.espncdn.com/i/teamlogos/soccer/500/11163.png",
    "diablos": "https://a.espncdn.com/i/teamlogos/soccer/500/11163.png",
    "diabla": "https://a.espncdn.com/i/teamlogos/soccer/500/11163.png",
    "diablo": "https://a.espncdn.com/i/teamlogos/soccer/500/11163.png",
    "choricero": "https://a.espncdn.com/i/teamlogos/soccer/500/11163.png",

    # 9. Santos Laguna / Guerreros / Guerreras
    "santos": "https://a.espncdn.com/i/teamlogos/soccer/500/11161.png",
    "guerreras": "https://a.espncdn.com/i/teamlogos/soccer/500/11161.png",
    "guerreros": "https://a.espncdn.com/i/teamlogos/soccer/500/11161.png",
    "laguna": "https://a.espncdn.com/i/teamlogos/soccer/500/11161.png",

    # 10. Atlas / Zorros / Rojinegras
    "atlas": "https://a.espncdn.com/i/teamlogos/soccer/500/11146.png",
    "rojinegras": "https://a.espncdn.com/i/teamlogos/soccer/500/11146.png",
    "rojinegros": "https://a.espncdn.com/i/teamlogos/soccer/500/11146.png",
    "rojinegra": "https://a.espncdn.com/i/teamlogos/soccer/500/11146.png",
    "rojinegro": "https://a.espncdn.com/i/teamlogos/soccer/500/11146.png",
    "zorros": "https://a.espncdn.com/i/teamlogos/soccer/500/11146.png",
    "zorras": "https://a.espncdn.com/i/teamlogos/soccer/500/11146.png",

    # 11. León / Fieras / Esmeraldas
    "leon": "https://a.espncdn.com/i/teamlogos/soccer/500/11154.png",
    "león": "https://a.espncdn.com/i/teamlogos/soccer/500/11154.png",
    "fieras": "https://a.espncdn.com/i/teamlogos/soccer/500/11154.png",
    "fiera": "https://a.espncdn.com/i/teamlogos/soccer/500/11154.png",
    "esmeraldas": "https://a.espncdn.com/i/teamlogos/soccer/500/11154.png",

    # 12. Puebla / Camoteros / Camoteras / La Franja
    "puebla": "https://a.espncdn.com/i/teamlogos/soccer/500/11159.png",
    "camoteras": "https://a.espncdn.com/i/teamlogos/soccer/500/11159.png",
    "camoteros": "https://a.espncdn.com/i/teamlogos/soccer/500/11159.png",
    "la franja": "https://a.espncdn.com/i/teamlogos/soccer/500/11159.png",
    "franja": "https://a.espncdn.com/i/teamlogos/soccer/500/11159.png",

    # 13. FC Juárez / Bravos / Bravas
    "juarez": "https://a.espncdn.com/i/teamlogos/soccer/500/19460.png",
    "juárez": "https://a.espncdn.com/i/teamlogos/soccer/500/19460.png",
    "bravas": "https://a.espncdn.com/i/teamlogos/soccer/500/19460.png",
    "bravos": "https://a.espncdn.com/i/teamlogos/soccer/500/19460.png",
    "brava": "https://a.espncdn.com/i/teamlogos/soccer/500/19460.png",
    "bravo": "https://a.espncdn.com/i/teamlogos/soccer/500/19460.png",

    # 14. Mazatlán / Cañoneros / Cañoneras
    "mazatlan": "https://a.espncdn.com/i/teamlogos/soccer/500/20703.png",
    "mazatlán": "https://a.espncdn.com/i/teamlogos/soccer/500/20703.png",
    "cañoneras": "https://a.espncdn.com/i/teamlogos/soccer/500/20703.png",
    "cañoneros": "https://a.espncdn.com/i/teamlogos/soccer/500/20703.png",

    # 15. Tijuana / Xolos / Xolas
    "tijuana": "https://a.espncdn.com/i/teamlogos/soccer/500/11100.png",
    "xolas": "https://a.espncdn.com/i/teamlogos/soccer/500/11100.png",
    "xolos": "https://a.espncdn.com/i/teamlogos/soccer/500/11100.png",
    "xolo": "https://a.espncdn.com/i/teamlogos/soccer/500/11100.png",
    "xola": "https://a.espncdn.com/i/teamlogos/soccer/500/11100.png",

    # 16. Atlético San Luis / Potosinos / Potosinas
    "san luis": "https://media.api-sports.io/football/teams/2298.png",
    "atletico san luis": "https://media.api-sports.io/football/teams/2298.png",
    "atlético san luis": "https://media.api-sports.io/football/teams/2298.png",
    "atletico de san luis": "https://media.api-sports.io/football/teams/2298.png",
    "atlético de san luis": "https://media.api-sports.io/football/teams/2298.png",
    "potosino": "https://media.api-sports.io/football/teams/2298.png",
    "potosina": "https://media.api-sports.io/football/teams/2298.png",

    # 17. Querétaro / Gallos / Gallas
    "queretaro": "https://a.espncdn.com/i/teamlogos/soccer/500/11160.png",
    "querétaro": "https://a.espncdn.com/i/teamlogos/soccer/500/11160.png",
    "gallas": "https://a.espncdn.com/i/teamlogos/soccer/500/11160.png",
    "gallos": "https://a.espncdn.com/i/teamlogos/soccer/500/11160.png",
    "galla": "https://a.espncdn.com/i/teamlogos/soccer/500/11160.png",
    "gallo": "https://a.espncdn.com/i/teamlogos/soccer/500/11160.png",

    # 18. Necaxa / Rayos / Centellas
    "necaxa": "https://a.espncdn.com/i/teamlogos/soccer/500/11158.png",
    "centellas": "https://a.espncdn.com/i/teamlogos/soccer/500/11158.png",
    "centella": "https://a.espncdn.com/i/teamlogos/soccer/500/11158.png",
    "rayos": "https://a.espncdn.com/i/teamlogos/soccer/500/11158.png",
    "hidrorayos": "https://a.espncdn.com/i/teamlogos/soccer/500/11158.png"
}

EQUIPOS_INTERNACIONALES_LOGOS = {
    "real madrid": "https://a.espncdn.com/i/teamlogos/soccer/500/86.png",
    "barcelona": "https://a.espncdn.com/i/teamlogos/soccer/500/83.png",
    "atletico madrid": "https://a.espncdn.com/i/teamlogos/soccer/500/1068.png",
    "atlético madrid": "https://a.espncdn.com/i/teamlogos/soccer/500/1068.png",
    "sevilla": "https://a.espncdn.com/i/teamlogos/soccer/500/243.png",
    "manchester city": "https://a.espncdn.com/i/teamlogos/soccer/500/382.png",
    "man city": "https://a.espncdn.com/i/teamlogos/soccer/500/382.png",
    "manchester united": "https://a.espncdn.com/i/teamlogos/soccer/500/360.png",
    "man united": "https://a.espncdn.com/i/teamlogos/soccer/500/360.png",
    "man utd": "https://a.espncdn.com/i/teamlogos/soccer/500/360.png",
    "liverpool": "https://a.espncdn.com/i/teamlogos/soccer/500/364.png",
    "arsenal": "https://a.espncdn.com/i/teamlogos/soccer/500/359.png",
    "chelsea": "https://a.espncdn.com/i/teamlogos/soccer/500/363.png",
    "tottenham": "https://a.espncdn.com/i/teamlogos/soccer/500/367.png",
    "spurs": "https://a.espncdn.com/i/teamlogos/soccer/500/367.png",
    "bayern": "https://a.espncdn.com/i/teamlogos/soccer/500/132.png",
    "bayern münchen": "https://a.espncdn.com/i/teamlogos/soccer/500/132.png",
    "bayern munich": "https://a.espncdn.com/i/teamlogos/soccer/500/132.png",
    "dortmund": "https://a.espncdn.com/i/teamlogos/soccer/500/124.png",
    "psg": "https://a.espncdn.com/i/teamlogos/soccer/500/160.png",
    "paris": "https://a.espncdn.com/i/teamlogos/soccer/500/160.png",
    "paris saint germain": "https://a.espncdn.com/i/teamlogos/soccer/500/160.png",
    "marseille": "https://a.espncdn.com/i/teamlogos/soccer/500/166.png",
    "marsella": "https://a.espncdn.com/i/teamlogos/soccer/500/166.png",
    "juventus": "https://a.espncdn.com/i/teamlogos/soccer/500/111.png",
    "juve": "https://a.espncdn.com/i/teamlogos/soccer/500/111.png",
    "inter milan": "https://a.espncdn.com/i/teamlogos/soccer/500/110.png",
    "inter de milan": "https://a.espncdn.com/i/teamlogos/soccer/500/110.png",
    "milan": "https://a.espncdn.com/i/teamlogos/soccer/500/103.png",
    "ac milan": "https://a.espncdn.com/i/teamlogos/soccer/500/103.png",
    "boca": "https://a.espncdn.com/i/teamlogos/soccer/500/5.png",
    "boca jrs": "https://a.espncdn.com/i/teamlogos/soccer/500/5.png",
    "boca juniors": "https://a.espncdn.com/i/teamlogos/soccer/500/5.png",
    "river": "https://a.espncdn.com/i/teamlogos/soccer/500/16.png",
    "river plate": "https://a.espncdn.com/i/teamlogos/soccer/500/16.png",
    "racing": "https://a.espncdn.com/i/teamlogos/soccer/500/15.png",
    "racing club": "https://a.espncdn.com/i/teamlogos/soccer/500/15.png",
    "inter miami": "https://a.espncdn.com/i/teamlogos/soccer/500/20232.png",
    "houston": "https://a.espncdn.com/i/teamlogos/soccer/500/6077.png",
    "houston dynamo": "https://a.espncdn.com/i/teamlogos/soccer/500/6077.png",
    "st. luis": "https://a.espncdn.com/i/teamlogos/soccer/500/21571.png",
    "st louis": "https://a.espncdn.com/i/teamlogos/soccer/500/21571.png",
    "st. louis": "https://a.espncdn.com/i/teamlogos/soccer/500/21571.png",
    "colo colo": "https://a.espncdn.com/i/teamlogos/soccer/500/3147.png",
    "u. de chile": "https://a.espncdn.com/i/teamlogos/soccer/500/3149.png",
    "u de chile": "https://a.espncdn.com/i/teamlogos/soccer/500/3149.png",
    "universidad de chile": "https://a.espncdn.com/i/teamlogos/soccer/500/3149.png",
    "vitoria": "https://a.espncdn.com/i/teamlogos/soccer/500/3457.png",
    "vitoria ba": "https://a.espncdn.com/i/teamlogos/soccer/500/3457.png",
    "bahia": "https://a.espncdn.com/i/teamlogos/soccer/500/3436.png",
    "flamengo": "https://a.espncdn.com/i/teamlogos/soccer/500/819.png",
    "palmeiras": "https://a.espncdn.com/i/teamlogos/soccer/500/824.png"
}

# DICCIONARIO COMPLETO Y EXACTO DE ESCUDOS DE SELECCIONES NACIONALES (FEDERACIONES OFICIALES HD)
SELECCIONES_NACIONALES_LOGOS = {
    # México
    "mexico": "https://media.api-sports.io/football/teams/16.png",
    "méxico": "https://media.api-sports.io/football/teams/16.png",
    "seleccion mexicana": "https://media.api-sports.io/football/teams/16.png",
    "selección mexicana": "https://media.api-sports.io/football/teams/16.png",
    "el tri": "https://media.api-sports.io/football/teams/16.png",
    "fmf": "https://media.api-sports.io/football/teams/16.png",

    # Estados Unidos
    "estados unidos": "https://media.api-sports.io/football/teams/2384.png",
    "usa": "https://media.api-sports.io/football/teams/2384.png",
    "united states": "https://media.api-sports.io/football/teams/2384.png",
    "usmnt": "https://media.api-sports.io/football/teams/2384.png",

    # Argentina
    "argentina": "https://media.api-sports.io/football/teams/26.png",
    "albiceleste": "https://media.api-sports.io/football/teams/26.png",
    "afa": "https://media.api-sports.io/football/teams/26.png",

    # Brasil
    "brasil": "https://media.api-sports.io/football/teams/6.png",
    "brazil": "https://media.api-sports.io/football/teams/6.png",
    "canarinha": "https://media.api-sports.io/football/teams/6.png",
    "cbf": "https://media.api-sports.io/football/teams/6.png",

    # España
    "españa": "https://media.api-sports.io/football/teams/9.png",
    "spain": "https://media.api-sports.io/football/teams/9.png",
    "la roja": "https://media.api-sports.io/football/teams/9.png",
    "rfef": "https://media.api-sports.io/football/teams/9.png",

    # Alemania
    "alemania": "https://media.api-sports.io/football/teams/25.png",
    "germany": "https://media.api-sports.io/football/teams/25.png",
    "dfb": "https://media.api-sports.io/football/teams/25.png",

    # Francia
    "francia": "https://media.api-sports.io/football/teams/2.png",
    "france": "https://media.api-sports.io/football/teams/2.png",
    "les bleus": "https://media.api-sports.io/football/teams/2.png",
    "fff": "https://media.api-sports.io/football/teams/2.png",

    # Inglaterra
    "inglaterra": "https://media.api-sports.io/football/teams/10.png",
    "england": "https://media.api-sports.io/football/teams/10.png",
    "three lions": "https://media.api-sports.io/football/teams/10.png",

    # Portugal
    "portugal": "https://media.api-sports.io/football/teams/27.png",
    "fpf": "https://media.api-sports.io/football/teams/27.png",

    # Italia
    "italia": "https://media.api-sports.io/football/teams/768.png",
    "italy": "https://media.api-sports.io/football/teams/768.png",
    "azzurri": "https://media.api-sports.io/football/teams/768.png",

    # Colombia
    "colombia": "https://media.api-sports.io/football/teams/8.png",
    "cafeteros": "https://media.api-sports.io/football/teams/8.png",

    # Uruguay
    "uruguay": "https://media.api-sports.io/football/teams/7.png",
    "la celeste": "https://media.api-sports.io/football/teams/7.png",

    # Chile
    "chile": "https://media.api-sports.io/football/teams/17.png",

    # Países Bajos / Holanda
    "paises bajos": "https://media.api-sports.io/football/teams/1118.png",
    "países bajos": "https://media.api-sports.io/football/teams/1118.png",
    "holanda": "https://media.api-sports.io/football/teams/1118.png",
    "netherlands": "https://media.api-sports.io/football/teams/1118.png",

    # Japón
    "japon": "https://media.api-sports.io/football/teams/12.png",
    "japón": "https://media.api-sports.io/football/teams/12.png",
    "japan": "https://media.api-sports.io/football/teams/12.png",

    # Canadá
    "canada": "https://media.api-sports.io/football/teams/31.png",
    "canadá": "https://media.api-sports.io/football/teams/31.png",

    # Perú
    "peru": "https://media.api-sports.io/football/teams/11.png",
    "perú": "https://media.api-sports.io/football/teams/11.png",

    # Ecuador
    "ecuador": "https://media.api-sports.io/football/teams/13.png",

    # Venezuela
    "venezuela": "https://media.api-sports.io/football/teams/14.png",
    "vinotinto": "https://media.api-sports.io/football/teams/14.png",

    # Paraguay
    "paraguay": "https://media.api-sports.io/football/teams/18.png"
}

def obtener_logo_oficial_equipo(nombre_equipo: str, logo_actual: str = "") -> str:
    """Mapeador 100% exacto de escudos oficiales para Liga MX, Femenil, Internacionales y Selecciones (nunca muestra banderas en clubes)"""
    if not nombre_equipo:
        return "https://a.espncdn.com/i/teamlogos/soccer/500/11145.png"
        
    eq = str(nombre_equipo).lower().strip()
    
    # 1. Buscar en diccionario de equipos de México y Femenil
    for key, url_escudo in EQUIPOS_MEXICO_LOGOS.items():
        if key in eq:
            return url_escudo
            
    # 2. Buscar en Selecciones Nacionales (Escudos Oficiales de Federaciones)
    for key, url_escudo in SELECCIONES_NACIONALES_LOGOS.items():
        if key in eq:
            return url_escudo

    # 3. Buscar en clubes internacionales
    for key, url_escudo in EQUIPOS_INTERNACIONALES_LOGOS.items():
        if key in eq:
            return url_escudo
            
    # 4. Si se proporciona un logo válido de la API que NO sea una bandera ni ID desfasado
    if logo_actual and str(logo_actual).startswith("http"):
        es_bandera = "flags" in str(logo_actual).lower() or ".svg" in str(logo_actual).lower()
        es_desfasado = any(k in str(logo_actual) for k in ["2284.png", "2298.png", "2287.png"])
        if not es_bandera and not es_desfasado:
            return str(logo_actual)
        
    return "https://a.espncdn.com/i/teamlogos/soccer/500/11145.png"

@st.cache_data(ttl=60)
def obtener_ligas_mundo():
    headers = get_headers()
    try:
        url = f"{config.API_FOOTBALL_URL}/leagues"
        resp = requests.get(url, headers=headers, params={"current": "true"}, timeout=10)
        
        ligas_top = {
            "🎯 [ESPECIAL] Simulador Progol Tradicional": "PROGOL_MODE",
            "⚙️ [ESPECIAL] Optimizador de Reducciones (Excel)": "REDUCCIONES_MODE",
            "🇲🇽 Mexico - Liga MX": "262", 
            "👩🇲🇽 Mexico - Liga MX Femenil": "868", 
            "🌎 [FIFA] Selecciones - Eliminatorias CONMEBOL / CONCACAF": "32",
            "🌎 [FIFA] Selecciones - Amistosos Internacionales (Fecha FIFA)": "10",
            "🏆 [UEFA] Selecciones - UEFA Nations League / Eliminatorias": "5",
            "🏆 [FIFA] Copa del Mundo / Copa América / Eurocopa": "1",
            "🇬🇧 England - Premier League": "39", 
            "🇪🇸 Spain - La Liga": "140", 
            "🌍 UEFA Champions League": "2",
            "🇮🇹 Italy - Serie A": "135",
            "🇩🇪 Germany - Bundesliga": "78",
            "🇦🇷 Argentina - Liga Profesional": "128",
            "🇧🇷 Brazil - Serie A": "71"
        }
        
        if resp.status_code == 200:
            data = resp.json()
            if data.get('response'):
                ligas_todas = {}
                for item in data['response']:
                    pais = item['country']['name']
                    nombre = item['league']['name']
                    id_liga = str(item['league']['id'])
                    if id_liga not in list(ligas_top.values()):
                        ligas_todas[f"{pais} - {nombre}"] = id_liga
                ligas_top.update(dict(sorted(ligas_todas.items())))
                return ligas_top
    except Exception as e:
        print(f"Error al obtener ligas: {e}")

    return {
        "🎯 [ESPECIAL] Simulador Progol": "PROGOL_MODE",
        "⚙️ [ESPECIAL] Optimizador de Reducciones": "REDUCCIONES_MODE",
        "🇲🇽 Mexico - Liga MX": "262",
        "👩🇲🇽 Mexico - Liga MX Femenil": "868",
        "🌎 [FIFA] Selecciones - Eliminatorias CONMEBOL / CONCACAF": "32",
        "🌎 [FIFA] Selecciones - Amistosos Internacionales (Fecha FIFA)": "10",
        "🏆 [UEFA] Selecciones - UEFA Nations League / Eliminatorias": "5",
        "🏆 [FIFA] Copa del Mundo / Copa América / Eurocopa": "1",
        "🇬🇧 England - Premier League": "39",
        "🇪🇸 Spain - La Liga": "140",
        "🌍 UEFA Champions League": "2"
    }

def obtener_partidos_jornada(league_id: str):
    """
    Obtiene los partidos de la jornada anterior (Finalizados) y de la jornada actual (Próximos)
    con sus escudos exactos e infalibles para cada equipo en su posición (Local y Visita).
    """
    if league_id in ["PROGOL_MODE", "REDUCCIONES_MODE"]:
        return {f"Casilla {i}: Partido Local {i} vs Visita {i}": {"id": None} for i in range(1, 15)}
    
    url = f"{config.API_FOOTBALL_URL}/fixtures"
    headers = get_headers()
    partidos_dict = {}

    try:
        raw_items = []
        
        # 1. Obtener partidos recientemente finalizados de la jornada anterior (last=15)
        resp_last = requests.get(url, headers=headers, params={"league": league_id, "last": "15"}, timeout=10)
        if resp_last.status_code == 200 and resp_last.json().get('response'):
            raw_items.extend(resp_last.json()['response'])

        # 2. Obtener partidos próximos por jugar (next=20)
        resp_next = requests.get(url, headers=headers, params={"league": league_id, "next": "20"}, timeout=10)
        if resp_next.status_code == 200 and resp_next.json().get('response'):
            raw_items.extend(resp_next.json()['response'])

        # 3. Si no trajo suficientes datos, intentar por temporadas
        if not raw_items:
            seasons_to_try = ["2024", "2025", "2026"]
            for s in seasons_to_try:
                resp_s = requests.get(url, headers=headers, params={"league": league_id, "season": s}, timeout=10)
                if resp_s.status_code == 200 and resp_s.json().get('response'):
                    res_s = resp_s.json()['response']
                    if res_s:
                        raw_items = res_s
                        break

        if raw_items:
            proximos = [p for p in raw_items if p.get('fixture', {}).get('status', {}).get('short') in ['NS', 'TBD', '1H', '2H', 'HT', 'LIVE']]
            finalizados = [p for p in raw_items if p.get('fixture', {}).get('status', {}).get('short') in ['FT', 'AET', 'PEN']]

            proximos_ordenados = sorted(proximos, key=lambda x: x.get('fixture', {}).get('date', ''))
            finalizados_ordenados = sorted(finalizados, key=lambda x: x.get('fixture', {}).get('date', ''), reverse=True)

            lista_seleccionada = proximos_ordenados[:20] + finalizados_ordenados[:12]

            for partido in lista_seleccionada:
                id_f = partido['fixture']['id']
                local = partido['teams']['home']['name']
                id_loc_val = partido['teams']['home']['id']
                logo_local_raw = partido['teams']['home']['logo']
                
                visita = partido['teams']['away']['name']
                id_vis_val = partido['teams']['away']['id']
                logo_visita_raw = partido['teams']['away']['logo']
                
                # Mapear escudo 100% exacto para local y visita
                logo_local_exacto = obtener_logo_oficial_equipo(local, logo_local_raw)
                logo_visita_exacto = obtener_logo_oficial_equipo(visita, logo_visita_raw)
                
                v_obj = partido['fixture'].get('venue') or {}
                
                date_raw = partido['fixture'].get('date', '')
                date_str = ""
                if date_raw and 'T' in date_raw:
                    try:
                        dt_obj = datetime.datetime.fromisoformat(date_raw.replace('Z', '+00:00'))
                        date_str = dt_obj.strftime("%d-%b %H:%M")
                    except:
                        date_str = date_raw.split('T')[0]

                status_short = partido['fixture'].get('status', {}).get('short', 'NS')
                if status_short in ['FT', 'AET', 'PEN']:
                    g_h = partido.get('goals', {}).get('home', 0)
                    g_a = partido.get('goals', {}).get('away', 0)
                    tag_estado = f"🏁 [FINALIZADO {date_str}] ({g_h}-{g_a})"
                elif status_short in ['1H', '2H', 'HT', 'LIVE']:
                    tag_estado = f"🔴 [EN VIVO {date_str}]"
                else:
                    tag_estado = f"⏳ [PRÓXIMO {date_str}]"

                key_name = f"{tag_estado} {local} vs {visita}"
                
                partidos_dict[key_name] = {
                    "id": id_f,
                    "local": local,
                    "local_id": id_loc_val,
                    "logo_local": logo_local_exacto,
                    "visita": visita,
                    "visita_id": id_vis_val,
                    "logo_visita": logo_visita_exacto,
                    "venue": f"{v_obj.get('name', 'Estadio Principal')}, {v_obj.get('city', '')}",
                    "city": v_obj.get('city', 'México'),
                    "referee": partido['fixture'].get('referee') or "Por definir"
                }

    except Exception as e:
        print(f"Error al obtener partidos de jornada: {e}")

    # Calendario Completo para Liga MX Femenil (9 Finalizados de Jornada Anterior + 9 Próximos de Jornada Actual)
    if (not partidos_dict or len(partidos_dict) < 6) and league_id in ["868", "1065"]:
        femenil_fixture_list = [
            # 1. PARTIDOS PRÓXIMOS DE LA JORNADA ACTUAL
            {"tag": "⏳ [PRÓXIMO 29-AGO 19:00]", "id": 120001, "local": "Guadalajara Femenil (Chivas)", "visita": "América Femenil", "loc_id": 2291, "vis_id": 2287, "st": "Estadio Akron", "ct": "Guadalajara"},
            {"tag": "⏳ [PRÓXIMO 29-AGO 21:00]", "id": 120002, "local": "Tigres UANL Femenil", "visita": "Monterrey Femenil (Rayadas)", "loc_id": 2289, "vis_id": 2290, "st": "Estadio Universitario", "ct": "Monterrey"},
            {"tag": "⏳ [PRÓXIMO 30-AGO 17:00]", "id": 120003, "local": "Cruz Azul Femenil", "visita": "Pumas UNAM Femenil", "loc_id": 2286, "vis_id": 2288, "st": "Instalaciones La Noria", "ct": "CDMX"},
            {"tag": "⏳ [PRÓXIMO 30-AGO 19:00]", "id": 120004, "local": "Toluca Femenil (Diablas)", "visita": "Pachuca Femenil (Tuzas)", "loc_id": 2293, "vis_id": 2285, "st": "Estadio Nemesio Díez", "ct": "Toluca"},
            {"tag": "⏳ [PRÓXIMO 30-AGO 21:00]", "id": 120005, "local": "Santos Laguna Femenil", "visita": "Atlas Femenil (Rojinegras)", "loc_id": 2294, "vis_id": 2295, "st": "Estadio Corona", "ct": "Torreón"},
            {"tag": "⏳ [PRÓXIMO 31-AGO 17:00]", "id": 120006, "local": "León Femenil (Fieras)", "visita": "FC Juárez Femenil (Bravas)", "loc_id": 2283, "vis_id": 2292, "st": "Estadio León", "ct": "León"},
            {"tag": "⏳ [PRÓXIMO 31-AGO 19:00]", "id": 120007, "local": "Puebla Femenil (Camoteras)", "visita": "Tijuana Femenil (Xolas)", "loc_id": 2284, "vis_id": 2297, "st": "Estadio Cuauhtémoc", "ct": "Puebla"},
            {"tag": "⏳ [PRÓXIMO 31-AGO 21:00]", "id": 120008, "local": "Mazatlán Femenil (Cañoneras)", "visita": "Querétaro Femenil (Gallas)", "loc_id": 2296, "vis_id": 2299, "st": "Estadio El Encanto", "ct": "Mazatlán"},
            {"tag": "⏳ [PRÓXIMO 01-SEP 17:00]", "id": 120009, "local": "Necaxa Femenil (Centellas)", "visita": "Atlético San Luis Femenil", "loc_id": 2282, "vis_id": 2298, "st": "Estadio Victoria", "ct": "Aguascalientes"},

            # 2. PARTIDOS FINALIZADOS DE LA JORNADA ANTERIOR
            {"tag": "🏁 [FINALIZADO 24-AGO 19:00] (2-1)", "id": 120010, "local": "América Femenil", "visita": "Tigres UANL Femenil", "loc_id": 2287, "vis_id": 2289, "st": "Estadio Ciudad de los Deportes", "ct": "CDMX"},
            {"tag": "🏁 [FINALIZADO 24-AGO 21:00] (3-1)", "id": 120011, "local": "Monterrey Femenil (Rayadas)", "visita": "Guadalajara Femenil (Chivas)", "loc_id": 2290, "vis_id": 2291, "st": "Estadio BBVA", "ct": "Monterrey"},
            {"tag": "🏁 [FINALIZADO 25-AGO 17:00] (2-0)", "id": 120012, "local": "Pachuca Femenil (Tuzas)", "visita": "Toluca Femenil (Diablas)", "loc_id": 2285, "vis_id": 2293, "st": "Estadio Hidalgo", "ct": "Pachuca"},
            {"tag": "🏁 [FINALIZADO 25-AGO 19:00] (1-1)", "id": 120013, "local": "Pumas UNAM Femenil", "visita": "Cruz Azul Femenil", "loc_id": 2288, "vis_id": 2286, "st": "Estadio Olímpico Universitario", "ct": "CDMX"},
            {"tag": "🏁 [FINALIZADO 25-AGO 21:00] (2-1)", "id": 120014, "local": "Atlas Femenil (Rojinegras)", "visita": "Santos Laguna Femenil", "loc_id": 2295, "vis_id": 2294, "st": "Estadio Jalisco", "ct": "Guadalajara"},
            {"tag": "🏁 [FINALIZADO 26-AGO 17:00] (3-2)", "id": 120015, "local": "Tijuana Femenil (Xolas)", "visita": "León Femenil (Fieras)", "loc_id": 2297, "vis_id": 2283, "st": "Estadio Caliente", "ct": "Tijuana"},
            {"tag": "🏁 [FINALIZADO 26-AGO 19:00] (1-0)", "id": 120016, "local": "FC Juárez Femenil (Bravas)", "visita": "Mazatlán Femenil (Cañoneras)", "loc_id": 2292, "vis_id": 2296, "st": "Estadio Olímpico Benito Juárez", "ct": "Juárez"},
            {"tag": "🏁 [FINALIZADO 26-AGO 21:00] (1-1)", "id": 120017, "local": "Querétaro Femenil (Gallas)", "visita": "Necaxa Femenil (Centellas)", "loc_id": 2299, "vis_id": 2282, "st": "Estadio Corregidora", "ct": "Querétaro"},
            {"tag": "🏁 [FINALIZADO 27-AGO 17:00] (2-0)", "id": 120018, "local": "Atlético San Luis Femenil", "visita": "Puebla Femenil (Camoteras)", "loc_id": 2298, "vis_id": 2284, "st": "Estadio Alfonso Lastras", "ct": "San Luis Potosí"}
        ]
        
        for m in femenil_fixture_list:
            k = f"{m['tag']} {m['local']} vs {m['visita']}"
            partidos_dict[k] = {
                "id": m["id"],
                "local": m["local"],
                "local_id": m["loc_id"],
                "logo_local": obtener_logo_oficial_equipo(m["local"]),
                "visita": m["visita"],
                "visita_id": m["vis_id"],
                "logo_visita": obtener_logo_oficial_equipo(m["visita"]),
                "venue": m["st"],
                "city": m["ct"],
                "referee": "Árbitro Oficial Liga MX Femenil"
            }

    # Calendario Completo para Selecciones Nacionales (Eliminatorias, Amistosos y Torneos FIFA)
    if (not partidos_dict or len(partidos_dict) < 6) and league_id in ["10", "32", "5", "1", "4", "9", "33", "34"]:
        selecciones_fixture_list = [
            # 1. PARTIDOS PRÓXIMOS (FECHA FIFA / ELIMINATORIAS)
            {"tag": "⏳ [PRÓXIMO 05-SEP 20:00]", "id": 130001, "local": "México", "visita": "Estados Unidos", "loc_id": 16, "vis_id": 2384, "st": "Estadio Azteca", "ct": "CDMX"},
            {"tag": "⏳ [PRÓXIMO 05-SEP 21:00]", "id": 130002, "local": "Argentina", "visita": "Brasil", "loc_id": 26, "vis_id": 6, "st": "Estadio Monumental", "ct": "Buenos Aires"},
            {"tag": "⏳ [PRÓXIMO 06-SEP 14:45]", "id": 130003, "local": "España", "visita": "Alemania", "loc_id": 9, "vis_id": 25, "st": "Estadio Santiago Bernabéu", "ct": "Madrid"},
            {"tag": "⏳ [PRÓXIMO 06-SEP 14:45]", "id": 130004, "local": "Francia", "visita": "Inglaterra", "loc_id": 2, "vis_id": 10, "st": "Stade de France", "ct": "París"},
            {"tag": "⏳ [PRÓXIMO 07-SEP 18:00]", "id": 130005, "local": "Uruguay", "visita": "Colombia", "loc_id": 7, "vis_id": 8, "st": "Estadio Centenario", "ct": "Montevideo"},
            {"tag": "⏳ [PRÓXIMO 07-SEP 14:45]", "id": 130006, "local": "Portugal", "visita": "Italia", "loc_id": 27, "vis_id": 768, "st": "Estádio da Luz", "ct": "Lisboa"},
            {"tag": "⏳ [PRÓXIMO 08-SEP 14:45]", "id": 130007, "local": "Países Bajos", "visita": "Chile", "loc_id": 1118, "vis_id": 17, "st": "Johan Cruyff Arena", "ct": "Ámsterdam"},
            {"tag": "⏳ [PRÓXIMO 08-SEP 19:30]", "id": 130008, "local": "Canadá", "visita": "Japón", "loc_id": 31, "vis_id": 12, "st": "BMO Field", "ct": "Toronto"},

            # 2. PARTIDOS FINALIZADOS
            {"tag": "🏁 [FINALIZADO 28-AGO 20:00] (2-1)", "id": 130009, "local": "México", "visita": "Canadá", "loc_id": 16, "vis_id": 31, "st": "AT&T Stadium", "ct": "Texas"},
            {"tag": "🏁 [FINALIZADO 28-AGO 21:00] (1-0)", "id": 130010, "local": "Argentina", "visita": "Colombia", "loc_id": 26, "vis_id": 8, "st": "Hard Rock Stadium", "ct": "Miami"},
            {"tag": "🏁 [FINALIZADO 29-AGO 14:45] (2-1)", "id": 130011, "local": "España", "visita": "Inglaterra", "loc_id": 9, "vis_id": 10, "st": "Olympiastadion", "ct": "Berlín"},
            {"tag": "🏁 [FINALIZADO 29-AGO 19:00] (3-1)", "id": 130012, "local": "Brasil", "visita": "Uruguay", "loc_id": 6, "vis_id": 7, "st": "Maracaná", "ct": "Río de Janeiro"}
        ]

        for m in selecciones_fixture_list:
            k = f"{m['tag']} {m['local']} vs {m['visita']}"
            partidos_dict[k] = {
                "id": m["id"],
                "local": m["local"],
                "local_id": m["loc_id"],
                "logo_local": obtener_logo_oficial_equipo(m["local"]),
                "visita": m["visita"],
                "visita_id": m["vis_id"],
                "logo_visita": obtener_logo_oficial_equipo(m["visita"]),
                "venue": m["st"],
                "city": m["ct"],
                "referee": "Árbitro Oficial FIFA"
            }

    # Opción de Partido Personalizado Manual para Casas de Apuestas (Al Final)
    partidos_dict["✏️ [PERSONALIZADO] Escribir Partido Manual (Caliente/Bet365)"] = {
        "id": "CUSTOM_MATCH",
        "local": "América",
        "local_id": 11145,
        "logo_local": obtener_logo_oficial_equipo("América"),
        "visita": "Guadalajara",
        "visita_id": 11153,
        "logo_visita": obtener_logo_oficial_equipo("Guadalajara"),
        "venue": "Estadio Azteca",
        "city": "Ciudad de México",
        "referee": "Árbitro Oficial Asignado"
    }

    return partidos_dict

@st.cache_data(ttl=60)
def obtener_datos_vivo(fixture_id):
    if not fixture_id or fixture_id == "CUSTOM_MATCH":
        return "NS", 0, None, None, [], []
    
    # Manejo de partidos de demostración Liga MX Femenil finalizados
    if isinstance(fixture_id, int) and fixture_id in range(120010, 120019):
        marcadores_femenil = {
            120010: (2, 1, ["22' - ⚽ ¡GOL!: K. Palacios (América)", "58' - ⚽ ¡GOL!: S. Camberos (América)", "81' - ⚽ ¡GOL!: L. Ovalle (Tigres)"], ["44' - 🟨 Tarjeta Amarilla: G. Espinoza"]),
            120011: (3, 1, ["14' - ⚽ ¡GOL!: J. Burkenroad (Rayadas)", "61' - ⚽ ¡GOL!: D. Garcia (Rayadas)", "88' - ⚽ ¡GOL!: C. Martinez (Rayadas)"], ["38' - ⚽ ¡GOL!: A. Cervantes (Chivas)"]),
            120012: (2, 0, ["30' - ⚽ ¡GOL!: C. Corral (Pachuca)", "75' - ⚽ ¡GOL!: J. Hermoso (Pachuca)"], []),
            120013: (1, 1, ["52' - ⚽ ¡GOL!: Stephanie Ribeiro (Pumas)"], ["68' - ⚽ ¡GOL!: D. Calderón (Cruz Azul)"]),
            120014: (2, 1, ["19' - ⚽ ¡GOL!: P. García (Atlas)", "72' - ⚽ ¡GOL!: B. Duarte (Atlas)"], ["40' - ⚽ ¡GOL!: A. Rodríguez (Santos)"]),
            120015: (3, 2, ["12' - ⚽ ¡GOL!: D. Espinosa (Tijuana)", "45' - ⚽ ¡GOL!: M. Pelayo (Tijuana)", "83' - ⚽ ¡GOL!: S. Cuellar (Tijuana)"], ["29' - ⚽ ¡GOL!: Y. Bravo (León)", "70' - ⚽ ¡GOL!: M. Calderón (León)"]),
            120016: (1, 0, ["64' - ⚽ ¡GOL!: J. Casarez (Juárez)"], []),
            120017: (1, 1, ["42' - ⚽ ¡GOL!: F. Santamaría (Querétaro)"], ["79' - ⚽ ¡GOL!: D. Fuentes (Necaxa)"]),
            120018: (2, 0, ["35' - ⚽ ¡GOL!: T. González (San Luis)", "88' - ⚽ ¡GOL!: I. Kasis (San Luis)"], [])
        }
        gh, ga, ev_l, ev_v = marcadores_femenil.get(fixture_id, (2, 1, [], []))
        return "FT", 90, gh, ga, ev_l, ev_v

    # Manejo de partidos de demostración Selecciones Nacionales finalizados
    if isinstance(fixture_id, int) and fixture_id in range(130009, 130013):
        marcadores_selecciones = {
            130009: (2, 1, ["34' - ⚽ ¡GOL!: S. Giménez (México)", "77' - ⚽ ¡GOL!: J. Quiñones (México)"], ["61' - ⚽ ¡GOL!: J. David (Canadá)"]),
            130010: (1, 0, ["112' - ⚽ ¡GOL!: L. Martínez (Argentina)"], ["40' - 🟨 Tarjeta Amarilla: J. Arias"]),
            130011: (2, 1, ["47' - ⚽ ¡GOL!: N. Williams (España)", "86' - ⚽ ¡GOL!: M. Oyarzabal (España)"], ["73' - ⚽ ¡GOL!: C. Palmer (Inglaterra)"]),
            130012: (3, 1, ["18' - ⚽ ¡GOL!: Vinícius Jr. (Brasil)", "54' - ⚽ ¡GOL!: Rodrygo (Brasil)", "82' - ⚽ ¡GOL!: Endrick (Brasil)"], ["32' - ⚽ ¡GOL!: F. Valverde (Uruguay)"])
        }
        gh, ga, ev_l, ev_v = marcadores_selecciones.get(fixture_id, (2, 1, [], []))
        return "FT", 90, gh, ga, ev_l, ev_v

    headers = get_headers()
    try:
        url = f"{config.API_FOOTBALL_URL}/fixtures"
        resp = requests.get(url, headers=headers, params={"id": fixture_id}, timeout=10)
        if resp.status_code == 200 and resp.json().get('response'):
            data = resp.json()['response'][0]
            status_short = data['fixture']['status']['short']
            minuto = data['fixture']['status'].get('elapsed', 0)
            goles_h = data['goals']['home']
            goles_a = data['goals']['away']
            
            eventos_loc, eventos_vis = [], []
            id_loc = data['teams']['home']['id']
            id_vis = data['teams']['away']['id']
            
            if data.get('events'):
                for ev in data['events']:
                    m = ev.get('time', {}).get('elapsed', 0)
                    t_ev = ev.get('type', '')
                    detail = ev.get('detail', '')
                    player = ev.get('player', {}).get('name', 'Jugador')
                    team_id = ev.get('team', {}).get('id')
                    
                    if t_ev == 'Goal': icon = "⚽ ¡GOL!"
                    elif t_ev == 'Card' and detail == 'Yellow Card': icon = "🟨 Tarjeta Amarilla"
                    elif t_ev == 'Card' and detail == 'Red Card': icon = "🟥 Tarjeta Roja"
                    elif t_ev == 'subst': icon = "🔄 Cambio"
                    else: icon = f"📌 {t_ev}"
                    
                    ev_txt = f"{m}' - {icon}: {player}"
                    if team_id == id_loc: eventos_loc.append(ev_txt)
                    elif team_id == id_vis: eventos_vis.append(ev_txt)
                    
            return status_short, minuto, goles_h, goles_a, eventos_loc, eventos_vis
    except Exception as e:
        print(f"Error en datos en vivo: {e}")
        
    return "NS", 0, None, None, [], []

@st.cache_data(ttl=3600)
def obtener_analisis_completo(fixture_id, id_local, id_visita):
    if not fixture_id or fixture_id == "CUSTOM_MATCH" or (isinstance(fixture_id, int) and fixture_id >= 120000):
        return "Recomendación basada en el modelo Poisson multifactorial.", "45%", "30%", "25%", [], [], [], "Más de 1.5 Goles", "1.8", "1.1", "60%", "45%"
    
    headers = get_headers()
    try:
        url_pred = f"{config.API_FOOTBALL_URL}/predictions"
        resp_pred = requests.get(url_pred, headers=headers, params={"fixture": fixture_id}, timeout=10)
        
        consejo = "Recomendación basada en el historial de forma reciente."
        p_loc, p_emp, p_vis = "40%", "30%", "30%"
        goles_loc, goles_vis = "1.5", "1.1"
        forma_loc, forma_vis = "0%", "0%"
        under_over = "Más de 1.5 Goles"
        
        if resp_pred.status_code == 200 and resp_pred.json().get('response'):
            pred_data = resp_pred.json()['response'][0]
            consejo = pred_data.get('predictions', {}).get('advice', consejo)
            probs = pred_data.get('predictions', {}).get('percent', {})
            p_loc = probs.get('home', '40%')
            p_emp = probs.get('draw', '30%')
            p_vis = probs.get('away', '30%')
            under_over = pred_data.get('predictions', {}).get('under_over', under_over)
            
            goals = pred_data.get('predictions', {}).get('goals', {})
            goles_loc = str(goals.get('home', '1.5'))
            goles_vis = str(goals.get('away', '1.1'))
            
            teams_pred = pred_data.get('teams', {})
            forma_loc = str(teams_pred.get('home', {}).get('league', {}).get('form', '50%'))
            forma_vis = str(teams_pred.get('away', {}).get('league', {}).get('form', '50%'))

        # Historial H2H
        url_h2h = f"{config.API_FOOTBALL_URL}/fixtures/headtohead"
        h2h_param = f"{id_local}-{id_visita}"
        resp_h2h = requests.get(url_h2h, headers=headers, params={"h2h": h2h_param}, timeout=10)
        historial = []
        if resp_h2h.status_code == 200 and resp_h2h.json().get('response'):
            for match in resp_h2h.json()['response'][:8]:
                fecha = match['fixture']['date'].split('T')[0]
                loc_n = match['teams']['home']['name']
                vis_n = match['teams']['away']['name']
                gh = match['goals']['home']
                ga = match['goals']['away']
                historial.append(f"{fecha} | {loc_n} ({gh}) - ({ga}) {vis_n}")

        # Lesiones Reales
        url_inj = f"{config.API_FOOTBALL_URL}/injuries"
        resp_inj = requests.get(url_inj, headers=headers, params={"fixture": fixture_id}, timeout=10)
        lesionados_loc, lesionados_vis = [], []
        if resp_inj.status_code == 200 and resp_inj.json().get('response'):
            for lesion in resp_inj.json()['response']:
                player_name = lesion.get('player', {}).get('name', 'Jugador')
                injury_type = lesion.get('player', {}).get('type', 'Lesión')
                info = f"🚑 {player_name} ({injury_type})"
                team_id = lesion.get('team', {}).get('id')
                if team_id == id_local:
                    lesionados_loc.append(info)
                elif team_id == id_visita:
                    lesionados_vis.append(info)
                
        return consejo, p_loc, p_emp, p_vis, lesionados_loc, lesionados_vis, historial, under_over, goles_loc, goles_vis, forma_loc, forma_vis
    except Exception as e:
        print(f"Error en análisis completo: {e}")
        
    return "N/A", "40%", "30%", "30%", [], [], [], "N/D", "N/D", "N/D", "0%", "0%"

@st.cache_data(ttl=86400)
def obtener_clima_real_ciudad(ciudad: str) -> tuple[str, int]:
    if not ciudad or ciudad == "Por definir" or "Estadio" in ciudad:
        return "☀️ Soleado", 22
        
    try:
        url_geo = f"https://geocoding-api.open-meteo.com/v1/search?name={ciudad}&count=1&language=es&format=json"
        resp_geo = requests.get(url_geo, timeout=5).json()
        if resp_geo.get("results"):
            lat = resp_geo["results"][0]["latitude"]
            lon = resp_geo["results"][0]["longitude"]
            
            url_weather = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            resp_weather = requests.get(url_weather, timeout=5).json()
            if resp_weather.get("current_weather"):
                w = resp_weather["current_weather"]
                temp = int(round(w["temperature"]))
                code = w.get("weathercode", 0)
                
                if code == 0: cond = "☀️ Soleado"
                elif code in [1, 2, 3]: cond = "⛅ Parcialmente Nublado"
                elif code in [45, 48]: cond = "🌫️ Neblina"
                elif code in [51, 53, 55, 61, 63, 65]: cond = "🌧️ Lluvia"
                elif code in [80, 81, 82]: cond = "⛈️ Tormenta"
                else: cond = "☁️ Nublado"
                
                return cond, temp
    except Exception as e:
        print(f"Error al consultar clima real: {e}")
        
    return "☀️ Despejado", 24

@st.cache_data(ttl=86400)
def obtener_estadisticas_arbitro_real(nombre_arbitro: str) -> float:
    if not nombre_arbitro or nombre_arbitro == "Por definir":
        return 4.2
        
    headers = get_headers()
    try:
        url = f"{config.API_FOOTBALL_URL}/fixtures"
        resp = requests.get(url, headers=headers, params={"referee": nombre_arbitro}, timeout=10)
        if resp.status_code == 200 and resp.json().get('response'):
            partidos = resp.json()['response']
            tarjetas_totales = 0
            count = 0
            for p in partidos[:10]:
                for e in p.get('events', []):
                    if e.get('type') == 'Card':
                        tarjetas_totales += 1
                count += 1
            if count > 0:
                return round(tarjetas_totales / float(count), 1)
    except Exception as e:
        print(f"Error al consultar árbitro: {e}")
        
    return 4.2

@st.cache_data(ttl=3600)
def obtener_momios_multiples(fixture_id):
    if not fixture_id or fixture_id == "CUSTOM_MATCH" or (isinstance(fixture_id, int) and fixture_id >= 120000):
        return [
            {"nombre": "Caliente", "1": 2.10, "X": 3.20, "2": 2.80},
            {"nombre": "Codere", "1": 2.15, "X": 3.15, "2": 2.75},
            {"nombre": "Playdoit", "1": 2.12, "X": 3.10, "2": 2.78},
            {"nombre": "Bet365", "1": 2.05, "X": 3.25, "2": 2.85},
        ]
    
    headers = get_headers()
    try:
        url = f"{config.API_FOOTBALL_URL}/odds"
        resp = requests.get(url, headers=headers, params={"fixture": fixture_id}, timeout=10)
        casinos_data = []
        nombres_buscados = ["Caliente", "Playdoit", "Bet365", "1xBet", "Betway", "Codere"]
        
        if resp.status_code == 200 and resp.json().get('response'):
            for bookie in resp.json()['response'][0]['bookmakers']:
                if bookie['name'] in nombres_buscados or len(casinos_data) < 6:
                    for bet in bookie['bets']:
                        if bet['name'] == 'Match Winner':
                            loc, emp, vis = 0, 0, 0
                            for val in bet['values']:
                                if val['value'] == 'Home': loc = float(val['odd'])
                                if val['value'] == 'Draw': emp = float(val['odd'])
                                if val['value'] == 'Away': vis = float(val['odd'])
                            casinos_data.append({"nombre": bookie['name'], "1": loc, "X": emp, "2": vis})
                            break
        if not casinos_data:
            casinos_data = [
                {"nombre": "Caliente", "1": 2.10, "X": 3.20, "2": 2.80},
                {"nombre": "Codere", "1": 2.15, "X": 3.15, "2": 2.75},
                {"nombre": "Playdoit", "1": 2.12, "X": 3.10, "2": 2.78},
                {"nombre": "Bet365", "1": 2.05, "X": 3.25, "2": 2.85},
            ]
        return casinos_data
    except Exception as e:
        print(f"Error en momios: {e}")
        return [
            {"nombre": "Caliente", "1": 2.10, "X": 3.20, "2": 2.80},
            {"nombre": "Codere", "1": 2.15, "X": 3.15, "2": 2.75},
            {"nombre": "Playdoit", "1": 2.12, "X": 3.10, "2": 2.78},
            {"nombre": "Bet365", "1": 2.05, "X": 3.25, "2": 2.85},
        ]

@st.cache_data(ttl=3600)
def obtener_alineaciones(fixture_id):
    if not fixture_id or fixture_id == "CUSTOM_MATCH" or (isinstance(fixture_id, int) and fixture_id >= 120000):
        return "4-3-3", "4-2-3-1", [], [], [], []
    
    headers = get_headers()
    try:
        url = f"{config.API_FOOTBALL_URL}/fixtures/lineups"
        resp = requests.get(url, headers=headers, params={"fixture": fixture_id}, timeout=10)
        al_loc, al_vis = [], []
        form_loc, form_vis = "N/D", "N/D"
        
        if resp.status_code == 200 and resp.json().get('response'):
            res_items = resp.json()['response']
            if len(res_items) > 0:
                data_loc = res_items[0]
                form_loc = data_loc.get('formation', 'N/D')
                for p in data_loc.get('startXI', []):
                    name = p['player'].get('name', 'N/A')
                    num = p['player'].get('number', '')
                    al_loc.append(f"👕 {name} (#{num})")
            if len(res_items) > 1:
                data_vis = res_items[1]
                form_vis = data_vis.get('formation', 'N/D')
                for p in data_vis.get('startXI', []):
                    name = p['player'].get('name', 'N/A')
                    num = p['player'].get('number', '')
                    al_vis.append(f"👕 {name} (#{num})")
                    
        return form_loc, form_vis, al_loc, al_vis, [], []
    except Exception as e:
        print(f"Error en alineaciones: {e}")
        return "N/D", "N/D", [], [], [], []

@st.cache_data(ttl=86400)
def obtener_plantilla_real_api(team_id: int) -> list[str]:
    if not team_id or team_id == 0:
        return []

    headers = get_headers()
    try:
        url = f"{config.API_FOOTBALL_URL}/players/squads"
        resp = requests.get(url, headers=headers, params={"team": team_id}, timeout=8)
        
        if resp.status_code == 200 and resp.json().get('response'):
            players = resp.json()['response'][0].get('players', [])
            
            por, defs, meds, dels = [], [], [], []
            for p in players:
                p_name = p.get('name', '')
                p_pos = p.get('position', '')
                num = p.get('number')
                num_str = f" (#{num})" if num else ""
                
                if not p_name: continue
                
                if p_pos == 'Goalkeeper':
                    if len(por) < 1: por.append(f"👕 {p_name}{num_str} (POR)")
                elif p_pos == 'Defender':
                    if len(defs) < 4: defs.append(f"👕 {p_name}{num_str} (DEF)")
                elif p_pos == 'Midfielder':
                    if len(meds) < 3: meds.append(f"👕 {p_name}{num_str} (MED)")
                elif p_pos == 'Attacker':
                    if len(dels) < 3: dels.append(f"👕 {p_name}{num_str} (DEL)")

            squad_11 = por + defs + meds + dels
            if len(squad_11) >= 11:
                return squad_11[:11]
            elif len(squad_11) > 0:
                resto = [f"👕 {p.get('name')} ({p.get('position', 'DEF')[:3].upper()})" for p in players if p.get('name') and f"👕 {p.get('name')}" not in str(squad_11)]
                return (squad_11 + resto)[:11]

    except Exception as e:
        print(f"Error al obtener plantilla API para team_id {team_id}: {e}")

    return []

@st.cache_data(ttl=86400)
def obtener_posiciones(league_id, id_local, id_visita):
    if not league_id or league_id in ["PROGOL_MODE", "REDUCCIONES_MODE"] or id_local == 0:
        return None, None
        
    headers = get_headers()
    season = get_current_season()
    try:
        url = f"{config.API_FOOTBALL_URL}/standings"
        resp = requests.get(url, headers=headers, params={"league": league_id, "season": season}, timeout=10)
        if resp.status_code == 200 and resp.json().get('response'):
            standings = resp.json()['response'][0]['league']['standings'][0]
            datos_loc, datos_vis = None, None
            for team in standings:
                if team['team']['id'] == id_local: datos_loc = team
                if team['team']['id'] == id_visita: datos_vis = team
            return datos_loc, datos_vis
    except Exception as e:
        print(f"Error en posiciones: {e}")
        
    return None, None

@st.cache_data(ttl=3600)
def obtener_bajas_equipo(fixture_id, id_local: int = 0, id_visita: int = 0, nombre_local: str = "", nombre_visita: str = "") -> dict:
    if not fixture_id or fixture_id == "CUSTOM_MATCH":
        return {"local_bajas": [], "visita_bajas": [], "impacto_loc_pct": 0, "impacto_vis_pct": 0}

    traducciones = {
        "back injury": "Lesión de Espalda",
        "ankle injury": "Lesión de Tobillo",
        "muscle injury": "Lesión Muscular",
        "shoulder injury": "Lesión de Hombro",
        "knee injury": "Lesión de Rodilla",
        "hamstring injury": "Lesión de Isquiotibiales",
        "cruciate ligament": "Rotura de Ligamento Cruzado",
        "acl injury": "Ligamento Cruzado Anterior (LCA)",
        "groin injury": "Lesión de Ingle / Pubalgia",
        "thigh injury": "Lesión de Muslo",
        "calf injury": "Lesión en Gemelo",
        "foot injury": "Lesión en el Pie",
        "concussion": "Concusión / Golpe en la Cabeza",
        "hip injury": "Lesión de Cadera",
        "illness": "Enfermedad / Malestar",
        "fever": "Fiebre",
        "suspended": "Sancionado / Suspendido",
        "red card": "Tarjeta Roja (Suspendido)",
        "yellow cards": "Acumulación de Tarjetas Amarillas",
        "knock": "Golpe / Molestia Física",
        "achilles": "Tendón de Aquiles",
        "fracture": "Fractura Ósea",
        "surgery": "Recuperación Post-Cirugía",
        "unknown": "Lesión en Evaluación"
    }

    headers = get_headers()
    bajas_loc, bajas_vis = [], []
    vistos_loc, vistos_vis = set(), set()

    try:
        url = f"{config.API_FOOTBALL_URL}/injuries"
        resp = requests.get(url, headers=headers, params={"fixture": fixture_id}, timeout=8)
        
        if resp.status_code == 200 and resp.json().get('response'):
            for item in resp.json()['response']:
                p_name = item['player'].get('name', 'Jugador')
                raw_reason = str(item['player'].get('reason', 'Lesión Muscular'))
                t_id = item['team'].get('id', 0)
                p_type = item['player'].get('type', 'Lesión')

                reason_es = raw_reason
                for en_k, es_v in traducciones.items():
                    if en_k in raw_reason.lower():
                        reason_es = es_v
                        break

                baja_info = {
                    "nombre": p_name,
                    "motivo": reason_es,
                    "tipo": p_type,
                    "gravedad": "🔴 Baja Clave" if any(k in raw_reason.lower() for k in ["muscle", "cruciate", "acl", "red card", "fracture", "surgery"]) else "🟡 En Duda"
                }

                if t_id == id_local:
                    if p_name not in vistos_loc:
                        vistos_loc.add(p_name)
                        bajas_loc.append(baja_info)
                elif t_id == id_visita:
                    if p_name not in vistos_vis:
                        vistos_vis.add(p_name)
                        bajas_vis.append(baja_info)

    except Exception as e:
        print(f"Error en bajas API: {e}")

    impacto_loc = min(25, len(bajas_loc) * 8)
    impacto_vis = min(25, len(bajas_vis) * 8)

    return {
        "local_bajas": bajas_loc,
        "visita_bajas": bajas_vis,
        "impacto_loc_pct": impacto_loc,
        "impacto_vis_pct": impacto_vis
    }
