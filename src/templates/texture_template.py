"""Texture / pattern generators for the Monad Design System.

Each public function receives the raw ``textures`` dict extracted from
``colors.json["Textures"]`` and returns a formatted string artifact.
"""

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _svg_encode(raw):
    """Minimal percent-encoding for inline SVG in CSS url().

    Only encodes the characters that must be escaped in a data URI
    wrapped in double quotes.  Keeps the SVG human-readable.
    """
    return raw.replace("#", "%23")


def _svg_data_uri(svg_body, width, height):
    """Wrap an SVG body in a full SVG element and return a CSS url() data URI."""
    raw = (
        f"<svg xmlns='http://www.w3.org/2000/svg' "
        f"width='{width}' height='{height}'>{svg_body}</svg>"
    )
    return f'url("data:image/svg+xml,{_svg_encode(raw)}")'


def _build_svg_uris(textures_data):
    """Return ``{id: css_url_string}`` for every texture definition."""
    uris = {}
    for key, t in textures_data.items():
        tid = t["id"]
        sp = t["spacing"]
        op = t["opacity"]

        if tid == "dot":
            r = t.get("radius", 1.5)
            cx = sp / 2
            cy = sp / 2
            body = (
                f"<circle cx='{cx}' cy='{cy}' r='{r}' "
                f"fill='black' fill-opacity='{op}'/>"
            )
            uris[tid] = _svg_data_uri(body, sp, sp)

        elif tid == "hatch-v":
            sw = t.get("stroke_width", 1)
            x = sp / 2
            body = (
                f"<line x1='{x}' y1='0' x2='{x}' y2='{sp}' "
                f"stroke='black' stroke-width='{sw}' stroke-opacity='{op}'/>"
            )
            uris[tid] = _svg_data_uri(body, sp, sp)

        elif tid == "hatch-h":
            sw = t.get("stroke_width", 1)
            y = sp / 2
            body = (
                f"<line x1='0' y1='{y}' x2='{sp}' y2='{y}' "
                f"stroke='black' stroke-width='{sw}' stroke-opacity='{op}'/>"
            )
            uris[tid] = _svg_data_uri(body, sp, sp)

        elif tid == "hatch-x":
            sw = t.get("stroke_width", 1)
            mid_x = sp / 2
            mid_y = sp / 2
            body = (
                f"<line x1='{mid_x}' y1='0' x2='{mid_x}' y2='{sp}' "
                f"stroke='black' stroke-width='{sw}' stroke-opacity='{op}'/>"
                f"<line x1='0' y1='{mid_y}' x2='{sp}' y2='{mid_y}' "
                f"stroke='black' stroke-width='{sw}' stroke-opacity='{op}'/>"
            )
            uris[tid] = _svg_data_uri(body, sp, sp)

        elif tid == "hatch-fwd":
            sw = t.get("stroke_width", 1)
            # Three copies of the diagonal to tile seamlessly
            body = (
                f"<line x1='0' y1='{sp}' x2='{sp}' y2='0' "
                f"stroke='black' stroke-width='{sw}' stroke-opacity='{op}'/>"
                f"<line x1='-{sp}' y1='{sp}' x2='{sp}' y2='-{sp}' "
                f"stroke='black' stroke-width='{sw}' stroke-opacity='{op}'/>"
                f"<line x1='0' y1='{sp * 2}' x2='{sp * 2}' y2='0' "
                f"stroke='black' stroke-width='{sw}' stroke-opacity='{op}'/>"
            )
            uris[tid] = _svg_data_uri(body, sp, sp)

        elif tid == "hatch-bwd":
            sw = t.get("stroke_width", 1)
            body = (
                f"<line x1='0' y1='0' x2='{sp}' y2='{sp}' "
                f"stroke='black' stroke-width='{sw}' stroke-opacity='{op}'/>"
                f"<line x1='-{sp}' y1='0' x2='{sp}' y2='{sp * 2}' "
                f"stroke='black' stroke-width='{sw}' stroke-opacity='{op}'/>"
                f"<line x1='0' y1='-{sp}' x2='{sp * 2}' y2='{sp}' "
                f"stroke='black' stroke-width='{sw}' stroke-opacity='{op}'/>"
            )
            uris[tid] = _svg_data_uri(body, sp, sp)

    return uris


# ---------------------------------------------------------------------------
# CSS fragment (injected into monad.css via create_monad_system)
# ---------------------------------------------------------------------------

def create_texture_css_fragment(textures_data):
    """Return a CSS fragment with Strata texture tokens and Atomos utility classes."""
    if not textures_data:
        return ""

    uris = _build_svg_uris(textures_data)

    # Ordered list of IDs for deterministic output
    ordered = ["dot", "hatch-v", "hatch-h", "hatch-x", "hatch-fwd", "hatch-bwd"]
    ids = [tid for tid in ordered if tid in uris]

    # -- Strata tokens --
    token_lines = []
    for tid in ids:
        token_lines.append(f"  --strata-texture-{tid}: {uris[tid]};")
    tokens_block = "\n".join(token_lines)

    # -- Atomos utility classes --
    class_lines = []
    for tid in ids:
        class_lines.append(
            f".atomos-texture--{tid} {{ background-image: var(--strata-texture-{tid}); }}"
        )
    classes_block = "\n".join(class_lines)

    return f"""

/* =========================================================================
   STRATA — TEXTURE TOKENS
   ========================================================================= */
:root {{
{tokens_block}
}}

/* =========================================================================
   ATOMOS — TEXTURE UTILITIES
   ========================================================================= */
.atomos-texture {{
  background-repeat: repeat;
  background-size: auto;
}}
{classes_block}
"""


# ---------------------------------------------------------------------------
# Python / matplotlib
# ---------------------------------------------------------------------------

def create_texture_python(textures_data):
    """Return a Python code fragment appended to seaborn_palette.py."""
    if not textures_data:
        return ""

    # Map texture IDs to matplotlib hatch characters
    hatch_map = {
        "dot": ".",
        "hatch-v": "|",
        "hatch-h": "-",
        "hatch-x": "+",
        "hatch-fwd": "/",
        "hatch-bwd": "\\\\",
    }

    param_lines = []
    for key, t in textures_data.items():
        tid = t["id"]
        sp = t["spacing"]
        op = t["opacity"]
        density = max(1, int(16 / sp))
        param_lines.append(
            f'    "{tid}": {{"density": {density}, "opacity": {op}}},'
        )

    hatch_entries = []
    for key, t in textures_data.items():
        tid = t["id"]
        ch = hatch_map.get(tid, "")
        hatch_entries.append(f'    "{tid}": "{ch}",')

    return f"""

# ── Texture / Pattern Support ────────────────────────────────────────────────

TEXTURE_HATCHES = {{
{chr(10).join(hatch_entries)}
}}

TEXTURE_PARAMS = {{
{chr(10).join(param_lines)}
}}


def apply_texture(patches, texture_id, color=None):
    \"\"\"Apply a Monad texture hatch to matplotlib bar patches.

    Parameters
    ----------
    patches : list[matplotlib.patches.Patch]
        The ``.patches`` attribute of a bar container, or any iterable of Patch objects.
    texture_id : str
        One of the TEXTURE_HATCHES keys (e.g. ``"dot"``, ``"hatch-v"``).
    color : str or None
        Optional edge color for the hatch lines.  Falls back to patch edge color.
    \"\"\"
    hatch_char = TEXTURE_HATCHES.get(texture_id, "")
    params = TEXTURE_PARAMS.get(texture_id, {{}})
    density = params.get("density", 1)
    pattern = hatch_char * density
    for patch in patches:
        patch.set_hatch(pattern)
        if color is not None:
            patch.set_edgecolor(color)
"""


# ---------------------------------------------------------------------------
# C# / Unity
# ---------------------------------------------------------------------------

def create_texture_csharp(textures_data):
    """Return a complete TexturePatterns.cs file."""
    if not textures_data:
        return ""

    # Pull default values from JSON
    def _val(key, field, default):
        return textures_data.get(key, {}).get(field, default)

    dot_spacing = int(_val("dot", "spacing", 12))
    dot_radius = _val("dot", "radius", 1.5)
    hv_spacing = int(_val("hatch_v", "spacing", 8))
    hv_sw = int(_val("hatch_v", "stroke_width", 1))
    hh_spacing = int(_val("hatch_h", "spacing", 8))
    hh_sw = int(_val("hatch_h", "stroke_width", 1))
    hx_spacing = int(_val("hatch_x", "spacing", 8))
    hx_sw = int(_val("hatch_x", "stroke_width", 1))
    hf_spacing = int(_val("hatch_fwd", "spacing", 10))
    hf_sw = int(_val("hatch_fwd", "stroke_width", 1))
    hb_spacing = int(_val("hatch_bwd", "spacing", 10))
    hb_sw = int(_val("hatch_bwd", "stroke_width", 1))

    return f"""// TexturePatterns.cs — Monad Design System
// Generated from colors.json — do not edit directly.
//
// Procedural tileable texture generators for Unity.
// Usage:
//   Texture2D tex = TexturePatterns.CreateDot(ColorPalette.Information2);
//   material.mainTexture = tex;

using UnityEngine;

namespace Utility
{{
    public static class TexturePatterns
    {{
        /// <summary>Create a tileable dot-grid texture.</summary>
        public static Texture2D CreateDot(Color color, int cellSize = {dot_spacing}, float radius = {dot_radius}f, int size = 128)
        {{
            var tex = new Texture2D(size, size, TextureFormat.RGBA32, false);
            tex.filterMode = FilterMode.Point;
            tex.wrapMode = TextureWrapMode.Repeat;
            var clear = new Color(0, 0, 0, 0);
            var pixels = new Color[size * size];
            for (int i = 0; i < pixels.Length; i++) pixels[i] = clear;

            float r2 = radius * radius;
            for (int y = 0; y < size; y++)
                for (int x = 0; x < size; x++)
                {{
                    float cx = (x % cellSize) - cellSize * 0.5f;
                    float cy = (y % cellSize) - cellSize * 0.5f;
                    if (cx * cx + cy * cy <= r2)
                        pixels[y * size + x] = color;
                }}

            tex.SetPixels(pixels);
            tex.Apply();
            return tex;
        }}

        /// <summary>Create a tileable vertical-line hatch texture.</summary>
        public static Texture2D CreateHatchVertical(Color color, int cellSize = {hv_spacing}, int strokeWidth = {hv_sw}, int size = 128)
        {{
            return CreateLineHatch(color, cellSize, strokeWidth, size, vertical: true, horizontal: false);
        }}

        /// <summary>Create a tileable horizontal-line hatch texture.</summary>
        public static Texture2D CreateHatchHorizontal(Color color, int cellSize = {hh_spacing}, int strokeWidth = {hh_sw}, int size = 128)
        {{
            return CreateLineHatch(color, cellSize, strokeWidth, size, vertical: false, horizontal: true);
        }}

        /// <summary>Create a tileable cross-hatch texture.</summary>
        public static Texture2D CreateCrossHatch(Color color, int cellSize = {hx_spacing}, int strokeWidth = {hx_sw}, int size = 128)
        {{
            return CreateLineHatch(color, cellSize, strokeWidth, size, vertical: true, horizontal: true);
        }}

        /// <summary>Create a tileable forward-diagonal (/) hatch texture.</summary>
        public static Texture2D CreateHatchForward(Color color, int cellSize = {hf_spacing}, int strokeWidth = {hf_sw}, int size = 128)
        {{
            return CreateDiagonalHatch(color, cellSize, strokeWidth, size, forward: true);
        }}

        /// <summary>Create a tileable backward-diagonal (\\) hatch texture.</summary>
        public static Texture2D CreateHatchBackward(Color color, int cellSize = {hb_spacing}, int strokeWidth = {hb_sw}, int size = 128)
        {{
            return CreateDiagonalHatch(color, cellSize, strokeWidth, size, forward: false);
        }}

        // ── Shared builders ─────────────────────────────────────────────────

        private static Texture2D CreateLineHatch(Color color, int cellSize, int strokeWidth, int size, bool vertical, bool horizontal)
        {{
            var tex = new Texture2D(size, size, TextureFormat.RGBA32, false);
            tex.filterMode = FilterMode.Point;
            tex.wrapMode = TextureWrapMode.Repeat;
            var clear = new Color(0, 0, 0, 0);
            var pixels = new Color[size * size];
            for (int i = 0; i < pixels.Length; i++) pixels[i] = clear;

            int half = strokeWidth / 2;
            for (int y = 0; y < size; y++)
                for (int x = 0; x < size; x++)
                {{
                    bool hit = false;
                    if (vertical)
                    {{
                        int dx = (x % cellSize) - cellSize / 2;
                        if (Mathf.Abs(dx) <= half) hit = true;
                    }}
                    if (horizontal)
                    {{
                        int dy = (y % cellSize) - cellSize / 2;
                        if (Mathf.Abs(dy) <= half) hit = true;
                    }}
                    if (hit) pixels[y * size + x] = color;
                }}

            tex.SetPixels(pixels);
            tex.Apply();
            return tex;
        }}

        private static Texture2D CreateDiagonalHatch(Color color, int cellSize, int strokeWidth, int size, bool forward)
        {{
            var tex = new Texture2D(size, size, TextureFormat.RGBA32, false);
            tex.filterMode = FilterMode.Point;
            tex.wrapMode = TextureWrapMode.Repeat;
            var clear = new Color(0, 0, 0, 0);
            var pixels = new Color[size * size];
            for (int i = 0; i < pixels.Length; i++) pixels[i] = clear;

            float halfW = strokeWidth * 0.5f;
            for (int y = 0; y < size; y++)
                for (int x = 0; x < size; x++)
                {{
                    // Distance from the nearest diagonal in the tiling grid.
                    float d;
                    if (forward)
                        d = ((x + y) % cellSize);
                    else
                        d = ((x - y % cellSize + cellSize) % cellSize);
                    // Wrap to center of cell
                    if (d > cellSize * 0.5f) d = cellSize - d;
                    if (d <= halfW) pixels[y * size + x] = color;
                }}

            tex.SetPixels(pixels);
            tex.Apply();
            return tex;
        }}
    }}
}}
"""


# ---------------------------------------------------------------------------
# SwiftUI
# ---------------------------------------------------------------------------

def create_texture_swiftui(textures_data):
    """Return a complete MonadTextures.swift file."""
    if not textures_data:
        return ""

    def _val(key, field, default):
        return textures_data.get(key, {}).get(field, default)

    dot_r = _val("dot", "radius", 1.5)
    dot_sp = _val("dot", "spacing", 12)
    hv_sp = _val("hatch_v", "spacing", 8)
    hv_sw = _val("hatch_v", "stroke_width", 1)
    hh_sp = _val("hatch_h", "spacing", 8)
    hh_sw = _val("hatch_h", "stroke_width", 1)
    hx_sp = _val("hatch_x", "spacing", 8)
    hx_sw = _val("hatch_x", "stroke_width", 1)
    hf_sp = _val("hatch_fwd", "spacing", 10)
    hf_sw = _val("hatch_fwd", "stroke_width", 1)
    hb_sp = _val("hatch_bwd", "spacing", 10)
    hb_sw = _val("hatch_bwd", "stroke_width", 1)

    return f"""// MonadTextures.swift — Monad Design System
// Generated from colors.json — do not edit directly.
//
// Provides tileable texture patterns as SwiftUI views.
// Usage:
//   Rectangle().monadTexture(.dot)
//   Rectangle().monadTexture(.hatchFwd, color: MonadStrata.interactive)

import SwiftUI

// MARK: - Texture Enum

public enum MonadTexture: String, CaseIterable {{
    case dot      = "dot"
    case hatchV   = "hatch-v"
    case hatchH   = "hatch-h"
    case hatchX   = "hatch-x"
    case hatchFwd = "hatch-fwd"
    case hatchBwd = "hatch-bwd"

    /// Cell spacing in points (from colors.json).
    public var spacing: CGFloat {{
        switch self {{
        case .dot:      return {dot_sp}
        case .hatchV:   return {hv_sp}
        case .hatchH:   return {hh_sp}
        case .hatchX:   return {hx_sp}
        case .hatchFwd: return {hf_sp}
        case .hatchBwd: return {hb_sp}
        }}
    }}

    /// Stroke width or dot radius in points.
    public var strokeSize: CGFloat {{
        switch self {{
        case .dot:      return {dot_r}
        case .hatchV:   return {hv_sw}
        case .hatchH:   return {hh_sw}
        case .hatchX:   return {hx_sw}
        case .hatchFwd: return {hf_sw}
        case .hatchBwd: return {hb_sw}
        }}
    }}
}}

// MARK: - Pattern View

public struct TexturePatternView: View {{
    public let texture: MonadTexture
    public let color: Color
    public let opacity: Double

    public init(texture: MonadTexture, color: Color, opacity: Double = 0.6) {{
        self.texture = texture
        self.color = color
        self.opacity = opacity
    }}

    public var body: some View {{
        Canvas {{ context, size in
            let sp = texture.spacing
            let cols = Int(ceil(size.width / sp)) + 1
            let rows = Int(ceil(size.height / sp)) + 1

            context.opacity = opacity

            switch texture {{
            case .dot:
                let r = texture.strokeSize
                for row in 0..<rows {{
                    for col in 0..<cols {{
                        let cx = CGFloat(col) * sp + sp / 2
                        let cy = CGFloat(row) * sp + sp / 2
                        let rect = CGRect(x: cx - r, y: cy - r, width: r * 2, height: r * 2)
                        context.fill(Ellipse().path(in: rect), with: .color(color))
                    }}
                }}

            case .hatchV:
                let sw = texture.strokeSize
                for col in 0..<cols {{
                    let x = CGFloat(col) * sp + sp / 2
                    let rect = CGRect(x: x - sw / 2, y: 0, width: sw, height: size.height)
                    context.fill(Rectangle().path(in: rect), with: .color(color))
                }}

            case .hatchH:
                let sw = texture.strokeSize
                for row in 0..<rows {{
                    let y = CGFloat(row) * sp + sp / 2
                    let rect = CGRect(x: 0, y: y - sw / 2, width: size.width, height: sw)
                    context.fill(Rectangle().path(in: rect), with: .color(color))
                }}

            case .hatchX:
                let sw = texture.strokeSize
                for col in 0..<cols {{
                    let x = CGFloat(col) * sp + sp / 2
                    let rect = CGRect(x: x - sw / 2, y: 0, width: sw, height: size.height)
                    context.fill(Rectangle().path(in: rect), with: .color(color))
                }}
                for row in 0..<rows {{
                    let y = CGFloat(row) * sp + sp / 2
                    let rect = CGRect(x: 0, y: y - sw / 2, width: size.width, height: sw)
                    context.fill(Rectangle().path(in: rect), with: .color(color))
                }}

            case .hatchFwd:
                let sw = texture.strokeSize
                for offset in -(rows)...(cols + rows) {{
                    var path = Path()
                    let startX = CGFloat(offset) * sp
                    path.move(to: CGPoint(x: startX, y: 0))
                    path.addLine(to: CGPoint(x: startX - size.height, y: size.height))
                    context.stroke(path, with: .color(color), lineWidth: sw)
                }}

            case .hatchBwd:
                let sw = texture.strokeSize
                for offset in -(rows)...(cols + rows) {{
                    var path = Path()
                    let startX = CGFloat(offset) * sp
                    path.move(to: CGPoint(x: startX, y: 0))
                    path.addLine(to: CGPoint(x: startX + size.height, y: size.height))
                    context.stroke(path, with: .color(color), lineWidth: sw)
                }}
            }}
        }}
    }}
}}

// MARK: - View Modifier

extension View {{
    /// Overlay a repeating Monad texture pattern.
    public func monadTexture(_ texture: MonadTexture, color: Color = .primary, opacity: Double = 0.6) -> some View {{
        self.overlay(TexturePatternView(texture: texture, color: color, opacity: opacity))
    }}
}}
"""
