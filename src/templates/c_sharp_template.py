def create_csharp_template(
    background_color="#0F1113",
    primary_text_color="#EEF2F6",
    secondary_text_color="#B6BFCC",
    information_1_color="#2B9ED1",
    information_2_color="#1E88C8",
    information_3_color="#6EAD45",
    warning_color="#D7A12A",
    alert_color="#D64C45",
    highlight_color="#FFEB3B",
    disabled_color="#7D8794",
    start_color="#4CAF50",
    end_color="#9C27B0",
    foot_color="#FFEB3B",
    hand_color="#1E88C8",
    layer01_color="#181B1F",
    layer02_color="#1F232A",
    layer03_color="#262B33",
    class_name="ColorPalette",
):
    template = f"""// GENERATED — DO NOT EDIT
// Source: monad_system/colors.json via src/templates/c_sharp_template.py
using UnityEngine;

namespace Utility
{{
    public static class {class_name}
    {{
        // Predefined colors
        public static readonly Color Background;
        public static readonly Color PrimaryText;
        public static readonly Color SecondaryText;

        // Layered backgrounds (depth tiers — see colors.json General_UI_Colors)
        public static readonly Color Layer_01;
        public static readonly Color Layer_02;
        public static readonly Color Layer_03;

        // Annotation colors
        public static readonly Color Information1;
        public static readonly Color Information2;
        public static readonly Color Information3;

        public static readonly Color Warning1;

        public static readonly Color Alert;

        public static readonly Color Highlight;
        public static readonly Color Disabled;

        public static readonly Color Start;
        public static readonly Color Hand;
        public static readonly Color Foot;
        public static readonly Color Finish;

        // Other predefined properties
        public static readonly float LowOpacity;
        public static readonly float HighOpacity;

        // Static constructor to initialize colors
        static {class_name}()
        {{
            // Base
            Background = ColorFromHex("{background_color}");
            PrimaryText = ColorFromHex("{primary_text_color}");
            SecondaryText = ColorFromHex("{secondary_text_color}");

            // Layered backgrounds
            Layer_01 = ColorFromHex("{layer01_color}");
            Layer_02 = ColorFromHex("{layer02_color}");
            Layer_03 = ColorFromHex("{layer03_color}");

            // Annotation colors
            Information1 = ColorFromHex("{information_1_color}");
            Information2 = ColorFromHex("{information_2_color}");
            Information3 = ColorFromHex("{information_3_color}");

            Warning1 = ColorFromHex("{warning_color}");
            Alert = ColorFromHex("{alert_color}");

            Highlight = ColorFromHex("{highlight_color}");
            Disabled = ColorFromHex("{disabled_color}");

            Start = ColorFromHex("{start_color}");
            Hand = ColorFromHex("{hand_color}");
            Foot = ColorFromHex("{foot_color}");
            Finish = ColorFromHex("{end_color}");

            // Set the available opacities.
            LowOpacity = 0.2f;
            HighOpacity = 0.8f;
        }}

        // Create RGB color from 0-255 values
        private static Color ColorFromRGB(int r, int g, int b)
        {{
            r = Mathf.Clamp(r, 0, 255);
            g = Mathf.Clamp(g, 0, 255);
            b = Mathf.Clamp(b, 0, 255);

            return new Color(r / 255f, g / 255f, b / 255f);
        }}

        // Converts a hex color code to a Color object
        public static Color ColorFromHex(string hexCode)
        {{
            if (hexCode.StartsWith("#"))
            {{
                hexCode = hexCode.Substring(1); // Remove the '#' if present.
            }}

            if (hexCode.Length != 6)
            {{
                throw new System.ArgumentException("Invalid hex color code. It should be 6 characters long.");
            }}

            // Parse the red, green, and blue components from the hex string.
            float r = int.Parse(hexCode.Substring(0, 2), System.Globalization.NumberStyles.HexNumber) / 255f;
            float g = int.Parse(hexCode.Substring(2, 2), System.Globalization.NumberStyles.HexNumber) / 255f;
            float b = int.Parse(hexCode.Substring(4, 2), System.Globalization.NumberStyles.HexNumber) / 255f;

            return new Color(r, g, b, 1f); // Default alpha is 1 (fully opaque).
        }}
    }}
}}
"""
    return template
