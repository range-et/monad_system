def create_python_template(
    # Dark theme
    bg_dark="#121212",
    layer01_dark="#1e1e1e",
    layer02_dark="#262626",
    layer03_dark="#333333",
    text_primary_dark="#E0E0E0",
    text_secondary_dark="#B0B0B0",
    text_disabled_dark="#757575",
    # Light theme
    bg_light="#f4f4f4",
    layer01_light="#ffffff",
    layer02_light="#f4f4f4",
    layer03_light="#e8e8e8",
    text_primary_light="#161616",
    text_secondary_light="#525252",
    text_disabled_light="#8d8d8d",
    # Shared semantic colors
    interactive="#03A9F4",
    support_info="#00BCD4",
    support_info_alt="#03A9F4",
    support_success="#8BC34A",
    support_warning="#FFC107",
    support_error="#F44336",
    highlight="#FFEB3B",
    disabled="#757575",
    # Movement colors
    move_start="#4CAF50",
    move_hand="#03A9F4",
    move_foot="#FFEB3B",
    move_finish="#9C27B0",
):
    return f'''"""
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

PALETTE_DARK = {{
    "bg":             "{bg_dark}",
    "layer_01":       "{layer01_dark}",
    "layer_02":       "{layer02_dark}",
    "layer_03":       "{layer03_dark}",
    "text_primary":   "{text_primary_dark}",
    "text_secondary": "{text_secondary_dark}",
    "text_disabled":  "{text_disabled_dark}",
    "interactive":    "{interactive}",
    "info":           "{support_info}",
    "success":        "{support_success}",
    "warning":        "{support_warning}",
    "error":          "{support_error}",
    "highlight":      "{highlight}",
    "disabled":       "{disabled}",
}}

PALETTE_LIGHT = {{
    "bg":             "{bg_light}",
    "layer_01":       "{layer01_light}",
    "layer_02":       "{layer02_light}",
    "layer_03":       "{layer03_light}",
    "text_primary":   "{text_primary_light}",
    "text_secondary": "{text_secondary_light}",
    "text_disabled":  "{text_disabled_light}",
    "interactive":    "{interactive}",
    "info":           "{support_info}",
    "success":        "{support_success}",
    "warning":        "{support_warning}",
    "error":          "{support_error}",
    "highlight":      "{highlight}",
    "disabled":       "{disabled}",
}}

STATUS_COLORS = {{
    "info":     "{support_info}",
    "info_alt": "{support_info_alt}",
    "success":  "{support_success}",
    "warning":  "{support_warning}",
    "error":    "{support_error}",
}}

MOVEMENT_COLORS = {{
    "start":  "{move_start}",
    "hand":   "{move_hand}",
    "foot":   "{move_foot}",
    "finish": "{move_finish}",
}}

# Ordered categorical palette — use with sns.set_palette() or as bar/line colors.
# Order: interactive → info → success → warning → error → highlight → finish
CATEGORICAL = [
    "{interactive}",
    "{support_info}",
    "{support_success}",
    "{support_warning}",
    "{support_error}",
    "{highlight}",
    "{move_finish}",
    "{move_start}",
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
        colors = ["{bg_dark}", "{layer02_dark}", "{support_info}", "{interactive}"]
    else:
        colors = ["{bg_light}", "{layer03_light}", "{support_info}", "{interactive}"]
    return LinearSegmentedColormap.from_list(name, colors)


def make_diverging_cmap(name: str = "ds_diverging") -> LinearSegmentedColormap:
    """
    Create a diverging colormap: error (red) → neutral → success (green).

    Useful for correlation matrices, diff views, and gain/loss charts.
    """
    colors = ["{support_error}", "{disabled}", "{support_success}"]
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

    plt.rcParams.update({{
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
    }})

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

    plt.rcParams.update({{
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
    }})

    if fig is not None:
        fig.patch.set_facecolor(bg)
    if ax is not None:
        ax.set_facecolor(layer)
'''
