
    namespace Utility
    {
        public static class ColorPalette
        {
            // Predefined colors
            public static readonly Color Background;
            public static readonly Color PrimaryText;
            public static readonly Color SecondaryText;

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
            static ColorPalette()
            {
                // Base
                Background = ColorFromHex("#0F1113");
                PrimaryText = ColorFromHex("#EEF2F6");
                SecondaryText = ColorFromHex("#B6BFCC");

                // Annotation colors
                Information1 = ColorFromHex("#2B9ED1");
                Information2 = ColorFromHex("#1E88C8");
                Information3 = ColorFromHex("#6EAD45");

                Warning1 = ColorFromHex("#D7A12A");
                Alert = ColorFromHex("#D64C45");

                Highlight = ColorFromHex("#FFEB3B");
                Disabled = ColorFromHex("#757575");

                Start = ColorFromHex("#4CAF50");
                Hand = ColorFromHex("#03A9F4");
                Foot = ColorFromHex("#FFEB3B");
                Finish = ColorFromHex("#9C27B0");

                // Set the available opacities.
                LowOpacity = 0.2f;
                HighOpacity = 0.8f;
            }

            // Create RGB color from 0-255 values
            private static Color ColorFromRGB(int r, int g, int b)
            {
                r = Mathf.Clamp(r, 0, 255);
                g = Mathf.Clamp(g, 0, 255);
                b = Mathf.Clamp(b, 0, 255);

                return new Color(r / 255f, g / 255f, b / 255f);
            }

            // Converts a hex color code to a Color object
            public static Color ColorFromHex(string hexCode)
            {
                if (hexCode.StartsWith("#"))
                {
                    hexCode = hexCode.Substring(1); // Remove the '#' if present.
                }

                if (hexCode.Length != 6)
                {
                    throw new System.ArgumentException("Invalid hex color code. It should be 6 characters long.");
                }

                // Parse the red, green, and blue components from the hex string.
                float r = int.Parse(hexCode.Substring(0, 2), System.Globalization.NumberStyles.HexNumber) / 255f;
                float g = int.Parse(hexCode.Substring(2, 2), System.Globalization.NumberStyles.HexNumber) / 255f;
                float b = int.Parse(hexCode.Substring(4, 2), System.Globalization.NumberStyles.HexNumber) / 255f;

                return new Color(r, g, b, 1f); // Default alpha is 1 (fully opaque).
            }
        }
    }
    