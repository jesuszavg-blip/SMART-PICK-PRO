import html

def render_cancha_tactica(equipo_local: str, equipo_visita: str, form_loc: str, form_vis: str, al_loc: list[str], al_vis: list[str]) -> str:
    """
    Renderiza la Cancha Táctica 2D estilo SofaScore/FotMob (Disposición Vertical 2D Completa).
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

    html_code = f'''
<div style="background: radial-gradient(circle, #2e7d32 0%, #1b4d2e 65%, #0d2e15 100%); border: 3px solid #00E676; border-radius: 16px; padding: 18px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; position: relative; color: white; box-shadow: 0 10px 30px rgba(0,0,0,0.6); overflow: hidden;">
    
    <!-- Líneas del Campo -->
    <div style="position: absolute; top: 50%; left: 10px; right: 10px; height: 2px; background: rgba(255,255,255,0.4); transform: translateY(-50%);"></div>
    <div style="position: absolute; top: 50%; left: 50%; width: 110px; height: 110px; border: 2px solid rgba(255,255,255,0.4); border-radius: 50%; transform: translate(-50%, -50%);"></div>
    
    <!-- Áreas de Meta -->
    <div style="position: absolute; top: 10px; left: 50%; width: 180px; height: 60px; border: 2px solid rgba(255,255,255,0.4); border-top: none; transform: translateX(-50%);"></div>
    <div style="position: absolute; bottom: 10px; left: 50%; width: 180px; height: 60px; border: 2px solid rgba(255,255,255,0.4); border-bottom: none; transform: translateX(-50%);"></div>

    <!-- Encabezado Local (Arriba) -->
    <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(18,20,29,0.92); padding: 8px 16px; border-radius: 12px; border-left: 5px solid #3498db; margin-bottom: 12px; position: relative; z-index: 10;">
        <div style="font-size: 15px; font-weight: 900; color: #ffffff;">🔵 {loc_name}</div>
        <div style="color: #00E676; font-size: 11px; font-weight: bold;">{status_loc}</div>
    </div>

    <!-- MITAD CAMPO LOCAL (TOP) -->
    <div style="height: 250px; display: flex; flex-direction: column; justify-content: space-around; position: relative; z-index: 10; padding: 5px 0;">
        
        <!-- Portero Local -->
        <div style="display: flex; justify-content: center;">
            <div style="text-align: center;">
                <div style="background: #f39c12; color: white; width: 32px; height: 32px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 13px; border: 2px solid white; box-shadow: 0 3px 6px rgba(0,0,0,0.5);">1</div>
                <div style="background: rgba(0,0,0,0.85); color: white; font-size: 10px; font-weight: bold; padding: 2px 6px; border-radius: 8px; margin-top: 2px; white-space: nowrap;">{p_l[0]}</div>
            </div>
        </div>

        <!-- Defensas Local (4) -->
        <div style="display: flex; justify-content: space-around; padding: 0 15px;">
            <div style="text-align: center;"><div style="background: #3498db; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">2</div><div style="background: rgba(0,0,0,0.85); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 70px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{p_l[1]}</div></div>
            <div style="text-align: center;"><div style="background: #3498db; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">4</div><div style="background: rgba(0,0,0,0.85); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 70px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{p_l[2]}</div></div>
            <div style="text-align: center;"><div style="background: #3498db; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">5</div><div style="background: rgba(0,0,0,0.85); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 70px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{p_l[3]}</div></div>
            <div style="text-align: center;"><div style="background: #3498db; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">3</div><div style="background: rgba(0,0,0,0.85); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 70px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{p_l[4]}</div></div>
        </div>

        <!-- Mediocampo Local (3) -->
        <div style="display: flex; justify-content: space-around; padding: 0 40px;">
            <div style="text-align: center;"><div style="background: #3498db; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">6</div><div style="background: rgba(0,0,0,0.85); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{p_l[5]}</div></div>
            <div style="text-align: center;"><div style="background: #3498db; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">8</div><div style="background: rgba(0,0,0,0.85); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{p_l[6]}</div></div>
            <div style="text-align: center;"><div style="background: #3498db; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">10</div><div style="background: rgba(0,0,0,0.85); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{p_l[7]}</div></div>
        </div>

        <!-- Delanteros Local (3) -->
        <div style="display: flex; justify-content: space-around; padding: 0 30px;">
            <div style="text-align: center;"><div style="background: #3498db; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">7</div><div style="background: rgba(0,0,0,0.85); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{p_l[8]}</div></div>
            <div style="text-align: center;"><div style="background: #3498db; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">9</div><div style="background: rgba(0,0,0,0.85); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{p_l[9]}</div></div>
            <div style="text-align: center;"><div style="background: #3498db; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">11</div><div style="background: rgba(0,0,0,0.85); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{p_l[10]}</div></div>
        </div>

    </div>

    <!-- MITAD CAMPO VISITA (BOTTOM) -->
    <div style="height: 250px; display: flex; flex-direction: column; justify-content: space-around; position: relative; z-index: 10; padding: 5px 0; margin-top: 15px;">
        
        <!-- Delanteros Visita (3) -->
        <div style="display: flex; justify-content: space-around; padding: 0 30px;">
            <div style="text-align: center;"><div style="background: #e74c3c; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">7</div><div style="background: rgba(0,0,0,0.85); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{p_v[8]}</div></div>
            <div style="text-align: center;"><div style="background: #e74c3c; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">9</div><div style="background: rgba(0,0,0,0.85); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{p_v[9]}</div></div>
            <div style="text-align: center;"><div style="background: #e74c3c; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">11</div><div style="background: rgba(0,0,0,0.85); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{p_v[10]}</div></div>
        </div>

        <!-- Mediocampo Visita (3) -->
        <div style="display: flex; justify-content: space-around; padding: 0 40px;">
            <div style="text-align: center;"><div style="background: #e74c3c; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">6</div><div style="background: rgba(0,0,0,0.85); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{p_v[5]}</div></div>
            <div style="text-align: center;"><div style="background: #e74c3c; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">8</div><div style="background: rgba(0,0,0,0.85); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{p_v[6]}</div></div>
            <div style="text-align: center;"><div style="background: #e74c3c; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">10</div><div style="background: rgba(0,0,0,0.85); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 75px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{p_v[7]}</div></div>
        </div>

        <!-- Defensas Visita (4) -->
        <div style="display: flex; justify-content: space-around; padding: 0 15px;">
            <div style="text-align: center;"><div style="background: #e74c3c; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">2</div><div style="background: rgba(0,0,0,0.85); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 70px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{p_v[1]}</div></div>
            <div style="text-align: center;"><div style="background: #e74c3c; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">4</div><div style="background: rgba(0,0,0,0.85); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 70px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{p_v[2]}</div></div>
            <div style="text-align: center;"><div style="background: #e74c3c; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">5</div><div style="background: rgba(0,0,0,0.85); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 70px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{p_v[3]}</div></div>
            <div style="text-align: center;"><div style="background: #e74c3c; color: white; width: 28px; height: 28px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; border: 2px solid white;">3</div><div style="background: rgba(0,0,0,0.85); color: white; font-size: 9px; font-weight: bold; padding: 1px 4px; border-radius: 6px; margin-top: 2px; max-width: 70px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{p_v[4]}</div></div>
        </div>

        <!-- Portero Visita -->
        <div style="display: flex; justify-content: center;">
            <div style="text-align: center;">
                <div style="background: #f39c12; color: white; width: 32px; height: 32px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 13px; border: 2px solid white; box-shadow: 0 3px 6px rgba(0,0,0,0.5);">1</div>
                <div style="background: rgba(0,0,0,0.85); color: white; font-size: 10px; font-weight: bold; padding: 2px 6px; border-radius: 8px; margin-top: 2px; white-space: nowrap;">{p_v[0]}</div>
            </div>
        </div>

    </div>

    <!-- Encabezado Visita (Abajo) -->
    <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(18,20,29,0.92); padding: 8px 16px; border-radius: 12px; border-right: 5px solid #e74c3c; margin-top: 12px; position: relative; z-index: 10;">
        <div style="font-size: 15px; font-weight: 900; color: #ffffff;">🔴 {vis_name}</div>
        <div style="color: #00E676; font-size: 11px; font-weight: bold;">{status_vis}</div>
    </div>

</div>'''

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
        status_color = "#E74C3C"
    elif status in ['FT', 'AET', 'PEN']:
        status_label = "🏁 FINALIZADO (90')"
        status_color = "#00E676"
    else:
        status_label = "⏳ PRÓXIMO ENCUENTRO"
        status_color = "#FFD700"

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
                {"min": 0, "icon": "📢", "title": "Inicio del Partido", "player": f"Alineación Oficial de {loc_name}", "detail": "Esquema táctico confirmado"},
                {"min": 15, "icon": "🎯", "title": "Ocasión de Gol", "player": f"{loc_name}", "detail": "Disparo a puerta desviado por el arquero"},
                {"min": 45, "icon": "⏱️", "title": "Entretiempo", "player": "Charla Técnica", "detail": "Ajustes tácticos de medio tiempo"}
            ]
            eventos_visita = [
                {"min": 0, "icon": "📢", "title": "Inicio del Partido", "player": f"Alineación Oficial de {vis_name}", "detail": "Esquema táctico confirmado"},
                {"min": 28, "icon": "🛡️", "title": "Bloqueo Defensivo", "player": f"{vis_name}", "detail": "Corte providencial en zona baja"},
                {"min": 45, "icon": "⏱️", "title": "Entretiempo", "player": "Charla Técnica", "detail": "Reorganización de líneas"}
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
            html_ev_loc += f'<div style="display:flex; align-items:center; justify-content:flex-end; gap:10px; margin-bottom:12px;"><div style="background:#1E2130; border:1px solid #2D3245; border-right:3px solid #00E676; padding:8px 12px; border-radius:8px 2px 2px 8px; text-align:right; max-width:85%;"><div style="font-size:13px; font-weight:800; color:#FFFFFF;">{html.escape(det_str)}</div></div><div style="background:#00E676; color:#0E1117; font-weight:900; font-size:12px; padding:4px 8px; border-radius:50px; min-width:32px; text-align:center; box-shadow:0 0 8px rgba(0,230,118,0.4);">{m_val}\'</div></div>'
        elif isinstance(ev, dict):
            html_ev_loc += f'<div style="display:flex; align-items:center; justify-content:flex-end; gap:10px; margin-bottom:12px;"><div style="background:#1E2130; border:1px solid #2D3245; border-right:3px solid #00E676; padding:8px 12px; border-radius:8px 2px 2px 8px; text-align:right; max-width:85%;"><div style="font-size:13px; font-weight:800; color:#FFFFFF;">{ev.get("icon", "📌")} <b>{html.escape(ev.get("title", ""))}</b></div><div style="font-size:12px; color:#00E676; font-weight:bold;">{html.escape(ev.get("player", ""))}</div><div style="font-size:11px; color:#aaa;">{html.escape(ev.get("detail", ""))}</div></div><div style="background:#00E676; color:#0E1117; font-weight:900; font-size:12px; padding:4px 8px; border-radius:50px; min-width:32px; text-align:center; box-shadow:0 0 8px rgba(0,230,118,0.4);">{ev.get("min", 0)}\'</div></div>'

    # Formatear lista de eventos visita
    html_ev_vis = ""
    for ev in eventos_visita:
        if isinstance(ev, str):
            partes = ev.split(" - ")
            m_str = partes[0] if len(partes) > 0 else "0'"
            det_str = partes[1] if len(partes) > 1 else ev
            ev_icon = "⚽" if "GOL" in det_str else ("🟨" if "Amarilla" in det_str else ("🟥" if "Roja" in det_str else ("🔄" if "Cambio" in det_str else "📌")))
            m_val = m_str.replace("'", "")
            html_ev_vis += f'<div style="display:flex; align-items:center; justify-content:flex-start; gap:10px; margin-bottom:12px;"><div style="background:#E74C3C; color:white; font-weight:900; font-size:12px; padding:4px 8px; border-radius:50px; min-width:32px; text-align:center; box-shadow:0 0 8px rgba(231,76,60,0.4);">{m_val}\'</div><div style="background:#1E2130; border:1px solid #2D3245; border-left:3px solid #E74C3C; padding:8px 12px; border-radius:2px 8px 8px 2px; text-align:left; max-width:85%;"><div style="font-size:13px; font-weight:800; color:#FFFFFF;">{html.escape(det_str)}</div></div></div>'
        elif isinstance(ev, dict):
            html_ev_vis += f'<div style="display:flex; align-items:center; justify-content:flex-start; gap:10px; margin-bottom:12px;"><div style="background:#E74C3C; color:white; font-weight:900; font-size:12px; padding:4px 8px; border-radius:50px; min-width:32px; text-align:center; box-shadow:0 0 8px rgba(231,76,60,0.4);">{ev.get("min", 0)}\'</div><div style="background:#1E2130; border:1px solid #2D3245; border-left:3px solid #E74C3C; padding:8px 12px; border-radius:2px 8px 8px 2px; text-align:left; max-width:85%;"><div style="font-size:13px; font-weight:800; color:#FFFFFF;">{ev.get("icon", "📌")} <b>{html.escape(ev.get("title", ""))}</b></div><div style="font-size:12px; color:#FF7675; font-weight:bold;">{html.escape(ev.get("player", ""))}</div><div style="font-size:11px; color:#aaa;">{html.escape(ev.get("detail", ""))}</div></div></div>'

    pct_tiros_l = int((tiros_local / max(1, tiros_local + tiros_visita)) * 100)
    pct_tiros_v = 100 - pct_tiros_l

    html_full = (
        f'<div style="background: linear-gradient(180deg, #12151E 0%, #0E1117 100%); border: 2px solid #00E676; border-radius: 16px; padding: 20px; color: white; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #2D3245; padding-bottom:14px; margin-bottom:16px;">'
        f'<div style="font-size:18px; font-weight:900; color:#FFD700;">⏱️ CENTRO DE PARTIDO: MINUTO A MINUTO EN VIVO</div>'
        f'<div style="background:{status_color}; color:#0E1117; font-weight:900; padding:5px 14px; border-radius:20px; font-size:13px; letter-spacing:1px;">{status_label}</div>'
        f'</div>'
        f'<div style="display:grid; grid-template-columns: 1fr auto 1fr; align-items:center; gap:15px; margin-bottom:20px; background:#161922; padding:15px; border-radius:12px; border:1px solid #2A2D3E;">'
        f'<div style="display:flex; align-items:center; justify-content:flex-end; gap:12px;"><span style="font-size:17px; font-weight:900; color:#FFFFFF; text-align:right;">{loc_name}</span><img src="{logo_local}" style="width:48px; height:48px; object-fit:contain;"></div>'
        f'<div style="text-align:center; padding:0 15px;"><div style="background:#0E1117; border:2px solid #00E676; padding:6px 20px; border-radius:10px; font-size:28px; font-weight:900; color:#00E676; letter-spacing:4px;">{g_l} - {g_v}</div></div>'
        f'<div style="display:flex; align-items:center; justify-content:flex-start; gap:12px;"><img src="{logo_visita}" style="width:48px; height:48px; object-fit:contain;"><span style="font-size:17px; font-weight:900; color:#FFFFFF; text-align:left;">{vis_name}</span></div>'
        f'</div>'
        f'<div style="background:#161922; padding:14px; border-radius:12px; margin-bottom:20px; border:1px solid #2A2D3E;">'
        f'<div style="font-size:12px; font-weight:800; color:#00E676; text-transform:uppercase; margin-bottom:10px; text-align:center;">📊 ESTADÍSTICAS DEL PARTIDO EN TIEMPO REAL</div>'
        f'<div style="margin-bottom:10px;"><div style="display:flex; justify-content:space-between; font-size:12px; font-weight:bold; margin-bottom:4px;"><span style="color:#00E676;">{pos_local}%</span><span style="color:#aaa;">Posesión de Balón</span><span style="color:#E74C3C;">{pos_visita}%</span></div><div style="display:flex; height:8px; border-radius:4px; overflow:hidden; background:#2D3245;"><div style="width:{pos_local}%; background:#00E676;"></div><div style="width:{pos_visita}%; background:#E74C3C;"></div></div></div>'
        f'<div style="margin-bottom:6px;"><div style="display:flex; justify-content:space-between; font-size:12px; font-weight:bold; margin-bottom:4px;"><span style="color:#00E676;">{tiros_local} Tiros</span><span style="color:#aaa;">Disparos al Arco</span><span style="color:#E74C3C;">{tiros_visita} Tiros</span></div><div style="display:flex; height:8px; border-radius:4px; overflow:hidden; background:#2D3245;"><div style="width:{pct_tiros_l}%; background:#00E676;"></div><div style="width:{pct_tiros_v}%; background:#E74C3C;"></div></div></div>'
        f'</div>'
        f'<div style="display:grid; grid-template-columns: 1fr 2px 1fr; gap:16px; position:relative; margin-top:10px;">'
        f'<div><div style="text-align:right; font-size:14px; font-weight:900; color:#00E676; margin-bottom:12px; border-bottom:2px solid #00E676; padding-bottom:4px;">🔵 ACCIONES {loc_name.upper()}</div>{html_ev_loc}</div>'
        f'<div style="background: linear-gradient(180deg, #00E676 0%, #2D3245 50%, #E74C3C 100%); width:2px; border-radius:2px;"></div>'
        f'<div><div style="text-align:left; font-size:14px; font-weight:900; color:#E74C3C; margin-bottom:12px; border-bottom:2px solid #E74C3C; padding-bottom:4px;">🔴 ACCIONES {vis_name.upper()}</div>{html_ev_vis}</div>'
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
        st_badge = f'<span style="background:rgba(231,76,60,0.2); color:#E74C3C; border:1px solid #E74C3C; padding:3px 10px; border-radius:20px; font-weight:900; font-size:11px; letter-spacing:0.5px;">🔴 {st_val} {min_val}\'</span>'
    elif st_val == 'HT':
        st_badge = '<span style="background:rgba(255,215,0,0.2); color:#FFD700; border:1px solid #FFD700; padding:3px 10px; border-radius:20px; font-weight:900; font-size:11px;">⏸️ ENTRETIEMPO</span>'
    elif st_val in ['FT', 'AET', 'PEN']:
        st_badge = '<span style="background:rgba(0,230,118,0.2); color:#00E676; border:1px solid #00E676; padding:3px 10px; border-radius:20px; font-weight:900; font-size:11px;">🏁 FINAL</span>'
    else:
        st_badge = f'<span style="background:rgba(255,255,255,0.1); color:#aaa; border:1px solid #444; padding:3px 10px; border-radius:20px; font-weight:bold; font-size:11px;">⏳ {st_val}</span>'

    card_html = f'''
    <div style="background:linear-gradient(135deg, #161922 0%, #1E2130 100%); border:1px solid #2D3245; border-radius:14px; padding:14px 18px; margin-bottom:10px; box-shadow:0 4px 15px rgba(0,0,0,0.3);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; border-bottom:1px solid #252836; padding-bottom:6px;">
            <div style="color:#aaa; font-size:11px; font-weight:bold;">📍 {venue}</div>
            <div>{st_badge}</div>
        </div>
        <div style="display:grid; grid-template-columns:1fr auto 1fr; align-items:center; gap:12px; margin-bottom:6px;">
            <div style="display:flex; align-items:center; justify-content:flex-end; gap:10px; text-align:right;">
                <span style="color:#FFFFFF; font-weight:900; font-size:15px; line-height:1.2;">{loc}</span>
                <img src="{logo_l}" style="width:36px; height:36px; object-fit:contain; flex-shrink:0;">
            </div>
            <div style="background:#0E1117; border:1.5px solid #00E676; padding:4px 16px; border-radius:8px; font-size:22px; font-weight:900; color:#00E676; letter-spacing:2px; text-align:center; min-width:70px;">
                {g_l} - {g_v}
            </div>
            <div style="display:flex; align-items:center; justify-content:flex-start; gap:10px; text-align:left;">
                <img src="{logo_v}" style="width:36px; height:36px; object-fit:contain; flex-shrink:0;">
                <span style="color:#FFFFFF; font-weight:900; font-size:15px; line-height:1.2;">{vis}</span>
            </div>
        </div>
    </div>
    '''
    return card_html


def render_ticket_parlay_altas(parlay_data: dict) -> str:
    """
    Renderiza el boleto de Parlay Maestro de Altas en Goles (Top 15) con diseño deportivo VIP.
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
        mercado = html.escape(str(p.get("mercado", "Más de 1.5 Goles")))
        prob = p.get("probabilidad", 75.0)
        cuota = p.get("cuota", 1.30)

        html_items += f'''
        <div style="display:flex; justify-content:space-between; align-items:center; background:#161922; border:1px solid #2D3245; border-left:4px solid #00E676; padding:10px 14px; border-radius:8px; margin-bottom:8px;">
            <div style="flex:1;">
                <div style="color:#aaa; font-size:11px; font-weight:bold;">{idx+1}. {liga}</div>
                <div style="color:#FFFFFF; font-weight:900; font-size:14px; margin-top:2px;">{loc} vs {vis}</div>
            </div>
            <div style="text-align:right; display:flex; align-items:center; gap:10px;">
                <div style="background:rgba(0,230,118,0.15); border:1px solid #00E676; color:#00E676; font-weight:900; padding:4px 10px; border-radius:6px; font-size:13px;">
                    ⚽ {mercado}
                </div>
                <div style="background:#1E2130; border:1px solid #FFD700; color:#FFD700; font-weight:900; padding:4px 10px; border-radius:6px; font-size:13px; min-width:65px; text-align:center;">
                    @{cuota:.2f}
                </div>
                <div style="background:#0E1117; color:#FFFFFF; font-weight:bold; font-size:11px; padding:4px 8px; border-radius:4px; border:1px solid #333;">
                    {prob}%
                </div>
            </div>
        </div>
        '''

    html_ticket = f'''
    <div style="background:linear-gradient(135deg, #12151E 0%, #0E1117 100%); border:2px solid #00E676; border-radius:16px; padding:20px; color:white; margin-bottom:20px; box-shadow:0 8px 25px rgba(0,230,118,0.2);">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #2D3245; padding-bottom:14px; margin-bottom:16px;">
            <div>
                <div style="font-size:20px; font-weight:900; color:#00E676;">🔥 BOLETO PARLAY MAESTRO DE ALTAS</div>
                <div style="color:#aaa; font-size:13px;">Selección de los {total_p} partidos con mayor volumen ofensivo y xG esperado</div>
            </div>
            <div style="text-align:right; background:#161922; border:1.5px solid #FFD700; padding:8px 18px; border-radius:10px;">
                <div style="font-size:11px; color:#FFD700; font-weight:bold; text-transform:uppercase;">Cuota Combinada Total</div>
                <div style="font-size:24px; font-weight:900; color:#00E676; letter-spacing:1px;">x{cuota_tot:,.2f}</div>
            </div>
        </div>
        <div>
            {html_items}
        </div>
    </div>
    '''
    return html_ticket


def render_ticket_empates_oro(empates_data: dict) -> str:
    """
    Renderiza el boleto de Radar de Empates de Oro (Top 5) con diseño deportivo VIP.
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
        prob = e.get("probabilidad_empate", 33.0)
        cuota = e.get("cuota_empate", 3.25)
        marcador = html.escape(str(e.get("marcador_probable", "1 - 1")))
        doble_op = html.escape(str(e.get("doble_oportunidad", "")))

        html_items += f'''
        <div style="background:#161922; border:1px solid #2D3245; border-left:4px solid #FFD700; padding:14px 18px; border-radius:10px; margin-bottom:12px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="color:#aaa; font-size:12px; font-weight:bold;">{idx+1}. {liga}</span>
                <span style="background:rgba(255,215,0,0.15); color:#FFD700; border:1px solid #FFD700; font-weight:900; padding:2px 10px; border-radius:12px; font-size:12px;">⚖️ Paridad Extrema</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span style="color:#FFFFFF; font-weight:900; font-size:16px;">{loc} vs {vis}</span>
                <span style="background:#0E1117; border:2px solid #FFD700; color:#FFD700; font-weight:900; padding:4px 14px; border-radius:8px; font-size:16px;">Cuota @{cuota:.2f}</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; background:#1E2130; padding:8px 12px; border-radius:6px; font-size:12px;">
                <span style="color:#00E676; font-weight:bold;">🎯 Marcador Probable: <b>{marcador}</b> (Prob: {prob}%)</span>
                <span style="color:#ddd;">🛡️ Opción Segura: <b>{doble_op}</b></span>
            </div>
        </div>
        '''

    html_ticket = f'''
    <div style="background:linear-gradient(135deg, #12151E 0%, #0E1117 100%); border:2px solid #FFD700; border-radius:16px; padding:20px; color:white; margin-bottom:20px; box-shadow:0 8px 25px rgba(255,215,0,0.2);">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #2D3245; padding-bottom:14px; margin-bottom:16px;">
            <div>
                <div style="font-size:20px; font-weight:900; color:#FFD700;">⚖️ RADAR DE EMPATES DE ORO (TOP 5 DE ALTO VALOR)</div>
                <div style="color:#aaa; font-size:13px;">5 encuentros de máxima paridad táctica con cuotas superiores a 3.00</div>
            </div>
            <div style="text-align:right; background:#161922; border:1.5px solid #00E676; padding:8px 18px; border-radius:10px;">
                <div style="font-size:11px; color:#00E676; font-weight:bold; text-transform:uppercase;">Cuota Parlay Empates</div>
                <div style="font-size:24px; font-weight:900; color:#FFD700; letter-spacing:1px;">x{cuota_tot:,.2f}</div>
            </div>
        </div>
        <div>
            {html_items}
        </div>
    </div>
    '''
    return html_ticket



