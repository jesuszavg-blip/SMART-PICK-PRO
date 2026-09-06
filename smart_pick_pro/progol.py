import random
import zlib
import streamlit as st

try:
    import pandas as pd
    HAS_PANDAS = True
except Exception:
    pd = None
    HAS_PANDAS = False

try:
    import analytics
except ImportError:
    analytics = None

# Base de datos calibrada de fuerza relativa de clubes y selecciones
TEAM_POWER_RATINGS = {
    # TIER 1: Gigantes Mundiales / Elite Europa
    "real madrid": 92, "manchester city": 92, "man city": 92, "bayern": 90, "bayern munich": 90, "bayern münchen": 90,
    "barcelona": 89, "psg": 88, "liverpool": 90, "arsenal": 89, "inter": 88, "inter milan": 88,
    
    # TIER 2: Top Europa & Gigantes Liga MX / Conmebol
    "atletico madrid": 85, "atlético madrid": 85, "chelsea": 85, "tottenham": 85, "aston villa": 84, "newcastle": 83,
    "juventus": 84, "milan": 84, "ac milan": 84, "napoli": 84, "dortmund": 85, "leverkusen": 86, "bayer leverkusen": 86,
    "america": 86, "américa": 86, "monterrey": 86, "rayados": 86, "tigres": 85, "tigres uanl": 85, "cruz azul": 85, "toluca": 84, "pachuca": 85,
    "flamengo": 84, "palmeiras": 84, "river": 83, "river plate": 83, "boca": 82, "boca jrs": 82, "boca juniors": 82,
    
    # TIER 3: Liga MX Medios-Altos / Europa Media
    "guadalajara": 81, "chivas": 81, "pumas": 81, "pumas unam": 81, "leon": 78, "león": 78, "santos": 77, "santos laguna": 77,
    "san luis": 77, "atletico san luis": 77, "atlético san luis": 77, "necaxa": 76, "atlas": 76, "tijuana": 75, "xolos": 75, "puebla": 74, "juarez": 74, "mazatlan": 74,
    "valencia": 81, "celta": 78, "celta de vigo": 78, "sevilla": 81, "betis": 82, "real sociedad": 82, "villarreal": 82, "athletic": 82,
    "brighton": 81, "brentford": 78, "west ham": 80, "fulham": 79, "crystal palace": 78, "wolves": 78, "ipswich": 73, "sunderland": 73,
    "bolonia": 79, "bologna": 79, "lazio": 83, "roma": 82, "fiorentina": 81, "atalanta": 84, "torino": 78,
    "estoril": 74, "rio ave": 74, "porto": 84, "benfica": 85, "sporting": 85, "braga": 80,
    "inter p. a.": 80, "internacional": 80, "at. mineiro": 82, "atletico mineiro": 82, "atlético mineiro": 82,
    "vitoria ba": 74, "bahia": 78, "racing": 80, "racing club": 80,
    "st. luis": 75, "st. louis": 75, "houston": 78, "houston dynamo": 78, "lafc": 80, "inter miami": 83,
    "u. de chile": 78, "universidad de chile": 78, "colo colo": 80, "colo-colo": 80,
    
    # LIGA MX FEMENIL
    "tigres f": 85, "america f": 85, "américa f": 85, "monterrey f": 85, "rayadas f": 85, "pachuca f": 84, "guadalajara f": 82, "chivas f": 82,
    "tijuana f": 77, "pumas f": 77, "toluca f": 76, "atlas f": 76, "juarez f": 76, "león f": 74
}

REDUCCIONES_PREDEFINIDAS = {
    "🔥 PRIMERA - 4 TRIPLES (4T)": {"triples": 4, "dobles": 0, "descripcion": "4 Triples + 10 Fijos"},
    "⚡ SEGUNDA - 7 DOBLES (7D)": {"triples": 0, "dobles": 7, "descripcion": "7 Dobles + 7 Fijos"},
    "🎯 TERCERA - 3 TRIPLES + 3 DOBLES (3T 3D)": {"triples": 3, "dobles": 3, "descripcion": "3 Triples + 3 Dobles + 8 Fijos"},
    "🚀 CUARTA - 2 TRIPLES + 6 DOBLES (2T 6D)": {"triples": 2, "dobles": 6, "descripcion": "2 Triples + 6 Dobles + 6 Fijos"},
    "💎 QUINTA - 8 TRIPLES (8T)": {"triples": 8, "dobles": 0, "descripcion": "8 Triples + 6 Fijos"},
    "👑 SEXTA - 11 DOBLES (11D)": {"triples": 0, "dobles": 11, "descripcion": "11 Dobles + 3 Fijos"},
}

CANTIDAD_BOLETAS_REDUCCION_OPTIMA = {
    "🔥 PRIMERA - 4 TRIPLES (4T)": 9,
    "⚡ SEGUNDA - 7 DOBLES (7D)": 16,
    "🎯 TERCERA - 3 TRIPLES + 3 DOBLES (3T 3D)": 24,
    "🚀 CUARTA - 2 TRIPLES + 6 DOBLES (2T 6D)": 18,
    "💎 QUINTA - 8 TRIPLES (8T)": 32,
    "👑 SEXTA - 11 DOBLES (11D)": 32,
}

def obtener_fuerza_equipo(nombre: str) -> float:
    """Calcula el índice de fuerza de un equipo normalizando su nombre."""
    if not nombre:
        return 76.0
    n_clean = str(nombre).lower().strip().replace(".", "").replace("  ", " ")
    
    # 1. Búsqueda exacta
    if n_clean in TEAM_POWER_RATINGS:
        return float(TEAM_POWER_RATINGS[n_clean])
        
    # 2. Búsqueda por subcadena
    for k, v in TEAM_POWER_RATINGS.items():
        if k in n_clean or n_clean in k:
            return float(v)
            
    # 3. Fallback determinista con CRC32
    seed = zlib.crc32(n_clean.encode('utf-8'))
    return 74.0 + (seed % 9)

def estimar_probabilidades_partido_progol(local: str, visita: str, fixture_id=None) -> dict:
    """
    Evalúa un partido de la jornada Progol utilizando el motor multifactorial
    (Poisson + Dixon-Coles) asegurando 100% de coherencia con el análisis profundo.
    """
    p_loc_rating = obtener_fuerza_equipo(local)
    p_vis_rating = obtener_fuerza_equipo(visita)
    
    # Ventaja de localía calibrada (+2.0 puntos de rating)
    ventaja_local = 2.0
    diff = (p_loc_rating + ventaja_local) - p_vis_rating
    
    lambda_h = max(0.55, min(3.2, 1.35 + (diff * 0.055)))
    lambda_a = max(0.55, min(3.2, 1.20 - (diff * 0.055)))
    
    p_l_est = max(0.12, min(0.80, 0.38 + (diff * 0.028)))
    p_v_est = max(0.12, min(0.80, 0.32 - (diff * 0.028)))
    p_e_est = max(0.15, min(0.38, 1.0 - (p_l_est + p_v_est)))
    
    if analytics and hasattr(analytics, "calcular_matriz_poisson_multifactorial"):
        try:
            sp = analytics.calcular_matriz_poisson_multifactorial(
                prob_loc_str=f"{p_l_est*100:.1f}%",
                prob_emp_str=f"{p_e_est*100:.1f}%",
                prob_vis_str=f"{p_v_est*100:.1f}%",
                goles_loc_est=f"{lambda_h:.2f}",
                goles_vis_est=f"{lambda_a:.2f}"
            )
            p_l = float(sp.get("p_home_win", p_l_est * 100))
            p_e = float(sp.get("p_draw", p_e_est * 100))
            p_v = float(sp.get("p_away_win", p_v_est * 100))
            p_1x = float(sp.get("p_1X", p_l + p_e))
            p_x2 = float(sp.get("p_X2", p_v + p_e))
        except Exception:
            p_l, p_e, p_v = round(p_l_est * 100, 1), round(p_e_est * 100, 1), round(p_v_est * 100, 1)
            p_1x, p_x2 = round(p_l + p_e, 1), round(p_v + p_e, 1)
    else:
        p_l, p_e, p_v = round(p_l_est * 100, 1), round(p_e_est * 100, 1), round(p_v_est * 100, 1)
        p_1x, p_x2 = round(p_l + p_e, 1), round(p_v + p_e, 1)

    p_12 = round(p_l + p_v, 1)

    # 1. Determinación de Pick Fijo Base
    if p_l >= p_v and p_l >= p_e:
        pick_fijo = "1"
        pick_fijo_txt = "Fijo Local (1)"
    elif p_v >= p_l and p_v >= p_e:
        pick_fijo = "2"
        pick_fijo_txt = "Fijo Visita (2)"
    else:
        # En caso de empate como opción más probable
        if p_v >= p_l:
            pick_fijo = "2"
            pick_fijo_txt = "Fijo Visita (2)"
        else:
            pick_fijo = "1"
            pick_fijo_txt = "Fijo Local (1)"

    # 2. Determinación de Pick Doble Base
    if p_x2 >= p_1x and p_x2 >= p_12:
        pick_doble = "X2"
        pick_doble_txt = "Doble Empate/Visita (X2)"
        doble_options = ['X', '2']
    elif p_1x >= p_x2 and p_1x >= p_12:
        pick_doble = "1X"
        pick_doble_txt = "Doble Local/Empate (1X)"
        doble_options = ['1', 'X']
    else:
        pick_doble = "12"
        pick_doble_txt = "Doble Local/Visita (12)"
        doble_options = ['1', '2']

    # 3. Índice de Incertidumbre (los partidos con probabilidades más parejas tienen mayor incertidumbre)
    # Partidos con 35% L, 33% E, 32% V tienen score alto -> Candidatos ideales a Triples / Dobles
    # Partidos con 70% L, 20% E, 10% V tienen score bajo -> Candidatos ideales a Fijos
    prob_max = max(p_l, p_e, p_v)
    diff_extremos = abs(p_l - p_v)
    incertidumbre = round(100.0 - prob_max - (diff_extremos * 0.4), 2)

    return {
        "local": local,
        "visita": visita,
        "p_home_win": p_l,
        "p_draw": p_e,
        "p_away_win": p_v,
        "p_1X": p_1x,
        "p_X2": p_x2,
        "p_12": p_12,
        "pick_fijo": pick_fijo,
        "pick_fijo_txt": pick_fijo_txt,
        "pick_doble": pick_doble,
        "pick_doble_txt": pick_doble_txt,
        "doble_options": doble_options,
        "incertidumbre": incertidumbre,
        "prob_max": prob_max,
        "resumen_probas": f"{p_l:.0f}% L | {p_e:.0f}% E | {p_v:.0f}% V"
    }

def generar_quiniela_progol(num_dobles: int, num_triples: int, jornada_oficial: list[dict] = None) -> list[dict]:
    """
    Genera una combinación inteligente y matemáticamente consistente de quiniela Progol
    de 14 casilleros evaluando las probabilidades reales de cada encuentro:
    - Asigna Triples a los partidos con mayor incertidumbre/paridad.
    - Asigna Dobles a los siguientes partidos más disputados con su doble de mayor EV (1X, X2 o 12).
    - Asigna Fijos a los partidos con mayor certeza estadística y ventaja probada.
    """
    if not jornada_oficial:
        from jornada_manager import cargar_jornada_activa
        jornada_oficial = cargar_jornada_activa()

    # 1. Analizar cada uno de los 14 encuentros con el motor de IA
    analisis_partidos = []
    for idx in range(1, 15):
        p_info = jornada_oficial[idx - 1] if len(jornada_oficial) >= idx else {"local": f"Local {idx}", "visita": f"Visita {idx}", "id": None}
        loc_name = p_info.get("local", f"Local {idx}")
        vis_name = p_info.get("visita", f"Visita {idx}")
        f_id = p_info.get("id")
        
        datos_eval = estimar_probabilidades_partido_progol(loc_name, vis_name, f_id)
        datos_eval["casilla"] = idx
        analisis_partidos.append(datos_eval)

    # 2. Ordenar casillas por nivel de incertidumbre descendente
    # Mayor incertidumbre -> Candidatos a Triples primero, luego Dobles, luego Fijos
    ranking_incertidumbre = sorted(analisis_partidos, key=lambda x: x["incertidumbre"], reverse=True)
    
    casillas_triples = set([item["casilla"] for item in ranking_incertidumbre[:num_triples]])
    casillas_dobles = set([item["casilla"] for item in ranking_incertidumbre[num_triples:num_triples + num_dobles]])

    boleta = []
    for p in analisis_partidos:
        c_idx = p["casilla"]
        if c_idx in casillas_triples:
            sugerencia = "Triple (1/X/2)"
            tipo = "triple"
            color_borde = "#D4AF37"
            pick_base = p["pick_fijo"]
        elif c_idx in casillas_dobles:
            sugerencia = p["pick_doble_txt"]
            tipo = "doble"
            color_borde = "#38BDF8"
            pick_base = p["pick_fijo"]
        else:
            sugerencia = p["pick_fijo_txt"]
            tipo = "fijo"
            color_borde = "#10B981" if p["prob_max"] >= 50.0 else "#F3E5AB"
            pick_base = p["pick_fijo"]

        boleta.append({
            "casilla": c_idx,
            "partido": f"{p['local']} vs {p['visita']}",
            "sugerencia": sugerencia,
            "tipo": tipo,
            "color_borde": color_borde,
            "pick_base": pick_base,
            "doble_tipo": p["pick_doble"],
            "analisis": p
        })

    return sorted(boleta, key=lambda x: x["casilla"])

def obtener_config_reduccion(nombre_estrat: str) -> dict:
    """Busca la configuración de reducción por clave exacta o coincidencia parcial."""
    if not nombre_estrat:
        return {"triples": 2, "dobles": 6, "descripcion": "2T 6D"}
    if nombre_estrat in REDUCCIONES_PREDEFINIDAS:
        return REDUCCIONES_PREDEFINIDAS[nombre_estrat]
    n_lower = str(nombre_estrat).lower()
    for k, v in REDUCCIONES_PREDEFINIDAS.items():
        if n_lower in k.lower() or k.lower() in n_lower:
            return v
        if "primera" in n_lower and "primera" in k.lower(): return v
        if "segunda" in n_lower and "segunda" in k.lower(): return v
        if "tercera" in n_lower and "tercera" in k.lower(): return v
        if "cuarta" in n_lower and "cuarta" in k.lower(): return v
        if "quinta" in n_lower and "quinta" in k.lower(): return v
        if "sexta" in n_lower and "sexta" in k.lower(): return v
    return {"triples": 2, "dobles": 6, "descripcion": "2T 6D"}

def obtener_reduccion_predefinida(nombre_estrat: str, jornada_oficial: list[dict] = None) -> list[dict]:
    """Genera la estructura de combinaciones para una estrategia de reducción predefinida con asignación inteligente por IA."""
    if not jornada_oficial:
        from jornada_manager import cargar_jornada_activa
        jornada_oficial = cargar_jornada_activa()

    config_estrat = obtener_config_reduccion(nombre_estrat)
    raw_triples = config_estrat.get("triples", 4)
    raw_dobles = config_estrat.get("dobles", 0)
    
    num_triples = raw_triples if isinstance(raw_triples, int) else len(raw_triples)
    num_dobles = raw_dobles if isinstance(raw_dobles, int) else len(raw_dobles)

    # Optimización inteligente: colocar Triples en máxima incertidumbre y Dobles en media
    boleta_optimizada = generar_quiniela_progol(num_dobles=num_dobles, num_triples=num_triples, jornada_oficial=jornada_oficial)

    casilleros = []
    for item in boleta_optimizada:
        casilleros.append({
            "casilla": item["casilla"],
            "partido": item["partido"],
            "tipo_txt": item["sugerencia"],
            "color_borde": item["color_borde"],
            "analisis": item["analisis"],
            "tipo": item["tipo"],
            "pick_base": item["pick_base"],
            "doble_tipo": item["doble_tipo"]
        })

    return casilleros

def generar_boletas_sencillas_reducidas(jornada_oficial: list[dict], nombre_estrat: str, n_boletas: int = None) -> list[dict]:
    """
    Genera N boletas sencillas reducidas (cada una con 14 pronósticos individuales '1', 'X', '2')
    matemáticamente optimizadas según la estrategia de reducción y las probabilidades reales.
    """
    if not jornada_oficial:
        from jornada_manager import cargar_jornada_activa
        jornada_oficial = cargar_jornada_activa()

    if n_boletas is None or n_boletas <= 0:
        n_boletas = CANTIDAD_BOLETAS_REDUCCION_OPTIMA.get(nombre_estrat, 16)

    config_estrat = obtener_config_reduccion(nombre_estrat)
    raw_triples = config_estrat.get("triples", 4)
    raw_dobles = config_estrat.get("dobles", 0)
    
    num_triples = raw_triples if isinstance(raw_triples, int) else len(raw_triples)
    num_dobles = raw_dobles if isinstance(raw_dobles, int) else len(raw_dobles)

    # Obtener la asignación óptima de casillas según la IA
    casillas_optimizadas = generar_quiniela_progol(num_dobles=num_dobles, num_triples=num_triples, jornada_oficial=jornada_oficial)

    boletas = []

    for b_idx in range(n_boletas):
        pronosticos_boleta = []
        
        for item in casillas_optimizadas:
            casilla = item["casilla"]
            p_partido = item["partido"]
            tipo = item["tipo"]
            stats = item["analisis"]
            
            if tipo == "triple":
                # Secuencia de triples priorizando el pick más probable de la IA
                sec_triples = [stats["pick_fijo"], "X" if stats["pick_fijo"] != "X" else "1", "2" if stats["pick_fijo"] == "1" else "1"]
                pick = sec_triples[(b_idx + casilla) % 3]
            elif tipo == "doble":
                # Doble real del partido (1X, X2 o 12)
                sec_dobles = stats["doble_options"]
                pick = sec_dobles[(b_idx + casilla) % 2]
            else:
                # Fijo 100% coherente con el análisis de IA
                pick = stats["pick_fijo"]

            pronosticos_boleta.append({
                "casilla": casilla,
                "partido": p_partido,
                "pick": pick
            })

        boletas.append({
            "numero_boleta": b_idx + 1,
            "pronosticos": pronosticos_boleta,
            "resumen_txt": " - ".join([f"C{p['casilla']}:{p['pick']}" for p in pronosticos_boleta]),
            "cadena_corta": "".join([p['pick'] for p in pronosticos_boleta])
        })

    return boletas

def verificar_aciertos_quiniela(boletas: list[dict], resultados_oficiales: list[str]) -> list[dict]:
    """
    Compara las boletas generadas contra los 14 resultados oficiales ('1', 'X', '2')
    y calcula el número de aciertos, ordenando de mayor a menor éxito.
    """
    if not resultados_oficiales or len(resultados_oficiales) < 14:
        return []

    evaluaciones = []
    for b in boletas:
        aciertos = 0
        detalle = []
        
        for idx, p in enumerate(b.get("pronosticos", [])):
            if idx < len(resultados_oficiales):
                real = resultados_oficiales[idx].upper().strip()
                pick = p.get("pick", "").upper().strip()
                es_acierto = (pick == real)
                if es_acierto:
                    aciertos += 1
                detalle.append({
                    "casilla": idx + 1,
                    "pick": pick,
                    "resultado": real,
                    "acierto": es_acierto
                })

        evaluaciones.append({
            "numero_boleta": b.get("numero_boleta", 1),
            "cadena_corta": b.get("cadena_corta", ""),
            "aciertos": aciertos,
            "detalle": detalle,
            "es_ganadora_1er": aciertos == 14,
            "es_ganadora_2do": aciertos == 13,
            "es_ganadora_3er": aciertos == 12,
            "es_premio": aciertos >= 10
        })

    return sorted(evaluaciones, key=lambda x: x["aciertos"], reverse=True)

def exportar_boletas_texto_plano(boletas: list[dict], jornada_oficial: list[dict] = None) -> str:
    """Genera un reporte en texto limpio con todas las boletas para copiar o imprimir."""
    lineas = [
        "🏆 SMART PICK PRO - REPORTE DE BOLETAS REDUCIDAS PROGOL 🏆",
        f"Total de boletas generadas: {len(boletas)}",
        "============================================================"
    ]
    
    for b in boletas:
        lineas.append(f"\n🎟️ BOLETA #{b['numero_boleta']} | Secuencia: {b['cadena_corta']}")
        for p in b.get("pronosticos", []):
            lineas.append(f"  Casilla {p['casilla']:02d}: {p['partido']} -> [{p['pick']}]")
            
    lineas.append("\n============================================================")
    lineas.append("¡Mucha suerte en tu quiniela!")
    return "\n".join(lineas)

def procesar_reducciones_excel(file_path_or_buffer):
    """Carga y procesa las hojas de un archivo Excel de reducciones de quinielas."""
    if not HAS_PANDAS or pd is None:
        return None, []
        
    try:
        xls = pd.ExcelFile(file_path_or_buffer)
        return xls, xls.sheet_names
    except Exception as e:
        print(f"Error al procesar Excel: {e}")
        return None, []
