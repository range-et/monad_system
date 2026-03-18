import json
import os
import argparse

from templates.c_sharp_template import create_csharp_template
from templates.css_template import create_css_template, create_monad_system
from templates.python_template import create_python_template
from templates.js_template import create_js_template
from preview_render import render_palette


def load_json(json_path):
    with open(json_path, "r") as file:
        data = json.load(file)
    return data


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

    return {
        "css_tokens": css_tokens,
        "css_library": css_library,
        "c_sharp_dark": csharp_dark,
        "c_sharp_light": csharp_light,
        "python": python_code,
        "js": js_code,
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
                render_palette(json_data, args.output_path)
                print("Rendered color palette image → build/rendered_palette.png")
            except Exception as e:
                print(f"Warning: could not render palette image: {e}")

        code = prepare_templates(json_data)
        print("Generated all templates")

        outputs = {
            "ColorPalette.css":     code["css_tokens"],
            "monad.css":            code["css_library"],
            "monad.js":             code["js"],
            "ColorPalette.cs":      code["c_sharp_dark"],
            "ColorPaletteLight.cs": code["c_sharp_light"],
            "seaborn_palette.py":   code["python"],
        }

        for filename, content in outputs.items():
            path = os.path.join(args.output_path, filename)
            with open(path, "w") as f:
                f.write(content)
            print(f"Saved → build/{filename}")

        print("\nDone. Artifacts in build/:")
        for filename in outputs:
            print(f"  {filename}")

    except Exception as e:
        print(f"Error: {e}")
        raise
