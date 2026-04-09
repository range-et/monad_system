"""C++ / Arduino header generators for the Monad Design System.

Target environments
-------------------
* Arduino (AVR, SAMD, ESP32, ESP8266, RP2040, STM32)
* Bare-metal embedded — e-ink (Waveshare/GxEPD), OLED (SSD1306),
  TFT (ST7735/ILI9341/TFT_eSPI), LED matrices, LVGL.
* Any C++11+ project.

Design goals
------------
* Header-only. No STL. No dynamic allocation. No PROGMEM macros required —
  ``constexpr`` literals fold into the instruction stream on AVR.
* RGB888 source-of-truth (uint32_t, ``0x00RRGGBB``).
* Constexpr conversions to RGB565, 8-bit grayscale, and 1-bit monochrome
  so a single token works on a TFT, an OLED, and a B&W e-ink panel.
* Two namespaces — ``monad::dark`` and ``monad::light`` — plus a
  ``monad::theme`` alias selectable with ``MONAD_LIGHT_THEME``.
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _hex_to_uint32(hex_color):
    """``'#0F1113'`` → ``0x0F1113`` (int). Strips a leading ``#`` and any
    trailing 8-digit alpha so the result is always 24-bit RGB888."""
    h = hex_color.lstrip("#")
    if len(h) == 8:
        h = h[:6]
    return int(h, 16)


def _fmt_const(name, hex_value, indent="    ", width=18):
    v = _hex_to_uint32(hex_value)
    pad = max(1, width - len(name))
    return f"{indent}constexpr uint32_t {name}{' ' * pad}= 0x{v:06X};"


def _parse_bezier(css_value):
    """Extract (x1, y1, x2, y2) floats from a CSS cubic-bezier() string.
    Returns ``None`` for ``"linear"`` or any unrecognised input.
    """
    import re
    m = re.match(
        r"cubic-bezier\(\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^)]+)\)",
        css_value.strip(),
    )
    if not m:
        return None
    return tuple(float(v) for v in m.groups())


# ---------------------------------------------------------------------------
# MonadPalette.h
# ---------------------------------------------------------------------------

def create_cpp_palette_header(
    *,
    # Dark theme surfaces / text / borders
    bg_dark,
    layer01_dark,
    layer02_dark,
    layer03_dark,
    text_primary_dark,
    text_secondary_dark,
    text_disabled_dark,
    border_dark,
    border_subtle_dark,
    # Light theme surfaces / text / borders
    bg_light,
    layer01_light,
    layer02_light,
    layer03_light,
    text_primary_light,
    text_secondary_light,
    text_disabled_light,
    border_light,
    border_subtle_light,
    # Shared semantic / brand tokens
    interactive,
    support_info,
    support_success,
    support_warning,
    support_error,
    highlight,
    disabled,
    move_start,
    move_hand,
    move_foot,
    move_finish,
):
    """Return the contents of ``MonadPalette.h``."""

    shared = [
        ("INTERACTIVE",     interactive),
        ("SUPPORT_INFO",    support_info),
        ("SUPPORT_SUCCESS", support_success),
        ("SUPPORT_WARNING", support_warning),
        ("SUPPORT_ERROR",   support_error),
        ("HIGHLIGHT",       highlight),
        ("DISABLED",        disabled),
        ("MOVE_START",      move_start),
        ("MOVE_HAND",       move_hand),
        ("MOVE_FOOT",       move_foot),
        ("MOVE_FINISH",     move_finish),
    ]
    dark = [
        ("BACKGROUND",     bg_dark),
        ("LAYER_01",       layer01_dark),
        ("LAYER_02",       layer02_dark),
        ("LAYER_03",       layer03_dark),
        ("TEXT_PRIMARY",   text_primary_dark),
        ("TEXT_SECONDARY", text_secondary_dark),
        ("TEXT_DISABLED",  text_disabled_dark),
        ("BORDER",         border_dark),
        ("BORDER_SUBTLE",  border_subtle_dark),
    ]
    light = [
        ("BACKGROUND",     bg_light),
        ("LAYER_01",       layer01_light),
        ("LAYER_02",       layer02_light),
        ("LAYER_03",       layer03_light),
        ("TEXT_PRIMARY",   text_primary_light),
        ("TEXT_SECONDARY", text_secondary_light),
        ("TEXT_DISABLED",  text_disabled_light),
        ("BORDER",         border_light),
        ("BORDER_SUBTLE",  border_subtle_light),
    ]

    lines = [
        "// MonadPalette.h",
        "// Generated from colors.json — do not edit directly.",
        "// Monad Design System — header-only C++ palette for Arduino, ESP32,",
        "// e-ink, OLED, TFT, and other embedded displays.",
        "//",
        "// Source of truth is 24-bit RGB888 (uint32_t, 0x00RRGGBB). Use the",
        "// constexpr helpers rgb565(), gray8(), mono() to downsample for the",
        "// display you are targeting — the compiler folds them to literals.",
        "",
        "#pragma once",
        "",
        "#include <stdint.h>",
        "",
        "namespace monad {",
        "",
        "// ── Format conversion helpers ──────────────────────────────────────────",
        "// RGB888 source colors are packed as 0x00RRGGBB in a uint32_t.",
        "",
        "constexpr uint8_t r8(uint32_t c) { return (uint8_t)((c >> 16) & 0xFF); }",
        "constexpr uint8_t g8(uint32_t c) { return (uint8_t)((c >>  8) & 0xFF); }",
        "constexpr uint8_t b8(uint32_t c) { return (uint8_t)( c        & 0xFF); }",
        "",
        "// RGB565 — colour TFTs and most colour e-ink drivers",
        "// (Adafruit GFX, TFT_eSPI, LVGL, GxEPD2 colour modes).",
        "constexpr uint16_t rgb565(uint32_t c) {",
        "    return (uint16_t)(((r8(c) & 0xF8) << 8)",
        "                    | ((g8(c) & 0xFC) << 3)",
        "                    |  (b8(c) >> 3));",
        "}",
        "",
        "// 8-bit grayscale using Rec. 601 luma. Integer-only, AVR-safe.",
        "constexpr uint8_t gray8(uint32_t c) {",
        "    return (uint8_t)((r8(c) * 77 + g8(c) * 150 + b8(c) * 29) >> 8);",
        "}",
        "",
        "// 1-bit monochrome — for SSD1306 OLEDs and B&W e-ink",
        "// (Waveshare, GxEPD2). Returns true when the colour is closer to",
        "// white than black (the standard 1-bit imaging convention). For",
        "// e-ink panels where 'true == ink on paper' you typically want the",
        "// inverted form: bool ink = !mono(token);",
        "constexpr bool mono(uint32_t c, uint8_t threshold = 128) {",
        "    return gray8(c) >= threshold;",
        "}",
        "",
        "// ── Dark theme (default) ───────────────────────────────────────────────",
        "namespace dark {",
    ]
    for name, val in dark:
        lines.append(_fmt_const(name, val))
    lines.append("")
    lines.append("    // Shared semantic tokens")
    for name, val in shared:
        lines.append(_fmt_const(name, val))
    lines.append("}  // namespace dark")
    lines.append("")
    lines.append("// ── Light theme ────────────────────────────────────────────────────────")
    lines.append("namespace light {")
    for name, val in light:
        lines.append(_fmt_const(name, val))
    lines.append("")
    lines.append("    // Shared semantic tokens")
    for name, val in shared:
        lines.append(_fmt_const(name, val))
    lines.append("}  // namespace light")
    lines.append("")
    lines.append("// ── Active theme alias ─────────────────────────────────────────────────")
    lines.append("// Dark is the default. Define MONAD_LIGHT_THEME before including to flip.")
    lines.append("#ifdef MONAD_LIGHT_THEME")
    lines.append("namespace theme = light;")
    lines.append("#else")
    lines.append("namespace theme = dark;")
    lines.append("#endif")
    lines.append("")
    lines.append("}  // namespace monad")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# MonadMotion.h
# ---------------------------------------------------------------------------

def create_cpp_motion_header(motion):
    """Return the contents of ``MonadMotion.h``.

    Falls back to the legacy hardcoded fast/base/slow values when no
    ``Motion`` block is present in ``colors.json`` (mirrors the behaviour
    of every other motion generator).
    """
    lines = [
        "// MonadMotion.h",
        "// Generated from colors.json — do not edit directly.",
        "// Monad Design System — motion tokens for embedded C++.",
        "//",
        "// Durations are uint16_t milliseconds (fits comfortably in AVR).",
        "// Easings are cubic-bezier control points (floats) — pair with",
        "// your own interpolator, or feed straight into LVGL anim_path_cb.",
        "",
        "#pragma once",
        "",
        "#include <stdint.h>",
        "",
        "namespace monad {",
        "namespace motion {",
        "",
    ]

    if not motion:
        lines += [
            "// Legacy fallback — no Motion block present in colors.json.",
            "constexpr uint16_t DURATION_FAST_MS   = 80;",
            "constexpr uint16_t DURATION_BASE_MS   = 160;",
            "constexpr uint16_t DURATION_SLOW_MS   = 280;",
            "",
            "}  // namespace motion",
            "}  // namespace monad",
            "",
        ]
        return "\n".join(lines)

    durations = motion.get("durations", {})
    easings = motion.get("easings", {})

    lines.append("// ── Durations (milliseconds) ───────────────────────────────────────────")
    for key, val in durations.items():
        ms = val["ms"]
        name = f"DURATION_{key.upper()}_MS"
        pad = max(1, 22 - len(name))
        lines.append(f"constexpr uint16_t {name}{' ' * pad}= {ms};")

    lines.append("")
    lines.append("// ── Easing curves (cubic-bezier control points) ────────────────────────")
    lines.append("struct Bezier { float x1, y1, x2, y2; };")
    lines.append("")

    for key, val in easings.items():
        css_val = val["css"]
        pts = _parse_bezier(css_val)
        # JSON keys are e.g. "ease_out" / "linear" — avoid producing
        # double-prefixed identifiers like EASE_EASE_OUT.
        name = key.upper() if key.startswith("ease_") else "EASE_" + key.upper()
        if pts is None:
            lines.append(f"// {name}: linear — no bezier control points needed")
            continue
        lines.append(
            f"constexpr Bezier {name} = {{ "
            f"{pts[0]}f, {pts[1]}f, {pts[2]}f, {pts[3]}f }};"
        )

    lines.append("")
    lines.append("// ── Interpolation helpers — handy for LED fades and frame timing ───────")
    lines.append("constexpr uint8_t lerp_u8(uint8_t a, uint8_t b, float t) {")
    lines.append("    return (uint8_t)((float)a + ((float)b - (float)a) * t);")
    lines.append("}")
    lines.append("")
    lines.append("// Linear-interpolate two RGB888 colours by t in [0, 1].")
    lines.append("// Useful for fading between Monad palette tokens on RGB LEDs.")
    lines.append("constexpr uint32_t lerp_rgb(uint32_t a, uint32_t b, float t) {")
    lines.append("    return ((uint32_t)lerp_u8((uint8_t)((a >> 16) & 0xFF),")
    lines.append("                              (uint8_t)((b >> 16) & 0xFF), t) << 16)")
    lines.append("         | ((uint32_t)lerp_u8((uint8_t)((a >>  8) & 0xFF),")
    lines.append("                              (uint8_t)((b >>  8) & 0xFF), t) <<  8)")
    lines.append("         |  (uint32_t)lerp_u8((uint8_t)( a        & 0xFF),")
    lines.append("                              (uint8_t)( b        & 0xFF), t);")
    lines.append("}")
    lines.append("")
    lines.append("}  // namespace motion")
    lines.append("}  // namespace monad")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Monad.h — umbrella header
# ---------------------------------------------------------------------------

def create_cpp_umbrella_header():
    return """\
// Monad.h — umbrella header for the Monad Design System C++ library.
// Generated from colors.json — do not edit directly.
//
// Usage (Arduino + TFT_eSPI / Adafruit GFX):
//
//   #include <Monad.h>
//   using namespace monad;
//   tft.fillScreen(rgb565(theme::BACKGROUND));
//   tft.setTextColor(rgb565(theme::TEXT_PRIMARY), rgb565(theme::BACKGROUND));
//   tft.drawRect(0, 0, 100, 20, rgb565(theme::INTERACTIVE));
//
// Usage (SSD1306 OLED — pixel-on means white-on-black):
//
//   #include <Monad.h>
//   using namespace monad;
//   if (mono(theme::INTERACTIVE)) display.drawPixel(x, y, SSD1306_WHITE);
//
// Usage (Waveshare / GxEPD2 monochrome e-ink — ink on paper):
//
//   #define MONAD_LIGHT_THEME    // paper-like UI uses the light theme
//   #include <Monad.h>
//   using namespace monad;
//   // mono() returns true when the colour is closer to white. For e-ink
//   // we want the *dark* tokens drawn as ink, so invert with !mono.
//   uint16_t fg = !mono(theme::TEXT_PRIMARY) ? GxEPD_BLACK : GxEPD_WHITE;
//   display.setTextColor(fg);
//
// Switch theme: define MONAD_LIGHT_THEME before including this header.
//   #define MONAD_LIGHT_THEME
//   #include <Monad.h>

#pragma once

#include "MonadPalette.h"
#include "MonadMotion.h"
"""


# ---------------------------------------------------------------------------
# Arduino library metadata
# ---------------------------------------------------------------------------

def create_cpp_library_properties():
    return """\
name=Monad
version=1.0.0
author=Monad System
maintainer=Monad System
sentence=Monad Design System palette and motion tokens for embedded C++.
paragraph=Header-only library exposing the Monad Design System palette and motion tokens for Arduino, ESP32, e-ink, OLED, and TFT displays. Constexpr RGB888 source with zero-cost RGB565, 8-bit grayscale, and 1-bit monochrome conversions so one token set drives every display class.
category=Display
url=https://github.com/monad-system/monad
architectures=*
includes=Monad.h
"""


def create_cpp_keywords():
    """Arduino IDE syntax-highlight file. Tabs are required between
    identifier and KEYWORD class — the IDE parser is strict."""
    return (
        "Monad\tKEYWORD1\n"
        "monad\tKEYWORD1\n"
        "dark\tKEYWORD1\n"
        "light\tKEYWORD1\n"
        "theme\tKEYWORD1\n"
        "motion\tKEYWORD1\n"
        "Bezier\tKEYWORD1\n"
        "\n"
        "rgb565\tKEYWORD2\n"
        "gray8\tKEYWORD2\n"
        "mono\tKEYWORD2\n"
        "r8\tKEYWORD2\n"
        "g8\tKEYWORD2\n"
        "b8\tKEYWORD2\n"
        "lerp_u8\tKEYWORD2\n"
        "lerp_rgb\tKEYWORD2\n"
        "\n"
        "BACKGROUND\tLITERAL1\n"
        "LAYER_01\tLITERAL1\n"
        "LAYER_02\tLITERAL1\n"
        "LAYER_03\tLITERAL1\n"
        "TEXT_PRIMARY\tLITERAL1\n"
        "TEXT_SECONDARY\tLITERAL1\n"
        "TEXT_DISABLED\tLITERAL1\n"
        "BORDER\tLITERAL1\n"
        "BORDER_SUBTLE\tLITERAL1\n"
        "INTERACTIVE\tLITERAL1\n"
        "SUPPORT_INFO\tLITERAL1\n"
        "SUPPORT_SUCCESS\tLITERAL1\n"
        "SUPPORT_WARNING\tLITERAL1\n"
        "SUPPORT_ERROR\tLITERAL1\n"
        "HIGHLIGHT\tLITERAL1\n"
        "DISABLED\tLITERAL1\n"
        "MOVE_START\tLITERAL1\n"
        "MOVE_HAND\tLITERAL1\n"
        "MOVE_FOOT\tLITERAL1\n"
        "MOVE_FINISH\tLITERAL1\n"
        "DURATION_FAST_MS\tLITERAL1\n"
        "DURATION_BASE_MS\tLITERAL1\n"
        "DURATION_SLOW_MS\tLITERAL1\n"
        "DURATION_SLOWER_MS\tLITERAL1\n"
        "EASE_OUT\tLITERAL1\n"
        "EASE_IN\tLITERAL1\n"
        "EASE_IN_OUT\tLITERAL1\n"
    )
