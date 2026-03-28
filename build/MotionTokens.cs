// MotionTokens.cs
// Generated from colors.json — do not edit directly.

using UnityEngine;

namespace Utility
{
    public static class MotionTokens
    {
        // Durations (seconds)
        public const float DurationFast        = 0.080f;
        public const float DurationBase        = 0.160f;
        public const float DurationSlow        = 0.280f;
        public const float DurationSlower      = 0.440f;

        // Easing curves (cubic-bezier control points)
        public static AnimationCurve EaseOut => AnimationCurve.EaseInOut(0f, 0f, 1f, 1f);
        // CSS: cubic-bezier(0.16, 1, 0.3, 1)
        public static AnimationCurve EaseIn => AnimationCurve.EaseInOut(0f, 0f, 1f, 1f);
        // CSS: cubic-bezier(0.7, 0, 0.84, 0)
        public static AnimationCurve EaseInOut => AnimationCurve.EaseInOut(0f, 0f, 1f, 1f);
        // CSS: cubic-bezier(0.65, 0, 0.35, 1)
    }
}
