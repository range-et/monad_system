from PIL import Image, ImageDraw, ImageFont
import math
import os


def _rgb(data, fallback=(0, 0, 0)):
    rgb = data.get("rgb")
    if isinstance(rgb, list) and len(rgb) >= 3:
        return tuple(rgb[:3])
    return fallback


def _draw_texture_pattern(img, x, y, w, h, texture_def, color):
    """Draw a clipped texture pattern into a rectangular region of *img*."""
    tid = texture_def["id"]
    sp = texture_def["spacing"]
    op = texture_def.get("opacity", 0.6)

    # Blend color with opacity against the chip background
    chip_bg = (18, 20, 24)
    r = int(color[0] * op + chip_bg[0] * (1 - op))
    g = int(color[1] * op + chip_bg[1] * (1 - op))
    b = int(color[2] * op + chip_bg[2] * (1 - op))
    fill = (r, g, b)

    # Scale up spacing for visibility in the preview
    sp = max(sp, 6) * 2

    # Draw into a temporary image, then paste (acts as a clip mask)
    tile = Image.new("RGB", (w, h), chip_bg)
    td = ImageDraw.Draw(tile)

    if tid == "dot":
        radius = max(3, int(texture_def.get("radius", 1.5) * 2.5))
        for row in range(int(math.ceil(h / sp)) + 1):
            for col in range(int(math.ceil(w / sp)) + 1):
                cx = int(col * sp + sp / 2)
                cy = int(row * sp + sp / 2)
                td.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=fill)

    elif tid == "hatch-v":
        sw = max(1, texture_def.get("stroke_width", 1) * 2)
        for col in range(int(math.ceil(w / sp)) + 1):
            lx = int(col * sp + sp / 2)
            td.line((lx, 0, lx, h), fill=fill, width=sw)

    elif tid == "hatch-h":
        sw = max(1, texture_def.get("stroke_width", 1) * 2)
        for row in range(int(math.ceil(h / sp)) + 1):
            ly = int(row * sp + sp / 2)
            td.line((0, ly, w, ly), fill=fill, width=sw)

    elif tid == "hatch-x":
        sw = max(1, texture_def.get("stroke_width", 1) * 2)
        for col in range(int(math.ceil(w / sp)) + 1):
            lx = int(col * sp + sp / 2)
            td.line((lx, 0, lx, h), fill=fill, width=sw)
        for row in range(int(math.ceil(h / sp)) + 1):
            ly = int(row * sp + sp / 2)
            td.line((0, ly, w, ly), fill=fill, width=sw)

    elif tid == "hatch-fwd":
        sw = max(1, texture_def.get("stroke_width", 1) * 2)
        diag_range = int(math.ceil((w + h) / sp)) + 2
        for i in range(-diag_range, diag_range):
            x0 = int(i * sp)
            td.line((x0, h, x0 + h, 0), fill=fill, width=sw)

    elif tid == "hatch-bwd":
        sw = max(1, texture_def.get("stroke_width", 1) * 2)
        diag_range = int(math.ceil((w + h) / sp)) + 2
        for i in range(-diag_range, diag_range):
            x0 = int(i * sp)
            td.line((x0, 0, x0 + h, h), fill=fill, width=sw)

    img.paste(tile, (x, y))


def render_palette(data: dict, out_path: str, width: int = 2200, height: int = 2400):
    """Render a high-contrast swatch board for dark/light base layers and semantic tokens."""

    d = data["Default_Colors"]
    g_dark = d["General_UI_Colors"]
    g_light = data["Light_Mode"]["General_UI_Colors"]
    info = d["Information_Indicators"]
    warn = d["Warnings_and_Alerts"]
    hl = d["Highlights_and_Disabled"]
    move = d["Movement_Colors"]
    textures = data.get("Textures", {})

    canvas_bg = (18, 20, 24)
    card_bg = (27, 31, 38)
    label_color = (200, 208, 220)
    img = Image.new("RGB", (width, height), canvas_bg)
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("Helvetica", 52)
        font_head = ImageFont.truetype("Helvetica", 34)
        font_body = ImageFont.truetype("Helvetica", 24)
        font_small = ImageFont.truetype("Helvetica", 20)
    except Exception:
        font_title = ImageFont.load_default()
        font_head = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_small = ImageFont.load_default()

    draw.text((60, 36), "Monad Palette Board", fill=(242, 246, 252), font=font_title)
    draw.text((60, 96), "Dark + Light base layers + semantic roles", fill=(157, 171, 191), font=font_body)

    def draw_chip(x, y, w, h, name, token, color, text_color=(10, 12, 14)):
        draw.rounded_rectangle((x, y, x + w, y + h), radius=8, fill=color)
        draw.text((x + 14, y + 12), name, fill=text_color, font=font_body)
        draw.text((x + 14, y + 42), token, fill=text_color, font=font_small)

    chip_h = 86
    chip_gap = 16
    col_top = 150
    col_title_y = 174
    col_chip_start = 240

    def _col_bottom(token_count):
        chips_height = token_count * chip_h + max(0, token_count - 1) * chip_gap
        return col_chip_start + chips_height + 76

    def draw_column(title, base_x, tokens, text_rgb):
        col_bottom = _col_bottom(len(tokens))
        draw.rounded_rectangle((base_x, col_top, base_x + 980, col_bottom), radius=14, fill=card_bg)
        draw.text((base_x + 26, col_title_y), title, fill=(245, 248, 252), font=font_head)
        y = col_chip_start
        for entry in tokens:
            name, token_name, node = entry
            color = _rgb(node)
            chip_text = (245, 248, 252) if sum(color) < 420 else (20, 26, 34)
            draw_chip(base_x + 26, y, 930, chip_h, name, token_name, color, chip_text)
            y += chip_h + chip_gap

        draw.text((base_x + 26, col_bottom - 58), "Primary text sample", fill=text_rgb, font=font_body)
        draw.text((base_x + 26, col_bottom - 30), "Secondary text sample", fill=_rgb(tokens[5][2]), font=font_body)

        return col_bottom

    dark_tokens = [
        ("Background", "--strata-bg", g_dark["Background"]),
        ("Layer 01", "--strata-layer-01", g_dark["Layer_01"]),
        ("Layer 02", "--strata-layer-02", g_dark["Layer_02"]),
        ("Layer 03", "--strata-layer-03", g_dark["Layer_03"]),
        ("Primary Text", "--strata-text-primary", g_dark["Primary_Text"]),
        ("Secondary Text", "--strata-text-secondary", g_dark["Secondary_Text"]),
        ("Disabled Text", "--strata-text-disabled", g_dark["Disabled_Text"]),
        ("Border", "--strata-border", g_dark["Border"]),
        ("Border Subtle", "--strata-border-subtle", g_dark["Border_Subtle"]),
    ]

    light_tokens = [
        ("Background", "--strata-bg", g_light["Background"]),
        ("Layer 01", "--strata-layer-01", g_light["Layer_01"]),
        ("Layer 02", "--strata-layer-02", g_light["Layer_02"]),
        ("Layer 03", "--strata-layer-03", g_light["Layer_03"]),
        ("Primary Text", "--strata-text-primary", g_light["Primary_Text"]),
        ("Secondary Text", "--strata-text-secondary", g_light["Secondary_Text"]),
        ("Disabled Text", "--strata-text-disabled", g_light["Disabled_Text"]),
        ("Border", "--strata-border", g_light["Border"]),
        ("Border Subtle", "--strata-border-subtle", g_light["Border_Subtle"]),
    ]

    dark_col_bottom = draw_column("Dark Base Layer", 60, dark_tokens, _rgb(g_dark["Primary_Text"]))
    light_col_bottom = draw_column("Light Base Layer", 1140, light_tokens, _rgb(g_light["Primary_Text"]))
    base_section_bottom = max(dark_col_bottom, light_col_bottom)

    semantic_top = base_section_bottom + 36
    semantic_title_y = semantic_top + 24

    semantic_cards_y = semantic_top + 80

    semantic = [
        ("Info", "--strata-info", info["Information_1"]),
        ("Interactive", "--strata-interactive", info["Information_2"]),
        ("Success", "--strata-success", info["Information_3"]),
        ("Warning", "--strata-warning", warn["Warning_1"]),
        ("Error", "--strata-error", warn["Alert_1"]),
        ("Highlight", "--strata-highlight", hl["Highlight"]),
        ("Disabled", "--strata-disabled", hl["Disabled"]),
        ("Move Start", "--strata-move-start", move["Start"]),
        ("Move Hand", "--strata-move-hand", move["Hand"]),
        ("Move Foot", "--strata-move-foot", move["Foot"]),
        ("Move Finish", "--strata-move-finish", move["Finish"]),
    ]

    x = 86
    y = semantic_cards_y
    w = 350
    h = 110
    gap_x = 20
    gap_y = 20
    per_row = 5

    semantic_rows = (len(semantic) + per_row - 1) // per_row
    semantic_bottom = y + semantic_rows * h + max(0, semantic_rows - 1) * gap_y + 48
    draw.rounded_rectangle((60, semantic_top, 2060, semantic_bottom), radius=14, fill=card_bg)
    draw.text((86, semantic_title_y), "Semantic + Domain Colors", fill=(245, 248, 252), font=font_head)

    for i, (name, token_name, node) in enumerate(semantic):
        color = _rgb(node)
        chip_text = (245, 248, 252) if sum(color) < 430 else (20, 26, 34)
        cx = x + (i % per_row) * (w + gap_x)
        cy = y + (i // per_row) * (h + gap_y)
        draw_chip(cx, cy, w, h, name, token_name, color, chip_text)

    draw.text((86, semantic_bottom - 22), "Tip: compare this board against previous render to verify perceptual shifts.", fill=label_color, font=font_small)

    # ── Textures section ──────────────────────────────────────────────────
    if textures:
        texture_top = semantic_bottom + 36
        texture_title_y = texture_top + 24
        texture_chips_y = texture_top + 80

        # Ordered display
        texture_order = ["dot", "hatch_v", "hatch_h", "hatch_x", "hatch_fwd", "hatch_bwd"]
        texture_list = [(k, textures[k]) for k in texture_order if k in textures]

        tex_w = 310
        tex_h = 140
        tex_gap_x = 14
        tex_gap_y = 20
        tex_per_row = 6

        tex_rows = (len(texture_list) + tex_per_row - 1) // tex_per_row
        texture_bottom = texture_chips_y + tex_rows * tex_h + max(0, tex_rows - 1) * tex_gap_y + 48

        # Ensure canvas is tall enough
        if texture_bottom + 40 > height:
            new_height = texture_bottom + 60
            new_img = Image.new("RGB", (width, new_height), canvas_bg)
            new_img.paste(img, (0, 0))
            img = new_img
            draw = ImageDraw.Draw(img)

        draw.rounded_rectangle((60, texture_top, 2060, texture_bottom), radius=14, fill=card_bg)
        draw.text((86, texture_title_y), "Textures", fill=(245, 248, 252), font=font_head)

        # Use interactive color for the pattern strokes
        pattern_color = _rgb(info["Information_2"])

        for i, (key, tdef) in enumerate(texture_list):
            cx = 86 + (i % tex_per_row) * (tex_w + tex_gap_x)
            cy = texture_chips_y + (i // tex_per_row) * (tex_h + tex_gap_y)

            # Draw chip background
            draw.rounded_rectangle((cx, cy, cx + tex_w, cy + tex_h), radius=8, fill=canvas_bg)

            # Draw the pattern into the chip (clipped via temp image)
            _draw_texture_pattern(img, cx + 4, cy + 4, tex_w - 8, tex_h - 36, tdef, pattern_color)

            # Label at bottom of chip
            draw.text((cx + 14, cy + tex_h - 30), tdef["name"], fill=(200, 208, 220), font=font_small)

    img.save(os.path.join(out_path, "rendered_palette.png"), "PNG")