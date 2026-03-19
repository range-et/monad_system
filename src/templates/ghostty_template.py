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
    background="#0F1113",
    foreground="#EEF2F6",
    cursor_color="#1E88C8",
    cursor_text="#0F1113",
    selection_background="#143549",
    selection_foreground="#EEF2F6",
    # ANSI normal (0-7) — slightly muted for comfortable normal usage
    ansi_black="#0F1113",
    ansi_red="#D64C45",
    ansi_green="#6EAD45",
    ansi_yellow="#D7A12A",
    ansi_blue="#1E88C8",
    ansi_magenta="#9C27B0",
    ansi_cyan="#2B9ED1",
    ansi_white="#B6BFCC",
    # ANSI bright (8-15) — full vivid palette values
    ansi_bright_black="#2A313A",
    ansi_bright_red="#E15049",
    ansi_bright_green="#4CAF50",
    ansi_bright_yellow="#FFEB3B",
    ansi_bright_blue="#349CD8",
    ansi_bright_magenta="#B15CC9",
    ansi_bright_cyan="#5EB5DD",
    ansi_bright_white="#EEF2F6",
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
    background="#F2F4F7",
    foreground="#141A22",
    cursor_color="#1A74AA",
    cursor_text="#ffffff",
    selection_background="#B1CEE0",
    selection_foreground="#141A22",
    # ANSI normal (0-7) — darkened for contrast on light background
    ansi_black="#141A22",
    ansi_red="#963531",
    ansi_green="#47702D",
    ansi_yellow="#C29126",
    ansi_blue="#1A74AA",
    ansi_magenta="#6D1B7B",
    ansi_cyan="#1C6788",
    ansi_white="#4F5A69",
    # ANSI bright (8-15) — full vivid palette values for rich output
    ansi_bright_black="#7E8998",
    ansi_bright_red="#D64C45",
    ansi_bright_green="#6EAD45",
    ansi_bright_yellow="#D7A12A",
    ansi_bright_blue="#1E88C8",
    ansi_bright_magenta="#9C27B0",
    ansi_bright_cyan="#2B9ED1",
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
