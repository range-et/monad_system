"""Motion / animation token generators for the Monad Design System.

Each public function receives the raw ``motion`` dict extracted from
``colors.json["Motion"]`` and returns a formatted string artifact.
"""

import re

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _parse_bezier(css_value):
    """Extract (x1, y1, x2, y2) floats from a CSS cubic-bezier() string.

    Returns None for ``"linear"`` or unrecognised values.
    """
    m = re.match(
        r"cubic-bezier\(\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^)]+)\)",
        css_value.strip(),
    )
    if not m:
        return None
    return tuple(float(v) for v in m.groups())


def _dur_key_to_camel(key):
    """``'ease_out'`` -> ``'easeOut'``."""
    parts = key.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def _dur_key_to_pascal(key):
    """``'ease_out'`` -> ``'EaseOut'``."""
    return "".join(p.capitalize() for p in key.split("_"))


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

_LEGACY_CSS = """\
  /* Threshold timing — linear, predictable */
  --threshold-fast:   80ms linear;
  --threshold-base:   160ms linear;
  --threshold-slow:   280ms linear;"""


def create_motion_css_tokens(motion):
    """Return CSS custom-property block for motion tokens.

    When *motion* is ``None`` the three legacy hardcoded lines are returned
    so that existing output is identical (backward compat).
    """
    if motion is None:
        return _LEGACY_CSS

    durations = motion.get("durations", {})
    easings = motion.get("easings", {})

    lines = []
    lines.append("")
    lines.append("  /* Threshold — durations */")
    for key, val in durations.items():
        ms = val["ms"]
        pad = max(1, 10 - len(key))
        lines.append(f"  --threshold-duration-{key}:{' ' * pad}{ms}ms;")

    lines.append("")
    lines.append("  /* Threshold — easing */")
    for key, val in easings.items():
        css_name = key.replace("_", "-")
        # Avoid double "ease": key "ease_out" → "ease-out", not "ease-ease-out"
        if css_name == "linear":
            var_suffix = "ease-linear"
        else:
            var_suffix = css_name
        css_val = val["css"]
        pad = max(1, 12 - len(var_suffix))
        lines.append(f"  --threshold-{var_suffix}:{' ' * pad}{css_val};")

    lines.append("")
    lines.append("  /* Threshold — composed shorthands (backward compat) */")
    for key in durations:
        if key == "slower":
            continue
        pad = max(1, 10 - len(key))
        lines.append(
            f"  --threshold-{key}:{' ' * pad}"
            f"var(--threshold-duration-{key})  var(--threshold-ease-linear);"
        )

    return "\n".join(lines)


def create_motion_css_reduced():
    """Return the ``@media (prefers-reduced-motion)`` block."""
    return """\

@media (prefers-reduced-motion: reduce) {
  :root, [data-strata="light"] {
    --threshold-duration-fast:   0.01ms;
    --threshold-duration-base:   0.01ms;
    --threshold-duration-slow:   0.01ms;
    --threshold-duration-slower: 0.01ms;
  }
}"""


# ---------------------------------------------------------------------------
# Python (appended to seaborn_palette.py)
# ---------------------------------------------------------------------------

def create_motion_python(motion):
    """Return a Python code fragment with duration and easing dicts."""
    if not motion:
        return ""

    durations = motion.get("durations", {})
    easings = motion.get("easings", {})

    lines = [
        "",
        "",
        "# ── Motion tokens ────────────────────────────────────────────────────",
        "",
        "MOTION_DURATIONS = {",
    ]
    for key, val in durations.items():
        sec = val["ms"] / 1000
        pad = max(1, 10 - len(key))
        lines.append(f'    "{key}":{" " * pad}{sec:.3f},')
    lines.append("}")

    lines.append("")
    lines.append("MOTION_EASINGS = {")
    for key, val in easings.items():
        css_val = val["css"]
        pts = _parse_bezier(css_val)
        if pts is None:
            lines.append(f'    "{key}":      None,  # linear')
        else:
            lines.append(f'    "{key}": ({pts[0]}, {pts[1]}, {pts[2]}, {pts[3]}),')
    lines.append("}")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# C# / Unity
# ---------------------------------------------------------------------------

def create_motion_csharp(motion):
    """Return a complete MotionTokens.cs file."""
    if not motion:
        return ""

    durations = motion.get("durations", {})
    easings = motion.get("easings", {})

    lines = [
        "// MotionTokens.cs",
        "// Generated from colors.json — do not edit directly.",
        "",
        "using UnityEngine;",
        "",
        "namespace Monad",
        "{",
        "    public static class MotionTokens",
        "    {",
        "        // Durations (seconds)",
    ]
    for key, val in durations.items():
        sec = val["ms"] / 1000
        name = _dur_key_to_pascal(key)
        pad = max(1, 12 - len(name))
        lines.append(f"        public const float Duration{name}{' ' * pad}= {sec:.3f}f;")

    lines.append("")
    lines.append("        // Easing curves (cubic-bezier control points)")

    for key, val in easings.items():
        css_val = val["css"]
        pts = _parse_bezier(css_val)
        if pts is None:
            continue  # skip linear — Unity's AnimationCurve.Linear is built-in
        name = _dur_key_to_pascal(key)
        lines.append(f"        public static AnimationCurve {name} => AnimationCurve.EaseInOut(0f, 0f, 1f, 1f);")
        lines.append(f"        // CSS: {css_val}")

    lines.append("    }")
    lines.append("}")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# SwiftUI
# ---------------------------------------------------------------------------

def create_motion_swiftui(motion):
    """Return a complete MonadMotion.swift file."""
    if not motion:
        return ""

    durations = motion.get("durations", {})
    easings = motion.get("easings", {})

    lines = [
        "// MonadMotion.swift",
        "// Generated from colors.json — do not edit directly.",
        "// Motion tokens mirror build/monad.css (--threshold-*).",
        "",
        "import SwiftUI",
        "",
        "public enum MonadMotion {",
        "",
        "    // MARK: - Durations (seconds)",
        "",
    ]
    for key, val in durations.items():
        sec = val["ms"] / 1000
        name = "duration" + _dur_key_to_pascal(key)
        pad = max(1, 18 - len(name))
        lines.append(f"    public static let {name}:{' ' * pad}Double = {sec:.3f}")

    lines.append("")
    lines.append("    // MARK: - Easing curves")
    lines.append("")

    for key, val in easings.items():
        css_val = val["css"]
        pts = _parse_bezier(css_val)
        if pts is None:
            continue  # linear is SwiftUI's .linear — no need to define
        name = _dur_key_to_camel(key)
        lines.append(
            f"    public static let {name} = Animation.timingCurve("
            f"{pts[0]}, {pts[1]}, {pts[2]}, {pts[3]})"
        )

    lines.append("}")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# JS (injected into monad.js IIFE)
# ---------------------------------------------------------------------------

def create_motion_js(motion):
    """Return a JS block that exposes motion tokens on ``window.MN.motion``."""
    if not motion:
        return ""

    durations = motion.get("durations", {})
    easings = motion.get("easings", {})

    lines = [
        "",
        "  // -----------------------------------------------------------------------",
        "  // Motion tokens",
        "  // -----------------------------------------------------------------------",
        "  var MN = window.MN || {};",
        "  MN.motion = {",
        "    duration: {",
    ]
    dur_entries = list(durations.items())
    for i, (key, val) in enumerate(dur_entries):
        comma = "," if i < len(dur_entries) - 1 else ""
        lines.append(f"      {_dur_key_to_camel(key)}: {val['ms']}{comma}")
    lines.append("    },")
    lines.append("    easing: {")
    eas_entries = list(easings.items())
    for i, (key, val) in enumerate(eas_entries):
        comma = "," if i < len(eas_entries) - 1 else ""
        name = _dur_key_to_camel(key)
        lines.append(f"      {name}: '{val['css']}'{comma}")
    lines.append("    }")
    lines.append("  };")
    lines.append("  window.MN = MN;")

    return "\n".join(lines)
