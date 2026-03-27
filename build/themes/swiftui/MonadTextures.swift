// MonadTextures.swift — Monad Design System
// Generated from colors.json — do not edit directly.
//
// Provides tileable texture patterns as SwiftUI views.
// Usage:
//   Rectangle().monadTexture(.dot)
//   Rectangle().monadTexture(.hatchFwd, color: MonadStrata.interactive)

import SwiftUI

// MARK: - Texture Enum

public enum MonadTexture: String, CaseIterable {
    case dot      = "dot"
    case hatchV   = "hatch-v"
    case hatchH   = "hatch-h"
    case hatchX   = "hatch-x"
    case hatchFwd = "hatch-fwd"
    case hatchBwd = "hatch-bwd"

    /// Cell spacing in points (from colors.json).
    public var spacing: CGFloat {
        switch self {
        case .dot:      return 12
        case .hatchV:   return 8
        case .hatchH:   return 8
        case .hatchX:   return 8
        case .hatchFwd: return 10
        case .hatchBwd: return 10
        }
    }

    /// Stroke width or dot radius in points.
    public var strokeSize: CGFloat {
        switch self {
        case .dot:      return 1.5
        case .hatchV:   return 1
        case .hatchH:   return 1
        case .hatchX:   return 1
        case .hatchFwd: return 1
        case .hatchBwd: return 1
        }
    }
}

// MARK: - Pattern View

public struct TexturePatternView: View {
    public let texture: MonadTexture
    public let color: Color
    public let opacity: Double

    public init(texture: MonadTexture, color: Color, opacity: Double = 0.6) {
        self.texture = texture
        self.color = color
        self.opacity = opacity
    }

    public var body: some View {
        Canvas { context, size in
            let sp = texture.spacing
            let cols = Int(ceil(size.width / sp)) + 1
            let rows = Int(ceil(size.height / sp)) + 1

            context.opacity = opacity

            switch texture {
            case .dot:
                let r = texture.strokeSize
                for row in 0..<rows {
                    for col in 0..<cols {
                        let cx = CGFloat(col) * sp + sp / 2
                        let cy = CGFloat(row) * sp + sp / 2
                        let rect = CGRect(x: cx - r, y: cy - r, width: r * 2, height: r * 2)
                        context.fill(Ellipse().path(in: rect), with: .color(color))
                    }
                }

            case .hatchV:
                let sw = texture.strokeSize
                for col in 0..<cols {
                    let x = CGFloat(col) * sp + sp / 2
                    let rect = CGRect(x: x - sw / 2, y: 0, width: sw, height: size.height)
                    context.fill(Rectangle().path(in: rect), with: .color(color))
                }

            case .hatchH:
                let sw = texture.strokeSize
                for row in 0..<rows {
                    let y = CGFloat(row) * sp + sp / 2
                    let rect = CGRect(x: 0, y: y - sw / 2, width: size.width, height: sw)
                    context.fill(Rectangle().path(in: rect), with: .color(color))
                }

            case .hatchX:
                let sw = texture.strokeSize
                for col in 0..<cols {
                    let x = CGFloat(col) * sp + sp / 2
                    let rect = CGRect(x: x - sw / 2, y: 0, width: sw, height: size.height)
                    context.fill(Rectangle().path(in: rect), with: .color(color))
                }
                for row in 0..<rows {
                    let y = CGFloat(row) * sp + sp / 2
                    let rect = CGRect(x: 0, y: y - sw / 2, width: size.width, height: sw)
                    context.fill(Rectangle().path(in: rect), with: .color(color))
                }

            case .hatchFwd:
                let sw = texture.strokeSize
                for offset in -(rows)...(cols + rows) {
                    var path = Path()
                    let startX = CGFloat(offset) * sp
                    path.move(to: CGPoint(x: startX, y: 0))
                    path.addLine(to: CGPoint(x: startX - size.height, y: size.height))
                    context.stroke(path, with: .color(color), lineWidth: sw)
                }

            case .hatchBwd:
                let sw = texture.strokeSize
                for offset in -(rows)...(cols + rows) {
                    var path = Path()
                    let startX = CGFloat(offset) * sp
                    path.move(to: CGPoint(x: startX, y: 0))
                    path.addLine(to: CGPoint(x: startX + size.height, y: size.height))
                    context.stroke(path, with: .color(color), lineWidth: sw)
                }
            }
        }
    }
}

// MARK: - View Modifier

extension View {
    /// Overlay a repeating Monad texture pattern.
    public func monadTexture(_ texture: MonadTexture, color: Color = .primary, opacity: Double = 0.6) -> some View {
        self.overlay(TexturePatternView(texture: texture, color: color, opacity: opacity))
    }
}
