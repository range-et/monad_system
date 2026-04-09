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
from templates.xcode_template import (
    create_xcode_dark_theme,
    create_xcode_light_theme,
)
from templates.swiftui_template import create_swiftui_strata
from templates.texture_template import (
    create_texture_css_fragment,
    create_texture_python,
    create_texture_csharp,
    create_texture_swiftui,
)
from templates.motion_template import (
    create_motion_css_tokens,
    create_motion_css_reduced,
    create_motion_python,
    create_motion_csharp,
    create_motion_swiftui,
    create_motion_js,
)
from templates.cpp_template import (
    create_cpp_palette_header,
    create_cpp_motion_header,
    create_cpp_umbrella_header,
    create_cpp_library_properties,
    create_cpp_keywords,
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


def _rgba_alpha(color_value, default=0.5):
    """Extract alpha from rgba(r,g,b,a) strings; return default for other formats."""
    if not isinstance(color_value, str):
        return default
    value = color_value.strip().lower()
    if not value.startswith("rgba(") or not value.endswith(")"):
        return default
    parts = value[5:-1].split(",")
    if len(parts) != 4:
        return default
    try:
        alpha = float(parts[3].strip())
    except ValueError:
        return default
    return max(0.0, min(1.0, alpha))


def prepare_templates(json_data):
    d = json_data.get("Default_Colors", {})
    dm = d.get("General_UI_Colors", {})
    lm = json_data.get("Light_Mode", {}).get("General_UI_Colors", {})
    textures = json_data.get("Textures", {})
    motion = json_data.get("Motion", None)

    # Dark theme values from Default_Colors
    background_color = dm.get("Background", {}).get("hex", "#121212")
    primary_text_color = dm.get("Primary_Text", {}).get("hex", "#E0E0E0")
    secondary_text_color = dm.get("Secondary_Text", {}).get("hex", "#B0B0B0")
    information_1_color = d.get("Information_Indicators", {}).get("Information_1", {}).get("hex", "#00BCD4")
    information_2_color = d.get("Information_Indicators", {}).get("Information_2", {}).get("hex", "#03A9F4")
    information_3_color = d.get("Information_Indicators", {}).get("Information_3", {}).get("hex", "#8BC34A")
    warning_color = d.get("Warnings_and_Alerts", {}).get("Warning_1", {}).get("hex", "#FFC107")
    alert_color = d.get("Warnings_and_Alerts", {}).get("Alert_1", {}).get("hex", "#F44336")
    highlight_color = d.get("Highlights_and_Disabled", {}).get("Highlight", {}).get("hex", "#FFEB3B")
    disabled_color = d.get("Highlights_and_Disabled", {}).get("Disabled", {}).get("hex", "#757575")

    # Optional explicit dark-mode base layer overrides
    layer01_dark = dm.get("Layer_01", {}).get("hex", _shift_bg(background_color, 18))
    layer02_dark = dm.get("Layer_02", {}).get("hex", _shift_bg(background_color, 26))
    layer03_dark = dm.get("Layer_03", {}).get("hex", _shift_bg(background_color, 33))
    text_disabled_dark = dm.get("Disabled_Text", {}).get("hex", disabled_color)
    border_dark = dm.get("Border", {}).get("hex", _shift_bg(background_color, 49))
    border_subtle_dark = dm.get("Border_Subtle", {}).get("hex", _shift_bg(background_color, 24))
    overlay_dark = dm.get("Overlay", {}).get("hex", "rgba(0,0,0,0.72)")
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
    border_subtle_light = lm.get("Border_Subtle", {}).get("hex", _shift_bg(border_light, 26))
    overlay_light = lm.get("Overlay", {}).get("hex", "rgba(0,0,0,0.5)")
    overlay_dark_alpha = _rgba_alpha(overlay_dark, default=0.72)
    overlay_light_alpha = _rgba_alpha(overlay_light, default=0.50)

    # ── Derived interactive hover/active shades ───────────────────────────────
    ia_hover  = _darken(information_2_color, 0.85)   # #0288d1 for #03A9F4
    ia_active = _darken(information_2_color, 0.75)   # #0277bd

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

    # --- Build: Texture CSS fragment (injected into monad.css) ---
    texture_css = create_texture_css_fragment(textures) if textures else ""

    # --- Build: Motion CSS tokens (injected into monad.css :root) ---
    motion_css = create_motion_css_tokens(motion)
    motion_reduced = create_motion_css_reduced() if motion else ""

    # --- Build: Monad System CSS (monad.css) ---
    css_library = create_monad_system(
        bg_dark=background_color,
        layer01_dark=layer01_dark,
        layer02_dark=layer02_dark,
        layer03_dark=layer03_dark,
        text_primary_dark=primary_text_color,
        text_secondary_dark=secondary_text_color,
        text_disabled_dark=text_disabled_dark,
        border_dark=border_dark,
        border_subtle_dark=border_subtle_dark,
        overlay_dark=overlay_dark,
        bg_light=bg_light,
        layer01_light=layer01_light,
        layer02_light=layer02_light,
        layer03_light=layer03_light,
        text_primary_light=text_primary_light,
        text_secondary_light=text_secondary_light,
        text_disabled_light=text_disabled_light,
        border_light=border_light,
        border_subtle_light=border_subtle_light,
        overlay_light=overlay_light,
        interactive=information_2_color,
        interactive_hover=ia_hover,
        interactive_active=ia_active,
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
        texture_css_fragment=texture_css,
        motion_css_tokens=motion_css,
        motion_css_reduced=motion_reduced,
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
        layer01_color=layer01_dark,
        layer02_color=layer02_dark,
        layer03_color=layer03_dark,
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
        layer01_color=layer01_light,
        layer02_color=layer02_light,
        layer03_color=layer03_light,
        class_name="ColorPaletteLight",
    )

    # --- Build: Python seaborn/matplotlib helpers ---
    python_code = create_python_template(
        bg_dark=background_color,
        text_primary_dark=primary_text_color,
        text_secondary_dark=secondary_text_color,
        text_disabled_dark=text_disabled_dark,
        bg_light=bg_light,
        layer01_light=layer01_light,
        layer02_light=layer02_light,
        layer03_light=layer03_light,
        text_primary_light=text_primary_light,
        text_secondary_light=text_secondary_light,
        text_disabled_light=text_disabled_light,
        border_light=border_light,
        border_subtle_light=border_subtle_light,
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

    motion_js = create_motion_js(motion)
    js_code = create_js_template(motion_js=motion_js)

    # ── Derived dark surface layers (or explicit overrides) ───────────────────
    activity_bar_dark = _shift_bg(background_color, -5) if background_color != "#121212" \
        else "#0d0d0d"

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

    # ── Xcode themes ──────────────────────────────────────────────────────────
    xcode_dark = create_xcode_dark_theme(
        background=background_color,
        line_highlight=layer01_dark,
        insertion_point=information_2_color,
        invisibles=layer03_dark,
        selection=_blend(information_2_color, background_color, 0.30),
        plain_text=primary_text_color,
        comment=disabled_color,
        comment_doc=disabled_color,
        comment_doc_keyword=information_2_color,
        keyword=information_2_color,
        preprocessor=end_color,
        string=information_3_color,
        character=information_3_color,
        number=warning_color,
        url=information_2_color,
        identifier_class=information_1_color,
        identifier_class_system=information_1_color,
        identifier_type=information_1_color,
        identifier_type_system=information_1_color,
        identifier_function=information_1_color,
        identifier_function_system=information_1_color,
        identifier_constant=highlight_color,
        identifier_constant_system=highlight_color,
        identifier_variable=primary_text_color,
        identifier_variable_system=primary_text_color,
        identifier_macro=end_color,
        identifier_macro_system=end_color,
        declaration_other=primary_text_color,
        declaration_type=information_1_color,
        attribute=secondary_text_color,
        gutter_bg=activity_bar_dark,
        gutter_fg=disabled_color,
        console_bg=background_color,
        console_fg=primary_text_color,
        console_input=information_2_color,
        console_output=secondary_text_color,
        console_exec_status=disabled_color,
        console_cursor=information_2_color,
    )

    # SwiftUI Strata — layers/borders match create_monad_system defaults (monad.css)
    swiftui_strata = create_swiftui_strata(
        bg_dark=background_color,
        layer01_dark=layer01_dark,
        layer02_dark=layer02_dark,
        layer03_dark=layer03_dark,
        text_primary_dark=primary_text_color,
        text_secondary_dark=secondary_text_color,
        text_disabled_dark=text_disabled_dark,
        border_dark=border_dark,
        border_subtle_dark=border_subtle_dark,
        bg_light=bg_light,
        layer01_light=layer01_light,
        layer02_light=layer02_light,
        layer03_light=layer03_light,
        text_primary_light=text_primary_light,
        text_secondary_light=text_secondary_light,
        text_disabled_light=text_disabled_light,
        border_light=border_light,
        border_subtle_light=border_subtle_light,
        overlay_dark_alpha=overlay_dark_alpha,
        overlay_light_alpha=overlay_light_alpha,
        interactive=information_2_color,
        interactive_hover=ia_hover,
        interactive_active=ia_active,
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

    xcode_light = create_xcode_light_theme(
        background=bg_light,
        line_highlight=layer02_light,
        insertion_point=ia_hover,
        invisibles=border_light,
        selection=_blend(ia_hover, bg_light, 0.30),
        plain_text=text_primary_light,
        comment=text_disabled_light,
        comment_doc=text_disabled_light,
        comment_doc_keyword=ia_hover,
        keyword=ia_hover,
        preprocessor=_darken(end_color, 0.70),
        string=_darken(information_3_color, 0.65),
        character=_darken(information_3_color, 0.65),
        number=_darken(warning_color, 0.75),
        url=ia_hover,
        identifier_class=_darken(information_1_color, 0.65),
        identifier_class_system=_darken(information_1_color, 0.65),
        identifier_type=_darken(information_1_color, 0.65),
        identifier_type_system=_darken(information_1_color, 0.65),
        identifier_function=_darken(information_1_color, 0.65),
        identifier_function_system=_darken(information_1_color, 0.65),
        identifier_constant=_darken(warning_color, 0.55),
        identifier_constant_system=_darken(warning_color, 0.55),
        identifier_variable=text_primary_light,
        identifier_variable_system=text_primary_light,
        identifier_macro=_darken(end_color, 0.70),
        identifier_macro_system=_darken(end_color, 0.70),
        declaration_other=text_primary_light,
        declaration_type=_darken(information_1_color, 0.65),
        attribute=text_secondary_light,
        gutter_bg=layer01_light,
        gutter_fg=text_disabled_light,
        console_bg=bg_light,
        console_fg=text_primary_light,
        console_input=ia_hover,
        console_output=text_secondary_light,
        console_exec_status=text_disabled_light,
        console_cursor=ia_hover,
    )

    # --- Build: Texture artifacts (Python, C#, SwiftUI) ---
    texture_python  = create_texture_python(textures)  if textures else ""
    texture_csharp  = create_texture_csharp(textures)  if textures else ""
    texture_swiftui = create_texture_swiftui(textures) if textures else ""

    # --- Build: Motion artifacts (Python, C#, SwiftUI) ---
    motion_python  = create_motion_python(motion)
    motion_csharp  = create_motion_csharp(motion)
    motion_swiftui = create_motion_swiftui(motion)

    # --- Build: C++ / Arduino headers (palette + motion + lib metadata) ---
    cpp_palette = create_cpp_palette_header(
        bg_dark=background_color,
        layer01_dark=layer01_dark,
        layer02_dark=layer02_dark,
        layer03_dark=layer03_dark,
        text_primary_dark=primary_text_color,
        text_secondary_dark=secondary_text_color,
        text_disabled_dark=text_disabled_dark,
        border_dark=border_dark,
        border_subtle_dark=border_subtle_dark,
        bg_light=bg_light,
        layer01_light=layer01_light,
        layer02_light=layer02_light,
        layer03_light=layer03_light,
        text_primary_light=text_primary_light,
        text_secondary_light=text_secondary_light,
        text_disabled_light=text_disabled_light,
        border_light=border_light,
        border_subtle_light=border_subtle_light,
        interactive=information_2_color,
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
    cpp_motion             = create_cpp_motion_header(motion)
    cpp_umbrella           = create_cpp_umbrella_header()
    cpp_library_properties = create_cpp_library_properties()
    cpp_keywords           = create_cpp_keywords()

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
        "xcode_dark":    xcode_dark,
        "xcode_light":   xcode_light,
        "swiftui_strata": swiftui_strata,
        "texture_python":  texture_python,
        "texture_csharp":  texture_csharp,
        "texture_swiftui": texture_swiftui,
        "motion_python":   motion_python,
        "motion_csharp":   motion_csharp,
        "motion_swiftui":  motion_swiftui,
        "cpp_palette":            cpp_palette,
        "cpp_motion":             cpp_motion,
        "cpp_umbrella":           cpp_umbrella,
        "cpp_library_properties": cpp_library_properties,
        "cpp_keywords":           cpp_keywords,
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
            "TexturePatterns.cs":   code["texture_csharp"],
            "MotionTokens.cs":      code["motion_csharp"],
            "seaborn_palette.py":   code["python"] + code["texture_python"] + code["motion_python"],
            # ── VS Code theme extension ───────────────────────────────────────
            "themes/vscode/package.json":                  code["vscode_pkg"],
            "themes/vscode/monad-dark-color-theme.json":   code["vscode_dark"],
            "themes/vscode/monad-light-color-theme.json":  code["vscode_light"],
            "themes/vscode/README.md":                     code["vscode_readme"],
            "themes/vscode/LICENSE":                       code["vscode_license"],
            # ── Ghostty themes ────────────────────────────────────────────────
            "themes/ghostty/Monad Dark":   code["ghostty_dark"],
            "themes/ghostty/Monad Light": code["ghostty_light"],
            "themes/xcode/Monad Dark.xccolortheme": code["xcode_dark"],
            "themes/xcode/Monad Light.xccolortheme": code["xcode_light"],
            "themes/swiftui/MonadStrata.swift":   code["swiftui_strata"],
            "themes/swiftui/MonadTextures.swift": code["texture_swiftui"],
            "themes/swiftui/MonadMotion.swift":  code["motion_swiftui"],
            # ── C++ / Arduino header-only library ─────────────────────────────
            "cpp/Monad/src/Monad.h":         code["cpp_umbrella"],
            "cpp/Monad/src/MonadPalette.h":  code["cpp_palette"],
            "cpp/Monad/src/MonadMotion.h":   code["cpp_motion"],
            "cpp/Monad/library.properties":  code["cpp_library_properties"],
            "cpp/Monad/keywords.txt":        code["cpp_keywords"],
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
            ("C#",      ["ColorPalette.cs", "ColorPaletteLight.cs", "TexturePatterns.cs", "MotionTokens.cs"]),
            ("Python",  ["seaborn_palette.py"]),
            ("VS Code", ["themes/vscode/package.json",
                         "themes/vscode/monad-dark-color-theme.json",
                         "themes/vscode/monad-light-color-theme.json",
                         "themes/vscode/README.md",
                         "themes/vscode/LICENSE"]),
            ("Ghostty", ["themes/ghostty/Monad Dark",
                         "themes/ghostty/Monad Light"]),
            ("Xcode",   ["themes/xcode/Monad Dark.xccolortheme",
                         "themes/xcode/Monad Light.xccolortheme"]),
            ("SwiftUI", ["themes/swiftui/MonadStrata.swift",
                         "themes/swiftui/MonadTextures.swift",
                         "themes/swiftui/MonadMotion.swift"]),
            ("C++ / Arduino", ["cpp/Monad/src/Monad.h",
                               "cpp/Monad/src/MonadPalette.h",
                               "cpp/Monad/src/MonadMotion.h",
                               "cpp/Monad/library.properties",
                               "cpp/Monad/keywords.txt"]),
        ]
        for group_name, files in groups:
            print(f"\n  [{group_name}]")
            for f in files:
                print(f"    {f}")

    except Exception as e:
        print(f"Error: {e}")
        raise
