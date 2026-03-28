"""
Generate animated GIF visualizations of the Monad Design System motion tokens.

Reads colors.json for Motion definitions, produces:
  build/motion_easing_curves.gif  — 4 easing curves with animated dot
  build/motion_durations.gif      — 4 duration bars filling at real speed

Usage:  python src/gen_motion_gifs.py
"""

import json
import os
import re
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BUILD = REPO / "build"

# ── Design system colors ────────────────────────────────────────────────────
BG       = "#0F1113"
GRID     = "#2A313A"
TEXT     = "#B6BFCC"
DOT      = "#EEF2F6"
CURVE_COLORS = {
    "linear":      "#7D8794",
    "ease_out":    "#2B9ED1",
    "ease_in":     "#D64C45",
    "ease_in_out": "#1E88C8",
}
BAR_COLOR = "#1E88C8"

LABELS = {
    "linear":      "linear",
    "ease_out":    "ease-out",
    "ease_in":     "ease-in",
    "ease_in_out": "ease-in-out",
}


# ── Cubic bezier math ───────────────────────────────────────────────────────

def parse_bezier(css_val):
    m = re.match(r"cubic-bezier\(\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^)]+)\)", css_val.strip())
    if not m:
        return None
    return tuple(float(v) for v in m.groups())


def bezier_y(pts, x):
    """Evaluate y at progress x for a cubic-bezier curve."""
    if pts is None:
        return x
    x1, y1, x2, y2 = pts
    # Newton's method: find t such that B_x(t) = x
    t = x
    for _ in range(12):
        bx = 3*x1*t*(1-t)**2 + 3*x2*t**2*(1-t) + t**3
        dx = 3*x1*(1-t)**2 - 6*x1*t*(1-t) + 6*x2*t*(1-t) - 3*x2*t**2 + 3*t**2
        if abs(dx) < 1e-10:
            break
        t -= (bx - x) / dx
        t = max(0.0, min(1.0, t))
    return 3*y1*t*(1-t)**2 + 3*y2*t**2*(1-t) + t**3


def curve_points(pts, n=200):
    xs = np.linspace(0, 1, n)
    ys = np.array([bezier_y(pts, x) for x in xs])
    return xs, ys


# ── GIF 1: Easing curves ───────────────────────────────────────────────────

def gen_easing_gif(motion, out_path):
    easings = motion["easings"]
    keys = list(easings.keys())
    pts_map = {k: parse_bezier(v["css"]) for k, v in easings.items()}

    fig, axes = plt.subplots(1, 4, figsize=(8, 2.8), facecolor=BG)
    fig.subplots_adjust(left=0.04, right=0.96, top=0.88, bottom=0.18, wspace=0.35)

    lines = {}
    dots = {}

    for i, key in enumerate(keys):
        ax = axes[i]
        ax.set_facecolor(BG)
        xs, ys = curve_points(pts_map[key])
        color = CURVE_COLORS.get(key, TEXT)

        # grid
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.1, 1.1)
        for g in [0, 0.25, 0.5, 0.75, 1.0]:
            ax.axhline(g, color=GRID, linewidth=0.5, zorder=0)
            ax.axvline(g, color=GRID, linewidth=0.5, zorder=0)

        # diagonal reference
        ax.plot([0, 1], [0, 1], color=GRID, linewidth=0.8, linestyle="--", zorder=1)

        # curve
        ax.plot(xs, ys, color=color, linewidth=2, zorder=2)

        # dot (animated)
        dot, = ax.plot([], [], "s", color=DOT, markersize=5, zorder=3)
        dots[key] = dot

        # label
        ax.set_title(LABELS[key], fontsize=9, fontfamily="monospace", color=TEXT, pad=6)

        # clean axes
        ax.tick_params(colors=GRID, labelsize=6)
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        for spine in ax.spines.values():
            spine.set_color(GRID)
            spine.set_linewidth(0.5)
        ax.tick_params(axis="both", which="both", length=0)
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontfamily("monospace")
            label.set_color(GRID)

    total_frames = 90  # 3s at 30fps
    anim_frames = 60   # 2s animation
    pause_frames = total_frames - anim_frames

    def update(frame):
        if frame < anim_frames:
            progress = frame / (anim_frames - 1)
        else:
            progress = -1  # hide dot during pause

        for key in keys:
            if progress < 0:
                dots[key].set_data([], [])
            else:
                y = bezier_y(pts_map[key], progress)
                dots[key].set_data([progress], [y])
        return list(dots.values())

    anim = FuncAnimation(fig, update, frames=total_frames, interval=33, blit=True)
    anim.save(str(out_path), writer="pillow", dpi=100)
    plt.close(fig)
    print(f"Saved -> {out_path}")


# ── GIF 2: Duration bars ───────────────────────────────────────────────────

def gen_duration_gif(motion, out_path):
    durations = motion["durations"]
    keys = list(durations.keys())
    ms_vals = [v["ms"] for v in durations.values()]
    max_ms = max(ms_vals)

    fig, ax = plt.subplots(figsize=(6, 2.4), facecolor=BG)
    fig.subplots_adjust(left=0.18, right=0.88, top=0.92, bottom=0.08)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 1.05)
    ax.set_ylim(-0.5, len(keys) - 0.5)
    ax.invert_yaxis()

    # track backgrounds
    for i in range(len(keys)):
        ax.barh(i, 1.0, height=0.55, color="#171A1E", edgecolor=GRID, linewidth=0.5)

    # fill bars (animated)
    bars = []
    for i in range(len(keys)):
        bar = ax.barh(i, 0, height=0.55, color=BAR_COLOR)
        bars.append(bar[0])

    # labels
    ax.set_yticks(range(len(keys)))
    ax.set_yticklabels([f"{k}  {ms_vals[i]}ms" for i, k in enumerate(keys)],
                       fontfamily="monospace", fontsize=9, color=TEXT)
    ax.set_xticks([])

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="y", length=0)

    # title
    ax.set_title("duration comparison", fontsize=9, fontfamily="monospace",
                 color=TEXT, pad=8, loc="left")

    # Scale: slowest bar takes 2s (60 frames at 30fps)
    total_frames = 90
    scale_frames = 60

    def update(frame):
        if frame >= total_frames - 10:
            # reset pause
            for bar in bars:
                bar.set_width(0)
            return bars

        for i, key in enumerate(keys):
            ms = ms_vals[i]
            bar_frames = (ms / max_ms) * scale_frames
            if frame < bar_frames:
                progress = frame / bar_frames
            else:
                progress = 1.0
            bars[i].set_width(progress)
        return bars

    anim = FuncAnimation(fig, update, frames=total_frames, interval=33, blit=True)
    anim.save(str(out_path), writer="pillow", dpi=100)
    plt.close(fig)
    print(f"Saved -> {out_path}")


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    with open(REPO / "colors.json", "r") as f:
        data = json.load(f)

    motion = data.get("Motion")
    if not motion:
        print("No Motion section in colors.json, skipping GIF generation.")
        exit(0)

    os.makedirs(BUILD, exist_ok=True)
    gen_easing_gif(motion, BUILD / "motion_easing_curves.gif")
    gen_duration_gif(motion, BUILD / "motion_durations.gif")
    print("Done.")
