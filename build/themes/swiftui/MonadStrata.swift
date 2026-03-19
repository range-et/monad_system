// MonadStrata.swift
// Generated from colors.json — do not edit directly.
// Strata tokens mirror build/monad.css (--strata-*).

import SwiftUI

#if canImport(UIKit)
import UIKit
#endif
#if canImport(AppKit)
import AppKit
#endif

public enum MonadStrata {

    // MARK: - Ground / type / structure (light / dark)

    public static let bg = _adaptive(
        light: "#F2F4F7",
        dark: "#0F1113"
    )
    public static let layer01 = _adaptive(
        light: "#ffffff",
        dark: "#171A1E"
    )
    public static let layer02 = _adaptive(
        light: "#EDF1F5",
        dark: "#1F242B"
    )
    public static let layer03 = _adaptive(
        light: "#E3E8EE",
        dark: "#2A313A"
    )

    public static let textPrimary = _adaptive(
        light: "#141A22",
        dark: "#EEF2F6"
    )
    public static let textSecondary = _adaptive(
        light: "#4F5A69",
        dark: "#B6BFCC"
    )
    public static let textDisabled = _adaptive(
        light: "#7E8998",
        dark: "#7D8794"
    )

    public static let border = _adaptive(
        light: "#BCC6D2",
        dark: "#3A434F"
    )
    public static let borderSubtle = _adaptive(
        light: "#D8DFE7",
        dark: "#2B323A"
    )

    public static var overlay: Color {
        #if os(macOS)
        Color(nsColor: NSColor(name: nil, dynamicProvider: { appearance in
            let dark = appearance.bestMatch(from: [.darkAqua, .aqua]) == .darkAqua
            return NSColor.black.withAlphaComponent(dark ? 0.65 : 0.24)
        })!)
        #else
        Color(uiColor: UIColor { traits in
            traits.userInterfaceStyle == .dark
                ? UIColor.black.withAlphaComponent(0.65)
                : UIColor.black.withAlphaComponent(0.24)
        })
        #endif
    }

    // MARK: - Signal (shared + hover states)

    public static let interactive = Color(hex: "#1E88C8")
    public static let interactiveHover = Color(hex: "#1973AA")
    public static let interactiveActive = Color(hex: "#166696")

    // MARK: - Status

    public static let info = Color(hex: "#2B9ED1")
    public static let success = Color(hex: "#6EAD45")
    public static let warning = Color(hex: "#D7A12A")
    public static let error = Color(hex: "#D64C45")

    public static let infoBg = info.opacity(0.10)
    public static let successBg = success.opacity(0.10)
    public static let warningBg = warning.opacity(0.10)
    public static let errorBg = error.opacity(0.10)

    // MARK: - Movement domain

    public static let moveStart = Color(hex: "#4CAF50")
    public static let moveHand = Color(hex: "#03A9F4")
    public static let moveFoot = Color(hex: "#FFEB3B")
    public static let moveFinish = Color(hex: "#9C27B0")

    // MARK: - Misc

    public static let highlight = Color(hex: "#FFEB3B")
    public static let disabled = Color(hex: "#757575")

    /// Matches CSS `var(--threshold-fast)` (80ms linear).
    public static let thresholdFastSeconds: Double = 0.08

    // MARK: - Adaptive helper

    fileprivate static func _adaptive(light: String, dark: String) -> Color {
        #if os(macOS)
        Color(nsColor: NSColor(name: nil, dynamicProvider: { appearance in
            let isDark = appearance.bestMatch(from: [.darkAqua, .aqua]) == .darkAqua
            return NSColor(hex: isDark ? dark : light)
        })!)
        #else
        Color(uiColor: UIColor { traits in
            UIColor(hex: traits.userInterfaceStyle == .dark ? dark : light)
        })
        #endif
    }
}

// MARK: - Hex parsing

extension Color {
    init(hex: String) {
        let cleaned = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: cleaned).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch cleaned.count {
        case 6:
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8:
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }
        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue: Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}

#if canImport(UIKit)
extension UIColor {
    convenience init(hex: String) {
        let cleaned = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: cleaned).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch cleaned.count {
        case 6:
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8:
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }
        self.init(red: CGFloat(r) / 255, green: CGFloat(g) / 255, blue: CGFloat(b) / 255, alpha: CGFloat(a) / 255)
    }
}
#endif

#if canImport(AppKit)
extension NSColor {
    convenience init(hex: String) {
        let cleaned = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: cleaned).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch cleaned.count {
        case 6:
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8:
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }
        self.init(
            red: CGFloat(r) / 255,
            green: CGFloat(g) / 255,
            blue: CGFloat(b) / 255,
            alpha: CGFloat(a) / 255
        )
    }
}
#endif
