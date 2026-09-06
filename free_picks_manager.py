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
    datos = _cargar_datos()
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    picks = datos.get("picks", [])
    
    # 1. Buscar si ya existe un pick para la fecha de hoy o si el último pick registrado corresponde a este día
    for p in picks:
        if p.get("fecha") == today_str:
            if p.get("resultado") in ["PENDIENTE", "EN JUEGO"]:
                p = _verificar_resultado_un_pick(p)
                _guardar_datos(datos)
            return p

    # 2. Si no existe para today_str, buscar Banker #1 de Fijos de Oro
    fijos_data = analytics.generar_top_fijos_oro(top_n=1, filtro_tipo="super_favoritos", alcance_ligas="elite_top")
    picks_lista = fijos_data.get("fijos", [])
    
    if picks_lista:
        top_banker = picks_lista[0]
        partido_nombre = f"{top_banker.get('local')} vs {top_banker.get('visita')}"
        fixture_id = top_banker.get("id", 0)
        
        # Verificar si este mismo partido ya estaba registrado en los últimos picks
        for p in picks:
            if (p.get("fixture_id") and p.get("fixture_id") == fixture_id) or p.get("partido", "").strip().lower() == partido_nombre.strip().lower():
                if p.get("resultado") in ["PENDIENTE", "EN JUEGO"]:
                    p = _verificar_resultado_un_pick(p)
                    _guardar_datos(datos)
                return p

        nuevo_pick = {
            "id": f"FREE-{today_str}",
            "fecha": today_str,
            "partido": partido_nombre,
            "local": top_banker.get("local"),
            "local_id": top_banker.get("local_id", 0),
            "logo_local": top_banker.get("logo_local", ""),
            "visita": top_banker.get("visita"),
            "visita_id": top_banker.get("visita_id", 0),
            "logo_visita": top_banker.get("logo_visita", ""),
            "liga": top_banker.get("liga", "Ligas Élite"),
            "hora": top_banker.get("hora", "Hoy"),
            "mercado": top_banker.get("mercado", "Victoria Local (1)"),
            "es_local": top_banker.get("es_local_fijo", True),
            "cuota": top_banker.get("cuota_fijo", 1.30),
            "probabilidad": top_banker.get("probabilidad_fijo", 80.0),
            "doble_op": top_banker.get("doble_conservadora", ""),
            "fixture_id": fixture_id,
            "resultado": "PENDIENTE",
            "marcador": "Por Jugar",
            "icono": "⏳"
        }
    else:
        partido_nombre = "Bayern Múnich vs Bochum"
        fixture_id = 1301033
        
        # Verificar si ya existe en picks
        for p in picks:
            if (p.get("fixture_id") and p.get("fixture_id") == fixture_id) or p.get("partido", "").strip().lower() == partido_nombre.strip().lower():
                if p.get("resultado") in ["PENDIENTE", "EN JUEGO"]:
                    p = _verificar_resultado_un_pick(p)
                    _guardar_datos(datos)
                return p

        nuevo_pick = {
            "id": f"FREE-{today_str}",
            "fecha": today_str,
            "partido": partido_nombre,
            "local": "Bayern Múnich",
            "local_id": 157,
            "logo_local": api_client.obtener_logo_oficial_equipo("Bayern Múnich"),
            "visita": "Bochum",
            "visita_id": 176,
            "logo_visita": api_client.obtener_logo_oficial_equipo("Bochum"),
            "liga": "🇩🇪 Bundesliga",
            "hora": "13:30 hrs (CDMX)",
            "mercado": "Victoria Bayern Múnich (1)",
            "es_local": True,
            "cuota": 1.29,
            "probabilidad": 81.2,
            "doble_op": "Bayern Múnich o Empate (1X) (95.0%)",
            "fixture_id": fixture_id,
            "resultado": "PENDIENTE",
            "marcador": "Por Jugar",
            "icono": "⏳"
        }

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
