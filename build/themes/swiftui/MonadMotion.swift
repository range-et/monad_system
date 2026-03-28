// MonadMotion.swift
// Generated from colors.json — do not edit directly.
// Motion tokens mirror build/monad.css (--threshold-*).

import SwiftUI

public enum MonadMotion {

    // MARK: - Durations (seconds)

    public static let durationFast:      Double = 0.080
    public static let durationBase:      Double = 0.160
    public static let durationSlow:      Double = 0.280
    public static let durationSlower:    Double = 0.440

    // MARK: - Easing curves

    public static let easeOut = Animation.timingCurve(0.16, 1.0, 0.3, 1.0)
    public static let easeIn = Animation.timingCurve(0.7, 0.0, 0.84, 0.0)
    public static let easeInOut = Animation.timingCurve(0.65, 0.0, 0.35, 1.0)
}
