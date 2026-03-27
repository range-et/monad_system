"""
Design System Color Palette
Generated from colors.json — do not edit directly.

Usage:
    from seaborn_palette import (
        PALETTE_DARK, PALETTE_LIGHT,
        CATEGORICAL, STATUS_COLORS, MOVEMENT_COLORS,
        make_sequential_cmap,
    )
    import seaborn as sns
    sns.set_palette(CATEGORICAL)
"""

from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Token dictionaries
# ---------------------------------------------------------------------------

PALETTE_DARK = {
    "bg":             "#0F1113",
    "layer_01":       "#1e1e1e",
    "layer_02":       "#262626",
    "layer_03":       "#333333",
    "text_primary":   "#EEF2F6",
    "text_secondary": "#B6BFCC",
    "text_disabled":  "#7D8794",
    "interactive":    "#1E88C8",
    "info":           "#2B9ED1",
    "success":        "#6EAD45",
    "warning":        "#D7A12A",
    "error":          "#D64C45",
    "highlight":      "#FFEB3B",
    "disabled":       "#757575",
}

PALETTE_LIGHT = {
    "bg":             "#F2F4F7",
    "layer_01":       "#ffffff",
    "layer_02":       "#EDF1F5",
    "layer_03":       "#E3E8EE",
    "text_primary":   "#141A22",
    "text_secondary": "#4F5A69",
    "text_disabled":  "#7E8998",
    "interactive":    "#1E88C8",
    "info":           "#2B9ED1",
    "success":        "#6EAD45",
    "warning":        "#D7A12A",
    "error":          "#D64C45",
    "highlight":      "#FFEB3B",
    "disabled":       "#757575",
}

STATUS_COLORS = {
    "info":     "#2B9ED1",
    "info_alt": "#1E88C8",
    "success":  "#6EAD45",
    "warning":  "#D7A12A",
    "error":    "#D64C45",
}

MOVEMENT_COLORS = {
    "start":  "#4CAF50",
    "hand":   "#03A9F4",
    "foot":   "#FFEB3B",
    "finish": "#9C27B0",
}

# Ordered categorical palette — use with sns.set_palette() or as bar/line colors.
# Order: interactive → info → success → warning → error → highlight → finish
CATEGORICAL = [
    "#1E88C8",
    "#2B9ED1",
    "#6EAD45",
    "#D7A12A",
    "#D64C45",
    "#FFEB3B",
    "#9C27B0",
    "#4CAF50",
]


# ---------------------------------------------------------------------------
# Colormaps
# ---------------------------------------------------------------------------

def make_sequential_cmap(dark: bool = True, name: str = "ds_sequential") -> LinearSegmentedColormap:
    """
    Create a perceptually sequential colormap from the design system palette.

    dark=True:  dark background → cyan/blue accent (suitable for dark figures)
    dark=False: light background → teal/cyan accent (suitable for light figures)

    Example:
        cmap = make_sequential_cmap(dark=True)
        plt.imshow(data, cmap=cmap)
    """
    if dark:
        colors = ["#0F1113", "#262626", "#2B9ED1", "#1E88C8"]
    else:
        colors = ["#F2F4F7", "#E3E8EE", "#2B9ED1", "#1E88C8"]
    return LinearSegmentedColormap.from_list(name, colors)


def make_diverging_cmap(name: str = "ds_diverging") -> LinearSegmentedColormap:
    """
    Create a diverging colormap: error (red) → neutral → success (green).

    Useful for correlation matrices, diff views, and gain/loss charts.
    """
    colors = ["#D64C45", "#757575", "#6EAD45"]
    return LinearSegmentedColormap.from_list(name, colors)


def make_status_cmap(name: str = "ds_status") -> ListedColormap:
    """
    Discrete 4-step colormap: info → success → warning → error.
    Useful for categorical heatmaps with severity levels.
    """
    colors = [
        STATUS_COLORS["info"],
        STATUS_COLORS["success"],
        STATUS_COLORS["warning"],
        STATUS_COLORS["error"],
    ]
    return ListedColormap(colors, name=name)


# ---------------------------------------------------------------------------
# Figure helpers
# ---------------------------------------------------------------------------

def apply_dark_theme(fig=None, ax=None):
    """
    Apply dark-theme styling to a matplotlib figure/axes pair.
    Call after creating your figure.

    Example:
        fig, ax = plt.subplots()
        apply_dark_theme(fig, ax)
        ax.plot(x, y)
    """
    bg = PALETTE_DARK["bg"]
    layer = PALETTE_DARK["layer_01"]
    text = PALETTE_DARK["text_primary"]
    subtext = PALETTE_DARK["text_secondary"]

    plt.rcParams.update({
        "figure.facecolor": bg,
        "axes.facecolor":   layer,
        "axes.edgecolor":   PALETTE_DARK.get("border", "#3d3d3d"),
        "axes.labelcolor":  text,
        "xtick.color":      subtext,
        "ytick.color":      subtext,
        "text.color":       text,
        "grid.color":       "#2a2a2a",
        "grid.linestyle":   "--",
        "grid.linewidth":   0.5,
        "font.family":      "Inter",
    })

    if fig is not None:
        fig.patch.set_facecolor(bg)
    if ax is not None:
        ax.set_facecolor(layer)


def apply_light_theme(fig=None, ax=None):
    """
    Apply light-theme styling to a matplotlib figure/axes pair.
    """
    bg = PALETTE_LIGHT["bg"]
    layer = PALETTE_LIGHT["layer_01"]
    text = PALETTE_LIGHT["text_primary"]
    subtext = PALETTE_LIGHT["text_secondary"]

    plt.rcParams.update({
        "figure.facecolor": bg,
        "axes.facecolor":   layer,
        "axes.edgecolor":   "#BCC6D2",
        "axes.labelcolor":  text,
        "xtick.color":      subtext,
        "ytick.color":      subtext,
        "text.color":       text,
        "grid.color":       "#D8DFE7",
        "grid.linestyle":   "--",
        "grid.linewidth":   0.5,
        "font.family":      "Inter",
    })

    if fig is not None:
        fig.patch.set_facecolor(bg)
    if ax is not None:
        ax.set_facecolor(layer)


# ── Texture / Pattern Support ────────────────────────────────────────────────

TEXTURE_HATCHES = {
    "dot": ".",
    "hatch-v": "|",
    "hatch-h": "-",
    "hatch-x": "+",
    "hatch-fwd": "/",
    "hatch-bwd": "\\",
}

TEXTURE_PARAMS = {
    "dot": {"density": 1, "opacity": 0.6},
    "hatch-v": {"density": 2, "opacity": 0.6},
    "hatch-h": {"density": 2, "opacity": 0.6},
    "hatch-x": {"density": 2, "opacity": 0.6},
    "hatch-fwd": {"density": 1, "opacity": 0.6},
    "hatch-bwd": {"density": 1, "opacity": 0.6},
}


def apply_texture(patches, texture_id, color=None):
    """Apply a Monad texture hatch to matplotlib bar patches.

    Parameters
    ----------
    patches : list[matplotlib.patches.Patch]
        The ``.patches`` attribute of a bar container, or any iterable of Patch objects.
    texture_id : str
        One of the TEXTURE_HATCHES keys (e.g. ``"dot"``, ``"hatch-v"``).
    color : str or None
        Optional edge color for the hatch lines.  Falls back to patch edge color.
    """
    hatch_char = TEXTURE_HATCHES.get(texture_id, "")
    params = TEXTURE_PARAMS.get(texture_id, {})
    density = params.get("density", 1)
    pattern = hatch_char * density
    for patch in patches:
        patch.set_hatch(pattern)
        if color is not None:
            patch.set_edgecolor(color)
