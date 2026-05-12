import copy
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import compile_color as cc
from preview_render import render_palette


class CompileColorPipelineTests(unittest.TestCase):
    def _load_colors(self):
        with open(REPO_ROOT / "colors.json", "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _xcode_color(hex_color):
        h = hex_color.lstrip("#")
        r = int(h[0:2], 16) / 255.0
        g = int(h[2:4], 16) / 255.0
        b = int(h[4:6], 16) / 255.0
        return f"{r:.4f} {g:.4f} {b:.4f} 1"

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

        # Remove explicit layer overrides to verify derivation fallback path.
        modified["Default_Colors"]["General_UI_Colors"].pop("Layer_01", None)
        modified["Default_Colors"]["General_UI_Colors"].pop("Layer_02", None)
        modified["Default_Colors"]["General_UI_Colors"].pop("Layer_03", None)
        modified["Default_Colors"]["General_UI_Colors"].pop("Border", None)
        modified["Default_Colors"]["General_UI_Colors"].pop("Border_Subtle", None)
        modified["Light_Mode"]["General_UI_Colors"].pop("Border_Subtle", None)

        modified["Default_Colors"]["General_UI_Colors"]["Background"]["hex"] = bg
        outputs = cc.prepare_templates(modified)

        layer01 = cc._shift_bg(bg, 18)
        layer02 = cc._shift_bg(bg, 26)
        layer03 = cc._shift_bg(bg, 33)
        border_dark = cc._shift_bg(bg, 49)
        border_subtle_dark = cc._shift_bg(bg, 24)
        light_layer01 = modified["Light_Mode"]["General_UI_Colors"]["Layer_01"]["hex"]
        light_layer02 = modified["Light_Mode"]["General_UI_Colors"]["Layer_02"]["hex"]
        light_layer03 = modified["Light_Mode"]["General_UI_Colors"]["Layer_03"]["hex"]
        light_border = modified["Light_Mode"]["General_UI_Colors"]["Border"]["hex"]
        border_subtle_light = cc._shift_bg(light_border, 26)

        self.assertIn(f'light: "{light_layer01}",\n        dark: "{layer01}"', outputs["swiftui_strata"])
        self.assertIn(f'light: "{light_layer02}",\n        dark: "{layer02}"', outputs["swiftui_strata"])
        self.assertIn(f'light: "{light_layer03}",\n        dark: "{layer03}"', outputs["swiftui_strata"])
        self.assertIn(
            f'public static let border = _adaptive(\n        light: "{light_border}",\n        dark: "{border_dark}"',
            outputs["swiftui_strata"],
        )
        self.assertIn(
            f'public static let borderSubtle = _adaptive(\n        light: "{border_subtle_light}",\n        dark: "{border_subtle_dark}"',
            outputs["swiftui_strata"],
        )
        self.assertIn(f"background = {bg}", outputs["ghostty_dark"])
        self.assertIn(f"palette = 0={bg}", outputs["ghostty_dark"])

    def test_generated_js_uses_explicit_threshold_and_rail_contracts(self):
        outputs = cc.prepare_templates(self._load_colors())
        js = outputs["js"]

        self.assertIn("[data-mn-threshold-toggle]", js)
        self.assertIn("[data-mn-threshold-nav]", js)
        self.assertIn("[data-mn-rail-toggle]", js)
        self.assertIn("[data-mn-rail]", js)
        self.assertIn("aria-pressed", js)

    def test_generated_css_emits_on_signal_tokens_and_switch_focus_style(self):
        outputs = cc.prepare_templates(self._load_colors())
        css = outputs["css_library"]

        self.assertIn("--strata-on-interactive:", css)
        self.assertIn("--strata-on-info:", css)
        self.assertIn("--strata-on-success:", css)
        self.assertIn("--strata-on-warning:", css)
        self.assertIn("--strata-on-error:", css)
        self.assertIn(".atomos-switch input:focus-visible + .atomos-switch__track", css)

    def test_dark_palette_token_propagates_across_all_targets(self):
        data = self._load_colors()
        modified = copy.deepcopy(data)

        info2 = "#13579B"
        modified["Default_Colors"]["Information_Indicators"]["Information_2"]["hex"] = info2

        outputs = cc.prepare_templates(modified)

        self.assertIn(f"--strata-interactive:        {info2};", outputs["css_library"])
        self.assertIn(f"Information2 = ColorFromHex(\"{info2}\");", outputs["c_sharp_dark"])
        self.assertIn(f'"interactive":    "{info2}"', outputs["python"])
        self.assertIn(f'public static let interactive = Color(hex: "{info2}")', outputs["swiftui_strata"])
        self.assertIn(f"cursor-color       = {info2}", outputs["ghostty_dark"])
        self.assertIn(f'"button.background": "{info2}"', outputs["vscode_dark"])

        # Xcode themes store normalized RGBA floats, not hex literals.
        xcode_info2 = self._xcode_color(info2)
        self.assertIn(xcode_info2, outputs["xcode_dark"])

    def test_light_base_tokens_propagate_across_light_targets(self):
        data = self._load_colors()
        modified = copy.deepcopy(data)

        light_bg = "#ECEFF4"
        light_text = "#1A1E27"
        modified["Light_Mode"]["General_UI_Colors"]["Background"]["hex"] = light_bg
        modified["Light_Mode"]["General_UI_Colors"]["Primary_Text"]["hex"] = light_text

        outputs = cc.prepare_templates(modified)

        self.assertIn(f"Background = ColorFromHex(\"{light_bg}\");", outputs["c_sharp_light"])
        self.assertIn(f"PrimaryText = ColorFromHex(\"{light_text}\");", outputs["c_sharp_light"])
        self.assertIn(f'"editor.background": "{light_bg}"', outputs["vscode_light"])
        self.assertIn(f"background = {light_bg}", outputs["ghostty_light"])
        self.assertIn(f"foreground = {light_text}", outputs["ghostty_light"])
        self.assertIn(f'light: "{light_bg}"', outputs["swiftui_strata"])

        xcode_bg = self._xcode_color(light_bg)
        xcode_text = self._xcode_color(light_text)
        self.assertIn(xcode_bg, outputs["xcode_light"])
        self.assertIn(xcode_text, outputs["xcode_light"])

    def test_csharp_unity_template_compiles_cleanly(self):
        """The generated C# must be drop-in compilable in a Unity project:
        needs `using UnityEngine;` for Color/Mathf, the static constructor name
        must match the class name, and Layer_01/02/03 must be exposed as fields.
        """
        outputs = cc.prepare_templates(self._load_colors())

        dark = outputs["c_sharp_dark"]
        light = outputs["c_sharp_light"]

        # Both files must import UnityEngine for Color and Mathf to resolve.
        self.assertIn("using UnityEngine;", dark)
        self.assertIn("using UnityEngine;", light)

        # Namespace must be `Monad`, NOT `Utility`. The Beta-Bot Unity project
        # already has a `Master.Utility` class referenced as `Utility.X`; if
        # this template emits `namespace Utility`, the C# resolver picks the
        # namespace first and breaks every existing call site.
        self.assertIn("namespace Monad", dark)
        self.assertIn("namespace Monad", light)
        self.assertNotIn("namespace Utility", dark)
        self.assertNotIn("namespace Utility", light)

        # Static constructor name must match class name (C# language requirement).
        self.assertIn("public static class ColorPalette", dark)
        self.assertIn("static ColorPalette()", dark)
        self.assertIn("public static class ColorPaletteLight", light)
        self.assertIn("static ColorPaletteLight()", light)
        # And the dark file must NOT contain a "ColorPaletteLight()" constructor and vice-versa.
        self.assertNotIn("static ColorPaletteLight()", dark)
        self.assertNotIn("static ColorPalette()", light)

        # Layer_01/02/03 fields are exposed and assigned in both themes.
        for field in ("Layer_01", "Layer_02", "Layer_03"):
            self.assertIn(f"public static readonly Color {field};", dark,
                          f"Dark C# missing field {field}")
            self.assertIn(f"public static readonly Color {field};", light,
                          f"Light C# missing field {field}")
            self.assertIn(f"{field} = ColorFromHex(", dark,
                          f"Dark C# missing assignment for {field}")
            self.assertIn(f"{field} = ColorFromHex(", light,
                          f"Light C# missing assignment for {field}")

    def test_csharp_layer_tokens_propagate_from_colors_json(self):
        """Editing Light_Mode.General_UI_Colors.Layer_01 in colors.json must
        flow into ColorPaletteLight.cs."""
        data = self._load_colors()
        modified = copy.deepcopy(data)

        layer1_light = "#F1F2F3"
        modified["Light_Mode"]["General_UI_Colors"]["Layer_01"]["hex"] = layer1_light

        outputs = cc.prepare_templates(modified)
        self.assertIn(f'Layer_01 = ColorFromHex("{layer1_light}");',
                      outputs["c_sharp_light"])


    # ── HTML showcase tests ─────────────────────────────────────────────────

    def test_components_html_references_all_texture_classes(self):
        html_path = REPO_ROOT / "samples" / "components.html"
        html = html_path.read_text(encoding="utf-8")
        for tid in ("dot", "hatch-v", "hatch-h", "hatch-x", "hatch-fwd", "hatch-bwd"):
            self.assertIn(f"atomos-texture--{tid}", html,
                          f"components.html missing texture class for {tid}")

    def test_components_html_references_strata_color_tokens(self):
        html_path = REPO_ROOT / "samples" / "components.html"
        html = html_path.read_text(encoding="utf-8")
        for token in ("--strata-bg", "--strata-interactive", "--strata-info",
                      "--strata-success", "--strata-warning", "--strata-error",
                      "--strata-text-primary", "--strata-border"):
            self.assertIn(token, html, f"components.html missing token {token}")

    def test_built_css_contains_colors_from_json(self):
        data = self._load_colors()
        outputs = cc.prepare_templates(data)
        css = outputs["css_library"]
        d = data["Default_Colors"]
        # Verify key hex values from colors.json appear in the CSS
        bg = d["General_UI_Colors"]["Background"]["hex"]
        interactive = d["Information_Indicators"]["Information_2"]["hex"]
        error = d["Warnings_and_Alerts"]["Alert_1"]["hex"]
        self.assertIn(bg, css, "Background hex missing from CSS")
        self.assertIn(interactive, css, "Interactive hex missing from CSS")
        self.assertIn(error, css, "Error hex missing from CSS")

    # ── Palette render tests ────────────────────────────────────────────────

    def test_render_palette_produces_valid_png(self):
        data = self._load_colors()
        with tempfile.TemporaryDirectory() as tmp:
            render_palette(data, tmp)
            png_path = os.path.join(tmp, "rendered_palette.png")
            self.assertTrue(os.path.isfile(png_path), "rendered_palette.png not created")
            size = os.path.getsize(png_path)
            self.assertGreater(size, 10_000, f"PNG too small ({size} bytes)")

    def test_render_palette_without_textures(self):
        data = self._load_colors()
        data.pop("Textures", None)
        with tempfile.TemporaryDirectory() as tmp:
            render_palette(data, tmp)
            png_path = os.path.join(tmp, "rendered_palette.png")
            self.assertTrue(os.path.isfile(png_path), "should render without Textures key")

    # ── Texture tests ──────────────────────────────────────────────────────

    def test_texture_tokens_in_css_library(self):
        data = self._load_colors()
        outputs = cc.prepare_templates(data)
        css = outputs["css_library"]

        for tid in ("dot", "hatch-v", "hatch-h", "hatch-x", "hatch-fwd", "hatch-bwd"):
            self.assertIn(f"--strata-texture-{tid}:", css)
            self.assertIn(f".atomos-texture--{tid}", css)
        self.assertIn("data:image/svg+xml", css)
        self.assertIn(".atomos-texture {", css)

    def test_texture_python_hatch_mappings(self):
        data = self._load_colors()
        outputs = cc.prepare_templates(data)
        py = outputs["texture_python"]

        self.assertIn("TEXTURE_HATCHES", py)
        for ch in ('"."', '"|"', '"-"', '"+"', '"/"', '"\\\\"'):
            self.assertIn(ch, py)
        self.assertIn("def apply_texture(", py)

    def test_texture_csharp_methods(self):
        data = self._load_colors()
        outputs = cc.prepare_templates(data)
        cs = outputs["texture_csharp"]

        for method in ("CreateDot", "CreateHatchVertical", "CreateHatchHorizontal",
                       "CreateCrossHatch", "CreateHatchForward", "CreateHatchBackward"):
            self.assertIn(method, cs)
        self.assertIn("Texture2D", cs)
        self.assertIn("namespace Monad", cs)

    def test_texture_swiftui_enum(self):
        data = self._load_colors()
        outputs = cc.prepare_templates(data)
        swift = outputs["texture_swiftui"]

        self.assertIn("enum MonadTexture", swift)
        for case in ("case dot", "case hatchV", "case hatchH", "case hatchX",
                     "case hatchFwd", "case hatchBwd"):
            self.assertIn(case, swift)
        self.assertIn("func monadTexture(", swift)
        self.assertIn("TexturePatternView", swift)

    def test_texture_params_propagate_from_json(self):
        data = self._load_colors()
        modified = copy.deepcopy(data)
        modified["Textures"]["dot"]["spacing"] = 20
        modified["Textures"]["dot"]["radius"] = 2.5
        outputs = cc.prepare_templates(modified)
        css = outputs["css_library"]

        self.assertIn("width='20'", css)
        self.assertIn("r='2.5'", css)

    def test_missing_textures_backward_compat(self):
        data = self._load_colors()
        modified = copy.deepcopy(data)
        modified.pop("Textures", None)
        outputs = cc.prepare_templates(modified)

        # All original 16 keys still present
        for key in ("css_tokens", "css_library", "c_sharp_dark", "c_sharp_light",
                    "python", "js", "vscode_dark", "vscode_light", "vscode_pkg",
                    "vscode_readme", "vscode_license", "ghostty_dark", "ghostty_light",
                    "xcode_dark", "xcode_light", "swiftui_strata"):
            self.assertIn(key, outputs)

        # Texture artifacts should be empty strings
        for key in ("texture_python", "texture_csharp", "texture_swiftui"):
            self.assertEqual(outputs[key], "")

        # No texture tokens in CSS
        self.assertNotIn("--strata-texture-", outputs["css_library"])


    # ── Motion token tests ─────────────────────────────────────────────────

    def test_motion_tokens_in_css_library(self):
        data = self._load_colors()
        outputs = cc.prepare_templates(data)
        css = outputs["css_library"]

        # Duration tokens
        for key in ("fast", "base", "slow", "slower"):
            self.assertIn(f"--threshold-duration-{key}:", css)

        # Easing tokens
        self.assertIn("--threshold-ease-linear:", css)
        self.assertIn("--threshold-ease-out:", css)
        self.assertIn("--threshold-ease-in:", css)
        self.assertIn("--threshold-ease-in-out:", css)
        self.assertIn("cubic-bezier(0.16, 1, 0.3, 1)", css)

        # Composed shorthands (backward compat)
        self.assertIn("--threshold-fast:", css)
        self.assertIn("--threshold-base:", css)
        self.assertIn("--threshold-slow:", css)

        # Reduced motion
        self.assertIn("prefers-reduced-motion: reduce", css)

    def test_motion_python_durations_and_easings(self):
        data = self._load_colors()
        outputs = cc.prepare_templates(data)
        py = outputs["motion_python"]

        self.assertIn("MOTION_DURATIONS", py)
        self.assertIn("MOTION_EASINGS", py)
        self.assertIn('"fast":', py)
        self.assertIn("0.080", py)
        self.assertIn('"ease_out":', py)
        self.assertIn("(0.16, 1.0, 0.3, 1.0)", py)

    def test_motion_csharp_constants(self):
        data = self._load_colors()
        outputs = cc.prepare_templates(data)
        cs = outputs["motion_csharp"]

        self.assertIn("namespace Monad", cs)
        self.assertIn("MotionTokens", cs)
        self.assertIn("DurationFast", cs)
        self.assertIn("DurationBase", cs)
        self.assertIn("DurationSlow", cs)
        self.assertIn("DurationSlower", cs)
        self.assertIn("0.080f", cs)
        self.assertIn("AnimationCurve", cs)

    def test_motion_swiftui_enum(self):
        data = self._load_colors()
        outputs = cc.prepare_templates(data)
        swift = outputs["motion_swiftui"]

        self.assertIn("enum MonadMotion", swift)
        self.assertIn("durationFast", swift)
        self.assertIn("durationBase", swift)
        self.assertIn("durationSlow", swift)
        self.assertIn("durationSlower", swift)
        self.assertIn("0.080", swift)
        self.assertIn("Animation.timingCurve", swift)
        self.assertIn("easeOut", swift)

    def test_motion_js_namespace(self):
        data = self._load_colors()
        outputs = cc.prepare_templates(data)
        js = outputs["js"]

        self.assertIn("MN.motion", js)
        self.assertIn("duration:", js)
        self.assertIn("easing:", js)
        self.assertIn("fast: 80", js)
        self.assertIn("cubic-bezier(0.16, 1, 0.3, 1)", js)

    def test_motion_params_propagate_from_json(self):
        data = self._load_colors()
        modified = copy.deepcopy(data)
        modified["Motion"]["durations"]["fast"]["ms"] = 100
        modified["Motion"]["easings"]["ease_out"]["css"] = "cubic-bezier(0.2, 1, 0.4, 1)"
        outputs = cc.prepare_templates(modified)

        # CSS
        self.assertIn("100ms", outputs["css_library"])
        self.assertIn("cubic-bezier(0.2, 1, 0.4, 1)", outputs["css_library"])

        # Python
        full_py = outputs["python"] + outputs["motion_python"]
        self.assertIn("0.100", full_py)

        # C#
        self.assertIn("0.100f", outputs["motion_csharp"])

        # SwiftUI
        self.assertIn("0.100", outputs["motion_swiftui"])

        # JS
        self.assertIn("fast: 100", outputs["js"])

    def test_missing_motion_backward_compat(self):
        data = self._load_colors()
        modified = copy.deepcopy(data)
        modified.pop("Motion", None)
        outputs = cc.prepare_templates(modified)

        # All original 16 keys still present
        for key in ("css_tokens", "css_library", "c_sharp_dark", "c_sharp_light",
                    "python", "js", "vscode_dark", "vscode_light", "vscode_pkg",
                    "vscode_readme", "vscode_license", "ghostty_dark", "ghostty_light",
                    "xcode_dark", "xcode_light", "swiftui_strata"):
            self.assertIn(key, outputs)

        # Motion artifacts should be empty strings
        for key in ("motion_python", "motion_csharp", "motion_swiftui"):
            self.assertEqual(outputs[key], "")

        # Legacy hardcoded values still in CSS
        self.assertIn("--threshold-fast:", outputs["css_library"])
        self.assertIn("80ms linear", outputs["css_library"])

    # ── C++ / Arduino tests ────────────────────────────────────────────────

    def test_cpp_artifacts_emitted(self):
        outputs = cc.prepare_templates(self._load_colors())
        for key in ("cpp_palette", "cpp_motion", "cpp_umbrella",
                    "cpp_library_properties", "cpp_keywords"):
            self.assertIn(key, outputs)
            self.assertTrue(outputs[key], f"{key} should be non-empty")

    def test_cpp_palette_structure(self):
        outputs = cc.prepare_templates(self._load_colors())
        h = outputs["cpp_palette"]

        # Header guards and stdint dependency
        self.assertIn("#pragma once", h)
        self.assertIn("#include <stdint.h>", h)

        # Top-level namespace + theme namespaces + alias
        self.assertIn("namespace monad {", h)
        self.assertIn("namespace dark {", h)
        self.assertIn("namespace light {", h)
        self.assertIn("namespace theme = light;", h)
        self.assertIn("namespace theme = dark;", h)
        self.assertIn("MONAD_LIGHT_THEME", h)

        # Constexpr conversion helpers
        self.assertIn("constexpr uint16_t rgb565(uint32_t c)", h)
        self.assertIn("constexpr uint8_t gray8(uint32_t c)", h)
        self.assertIn("constexpr bool mono(uint32_t c", h)

        # All semantic and surface tokens present in both themes
        for token in ("BACKGROUND", "LAYER_01", "LAYER_02", "LAYER_03",
                      "TEXT_PRIMARY", "TEXT_SECONDARY", "TEXT_DISABLED",
                      "BORDER", "BORDER_SUBTLE", "INTERACTIVE",
                      "SUPPORT_INFO", "SUPPORT_SUCCESS", "SUPPORT_WARNING",
                      "SUPPORT_ERROR", "HIGHLIGHT", "DISABLED",
                      "MOVE_START", "MOVE_HAND", "MOVE_FOOT", "MOVE_FINISH"):
            self.assertIn(token, h, f"missing token {token} in MonadPalette.h")

    def test_cpp_palette_hex_propagates_from_json(self):
        data = self._load_colors()
        modified = copy.deepcopy(data)
        info2 = "#13579B"
        modified["Default_Colors"]["Information_Indicators"]["Information_2"]["hex"] = info2
        outputs = cc.prepare_templates(modified)

        # 0x13579B should appear as the INTERACTIVE constant in both namespaces
        self.assertIn("INTERACTIVE       = 0x13579B;", outputs["cpp_palette"])
        # Counts: shared block is emitted in both dark and light → 2 occurrences
        self.assertEqual(outputs["cpp_palette"].count("0x13579B"), 2)

    def test_cpp_palette_dark_background_propagates(self):
        data = self._load_colors()
        modified = copy.deepcopy(data)
        bg = "#102030"
        modified["Default_Colors"]["General_UI_Colors"]["Background"]["hex"] = bg
        outputs = cc.prepare_templates(modified)

        # Dark BACKGROUND constant uses the new hex
        self.assertIn("BACKGROUND        = 0x102030;", outputs["cpp_palette"])
        # Light theme background must be unchanged (different value)
        self.assertNotIn("BACKGROUND        = 0x102030;\n}",
                         outputs["cpp_palette"].split("namespace light {")[1])

    def test_cpp_motion_durations_and_easings(self):
        outputs = cc.prepare_templates(self._load_colors())
        h = outputs["cpp_motion"]

        self.assertIn("namespace monad {", h)
        self.assertIn("namespace motion {", h)
        self.assertIn("constexpr uint16_t DURATION_FAST_MS", h)
        self.assertIn("= 80;", h)
        self.assertIn("DURATION_BASE_MS", h)
        self.assertIn("DURATION_SLOW_MS", h)
        self.assertIn("DURATION_SLOWER_MS", h)

        self.assertIn("struct Bezier", h)
        self.assertIn("EASE_OUT", h)
        self.assertIn("EASE_IN", h)
        self.assertIn("EASE_IN_OUT", h)
        # Linear has no bezier definition — only a comment
        self.assertIn("EASE_LINEAR: linear", h)

        self.assertIn("constexpr uint8_t lerp_u8", h)
        self.assertIn("constexpr uint32_t lerp_rgb", h)

    def test_cpp_motion_params_propagate(self):
        data = self._load_colors()
        modified = copy.deepcopy(data)
        modified["Motion"]["durations"]["fast"]["ms"] = 100
        modified["Motion"]["easings"]["ease_out"]["css"] = "cubic-bezier(0.2, 1, 0.4, 1)"
        outputs = cc.prepare_templates(modified)

        h = outputs["cpp_motion"]
        # Spacing between identifier and "=" is alignment-driven; assert the
        # identifier and value, not the exact pad width.
        self.assertRegex(h, r"DURATION_FAST_MS\s+= 100;")
        self.assertIn("EASE_OUT = { 0.2f, 1.0f, 0.4f, 1.0f };", h)
        # Sanity: no double-prefixed identifiers.
        self.assertNotIn("EASE_EASE_", h)

    def test_cpp_motion_missing_falls_back(self):
        data = self._load_colors()
        modified = copy.deepcopy(data)
        modified.pop("Motion", None)
        outputs = cc.prepare_templates(modified)

        h = outputs["cpp_motion"]
        self.assertIn("Legacy fallback", h)
        self.assertIn("DURATION_FAST_MS   = 80;", h)
        self.assertIn("DURATION_BASE_MS   = 160;", h)
        self.assertIn("DURATION_SLOW_MS   = 280;", h)

    def test_cpp_umbrella_includes_palette_and_motion(self):
        outputs = cc.prepare_templates(self._load_colors())
        h = outputs["cpp_umbrella"]
        self.assertIn("#pragma once", h)
        self.assertIn('#include "MonadPalette.h"', h)
        self.assertIn('#include "MonadMotion.h"', h)
        self.assertIn("MONAD_LIGHT_THEME", h)

    def test_cpp_library_properties_arduino_fields(self):
        outputs = cc.prepare_templates(self._load_colors())
        props = outputs["cpp_library_properties"]
        for field in ("name=", "version=", "author=", "maintainer=",
                      "sentence=", "paragraph=", "category=", "url=",
                      "architectures=", "includes=Monad.h"):
            self.assertIn(field, props)

    def test_cpp_keywords_uses_tabs(self):
        outputs = cc.prepare_templates(self._load_colors())
        kw = outputs["cpp_keywords"]
        # Arduino IDE requires literal tabs between identifier and class
        self.assertIn("rgb565\tKEYWORD2", kw)
        self.assertIn("BACKGROUND\tLITERAL1", kw)
        self.assertIn("monad\tKEYWORD1", kw)

    # ── Streamlit tests ────────────────────────────────────────────────────

    def test_streamlit_artifacts_emitted(self):
        outputs = cc.prepare_templates(self._load_colors())
        for key in ("streamlit_config", "streamlit_config_light",
                    "streamlit_helper", "streamlit_readme"):
            self.assertIn(key, outputs)
            self.assertTrue(outputs[key], f"{key} should be non-empty")

    def test_streamlit_dark_config_uses_dark_tokens(self):
        data = self._load_colors()
        outputs = cc.prepare_templates(data)
        cfg = outputs["streamlit_config"]

        d = data["Default_Colors"]["General_UI_Colors"]
        bg = d["Background"]["hex"]
        layer02 = d["Layer_02"]["hex"]
        text = d["Primary_Text"]["hex"]
        border = d["Border"]["hex"]

        self.assertIn("[theme]", cfg)
        self.assertIn('base                     = "dark"', cfg)
        self.assertIn(f'backgroundColor          = "{bg}"', cfg)
        self.assertIn(f'secondaryBackgroundColor = "{layer02}"', cfg)
        self.assertIn(f'textColor                = "{text}"', cfg)
        self.assertIn(f'borderColor              = "{border}"', cfg)
        self.assertIn('baseRadius               = "none"', cfg)

    def test_streamlit_light_config_uses_light_tokens(self):
        data = self._load_colors()
        outputs = cc.prepare_templates(data)
        light = outputs["streamlit_config_light"]

        l = data["Light_Mode"]["General_UI_Colors"]
        self.assertIn('base                     = "light"', light)
        self.assertIn(f'backgroundColor          = "{l["Background"]["hex"]}"', light)
        self.assertIn(f'secondaryBackgroundColor = "{l["Layer_02"]["hex"]}"', light)
        self.assertIn(f'textColor                = "{l["Primary_Text"]["hex"]}"', light)
        self.assertIn(f'borderColor              = "{l["Border"]["hex"]}"', light)
        self.assertIn('baseRadius               = "none"', light)

    def test_streamlit_helper_exposes_apply_and_token_tables(self):
        outputs = cc.prepare_templates(self._load_colors())
        helper = outputs["streamlit_helper"]

        self.assertIn("def apply_monad_theme(", helper)
        self.assertIn("DARK_TOKENS", helper)
        self.assertIn("LIGHT_TOKENS", helper)
        self.assertIn("import streamlit as st", helper)
        self.assertIn('"background":', helper)
        self.assertIn('"layer-01":', helper)
        self.assertIn('"layer-02":', helper)
        self.assertIn('"layer-03":', helper)
        self.assertIn('"text-primary":', helper)
        self.assertIn('"border":', helper)

    def test_streamlit_dark_token_propagates_from_json(self):
        data = self._load_colors()
        modified = copy.deepcopy(data)
        bg = "#102030"
        modified["Default_Colors"]["General_UI_Colors"]["Background"]["hex"] = bg
        outputs = cc.prepare_templates(modified)

        self.assertIn(f'backgroundColor          = "{bg}"',
                      outputs["streamlit_config"])
        self.assertIn(f'"background":       "{bg}"',
                      outputs["streamlit_helper"])

    def test_streamlit_light_token_propagates_from_json(self):
        data = self._load_colors()
        modified = copy.deepcopy(data)
        light_bg = "#ECEFF4"
        modified["Light_Mode"]["General_UI_Colors"]["Background"]["hex"] = light_bg
        outputs = cc.prepare_templates(modified)

        self.assertIn(f'backgroundColor          = "{light_bg}"',
                      outputs["streamlit_config_light"])
        self.assertIn(f'"background":       "{light_bg}"',
                      outputs["streamlit_helper"])

    def test_streamlit_readme_documents_artifacts(self):
        outputs = cc.prepare_templates(self._load_colors())
        readme = outputs["streamlit_readme"]
        for token in ("config.toml", "config-light.toml",
                      "monad_streamlit.py", "apply_monad_theme"):
            self.assertIn(token, readme,
                          f"streamlit README missing reference to {token}")

    # ── HTML showcase tests (dashboard + motion) ───────────────────────────

    def test_dashboard_html_references_strata_tokens(self):
        html_path = REPO_ROOT / "samples" / "dashboard.html"
        html = html_path.read_text(encoding="utf-8")
        for token in ("--strata-bg", "--strata-layer-01", "--strata-layer-02",
                      "--strata-border", "--strata-border-subtle",
                      "--strata-text-primary", "--strata-text-secondary",
                      "--strata-text-disabled",
                      "--strata-interactive", "--strata-on-interactive",
                      "--strata-info", "--strata-success",
                      "--strata-warning", "--strata-error",
                      "--threshold-fast"):
            self.assertIn(token, html,
                          f"dashboard.html missing token {token}")

    def test_motion_html_references_threshold_tokens(self):
        html_path = REPO_ROOT / "samples" / "motion.html"
        html = html_path.read_text(encoding="utf-8")
        # Motion page must reference the duration + easing tokens it showcases
        for token in ("--threshold-duration-fast",
                      "--threshold-duration-base",
                      "--threshold-duration-slow",
                      "--threshold-duration-slower",
                      "--threshold-ease-linear",
                      "--threshold-ease-out",
                      "--threshold-ease-in",
                      "--threshold-ease-in-out"):
            self.assertIn(token, html,
                          f"motion.html missing token {token}")
        # Plus the strata surface tokens used to render the demos
        for token in ("--strata-layer-01", "--strata-layer-02",
                      "--strata-interactive", "--strata-text-primary",
                      "--strata-border"):
            self.assertIn(token, html,
                          f"motion.html missing strata token {token}")

    # ── VS Code package.json metadata ──────────────────────────────────────

    def test_vscode_package_json_is_valid_and_lists_both_themes(self):
        import json as _json
        outputs = cc.prepare_templates(self._load_colors())
        pkg = _json.loads(outputs["vscode_pkg"])

        # Required VS Code extension fields
        for field in ("name", "displayName", "version", "publisher",
                      "engines", "categories", "contributes"):
            self.assertIn(field, pkg, f"package.json missing {field}")

        self.assertIn("Themes", pkg["categories"])
        self.assertIn("vscode", pkg["engines"])

        themes = pkg["contributes"].get("themes", [])
        self.assertEqual(len(themes), 2,
                         "package.json must contribute both dark + light themes")

        labels = {t.get("label") for t in themes}
        self.assertEqual(labels, {"Monad Dark", "Monad Light"})

        # Each theme entry must declare a uiTheme + path
        for entry in themes:
            self.assertIn("uiTheme", entry)
            self.assertIn("path", entry)
            self.assertTrue(entry["path"].endswith(".json"))

        # Dark→vs-dark, Light→vs
        by_label = {t["label"]: t for t in themes}
        self.assertEqual(by_label["Monad Dark"]["uiTheme"], "vs-dark")
        self.assertEqual(by_label["Monad Light"]["uiTheme"], "vs")

    def test_vscode_readme_and_license_non_empty(self):
        outputs = cc.prepare_templates(self._load_colors())
        # README references both themes by name
        self.assertIn("Monad Dark", outputs["vscode_readme"])
        self.assertIn("Monad Light", outputs["vscode_readme"])
        # LICENSE has a recognizable header
        license_text = outputs["vscode_license"]
        self.assertTrue(len(license_text) > 200,
                        "LICENSE looks suspiciously short")

    # ── draw.io exporter tests ─────────────────────────────────────────────

    def test_drawio_artifacts_emitted(self):
        outputs = cc.prepare_templates(self._load_colors())
        for key in ("drawio_styles_json", "drawio_stylesheet",
                    "drawio_example", "drawio_readme"):
            self.assertIn(key, outputs)
            self.assertTrue(outputs[key], f"{key} should be non-empty")

    def test_drawio_styles_json_is_valid_and_themed(self):
        import json as _json
        outputs = cc.prepare_templates(self._load_colors())
        data = _json.loads(outputs["drawio_styles_json"])
        self.assertIn("dark", data)
        self.assertIn("light", data)

        expected_tokens = {
            "monad.surface", "monad.layer-01", "monad.layer-02", "monad.layer-03",
            "monad.interactive", "monad.info", "monad.success",
            "monad.warning", "monad.error", "monad.highlight", "monad.disabled",
            "monad.text-primary", "monad.text-secondary", "monad.text-disabled",
            "monad.edge", "monad.edge-subtle",
            "monad.edge-interactive", "monad.edge-dashed",
            "monad.move-start", "monad.move-hand",
            "monad.move-foot", "monad.move-finish",
        }
        self.assertEqual(set(data["dark"].keys()), expected_tokens)
        self.assertEqual(set(data["light"].keys()), expected_tokens)

        # Every Monad rule encoded in node styles
        for token, style in data["dark"].items():
            if token.startswith("monad.edge") or token.startswith("monad.text"):
                continue
            self.assertIn("rounded=0", style, f"{token} must have rounded=0")
            self.assertIn("shadow=0", style, f"{token} must have shadow=0")
            self.assertIn("gradient=0", style, f"{token} must have gradient=0")

        # Every edge style is orthogonal and not rounded
        for token, style in data["dark"].items():
            if not token.startswith("monad.edge"):
                continue
            self.assertIn("edgeStyle=orthogonalEdgeStyle", style)
            self.assertIn("rounded=0", style)

    def test_drawio_dark_palette_token_propagates(self):
        import json as _json
        data = self._load_colors()
        modified = copy.deepcopy(data)
        info2 = "#13579B"
        modified["Default_Colors"]["Information_Indicators"]["Information_2"]["hex"] = info2
        outputs = cc.prepare_templates(modified)
        styles = _json.loads(outputs["drawio_styles_json"])

        # interactive node + edge in dark theme use the new hex
        self.assertIn(f"fillColor={info2}", styles["dark"]["monad.interactive"])
        self.assertIn(f"strokeColor={info2}", styles["dark"]["monad.interactive"])
        self.assertIn(f"strokeColor={info2}", styles["dark"]["monad.edge-interactive"])
        # And in the stylesheet snippet
        self.assertIn(f'value="{info2}"', outputs["drawio_stylesheet"])
        # Same token shared across themes — also present in light palette
        self.assertIn(f"fillColor={info2}", styles["light"]["monad.interactive"])

    def test_drawio_light_layer_token_propagates(self):
        import json as _json
        data = self._load_colors()
        modified = copy.deepcopy(data)
        layer1_light = "#F1F2F3"
        modified["Light_Mode"]["General_UI_Colors"]["Layer_01"]["hex"] = layer1_light
        outputs = cc.prepare_templates(modified)
        styles = _json.loads(outputs["drawio_styles_json"])

        self.assertIn(f"fillColor={layer1_light}", styles["light"]["monad.layer-01"])
        # Dark layer-01 unchanged
        self.assertNotIn(f"fillColor={layer1_light}",
                         styles["dark"]["monad.layer-01"])

    def test_drawio_stylesheet_is_valid_xml(self):
        import xml.etree.ElementTree as ET
        outputs = cc.prepare_templates(self._load_colors())
        tree = ET.fromstring(outputs["drawio_stylesheet"])
        self.assertEqual(tree.tag, "mxStylesheet")

        # Each style entry is wrapped in <add as="monad.*">
        names = {add.get("as") for add in tree.findall("./styles/add")}
        self.assertIn("monad.layer-01", names)
        self.assertIn("monad.interactive", names)
        self.assertIn("monad.edge", names)

    def test_drawio_example_passes_plugin_validation_rules(self):
        """Mirrors the validation in
        Desktop/drawio-amp/.amp/plugins/drawio.ts (ensureMxGraphModel +
        edge geometry rule). The example must be drop-in safe to feed
        into the drawio_create tool.
        """
        import xml.etree.ElementTree as ET
        outputs = cc.prepare_templates(self._load_colors())
        xml = outputs["drawio_example"].strip()

        # Rule 1: must start with <mxGraphModel
        self.assertTrue(xml.startswith("<mxGraphModel"),
                        f"example must start with <mxGraphModel>, got: {xml[:40]!r}")

        # Rule 2: zero XML comments
        self.assertNotIn("<!--", xml)

        # Rule 3: parses as well-formed XML
        root = ET.fromstring(xml)
        self.assertEqual(root.tag, "mxGraphModel")

        # Rule 4: every mxCell with edge="1" has a child
        # <mxGeometry relative="1" as="geometry" />
        edges = [c for c in root.iter("mxCell") if c.get("edge") == "1"]
        self.assertGreater(len(edges), 0, "example should include edge cells")
        for edge in edges:
            geom = edge.find("mxGeometry")
            self.assertIsNotNone(geom, "edge missing <mxGeometry>")
            self.assertEqual(geom.get("relative"), "1",
                             "edge geometry must have relative=\"1\"")
            self.assertEqual(geom.get("as"), "geometry",
                             "edge geometry must have as=\"geometry\"")

        # Rule 5: every mxCell id is unique
        ids = [c.get("id") for c in root.iter("mxCell")]
        self.assertEqual(len(ids), len(set(ids)),
                         "duplicate mxCell ids in example")


if __name__ == "__main__":
    unittest.main()
