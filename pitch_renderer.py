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
