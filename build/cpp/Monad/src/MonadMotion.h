// MonadMotion.h
// Generated from colors.json — do not edit directly.
// Monad Design System — motion tokens for embedded C++.
//
// Durations are uint16_t milliseconds (fits comfortably in AVR).
// Easings are cubic-bezier control points (floats) — pair with
// your own interpolator, or feed straight into LVGL anim_path_cb.

#pragma once

#include <stdint.h>

namespace monad {
namespace motion {

// ── Durations (milliseconds) ───────────────────────────────────────────
constexpr uint16_t DURATION_FAST_MS      = 80;
constexpr uint16_t DURATION_BASE_MS      = 160;
constexpr uint16_t DURATION_SLOW_MS      = 280;
constexpr uint16_t DURATION_SLOWER_MS    = 440;

// ── Easing curves (cubic-bezier control points) ────────────────────────
struct Bezier { float x1, y1, x2, y2; };

// EASE_LINEAR: linear — no bezier control points needed
constexpr Bezier EASE_OUT = { 0.16f, 1.0f, 0.3f, 1.0f };
constexpr Bezier EASE_IN = { 0.7f, 0.0f, 0.84f, 0.0f };
constexpr Bezier EASE_IN_OUT = { 0.65f, 0.0f, 0.35f, 1.0f };

// ── Interpolation helpers — handy for LED fades and frame timing ───────
constexpr uint8_t lerp_u8(uint8_t a, uint8_t b, float t) {
    return (uint8_t)((float)a + ((float)b - (float)a) * t);
}

// Linear-interpolate two RGB888 colours by t in [0, 1].
// Useful for fading between Monad palette tokens on RGB LEDs.
constexpr uint32_t lerp_rgb(uint32_t a, uint32_t b, float t) {
    return ((uint32_t)lerp_u8((uint8_t)((a >> 16) & 0xFF),
                              (uint8_t)((b >> 16) & 0xFF), t) << 16)
         | ((uint32_t)lerp_u8((uint8_t)((a >>  8) & 0xFF),
                              (uint8_t)((b >>  8) & 0xFF), t) <<  8)
         |  (uint32_t)lerp_u8((uint8_t)( a        & 0xFF),
                              (uint8_t)( b        & 0xFF), t);
}

}  // namespace motion
}  // namespace monad
