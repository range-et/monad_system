"""
Ghostty terminal theme generator for the Monad System.

Accepts palette tokens and returns config file strings for:
  - "Monad Dark"   (dark theme)
  - "Monad Light"  (light theme)

Ghostty theme files share the same syntax as ~/.config/ghostty/config.
Install: copy output files to ~/.config/ghostty/themes/

Activate in your Ghostty config:
    theme = Monad Dark
    # or auto-switch with OS mode:
    theme = light:Monad Light,dark:Monad Dark
"""

from datetime import datetime


def create_ghostty_dark_theme(
    background="#121212",
    foreground="#E0E0E0",
    cursor_color="#03A9F4",
    cursor_text="#121212",
    selection_background="#0D3F55",
    selection_foreground="#E0E0E0",
    # ANSI normal (0-7) — slightly muted for comfortable normal usage
    ansi_black="#121212",
    ansi_red="#F44336",
    ansi_green="#8BC34A",
    ansi_yellow="#FFC107",
    ansi_blue="#03A9F4",
    ansi_magenta="#9C27B0",
    ansi_cyan="#00BCD4",
    ansi_white="#B0B0B0",
    # ANSI bright (8-15) — full vivid palette values
    ansi_bright_black="#333333",
    ansi_bright_red="#EF5350",
    ansi_bright_green="#4CAF50",
    ansi_bright_yellow="#FFEB3B",
    ansi_bright_blue="#29B6F6",
    ansi_bright_magenta="#CE93D8",
    ansi_bright_cyan="#4DD0E1",
    ansi_bright_white="#E0E0E0",
):
    """Return the Ghostty dark theme config file as a string."""

    return f"""\
# Monad Dark
# Generated from Monad System colors.json
# Generated {datetime.now().strftime("%Y-%m-%d")}
#
# Install:  cp "Monad Dark" ~/.config/ghostty/themes/
# Activate: theme = Monad Dark
# OS sync:  theme = light:Monad Light,dark:Monad Dark

# ── Canvas ───────────────────────────────────────────────────────────────────
background = {background}
foreground = {foreground}

# ── Cursor ───────────────────────────────────────────────────────────────────
cursor-color       = {cursor_color}
cursor-text        = {cursor_text}
cursor-style       = block
cursor-style-blink = false

# ── Selection ────────────────────────────────────────────────────────────────
selection-background = {selection_background}
selection-foreground = {selection_foreground}

# ── ANSI palette — normal (0-7) ───────────────────────────────────────────────
palette = 0={ansi_black}
palette = 1={ansi_red}
palette = 2={ansi_green}
palette = 3={ansi_yellow}
palette = 4={ansi_blue}
palette = 5={ansi_magenta}
palette = 6={ansi_cyan}
palette = 7={ansi_white}

# ── ANSI palette — bright (8-15) ──────────────────────────────────────────────
palette = 8={ansi_bright_black}
palette = 9={ansi_bright_red}
palette = 10={ansi_bright_green}
palette = 11={ansi_bright_yellow}
palette = 12={ansi_bright_blue}
palette = 13={ansi_bright_magenta}
palette = 14={ansi_bright_cyan}
palette = 15={ansi_bright_white}
"""


def create_ghostty_light_theme(
    background="#f4f4f4",
    foreground="#161616",
    cursor_color="#0288d1",
    cursor_text="#ffffff",
    selection_background="#ABD3E9",
    selection_foreground="#161616",
    # ANSI normal (0-7) — darkened for contrast on light background
    ansi_black="#161616",
    ansi_red="#c62828",
    ansi_green="#558b2f",
    ansi_yellow="#e6ac00",
    ansi_blue="#0288d1",
    ansi_magenta="#6a1b9a",
    ansi_cyan="#00838f",
    ansi_white="#525252",
    # ANSI bright (8-15) — full vivid palette values for rich output
    ansi_bright_black="#8d8d8d",
    ansi_bright_red="#F44336",
    ansi_bright_green="#8BC34A",
    ansi_bright_yellow="#FFC107",
    ansi_bright_blue="#03A9F4",
    ansi_bright_magenta="#9C27B0",
    ansi_bright_cyan="#00BCD4",
    ansi_bright_white="#ffffff",
):
    """Return the Ghostty light theme config file as a string."""

    return f"""\
# Monad Light
# Derived from the Monad System design language — colors.json
# Generated {datetime.now().strftime("%Y-%m-%d")}
#
# Install:  cp "Monad Light" ~/.config/ghostty/themes/
# Activate: theme = Monad Light
# OS sync:  theme = light:Monad Light,dark:Monad Dark

# ── Canvas ───────────────────────────────────────────────────────────────────
background = {background}
foreground = {foreground}

# ── Cursor ───────────────────────────────────────────────────────────────────
cursor-color       = {cursor_color}
cursor-text        = {cursor_text}
cursor-style       = block
cursor-style-blink = false

# ── Selection ────────────────────────────────────────────────────────────────
selection-background = {selection_background}
selection-foreground = {selection_foreground}

# ── ANSI palette — normal (0-7) ───────────────────────────────────────────────
palette = 0={ansi_black}
palette = 1={ansi_red}
palette = 2={ansi_green}
palette = 3={ansi_yellow}
palette = 4={ansi_blue}
palette = 5={ansi_magenta}
palette = 6={ansi_cyan}
palette = 7={ansi_white}

# ── ANSI palette — bright (8-15) ──────────────────────────────────────────────
palette = 8={ansi_bright_black}
palette = 9={ansi_bright_red}
palette = 10={ansi_bright_green}
palette = 11={ansi_bright_yellow}
palette = 12={ansi_bright_blue}
palette = 13={ansi_bright_magenta}
palette = 14={ansi_bright_cyan}
palette = 15={ansi_bright_white}
"""
