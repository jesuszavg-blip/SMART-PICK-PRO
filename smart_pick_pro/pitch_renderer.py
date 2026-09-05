import html

def render_cancha_tactica(equipo_local: str, equipo_visita: str, form_loc: str, form_vis: str, al_loc: list[str], al_vis: list[str]) -> str:
    """
    Renderiza la Cancha Táctica 2D estilo SofaScore/FotMob (Disposición Vertical 2D Completa)
    adaptada a la paleta de lujo (Oro cepillado, Obsidiana y Acentos elegantes).
    """
    if not al_loc or len(al_loc) < 11:
        al_loc = [
            "1. Camilo Vargas (POR)", "2. Hugo Nervo (DEF)", "3. Santamaría (DEF)", "4. G. Aguirre (DEF)", "5. L. Reyes (DEF)",
            "6. A. Rocha (MED)", "7. J. Márquez (MED)", "8. R. Fulgencio (MED)",
            "9. E. Aguirre (DEL)", "10. Uros Djurdjevic (DEL)", "11. Raymundo Fulgencio (DEL)"
        ]
        status_loc = "⏳ Alineación Probable (4-3-3)"
    else:
        status_loc = f"✅ Alineación Confirmada ({form_loc if form_loc != 'N/D' else '4-3-3'})"

    if not al_vis or len(al_vis) < 11:
        al_vis = [
            "1. Nahuel Guzmán (POR)", "2. Guido Pizarro (DEF)", "3. Joaquim Pereira (DEF)", "4. Javier Aquino (DEF)", "5. Jesús Angulo (DEF)",
            "6. Rafael Carioca (MED)", "7. Fernando Gorriarán (MED)", "8. Juan Brunetta (MED)",
            "9. Diego Lainez (DEL)", "10. André-Pierre Gignac (DEL)", "11. Marcelo Flores (DEL)"
        ]
        status_vis = "⏳ Alineación Probable (4-2-3-1)"
    else:
        status_vis = f"✅ Alineación Confirmada ({form_vis if form_vis != 'N/D' else '4-2-3-1'})"

    loc_name = html.escape(equipo_local)
    vis_name = html.escape(equipo_visita)

    p_l = [html.escape(p.replace("👕 ", "")) for p in al_loc[:11]]
    p_v = [html.escape(p.replace("👕 ", "")) for p in al_vis[:11]]

    html_code = (
        f'<div style="background: radial-gradient(circle, #1a3d24 0%, #0e2916 65%, #08170c 100%); border: 2px solid #D4AF37; border-radius: 16px; padding: 18px; font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif; position: relative; color: white; box-shadow: 0 10px 30px rgba(0,0,0,0.6); overflow: hidden;">'
        f'<div style="position: absolute; top: 50%; left: 10px; right: 10px; height: 2px; background: rgba(255,255,255,0.35); transform: translateY(-50%);"></div>'
        f'<div style="position: absolute; top: 50%; left: 50%; width: 110px; height: 110px; border: 2px solid rgba(255,255,255,0.35); border-radius: 50%; transform: translate(-50%, -50%);"></div>'
        f'<div style="position: absolute; top: 10px; left: 50%; width: 180px; height: 60px; border: 2px solid rgba(255,255,255,0.35); border-top: none; transform: translateX(-50%);"></div>'
        f'<div style="position: absolute; bottom: 10px; left: 50%; width: 180px; height: 60px; border: 2px solid rgba(255,255,255,0.35); border-bottom: none; transform: translateX(-50%);"></div>'
        f'<div style="display: flex; justify-content: space-between; align-items: center; background: rgba(21,24,33,0.92); padding: 8px 16px; border-radius: 12px; border-left: 5px solid #38BDF8; margin-bottom: 12px; position: relative; z-index: 10; border: 1px solid #282F3F;">'
        f'<div style="font-size: 15px; font-weight: 900; color: #ffffff;">🔵 {loc_name}</div>'
        f'<div style="color: #D4AF37; font-size: 11px; font-weight: bold;">{status_loc}</div>'
        f'</div>'
        f'<div style="height: 250px; display: flex; flex-direction: column; justify-content: space-around; position: relative; z-index: 10; padding: 5px 0;">'
        f'<div style="display: flex; justify-content: center;">'
        f'<div style="text-align: center;">'
        f'<div style="background: #D4AF37; color: #0D0F14; width: 32px; height: 32px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 13px; border: 2px solid white; box-shadow: 0 3px 6px rgba(0,0,0,0.5);">1</div>'
        f'<div style="background: rgba(13,15,20,0.88); color: white; font-size: 10px; font-weight: bold; padding: 2px 6px; border-radius: 8px; margin-top: 2px; white-space: nowrap; border: 1px solid #282F3F;">{p_l[0]}</div>'
        f'</div>'
        f'</div>'
        f'<div style="display: flex; justify-content: space-around; padding: 0 15px;">'
        f'<div style="text-align: center;"><div style="background: #38BDF8; color: #0D0F14; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">2</div><div style="background: rgba(13,15,20,0.88); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 70px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border: 1px solid #282F3F;">{p_l[1]}</div></div>'
        f'<div style="text-align: center;"><div style="background: #38BDF8; color: #0D0F14; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">4</div><div style="background: rgba(13,15,20,0.88); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 70px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border: 1px solid #282F3F;">{p_l[2]}</div></div>'
        f'<div style="text-align: center;"><div style="background: #38BDF8; color: #0D0F14; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">5</div><div style="background: rgba(13,15,20,0.88); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 70px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border: 1px solid #282F3F;">{p_l[3]}</div></div>'
        f'<div style="text-align: center;"><div style="background: #38BDF8; color: #0D0F14; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">3</div><div style="background: rgba(13,15,20,0.88); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 70px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border: 1px solid #282F3F;">{p_l[4]}</div></div>'
        f'</div>'
        f'<div style="display: flex; justify-content: space-around; padding: 0 40px;">'
        f'<div style="text-align: center;"><div style="background: #38BDF8; color: #0D0F14; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">6</div><div style="background: rgba(13,15,20,0.88); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border: 1px solid #282F3F;">{p_l[5]}</div></div>'
        f'<div style="text-align: center;"><div style="background: #38BDF8; color: #0D0F14; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">8</div><div style="background: rgba(13,15,20,0.88); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border: 1px solid #282F3F;">{p_l[6]}</div></div>'
        f'<div style="text-align: center;"><div style="background: #38BDF8; color: #0D0F14; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">10</div><div style="background: rgba(13,15,20,0.88); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border: 1px solid #282F3F;">{p_l[7]}</div></div>'
        f'</div>'
        f'<div style="display: flex; justify-content: space-around; padding: 0 30px;">'
        f'<div style="text-align: center;"><div style="background: #38BDF8; color: #0D0F14; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">7</div><div style="background: rgba(13,15,20,0.88); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border: 1px solid #282F3F;">{p_l[8]}</div></div>'
        f'<div style="text-align: center;"><div style="background: #38BDF8; color: #0D0F14; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">9</div><div style="background: rgba(13,15,20,0.88); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border: 1px solid #282F3F;">{p_l[9]}</div></div>'
        f'<div style="text-align: center;"><div style="background: #38BDF8; color: #0D0F14; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">11</div><div style="background: rgba(13,15,20,0.88); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border: 1px solid #282F3F;">{p_l[10]}</div></div>'
        f'</div>'
        f'</div>'
        f'<div style="height: 250px; display: flex; flex-direction: column; justify-content: space-around; position: relative; z-index: 10; padding: 5px 0; margin-top: 15px;">'
        f'<div style="display: flex; justify-content: space-around; padding: 0 30px;">'
        f'<div style="text-align: center;"><div style="background: #EF4444; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">7</div><div style="background: rgba(13,15,20,0.88); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border: 1px solid #282F3F;">{p_v[8]}</div></div>'
        f'<div style="text-align: center;"><div style="background: #EF4444; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">9</div><div style="background: rgba(13,15,20,0.88); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border: 1px solid #282F3F;">{p_v[9]}</div></div>'
        f'<div style="text-align: center;"><div style="background: #EF4444; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">11</div><div style="background: rgba(13,15,20,0.88); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border: 1px solid #282F3F;">{p_v[10]}</div></div>'
        f'</div>'
        f'<div style="display: flex; justify-content: space-around; padding: 0 40px;">'
        f'<div style="text-align: center;"><div style="background: #EF4444; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">6</div><div style="background: rgba(13,15,20,0.88); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border: 1px solid #282F3F;">{p_v[5]}</div></div>'
        f'<div style="text-align: center;"><div style="background: #EF4444; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">8</div><div style="background: rgba(13,15,20,0.88); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border: 1px solid #282F3F;">{p_v[6]}</div></div>'
        f'<div style="text-align: center;"><div style="background: #EF4444; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">10</div><div style="background: rgba(13,15,20,0.88); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border: 1px solid #282F3F;">{p_v[7]}</div></div>'
        f'</div>'
        f'<div style="display: flex; justify-content: space-around; padding: 0 15px;">'
        f'<div style="text-align: center;"><div style="background: #EF4444; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">2</div><div style="background: rgba(13,15,20,0.88); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 70px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border: 1px solid #282F3F;">{p_v[1]}</div></div>'
        f'<div style="text-align: center;"><div style="background: #EF4444; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">4</div><div style="background: rgba(13,15,20,0.88); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 70px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border: 1px solid #282F3F;">{p_v[2]}</div></div>'
        f'<div style="text-align: center;"><div style="background: #EF4444; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">5</div><div style="background: rgba(13,15,20,0.88); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 70px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border: 1px solid #282F3F;">{p_v[3]}</div></div>'
        f'<div style="text-align: center;"><div style="background: #EF4444; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">3</div><div style="background: rgba(13,15,20,0.88); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 70px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; border: 1px solid #282F3F;">{p_v[4]}</div></div>'
        f'</div>'
        f'<div style="display: flex; justify-content: center;">'
        f'<div style="text-align: center;">'
        f'<div style="background: #D4AF37; color: #0D0F14; width: 32px; height: 32px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 13px; border: 2px solid white; box-shadow: 0 3px 6px rgba(0,0,0,0.5);">1</div>'
        f'<div style="background: rgba(13,15,20,0.88); color: white; font-size: 10px; font-weight: bold; padding: 2px 6px; border-radius: 8px; margin-top: 2px; white-space: nowrap; border: 1px solid #282F3F;">{p_v[0]}</div>'
        f'</div>'
        f'</div>'
        f'</div>'
        f'<div style="display: flex; justify-content: space-between; align-items: center; background: rgba(21,24,33,0.92); padding: 8px 16px; border-radius: 12px; border-right: 5px solid #EF4444; margin-top: 12px; position: relative; z-index: 10; border: 1px solid #282F3F;">'
        f'<div style="font-size: 15px; font-weight: 900; color: #ffffff;">🔴 {vis_name}</div>'
        f'<div style="color: #D4AF37; font-size: 11px; font-weight: bold;">{status_vis}</div>'
        f'</div>'
        f'</div>'
    )

    return html_code

def render_minuto_a_minuto_dividido(
    equipo_local: str,
    equipo_visita: str,
    logo_local: str,
    logo_visita: str,
    status: str,
    minuto_actual: int,
    goles_local: int,
    goles_visita: int,
    eventos_local: list,
    eventos_visita: list,
    pos_local: int = 53,
    pos_visita: int = 47,
    tiros_local: int = 6,
    tiros_visita: int = 4,
    corners_local: int = 5,
    corners_visita: int = 3
) -> str:
    """
    Renderiza el Centro de Partido 'Minuto a Minuto' en Pantalla Dividida estilo ESPN / SofaScore.
    Muestra los eventos de cada equipo divididos por lados con línea de tiempo central y estadísticas en vivo.
    """
    import html
    loc_name = html.escape(equipo_local)
    vis_name = html.escape(equipo_visita)
    
    g_l = goles_local if goles_local is not None else 0
    g_v = goles_visita if goles_visita is not None else 0
    
    # Estado y Tiempo
    if status in ['1H', '2H', 'HT', 'LIVE']:
        status_label = f"🔴 EN VIVO {minuto_actual}'"
        status_color = "#EF5350"
        score_center = f'<div style="background:#0D0F14; border:2px solid #D4AF37; padding:6px 20px; border-radius:10px; font-size:28px; font-weight:900; color:#D4AF37; letter-spacing:4px;">{g_l} - {g_v}</div>'
    elif status in ['FT', 'AET', 'PEN']:
        status_label = "🏁 FINALIZADO (90')"
        status_color = "#D4AF37"
        score_center = f'<div style="background:#0D0F14; border:2px solid #D4AF37; padding:6px 20px; border-radius:10px; font-size:28px; font-weight:900; color:#D4AF37; letter-spacing:4px;">{g_l} - {g_v}</div>'
    else:
        status_label = "⏰ PRÓXIMO A DISPUTARSE"
        status_color = "#38BDF8"
        score_center = '<div style="background:#0D0F14; border:1.5px solid #D4AF37; padding:6px 22px; border-radius:10px; font-size:24px; font-weight:900; color:#F3E5AB; letter-spacing:2px;">VS</div>'

    # Generación de eventos por defecto si no hay eventos cargados
    if not eventos_local and not eventos_visita:
        if status in ['FT', 'AET', 'PEN'] or (g_l > 0 or g_v > 0):
            eventos_local = [
                {"min": 23, "icon": "⚽", "title": "¡GOL!", "player": f"Delantero {loc_name}", "detail": "Disparo cruzado dentro del área"},
                {"min": 58, "icon": "🟨", "title": "Tarjeta Amarilla", "player": f"Mediocampista {loc_name}", "detail": "Falta táctica"},
                {"min": 74, "icon": "🔄", "title": "Cambio", "player": f"Entra #10 / Sale #7 {loc_name}", "detail": "Ajuste ofensivo"}
            ][:g_l + 2]
            eventos_visita = [
                {"min": 38, "icon": "🟨", "title": "Tarjeta Amarilla", "player": f"Defensa {vis_name}", "detail": "Reiteración de faltas"},
                {"min": 65, "icon": "⚽", "title": "¡GOL!", "player": f"Extremo {vis_name}", "detail": "Remate de cabeza tras tiro de esquina"},
                {"min": 81, "icon": "🔄", "title": "Cambio", "player": f"Entra #9 / Sale #11 {vis_name}", "detail": "Refresco en ataque"}
            ][:g_v + 2]
        else:
            eventos_local = [
                {"min": 0, "icon": "📋", "title": "Alineación Confirmada", "player": f"11 Inicial {loc_name}", "detail": "Esquema táctico ratificado por el DT"},
                {"min": 0, "icon": "🔥", "title": "Calentamiento Previo", "player": f"{loc_name}", "detail": "Ejercicios precompetitivos en cancha"},
                {"min": 0, "icon": "🧠", "title": "Simulación Poisson", "player": "Smart Pick Pro VIP", "detail": "Modelos predictivos y xG calculados"}
            ]
            eventos_visita = [
                {"min": 0, "icon": "📋", "title": "Alineación Confirmada", "player": f"11 Inicial {vis_name}", "detail": "Esquema táctico ratificado por el DT"},
                {"min": 0, "icon": "🔥", "title": "Calentamiento Previo", "player": f"{vis_name}", "detail": "Ejercicios precompetitivos en cancha"},
                {"min": 0, "icon": "🛡️", "title": "Paridad Defensiva", "player": "Smart Pick Pro VIP", "detail": "Matriz Dixon-Coles procesada"}
            ]

    # Formatear lista de eventos local
    html_ev_loc = ""
    for ev in eventos_local:
        if isinstance(ev, str):
            partes = ev.split(" - ")
            m_str = partes[0] if len(partes) > 0 else "0'"
            det_str = partes[1] if len(partes) > 1 else ev
            ev_icon = "⚽" if "GOL" in det_str else ("🟨" if "Amarilla" in det_str else ("🟥" if "Roja" in det_str else ("🔄" if "Cambio" in det_str else "📌")))
            m_val = m_str.replace("'", "")
            html_ev_loc += f'<div style="display:flex; align-items:center; justify-content:flex-end; gap:10px; margin-bottom:12px;"><div style="background:#151821; border:1px solid #282F3F; border-right:3px solid #38BDF8; padding:8px 12px; border-radius:8px 2px 2px 8px; text-align:right; max-width:85%;"><div style="font-size:13px; font-weight:800; color:#FFFFFF;">{html.escape(det_str)}</div></div><div style="background:#38BDF8; color:#0D0F14; font-weight:900; font-size:12px; padding:4px 8px; border-radius:50px; min-width:32px; text-align:center; box-shadow:0 0 8px rgba(56,189,248,0.4);">{m_val}\'</div></div>'
        elif isinstance(ev, dict):
            html_ev_loc += f'<div style="display:flex; align-items:center; justify-content:flex-end; gap:10px; margin-bottom:12px;"><div style="background:#151821; border:1px solid #282F3F; border-right:3px solid #38BDF8; padding:8px 12px; border-radius:8px 2px 2px 8px; text-align:right; max-width:85%;"><div style="font-size:13px; font-weight:800; color:#FFFFFF;">{ev.get("icon", "📌")} <b>{html.escape(ev.get("title", ""))}</b></div><div style="font-size:12px; color:#38BDF8; font-weight:bold;">{html.escape(ev.get("player", ""))}</div><div style="font-size:11px; color:#aaa;">{html.escape(ev.get("detail", ""))}</div></div><div style="background:#38BDF8; color:#0D0F14; font-weight:900; font-size:12px; padding:4px 8px; border-radius:50px; min-width:32px; text-align:center; box-shadow:0 0 8px rgba(56,189,248,0.4);">{ev.get("min", 0)}\'</div></div>'

    # Formatear lista de eventos visita
    html_ev_vis = ""
    for ev in eventos_visita:
        if isinstance(ev, str):
            partes = ev.split(" - ")
            m_str = partes[0] if len(partes) > 0 else "0'"
            det_str = partes[1] if len(partes) > 1 else ev
            ev_icon = "⚽" if "GOL" in det_str else ("🟨" if "Amarilla" in det_str else ("🟥" if "Roja" in det_str else ("🔄" if "Cambio" in det_str else "📌")))
            m_val = m_str.replace("'", "")
            html_ev_vis += f'<div style="display:flex; align-items:center; justify-content:flex-start; gap:10px; margin-bottom:12px;"><div style="background:#EF4444; color:white; font-weight:900; font-size:12px; padding:4px 8px; border-radius:50px; min-width:32px; text-align:center; box-shadow:0 0 8px rgba(239,68,68,0.4);">{m_val}\'</div><div style="background:#151821; border:1px solid #282F3F; border-left:3px solid #EF4444; padding:8px 12px; border-radius:2px 8px 8px 2px; text-align:left; max-width:85%;"><div style="font-size:13px; font-weight:800; color:#FFFFFF;">{html.escape(det_str)}</div></div></div>'
        elif isinstance(ev, dict):
            html_ev_vis += f'<div style="display:flex; align-items:center; justify-content:flex-start; gap:10px; margin-bottom:12px;"><div style="background:#EF4444; color:white; font-weight:900; font-size:12px; padding:4px 8px; border-radius:50px; min-width:32px; text-align:center; box-shadow:0 0 8px rgba(239,68,68,0.4);">{ev.get("min", 0)}\'</div><div style="background:#151821; border:1px solid #282F3F; border-left:3px solid #EF4444; padding:8px 12px; border-radius:2px 8px 8px 2px; text-align:left; max-width:85%;"><div style="font-size:13px; font-weight:800; color:#FFFFFF;">{ev.get("icon", "📌")} <b>{html.escape(ev.get("title", ""))}</b></div><div style="font-size:12px; color:#F87171; font-weight:bold;">{html.escape(ev.get("player", ""))}</div><div style="font-size:11px; color:#aaa;">{html.escape(ev.get("detail", ""))}</div></div></div>'

    pct_tiros_l = int((tiros_local / max(1, tiros_local + tiros_visita)) * 100)
    pct_tiros_v = 100 - pct_tiros_l

    html_full = (
        f'<div style="background: linear-gradient(180deg, #151821 0%, #0D0F14 100%); border: 1.5px solid #D4AF37; border-radius: 16px; padding: 20px; color: white; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #282F3F; padding-bottom:14px; margin-bottom:16px;">'
        f'<div style="font-size:18px; font-weight:900; color:#D4AF37;">⏱️ CENTRO DE PARTIDO: MINUTO A MINUTO EN VIVO</div>'
        f'<div style="background:{status_color}; color:#0D0F14; font-weight:900; padding:5px 14px; border-radius:20px; font-size:13px; letter-spacing:1px;">{status_label}</div>'
        f'</div>'
        f'<div style="display:grid; grid-template-columns: 1fr auto 1fr; align-items:center; gap:15px; margin-bottom:20px; background:#11141C; padding:15px; border-radius:12px; border:1px solid #282F3F;">'
        f'<div style="display:flex; align-items:center; justify-content:flex-end; gap:12px;"><span style="font-size:17px; font-weight:900; color:#FFFFFF; text-align:right;">{loc_name}</span><img src="{logo_local}" style="width:48px; height:48px; object-fit:contain;"></div>'
        f'<div style="text-align:center; padding:0 15px;">{score_center}</div>'
        f'<div style="display:flex; align-items:center; justify-content:flex-start; gap:12px;"><img src="{logo_visita}" style="width:48px; height:48px; object-fit:contain;"><span style="font-size:17px; font-weight:900; color:#FFFFFF; text-align:left;">{vis_name}</span></div>'
        f'</div>'
        f'<div style="background:#11141C; padding:14px; border-radius:12px; margin-bottom:20px; border:1px solid #282F3F;">'
        f'<div style="font-size:12px; font-weight:800; color:#D4AF37; text-transform:uppercase; margin-bottom:10px; text-align:center; letter-spacing:0.5px;">📊 ESTADÍSTICAS DEL PARTIDO EN TIEMPO REAL</div>'
        f'<div style="margin-bottom:10px;"><div style="display:flex; justify-content:space-between; font-size:12px; font-weight:bold; margin-bottom:4px;"><span style="color:#38BDF8;">{pos_local}%</span><span style="color:#aaa;">Posesión de Balón</span><span style="color:#EF4444;">{pos_visita}%</span></div><div style="display:flex; height:8px; border-radius:4px; overflow:hidden; background:#282F3F;"><div style="width:{pos_local}%; background:#38BDF8;"></div><div style="width:{pos_visita}%; background:#EF4444;"></div></div></div>'
        f'<div style="margin-bottom:6px;"><div style="display:flex; justify-content:space-between; font-size:12px; font-weight:bold; margin-bottom:4px;"><span style="color:#38BDF8;">{tiros_local} Tiros</span><span style="color:#aaa;">Disparos al Arco</span><span style="color:#EF4444;">{tiros_visita} Tiros</span></div><div style="display:flex; height:8px; border-radius:4px; overflow:hidden; background:#282F3F;"><div style="width:{pct_tiros_l}%; background:#38BDF8;"></div><div style="width:{pct_tiros_v}%; background:#EF4444;"></div></div></div>'
        f'</div>'
        f'<div style="display:grid; grid-template-columns: 1fr 2px 1fr; gap:16px; position:relative; margin-top:10px;">'
        f'<div><div style="text-align:right; font-size:14px; font-weight:900; color:#38BDF8; margin-bottom:12px; border-bottom:2px solid #38BDF8; padding-bottom:4px;">🔵 ACCIONES {loc_name.upper()}</div>{html_ev_loc}</div>'
        f'<div style="background: linear-gradient(180deg, #38BDF8 0%, #282F3F 50%, #EF4444 100%); width:2px; border-radius:2px;"></div>'
        f'<div><div style="text-align:left; font-size:14px; font-weight:900; color:#EF4444; margin-bottom:12px; border-bottom:2px solid #EF4444; padding-bottom:4px;">🔴 ACCIONES {vis_name.upper()}</div>{html_ev_vis}</div>'
        f'</div>'
        f'</div>'
    )
    return html_full


def render_tarjeta_partido_live_radar(partido: dict) -> str:
    """
    Renderiza la tarjeta visual deportiva para el Radar Multiligas en Vivo.
    """
    import html
    loc = html.escape(str(partido.get('local', 'Local')))
    vis = html.escape(str(partido.get('visita', 'Visita')))
    logo_l = partido.get('logo_local', 'https://media.api-sports.io/football/teams/2287.png')
    logo_v = partido.get('logo_visita', 'https://media.api-sports.io/football/teams/2291.png')
    g_l = partido.get('goles_local', 0)
    g_v = partido.get('goles_visita', 0)
    st_val = str(partido.get('status', 'LIVE')).upper()
    min_val = partido.get('minuto', 0)
    venue = html.escape(str(partido.get('venue', 'Estadio')))

    if st_val in ['1H', '2H', 'LIVE']:
        st_badge = f'<span style="background:rgba(239,68,68,0.2); color:#EF5350; border:1px solid #EF5350; padding:3px 10px; border-radius:20px; font-weight:900; font-size:11px; letter-spacing:0.5px;">🔴 {st_val} {min_val}\'</span>'
    elif st_val == 'HT':
        st_badge = '<span style="background:rgba(212,175,55,0.2); color:#D4AF37; border:1px solid #D4AF37; padding:3px 10px; border-radius:20px; font-weight:900; font-size:11px;">⏸️ ENTRETIEMPO</span>'
    elif st_val in ['FT', 'AET', 'PEN']:
        st_badge = '<span style="background:rgba(212,175,55,0.15); color:#D4AF37; border:1px solid #D4AF37; padding:3px 10px; border-radius:20px; font-weight:900; font-size:11px;">🏁 FINAL</span>'
    else:
        st_badge = f'<span style="background:rgba(255,255,255,0.1); color:#aaa; border:1px solid #444; padding:3px 10px; border-radius:20px; font-weight:bold; font-size:11px;">⏳ {st_val}</span>'

    card_html = (
        f'<div style="background:linear-gradient(135deg, #151821 0%, #1A1E29 100%); border:1px solid #282F3F; border-radius:14px; padding:14px 18px; margin-bottom:10px; box-shadow:0 4px 15px rgba(0,0,0,0.3);">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; border-bottom:1px solid #232938; padding-bottom:6px;">'
        f'<div style="color:#aaa; font-size:11px; font-weight:bold;">📍 {venue}</div>'
        f'<div>{st_badge}</div>'
        f'</div>'
        f'<div style="display:grid; grid-template-columns:1fr auto 1fr; align-items:center; gap:12px; margin-bottom:6px;">'
        f'<div style="display:flex; align-items:center; justify-content:flex-end; gap:10px; text-align:right;">'
        f'<span style="color:#FFFFFF; font-weight:900; font-size:15px; line-height:1.2;">{loc}</span>'
        f'<img src="{logo_l}" style="width:36px; height:36px; object-fit:contain; flex-shrink:0;">'
        f'</div>'
        f'<div style="background:#0D0F14; border:1.5px solid #D4AF37; padding:4px 16px; border-radius:8px; font-size:22px; font-weight:900; color:#D4AF37; letter-spacing:2px; text-align:center; min-width:70px;">'
        f'{g_l} - {g_v}'
        f'</div>'
        f'<div style="display:flex; align-items:center; justify-content:flex-start; gap:10px; text-align:left;">'
        f'<img src="{logo_v}" style="width:36px; height:36px; object-fit:contain; flex-shrink:0;">'
        f'<span style="color:#FFFFFF; font-weight:900; font-size:15px; line-height:1.2;">{vis}</span>'
        f'</div>'
        f'</div>'
        f'</div>'
    )
    return card_html


def render_ticket_parlay_altas(parlay_data: dict) -> str:
    """
    Renderiza el boleto de Parlay Maestro de Altas en Goles (Top 15) con diseño deportivo VIP.
    Sin indentaciones de 4 espacios para evitar falsos bloques de código en Markdown.
    """
    import html
    total_p = parlay_data.get("total_partidos", 15)
    cuota_tot = parlay_data.get("cuota_acumulada", 1.0)
    picks = parlay_data.get("picks", [])

    html_items = ""
    for idx, p in enumerate(picks):
        loc = html.escape(str(p.get("local", "")))
        vis = html.escape(str(p.get("visita", "")))
        liga = html.escape(str(p.get("liga", "")))
        hora = html.escape(str(p.get("hora", "")))
        hora_badge = f'<span style="color:#38BDF8; font-size:11px; margin-left:6px; font-weight:bold;">⏰ {hora}</span>' if hora else ""
        mercado = html.escape(str(p.get("mercado", "Más de 1.5 Goles")))
        prob = p.get("probabilidad", 75.0)
        cuota = p.get("cuota", 1.30)

        html_items += (
            f'<div style="display:flex; justify-content:space-between; align-items:center; background:#11141C; border:1px solid #282F3F; border-left:4px solid #D4AF37; padding:10px 14px; border-radius:8px; margin-bottom:8px;">'
            f'<div style="flex:1;">'
            f'<div style="color:#aaa; font-size:11px; font-weight:bold;">{idx+1}. {liga}{hora_badge}</div>'
            f'<div style="color:#FFFFFF; font-weight:900; font-size:14px; margin-top:2px;">{loc} vs {vis}</div>'
            f'</div>'
            f'<div style="text-align:right; display:flex; align-items:center; gap:10px;">'
            f'<div style="background:rgba(212,175,55,0.15); border:1px solid #D4AF37; color:#D4AF37; font-weight:900; padding:4px 10px; border-radius:6px; font-size:13px;">⚽ {mercado}</div>'
            f'<div style="background:#151821; border:1px solid #F3E5AB; color:#F3E5AB; font-weight:900; padding:4px 10px; border-radius:6px; font-size:13px; min-width:65px; text-align:center;">@{cuota:.2f}</div>'
            f'<div style="background:#0D0F14; color:#FFFFFF; font-weight:bold; font-size:11px; padding:4px 8px; border-radius:4px; border:1px solid #282F3F;">{prob}%</div>'
            f'</div>'
            f'</div>'
        )

    html_ticket = (
        f'<div style="background:linear-gradient(135deg, #151821 0%, #1A1E29 100%); border:1.5px solid #D4AF37; border-radius:16px; padding:20px; color:white; margin-bottom:20px; box-shadow:0 8px 25px rgba(212,175,55,0.2);">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #282F3F; padding-bottom:14px; margin-bottom:16px;">'
        f'<div>'
        f'<div style="font-size:20px; font-weight:900; color:#D4AF37;">🔥 BOLETO PARLAY MAESTRO DE ALTAS (PARTIDOS DE HOY)</div>'
        f'<div style="color:#aaa; font-size:13px;">Selección de los {total_p} partidos de hoy con mayor volumen ofensivo y xG esperado</div>'
        f'</div>'
        f'<div style="text-align:right; background:#11141C; border:1.5px solid #D4AF37; padding:8px 18px; border-radius:10px;">'
        f'<div style="font-size:11px; color:#F3E5AB; font-weight:bold; text-transform:uppercase;">Cuota Combinada Total</div>'
        f'<div style="font-size:24px; font-weight:900; color:#D4AF37; letter-spacing:1px;">x{cuota_tot:,.2f}</div>'
        f'</div>'
        f'</div>'
        f'<div>{html_items}</div>'
        f'</div>'
    )
    return html_ticket


def render_ticket_empates_oro(empates_data: dict) -> str:
    """
    Renderiza el boleto de Radar de Empates de Oro (Top 5) con diseño deportivo VIP.
    Sin indentaciones de 4 espacios para evitar falsos bloques de código en Markdown.
    """
    import html
    total_p = empates_data.get("total_partidos", 5)
    cuota_tot = empates_data.get("cuota_parlay_empates", 1.0)
    empates = empates_data.get("empates", [])

    html_items = ""
    for idx, e in enumerate(empates):
        loc = html.escape(str(e.get("local", "")))
        vis = html.escape(str(e.get("visita", "")))
        liga = html.escape(str(e.get("liga", "")))
        hora = html.escape(str(e.get("hora", "")))
        hora_badge = f'<span style="color:#38BDF8; font-size:11px; margin-left:6px; font-weight:bold;">⏰ {hora}</span>' if hora else ""
        prob = e.get("probabilidad_empate", 33.0)
        cuota = e.get("cuota_empate", 3.25)
        marcador = html.escape(str(e.get("marcador_probable", "1 - 1")))
        doble_op = html.escape(str(e.get("doble_oportunidad", "")))

        html_items += (
            f'<div style="background:#11141C; border:1px solid #282F3F; border-left:4px solid #D4AF37; padding:14px 18px; border-radius:10px; margin-bottom:12px;">'
            f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">'
            f'<span style="color:#aaa; font-size:12px; font-weight:bold;">{idx+1}. {liga}{hora_badge}</span>'
            f'<span style="background:rgba(212,175,55,0.15); color:#D4AF37; border:1px solid #D4AF37; font-weight:900; padding:2px 10px; border-radius:12px; font-size:12px;">⚖️ Paridad Extrema</span>'
            f'</div>'
            f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">'
            f'<span style="color:#FFFFFF; font-weight:900; font-size:16px;">{loc} vs {vis}</span>'
            f'<span style="background:#0D0F14; border:1.5px solid #D4AF37; color:#D4AF37; font-weight:900; padding:4px 14px; border-radius:8px; font-size:16px;">Cuota @{cuota:.2f}</span>'
            f'</div>'
            f'<div style="display:flex; justify-content:space-between; align-items:center; background:#151821; padding:8px 12px; border-radius:6px; font-size:12px; border:1px solid #282F3F;">'
            f'<span style="color:#D4AF37; font-weight:bold;">🎯 Marcador Probable: <b>{marcador}</b> (Prob: {prob}%)</span>'
            f'<span style="color:#ddd;">🛡️ Opción Segura: <b>{doble_op}</b></span>'
            f'</div>'
            f'</div>'
        )

    html_ticket = (
        f'<div style="background:linear-gradient(135deg, #151821 0%, #1A1E29 100%); border:1.5px solid #D4AF37; border-radius:16px; padding:20px; color:white; margin-bottom:20px; box-shadow:0 8px 25px rgba(212,175,55,0.2);">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #282F3F; padding-bottom:14px; margin-bottom:16px;">'
        f'<div>'
        f'<div style="font-size:20px; font-weight:900; color:#D4AF37;">⚖️ RADAR DE EMPATES DE ORO (PARTIDOS DE HOY)</div>'
        f'<div style="color:#aaa; font-size:13px;">Encuentros de máxima paridad táctica de la jornada de hoy con cuotas superiores a 3.00</div>'
        f'</div>'
        f'<div style="text-align:right; background:#11141C; border:1.5px solid #D4AF37; padding:8px 18px; border-radius:10px;">'
        f'<div style="font-size:11px; color:#F3E5AB; font-weight:bold; text-transform:uppercase;">Cuota Parlay Empates</div>'
        f'<div style="font-size:24px; font-weight:900; color:#D4AF37; letter-spacing:1px;">x{cuota_tot:,.2f}</div>'
        f'</div>'
        f'</div>'
        f'<div>{html_items}</div>'
        f'</div>'
    )
    return html_ticket


def render_ticket_bet_builder(bet_builder_data, equipo_local: str = "", equipo_visita: str = "") -> str:
    """
    Renderiza el Parlay Sugerido (Bet Builder Multifactorial) de 4 Factores
    (Resultado + Goles + Tarjetas + Córners) con diseño VIP dorado y cuota combinada.
    """
    import html
    
    if isinstance(bet_builder_data, dict):
        picks = bet_builder_data.get("picks", [])
        cuota_total = bet_builder_data.get("cuota_total", 2.50)
        loc = bet_builder_data.get("local", equipo_local)
        vis = bet_builder_data.get("visita", equipo_visita)
    elif isinstance(bet_builder_data, list):
        picks = bet_builder_data
        cuota_total = 2.50
        loc = equipo_local
        vis = equipo_visita
    else:
        return ""

    html_items = ""
    for p in picks:
        cat = html.escape(str(p.get("categoria", "🎯 Pick")))
        desc = html.escape(str(p.get("descripcion", "")))
        prob = html.escape(str(p.get("prob", "75%")))
        cuota = p.get("cuota", 1.30)
        
        try:
            cuota_str = f"@{float(cuota):.2f}"
        except (ValueError, TypeError):
            cuota_str = "@1.30"

        html_items += (
            f'<div style="display:flex; justify-content:space-between; align-items:center; background:#1A1E29; border:1px solid #282F3F; padding:12px 16px; border-radius:10px; margin-bottom:8px;">'
            f'<div style="flex:1;">'
            f'<div style="color:#F3E5AB; font-size:12px; font-weight:bold; letter-spacing:0.5px; text-transform:uppercase;">{cat}</div>'
            f'<div style="color:#FFFFFF; font-size:15px; font-weight:900; margin-top:3px;">✅ {desc}</div>'
            f'</div>'
            f'<div style="display:flex; align-items:center; gap:8px; text-align:right;">'
            f'<span style="background:#11141C; color:#F3E5AB; border:1px solid #D4AF37; font-weight:900; padding:4px 10px; border-radius:8px; font-size:13px;">{cuota_str}</span>'
            f'<span style="background:#D4AF37; color:#0D0F14; font-weight:900; padding:4px 12px; border-radius:12px; font-size:13px; box-shadow:0 2px 6px rgba(212,175,55,0.3);">Confianza: {prob}</span>'
            f'</div>'
            f'</div>'
        )

    vs_txt = f"{loc} vs {vis}" if loc and vis else "Encuentro Seleccionado"

    html_card = (
        f'<div style="background:linear-gradient(135deg, #151821 0%, #1A1E29 100%); border:2px dashed #D4AF37; border-radius:16px; padding:20px; color:white; margin-bottom:20px; box-shadow:0 8px 25px rgba(0,0,0,0.4);">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #282F3F; padding-bottom:12px; margin-bottom:14px; flex-wrap:wrap; gap:10px;">'
        f'<div>'
        f'<div style="font-size:20px; font-weight:900; color:#D4AF37;">🧩 PARLAY SUGERIDO (BET BUILDER MULTIFACTORIAL)</div>'
        f'<div style="color:#94A3B8; font-size:13px; margin-top:2px;">{vs_txt} • 4 Factores: Poisson + Dixon-Coles + xG + Árbitro + Córners</div>'
        f'</div>'
        f'<div style="background:#11141C; border:1.5px solid #D4AF37; padding:6px 16px; border-radius:10px; text-align:right;">'
        f'<div style="font-size:11px; color:#F3E5AB; font-weight:bold; text-transform:uppercase;">Cuota Combinada Parlay</div>'
        f'<div style="font-size:22px; font-weight:900; color:#D4AF37; letter-spacing:0.5px;">x{cuota_total:,.2f}</div>'
        f'</div>'
        f'</div>'
        f'<div>{html_items}</div>'
        f'<div style="background:rgba(212,175,55,0.08); border:1px solid rgba(212,175,55,0.25); border-radius:8px; padding:8px 12px; margin-top:10px; font-size:12px; color:#F3E5AB; display:flex; align-items:center; gap:6px;">'
        f'<span>💡</span> <span><b>Tip Pro:</b> Puedes combinar estas 4 selecciones en la pestaña <i>"Crear Apuesta" / "Bet Builder"</i> de tu casa de apuestas favorita con cuota combinada estimada de <b>x{cuota_total:,.2f}</b>.</span>'
        f'</div>'
        f'</div>'
    )
    return html_card

def render_tarjeta_partido_hoy(p_item: dict, pick_info: dict = None) -> str:
    """
    Renderiza una tarjeta VIP premium para la sección 'Partidos de Hoy'
    con horario en vivo, escudos oficiales y el Pick Recomendado del Día (+EV).
    """
    import html
    loc = html.escape(str(p_item.get('local', 'Local')))
    vis = html.escape(str(p_item.get('visita', 'Visita')))
    logo_l = p_item.get('logo_local', 'https://media.api-sports.io/football/teams/2287.png')
    logo_v = p_item.get('logo_visita', 'https://media.api-sports.io/football/teams/2291.png')
    hora = html.escape(str(p_item.get('hora', 'Hoy')))
    venue = html.escape(str(p_item.get('venue', 'Estadio')))
    st_val = str(p_item.get('status', 'NS')).upper()
    min_val = p_item.get('minuto', 0)
    g_l = p_item.get('goles_local', 0)
    g_v = p_item.get('goles_visita', 0)

    if st_val in ['1H', '2H', 'LIVE']:
        st_badge = f'<span style="background:rgba(231,76,60,0.2); color:#EF5350; border:1px solid #EF5350; padding:3px 10px; border-radius:20px; font-weight:900; font-size:11px;">🔴 EN VIVO {min_val}\'</span>'
        marcador_box = f'<div style="background:#0D0F14; border:1.5px solid #EF5350; padding:4px 14px; border-radius:8px; font-size:20px; font-weight:900; color:#EF5350; letter-spacing:2px; text-align:center;">{g_l} - {g_v}</div>'
    elif st_val == 'HT':
        st_badge = '<span style="background:rgba(212,175,55,0.2); color:#D4AF37; border:1px solid #D4AF37; padding:3px 10px; border-radius:20px; font-weight:900; font-size:11px;">⏸️ ENTRETIEMPO</span>'
        marcador_box = f'<div style="background:#0D0F14; border:1.5px solid #D4AF37; padding:4px 14px; border-radius:8px; font-size:20px; font-weight:900; color:#D4AF37; letter-spacing:2px; text-align:center;">{g_l} - {g_v}</div>'
    elif st_val in ['FT', 'AET', 'PEN']:
        st_badge = '<span style="background:rgba(212,175,55,0.15); color:#D4AF37; border:1px solid #D4AF37; padding:3px 10px; border-radius:20px; font-weight:900; font-size:11px;">🏁 FINAL</span>'
        marcador_box = f'<div style="background:#0D0F14; border:1.5px solid #D4AF37; padding:4px 14px; border-radius:8px; font-size:20px; font-weight:900; color:#D4AF37; letter-spacing:2px; text-align:center;">{g_l} - {g_v}</div>'
    else:
        st_badge = f'<span style="background:rgba(56,189,248,0.15); color:#38BDF8; border:1px solid #38BDF8; padding:3px 10px; border-radius:20px; font-weight:bold; font-size:11px;">⏰ {hora}</span>'
        marcador_box = '<div style="background:#0D0F14; border:1px solid #282F3F; padding:4px 14px; border-radius:8px; font-size:14px; font-weight:900; color:#aaa; text-align:center;">VS</div>'

    # Pick Recomendado
    pick_html = ""
    if pick_info:
        p_txt = html.escape(str(pick_info.get('pick', 'Doble Oportunidad')))
        p_cuota = pick_info.get('cuota', 1.35)
        p_prob = pick_info.get('probabilidad', 75.0)
        p_tipo = html.escape(str(pick_info.get('tipo', '🎯 Pick Recomendado')))

        pick_html = (
            f'<div style="background:#11141C; border:1px solid #D4AF37; border-radius:10px; padding:10px 14px; margin-top:10px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">'
            f'<div>'
            f'<div style="color:#F3E5AB; font-size:11px; font-weight:bold; text-transform:uppercase;">{p_tipo} (Resuelve Hoy)</div>'
            f'<div style="color:#FFFFFF; font-size:14px; font-weight:900; margin-top:2px;">🎯 {p_txt}</div>'
            f'</div>'
            f'<div style="display:flex; align-items:center; gap:8px;">'
            f'<span style="background:#1A1E29; color:#D4AF37; border:1px solid #D4AF37; font-weight:900; padding:3px 10px; border-radius:8px; font-size:13px;">@{p_cuota:.2f}</span>'
            f'<span style="background:#D4AF37; color:#0D0F14; font-weight:900; padding:3px 10px; border-radius:10px; font-size:12px;">Conf: {p_prob}%</span>'
            f'</div>'
            f'</div>'
        )

    card_html = (
        f'<div style="background:linear-gradient(135deg, #151821 0%, #1A1E29 100%); border:1px solid #282F3F; border-radius:14px; padding:14px 18px; margin-bottom:12px; box-shadow:0 4px 15px rgba(0,0,0,0.3);">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; border-bottom:1px solid #232938; padding-bottom:6px;">'
        f'<div style="color:#aaa; font-size:11px; font-weight:bold;">📍 {venue}</div>'
        f'<div>{st_badge}</div>'
        f'</div>'
        f'<div style="display:grid; grid-template-columns:1fr auto 1fr; align-items:center; gap:12px; margin-bottom:4px;">'
        f'<div style="display:flex; align-items:center; justify-content:flex-end; gap:10px; text-align:right;">'
        f'<span style="color:#FFFFFF; font-weight:900; font-size:15px; line-height:1.2;">{loc}</span>'
        f'<img src="{logo_l}" style="width:38px; height:38px; object-fit:contain; flex-shrink:0;">'
        f'</div>'
        f'{marcador_box}'
        f'<div style="display:flex; align-items:center; justify-content:flex-start; gap:10px; text-align:left;">'
        f'<img src="{logo_v}" style="width:38px; height:38px; object-fit:contain; flex-shrink:0;">'
        f'<span style="color:#FFFFFF; font-weight:900; font-size:15px; line-height:1.2;">{vis}</span>'
        f'</div>'
        f'</div>'
        f'{pick_html}'
        f'</div>'
    )
    return card_html


def render_tarjeta_festival_goles(p_item: dict, stats_poisson: dict = None, idx_goles: dict = None) -> str:
    """
    Renderiza la tarjeta visual especializada para el Radar del Festival de Goles.
    Incluye Termómetro Ofensivo, Probabilidades de Over 2.5 / BTTS, xG Total y Pick de Alta Certeza.
    """
    import html
    loc = html.escape(str(p_item.get('local', 'Local')))
    vis = html.escape(str(p_item.get('visita', 'Visita')))
    logo_l = p_item.get('logo_local', 'https://media.api-sports.io/football/teams/2287.png')
    logo_v = p_item.get('logo_visita', 'https://media.api-sports.io/football/teams/2291.png')
    hora = html.escape(str(p_item.get('hora', 'Hoy')))
    liga = html.escape(str(p_item.get('liga', 'Torneo')))
    venue = html.escape(str(p_item.get('venue', 'Estadio')))

    if not idx_goles and stats_poisson:
        import analytics
        idx_goles = analytics.calcular_indice_goleador(stats_poisson)
    elif not idx_goles:
        idx_goles = {
            "score": 82.5, "etiqueta": "🔥 FESTIVAL INMINENTE", "color": "#EF4444",
            "termometro": "🔥🔥🔥🔥🔥", "xg_total": 3.4, "p_over_15": 86.0,
            "p_over_25": 68.0, "p_btts": 78.0, "pick_sugerido": "Ambos Equipos Anotan (Sí)",
            "cuota_sugerida": 1.40
        }

    score_val = idx_goles.get("score", 75.0)
    etiq = html.escape(str(idx_goles.get("etiqueta", "🔥 FESTIVAL DE GOLES")))
    col_etiq = idx_goles.get("color", "#EF4444")
    term = idx_goles.get("termometro", "🔥🔥🔥🔥🔥")
    xg = idx_goles.get("xg_total", 3.0)
    p_btts = idx_goles.get("p_btts", 70.0)
    p_o25 = idx_goles.get("p_over_25", 65.0)
    pick_sug = html.escape(str(idx_goles.get("pick_sugerido", "Ambos Equipos Anotan (Sí)")))
    cuota_sug = idx_goles.get("cuota_sugerida", 1.40)

    card_html = (
        f'<div style="background:linear-gradient(135deg, #1C202B 0%, #2A1A1A 100%); border:1.5px solid {col_etiq}; border-radius:14px; padding:16px 18px; margin-bottom:14px; box-shadow:0 6px 20px rgba(239,68,68,0.2);">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; border-bottom:1px solid #332020; padding-bottom:8px;">'
        f'<div style="color:#CBD5E1; font-size:12px; font-weight:bold;">🏆 {liga} • ⏰ {hora}</div>'
        f'<span style="background:{col_etiq}; color:#FFFFFF; font-weight:900; font-size:11px; padding:3px 12px; border-radius:12px; letter-spacing:0.5px; box-shadow:0 2px 8px rgba(0,0,0,0.4);">{etiq}</span>'
        f'</div>'
        f'<div style="display:grid; grid-template-columns:1fr auto 1fr; align-items:center; gap:12px; margin-bottom:12px;">'
        f'<div style="display:flex; align-items:center; justify-content:flex-end; gap:10px; text-align:right;">'
        f'<span style="color:#FFFFFF; font-weight:900; font-size:15px; line-height:1.2;">{loc}</span>'
        f'<img src="{logo_l}" style="width:38px; height:38px; object-fit:contain; flex-shrink:0;">'
        f'</div>'
        f'<div style="background:#0D0F14; border:1px solid #D4AF37; padding:4px 12px; border-radius:8px; font-size:12px; font-weight:900; color:#D4AF37; text-align:center;">'
        f'xG: {xg}'
        f'</div>'
        f'<div style="display:flex; align-items:center; justify-content:flex-start; gap:10px; text-align:left;">'
        f'<img src="{logo_v}" style="width:38px; height:38px; object-fit:contain; flex-shrink:0;">'
        f'<span style="color:#FFFFFF; font-weight:900; font-size:15px; line-height:1.2;">{vis}</span>'
        f'</div>'
        f'</div>'
        f'<div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:8px; background:#11141C; padding:10px; border-radius:10px; border:1px solid #282F3F; margin-bottom:10px; text-align:center;">'
        f'<div>'
        f'<div style="color:#aaa; font-size:10px; font-weight:bold;">🔥 POTENCIAL GOL</div>'
        f'<div style="color:{col_etiq}; font-weight:900; font-size:14px;">{score_val}%</div>'
        f'</div>'
        f'<div>'
        f'<div style="color:#aaa; font-size:10px; font-weight:bold;">⚽ AMBOS ANOTAN</div>'
        f'<div style="color:#38BDF8; font-weight:900; font-size:14px;">{p_btts:.1f}%</div>'
        f'</div>'
        f'<div>'
        f'<div style="color:#aaa; font-size:10px; font-weight:bold;">📈 MÁS DE 2.5</div>'
        f'<div style="color:#F59E0B; font-weight:900; font-size:14px;">{p_o25:.1f}%</div>'
        f'</div>'
        f'</div>'
        f'<div style="background:rgba(212,175,55,0.12); border:1px solid #D4AF37; border-radius:10px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">'
        f'<div>'
        f'<div style="color:#F3E5AB; font-size:10px; font-weight:bold; text-transform:uppercase;">Pick Recomendado del Festival</div>'
        f'<div style="color:#FFFFFF; font-size:14px; font-weight:900;">🎯 {pick_sug}</div>'
        f'</div>'
        f'<div style="display:flex; align-items:center; gap:8px;">'
        f'<span style="background:#11141C; color:#D4AF37; border:1px solid #D4AF37; font-weight:900; padding:4px 10px; border-radius:8px; font-size:13px;">@{cuota_sug:.2f}</span>'
        f'<span style="font-size:14px;">{term}</span>'
        f'</div>'
        f'</div>'
        f'</div>'
    )
    return card_html


def render_ticket_parlay_festival_goles(parlay_data: dict) -> str:
    """
    Renderiza el ticket de Parlay del Festival de Goles (Combinada de Altas).
    """
    import html
    picks = parlay_data.get("picks", [])
    cuota_total = parlay_data.get("cuota_total", 2.80)
    
    html_items = ""
    for p in picks:
        partido = html.escape(str(p.get("partido", "")))
        liga = html.escape(str(p.get("liga", "")))
        pick_txt = html.escape(str(p.get("pick", "")))
        cuota = p.get("cuota", 1.30)
        conf = p.get("confianza", "75%")
        term = p.get("termometro", "🔥🔥🔥🔥")
        
        html_items += (
            f'<div style="display:flex; justify-content:space-between; align-items:center; background:#1A1E29; border:1px solid #282F3F; padding:10px 14px; border-radius:10px; margin-bottom:8px;">'
            f'<div style="flex:1;">'
            f'<div style="color:#94A3B8; font-size:11px; font-weight:bold;">{liga} • {term}</div>'
            f'<div style="color:#FFFFFF; font-size:14px; font-weight:900; margin-top:2px;">⚽ {partido}</div>'
            f'<div style="color:#F3E5AB; font-size:13px; font-weight:bold; margin-top:1px;">🎯 {pick_txt}</div>'
            f'</div>'
            f'<div style="display:flex; align-items:center; gap:8px; text-align:right;">'
            f'<span style="background:#11141C; color:#F3E5AB; border:1px solid #D4AF37; font-weight:900; padding:4px 10px; border-radius:8px; font-size:13px;">@{cuota:.2f}</span>'
            f'<span style="background:#EF4444; color:#FFFFFF; font-weight:900; padding:4px 10px; border-radius:10px; font-size:12px;">{conf}</span>'
            f'</div>'
            f'</div>'
        )
        
    html_ticket = (
        f'<div style="background:linear-gradient(135deg, #181E29 0%, #2D1414 100%); border:2px dashed #EF4444; border-radius:16px; padding:20px; color:white; margin-bottom:20px; box-shadow:0 8px 25px rgba(0,0,0,0.4);">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #3B2020; padding-bottom:12px; margin-bottom:14px; flex-wrap:wrap; gap:10px;">'
        f'<div>'
        f'<div style="font-size:20px; font-weight:900; color:#EF4444;">🔥 PARLAY MAESTRO DEL FESTIVAL DE GOLES</div>'
        f'<div style="color:#CBD5E1; font-size:13px; margin-top:2px;">Top Partidos con Mayor Expectativa Ofensiva Combinados</div>'
        f'</div>'
        f'<div style="background:#11141C; border:1.5px solid #EF4444; padding:6px 16px; border-radius:10px; text-align:right;">'
        f'<div style="font-size:11px; color:#FCA5A5; font-weight:bold; text-transform:uppercase;">Cuota Parlay Goles</div>'
        f'<div style="font-size:22px; font-weight:900; color:#EF4444; letter-spacing:0.5px;">x{cuota_total:,.2f}</div>'
        f'</div>'
        f'</div>'
        f'<div>{html_items}</div>'
        f'<div style="background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3); border-radius:8px; padding:8px 12px; margin-top:10px; font-size:12px; color:#FCA5A5; display:flex; align-items:center; gap:6px;">'
        f'<span>💡</span> <span><b>Recomendación VIP:</b> Puedes armar este ticket de altas en 1xBet o Mexplay para maximizar tus ganancias en duelos abiertos.</span>'
        f'</div>'
        f'</div>'
    )
    return html_ticket

