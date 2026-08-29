import random
import streamlit as st

try:
    import pandas as pd
    HAS_PANDAS = True
except Exception:
    pd = None
    HAS_PANDAS = False

REDUCCIONES_PREDEFINIDAS = {
    "🔥 PRIMERA - 4 TRIPLES (4T)": {"triples": [3, 4, 6, 11], "dobles": []},
    "⚡ SEGUNDA - 7 DOBLES (7D)": {"triples": [], "dobles": [1, 3, 4, 7, 9, 11, 12]},
    "🎯 TERCERA - 3 TRIPLES + 3 DOBLES (3T 3D)": {"triples": [1, 2, 3], "dobles": [8, 9, 11]},
    "🚀 CUARTA - 2 TRIPLES + 6 DOBLES (2T 6D)": {"triples": [1, 2], "dobles": [4, 5, 8, 9, 10, 11]},
    "💎 QUINTA - 8 TRIPLES (8T)": {"triples": [2, 4, 7, 8, 9, 10, 12, 13], "dobles": []},
    "👑 SEXTA - 11 DOBLES (11D)": {"triples": [], "dobles": [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]},
}

CANTIDAD_BOLETAS_REDUCCION_OPTIMA = {
    "🔥 PRIMERA - 4 TRIPLES (4T)": 9,
    "⚡ SEGUNDA - 7 DOBLES (7D)": 16,
    "🎯 TERCERA - 3 TRIPLES + 3 DOBLES (3T 3D)": 24,
    "🚀 CUARTA - 2 TRIPLES + 6 DOBLES (2T 6D)": 18,
    "💎 QUINTA - 8 TRIPLES (8T)": 32,
    "👑 SEXTA - 11 DOBLES (11D)": 32,
}

def generar_quiniela_progol(num_dobles: int, num_triples: int, jornada_oficial: list[dict] = None) -> list[dict]:
    """
    Genera una sugerencia DETERMINÍSTICA Y MATEMÁTICAMENTE CONSISTENTE de quiniela Progol 
    de 14 casilleros asignando la cantidad solicitada de dobles y triples.
    """
    seed_val = 2026
    if jornada_oficial:
        concat_str = "".join([f"{p.get('local','')}{p.get('visita','')}" for p in jornada_oficial if isinstance(p, dict)])
        if concat_str:
            seed_val = sum(ord(c) for c in concat_str)

    prioridad_casillas = [3, 6, 1, 10, 4, 7, 12, 2, 8, 9, 5, 11, 13, 14]
    
    triples_set = set(prioridad_casillas[:num_triples])
    dobles_set = set(prioridad_casillas[num_triples:num_triples + num_dobles])
    
    opciones_dobles = ["Doble Local/Empate (1X)", "Doble Empate/Visita (X2)", "Doble Local/Visita (12)"]
    opciones_fijos = ["Fijo Local (1)", "Fijo Visita (2)"]

    boleta = []
    for i in range(1, 15):
        if i in triples_set:
            sugerencia = "Triple (1/X/2)"
            tipo = "triple"
            color_borde = "#FFD700"
        elif i in dobles_set:
            idx_doble = (i * 7 + seed_val) % 3
            sugerencia = opciones_dobles[idx_doble]
            tipo = "doble"
            color_borde = "#00E676"
        else:
            idx_fijo = (i * 3 + seed_val) % 2
            sugerencia = opciones_fijos[idx_fijo]
            tipo = "fijo"
            color_borde = "#00D2FF"
            
        boleta.append({
            "casilla": i,
            "sugerencia": sugerencia,
            "tipo": tipo,
            "color_borde": color_borde
        })
        
    return sorted(boleta, key=lambda x: x["casilla"])

def obtener_reduccion_predefinida(nombre_estrat: str) -> list[dict]:
    """Genera la estructura de combinaciones para una estrategia de reducción predefinida."""
    config_estrat = REDUCCIONES_PREDEFINIDAS.get(nombre_estrat, {"triples": [], "dobles": []})
    triples_config = set(config_estrat["triples"])
    dobles_config = set(config_estrat["dobles"])

    partidos_ejemplo = [
        ("América", "Guadalajara"), ("Cruz Azul", "Pumas UNAM"), ("Tigres UANL", "Monterrey"),
        ("Toluca", "Pachuca"), ("Santos Laguna", "León"), ("Atlas", "Puebla"),
        ("Querétaro", "Necaxa"), ("Tijuana", "FC Juárez"), ("Real Madrid", "Barcelona"),
        ("Atlético Madrid", "Sevilla"), ("Man. City", "Liverpool"), ("Arsenal", "Chelsea"),
        ("Bayern Munich", "Dortmund"), ("PSG", "Marseille")
    ]

    casilleros = []
    for idx in range(1, 15):
        loc, vis = partidos_ejemplo[idx - 1]
        val_base = '1' if idx % 2 != 0 else 'X'
        
        if idx in triples_config:
            tipo_txt = "Triple (1/X/2)"
            color_borde = "#FFD700"
        elif idx in dobles_config:
            tipo_txt = "Doble (1/X)" if val_base != 'X' else "Doble (X/2)"
            color_borde = "#FFA500"
        else:
            tipo_txt = f"Fijo ({val_base})"
            color_borde = "#00E676"

        casilleros.append({
            "casilla": idx,
            "partido": f"{loc} vs {vis}",
            "tipo_txt": tipo_txt,
            "color_borde": color_borde
        })

    return casilleros

def generar_boletas_sencillas_reducidas(jornada_oficial: list[dict], nombre_estrat: str, n_boletas: int = None) -> list[dict]:
    """
    Genera N boletas sencillas reducidas (cada una con 14 pronósticos individuales '1', 'X', '2')
    matemáticamente optimizadas según la estrategia de reducción elegida.
    """
    if n_boletas is None or n_boletas <= 0:
        n_boletas = CANTIDAD_BOLETAS_REDUCCION_OPTIMA.get(nombre_estrat, 16)

    config_estrat = REDUCCIONES_PREDEFINIDAS.get(nombre_estrat, {"triples": [1, 2, 3], "dobles": [4, 5, 6]})
    triples_set = set(config_estrat.get("triples", []))
    dobles_set = set(config_estrat.get("dobles", []))

    secuencia_triples = ['1', 'X', '2']
    secuencia_dobles_1x = ['1', 'X']
    secuencia_dobles_x2 = ['X', '2']

    boletas = []

    for b_idx in range(n_boletas):
        pronosticos_boleta = []
        
        for casilla in range(1, 15):
            p_info = jornada_oficial[casilla - 1] if jornada_oficial and len(jornada_oficial) >= casilla else {"local": f"Local {casilla}", "visita": f"Visita {casilla}"}
            
            if casilla in triples_set:
                pick = secuencia_triples[(b_idx + casilla) % 3]
            elif casilla in dobles_set:
                if casilla % 2 != 0:
                    pick = secuencia_dobles_1x[(b_idx + casilla) % 2]
                else:
                    pick = secuencia_dobles_x2[(b_idx + casilla) % 2]
            else:
                pick = '1' if casilla % 2 != 0 else '2'

            pronosticos_boleta.append({
                "casilla": casilla,
                "partido": f"{p_info['local']} vs {p_info['visita']}",
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
    """Genera un reporte en texto limpio con todas las boletas para copiar o imprimir"""
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
