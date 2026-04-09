// MonadPalette.h
// Generated from colors.json — do not edit directly.
// Monad Design System — header-only C++ palette for Arduino, ESP32,
// e-ink, OLED, TFT, and other embedded displays.
//
// Source of truth is 24-bit RGB888 (uint32_t, 0x00RRGGBB). Use the
// constexpr helpers rgb565(), gray8(), mono() to downsample for the
// display you are targeting — the compiler folds them to literals.

#pragma once

#include <stdint.h>

namespace monad {

// ── Format conversion helpers ──────────────────────────────────────────
// RGB888 source colors are packed as 0x00RRGGBB in a uint32_t.

constexpr uint8_t r8(uint32_t c) { return (uint8_t)((c >> 16) & 0xFF); }
constexpr uint8_t g8(uint32_t c) { return (uint8_t)((c >>  8) & 0xFF); }
constexpr uint8_t b8(uint32_t c) { return (uint8_t)( c        & 0xFF); }

// RGB565 — colour TFTs and most colour e-ink drivers
// (Adafruit GFX, TFT_eSPI, LVGL, GxEPD2 colour modes).
constexpr uint16_t rgb565(uint32_t c) {
    return (uint16_t)(((r8(c) & 0xF8) << 8)
                    | ((g8(c) & 0xFC) << 3)
                    |  (b8(c) >> 3));
}

// 8-bit grayscale using Rec. 601 luma. Integer-only, AVR-safe.
constexpr uint8_t gray8(uint32_t c) {
    return (uint8_t)((r8(c) * 77 + g8(c) * 150 + b8(c) * 29) >> 8);
}

// 1-bit monochrome — for SSD1306 OLEDs and B&W e-ink
// (Waveshare, GxEPD2). Returns true when the colour is closer to
// white than black (the standard 1-bit imaging convention). For
// e-ink panels where 'true == ink on paper' you typically want the
// inverted form: bool ink = !mono(token);
constexpr bool mono(uint32_t c, uint8_t threshold = 128) {
    return gray8(c) >= threshold;
}

// ── Dark theme (default) ───────────────────────────────────────────────
namespace dark {
    constexpr uint32_t BACKGROUND        = 0x0F1113;
    constexpr uint32_t LAYER_01          = 0x171A1E;
    constexpr uint32_t LAYER_02          = 0x1F242B;
    constexpr uint32_t LAYER_03          = 0x2A313A;
    constexpr uint32_t TEXT_PRIMARY      = 0xEEF2F6;
    constexpr uint32_t TEXT_SECONDARY    = 0xB6BFCC;
    constexpr uint32_t TEXT_DISABLED     = 0x7D8794;
    constexpr uint32_t BORDER            = 0x3A434F;
    constexpr uint32_t BORDER_SUBTLE     = 0x2B323A;

    // Shared semantic tokens
    constexpr uint32_t INTERACTIVE       = 0x1E88C8;
    constexpr uint32_t SUPPORT_INFO      = 0x2B9ED1;
    constexpr uint32_t SUPPORT_SUCCESS   = 0x6EAD45;
    constexpr uint32_t SUPPORT_WARNING   = 0xD7A12A;
    constexpr uint32_t SUPPORT_ERROR     = 0xD64C45;
    constexpr uint32_t HIGHLIGHT         = 0xFFEB3B;
    constexpr uint32_t DISABLED          = 0x757575;
    constexpr uint32_t MOVE_START        = 0x4CAF50;
    constexpr uint32_t MOVE_HAND         = 0x03A9F4;
    constexpr uint32_t MOVE_FOOT         = 0xFFEB3B;
    constexpr uint32_t MOVE_FINISH       = 0x9C27B0;
}  // namespace dark

// ── Light theme ────────────────────────────────────────────────────────
namespace light {
    constexpr uint32_t BACKGROUND        = 0xF2F4F7;
    constexpr uint32_t LAYER_01          = 0xFFFFFF;
    constexpr uint32_t LAYER_02          = 0xEDF1F5;
    constexpr uint32_t LAYER_03          = 0xE3E8EE;
    constexpr uint32_t TEXT_PRIMARY      = 0x141A22;
    constexpr uint32_t TEXT_SECONDARY    = 0x4F5A69;
    constexpr uint32_t TEXT_DISABLED     = 0x7E8998;
    constexpr uint32_t BORDER            = 0xBCC6D2;
    constexpr uint32_t BORDER_SUBTLE     = 0xD8DFE7;

    // Shared semantic tokens
    constexpr uint32_t INTERACTIVE       = 0x1E88C8;
    constexpr uint32_t SUPPORT_INFO      = 0x2B9ED1;
    constexpr uint32_t SUPPORT_SUCCESS   = 0x6EAD45;
    constexpr uint32_t SUPPORT_WARNING   = 0xD7A12A;
    constexpr uint32_t SUPPORT_ERROR     = 0xD64C45;
    constexpr uint32_t HIGHLIGHT         = 0xFFEB3B;
    constexpr uint32_t DISABLED          = 0x757575;
    constexpr uint32_t MOVE_START        = 0x4CAF50;
    constexpr uint32_t MOVE_HAND         = 0x03A9F4;
    constexpr uint32_t MOVE_FOOT         = 0xFFEB3B;
    constexpr uint32_t MOVE_FINISH       = 0x9C27B0;
}  // namespace light

// ── Active theme alias ─────────────────────────────────────────────────
// Dark is the default. Define MONAD_LIGHT_THEME before including to flip.
#ifdef MONAD_LIGHT_THEME
namespace theme = light;
#else
namespace theme = dark;
#endif

}  // namespace monad
