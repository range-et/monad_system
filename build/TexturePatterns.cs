// TexturePatterns.cs — Monad Design System
// Generated from colors.json — do not edit directly.
//
// Procedural tileable texture generators for Unity.
// Usage:
//   Texture2D tex = TexturePatterns.CreateDot(ColorPalette.Information2);
//   material.mainTexture = tex;

using UnityEngine;

namespace Monad
{
    public static class TexturePatterns
    {
        /// <summary>Create a tileable dot-grid texture.</summary>
        public static Texture2D CreateDot(Color color, int cellSize = 12, float radius = 1.5f, int size = 128)
        {
            var tex = new Texture2D(size, size, TextureFormat.RGBA32, false);
            tex.filterMode = FilterMode.Point;
            tex.wrapMode = TextureWrapMode.Repeat;
            var clear = new Color(0, 0, 0, 0);
            var pixels = new Color[size * size];
            for (int i = 0; i < pixels.Length; i++) pixels[i] = clear;

            float r2 = radius * radius;
            for (int y = 0; y < size; y++)
                for (int x = 0; x < size; x++)
                {
                    float cx = (x % cellSize) - cellSize * 0.5f;
                    float cy = (y % cellSize) - cellSize * 0.5f;
                    if (cx * cx + cy * cy <= r2)
                        pixels[y * size + x] = color;
                }

            tex.SetPixels(pixels);
            tex.Apply();
            return tex;
        }

        /// <summary>Create a tileable vertical-line hatch texture.</summary>
        public static Texture2D CreateHatchVertical(Color color, int cellSize = 8, int strokeWidth = 1, int size = 128)
        {
            return CreateLineHatch(color, cellSize, strokeWidth, size, vertical: true, horizontal: false);
        }

        /// <summary>Create a tileable horizontal-line hatch texture.</summary>
        public static Texture2D CreateHatchHorizontal(Color color, int cellSize = 8, int strokeWidth = 1, int size = 128)
        {
            return CreateLineHatch(color, cellSize, strokeWidth, size, vertical: false, horizontal: true);
        }

        /// <summary>Create a tileable cross-hatch texture.</summary>
        public static Texture2D CreateCrossHatch(Color color, int cellSize = 8, int strokeWidth = 1, int size = 128)
        {
            return CreateLineHatch(color, cellSize, strokeWidth, size, vertical: true, horizontal: true);
        }

        /// <summary>Create a tileable forward-diagonal (/) hatch texture.</summary>
        public static Texture2D CreateHatchForward(Color color, int cellSize = 10, int strokeWidth = 1, int size = 128)
        {
            return CreateDiagonalHatch(color, cellSize, strokeWidth, size, forward: true);
        }

        /// <summary>Create a tileable backward-diagonal (\) hatch texture.</summary>
        public static Texture2D CreateHatchBackward(Color color, int cellSize = 10, int strokeWidth = 1, int size = 128)
        {
            return CreateDiagonalHatch(color, cellSize, strokeWidth, size, forward: false);
        }

        // ── Shared builders ─────────────────────────────────────────────────

        private static Texture2D CreateLineHatch(Color color, int cellSize, int strokeWidth, int size, bool vertical, bool horizontal)
        {
            var tex = new Texture2D(size, size, TextureFormat.RGBA32, false);
            tex.filterMode = FilterMode.Point;
            tex.wrapMode = TextureWrapMode.Repeat;
            var clear = new Color(0, 0, 0, 0);
            var pixels = new Color[size * size];
            for (int i = 0; i < pixels.Length; i++) pixels[i] = clear;

            int half = strokeWidth / 2;
            for (int y = 0; y < size; y++)
                for (int x = 0; x < size; x++)
                {
                    bool hit = false;
                    if (vertical)
                    {
                        int dx = (x % cellSize) - cellSize / 2;
                        if (Mathf.Abs(dx) <= half) hit = true;
                    }
                    if (horizontal)
                    {
                        int dy = (y % cellSize) - cellSize / 2;
                        if (Mathf.Abs(dy) <= half) hit = true;
                    }
                    if (hit) pixels[y * size + x] = color;
                }

            tex.SetPixels(pixels);
            tex.Apply();
            return tex;
        }

        private static Texture2D CreateDiagonalHatch(Color color, int cellSize, int strokeWidth, int size, bool forward)
        {
            var tex = new Texture2D(size, size, TextureFormat.RGBA32, false);
            tex.filterMode = FilterMode.Point;
            tex.wrapMode = TextureWrapMode.Repeat;
            var clear = new Color(0, 0, 0, 0);
            var pixels = new Color[size * size];
            for (int i = 0; i < pixels.Length; i++) pixels[i] = clear;

            float halfW = strokeWidth * 0.5f;
            for (int y = 0; y < size; y++)
                for (int x = 0; x < size; x++)
                {
                    // Distance from the nearest diagonal in the tiling grid.
                    float d;
                    if (forward)
                        d = ((x + y) % cellSize);
                    else
                        d = ((x - y % cellSize + cellSize) % cellSize);
                    // Wrap to center of cell
                    if (d > cellSize * 0.5f) d = cellSize - d;
                    if (d <= halfW) pixels[y * size + x] = color;
                }

            tex.SetPixels(pixels);
            tex.Apply();
            return tex;
        }
    }
}
