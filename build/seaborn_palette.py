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
    "bg":             "#121212",
    "layer_01":       "#1e1e1e",
    "layer_02":       "#262626",
    "layer_03":       "#333333",
    "text_primary":   "#E0E0E0",
    "text_secondary": "#B0B0B0",
    "text_disabled":  "#757575",
    "interactive":    "#03A9F4",
    "info":           "#00BCD4",
    "success":        "#8BC34A",
    "warning":        "#FFC107",
    "error":          "#F44336",
    "highlight":      "#FFEB3B",
    "disabled":       "#757575",
}

PALETTE_LIGHT = {
    "bg":             "#f4f4f4",
    "layer_01":       "#ffffff",
    "layer_02":       "#f4f4f4",
    "layer_03":       "#e8e8e8",
    "text_primary":   "#161616",
    "text_secondary": "#525252",
    "text_disabled":  "#8d8d8d",
    "interactive":    "#03A9F4",
    "info":           "#00BCD4",
    "success":        "#8BC34A",
    "warning":        "#FFC107",
    "error":          "#F44336",
    "highlight":      "#FFEB3B",
    "disabled":       "#757575",
}

STATUS_COLORS = {
    "info":     "#00BCD4",
    "info_alt": "#03A9F4",
    "success":  "#8BC34A",
    "warning":  "#FFC107",
    "error":    "#F44336",
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
    "#03A9F4",
    "#00BCD4",
    "#8BC34A",
    "#FFC107",
    "#F44336",
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
        colors = ["#121212", "#262626", "#00BCD4", "#03A9F4"]
    else:
        colors = ["#f4f4f4", "#e8e8e8", "#00BCD4", "#03A9F4"]
    return LinearSegmentedColormap.from_list(name, colors)


def make_diverging_cmap(name: str = "ds_diverging") -> LinearSegmentedColormap:
    """
    Create a diverging colormap: error (red) → neutral → success (green).

    Useful for correlation matrices, diff views, and gain/loss charts.
    """
    colors = ["#F44336", "#757575", "#8BC34A"]
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
        "axes.edgecolor":   "#c6c6c6",
        "axes.labelcolor":  text,
        "xtick.color":      subtext,
        "ytick.color":      subtext,
        "text.color":       text,
        "grid.color":       "#e8e8e8",
        "grid.linestyle":   "--",
        "grid.linewidth":   0.5,
        "font.family":      "Inter",
    })

    if fig is not None:
        fig.patch.set_facecolor(bg)
    if ax is not None:
        ax.set_facecolor(layer)
