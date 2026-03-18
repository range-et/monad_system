import json
import os
import argparse

from templates.c_sharp_template import create_csharp_template
from templates.css_template import create_css_template, create_monad_system
from templates.python_template import create_python_template
from templates.js_template import create_js_template
from templates.vscode_template import (
    build_dark_palette as vsc_dark_palette,
    build_light_palette as vsc_light_palette,
    create_vscode_dark_theme,
    create_vscode_light_theme,
    create_vscode_package_json,
    create_vscode_readme,
    create_vscode_license,
)
from templates.ghostty_template import (
    create_ghostty_dark_theme,
    create_ghostty_light_theme,
)


def load_json(json_path):
    with open(json_path, "r") as file:
        data = json.load(file)
    return data


# ─── Color math helpers ───────────────────────────────────────────────────────

def _darken(hex_color, factor=0.85):
    """Multiply each RGB channel by factor to darken or brighten. Clamped 0-255."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = min(255, max(0, int(r * factor)))
    g = min(255, max(0, int(g * factor)))
    b = min(255, max(0, int(b * factor)))
    return f"#{r:02X}{g:02X}{b:02X}"


def _blend(hex_fg, hex_bg, fg_opacity=0.3):
    """
    Blend hex_fg over hex_bg at fg_opacity — returns a solid 6-digit hex.
    Replaces alpha-suffix colors (#RRGGBBAA) for environments that don't
    support transparency in color values (e.g. Ghostty selection-background).
    """
    fh = hex_fg.lstrip("#")
    bh = hex_bg.lstrip("#")
    fr, fg, fb = int(fh[0:2], 16), int(fh[2:4], 16), int(fh[4:6], 16)
    br, bg_, bb = int(bh[0:2], 16), int(bh[2:4], 16), int(bh[4:6], 16)
    r = min(255, int(fr * fg_opacity + br * (1 - fg_opacity)))
    g = min(255, int(fg * fg_opacity + bg_ * (1 - fg_opacity)))
    b = min(255, int(fb * fg_opacity + bb * (1 - fg_opacity)))
    return f"#{r:02X}{g:02X}{b:02X}"


def _shift_bg(hex_color, amount=30):
    """Add amount to each channel to derive a lighter dark-mode surface."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = min(255, r + amount)
    g = min(255, g + amount)
    b = min(255, b + amount)
    return f"#{r:02X}{g:02X}{b:02X}"


def prepare_templates(json_data):
    d = json_data.get("Default_Colors", {})
    lm = json_data.get("Light_Mode", {}).get("General_UI_Colors", {})

    # Dark theme values from Default_Colors
    background_color = d.get("General_UI_Colors", {}).get("Background", {}).get("hex", "#121212")
    primary_text_color = d.get("General_UI_Colors", {}).get("Primary_Text", {}).get("hex", "#E0E0E0")
    secondary_text_color = d.get("General_UI_Colors", {}).get("Secondary_Text", {}).get("hex", "#B0B0B0")
    information_1_color = d.get("Information_Indicators", {}).get("Information_1", {}).get("hex", "#00BCD4")
    information_2_color = d.get("Information_Indicators", {}).get("Information_2", {}).get("hex", "#03A9F4")
    information_3_color = d.get("Information_Indicators", {}).get("Information_3", {}).get("hex", "#8BC34A")
    warning_color = d.get("Warnings_and_Alerts", {}).get("Warning_1", {}).get("hex", "#FFC107")
    alert_color = d.get("Warnings_and_Alerts", {}).get("Alert_1", {}).get("hex", "#F44336")
    highlight_color = d.get("Highlights_and_Disabled", {}).get("Highlight", {}).get("hex", "#FFEB3B")
    disabled_color = d.get("Highlights_and_Disabled", {}).get("Disabled", {}).get("hex", "#757575")
    start_color = d.get("Movement_Colors", {}).get("Start", {}).get("hex", "#4CAF50")
    end_color = d.get("Movement_Colors", {}).get("Finish", {}).get("hex", "#9C27B0")
    foot_color = d.get("Movement_Colors", {}).get("Foot", {}).get("hex", "#FFEB3B")
    hand_color = d.get("Movement_Colors", {}).get("Hand", {}).get("hex", "#03A9F4")

    # Light theme values from Light_Mode
    bg_light = lm.get("Background", {}).get("hex", "#f4f4f4")
    layer01_light = lm.get("Layer_01", {}).get("hex", "#ffffff")
    layer02_light = lm.get("Layer_02", {}).get("hex", "#f4f4f4")
    layer03_light = lm.get("Layer_03", {}).get("hex", "#e8e8e8")
    text_primary_light = lm.get("Primary_Text", {}).get("hex", "#161616")
    text_secondary_light = lm.get("Secondary_Text", {}).get("hex", "#525252")
    text_disabled_light = lm.get("Disabled_Text", {}).get("hex", "#8d8d8d")
    border_light = lm.get("Border", {}).get("hex", "#c6c6c6")

    # --- Build: raw tokens CSS (ColorPalette.css) ---
    css_tokens = create_css_template(
        background_color=background_color,
        primary_text_color=primary_text_color,
        secondary_text_color=secondary_text_color,
        information_1_color=information_1_color,
        information_2_color=information_2_color,
        information_3_color=information_3_color,
        warning_color=warning_color,
        alert_color=alert_color,
        highlight_color=highlight_color,
        disabled_color=disabled_color,
        start_color=start_color,
        end_color=end_color,
        foot_color=foot_color,
        hand_color=hand_color,
    )

    # --- Build: Monad System CSS (monad.css) ---
    css_library = create_monad_system(
        bg_dark=background_color,
        text_primary_dark=primary_text_color,
        text_secondary_dark=secondary_text_color,
        text_disabled_dark=disabled_color,
        bg_light=bg_light,
        layer01_light=layer01_light,
        layer02_light=layer02_light,
        layer03_light=layer03_light,
        text_primary_light=text_primary_light,
        text_secondary_light=text_secondary_light,
        text_disabled_light=text_disabled_light,
        border_light=border_light,
        interactive=information_2_color,
        interactive_hover="#0288d1",
        interactive_active="#0277bd",
        support_info=information_1_color,
        support_success=information_3_color,
        support_warning=warning_color,
        support_error=alert_color,
        highlight=highlight_color,
        disabled=disabled_color,
        move_start=start_color,
        move_hand=hand_color,
        move_foot=foot_color,
        move_finish=end_color,
    )

    # --- Build: C# (dark theme) ---
    csharp_dark = create_csharp_template(
        background_color=background_color,
        primary_text_color=primary_text_color,
        secondary_text_color=secondary_text_color,
        information_1_color=information_1_color,
        information_2_color=information_2_color,
        information_3_color=information_3_color,
        warning_color=warning_color,
        alert_color=alert_color,
        highlight_color=highlight_color,
        disabled_color=disabled_color,
        start_color=start_color,
        end_color=end_color,
        foot_color=foot_color,
        hand_color=hand_color,
    )

    # --- Build: C# (light theme) ---
    csharp_light = create_csharp_template(
        background_color=bg_light,
        primary_text_color=text_primary_light,
        secondary_text_color=text_secondary_light,
        information_1_color=information_1_color,
        information_2_color=information_2_color,
        information_3_color=information_3_color,
        warning_color=warning_color,
        alert_color=alert_color,
        highlight_color=highlight_color,
        disabled_color=text_disabled_light,
        start_color=start_color,
        end_color=end_color,
        foot_color=foot_color,
        hand_color=hand_color,
        class_name="ColorPaletteLight",
    )

    # --- Build: Python seaborn/matplotlib helpers ---
    python_code = create_python_template(
        bg_dark=background_color,
        text_primary_dark=primary_text_color,
        text_secondary_dark=secondary_text_color,
        text_disabled_dark=disabled_color,
        bg_light=bg_light,
        layer01_light=layer01_light,
        layer02_light=layer02_light,
        layer03_light=layer03_light,
        text_primary_light=text_primary_light,
        text_secondary_light=text_secondary_light,
        text_disabled_light=text_disabled_light,
        interactive=information_2_color,
        support_info=information_1_color,
        support_info_alt=information_2_color,
        support_success=information_3_color,
        support_warning=warning_color,
        support_error=alert_color,
        highlight=highlight_color,
        disabled=disabled_color,
        move_start=start_color,
        move_hand=hand_color,
        move_foot=foot_color,
        move_finish=end_color,
    )

    js_code = create_js_template()

    # ── Derived dark surface layers (shifted from bg) ─────────────────────────
    layer01_dark = _shift_bg(background_color, 18)   # #1e1e1e for #121212
    layer02_dark = _shift_bg(background_color, 26)   # #262626
    layer03_dark = _shift_bg(background_color, 33)   # #333333
    activity_bar_dark = _shift_bg(background_color, -5) if background_color != "#121212" \
        else "#0d0d0d"

    # ── Derived interactive hover/active shades ───────────────────────────────
    ia_hover  = _darken(information_2_color, 0.85)   # #0288d1 for #03A9F4
    ia_active = _darken(information_2_color, 0.75)   # #0277bd

    # ── VS Code themes ────────────────────────────────────────────────────────
    dark_pal = vsc_dark_palette(
        bg=background_color,
        text_primary=primary_text_color,
        text_secondary=secondary_text_color,
        text_disabled=disabled_color,
        border=_shift_bg(background_color, 49),      # #3d3d3d for #121212
        border_subtle=_shift_bg(background_color, 24),
        interactive=information_2_color,
        interactive_hover=ia_hover,
        interactive_active=ia_active,
        info=information_1_color,
        success=information_3_color,
        warning=warning_color,
        error=alert_color,
        highlight=highlight_color,
        move_start=start_color,
        move_hand=hand_color,
        move_foot=foot_color,
        move_finish=end_color,
        layer01=layer01_dark,
        layer02=layer02_dark,
        layer03=layer03_dark,
        activity_bar_bg=activity_bar_dark,
    )

    light_pal = vsc_light_palette(
        bg=bg_light,
        layer01=layer01_light,
        layer02=layer02_light,
        layer03=layer03_light,
        text_primary=text_primary_light,
        text_secondary=text_secondary_light,
        text_disabled=text_disabled_light,
        border=border_light,
        border_subtle=_shift_bg(border_light, 20),
        # Light theme uses pre-darkened accent shades for contrast
        interactive=ia_hover,
        interactive_hover=ia_active,
        interactive_active=_darken(information_2_color, 0.65),
        info=_darken(information_1_color, 0.65),
        success=_darken(information_3_color, 0.65),
        warning=_darken(warning_color, 0.90),
        error=_darken(alert_color, 0.70),
        highlight=_darken(highlight_color, 0.85),
        move_start=_darken(start_color, 0.65),
        move_hand=_darken(hand_color, 0.75),
        move_foot=_darken(foot_color, 0.85),
        move_finish=_darken(end_color, 0.70),
        vivid_interactive=information_2_color,
        vivid_info=information_1_color,
        vivid_success=information_3_color,
        vivid_warning=warning_color,
        vivid_error=alert_color,
        vivid_finish=end_color,
    )

    vscode_dark    = create_vscode_dark_theme(palette=dark_pal)
    vscode_light   = create_vscode_light_theme(palette=light_pal)
    vscode_pkg     = create_vscode_package_json()
    vscode_readme  = create_vscode_readme(dark_pal, light_pal)
    vscode_license = create_vscode_license()

    # ── Ghostty themes ────────────────────────────────────────────────────────
    ghostty_dark = create_ghostty_dark_theme(
        background=background_color,
        foreground=primary_text_color,
        cursor_color=information_2_color,
        cursor_text=background_color,
        selection_background=_blend(information_2_color, background_color, 0.30),
        selection_foreground=primary_text_color,
        ansi_black=background_color,
        ansi_red=alert_color,
        ansi_green=information_3_color,
        ansi_yellow=warning_color,
        ansi_blue=information_2_color,
        ansi_magenta=end_color,
        ansi_cyan=information_1_color,
        ansi_white=secondary_text_color,
        ansi_bright_black=layer03_dark,
        ansi_bright_red=_darken(alert_color, 1.05),       # slightly brighter
        ansi_bright_green=start_color,
        ansi_bright_yellow=highlight_color,
        ansi_bright_blue=_shift_bg(information_2_color, 20),
        ansi_bright_magenta=_darken(end_color, 0.60),     # lighter purple
        ansi_bright_cyan=_darken(information_1_color, 0.60),
        ansi_bright_white=primary_text_color,
    )

    ghostty_light = create_ghostty_light_theme(
        background=bg_light,
        foreground=text_primary_light,
        cursor_color=ia_hover,
        cursor_text=layer01_light,
        selection_background=_blend(ia_hover, bg_light, 0.30),
        selection_foreground=text_primary_light,
        ansi_black=text_primary_light,
        ansi_red=_darken(alert_color, 0.70),
        ansi_green=_darken(information_3_color, 0.65),
        ansi_yellow=_darken(warning_color, 0.90),
        ansi_blue=ia_hover,
        ansi_magenta=_darken(end_color, 0.70),
        ansi_cyan=_darken(information_1_color, 0.65),
        ansi_white=text_secondary_light,
        ansi_bright_black=text_disabled_light,
        ansi_bright_red=alert_color,
        ansi_bright_green=information_3_color,
        ansi_bright_yellow=warning_color,
        ansi_bright_blue=information_2_color,
        ansi_bright_magenta=end_color,
        ansi_bright_cyan=information_1_color,
        ansi_bright_white=layer01_light,
    )

    return {
        "css_tokens":    css_tokens,
        "css_library":   css_library,
        "c_sharp_dark":  csharp_dark,
        "c_sharp_light": csharp_light,
        "python":        python_code,
        "js":            js_code,
        "vscode_dark":    vscode_dark,
        "vscode_light":   vscode_light,
        "vscode_pkg":     vscode_pkg,
        "vscode_readme":  vscode_readme,
        "vscode_license": vscode_license,
        "ghostty_dark":  ghostty_dark,
        "ghostty_light": ghostty_light,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile design system artifacts from colors.json")
    parser.add_argument("--json_path", type=str, required=True, help="Path to the JSON file")
    parser.add_argument("--visualize", action="store_true", default=True, help="Render color palette preview image")
    parser.add_argument("--output_path", type=str, default="build/", help="Path to output directory")

    args = parser.parse_args()

    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)
    else:
        print("Output directory already exists — clearing existing files")
        for filename in os.listdir(args.output_path):
            file_path = os.path.join(args.output_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    try:
        json_data = load_json(args.json_path)
        print("Loaded JSON data")

        if args.visualize:
            try:
                from preview_render import render_palette
                render_palette(json_data, args.output_path)
                print("Rendered color palette image → build/rendered_palette.png")
            except Exception as e:
                print(f"Warning: could not render palette image: {e}")

        code = prepare_templates(json_data)
        print("Generated all templates")

        outputs = {
            # ── Existing artifacts ────────────────────────────────────────────
            "ColorPalette.css":     code["css_tokens"],
            "monad.css":            code["css_library"],
            "monad.js":             code["js"],
            "ColorPalette.cs":      code["c_sharp_dark"],
            "ColorPaletteLight.cs": code["c_sharp_light"],
            "seaborn_palette.py":   code["python"],
            # ── VS Code theme extension ───────────────────────────────────────
            "themes/vscode/package.json":                  code["vscode_pkg"],
            "themes/vscode/monad-dark-color-theme.json":   code["vscode_dark"],
            "themes/vscode/monad-light-color-theme.json":  code["vscode_light"],
            "themes/vscode/README.md":                     code["vscode_readme"],
            "themes/vscode/LICENSE":                       code["vscode_license"],
            # ── Ghostty themes ────────────────────────────────────────────────
            "themes/ghostty/Monad Dark":   code["ghostty_dark"],
            "themes/ghostty/Monad Light":  code["ghostty_light"],
        }

        for filename, content in outputs.items():
            path = os.path.join(args.output_path, filename)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(content)
            print(f"Saved → {os.path.join(args.output_path, filename)}")

        print("\nDone. Artifacts in build/:")
        groups = [
            ("Core",    ["ColorPalette.css", "monad.css", "monad.js"]),
            ("C#",      ["ColorPalette.cs", "ColorPaletteLight.cs"]),
            ("Python",  ["seaborn_palette.py"]),
            ("VS Code", ["themes/vscode/package.json",
                         "themes/vscode/monad-dark-color-theme.json",
                         "themes/vscode/monad-light-color-theme.json",
                         "themes/vscode/README.md",
                         "themes/vscode/LICENSE"]),
            ("Ghostty", ["themes/ghostty/Monad Dark",
                         "themes/ghostty/Monad Light"]),
        ]
        for group_name, files in groups:
            print(f"\n  [{group_name}]")
            for f in files:
                print(f"    {f}")

    except Exception as e:
        print(f"Error: {e}")
        raise
