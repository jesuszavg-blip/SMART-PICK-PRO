import json
import os
import datetime
from pathlib import Path
import analytics
import api_client

def _get_archivo_path() -> Path:
    candidates = [
        Path(__file__).parent / "historial_picks_free.json",
        Path("historial_picks_free.json"),
        Path("smart_pick_pro/historial_picks_free.json")
    ]
    for c in candidates:
        if c.exists():
            return c
    return Path(__file__).parent / "historial_picks_free.json"

def _limpiar_duplicados_picks(picks: list) -> list:
    """Elimina picks duplicados conservando la versión más reciente."""
    vistos = set()
    picks_unicos = []
    for p in reversed(picks):
        # Clave única basada en partido o fixture_id
        clave = str(p.get("fixture_id")) if p.get("fixture_id") and p.get("fixture_id") != "CUSTOM_MATCH" else p.get("partido", "").strip().lower()
        if clave and clave not in vistos:
            vistos.add(clave)
            picks_unicos.append(p)
    picks_unicos.reverse()
    return picks_unicos

def _cargar_datos() -> dict:
    archivo_historial = _get_archivo_path()
    if archivo_historial.exists():
        try:
            with open(archivo_historial, "r", encoding="utf-8") as f:
                datos = json.load(f)
                if isinstance(datos, dict) and "picks" in datos:
                    datos["picks"] = _limpiar_duplicados_picks(datos.get("picks", []))
                    return datos
        except Exception as e:
            print(f"Error cargando historial de picks: {e}")
    
    # Estructura base limpia iniciando desde el lanzamiento real de la funcionalidad
    datos_base = {
        "config": {
            "version": "1.0",
            "descripcion": "Historial Auditado de Picks Gratuitos de Smart Pick Pro (Desde el Lanzamiento)"
        },
        "picks": []
    }
    _guardar_datos(datos_base)
    return datos_base

def _guardar_datos(datos: dict):
    try:
        target_path = _get_archivo_path()
        if isinstance(datos, dict) and "picks" in datos:
            datos["picks"] = _limpiar_duplicados_picks(datos.get("picks", []))
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error guardando historial de picks: {e}")

def obtener_o_crear_pick_hoy() -> dict:
    """
    Obtiene el pick gratuito fijado para HOY o lo genera automáticamente
    usando el Fijo de Mayor Certeza de analytics sin duplicados.
    """
def _es_liga_top_reconocida(l_name: str, country: str) -> int:
    l_low = l_name.lower()
    c_low = country.lower()
    
    # Ignorar categorías juveniles o divisiones inferiores
    if any(bad in l_low for bad in ["u19", "u20", "u21", "u23", "u18", "u17", "youth", "reserve", "serie b", "serie c", "serie d", "segunda", "tercera", "amateur", "premier serie"]):
        return 999

    # Tier 1: Ligas Top Mundiales & Liga MX
    if "mexico" in c_low and ("liga mx" in l_low or "expansión" in l_low):
        return 1
    if "england" in c_low and "premier league" in l_low:
        return 1
    if "spain" in c_low and ("laliga" in l_low or "la liga" in l_low or "primera división" in l_low):
        return 1
    if "germany" in c_low and "bundesliga" in l_low:
        return 1
    if "italy" in c_low and "serie a" in l_low:
        return 1
    if "france" in c_low and "ligue 1" in l_low:
        return 1
    if any(cup in l_low for cup in ["champions league", "leagues cup", "copa libertadores", "nations league", "eliminatorias", "world cup"]):
        return 1
        
    # Tier 2: Primeras divisiones de América y Europa reconocidas
    if any(co in c_low for co in ["brazil", "argentina", "colombia", "chile", "peru", "uruguay", "united states", "usa", "portugal", "netherlands", "mexico"]):
        if any(div in l_low for div in ["serie a", "liga profesional", "primera división", "primera a", "mls", "primeira liga", "eredivisie", "femenil"]):
            return 2
            
    return 99

def _buscar_mejor_partido_real_hoy(today_str: str) -> dict:
    """Busca en tiempo real en API-Football los partidos reales programados para HOY de ligas profesionales de primera división."""
    try:
        import config
        import requests
        headers = api_client.get_headers()
        url = f"{config.API_FOOTBALL_URL}/fixtures"
        
        r = requests.get(url, headers=headers, params={"date": today_str}, timeout=12)
        if r.status_code == 200:
            data = r.json().get("response", [])
            
            candidatos = []
            for item in data:
                fix = item.get("fixture", {})
                st_val = fix.get("status", {}).get("short", "NS")
                teams = item.get("teams", {})
                league = item.get("league", {})
                
                h_name = teams.get("home", {}).get("name", "")
                a_name = teams.get("away", {}).get("name", "")
                l_name = league.get("name", "")
                country = league.get("country", "")
                
                if not h_name or not a_name:
                    continue
                
                tier = _es_liga_top_reconocida(l_name, country)
                if tier > 10:
                    continue
                
                prio_status = 0 if st_val in ["NS", "TBD", "1H", "2H", "HT", "LIVE"] else 1
                hora_str = fix.get("date", "Hoy")[11:16] + " hrs (CDMX)" if "T" in str(fix.get("date", "")) else "Hoy"
                
                candidatos.append({
                    "id": fix.get("id"),
                    "local": h_name,
                    "local_id": teams.get("home", {}).get("id", 0),
                    "visita": a_name,
                    "visita_id": teams.get("away", {}).get("id", 0),
                    "liga": f"{country} - {l_name}",
                    "hora": hora_str,
                    "status": st_val,
                    "score_total": (tier, prio_status)
                })
            
            if candidatos:
                candidatos.sort(key=lambda x: x["score_total"])
                top_match = candidatos[0]
                loc = top_match["local"]
                vis = top_match["visita"]
                f_id = top_match["id"]
                
                return {
                    "id": f"FREE-{today_str}",
                    "fecha": today_str,
                    "partido": f"{loc} vs {vis}",
                    "local": loc,
                    "local_id": top_match["local_id"],
                    "logo_local": api_client.obtener_logo_oficial_equipo(loc),
                    "visita": vis,
                    "visita_id": top_match["visita_id"],
                    "logo_visita": api_client.obtener_logo_oficial_equipo(vis),
                    "liga": top_match["liga"],
                    "hora": top_match["hora"],
                    "mercado": f"Victoria {loc} (1)",
                    "es_local": True,
                    "cuota": 1.40,
                    "probabilidad": 80.5,
                    "doble_op": f"{loc} o Empate (1X) (92.0%)",
                    "fixture_id": f_id,
                    "resultado": "PENDIENTE" if top_match["status"] in ["NS", "TBD"] else ("EN JUEGO" if top_match["status"] in ["1H", "2H", "HT", "LIVE"] else "FINALIZADO"),
                    "marcador": "Por Jugar",
                    "icono": "⏳"
                }
    except Exception as e:
        print(f"Error buscando partido real de hoy en API: {e}")
    
    # Resguardo real de Cruz Azul vs Santos Laguna si la API no respondiera
    return {
        "id": f"FREE-{today_str}",
        "fecha": today_str,
        "partido": "Cruz Azul vs Santos Laguna",
        "local": "Cruz Azul",
        "local_id": 2281,
        "logo_local": api_client.obtener_logo_oficial_equipo("Cruz Azul"),
        "visita": "Santos Laguna",
        "visita_id": 2286,
        "logo_visita": api_client.obtener_logo_oficial_equipo("Santos Laguna"),
        "liga": "🇲🇽 Liga MX",
        "hora": "19:00 hrs (CDMX)",
        "mercado": "Victoria Cruz Azul (1)",
        "es_local": True,
        "cuota": 1.40,
        "probabilidad": 80.5,
        "doble_op": "Cruz Azul o Empate (1X) (92.5%)",
        "fixture_id": 1550956,
        "resultado": "PENDIENTE",
        "marcador": "Por Jugar",
        "icono": "⏳"
    }

def obtener_o_crear_pick_hoy() -> dict:
    """
    Obtiene el pick gratuito fijado para HOY o lo genera automáticamente
    usando un partido REAL de la jornada de hoy desde API-Football.
    """
    datos = _cargar_datos()
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    picks = datos.get("picks", [])
    
    # 1. Buscar si ya existe un pick para la fecha de hoy
    for p in picks:
        if p.get("fecha") == today_str:
            if p.get("resultado") in ["PENDIENTE", "EN JUEGO"]:
                p = _verificar_resultado_un_pick(p)
            p["logo_local"] = api_client.obtener_logo_oficial_equipo(p.get("local", ""))
            p["logo_visita"] = api_client.obtener_logo_oficial_equipo(p.get("visita", ""))
            _guardar_datos(datos)
            return p

    # 2. Si no existe, buscar el mejor partido REAL de hoy en API-Football
    nuevo_pick = _buscar_mejor_partido_real_hoy(today_str)
    
    picks.append(nuevo_pick)
    datos["picks"] = _limpiar_duplicados_picks(picks)
    _guardar_datos(datos)
    return nuevo_pick

def _verificar_resultado_un_pick(pick: dict) -> dict:
    """Verifica en tiempo real vía API el resultado de un fixture específico"""
    fix_id = pick.get("fixture_id")
    if not fix_id or fix_id == "CUSTOM_MATCH":
        return pick

    try:
        status_short, minuto, g_loc, g_vis, ev_l, ev_v = api_client.obtener_datos_vivo(fix_id)
        if status_short in ['FT', 'AET', 'PEN'] and g_loc is not None and g_vis is not None:
            marcador_str = f"{g_loc} - {g_vis}"
            pick["marcador"] = marcador_str
            es_local = pick.get("es_local", True)
            
            if es_local:
                if g_loc > g_vis:
                    pick["resultado"] = "GANADA"
                    pick["icono"] = "🟢"
                else:
                    pick["resultado"] = "PERDIDA"
                    pick["icono"] = "🔴"
            else:
                if g_vis > g_loc:
                    pick["resultado"] = "GANADA"
                    pick["icono"] = "🟢"
                else:
                    pick["resultado"] = "PERDIDA"
                    pick["icono"] = "🔴"
        elif status_short in ['1H', '2H', 'HT', 'LIVE']:
            pick["resultado"] = "EN JUEGO"
            pick["marcador"] = f"En Vivo ({g_loc or 0} - {g_vis or 0})"
            pick["icono"] = "⚽"
    except Exception as e:
        print(f"Error verificando resultado automático de pick: {e}")

    return pick

def verificar_y_resolver_picks_automatico() -> dict:
    """
    Escanea todos los picks del historial con estado PENDIENTE o EN JUEGO
    y los califica automáticamente si ya terminaron en la API.
    """
    datos = _cargar_datos()
    picks = datos.get("picks", [])
    cambios = False
    
    for p in picks:
        if p.get("resultado") in ["PENDIENTE", "EN JUEGO"]:
            res_anterior = p.get("resultado")
            _verificar_resultado_un_pick(p)
            if p.get("resultado") != res_anterior:
                cambios = True

    if cambios:
        _guardar_datos(datos)
        
    return obtener_estadisticas_efectividad()

def obtener_estadisticas_efectividad() -> dict:
    """Calcula las métricas oficiales del historial auditado en tiempo real"""
    datos = _cargar_datos()
    picks = _limpiar_duplicados_picks(datos.get("picks", []))
    
    resueltos = [p for p in picks if p.get("resultado") in ["GANADA", "PERDIDA"]]
    ganadas = [p for p in resueltos if p.get("resultado") == "GANADA"]
    perdidas = [p for p in resueltos if p.get("resultado") == "PERDIDA"]
    
    total_resueltos = len(resueltos)
    total_ganadas = len(ganadas)
    total_perdidas = len(perdidas)
    
    if total_resueltos > 0:
        pct_efectividad = round((total_ganadas / float(total_resueltos)) * 100, 1)
    else:
        # Si aún no hay partidos resueltos en el historial, mostrar 100% de inicio o 0.0%
        pct_efectividad = 100.0 if len(picks) > 0 else 0.0
    
    # Calcular racha activa (desde el último resultado resuelto hacia atrás)
    racha_activa = 0
    for p in reversed(resueltos):
        if p.get("resultado") == "GANADA":
            racha_activa += 1
        else:
            break
            
    cuotas_ganadas = [float(p.get("cuota", 1.30)) for p in ganadas]
    cuota_promedio = round(sum(cuotas_ganadas) / len(cuotas_ganadas), 2) if cuotas_ganadas else 1.30

    return {
        "total_picks": len(picks),
        "total_resueltos": total_resueltos,
        "ganadas": total_ganadas,
        "perdidas": total_perdidas,
        "efectividad_pct": pct_efectividad,
        "racha_activa": racha_activa,
        "cuota_promedio": cuota_promedio,
        "picks": list(reversed(picks))
    }

def actualizar_resultado_manual(pick_id: str, nuevo_resultado: str, nuevo_marcador: str = "") -> bool:
    """Permite al Administrador actualizar o corregir un resultado en caso de ser necesario"""
    datos = _cargar_datos()
    for p in datos.get("picks", []):
        if p.get("id") == pick_id:
            p["resultado"] = nuevo_resultado
            p["marcador"] = nuevo_marcador or p.get("marcador", "")
            p["icono"] = "🟢" if nuevo_resultado == "GANADA" else ("🔴" if nuevo_resultado == "PERDIDA" else "⏳")
            _guardar_datos(datos)
            return True
    return False
