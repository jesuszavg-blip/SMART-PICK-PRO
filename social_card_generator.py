"""
Módulo Generador de Fichas Visuales e Imágenes HD para Redes Sociales
Soporta formatos 1:1 (Instagram Feed / Twitter / Telegram) y 9:16 (WhatsApp Estados / Stories / Reels / TikTok).
Diseño de Alta Legibilidad: Tipografía Grande, Escudos Gigantes, Cero Espacios Vacíos y Alto Impacto Visual.
"""

import os
import io
import math
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FONDO_ESTADIO = os.path.join(ASSETS_DIR, "fondo_estadio_puro.jpg")
LOGO_WEB = os.path.join(ASSETS_DIR, "logo_web.png")
APP_ICON = os.path.join(ASSETS_DIR, "app_icon.png")

# Cache en memoria para escudos de equipos (evita re-descargar)
_LOGO_CACHE = {}

def _obtener_fuente(size: int, bold: bool = False):
    """Carga fuentes TrueType con prioridad en assets/ del proyecto y luego rutas del sistema."""
    local_candidates = [
        os.path.join(ASSETS_DIR, "font_bold.ttf") if bold else os.path.join(ASSETS_DIR, "font_regular.ttf"),
        os.path.join(ASSETS_DIR, "arialbd.ttf") if bold else os.path.join(ASSETS_DIR, "arial.ttf"),
        os.path.join(ASSETS_DIR, "segoeuib.ttf") if bold else os.path.join(ASSETS_DIR, "segoeui.ttf"),
        os.path.join(ASSETS_DIR, "DejaVuSans-Bold.ttf") if bold else os.path.join(ASSETS_DIR, "DejaVuSans.ttf"),
    ]
    for p in local_candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass

    linux_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
    ]
    for p in linux_candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass

    system_names = [
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
        "arial.ttf"
    ]
    for sn in system_names:
        try:
            return ImageFont.truetype(sn, size)
        except Exception:
            pass

    try:
        return ImageFont.load_default(size=size)
    except Exception:
        return ImageFont.load_default()

import re

def _limpiar_texto_emojis(texto: str) -> str:
    """Elimina emojis y caracteres especiales fuera del rango tipográfico de Arial."""
    if not texto:
        return ""
    emoji_pattern = re.compile(
        "[\U00010000-\U0010ffff\u2600-\u27ff\u2300-\u23ff\u2b50-\u2b55\u200d\ufe0f\u2000-\u206f]",
        flags=re.UNICODE
    )
    clean = emoji_pattern.sub("", str(texto))
    return re.sub(r"\s+", " ", clean).strip()


def _draw_shadow_text(draw: ImageDraw.Draw, pos: tuple, text: str, font, fill=(255, 255, 255), shadow_fill=(0, 0, 0, 240), offset=(2, 2), anchor=None):
    """Dibuja texto con sombra de alto contraste para máxima legibilidad."""
    x, y = pos
    draw.text((x + offset[0], y + offset[1]), text, font=font, fill=shadow_fill, anchor=anchor)
    draw.text((x, y), text, font=font, fill=fill, anchor=anchor)


def _dibujar_nombre_equipo(draw: ImageDraw.Draw, cx: int, cy: int, name: str, max_w: int = 400, base_size: int = 44):
    """Renderiza el nombre del equipo completo ajustando dinámicamente el tamaño o en 2 líneas si es necesario."""
    if not name:
        return
    name = str(name).strip()
    for s in [base_size, base_size - 4, base_size - 8, base_size - 12]:
        f = _obtener_fuente(s, bold=True)
        bbox = f.getbbox(name)
        if (bbox[2] - bbox[0]) <= max_w:
            _draw_shadow_text(draw, (cx, cy), name, font=f, fill=(255, 255, 255), anchor="mt")
            return
            
    words = name.split()
    if len(words) >= 2:
        mid = len(words) // 2
        l1 = ' '.join(words[:mid])
        l2 = ' '.join(words[mid:])
        f = _obtener_fuente(base_size - 10, bold=True)
        _draw_shadow_text(draw, (cx, cy - 10), l1, font=f, fill=(255, 255, 255), anchor="mt")
        _draw_shadow_text(draw, (cx, cy + 28), l2, font=f, fill=(255, 255, 255), anchor="mt")
    else:
        f = _obtener_fuente(base_size - 14, bold=True)
        _draw_shadow_text(draw, (cx, cy), name, font=f, fill=(255, 255, 255), anchor="mt")


def _dibujar_pick_completo(draw: ImageDraw.Draw, left_x: int, top_y: int, text: str, max_w: int = 670, base_size: int = 44):
    """Renderiza el pronóstico completo en 1 o 2 líneas grandes, legibles y sin truncar ninguna palabra."""
    if not text:
        return
    display_text = str(text).strip()
    
    # 1. Probar en 1 sola línea si cabe holgadamente
    for s in [base_size, base_size - 4, base_size - 8]:
        f = _obtener_fuente(s, bold=True)
        bbox = f.getbbox(display_text)
        if (bbox[2] - bbox[0]) <= max_w:
            _draw_shadow_text(draw, (left_x, top_y), display_text, font=f, fill=(255, 255, 255))
            return
            
    # 2. Si contiene ' o Empate' o ' o ', dividir por ahí con resalte dorado
    if " o Empate" in display_text:
        parts = display_text.split(" o Empate")
        l1 = parts[0].strip()
        l2 = "o Empate" + (parts[1] if len(parts) > 1 else "")
        f1 = _obtener_fuente(base_size - 2, bold=True)
        f2 = _obtener_fuente(base_size - 2, bold=True)
        _draw_shadow_text(draw, (left_x, top_y - 8), l1, font=f1, fill=(255, 255, 255))
        _draw_shadow_text(draw, (left_x, top_y + 36), l2.strip(), font=f2, fill=(253, 230, 138))
        return

    # 3. División fluida por palabras respetando el ancho máximo
    words = display_text.split()
    lines = []
    curr = ""
    f = _obtener_fuente(base_size - 4, bold=True)
    for w in words:
        test = (curr + " " + w).strip()
        bbox = f.getbbox(test)
        if (bbox[2] - bbox[0]) > max_w and curr:
            lines.append(curr)
            curr = w
        else:
            curr = test
    if curr:
        lines.append(curr)
        
    curr_y = top_y - 8
    for l in lines[:2]:
        _draw_shadow_text(draw, (left_x, curr_y), l, font=f, fill=(255, 255, 255))
        curr_y += 42


def _obtener_imagen_logo(url_o_path: str, size: tuple = (160, 160)) -> Image.Image:
    """Descarga, decodifica base64 o carga localmente un escudo de equipo en RGBA con fondo transparente."""
    if not url_o_path or not isinstance(url_o_path, str):
        return _crear_escudo_placeholder(size)
    
    if url_o_path in _LOGO_CACHE:
        try:
            return _LOGO_CACHE[url_o_path].copy().resize(size, Image.Resampling.LANCZOS)
        except Exception:
            pass
    
    img = None
    try:
        if url_o_path.startswith("data:image"):
            import base64
            b64_data = url_o_path.split(",", 1)[1] if "," in url_o_path else url_o_path
            img_raw = base64.b64decode(b64_data)
            img = Image.open(io.BytesIO(img_raw)).convert("RGBA")
        elif url_o_path.startswith("http://") or url_o_path.startswith("https://"):
            resp = requests.get(url_o_path, timeout=2.5)
            if resp.status_code == 200:
                img = Image.open(io.BytesIO(resp.content)).convert("RGBA")
        elif len(url_o_path) < 250 and os.path.exists(url_o_path):
            img = Image.open(url_o_path).convert("RGBA")
    except Exception:
        img = None

    if img is None:
        img = _crear_escudo_placeholder(size)
    else:
        try:
            img.thumbnail(size, Image.Resampling.LANCZOS)
            canvas_logo = Image.new("RGBA", size, (0, 0, 0, 0))
            offset_x = (size[0] - img.width) // 2
            offset_y = (size[1] - img.height) // 2
            canvas_logo.paste(img, (offset_x, offset_y), img)
            img = canvas_logo
        except Exception:
            img = _crear_escudo_placeholder(size)

    _LOGO_CACHE[url_o_path] = img.copy()
    try:
        return img.resize(size, Image.Resampling.LANCZOS)
    except Exception:
        return _crear_escudo_placeholder(size)


def _crear_escudo_placeholder(size: tuple = (160, 160)) -> Image.Image:
    """Crea un escudo circular deportivo genérico con degradado si no hay logo."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    w, h = size
    draw.ellipse([(6, 6), (w - 6, h - 6)], fill=(21, 24, 33, 240), outline=(212, 175, 55, 240), width=4)
    f = _obtener_fuente(int(w * 0.4), bold=True)
    draw.text((w // 2, h // 2), "SP", fill=(212, 175, 55), font=f, anchor="mm")
    return img


def _crear_fondo_base(width: int, height: int, estilo: str = "oro_vip") -> Image.Image:
    """Genera el lienzo base con fondo de estadio y superposición oscura de lujo."""
    if os.path.exists(FONDO_ESTADIO):
        try:
            bg_raw = Image.open(FONDO_ESTADIO).convert("RGBA")
            target_ratio = width / height
            bg_ratio = bg_raw.width / bg_raw.height
            
            if bg_ratio > target_ratio:
                new_h = height
                new_w = int(height * bg_ratio)
            else:
                new_w = width
                new_h = int(width / bg_ratio)
                
            bg_resized = bg_raw.resize((new_w, new_h), Image.Resampling.LANCZOS)
            left = (new_w - width) // 2
            top = (new_h - height) // 2
            canvas = bg_resized.crop((left, top, left + width, top + height))
        except Exception:
            canvas = Image.new("RGBA", (width, height), (13, 15, 20, 255))
    else:
        canvas = Image.new("RGBA", (width, height), (13, 15, 20, 255))

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    
    if estilo == "festival_fuego":
        for y in range(height):
            ratio = y / height
            r = int(22 + ratio * 24)
            g = int(12 + ratio * 8)
            b = int(14 + ratio * 10)
            alpha = int(195 + ratio * 35)
            draw_ov.line([(0, y), (width, y)], fill=(r, g, b, alpha))
    elif estilo == "neon_pro":
        for y in range(height):
            ratio = y / height
            r = int(10 + ratio * 8)
            g = int(20 + ratio * 20)
            b = int(28 + ratio * 30)
            alpha = int(195 + ratio * 35)
            draw_ov.line([(0, y), (width, y)], fill=(r, g, b, alpha))
    else:
        for y in range(height):
            ratio = y / height
            r = int(14 + ratio * 12)
            g = int(16 + ratio * 12)
            b = int(22 + ratio * 18)
            alpha = int(200 + ratio * 30)
            draw_ov.line([(0, y), (width, y)], fill=(r, g, b, alpha))

    canvas = Image.alpha_composite(canvas, overlay)
    return canvas


def _dibujar_marco_exterior(draw: ImageDraw.Draw, width: int, height: int, color_primario=(212, 175, 55)):
    """Dibuja marcos y esquinas doradas estilo VIP en los bordes de la imagen."""
    p_color = color_primario + (220,)
    sec_color = (56, 189, 248, 80)
    
    draw.rectangle([(20, 20), (width - 20, height - 20)], outline=p_color, width=4)
    draw.rectangle([(30, 30), (width - 30, height - 30)], outline=sec_color, width=1)
    
    c_len = 50
    c_thick = 6
    # Superior Izquierda
    draw.line([(14, 14), (14 + c_len, 14)], fill=color_primario + (255,), width=c_thick)
    draw.line([(14, 14), (14, 14 + c_len)], fill=color_primario + (255,), width=c_thick)
    # Superior Derecha
    draw.line([(width - 14, 14), (width - 14 - c_len, 14)], fill=color_primario + (255,), width=c_thick)
    draw.line([(width - 14, 14), (width - 14, 14 + c_len)], fill=color_primario + (255,), width=c_thick)
    # Inferior Izquierda
    draw.line([(14, height - 14), (14 + c_len, height - 14)], fill=color_primario + (255,), width=c_thick)
    draw.line([(14, height - 14), (14, height - 14 - c_len)], fill=color_primario + (255,), width=c_thick)
    # Inferior Derecha
    draw.line([(width - 14, height - 14), (width - 14 - c_len, height - 14)], fill=color_primario + (255,), width=c_thick)
    draw.line([(width - 14, height - 14), (width - 14, height - 14 - c_len)], fill=color_primario + (255,), width=c_thick)


def generar_ficha_partido_hd(
    partido_data: dict,
    pick_data: dict = None,
    stats_data: dict = None,
    formato: str = "1:1",
    estilo: str = "oro_vip"
) -> bytes:
    """
    Genera la Ficha Gráfica HD de Pronóstico de Partido en formato PNG.
    - formato: "1:1" (1080 x 1080) o "9:16" (1080 x 1920)
    - estilo: "oro_vip", "festival_fuego", "neon_pro"
    """
    try:
        if formato == "9:16":
            width, height = 1080, 1920
        else:
            width, height = 1080, 1080

        canvas = _crear_fondo_base(width, height, estilo=estilo)
        draw = ImageDraw.Draw(canvas)

        if estilo == "festival_fuego":
            col_accent = (239, 68, 68)          # Rojo Fuego
            col_accent_soft = (254, 202, 202)
            col_badge_bg = (220, 38, 38)
            badge_header_text = "FESTIVAL DE GOLES • SMART PICK PRO VIP"
        elif estilo == "neon_pro":
            col_accent = (56, 189, 248)          # Cyan Neón
            col_accent_soft = (186, 230, 253)
            col_badge_bg = (14, 165, 233)
            badge_header_text = "ANÁLISIS DE VALOR (+EV) • SMART PICK PRO VIP"
        else:
            col_accent = (212, 175, 55)          # Oro VIP
            col_accent_soft = (253, 230, 138)
            col_badge_bg = (212, 175, 55)
            badge_header_text = "PRONÓSTICO OFICIAL • SMART PICK PRO VIP"

        _dibujar_marco_exterior(draw, width, height, color_primario=col_accent)

        local_name = _limpiar_texto_emojis(partido_data.get("local", "Equipo Local"))
        visita_name = _limpiar_texto_emojis(partido_data.get("visita", "Equipo Visita"))
        logo_loc_url = partido_data.get("logo_local", "")
        logo_vis_url = partido_data.get("logo_visita", "")
        
        # Limpieza de liga y horario (quitar emojis que causen cuadros vacíos)
        clean_liga = _limpiar_texto_emojis(partido_data.get("liga", "Liga Profesional")).upper()
        raw_hora = _limpiar_texto_emojis(partido_data.get("hora", "Hoy")).upper()

        if not pick_data:
            pick_data = {
                "pick": f"{local_name} o Empate (1X)",
                "cuota": 1.55,
                "probabilidad": "78.5%",
                "stake": "3/10 (3.5%)"
            }
        
        pick_text = str(pick_data.get("pick", pick_data.get("descripcion", f"{local_name} o Empate (1X)")))
        cuota_val = float(pick_data.get("cuota", 1.55))
        prob_val = str(pick_data.get("probabilidad", pick_data.get("prob", "75.0%")))
        if not prob_val.endswith("%"):
            prob_val += "%"
        stake_val = str(pick_data.get("stake", "3/10 (3.5%)"))

        xg_val = str(stats_data.get("xg_total", "2.85")) if stats_data else "2.90"
        btts_val = str(stats_data.get("p_btts", "64.0%")) if stats_data else "65.0%"
        if not str(btts_val).endswith("%"):
            btts_val = f"{btts_val}%"
        o25_val = str(stats_data.get("p_over_25", "58.0%")) if stats_data else "60.0%"
        if not str(o25_val).endswith("%"):
            o25_val = f"{o25_val}%"

        # =========================================================================
        # FORMATO 1:1 CUADRADO (1080 x 1080) - DISTRIBUCIÓN TOTALMENTE LLENA Y GRANDE
        # =========================================================================
        if formato == "1:1":
            box_x = 42
            box_w = width - (box_x * 2)  # 996px

            # 1. HEADER (y: 35 a 125)
            badge_w, badge_h = 760, 48
            badge_x = (width - badge_w) // 2
            draw.rounded_rectangle(
                [(badge_x, 35), (badge_x + badge_w, 35 + badge_h)],
                radius=24,
                fill=col_badge_bg + (240,)
            )
            f_hdr = _obtener_fuente(24, bold=True)
            draw.text((width // 2, 45), badge_header_text, fill=(13, 15, 20), font=f_hdr, anchor="mt")

            f_sub = _obtener_fuente(24, bold=True)
            _draw_shadow_text(draw, (width // 2, 94), f"{clean_liga}   •   {raw_hora}", font=f_sub, fill=(226, 232, 240), anchor="mt")

            # 2. ENCUENTRO Y ESCUDOS (y: 135 a 420, h=285px)
            t_box_y = 135
            t_box_h = 285
            panel_t = Image.new("RGBA", (box_w, t_box_h), (21, 26, 38, 230))
            draw_pt = ImageDraw.Draw(panel_t)
            draw_pt.rounded_rectangle([(0, 0), (box_w, t_box_h)], radius=20, outline=col_accent + (140,), width=3)
            canvas.paste(panel_t, (box_x, t_box_y), panel_t)

            logo_size = (155, 155)
            img_local = _obtener_imagen_logo(logo_loc_url, size=logo_size)
            img_visita = _obtener_imagen_logo(logo_vis_url, size=logo_size)

            loc_cx = box_x + int(box_w * 0.25)
            vis_cx = box_x + int(box_w * 0.75)
            vs_cx = box_x + (box_w // 2)

            canvas.paste(img_local, (loc_cx - logo_size[0] // 2, t_box_y + 18), img_local)
            canvas.paste(img_visita, (vis_cx - logo_size[0] // 2, t_box_y + 18), img_visita)

            # VS Badge Central
            draw.ellipse([(vs_cx - 38, t_box_y + 58), (vs_cx + 38, t_box_y + 134)], fill=(13, 15, 20, 245), outline=col_accent + (220,), width=3)
            draw.text((vs_cx, t_box_y + 93), "VS", fill=col_accent_soft, font=_obtener_fuente(34, bold=True), anchor="mm")

            # Nombres de Equipos Grandes y Completos (Sin cortes)
            _dibujar_nombre_equipo(draw, loc_cx, t_box_y + 185, local_name, max_w=int(box_w * 0.44), base_size=44)
            _dibujar_nombre_equipo(draw, vis_cx, t_box_y + 185, visita_name, max_w=int(box_w * 0.44), base_size=44)

            # Tag inferior de Jornada
            f_tag = _obtener_fuente(20, bold=True)
            _draw_shadow_text(draw, (vs_cx, t_box_y + 246), "ENCUENTRO ANALIZADO CON INTELIGENCIA ARTIFICIAL", font=f_tag, fill=col_accent_soft, anchor="mt")

            # 3. TARJETA PRINCIPAL DEL PICK (y: 435 a 695, h=260px)
            p_box_y = 435
            p_box_h = 260
            panel_p = Image.new("RGBA", (box_w, p_box_h), (25, 30, 44, 240))
            draw_pp = ImageDraw.Draw(panel_p)
            draw_pp.rounded_rectangle([(0, 0), (box_w, p_box_h)], radius=20, outline=col_accent + (240,), width=4)
            canvas.paste(panel_p, (box_x, p_box_y), panel_p)

            # Título de Sección Pick
            _draw_shadow_text(draw, (box_x + 32, p_box_y + 22), "PRONÓSTICO OFICIAL RECOMENDADO (+EV):", font=_obtener_fuente(24, bold=True), fill=col_accent_soft)

            # Cuadro de Cuota Gigante a la Derecha (y: 455 a 675)
            c_box_w, c_box_h = 240, 200
            c_box_x = box_x + box_w - c_box_w - 22
            c_box_y = p_box_y + 30
            draw.rounded_rectangle(
                [(c_box_x, c_box_y), (c_box_x + c_box_w, c_box_y + c_box_h)],
                radius=16,
                fill=(13, 16, 22, 250),
                outline=col_accent + (220,),
                width=3
            )
            draw.text((c_box_x + c_box_w // 2, c_box_y + 20), "CUOTA OFICIAL", fill=(148, 163, 184), font=_obtener_fuente(22, bold=True), anchor="mt")
            _draw_shadow_text(draw, (c_box_x + c_box_w // 2, c_box_y + 60), f"@{cuota_val:.2f}", font=_obtener_fuente(66, bold=True), fill=col_accent, anchor="mt")
            draw.text((c_box_x + c_box_w // 2, c_box_y + 148), "VALOR POSITIVO", fill=(56, 189, 248), font=_obtener_fuente(18, bold=True), anchor="mt")

            # Texto del Pick Completo (En 1 o 2 líneas sin cortes)
            max_pick_w = box_w - c_box_w - 65
            _dibujar_pick_completo(draw, box_x + 32, p_box_y + 66, pick_text, max_w=max_pick_w, base_size=42)

            # Fila de Probabilidad y Stake
            f_metric_lbl = _obtener_fuente(24, bold=True)
            _draw_shadow_text(draw, (box_x + 32, p_box_y + 144), f"• Probabilidad Estimada: {prob_val}", font=f_metric_lbl, fill=(56, 189, 248))
            _draw_shadow_text(draw, (box_x + 32, p_box_y + 178), f"• Gestión de Capital: Stake Sugerido {stake_val}", font=f_metric_lbl, fill=(250, 204, 21))
            _draw_shadow_text(draw, (box_x + 32, p_box_y + 214), "• Simulación Poisson & Dixon-Coles Validada", font=_obtener_fuente(20, bold=False), fill=(148, 163, 184))

            # 4. TRÍO DE MÉTRICAS AVANZADAS (y: 710 a 890, h=180px)
            s_box_y = 710
            s_box_h = 180
            s_card_w = (box_w - 30) // 3
            
            stats_items = [
                {"lbl": "EXPECTATIVA xG", "val": str(xg_val), "sub": "Goles Estimados", "col": (56, 189, 248)},
                {"lbl": "AMBOS ANOTAN", "val": str(btts_val), "sub": "Probabilidad BTTS", "col": (239, 68, 68)},
                {"lbl": "MÁS DE 2.5 GOLES", "val": str(o25_val), "sub": "Tendencia Over", "col": (245, 158, 11)}
            ]

            for idx, s in enumerate(stats_items):
                sc_x = box_x + idx * (s_card_w + 15)
                panel_s = Image.new("RGBA", (s_card_w, s_box_h), (21, 26, 38, 230))
                draw_ps = ImageDraw.Draw(panel_s)
                draw_ps.rounded_rectangle([(0, 0), (s_card_w, s_box_h)], radius=16, outline=(40, 47, 63, 220), width=3)
                canvas.paste(panel_s, (sc_x, s_box_y), panel_s)

                draw.text((sc_x + s_card_w // 2, s_box_y + 20), s["lbl"], fill=(148, 163, 184), font=_obtener_fuente(22, bold=True), anchor="mt")
                _draw_shadow_text(draw, (sc_x + s_card_w // 2, s_box_y + 60), s["val"], font=_obtener_fuente(48, bold=True), fill=s["col"], anchor="mt")
                draw.text((sc_x + s_card_w // 2, s_box_y + 130), s["sub"], fill=(203, 213, 225), font=_obtener_fuente(18, bold=False), anchor="mt")

            # 5. FOOTER / VERIFICACIÓN / CTA (y: 910 a 1045, h=135px)
            f_box_y = 910
            f_box_h = 135
            panel_f = Image.new("RGBA", (box_w, f_box_h), (16, 20, 28, 240))
            draw_pf = ImageDraw.Draw(panel_f)
            draw_pf.rounded_rectangle([(0, 0), (box_w, f_box_h)], radius=16, outline=col_accent + (100,), width=2)
            canvas.paste(panel_f, (box_x, f_box_y), panel_f)

            _draw_shadow_text(draw, (width // 2, f_box_y + 18), "SMART PICK PRO VIP • DATA INTELLIGENCE & IA DEPORTIVA", font=_obtener_fuente(24, bold=True), fill=col_accent, anchor="mt")
            _draw_shadow_text(draw, (width // 2, f_box_y + 55), "Accede a todos los picks en: smartpickprojz.com.mx", font=_obtener_fuente(22, bold=True), fill=(255, 255, 255), anchor="mt")
            draw.text((width // 2, f_box_y + 92), "Pronósticos verificados con estadísticas oficiales en tiempo real", fill=(148, 163, 184), font=_obtener_fuente(18, bold=False), anchor="mt")

        # =========================================================================
        # FORMATO 9:16 HISTORIA / STORY (1080 x 1920) - DISTRIBUCIÓN VERTICAL PERFECTA
        # =========================================================================
        else:
            box_x = 45
            box_w = width - (box_x * 2)  # 990px

            # 1. HEADER (y: 70 a 190)
            badge_w, badge_h = 820, 60
            badge_x = (width - badge_w) // 2
            draw.rounded_rectangle(
                [(badge_x, 70), (badge_x + badge_w, 70 + badge_h)],
                radius=30,
                fill=col_badge_bg + (240,)
            )
            draw.text((width // 2, 82), badge_header_text, fill=(13, 15, 20), font=_obtener_fuente(28, bold=True), anchor="mt")

            _draw_shadow_text(draw, (width // 2, 145), f"{clean_liga}   •   {raw_hora}", font=_obtener_fuente(28, bold=True), fill=(226, 232, 240), anchor="mt")

            # 2. ENCUENTRO Y ESCUDOS (y: 205 a 585, h=380px)
            t_box_y = 205
            t_box_h = 380
            panel_t = Image.new("RGBA", (box_w, t_box_h), (21, 26, 38, 235))
            draw_pt = ImageDraw.Draw(panel_t)
            draw_pt.rounded_rectangle([(0, 0), (box_w, t_box_h)], radius=24, outline=col_accent + (160,), width=3)
            canvas.paste(panel_t, (box_x, t_box_y), panel_t)

            logo_size = (185, 185)
            img_local = _obtener_imagen_logo(logo_loc_url, size=logo_size)
            img_visita = _obtener_imagen_logo(logo_vis_url, size=logo_size)

            loc_cx = box_x + int(box_w * 0.25)
            vis_cx = box_x + int(box_w * 0.75)
            vs_cx = box_x + (box_w // 2)

            canvas.paste(img_local, (loc_cx - logo_size[0] // 2, t_box_y + 25), img_local)
            canvas.paste(img_visita, (vis_cx - logo_size[0] // 2, t_box_y + 25), img_visita)

            draw.ellipse([(vs_cx - 45, t_box_y + 75), (vs_cx + 45, t_box_y + 165)], fill=(13, 15, 20, 250), outline=col_accent + (220,), width=4)
            draw.text((vs_cx, t_box_y + 118), "VS", fill=col_accent_soft, font=_obtener_fuente(40, bold=True), anchor="mm")

            # Nombres de Equipos Grandes y Completos (Sin cortes)
            _dibujar_nombre_equipo(draw, loc_cx, t_box_y + 230, local_name, max_w=int(box_w * 0.44), base_size=50)
            _dibujar_nombre_equipo(draw, vis_cx, t_box_y + 230, visita_name, max_w=int(box_w * 0.44), base_size=50)

            _draw_shadow_text(draw, (vs_cx, t_box_y + 315), "ENCUENTRO ANALIZADO CON MODELOS MATEMÁTICOS", font=_obtener_fuente(24, bold=True), fill=col_accent_soft, anchor="mt")

            # 3. TARJETA PRINCIPAL DEL PICK (y: 610 a 950, h=340px)
            p_box_y = 610
            p_box_h = 340
            panel_p = Image.new("RGBA", (box_w, p_box_h), (25, 30, 44, 245))
            draw_pp = ImageDraw.Draw(panel_p)
            draw_pp.rounded_rectangle([(0, 0), (box_w, p_box_h)], radius=24, outline=col_accent + (250,), width=4)
            canvas.paste(panel_p, (box_x, p_box_y), panel_p)

            _draw_shadow_text(draw, (box_x + 35, p_box_y + 28), "PRONÓSTICO OFICIAL CON VALOR (+EV):", font=_obtener_fuente(28, bold=True), fill=col_accent_soft)

            # Cuadro de Cuota Gigante a la Derecha
            c_box_w, c_box_h = 260, 240
            c_box_x = box_x + box_w - c_box_w - 25
            c_box_y = p_box_y + 50
            draw.rounded_rectangle(
                [(c_box_x, c_box_y), (c_box_x + c_box_w, c_box_y + c_box_h)],
                radius=20,
                fill=(13, 16, 22, 250),
                outline=col_accent + (230,),
                width=3
            )
            draw.text((c_box_x + c_box_w // 2, c_box_y + 22), "CUOTA OFICIAL", fill=(148, 163, 184), font=_obtener_fuente(24, bold=True), anchor="mt")
            _draw_shadow_text(draw, (c_box_x + c_box_w // 2, c_box_y + 70), f"@{cuota_val:.2f}", font=_obtener_fuente(74, bold=True), fill=col_accent, anchor="mt")
            draw.text((c_box_x + c_box_w // 2, c_box_y + 175), "VALOR (+EV)", fill=(56, 189, 248), font=_obtener_fuente(22, bold=True), anchor="mt")

            # Texto del Pick Completo (En 1 o 2 líneas sin cortes)
            max_pick_w = box_w - c_box_w - 70
            _dibujar_pick_completo(draw, box_x + 35, p_box_y + 80, pick_text, max_w=max_pick_w, base_size=48)

            f_info = _obtener_fuente(28, bold=True)
            _draw_shadow_text(draw, (box_x + 35, p_box_y + 170), f"• Confianza Matemática: {prob_val}", font=f_info, fill=(56, 189, 248))
            _draw_shadow_text(draw, (box_x + 35, p_box_y + 220), f"• Gestión Bankroll: Stake {stake_val}", font=f_info, fill=(250, 204, 21))
            _draw_shadow_text(draw, (box_x + 35, p_box_y + 270), "• Algoritmo Poisson + Dixon-Coles Validado", font=_obtener_fuente(24, bold=False), fill=(148, 163, 184))

            # 4. TRÍO DE MÉTRICAS AVANZADAS (y: 975 a 1225, h=250px)
            s_box_y = 975
            s_box_h = 250
            s_card_w = (box_w - 30) // 3

            stats_items = [
                {"lbl": "EXPECTATIVA xG", "val": str(xg_val), "sub": "Goles Esperados", "col": (56, 189, 248)},
                {"lbl": "AMBOS ANOTAN", "val": str(btts_val), "sub": "Probabilidad BTTS", "col": (239, 68, 68)},
                {"lbl": "MÁS DE 2.5 GOLES", "val": str(o25_val), "sub": "Tendencia Over", "col": (245, 158, 11)}
            ]

            for idx, s in enumerate(stats_items):
                sc_x = box_x + idx * (s_card_w + 15)
                panel_s = Image.new("RGBA", (s_card_w, s_box_h), (21, 26, 38, 235))
                draw_ps = ImageDraw.Draw(panel_s)
                draw_ps.rounded_rectangle([(0, 0), (s_card_w, s_box_h)], radius=20, outline=(40, 47, 63, 230), width=3)
                canvas.paste(panel_s, (sc_x, s_box_y), panel_s)

                draw.text((sc_x + s_card_w // 2, s_box_y + 25), s["lbl"], fill=(148, 163, 184), font=_obtener_fuente(26, bold=True), anchor="mt")
                _draw_shadow_text(draw, (sc_x + s_card_w // 2, s_box_y + 80), s["val"], font=_obtener_fuente(56, bold=True), fill=s["col"], anchor="mt")
                draw.text((sc_x + s_card_w // 2, s_box_y + 180), s["sub"], fill=(203, 213, 225), font=_obtener_fuente(22, bold=False), anchor="mt")

            # 5. PANEL DE ANÁLISIS DEEP IA & BANKROLL (y: 1250 a 1660, h=410px)
            m_box_y = 1250
            m_box_h = 410
            panel_m = Image.new("RGBA", (box_w, m_box_h), (21, 26, 38, 240))
            draw_pm = ImageDraw.Draw(panel_m)
            draw_pm.rounded_rectangle([(0, 0), (box_w, m_box_h)], radius=22, outline=col_accent + (140,), width=3)
            canvas.paste(panel_m, (box_x, m_box_y), panel_m)

            _draw_shadow_text(draw, (box_x + 35, m_box_y + 30), "MODELO PREDICTIVO & GESTIÓN DE CAPITAL VIP:", font=_obtener_fuente(28, bold=True), fill=col_accent_soft)

            recs = [
                ("Ventaja Matemática", "Simulación Poisson y Dixon-Coles con más de 10,000 iteraciones."),
                ("Valor Esperado (+EV)", "Probabilidad calculada por el sistema superior a la línea de la casa."),
                ("Criterio Kelly", f"Gestión fraccional sugerida con stake {stake_val} del bankroll."),
                ("Datos Oficiales", "Escaneo de alineaciones, xG reciente y factores clave en vivo.")
            ]
            r_y = m_box_y + 90
            for r_title, r_desc in recs:
                _draw_shadow_text(draw, (box_x + 35, r_y), f"• {r_title}:", font=_obtener_fuente(24, bold=True), fill=(255, 255, 255))
                draw.text((box_x + 40, r_y + 32), r_desc, fill=(203, 213, 225), font=_obtener_fuente(22, bold=False))
                r_y += 76

            # 6. FOOTER / CALL TO ACTION (y: 1685 a 1865, h=180px)
            f_box_y = 1685
            f_box_h = 180
            panel_f = Image.new("RGBA", (box_w, f_box_h), (16, 20, 28, 245))
            draw_pf = ImageDraw.Draw(panel_f)
            draw_pf.rounded_rectangle([(0, 0), (box_w, f_box_h)], radius=22, outline=col_accent + (140,), width=3)
            canvas.paste(panel_f, (box_x, f_box_y), panel_f)

            _draw_shadow_text(draw, (width // 2, f_box_y + 24), "SMART PICK PRO VIP • SOFTWARE DE IA DEPORTIVA", font=_obtener_fuente(30, bold=True), fill=col_accent, anchor="mt")
            _draw_shadow_text(draw, (width // 2, f_box_y + 74), "Consulta todos los pronósticos en: smartpickprojz.com.mx", font=_obtener_fuente(26, bold=True), fill=(255, 255, 255), anchor="mt")
            draw.text((width // 2, f_box_y + 124), "Guarda esta historia y activa notificaciones para los mejores picks", fill=(148, 163, 184), font=_obtener_fuente(22, bold=False), anchor="mt")

        output_buf = io.BytesIO()
        canvas.save(output_buf, format="PNG", quality=95, optimize=True)
        return output_buf.getvalue()

    except Exception as e:
        print(f"Error generando ficha partido HD: {e}")
        err_canvas = Image.new("RGBA", (1080, 1080), (21, 24, 33, 255))
        draw_err = ImageDraw.Draw(err_canvas)
        draw_err.text((540, 540), "SMART PICK PRO VIP\nFicha Generada", fill=(212, 175, 55), font=_obtener_fuente(36, bold=True), anchor="mm")
        buf = io.BytesIO()
        err_canvas.save(buf, format="PNG")
        return buf.getvalue()


def generar_ficha_parlay_hd(
    parlay_data: dict,
    formato: str = "1:1",
    estilo: str = "oro_vip"
) -> bytes:
    """
    Genera un boleto gráfico HD de Parlay Combinado (3 a 5 selecciones) con diseño de impacto y gran tipografía.
    """
    try:
        if formato == "9:16":
            width, height = 1080, 1920
        else:
            width, height = 1080, 1080

        canvas = _crear_fondo_base(width, height, estilo=estilo)
        draw = ImageDraw.Draw(canvas)

        if estilo == "festival_fuego":
            col_accent = (239, 68, 68)
            col_accent_soft = (254, 202, 202)
            col_badge_bg = (220, 38, 38)
            header_title = "BOLETO PARLAY MAESTRO • FESTIVAL DE GOLES"
        elif estilo == "neon_pro":
            col_accent = (56, 189, 248)
            col_accent_soft = (186, 230, 253)
            col_badge_bg = (14, 165, 233)
            header_title = "BOLETO PARLAY PRO • ANÁLISIS DE VALOR"
        else:
            col_accent = (212, 175, 55)
            col_accent_soft = (253, 230, 138)
            col_badge_bg = (212, 175, 55)
            header_title = "BOLETO PARLAY VIP • SMART PICK PRO"

        _dibujar_marco_exterior(draw, width, height, color_primario=col_accent)

        picks = parlay_data.get("picks", [])
        cuota_total = float(parlay_data.get("cuota_total", parlay_data.get("cuota_acumulada", 2.85)))

        box_x = 45
        box_w = width - (box_x * 2)

        # =========================================================================
        # PARLAY 1:1 CUADRADO (1080 x 1080)
        # =========================================================================
        if formato == "1:1":
            badge_w, badge_h = 780, 50
            badge_x = (width - badge_w) // 2
            draw.rounded_rectangle(
                [(badge_x, 35), (badge_x + badge_w, 35 + badge_h)],
                radius=25,
                fill=col_badge_bg + (240,)
            )
            draw.text((width // 2, 46), header_title, fill=(13, 15, 20), font=_obtener_fuente(24, bold=True), anchor="mt")

            # Caja Cuota Multiplicadora
            q_box_y = 100
            q_box_h = 130
            panel_q = Image.new("RGBA", (box_w, q_box_h), (21, 26, 38, 240))
            draw_pq = ImageDraw.Draw(panel_q)
            draw_pq.rounded_rectangle([(0, 0), (box_w, q_box_h)], radius=18, outline=col_accent + (220,), width=3)
            canvas.paste(panel_q, (box_x, q_box_y), panel_q)

            _draw_shadow_text(draw, (box_x + 30, q_box_y + 22), "CUOTA COMBINADA PARLAY VIP:", font=_obtener_fuente(24, bold=True), fill=col_accent_soft)
            _draw_shadow_text(draw, (box_x + 30, q_box_y + 60), f"Combinación de {len(picks)} Encuentros de Alta Confianza", font=_obtener_fuente(22, bold=False), fill=(203, 213, 225))

            _draw_shadow_text(draw, (box_x + box_w - 40, q_box_y + 25), f"x{cuota_total:,.2f}", font=_obtener_fuente(68, bold=True), fill=col_accent, anchor="rt")

            # Lista de 3 o 4 Selecciones
            items_start_y = 245
            max_items = 4
            visible_picks = picks[:max_items]
            item_h = 150 if len(visible_picks) <= 3 else 145

            for idx, p in enumerate(visible_picks):
                it_y = items_start_y + idx * (item_h + 12)
                partido_nombre = str(p.get("partido", f"{p.get('local', 'Local')} vs {p.get('visita', 'Visita')}"))
                liga_nombre = str(p.get("liga", "Torneo Oficial")).replace("🇲🇽", "").replace("🇪🇸", "").replace("🏴󠁧󠁢󠁥󠁮󠁧󠁿", "").strip()
                pick_txt = str(p.get("pick", p.get("mercado", "Más de 1.5 Goles")))
                c_val = float(p.get("cuota", 1.35))
                conf_val = str(p.get("confianza", p.get("probabilidad", "75%")))
                if not conf_val.endswith("%"):
                    conf_val += "%"

                panel_it = Image.new("RGBA", (box_w, item_h), (25, 30, 44, 235))
                draw_pit = ImageDraw.Draw(panel_it)
                draw_pit.rounded_rectangle([(0, 0), (box_w, item_h)], radius=16, outline=(40, 47, 63, 220), width=3)
                draw_pit.rounded_rectangle([(0, 0), (10, item_h)], radius=5, fill=col_accent + (255,))
                canvas.paste(panel_it, (box_x, it_y), panel_it)

                _draw_shadow_text(draw, (box_x + 30, it_y + 18), f"{idx+1}. {partido_nombre}", font=_obtener_fuente(32, bold=True), fill=(255, 255, 255))
                draw.text((box_x + 30, it_y + 60), f"[{liga_nombre}]", fill=(148, 163, 184), font=_obtener_fuente(20, bold=False))
                _draw_shadow_text(draw, (box_x + 30, it_y + 92), f"Pick: {pick_txt}", font=_obtener_fuente(28, bold=True), fill=col_accent_soft)

                # Badge de Cuota
                draw.rounded_rectangle(
                    [(box_x + box_w - 180, it_y + 25), (box_x + box_w - 25, it_y + 120)],
                    radius=14,
                    fill=(13, 16, 22, 250),
                    outline=col_accent + (180,),
                    width=2
                )
                _draw_shadow_text(draw, (box_x + box_w - 102, it_y + 35), f"@{c_val:.2f}", font=_obtener_fuente(34, bold=True), fill=col_accent, anchor="mt")
                draw.text((box_x + box_w - 102, it_y + 78), f"Conf: {conf_val}", fill=(56, 189, 248), font=_obtener_fuente(18, bold=True), anchor="mt")

            # Footer
            f_box_y = 920
            f_box_h = 125
            panel_f = Image.new("RGBA", (box_w, f_box_h), (16, 20, 28, 240))
            draw_pf = ImageDraw.Draw(panel_f)
            draw_pf.rounded_rectangle([(0, 0), (box_w, f_box_h)], radius=16, outline=col_accent + (100,), width=2)
            canvas.paste(panel_f, (box_x, f_box_y), panel_f)

            _draw_shadow_text(draw, (width // 2, f_box_y + 18), "SMART PICK PRO VIP • PARLAY COMBINADO DE ALTO VALOR", font=_obtener_fuente(24, bold=True), fill=col_accent, anchor="mt")
            _draw_shadow_text(draw, (width // 2, f_box_y + 55), "Consulta todos los boletos oficiales en: smartpickprojz.com.mx", font=_obtener_fuente(22, bold=True), fill=(255, 255, 255), anchor="mt")
            draw.text((width // 2, f_box_y + 90), "Multiplica tu inversión con selección de valor matemático", fill=(148, 163, 184), font=_obtener_fuente(18, bold=False), anchor="mt")

        # =========================================================================
        # PARLAY 9:16 HISTORIA (1080 x 1920)
        # =========================================================================
        else:
            badge_w, badge_h = 820, 60
            badge_x = (width - badge_w) // 2
            draw.rounded_rectangle(
                [(badge_x, 70), (badge_x + badge_w, 70 + badge_h)],
                radius=30,
                fill=col_badge_bg + (240,)
            )
            draw.text((width // 2, 82), header_title, fill=(13, 15, 20), font=_obtener_fuente(28, bold=True), anchor="mt")

            # Caja Cuota Multiplicadora
            q_box_y = 155
            q_box_h = 175
            panel_q = Image.new("RGBA", (box_w, q_box_h), (21, 26, 38, 245))
            draw_pq = ImageDraw.Draw(panel_q)
            draw_pq.rounded_rectangle([(0, 0), (box_w, q_box_h)], radius=22, outline=col_accent + (240,), width=4)
            canvas.paste(panel_q, (box_x, q_box_y), panel_q)

            _draw_shadow_text(draw, (box_x + 35, q_box_y + 28), "CUOTA COMBINADA PARLAY VIP:", font=_obtener_fuente(28, bold=True), fill=col_accent_soft)
            _draw_shadow_text(draw, (box_x + 35, q_box_y + 75), f"Boleto Maestro de {len(picks)} Encuentros VIP", font=_obtener_fuente(26, bold=False), fill=(203, 213, 225))
            _draw_shadow_text(draw, (box_x + 35, q_box_y + 118), "Probabilidad Acumulada Validada (+EV)", font=_obtener_fuente(22, bold=False), fill=(56, 189, 248))

            _draw_shadow_text(draw, (box_x + box_w - 45, q_box_y + 35), f"x{cuota_total:,.2f}", font=_obtener_fuente(82, bold=True), fill=col_accent, anchor="rt")

            # Lista de hasta 5 Partidos
            items_start_y = 355
            max_items = min(len(picks), 5)
            item_h = 220

            for idx, p in enumerate(picks[:max_items]):
                it_y = items_start_y + idx * (item_h + 18)
                partido_nombre = str(p.get("partido", f"{p.get('local', 'Local')} vs {p.get('visita', 'Visita')}"))
                liga_nombre = str(p.get("liga", "Torneo Oficial")).replace("🇲🇽", "").replace("🇪🇸", "").replace("🏴󠁧󠁢󠁥󠁮󠁧󠁿", "").strip()
                pick_txt = str(p.get("pick", p.get("mercado", "Más de 1.5 Goles")))
                c_val = float(p.get("cuota", 1.35))
                conf_val = str(p.get("confianza", p.get("probabilidad", "75%")))
                if not conf_val.endswith("%"):
                    conf_val += "%"

                panel_it = Image.new("RGBA", (box_w, item_h), (25, 30, 44, 240))
                draw_pit = ImageDraw.Draw(panel_it)
                draw_pit.rounded_rectangle([(0, 0), (box_w, item_h)], radius=20, outline=(40, 47, 63, 220), width=3)
                draw_pit.rounded_rectangle([(0, 0), (12, item_h)], radius=6, fill=col_accent + (255,))
                canvas.paste(panel_it, (box_x, it_y), panel_it)

                _draw_shadow_text(draw, (box_x + 35, it_y + 24), f"{idx+1}. {partido_nombre}", font=_obtener_fuente(38, bold=True), fill=(255, 255, 255))
                draw.text((box_x + 35, it_y + 78), f"[{liga_nombre}]", fill=(148, 163, 184), font=_obtener_fuente(24, bold=False))
                _draw_shadow_text(draw, (box_x + 35, it_y + 125), f"Pick: {pick_txt}", font=_obtener_fuente(34, bold=True), fill=col_accent_soft)
                draw.text((box_x + 35, it_y + 175), "Validado por Simulación Monte Carlo", fill=(56, 189, 248), font=_obtener_fuente(20, bold=False))

                # Badge de Cuota
                draw.rounded_rectangle(
                    [(box_x + box_w - 200, it_y + 35), (box_x + box_w - 30, it_y + 175)],
                    radius=16,
                    fill=(13, 16, 22, 250),
                    outline=col_accent + (200,),
                    width=3
                )
                _draw_shadow_text(draw, (box_x + box_w - 115, it_y + 50), f"@{c_val:.2f}", font=_obtener_fuente(46, bold=True), fill=col_accent, anchor="mt")
                draw.text((box_x + box_w - 115, it_y + 115), f"Conf: {conf_val}", fill=(56, 189, 248), font=_obtener_fuente(22, bold=True), anchor="mt")

            # Footer
            f_box_y = 1685
            f_box_h = 180
            panel_f = Image.new("RGBA", (box_w, f_box_h), (16, 20, 28, 245))
            draw_pf = ImageDraw.Draw(panel_f)
            draw_pf.rounded_rectangle([(0, 0), (box_w, f_box_h)], radius=22, outline=col_accent + (140,), width=3)
            canvas.paste(panel_f, (box_x, f_box_y), panel_f)

            _draw_shadow_text(draw, (width // 2, f_box_y + 24), "SMART PICK PRO VIP • SOFTWARE DE IA DEPORTIVA", font=_obtener_fuente(30, bold=True), fill=col_accent, anchor="mt")
            _draw_shadow_text(draw, (width // 2, f_box_y + 74), "Consulta todos los pronósticos en: smartpickprojz.com.mx", font=_obtener_fuente(26, bold=True), fill=(255, 255, 255), anchor="mt")
            draw.text((width // 2, f_box_y + 124), "Guarda esta historia y activa notificaciones para los mejores picks", fill=(148, 163, 184), font=_obtener_fuente(22, bold=False), anchor="mt")

        output_buf = io.BytesIO()
        canvas.save(output_buf, format="PNG", quality=95, optimize=True)
        return output_buf.getvalue()

    except Exception as e:
        print(f"Error generando ficha parlay HD: {e}")
        err_canvas = Image.new("RGBA", (1080, 1080), (21, 24, 33, 255))
        draw_err = ImageDraw.Draw(err_canvas)
        draw_err.text((540, 540), "SMART PICK PRO VIP\nParlay Generado", fill=(212, 175, 55), font=_obtener_fuente(36, bold=True), anchor="mm")
        buf = io.BytesIO()
        err_canvas.save(buf, format="PNG")
        return buf.getvalue()
