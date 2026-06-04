"""
Sublime Text generator for the Monad System.

Sublime Text uses two distinct JSON file formats:

  1. ``.sublime-color-scheme`` — editor canvas, gutter, syntax tokens.
  2. ``.sublime-theme``        — UI chrome (sidebar, tabs, status bar).
                                 Supports tiled PNG textures on UI surfaces
                                 via the ``layer{0..3}.texture`` property.

This module emits:

    Monad Dark.sublime-color-scheme
    Monad Light.sublime-color-scheme
    Monad.sublime-theme          (dark UI; textured sidebar)
    Monad Light.sublime-theme    (light UI; textured sidebar)
    textures/<id>.png            (tiled patterns reused by the .sublime-theme)

Drop the whole folder into:

    macOS:   ~/Library/Application Support/Sublime Text/Packages/Monad/
    Linux:   ~/.config/sublime-text/Packages/Monad/
    Windows: %APPDATA%/Sublime Text/Packages/Monad/

Then pick from:
    Preferences → Color Scheme → Monad Dark / Monad Light
    Preferences → Theme        → Monad / Monad Light
"""

import io
import json

try:
    from PIL import Image, ImageDraw
    _PIL_OK = True
except ImportError:  # pragma: no cover — Pillow already in requirements.txt
    _PIL_OK = False


# ─── Color scheme ────────────────────────────────────────────────────────────

def _popup_css(p):
    """Minimal CSS for hover-doc popups and the autocomplete detail pane."""
    return (
        f"html {{ background-color: {p['layer01']}; color: {p['text_primary']}; "
        f"padding: 0; margin: 0; }}"
        f"body {{ font-family: system; font-size: 0.95rem; padding: 8px 10px; }}"
        f"a {{ color: {p['interactive']}; text-decoration: none; }}"
        f"h1, h2, h3 {{ color: {p['text_primary']}; "
        f"font-weight: 600; margin: 0 0 4px 0; }}"
        f"code {{ background-color: {p['layer02']}; color: {p['text_primary']}; "
        f"padding: 1px 4px; border-radius: 0; font-family: monospace; }}"
        f"p, ul, ol {{ color: {p['text_secondary']}; margin: 4px 0; }}"
        f".error   {{ color: {p['error']}; }}"
        f".warning {{ color: {p['warning']}; }}"
        f".success {{ color: {p['success']}; }}"
        f".comment {{ color: {p['text_disabled']}; font-style: italic; }}"
    )


def _color_scheme(name, variant, p):
    """
    Build a Sublime Text .sublime-color-scheme dict.

    p is a flat palette dict with keys:
        bg, layer01, layer02, layer03,
        text_primary, text_secondary, text_disabled,
        border, border_subtle,
        interactive, interactive_hover, interactive_active,
        info, success, warning, error, highlight,
        move_start, move_hand, move_foot, move_finish.

    Sublime supports CSS-like color() adjusters — used for translucent washes
    so we don't have to pre-compute alpha hex.
    """
    return {
        "name":   name,
        "author": "Monad System",
        "variant": variant,           # "dark" or "light"
        # popup_css styles hover-doc tooltips and the LSP/auto-complete
        # detail pane. Sublime accepts a small CSS subset here.
        "popup_css": _popup_css(p),
        "variables": {
            "bg":              p["bg"],
            "layer01":         p["layer01"],
            "layer02":         p["layer02"],
            "layer03":         p["layer03"],
            "text_primary":    p["text_primary"],
            "text_secondary":  p["text_secondary"],
            "text_disabled":   p["text_disabled"],
            "border":          p["border"],
            "border_subtle":   p["border_subtle"],
            "interactive":     p["interactive"],
            "interactive_hover":  p["interactive_hover"],
            "interactive_active": p["interactive_active"],
            "info":      p["info"],
            "success":   p["success"],
            "warning":   p["warning"],
            "error":     p["error"],
            "highlight": p["highlight"],
            "move_start":  p["move_start"],
            "move_hand":   p["move_hand"],
            "move_foot":   p["move_foot"],
            "move_finish": p["move_finish"],
        },
        # Editor canvas + gutter + diagnostics
        "globals": {
            "background":                "var(bg)",
            "foreground":                "var(text_primary)",
            "invisibles":                "color(var(text_disabled) alpha(0.4))",
            "caret":                     "var(interactive)",
            "block_caret":               "var(interactive)",
            "line_highlight":            "var(layer01)",
            "misspelling":               "var(error)",
            "fold_marker":               "var(highlight)",
            "minimap_border":            "var(border)",
            "accent":                    "var(interactive)",
            "gutter":                    "var(bg)",
            "gutter_foreground":         "var(text_disabled)",
            "gutter_foreground_highlight": "var(text_primary)",
            "line_diff_added":           "var(success)",
            "line_diff_modified":        "var(interactive)",
            "line_diff_deleted":         "var(error)",
            "selection":                 "color(var(interactive) alpha(0.25))",
            "selection_foreground":      "var(text_primary)",
            "selection_border":          "var(interactive)",
            "selection_border_width":    "0",
            "inactive_selection":        "color(var(interactive) alpha(0.15))",
            "inactive_selection_foreground": "var(text_secondary)",
            "highlight":                 "var(warning)",
            "find_highlight":            "color(var(warning) alpha(0.35))",
            "find_highlight_foreground": "var(text_primary)",
            "guide":                     "var(border_subtle)",
            "active_guide":              "var(interactive)",
            "stack_guide":               "var(border)",
            "shadow":                    "color(black alpha(0.4))",
            "brackets_options":          "underline",
            "brackets_foreground":       "var(interactive)",
            "bracket_contents_options":  "underline",
            "bracket_contents_foreground": "var(interactive)",
            "tags_options":              "stippled_underline",
            "tags_foreground":           "var(interactive)",
        },
        # Syntax rules — TextMate-style scopes
        "rules": [
            {"name": "Comment",
             "scope": "comment, punctuation.definition.comment",
             "foreground": "var(text_disabled)",
             "font_style": "italic"},

            {"name": "String",
             "scope": "string - string.unquoted.heredoc",
             "foreground": "var(success)"},
            {"name": "String — regexp",
             "scope": "string.regexp",
             "foreground": "var(success)"},
            {"name": "String — escape",
             "scope": "constant.character.escape",
             "foreground": "var(info)"},
            {"name": "String — interpolation",
             "scope": "punctuation.section.interpolation, "
                      "meta.interpolation",
             "foreground": "var(info)"},

            {"name": "Number / boolean / constant",
             "scope": "constant.numeric, constant.language",
             "foreground": "var(warning)"},
            {"name": "Constant — user",
             "scope": "constant.other, variable.other.constant",
             "foreground": "var(highlight)"},

            {"name": "Keyword",
             "scope": "keyword, keyword.control, storage, "
                      "storage.type, storage.modifier",
             "foreground": "var(interactive)"},
            {"name": "Keyword — control flow",
             "scope": "keyword.control.flow, keyword.control.return, "
                      "keyword.control.trycatch",
             "foreground": "var(interactive)",
             "font_style": "italic"},
            {"name": "Operator",
             "scope": "keyword.operator",
             "foreground": "var(text_secondary)"},
            {"name": "Logical operator",
             "scope": "keyword.operator.logical, "
                      "keyword.operator.comparison",
             "foreground": "var(interactive)"},

            {"name": "Function definition",
             "scope": "entity.name.function",
             "foreground": "var(info)"},
            {"name": "Function call",
             "scope": "variable.function, meta.function-call",
             "foreground": "var(info)"},
            {"name": "Function parameter",
             "scope": "variable.parameter",
             "foreground": "var(text_secondary)",
             "font_style": "italic"},

            {"name": "Type / class",
             "scope": "entity.name.type, entity.name.class, "
                      "entity.name.struct, entity.name.enum, "
                      "entity.name.interface, entity.name.trait, "
                      "support.type, support.class",
             "foreground": "var(interactive_hover)"},
            {"name": "Inherited class",
             "scope": "entity.other.inherited-class",
             "foreground": "var(interactive_hover)",
             "font_style": "italic"},

            {"name": "Variable",
             "scope": "variable, variable.other",
             "foreground": "var(text_primary)"},
            {"name": "Self / this",
             "scope": "variable.language",
             "foreground": "var(interactive)",
             "font_style": "italic"},
            {"name": "Property",
             "scope": "variable.other.property, support.variable.property",
             "foreground": "var(text_secondary)"},
            {"name": "Attribute / object key",
             "scope": "entity.other.attribute-name, "
                      "meta.object-literal.key, "
                      "support.type.property-name",
             "foreground": "var(info)"},

            {"name": "Punctuation",
             "scope": "punctuation.separator, punctuation.terminator, "
                      "punctuation.accessor",
             "foreground": "var(text_disabled)"},
            {"name": "Brackets",
             "scope": "punctuation.definition.brackets, "
                      "punctuation.section, meta.brace",
             "foreground": "var(text_secondary)"},

            {"name": "Decorator / annotation",
             "scope": "meta.annotation, punctuation.definition.annotation, "
                      "entity.name.function.decorator",
             "foreground": "var(move_finish)"},

            {"name": "Module / namespace",
             "scope": "entity.name.namespace, entity.name.module, "
                      "support.module",
             "foreground": "var(info)"},
            {"name": "Import path",
             "scope": "meta.import string, meta.require string",
             "foreground": "var(success)"},

            # HTML / XML
            {"name": "HTML tag",
             "scope": "entity.name.tag",
             "foreground": "var(interactive)"},
            {"name": "HTML attribute",
             "scope": "entity.other.attribute-name.html",
             "foreground": "var(info)"},
            {"name": "HTML/XML tag punctuation",
             "scope": "punctuation.definition.tag",
             "foreground": "var(border)"},

            # CSS
            {"name": "CSS selector",
             "scope": "entity.name.tag.css, "
                      "entity.other.attribute-name.class.css, "
                      "entity.other.attribute-name.id.css",
             "foreground": "var(interactive)"},
            {"name": "CSS property",
             "scope": "support.type.property-name.css",
             "foreground": "var(info)"},
            {"name": "CSS unit / color",
             "scope": "constant.other.color.rgb-value.css, "
                      "keyword.other.unit.css, constant.numeric.css",
             "foreground": "var(warning)"},
            {"name": "CSS custom property",
             "scope": "variable.css, variable.scss",
             "foreground": "var(highlight)"},
            {"name": "CSS at-rule",
             "scope": "keyword.control.at-rule",
             "foreground": "var(move_finish)"},

            # Markdown
            {"name": "Markdown heading",
             "scope": "markup.heading, "
                      "punctuation.definition.heading",
             "foreground": "var(interactive)",
             "font_style": "bold"},
            {"name": "Markdown bold",
             "scope": "markup.bold",
             "foreground": "var(text_primary)",
             "font_style": "bold"},
            {"name": "Markdown italic",
             "scope": "markup.italic",
             "foreground": "var(text_primary)",
             "font_style": "italic"},
            {"name": "Markdown code",
             "scope": "markup.raw.inline, markup.raw.block",
             "foreground": "var(success)"},
            {"name": "Markdown link text",
             "scope": "markup.underline.link, string.other.link.title",
             "foreground": "var(info)"},
            {"name": "Markdown blockquote",
             "scope": "markup.quote",
             "foreground": "var(text_disabled)",
             "font_style": "italic"},

            # Diff
            {"name": "Diff added",
             "scope": "markup.inserted",
             "foreground": "var(success)"},
            {"name": "Diff removed",
             "scope": "markup.deleted",
             "foreground": "var(error)"},
            {"name": "Diff changed",
             "scope": "markup.changed",
             "foreground": "var(interactive)"},

            # Errors
            {"name": "Invalid",
             "scope": "invalid, invalid.illegal",
             "foreground": "var(error)"},
            {"name": "Deprecated",
             "scope": "invalid.deprecated",
             "foreground": "var(warning)",
             "font_style": "italic"},
        ],
    }


def create_sublime_color_scheme(name, variant, palette):
    """Return the JSON string for a .sublime-color-scheme file."""
    return json.dumps(_color_scheme(name, variant, palette), indent=2)


# ─── UI theme (.sublime-theme) ───────────────────────────────────────────────

def _ui_theme(name, palette, variant="dark", texture_id="dot"):
    """
    Build a .sublime-theme dict applying Monad surface tints + tiled
    textures to Sublime's UI chrome.

    Sublime themes use a layer-stack: layer0 (innermost) → layer3.
    Each layer can have a tint, opacity, texture, and inner_margin.

    ``variant`` ("dark" | "light") controls:
      - the base theme we extend (Adaptive flips icon polarity correctly)
      - the ``dark_content`` flag on sidebar/tab classes, which tells
        Sublime whether built-in icons (close X, expand triangle, file
        type glyphs) should render as light or dark.
    """
    p = palette
    tex_path = f"Monad/textures/{texture_id}.png"
    is_dark  = (variant == "dark")
    # Light icons on dark surfaces, dark icons on light surfaces.
    dark_content = is_dark

    return {
        # Adaptive adapts built-in icon polarity to the active color scheme;
        # we override its colors below but inherit its rule shapes.
        "extends": "Adaptive.sublime-theme",
        "variables": {
            "bg":             p["bg"],
            "layer01":        p["layer01"],
            "layer02":        p["layer02"],
            "layer03":        p["layer03"],
            "text_primary":   p["text_primary"],
            "text_secondary": p["text_secondary"],
            "text_disabled":  p["text_disabled"],
            "border":         p["border"],
            "border_subtle":  p["border_subtle"],
            "interactive":    p["interactive"],
            "success":        p["success"],
            "warning":        p["warning"],
            "error":          p["error"],
        },
        "rules": [
            # ── Sidebar (textured layer behind the tinted base) ──────────
            {
                "class": "sidebar_container",
                "layer0.tint":    "var(layer01)",
                "layer0.opacity": 1.0,
                "layer1.texture": tex_path,
                "layer1.tint":    "var(text_disabled)",
                "layer1.opacity": 0.08,
                "content_margin": [0, 0, 0, 0],
            },
            {
                "class": "sidebar_tree",
                "row_padding":   [8, 4],
                "indent":        12,
                "spacer_rows":   True,
                "dark_content":  dark_content,
            },
            {
                "class": "tree_row",
                "layer0.opacity": 0.0,
            },
            {
                "class": "tree_row", "attributes": ["hover"],
                "layer0.tint":    "var(layer02)",
                "layer0.opacity": 1.0,
            },
            {
                "class": "tree_row", "attributes": ["selected"],
                "layer0.tint":    "var(layer03)",
                "layer0.opacity": 1.0,
            },
            {
                "class": "sidebar_label",
                "color":        "var(text_secondary)",
                "font.size":    12,
            },
            {
                "class": "sidebar_label", "parents": [
                    {"class": "tree_row", "attributes": ["selected"]}
                ],
                "color": "var(text_primary)",
            },
            {
                "class": "sidebar_heading",
                "color":          "var(text_disabled)",
                "font.size":      11,
                "font.bold":      False,
                "case":           "upper",
            },

            # ── Tab bar ──────────────────────────────────────────────────
            {
                "class": "tabset_control",
                "layer0.tint":    "var(layer01)",
                "layer0.opacity": 1.0,
                "tab_height":     30,
                "tab_overlap":    0,
                "tab_min_width":  120,
            },
            {
                "class": "tab_control",
                "layer0.tint":    "var(layer01)",
                "layer0.opacity": 1.0,
                "content_margin": [12, 6, 12, 6],
            },
            {
                "class": "tab_control", "attributes": ["selected"],
                "layer0.tint":    "var(bg)",
                "layer0.opacity": 1.0,
            },
            {
                "class": "tab_control", "attributes": ["hover"],
                "layer0.tint":    "var(layer02)",
                "layer0.opacity": 1.0,
            },
            {
                "class": "tab_label",
                "color":          "var(text_disabled)",
                "font.size":      12,
            },
            {
                "class": "tab_label", "parents": [
                    {"class": "tab_control", "attributes": ["selected"]}
                ],
                "color": "var(text_primary)",
            },

            # ── Status bar ───────────────────────────────────────────────
            {
                "class": "status_bar",
                "layer0.tint":    "var(interactive)",
                "layer0.opacity": 1.0,
                "content_margin": [8, 4, 8, 4],
            },
            {
                "class": "label_control", "parents": [
                    {"class": "status_bar"}
                ],
                "color": "var(bg)",
                "font.size": 11,
            },

            # ── Title bar ────────────────────────────────────────────────
            {
                "class": "title_bar",
                "fg":             "var(text_primary)",
                "bg":             "var(bg)",
            },

            # ── Quick panel / overlay ────────────────────────────────────
            {
                "class": "overlay_control",
                "layer0.tint":    "var(layer01)",
                "layer0.opacity": 1.0,
                "content_margin": [0, 0, 0, 0],
            },
            {
                "class": "quick_panel",
                "row_padding":    [8, 6],
            },
            {
                "class": "quick_panel_row",
                "layer0.opacity": 0.0,
            },
            {
                "class": "quick_panel_row", "attributes": ["selected"],
                "layer0.tint":    "var(layer03)",
                "layer0.opacity": 1.0,
            },
            {
                "class": "quick_panel_label",
                "color":            "var(text_secondary)",
                "fg_blend":         False,
                "match_fg":         "var(interactive)",
                "selected_fg":      "var(text_primary)",
                "selected_match_fg":"var(interactive)",
            },

            # ── Console / output panels ──────────────────────────────────
            {
                "class": "console",
                "layer0.tint":    "var(bg)",
                "layer0.opacity": 1.0,
            },

            # ── Scroll bars ──────────────────────────────────────────────
            {
                "class": "scroll_bar_control",
                "layer0.tint":    "var(bg)",
                "layer0.opacity": 1.0,
            },
            {
                "class": "puck_control",
                "layer0.tint":    "var(border)",
                "layer0.opacity": 1.0,
            },
            {
                "class": "puck_control", "attributes": ["hover"],
                "layer0.tint":    "var(text_disabled)",
                "layer0.opacity": 1.0,
            },

            # ── Find panel ───────────────────────────────────────────────
            {
                "class": "panel_control",
                "layer0.tint":    "var(layer01)",
                "layer0.opacity": 1.0,
                "content_margin": [8, 8, 8, 8],
            },
            {
                "class": "text_line_control",
                "layer0.tint":    "var(layer02)",
                "layer0.opacity": 1.0,
                "content_margin": [6, 4, 6, 4],
            },

            # ── Buttons ──────────────────────────────────────────────────
            {
                "class": "icon_button_control",
                "layer0.tint":    "var(layer02)",
                "layer0.opacity": 1.0,
                "content_margin": [6, 4],
            },
            {
                "class": "icon_button_control", "attributes": ["hover"],
                "layer0.tint":    "var(layer03)",
            },
            {
                "class": "icon_button_control", "attributes": ["pressed"],
                "layer0.tint":    "var(interactive)",
            },

            # ── Sheet container (frame around editor sheets) ─────────────
            {
                "class": "sheet_container_control",
                "layer0.tint":    "var(bg)",
                "layer0.opacity": 1.0,
            },

            # ── Mini-map ─────────────────────────────────────────────────
            {
                "class": "mini_map_control",
                "viewport_color":           "color(var(interactive) alpha(0.30))",
                "viewport_outline_color":   "color(var(interactive) alpha(0.50))",
            },

            # ── Auto-complete popup ──────────────────────────────────────
            {
                "class": "auto_complete",
                "layer0.tint":    "var(layer01)",
                "layer0.opacity": 1.0,
                "row_padding":    [10, 6],
                "tint_index":     0,
                "dark_content":   dark_content,
            },
            {
                "class": "auto_complete_label",
                "fg":               "var(text_secondary)",
                "match_fg":         "var(interactive)",
                "selected_fg":      "var(text_primary)",
                "selected_match_fg":"var(interactive)",
            },
            {
                "class": "auto_complete_detail_pane",
                "layer0.tint":    "var(layer02)",
                "layer0.opacity": 1.0,
            },
            {
                "class": "auto_complete_info_label",
                "fg":             "var(text_disabled)",
            },
            {
                "class": "auto_complete_info_key",
                "fg":             "var(text_disabled)",
            },
            {
                "class": "auto_complete_info_value",
                "fg":             "var(text_secondary)",
            },
            {
                "class": "auto_complete_hint",
                "color":          "var(text_disabled)",
                "font.italic":    True,
            },

            # ── Kind-icon badges (autocomplete left rail) ────────────────
            #   The "kind" badges are the colored letter chips next to each
            #   completion item. Tinted via interactive/info/success/etc.
            {
                "class": "kind_container_control",
                "layer0.opacity": 1.0,
                "content_margin": [3, 0, 3, 0],
            },
            {"class": "kind_label_control",
             "color": "var(bg)", "font.bold": True},

            {"class": "kind_function_control",
             "layer0.tint": "var(interactive)", "layer0.opacity": 1.0},
            {"class": "kind_keyword_control",
             "layer0.tint": "var(interactive)", "layer0.opacity": 1.0},
            {"class": "kind_namespace_control",
             "layer0.tint": "var(info)", "layer0.opacity": 1.0},
            {"class": "kind_navigation_control",
             "layer0.tint": "var(info)", "layer0.opacity": 1.0},
            {"class": "kind_markup_control",
             "layer0.tint": "var(success)", "layer0.opacity": 1.0},
            {"class": "kind_snippet_control",
             "layer0.tint": "var(success)", "layer0.opacity": 1.0},
            {"class": "kind_type_control",
             "layer0.tint": "var(warning)", "layer0.opacity": 1.0},
            {"class": "kind_variable_control",
             "layer0.tint": "var(text_secondary)", "layer0.opacity": 1.0},
            {"class": "kind_ambiguous_control",
             "layer0.tint": "var(text_disabled)", "layer0.opacity": 1.0},

            # ── Tooltips / hover popups ──────────────────────────────────
            #   popup_control is the window; its inner HTML is styled by
            #   the color scheme's popup_css.
            {
                "class": "popup_control",
                "layer0.tint":    "var(layer01)",
                "layer0.opacity": 1.0,
                "content_margin": [1, 1, 1, 1],
            },

            # ── Menu (File/Edit/… on Windows + Linux; macOS uses native) ─
            {
                "class": "menu",
                "layer0.tint":    "var(layer01)",
                "layer0.opacity": 1.0,
            },
            {
                "class": "label_control", "parents": [{"class": "menu"}],
                "color":          "var(text_primary)",
            },
        ],
    }


def create_sublime_ui_theme(name, palette, variant="dark", texture_id="dot"):
    """Return the JSON string for a .sublime-theme file."""
    return json.dumps(_ui_theme(name, palette, variant, texture_id), indent=2)


# ─── Texture PNG generation ──────────────────────────────────────────────────

def create_sublime_texture_png(texture_def):
    """
    Render a single tiled texture as PNG bytes from a Texture entry in
    colors.json. Sublime tiles the PNG across the target surface, and
    the .sublime-theme applies tint + opacity on top, so the source PNG
    is monochrome black-on-transparent.
    """
    if not _PIL_OK:
        raise RuntimeError("Pillow is required to render Sublime textures")

    tid     = texture_def["id"]
    spacing = int(round(texture_def.get("spacing", 12)))
    opacity = float(texture_def.get("opacity", 0.6))
    alpha   = max(0, min(255, int(round(opacity * 255))))
    sw      = max(1, int(round(texture_def.get("stroke_width", 1))))

    img  = Image.new("RGBA", (spacing, spacing), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    ink  = (0, 0, 0, alpha)

    if tid == "dot":
        r = texture_def.get("radius", 1.5)
        cx = cy = spacing / 2
        draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            fill=ink,
        )

    elif tid == "hatch-v":
        x = spacing // 2
        draw.line([(x, 0), (x, spacing)], fill=ink, width=sw)

    elif tid == "hatch-h":
        y = spacing // 2
        draw.line([(0, y), (spacing, y)], fill=ink, width=sw)

    elif tid == "hatch-x":
        x = spacing // 2
        y = spacing // 2
        draw.line([(x, 0), (x, spacing)], fill=ink, width=sw)
        draw.line([(0, y), (spacing, y)], fill=ink, width=sw)

    elif tid == "hatch-fwd":
        # forward diagonal /  — also draw wrap-around copies for seamless tile
        draw.line([(-1, spacing + 1), (spacing + 1, -1)], fill=ink, width=sw)
        draw.line([(spacing - 1, spacing + 1), (spacing * 2 + 1, -1)],
                  fill=ink, width=sw)

    elif tid == "hatch-bwd":
        # backward diagonal \
        draw.line([(-1, -1), (spacing + 1, spacing + 1)], fill=ink, width=sw)
        draw.line([(-spacing - 1, -1), (1, spacing + 1)], fill=ink, width=sw)

    else:
        # unknown texture id — fall back to a single centred dot
        cx = cy = spacing / 2
        draw.ellipse([cx - 1, cy - 1, cx + 1, cy + 1], fill=ink)

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


# ─── Palette builders ────────────────────────────────────────────────────────

def build_sublime_palette(
    bg, layer01, layer02, layer03,
    text_primary, text_secondary, text_disabled,
    border, border_subtle,
    interactive, interactive_hover, interactive_active,
    info, success, warning, error, highlight,
    move_start, move_hand, move_foot, move_finish,
):
    """Assemble the flat palette dict consumed by _color_scheme / _ui_theme."""
    return {
        "bg":              bg,
        "layer01":         layer01,
        "layer02":         layer02,
        "layer03":         layer03,
        "text_primary":    text_primary,
        "text_secondary":  text_secondary,
        "text_disabled":   text_disabled,
        "border":          border,
        "border_subtle":   border_subtle,
        "interactive":          interactive,
        "interactive_hover":    interactive_hover,
        "interactive_active":   interactive_active,
        "info":      info,
        "success":   success,
        "warning":   warning,
        "error":     error,
        "highlight": highlight,
        "move_start":  move_start,
        "move_hand":   move_hand,
        "move_foot":   move_foot,
        "move_finish": move_finish,
    }


# ─── README ──────────────────────────────────────────────────────────────────

def create_sublime_readme():
    """Return the markdown installation guide for the Sublime package."""
    return """\
# Monad System — Sublime Text

Color schemes **and** UI theme generated from `colors.json`.

| File | What it skins |
|---|---|
| `Monad Dark.sublime-color-scheme`  | Editor canvas, gutter, syntax (dark)  |
| `Monad Light.sublime-color-scheme` | Editor canvas, gutter, syntax (light) |
| `Monad.sublime-theme`              | Sidebar, tabs, status bar (dark UI)   |
| `Monad Light.sublime-theme`        | Sidebar, tabs, status bar (light UI)  |
| `textures/*.png`                   | Tiled patterns layered on the sidebar |

> **Color scheme** ≠ **Theme.** Sublime separates editor colors from window chrome.
> You set them independently. Both ship here so the editor and the surrounding UI
> stay coherent.

---

## Install

Copy this whole folder into Sublime's `Packages/` directory as a folder named
`Monad`:

```
macOS    ~/Library/Application Support/Sublime Text/Packages/Monad/
Linux    ~/.config/sublime-text/Packages/Monad/
Windows  %APPDATA%\\Sublime Text\\Packages\\Monad\\
```

The fastest way:

```
Sublime Text → Preferences → Browse Packages…
```

Drop the `Monad` folder in there. Sublime hot-reloads — no restart needed.

---

## Activate

**Color scheme** (editor):

```
Preferences → Color Scheme → Monad → Monad Dark   (or Monad Light)
```

**Theme** (UI chrome):

```
Preferences → Theme → Monad → Monad.sublime-theme   (or Monad Light)
```

Or edit `Preferences.sublime-settings` directly:

```json
{
    "color_scheme": "Packages/Monad/Monad Dark.sublime-color-scheme",
    "theme":        "Monad.sublime-theme"
}
```

---

## Textures

Sublime UI themes can layer tiled PNG textures onto any panel via
`layer{0..3}.texture`. The default sidebar in this theme uses `dot.png` at
~8 % opacity tinted with `text_disabled` — a quiet stipple that breaks up
flat surfaces without competing with code.

To swap textures, edit `Monad.sublime-theme` and change:

```json
"layer1.texture": "Monad/textures/dot.png"
```

to any of the available textures:

```
textures/dot.png
textures/hatch-v.png
textures/hatch-h.png
textures/hatch-x.png
textures/hatch-fwd.png
textures/hatch-bwd.png
```

Or remove the `layer1.*` block entirely for a flat sidebar.

---

## Font

**Sublime themes cannot set the font.** Font face and size live in the
user's `Preferences.sublime-settings`:

```
Sublime Text → Preferences → Settings
```

Add to the **right-hand pane** (user overrides):

```json
{
    "font_face": "JetBrains Mono",
    "font_size": 13,
    "line_padding_top":    2,
    "line_padding_bottom": 2
}
```

Pick any monospace face you have installed. The Monad System uses a mono
for code and data; matching it here keeps the rendered output consistent
with the rest of the system.

---

## Customising syntax highlighting

Sublime maps **TextMate scopes** → colors. To change which color a token
type gets:

1. Put your caret on the token you want to recolor.
2. Run `Tools → Developer → Show Scope Name`
   (macOS `Ctrl+Shift+P`, Win/Linux `Ctrl+Alt+Shift+P`).
3. A popup shows the full scope stack — e.g. `source.python meta.function.python
   entity.name.function.python`. Copy the most specific selector you want
   to target.
4. Create `Packages/User/Monad Dark.sublime-color-scheme` (same filename,
   under `User/`) — Sublime auto-merges your overrides on top of ours:

   ```json
   {
       "rules": [
           {
               "name":       "Python function name — magenta",
               "scope":      "entity.name.function.python",
               "foreground": "#FF00AA",
               "font_style": "bold"
           }
       ]
   }
   ```

Editing the generated `Packages/Monad/Monad Dark.sublime-color-scheme`
directly works too, but your edits get clobbered on the next `make`.
The `User/` override file is the safe place.

### Adding entirely new tokens

The same workflow works for languages we don't cover yet — just add more
entries to `rules`. Sublime live-reloads color schemes; you'll see the
change as soon as you save.

---

## Rebuild from source

This package is generated. Edit `colors.json` and rebuild:

```bash
make
```

Outputs land in `build/themes/sublime/` — copy them back into `Packages/Monad/`.
"""
