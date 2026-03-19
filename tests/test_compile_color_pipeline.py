import copy
import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import compile_color as cc


class CompileColorPipelineTests(unittest.TestCase):
    def _load_colors(self):
        with open(REPO_ROOT / "colors.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def test_prepare_templates_emits_expected_artifacts(self):
        outputs = cc.prepare_templates(self._load_colors())

        expected_keys = {
            "css_tokens",
            "css_library",
            "c_sharp_dark",
            "c_sharp_light",
            "python",
            "js",
            "vscode_dark",
            "vscode_light",
            "vscode_pkg",
            "vscode_readme",
            "vscode_license",
            "ghostty_dark",
            "ghostty_light",
            "xcode_dark",
            "xcode_light",
            "swiftui_strata",
        }
        self.assertTrue(expected_keys.issubset(outputs.keys()))

    def test_information_2_propagates_to_ghostty_css_and_swiftui(self):
        data = self._load_colors()
        modified = copy.deepcopy(data)
        info2 = "#1A2B3C"

        modified["Default_Colors"]["Information_Indicators"]["Information_2"]["hex"] = info2
        outputs = cc.prepare_templates(modified)

        hover = cc._darken(info2, 0.85)
        active = cc._darken(info2, 0.75)

        self.assertIn(f"cursor-color       = {info2}", outputs["ghostty_dark"])
        self.assertIn(f"--strata-interactive:        {info2};", outputs["css_library"])
        self.assertIn(f"--strata-interactive-hover:  {hover};", outputs["css_library"])
        self.assertIn(f"--strata-interactive-active: {active};", outputs["css_library"])
        self.assertIn(
            f'public static let interactive = Color(hex: "{info2}")',
            outputs["swiftui_strata"],
        )
        self.assertIn(
            f'public static let interactiveHover = Color(hex: "{hover}")',
            outputs["swiftui_strata"],
        )
        self.assertIn(
            f'public static let interactiveActive = Color(hex: "{active}")',
            outputs["swiftui_strata"],
        )

    def test_dark_background_derives_swiftui_layers_and_ghostty_palette(self):
        data = self._load_colors()
        modified = copy.deepcopy(data)
        bg = "#102030"

        modified["Default_Colors"]["General_UI_Colors"]["Background"]["hex"] = bg
        outputs = cc.prepare_templates(modified)

        layer01 = cc._shift_bg(bg, 18)
        layer02 = cc._shift_bg(bg, 26)
        layer03 = cc._shift_bg(bg, 33)
        border_dark = cc._shift_bg(bg, 49)
        border_subtle_dark = cc._shift_bg(bg, 24)
        border_subtle_light = cc._shift_bg("#c6c6c6", 26)

        self.assertIn(f'light: "#ffffff",\n        dark: "{layer01}"', outputs["swiftui_strata"])
        self.assertIn(f'light: "#f4f4f4",\n        dark: "{layer02}"', outputs["swiftui_strata"])
        self.assertIn(f'light: "#e8e8e8",\n        dark: "{layer03}"', outputs["swiftui_strata"])
        self.assertIn(
            f'public static let border = _adaptive(\n        light: "#c6c6c6",\n        dark: "{border_dark}"',
            outputs["swiftui_strata"],
        )
        self.assertIn(
            f'public static let borderSubtle = _adaptive(\n        light: "{border_subtle_light}",\n        dark: "{border_subtle_dark}"',
            outputs["swiftui_strata"],
        )
        self.assertIn(f"background = {bg}", outputs["ghostty_dark"])
        self.assertIn(f"palette = 0={bg}", outputs["ghostty_dark"])


if __name__ == "__main__":
    unittest.main()
