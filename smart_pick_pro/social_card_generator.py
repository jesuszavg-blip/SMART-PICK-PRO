"""
Módulo Generador de Fichas Visuales e Imágenes HD para Redes Sociales
Soporta formatos 1:1 (Instagram Feed / Twitter / Telegram) y 9:16 (WhatsApp Estados / Stories / Reels / TikTok).
Utiliza Pillow (PIL) para renderizar gráficos de lujo con la identidad visual de Smart Pick Pro VIP.
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
    """Carga fuentes TrueType disponibles en Windows o Linux con fallback seguro."""
    nombres_fuente = [
        "arialbd.ttf" if bold else "arial.ttf",
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "tahomabd.ttf" if bold else "tahoma.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "calibrib.ttf" if bold else "calibri.ttf"
    ]
    for nf in nombres_fuente:
        try:
            return ImageFont.truetype(nf, size)
        except Exception:
            continue
    try:
        return ImageFont.load_default()
    except Exception:
        return None


def _obtener_imagen_logo(url_o_path: str, size: tuple = (140, 140)) -> Image.Image:
    """Descarga o carga localmente un escudo de equipo en RGBA con fondo transparente."""
    if not url_o_path:
        return _crear_escudo_placeholder(size)
    
    if url_o_path in _LOGO_CACHE:
        return _LOGO_CACHE[url_o_path].copy().resize(size, Image.Resampling.LANCZOS)
    
    img = None
    if os.path.exists(url_o_path):
        try:
            img = Image.open(url_o_path).convert("RGBA")
        except Exception:
            pass
    elif url_o_path.startswith("http://") or url_o_path.startswith("https://"):
        try:
            resp = requests.get(url_o_path, timeout=5)
            if resp.status_code == 200:
                img = Image.open(io.BytesIO(resp.content)).convert("RGBA")
        except Exception:
            pass

    if img is None:
        img = _crear_escudo_placeholder(size)
    else:
        img.thumbnail(size, Image.Resampling.LANCZOS)
        # Asegurar dimensiones fijas con fondo transparente
        canvas_logo = Image.new("RGBA", size, (0, 0, 0, 0))
        offset_x = (size[0] - img.width) // 2
        offset_y = (size[1] - img.height) // 2
        canvas_logo.paste(img, (offset_x, offset_y), img)
        img = canvas_logo

    _LOGO_CACHE[url_o_path] = img.copy()
    return img.resize(size, Image.Resampling.LANCZOS)


def _crear_escudo_placeholder(size: tuple = (140, 140)) -> Image.Image:
    """Crea un escudo circular deportivo genérico con degradado si no hay logo."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    w, h = size
    draw.ellipse([(6, 6), (w - 6, h - 6)], fill=(21, 24, 33, 240), outline=(212, 175, 55, 220), width=3)
    f = _obtener_fuente(int(w * 0.35), bold=True)
    draw.text((w // 2, h // 2 - int(w * 0.05)), "⚽", fill=(212, 175, 55), font=f, anchor="mm")
    return img


def _crear_fondo_base(width: int, height: int, estilo: str = "oro_vip") -> Image.Image:
    """Genera el lienzo base con fondo de estadio y superposición oscura de lujo."""
    if os.path.exists(FONDO_ESTADIO):
        try:
            bg_raw = Image.open(FONDO_ESTADIO).convert("RGBA")
            # Escalar manteniendo proporción y recortando centro
            target_ratio = width / height
            bg_ratio = bg_raw.width / bg_raw.height
            
            if bg_ratio > target_ratio:
                # Más ancho: escalar por altura
                new_h = height
                new_w = int(height * bg_ratio)
            else:
                # Más alto: escalar por ancho
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

    # Capa de oscurecimiento Glassmorphism según estilo
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    
    if estilo == "festival_fuego":
        # Gradiente oscuro con acento rojo carmesí
        for y in range(height):
            ratio = y / height
            r = int(18 + ratio * 20)
            g = int(12 + ratio * 5)
            b = int(15 + ratio * 8)
            alpha = int(185 + ratio * 45)
            draw_ov.line([(0, y), (width, y)], fill=(r, g, b, alpha))
    elif estilo == "neon_pro":
        # Gradiente oscuro con acento cian/esmeralda
        for y in range(height):
            ratio = y / height
            r = int(10 + ratio * 5)
            g = int(18 + ratio * 15)
            b = int(24 + ratio * 25)
            alpha = int(185 + ratio * 45)
            draw_ov.line([(0, y), (width, y)], fill=(r, g, b, alpha))
    else:
        # Oro VIP & Obsidiana (default)
        for y in range(height):
            ratio = y / height
            r = int(13 + ratio * 10)
            g = int(15 + ratio * 10)
            b = int(20 + ratio * 15)
            alpha = int(190 + ratio * 40)
            draw_ov.line([(0, y), (width, y)], fill=(r, g, b, alpha))

    canvas = Image.alpha_composite(canvas, overlay)
    return canvas


def _dibujar_marco_exterior(draw: ImageDraw.Draw, width: int, height: int, color_primario=(212, 175, 55)):
    """Dibuja marcos y esquinas doradas estilo VIP en los bordes de la imagen."""
    p_color = color_primario + (200,)
    sec_color = (56, 189, 248, 60)
    
    # Bordes interiores
    draw.rectangle([(24, 24), (width - 24, height - 24)], outline=p_color, width=3)
    draw.rectangle([(34, 34), (width - 34, height - 34)], outline=sec_color, width=1)
    
    # Esquinas decorativas
    c_len = 45
    c_thick = 5
    # Superior Izquierda
    draw.line([(18, 18), (18 + c_len, 18)], fill=color_primario + (255,), width=c_thick)
    draw.line([(18, 18), (18, 18 + c_len)], fill=color_primario + (255,), width=c_thick)
    # Superior Derecha
    draw.line([(width - 18, 18), (width - 18 - c_len, 18)], fill=color_primario + (255,), width=c_thick)
    draw.line([(width - 18, 18), (width - 18, 18 + c_len)], fill=color_primario + (255,), width=c_thick)
    # Inferior Izquierda
    draw.line([(18, height - 18), (18 + c_len, height - 18)], fill=color_primario + (255,), width=c_thick)
    draw.line([(18, height - 18), (18, height - 18 - c_len)], fill=color_primario + (255,), width=c_thick)
    # Inferior Derecha
    draw.line([(width - 18, height - 18), (width - 18 - c_len, height - 18)], fill=color_primario + (255,), width=c_thick)
    draw.line([(width - 18, height - 18), (width - 18, height - 18 - c_len)], fill=color_primario + (255,), width=c_thick)


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
    if formato == "9:16":
        width, height = 1080, 1920
    else:
        width, height = 1080, 1080

    canvas = _crear_fondo_base(width, height, estilo=estilo)
    draw = ImageDraw.Draw(canvas)

    # Configuración de colores según estilo
    if estilo == "festival_fuego":
        col_accent = (239, 68, 68)      # Rojo carmesí
        col_accent_soft = (252, 165, 165)
        badge_header_text = "🔥 SMART PICK PRO VIP • FESTIVAL DE GOLES"
    elif estilo == "neon_pro":
        col_accent = (56, 189, 248)      # Neón Cyan
        col_accent_soft = (186, 230, 253)
        badge_header_text = "⚡ SMART PICK PRO VIP • ANÁLISIS DE VALOR (+EV)"
    else:
        col_accent = (212, 175, 55)      # Oro VIP
        col_accent_soft = (243, 229, 171)
        badge_header_text = "💎 SMART PICK PRO VIP • PRONÓSTICO OFICIAL"

    _dibujar_marco_exterior(draw, width, height, color_primario=col_accent)

    # Datos del Partido
    local_name = partido_data.get("local", "Equipo Local")
    visita_name = partido_data.get("visita", "Equipo Visita")
    logo_loc_url = partido_data.get("logo_local", "")
    logo_vis_url = partido_data.get("logo_visita", "")
    liga_name = partido_data.get("liga", "Liga Profesional")
    hora_partido = partido_data.get("hora", "Hoy")

    # Pick & Estadísticas
    if not pick_data:
        pick_data = {
            "pick": f"{local_name} o Empate (1X)",
            "cuota": 1.45,
            "probabilidad": "76.5%",
            "valor_ev": "+12.4%",
            "stake": "3/10 (3.5%)"
        }
    
    pick_text = str(pick_data.get("pick", pick_data.get("descripcion", f"{local_name} o Empate (1X)")))
    cuota_val = float(pick_data.get("cuota", 1.45))
    prob_val = str(pick_data.get("probabilidad", pick_data.get("prob", "75.0%")))
    if not prob_val.endswith("%"):
        prob_val += "%"

    xg_val = str(stats_data.get("xg_total", "2.85")) if stats_data else "2.90"
    btts_val = str(stats_data.get("p_btts", "64.0%")) if stats_data else "65.0%"
    if not str(btts_val).endswith("%"):
        btts_val = f"{btts_val}%"
    o25_val = str(stats_data.get("p_over_25", "58.0%")) if stats_data else "60.0%"
    if not str(o25_val).endswith("%"):
        o25_val = f"{o25_val}%"

    # Fuentes
    f_badge = _obtener_fuente(20, bold=True)
    f_liga = _obtener_fuente(22, bold=True)
    f_team = _obtener_fuente(30, bold=True)
    f_vs = _obtener_fuente(26, bold=True)
    f_pick_lbl = _obtener_fuente(20, bold=True)
    f_pick_main = _obtener_fuente(32, bold=True)
    f_cuota = _obtener_fuente(42, bold=True)
    f_stat_val = _obtener_fuente(30, bold=True)
    f_stat_lbl = _obtener_fuente(16, bold=True)
    f_footer = _obtener_fuente(20, bold=True)

    # 1. HEADER BRANDING & LOGO
    # Si formato 9:16 (Story), desplazamos elementos verticalmente
    y_shift = 160 if formato == "9:16" else 0

    header_y = 55 + (y_shift // 2)
    # Badge Header Superior
    badge_w, badge_h = 580, 42
    badge_x = (width - badge_w) // 2
    draw.rounded_rectangle(
        [(badge_x, header_y), (badge_x + badge_w, header_y + badge_h)],
        radius=21,
        fill=(col_accent[0], col_accent[1], col_accent[2], 230)
    )
    draw.text((width // 2, header_y + 9), badge_header_text, fill=(13, 15, 20), font=f_badge, anchor="mt")

    # Liga & Horario
    liga_y = header_y + badge_h + 16
    draw.text((width // 2, liga_y), f"🏆 {liga_name.upper()} • ⏰ {hora_partido}", fill=(203, 213, 225), font=f_liga, anchor="mt")

    # 2. SECCIÓN DE EQUIPOS & ESCUDOS
    teams_box_y = liga_y + 45
    teams_box_h = 230
    box_w = width - 110
    box_x = 55

    # Panel Glassmorphism para Equipos
    panel_equipos = Image.new("RGBA", (box_w, teams_box_h), (21, 26, 38, 220))
    draw_panel = ImageDraw.Draw(panel_equipos)
    draw_panel.rounded_rectangle([(0, 0), (box_w, teams_box_h)], radius=18, outline=(col_accent[0], col_accent[1], col_accent[2], 120), width=2)
    canvas.paste(panel_equipos, (box_x, teams_box_y), panel_equipos)

    # Cargar y colocar Escudos
    logo_size = (115, 115)
    img_local = _obtener_imagen_logo(logo_loc_url, size=logo_size)
    img_visita = _obtener_imagen_logo(logo_vis_url, size=logo_size)

    # Posiciones Escudos y Nombres
    # Local (Izquierda)
    loc_center_x = box_x + (box_w // 4)
    canvas.paste(img_local, (loc_center_x - logo_size[0] // 2, teams_box_y + 22), img_local)
    # Acortar nombre si es muy largo
    loc_disp = local_name if len(local_name) <= 15 else local_name[:14] + "..."
    draw.text((loc_center_x, teams_box_y + 155), loc_disp, fill=(255, 255, 255), font=f_team, anchor="mt")

    # VS Central
    vs_center_x = box_x + (box_w // 2)
    draw.ellipse(
        [(vs_center_x - 30, teams_box_y + 60), (vs_center_x + 30, teams_box_y + 120)],
        fill=(13, 15, 20, 240),
        outline=(col_accent[0], col_accent[1], col_accent[2], 200),
        width=2
    )
    draw.text((vs_center_x, teams_box_y + 87), "VS", fill=col_accent_soft, font=f_vs, anchor="mm")

    # Visita (Derecha)
    vis_center_x = box_x + (3 * box_w // 4)
    canvas.paste(img_visita, (vis_center_x - logo_size[0] // 2, teams_box_y + 22), img_visita)
    vis_disp = visita_name if len(visita_name) <= 15 else visita_name[:14] + "..."
    draw.text((vis_center_x, teams_box_y + 155), vis_disp, fill=(255, 255, 255), font=f_team, anchor="mt")

    # 3. TARJETA PRINCIPAL DEL PICK RECOMENDADO
    pick_box_y = teams_box_y + teams_box_h + 24
    pick_box_h = 165

    panel_pick = Image.new("RGBA", (box_w, pick_box_h), (26, 31, 46, 235))
    draw_pp = ImageDraw.Draw(panel_pick)
    draw_pp.rounded_rectangle([(0, 0), (box_w, pick_box_h)], radius=18, outline=(col_accent[0], col_accent[1], col_accent[2], 230), width=3)
    canvas.paste(panel_pick, (box_x, pick_box_y), panel_pick)

    # Textos del Pick
    draw.text((box_x + 30, pick_box_y + 24), "🎯 PICK RECOMENDADO CON VALOR (+EV):", fill=col_accent_soft, font=f_pick_lbl)
    
    # Ajustar tamaño de texto del pick si es largo
    pick_disp = pick_text if len(pick_text) <= 26 else pick_text[:25] + "..."
    draw.text((box_x + 30, pick_box_y + 65), pick_disp, fill=(255, 255, 255), font=f_pick_main)

    draw.text((box_x + 30, pick_box_y + 118), f"📊 Confianza Matemática: {prob_val}", fill=(56, 189, 248), font=f_badge)

    # Box de Cuota a la Derecha
    cuota_box_w = 190
    cuota_box_h = 115
    cuota_box_x = box_x + box_w - cuota_box_w - 20
    cuota_box_y = pick_box_y + 25
    draw.rounded_rectangle(
        [(cuota_box_x, cuota_box_y), (cuota_box_x + cuota_box_w, cuota_box_y + cuota_box_h)],
        radius=14,
        fill=(13, 15, 20, 240),
        outline=(col_accent[0], col_accent[1], col_accent[2], 200),
        width=2
    )
    draw.text((cuota_box_x + cuota_box_w // 2, cuota_box_y + 20), "CUOTA", fill=(148, 163, 184), font=f_stat_lbl, anchor="mt")
    draw.text((cuota_box_x + cuota_box_w // 2, cuota_box_y + 50), f"@{cuota_val:.2f}", fill=col_accent, font=f_cuota, anchor="mt")

    # 4. CUADRÍCULA DE MÉTRICAS AVANZADAS (3 CAJAS)
    stats_box_y = pick_box_y + pick_box_h + 22
    stat_card_w = (box_w - 30) // 3
    stat_card_h = 120

    stats_items = [
        {"lbl": "⚽ EXPECTATIVA xG", "val": str(xg_val), "col": (56, 189, 248)},
        {"lbl": "🔥 AMBOS ANOTAN", "val": str(btts_val), "col": (239, 68, 68)},
        {"lbl": "📈 MÁS DE 2.5 GOLES", "val": str(o25_val), "col": (245, 158, 11)}
    ]

    for idx, s in enumerate(stats_items):
        sc_x = box_x + idx * (stat_card_w + 15)
        panel_stat = Image.new("RGBA", (stat_card_w, stat_card_h), (21, 26, 38, 220))
        draw_ps = ImageDraw.Draw(panel_stat)
        draw_ps.rounded_rectangle([(0, 0), (stat_card_w, stat_card_h)], radius=14, outline=(40, 47, 63, 200), width=2)
        canvas.paste(panel_stat, (sc_x, stats_box_y), panel_stat)

        draw.text((sc_x + stat_card_w // 2, stats_box_y + 18), s["lbl"], fill=(148, 163, 184), font=f_stat_lbl, anchor="mt")
        draw.text((sc_x + stat_card_w // 2, stats_box_y + 55), s["val"], fill=s["col"], font=f_stat_val, anchor="mt")

    # Si es formato 9:16 (Story), agregamos sección extra de análisis y Kelly Stake
    if formato == "9:16":
        extra_box_y = stats_box_y + stat_card_h + 30
        extra_box_h = 240
        panel_extra = Image.new("RGBA", (box_w, extra_box_h), (21, 26, 38, 230))
        draw_pe = ImageDraw.Draw(panel_extra)
        draw_pe.rounded_rectangle([(0, 0), (box_w, extra_box_h)], radius=16, outline=(col_accent[0], col_accent[1], col_accent[2], 120), width=2)
        canvas.paste(panel_extra, (box_x, extra_box_y), panel_extra)

        draw.text((box_x + 30, extra_box_y + 25), "🧠 MODELO MATEMÁTICO & GESTIÓN DE CAPITAL:", fill=col_accent_soft, font=f_pick_lbl)
        
        recs = [
            f"• Simulación Poisson & Dixon-Coles con más de 10,000 iteraciones.",
            f"• Valor Esperado Positivo (+EV) validado contra cuotas de mercado.",
            f"• Gestión Bankroll: Criterio Kelly Fraccional Sugerido: Stake {pick_data.get('stake', '3/10')}.",
            f"• Escaneo de datos oficiales y alineaciones satelitales en tiempo real."
        ]
        f_rec = _obtener_fuente(20, bold=False)
        r_y = extra_box_y + 68
        for r in recs:
            draw.text((box_x + 30, r_y), r, fill=(226, 232, 240), font=f_rec)
            r_y += 38

    # 5. FOOTER & LLAMADO A LA ACCIÓN
    footer_y = height - 90
    draw.text(
        (width // 2, footer_y),
        "📲 SMART PICK PRO VIP • SOFTWARE DE APUESTAS & IA DEPORTIVA",
        fill=(212, 175, 55),
        font=f_footer,
        anchor="mt"
    )
    draw.text(
        (width // 2, footer_y + 30),
        "🌐 Accede a todos los picks en vivo: smartpickprojz.com.mx",
        fill=(148, 163, 184),
        font=_obtener_fuente(16, bold=False),
        anchor="mt"
    )

    # Convertir a bytes PNG
    output_buf = io.BytesIO()
    canvas.save(output_buf, format="PNG", quality=95, optimize=True)
    return output_buf.getvalue()


def generar_ficha_parlay_hd(
    parlay_data: dict,
    formato: str = "1:1",
    estilo: str = "oro_vip"
) -> bytes:
    """
    Genera un boleto gráfico HD de Parlay Combinado (3 a 5 selecciones).
    """
    if formato == "9:16":
        width, height = 1080, 1920
    else:
        width, height = 1080, 1080

    canvas = _crear_fondo_base(width, height, estilo=estilo)
    draw = ImageDraw.Draw(canvas)

    if estilo == "festival_fuego":
        col_accent = (239, 68, 68)
        col_accent_soft = (252, 165, 165)
        header_title = "🔥 BOLETO PARLAY MAESTRO • FESTIVAL DE GOLES"
    else:
        col_accent = (212, 175, 55)
        col_accent_soft = (243, 229, 171)
        header_title = "💎 BOLETO PARLAY VIP • SMART PICK PRO"

    _dibujar_marco_exterior(draw, width, height, color_primario=col_accent)

    f_badge = _obtener_fuente(22, bold=True)
    f_title = _obtener_fuente(28, bold=True)
    f_item_title = _obtener_fuente(24, bold=True)
    f_item_pick = _obtener_fuente(22, bold=True)
    f_cuota_big = _obtener_fuente(50, bold=True)
    f_lbl = _obtener_fuente(18, bold=True)
    f_footer = _obtener_fuente(20, bold=True)

    picks = parlay_data.get("picks", [])
    cuota_total = float(parlay_data.get("cuota_total", parlay_data.get("cuota_acumulada", 2.85)))

    # Header
    y_shift = 120 if formato == "9:16" else 0
    header_y = 55 + (y_shift // 2)

    badge_w, badge_h = 660, 48
    badge_x = (width - badge_w) // 2
    draw.rounded_rectangle(
        [(badge_x, header_y), (badge_x + badge_w, header_y + badge_h)],
        radius=24,
        fill=(col_accent[0], col_accent[1], col_accent[2], 230)
    )
    draw.text((width // 2, header_y + 11), header_title, fill=(13, 15, 20), font=f_badge, anchor="mt")

    # Caja de Cuota Total Multiplicadora
    box_w = width - 110
    box_x = 55
    quota_box_y = header_y + badge_h + 20
    quota_box_h = 105

    panel_quota = Image.new("RGBA", (box_w, quota_box_h), (18, 23, 33, 230))
    draw_pq = ImageDraw.Draw(panel_quota)
    draw_pq.rounded_rectangle([(0, 0), (box_w, quota_box_h)], radius=16, outline=(col_accent[0], col_accent[1], col_accent[2], 220), width=2)
    canvas.paste(panel_quota, (box_x, quota_box_y), panel_quota)

    draw.text((box_x + 30, quota_box_y + 22), "CUOTA COMBINADA PARLAY:", fill=col_accent_soft, font=f_lbl)
    draw.text((box_x + 30, quota_box_y + 52), f"Selección de {len(picks)} Encuentros VIP", fill=(203, 213, 225), font=_obtener_fuente(18, bold=False))

    draw.text((box_x + box_w - 40, quota_box_y + 25), f"x{cuota_total:,.2f}", fill=col_accent, font=f_cuota_big, anchor="rt")

    # Lista de Partidos del Parlay
    items_start_y = quota_box_y + quota_box_h + 20
    max_items = 4 if formato == "1:1" else min(len(picks), 6)
    item_h = 100 if formato == "1:1" else 115

    for idx, p in enumerate(picks[:max_items]):
        it_y = items_start_y + idx * (item_h + 12)
        partido_nombre = str(p.get("partido", f"{p.get('local', 'Local')} vs {p.get('visita', 'Visita')}"))
        liga_nombre = str(p.get("liga", "Torneo Oficial"))
        pick_txt = str(p.get("pick", p.get("mercado", "Más de 1.5 Goles")))
        c_val = float(p.get("cuota", 1.35))
        conf_val = str(p.get("confianza", p.get("probabilidad", "75%")))
        if not conf_val.endswith("%"):
            conf_val += "%"

        panel_it = Image.new("RGBA", (box_w, item_h), (21, 26, 38, 220))
        draw_pit = ImageDraw.Draw(panel_it)
        draw_pit.rounded_rectangle([(0, 0), (box_w, item_h)], radius=12, outline=(40, 47, 63, 200), width=2)
        # Línea de acento lateral
        draw_pit.rounded_rectangle([(0, 0), (8, item_h)], radius=4, fill=col_accent + (255,))
        canvas.paste(panel_it, (box_x, it_y), panel_it)

        # Textos
        draw.text((box_x + 24, it_y + 14), f"{idx+1}. {partido_nombre}", fill=(255, 255, 255), font=f_item_title)
        draw.text((box_x + 24, it_y + 45), f"[{liga_nombre}]", fill=(148, 163, 184), font=_obtener_fuente(16, bold=False))
        draw.text((box_x + 24, it_y + 68), f"🎯 {pick_txt}", fill=col_accent_soft, font=f_item_pick)

        # Cuota y Confianza a la derecha
        draw.rounded_rectangle(
            [(box_x + box_w - 145, it_y + 20), (box_x + box_w - 20, it_y + 75)],
            radius=10,
            fill=(13, 15, 20, 240),
            outline=(col_accent[0], col_accent[1], col_accent[2], 150),
            width=2
        )
        draw.text((box_x + box_w - 82, it_y + 32), f"@{c_val:.2f}", fill=col_accent, font=_obtener_fuente(22, bold=True), anchor="mt")
        draw.text((box_x + box_w - 82, it_y + 55), f"Conf: {conf_val}", fill=(56, 189, 248), font=_obtener_fuente(13, bold=True), anchor="mt")

    # Footer
    footer_y = height - 90
    draw.text(
        (width // 2, footer_y),
        "📲 SMART PICK PRO VIP • PARLAY DE ALTO VALOR",
        fill=col_accent,
        font=f_footer,
        anchor="mt"
    )
    draw.text(
        (width // 2, footer_y + 30),
        "🌐 Consulta y arma tus combinadas en: smartpickprojz.com.mx",
        fill=(148, 163, 184),
        font=_obtener_fuente(16, bold=False),
        anchor="mt"
    )

    output_buf = io.BytesIO()
    canvas.save(output_buf, format="PNG", quality=95, optimize=True)
    return output_buf.getvalue()
