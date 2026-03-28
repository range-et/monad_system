"""Generate SwiftUI Strata colors from the same inputs as monad.css."""


def create_swiftui_strata(
    *,
    bg_dark,
    layer01_dark,
    layer02_dark,
    layer03_dark,
    text_primary_dark,
    text_secondary_dark,
    text_disabled_dark,
    border_dark,
    border_subtle_dark,
    bg_light,
    layer01_light,
    layer02_light,
    layer03_light,
    text_primary_light,
    text_secondary_light,
    text_disabled_light,
    border_light,
    border_subtle_light,
    overlay_dark_alpha,
    overlay_light_alpha,
    interactive,
    interactive_hover,
    interactive_active,
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
    """Emit MonadStrata.swift — adaptive Color values aligned with --strata-*."""

    def esc(s):
        return s.replace("\\", "\\\\").replace('"', '\\"')

    # Overlay alpha values are passed from compile_color.py and mirror monad.css.
    return f'''// MonadStrata.swift
// Generated from colors.json — do not edit directly.
// Strata tokens mirror build/monad.css (--strata-*).

import SwiftUI

#if canImport(UIKit)
import UIKit
#endif
#if canImport(AppKit)
import AppKit
#endif

public enum MonadStrata {{

    // MARK: - Ground / type / structure (light / dark)

    public static let bg = _adaptive(
        light: "{esc(bg_light)}",
        dark: "{esc(bg_dark)}"
    )
    public static let layer01 = _adaptive(
        light: "{esc(layer01_light)}",
        dark: "{esc(layer01_dark)}"
    )
    public static let layer02 = _adaptive(
        light: "{esc(layer02_light)}",
        dark: "{esc(layer02_dark)}"
    )
    public static let layer03 = _adaptive(
        light: "{esc(layer03_light)}",
        dark: "{esc(layer03_dark)}"
    )

    public static let textPrimary = _adaptive(
        light: "{esc(text_primary_light)}",
        dark: "{esc(text_primary_dark)}"
    )
    public static let textSecondary = _adaptive(
        light: "{esc(text_secondary_light)}",
        dark: "{esc(text_secondary_dark)}"
    )
    public static let textDisabled = _adaptive(
        light: "{esc(text_disabled_light)}",
        dark: "{esc(text_disabled_dark)}"
    )

    public static let border = _adaptive(
        light: "{esc(border_light)}",
        dark: "{esc(border_dark)}"
    )
    public static let borderSubtle = _adaptive(
        light: "{esc(border_subtle_light)}",
        dark: "{esc(border_subtle_dark)}"
    )

    public static var overlay: Color {{
        #if os(macOS)
        Color(nsColor: NSColor(name: nil, dynamicProvider: {{ appearance in
            let dark = appearance.bestMatch(from: [.darkAqua, .aqua]) == .darkAqua
            return NSColor.black.withAlphaComponent(dark ? {overlay_dark_alpha:.2f} : {overlay_light_alpha:.2f})
        }})!)
        #else
        Color(uiColor: UIColor {{ traits in
            traits.userInterfaceStyle == .dark
                ? UIColor.black.withAlphaComponent({overlay_dark_alpha:.2f})
                : UIColor.black.withAlphaComponent({overlay_light_alpha:.2f})
        }})
        #endif
    }}

    // MARK: - Signal (shared + hover states)

    public static let interactive = Color(hex: "{esc(interactive)}")
    public static let interactiveHover = Color(hex: "{esc(interactive_hover)}")
    public static let interactiveActive = Color(hex: "{esc(interactive_active)}")

    // MARK: - Status

    public static let info = Color(hex: "{esc(support_info)}")
    public static let success = Color(hex: "{esc(support_success)}")
    public static let warning = Color(hex: "{esc(support_warning)}")
    public static let error = Color(hex: "{esc(support_error)}")

    public static let infoBg = info.opacity(0.10)
    public static let successBg = success.opacity(0.10)
    public static let warningBg = warning.opacity(0.10)
    public static let errorBg = error.opacity(0.10)

    // MARK: - Movement domain

    public static let moveStart = Color(hex: "{esc(move_start)}")
    public static let moveHand = Color(hex: "{esc(move_hand)}")
    public static let moveFoot = Color(hex: "{esc(move_foot)}")
    public static let moveFinish = Color(hex: "{esc(move_finish)}")

    // MARK: - Misc

    public static let highlight = Color(hex: "{esc(highlight)}")
    public static let disabled = Color(hex: "{esc(disabled)}")

    // MARK: - Adaptive helper

    fileprivate static func _adaptive(light: String, dark: String) -> Color {{
        #if os(macOS)
        Color(nsColor: NSColor(name: nil, dynamicProvider: {{ appearance in
            let isDark = appearance.bestMatch(from: [.darkAqua, .aqua]) == .darkAqua
            return NSColor(hex: isDark ? dark : light)
        }})!)
        #else
        Color(uiColor: UIColor {{ traits in
            UIColor(hex: traits.userInterfaceStyle == .dark ? dark : light)
        }})
        #endif
    }}
}}

// MARK: - Hex parsing

extension Color {{
    init(hex: String) {{
        let cleaned = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: cleaned).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch cleaned.count {{
        case 6:
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8:
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }}
        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue: Double(b) / 255,
            opacity: Double(a) / 255
        )
    }}
}}

#if canImport(UIKit)
extension UIColor {{
    convenience init(hex: String) {{
        let cleaned = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: cleaned).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch cleaned.count {{
        case 6:
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8:
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }}
        self.init(red: CGFloat(r) / 255, green: CGFloat(g) / 255, blue: CGFloat(b) / 255, alpha: CGFloat(a) / 255)
    }}
}}
#endif

#if canImport(AppKit)
extension NSColor {{
    convenience init(hex: String) {{
        let cleaned = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: cleaned).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch cleaned.count {{
        case 6:
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8:
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }}
        self.init(
            red: CGFloat(r) / 255,
            green: CGFloat(g) / 255,
            blue: CGFloat(b) / 255,
            alpha: CGFloat(a) / 255
        )
    }}
}}
#endif
'''
