"""
Streamlit theme generator for the Monad System.

Emits two artifacts:

  1. ``config.toml``        — drop-in ``.streamlit/config.toml`` with both a
                              default (dark) ``[theme]`` block and a complete
                              light theme defined under ``[theme.light]`` for
                              users who want to flip the base manually.
  2. ``monad_streamlit.py`` — a small helper module that exposes
                              ``apply_monad_theme(mode="dark"|"light")``.
                              Calling it after ``st.set_page_config`` injects
                              the full Strata token set + Atomos surface
                              styling via ``st.markdown(... unsafe_allow_html
                              =True)``, so a Streamlit app inherits the same
                              Monad look that the CSS/JS targets ship.

Install:
    cp build/themes/streamlit/config.toml         your_app/.streamlit/config.toml
    cp build/themes/streamlit/monad_streamlit.py  your_app/

Use:
    import streamlit as st
    from monad_streamlit import apply_monad_theme

    st.set_page_config(page_title="My App", layout="wide")
    apply_monad_theme("dark")    # or "light"
"""

from datetime import datetime


# ─── config.toml ─────────────────────────────────────────────────────────────

def create_streamlit_config(
    *,
    # Dark (default) theme
    bg_dark,
    layer01_dark,
    layer02_dark,
    text_primary_dark,
    border_dark,
    interactive,
    interactive_hover,
    support_error,
    # Light theme
    bg_light,
    layer01_light,
    layer02_light,
    text_primary_light,
    border_light,
    interactive_light,
):
    """
    Return a ``.streamlit/config.toml`` string with a dark default ``[theme]``
    block and a complete ``[theme.light]`` override block.

    Streamlit reads the ``[theme]`` section automatically. The light variant
    is provided as a separate sibling block; users can swap by renaming or
    by maintaining ``config-light.toml`` alongside.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    return f"""\
# Monad System — Streamlit theme
# Generated from colors.json on {today}
#
# Drop into your app at: .streamlit/config.toml
# The default [theme] below is the Monad dark theme. To switch to light,
# either copy config-light.toml over this file, or copy the values from
# the [theme.light] reference block at the bottom of this file into [theme].
#
# For programmatic, per-page styling (Atomos surfaces, borders, focus rings)
# call ``apply_monad_theme()`` from ``monad_streamlit.py`` in your app.

[theme]
base                     = "dark"
primaryColor             = "{interactive}"
backgroundColor          = "{bg_dark}"
secondaryBackgroundColor = "{layer02_dark}"
textColor                = "{text_primary_dark}"
linkColor                = "{interactive_hover}"
borderColor              = "{border_dark}"
codeBackgroundColor      = "{layer01_dark}"
font                     = "sans serif"
codeFont                 = "monospace"
baseRadius               = "none"
showWidgetBorder         = true

[theme.sidebar]
backgroundColor          = "{layer01_dark}"
secondaryBackgroundColor = "{layer02_dark}"
textColor                = "{text_primary_dark}"
borderColor              = "{border_dark}"

# ── Reference: Monad Light theme ─────────────────────────────────────────────
# These values mirror Light_Mode in colors.json. To activate, paste them into
# the [theme] block above (replacing the dark values), or replace this file
# with config-light.toml.
#
# [theme]
# base                     = "light"
# primaryColor             = "{interactive_light}"
# backgroundColor          = "{bg_light}"
# secondaryBackgroundColor = "{layer02_light}"
# textColor                = "{text_primary_light}"
# linkColor                = "{interactive_light}"
# borderColor              = "{border_light}"
# codeBackgroundColor      = "{layer01_light}"
# font                     = "sans serif"
# codeFont                 = "monospace"
# baseRadius               = "none"
# showWidgetBorder         = true
"""


def create_streamlit_config_light(
    *,
    bg_light,
    layer01_light,
    layer02_light,
    text_primary_light,
    border_light,
    interactive_light,
):
    """Return a standalone Monad Light ``config.toml``."""
    today = datetime.now().strftime("%Y-%m-%d")
    return f"""\
# Monad System — Streamlit theme (Light)
# Generated from colors.json on {today}
#
# Drop into your app at: .streamlit/config.toml

[theme]
base                     = "light"
primaryColor             = "{interactive_light}"
backgroundColor          = "{bg_light}"
secondaryBackgroundColor = "{layer02_light}"
textColor                = "{text_primary_light}"
linkColor                = "{interactive_light}"
borderColor              = "{border_light}"
codeBackgroundColor      = "{layer01_light}"
font                     = "sans serif"
codeFont                 = "monospace"
baseRadius               = "none"
showWidgetBorder         = true

[theme.sidebar]
backgroundColor          = "{layer01_light}"
secondaryBackgroundColor = "{layer02_light}"
textColor                = "{text_primary_light}"
borderColor              = "{border_light}"
"""


# ─── monad_streamlit.py helper module ────────────────────────────────────────

def create_streamlit_helper(
    *,
    # Dark
    bg_dark,
    layer01_dark,
    layer02_dark,
    layer03_dark,
    text_primary_dark,
    text_secondary_dark,
    text_disabled_dark,
    border_dark,
    border_subtle_dark,
    # Light
    bg_light,
    layer01_light,
    layer02_light,
    layer03_light,
    text_primary_light,
    text_secondary_light,
    text_disabled_light,
    border_light,
    border_subtle_light,
    # Signals (shared)
    interactive,
    interactive_hover,
    interactive_active,
    interactive_light,
    support_info,
    support_success,
    support_warning,
    support_error,
    highlight,
    disabled,
    # Motion
    threshold_fast="80ms linear",
    threshold_base="160ms linear",
    threshold_slow="280ms linear",
):
    """
    Return a Python helper module string that, when placed next to a
    Streamlit app, exposes ``apply_monad_theme(mode)`` to inject the full
    Monad token set and Atomos primitive styles via a single
    ``st.markdown`` call.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    return f'''\
"""
monad_streamlit.py
==================

Apply the Monad System design language to a Streamlit app.

Generated from colors.json on {today}.

Usage
-----
    import streamlit as st
    from monad_streamlit import apply_monad_theme

    st.set_page_config(page_title="My App", layout="wide")
    apply_monad_theme("dark")   # or "light", or "auto" to follow Streamlit
                                # base when set in .streamlit/config.toml
"""

from typing import Literal

import streamlit as st


# ── Token tables ─────────────────────────────────────────────────────────────

DARK_TOKENS = {{
    "background":       "{bg_dark}",
    "layer-01":         "{layer01_dark}",
    "layer-02":         "{layer02_dark}",
    "layer-03":         "{layer03_dark}",
    "text-primary":     "{text_primary_dark}",
    "text-secondary":   "{text_secondary_dark}",
    "text-disabled":    "{text_disabled_dark}",
    "border":           "{border_dark}",
    "border-subtle":    "{border_subtle_dark}",
}}

LIGHT_TOKENS = {{
    "background":       "{bg_light}",
    "layer-01":         "{layer01_light}",
    "layer-02":         "{layer02_light}",
    "layer-03":         "{layer03_light}",
    "text-primary":     "{text_primary_light}",
    "text-secondary":   "{text_secondary_light}",
    "text-disabled":    "{text_disabled_light}",
    "border":           "{border_light}",
    "border-subtle":    "{border_subtle_light}",
}}

SIGNAL_TOKENS = {{
    "interactive":         "{interactive}",
    "interactive-hover":   "{interactive_hover}",
    "interactive-active":  "{interactive_active}",
    "support-info":        "{support_info}",
    "support-success":     "{support_success}",
    "support-warning":     "{support_warning}",
    "support-error":       "{support_error}",
    "highlight":           "{highlight}",
    "disabled":            "{disabled}",
}}

LIGHT_SIGNAL_OVERRIDES = {{
    "interactive":         "{interactive_light}",
}}

MOTION_TOKENS = {{
    "threshold-fast": "{threshold_fast}",
    "threshold-base": "{threshold_base}",
    "threshold-slow": "{threshold_slow}",
}}


# ── CSS builder ──────────────────────────────────────────────────────────────

def _root_block(surface: dict, signals: dict) -> str:
    lines = []
    for k, v in surface.items():
        lines.append(f"  --strata-{{k}}: {{v}};")
    for k, v in signals.items():
        lines.append(f"  --strata-{{k}}: {{v}};")
    for k, v in MOTION_TOKENS.items():
        lines.append(f"  --{{k}}: {{v}};")
    return "\\n".join(lines)


def _build_css(mode: str) -> str:
    if mode == "light":
        surface = LIGHT_TOKENS
        signals = {{**SIGNAL_TOKENS, **LIGHT_SIGNAL_OVERRIDES}}
    else:
        surface = DARK_TOKENS
        signals = SIGNAL_TOKENS

    root = _root_block(surface, signals)

    return f"""
<style>
:root {{{{
{{root}}
}}}}

/* ── App canvas ────────────────────────────────────────────────────────── */
html, body, [data-testid="stApp"], .stApp,
[data-testid="stAppViewContainer"] > .main {{{{
  background-color: var(--strata-background) !important;
  color: var(--strata-text-primary) !important;
  font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
}}}}

/* ── Sidebar ────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {{{{
  background-color: var(--strata-layer-01) !important;
  border-right: 1px solid var(--strata-border-subtle);
}}}}
section[data-testid="stSidebar"] * {{{{
  color: var(--strata-text-primary);
}}}}

/* ── Headings ──────────────────────────────────────────────────────────── */
h1, h2, h3, h4, h5, h6 {{{{
  color: var(--strata-text-primary);
  font-weight: 600;
  letter-spacing: -0.01em;
}}}}

/* ── Body text ─────────────────────────────────────────────────────────── */
p, span, label, li, .stMarkdown {{{{
  color: var(--strata-text-primary);
}}}}
small, .caption, [data-testid="stCaptionContainer"] {{{{
  color: var(--strata-text-secondary);
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}}}}

/* ── Inputs (Atomos surface tier) ──────────────────────────────────────── */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stDateInput input,
.stTimeInput input,
.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div {{{{
  background-color: var(--strata-layer-01) !important;
  color: var(--strata-text-primary) !important;
  border: 1px solid var(--strata-border) !important;
  border-radius: 0 !important;
  transition: border-color var(--threshold-fast),
              box-shadow var(--threshold-fast);
}}}}
.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {{{{
  outline: none !important;
  border-color: var(--strata-interactive) !important;
  box-shadow: 0 0 0 2px var(--strata-interactive) !important;
}}}}

/* ── Buttons ───────────────────────────────────────────────────────────── */
.stButton > button,
.stDownloadButton > button,
.stFormSubmitButton > button {{{{
  background-color: var(--strata-layer-02);
  color: var(--strata-text-primary);
  border: 1px solid var(--strata-border);
  border-radius: 0;
  font-weight: 500;
  transition: background-color var(--threshold-fast),
              border-color    var(--threshold-fast),
              color           var(--threshold-fast);
}}}}
.stButton > button:hover,
.stDownloadButton > button:hover,
.stFormSubmitButton > button:hover {{{{
  background-color: var(--strata-interactive);
  border-color:     var(--strata-interactive);
  color: #ffffff;
}}}}
.stButton > button:active,
.stDownloadButton > button:active,
.stFormSubmitButton > button:active {{{{
  background-color: var(--strata-interactive-active);
  border-color:     var(--strata-interactive-active);
}}}}
.stButton > button:focus-visible {{{{
  outline: 2px solid var(--strata-interactive);
  outline-offset: 2px;
}}}}

/* Primary button (kind="primary") */
.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {{{{
  background-color: var(--strata-interactive);
  border-color:     var(--strata-interactive);
  color: #ffffff;
}}}}
.stButton > button[kind="primary"]:hover {{{{
  background-color: var(--strata-interactive-hover);
  border-color:     var(--strata-interactive-hover);
}}}}

/* ── Sliders, checkboxes, radios — accent only ─────────────────────────── */
input[type="range"],
input[type="checkbox"],
input[type="radio"] {{{{
  accent-color: var(--strata-interactive);
}}}}

/* ── Tabs ──────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {{{{
  border-bottom: 1px solid var(--strata-border-subtle);
  gap: 0;
}}}}
.stTabs [data-baseweb="tab"] {{{{
  background: transparent;
  border: none;
  color: var(--strata-text-secondary);
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 0.75rem;
}}}}
.stTabs [aria-selected="true"] {{{{
  color: var(--strata-text-primary) !important;
  border-bottom: 2px solid var(--strata-interactive) !important;
}}}}

/* ── Code, pre, kbd ────────────────────────────────────────────────────── */
code, pre, kbd, samp, .stCode {{{{
  background-color: var(--strata-layer-01) !important;
  color: var(--strata-text-primary) !important;
  border: 1px solid var(--strata-border-subtle);
  border-radius: 0;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}}}}

/* ── Tables / dataframes ───────────────────────────────────────────────── */
[data-testid="stDataFrame"], [data-testid="stTable"] {{{{
  border: 1px solid var(--strata-border-subtle);
}}}}
[data-testid="stDataFrame"] th {{{{
  background-color: var(--strata-layer-02) !important;
  color: var(--strata-text-secondary) !important;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  font-size: 0.72rem;
}}}}

/* ── Metrics ───────────────────────────────────────────────────────────── */
[data-testid="stMetric"] {{{{
  background-color: var(--strata-layer-01);
  border: 1px solid var(--strata-border-subtle);
  padding: 0.75rem 1rem;
}}}}
[data-testid="stMetricLabel"] {{{{
  color: var(--strata-text-secondary) !important;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 0.7rem;
}}}}
[data-testid="stMetricValue"] {{{{
  color: var(--strata-text-primary) !important;
  font-weight: 600;
}}}}

/* ── Status surfaces (alerts) ──────────────────────────────────────────── */
[data-testid="stAlert"] {{{{
  border-radius: 0 !important;
  border-left-width: 3px !important;
}}}}
[data-baseweb="notification"][kind="info"]    {{{{ border-color: var(--strata-support-info)    !important; }}}}
[data-baseweb="notification"][kind="positive"]{{{{ border-color: var(--strata-support-success) !important; }}}}
[data-baseweb="notification"][kind="warning"] {{{{ border-color: var(--strata-support-warning) !important; }}}}
[data-baseweb="notification"][kind="negative"]{{{{ border-color: var(--strata-support-error)   !important; }}}}

/* ── Dividers & expanders ──────────────────────────────────────────────── */
hr, [data-testid="stDivider"] {{{{
  border-color: var(--strata-border-subtle);
}}}}
[data-testid="stExpander"] {{{{
  border: 1px solid var(--strata-border-subtle) !important;
  border-radius: 0 !important;
  background-color: var(--strata-layer-01);
}}}}

/* ── Reduced motion ────────────────────────────────────────────────────── */
@media (prefers-reduced-motion: reduce) {{{{
  *, *::before, *::after {{{{
    transition-duration: 0ms !important;
    animation-duration: 0ms !important;
  }}}}
}}}}
</style>
"""


# ── Public API ───────────────────────────────────────────────────────────────

Mode = Literal["dark", "light"]


def apply_monad_theme(mode: Mode = "dark") -> None:
    """
    Inject the Monad Strata token set + Atomos surface styles into the
    current Streamlit page.

    Call once per page, immediately after ``st.set_page_config``.

    Parameters
    ----------
    mode : "dark" | "light"
        Which surface palette to apply. Signals (interactive / support /
        highlight) come from ``Default_Colors`` in colors.json regardless of
        mode, with the interactive accent darkened on light surfaces for
        contrast.
    """
    if mode not in ("dark", "light"):
        raise ValueError(f'mode must be "dark" or "light", got {{mode!r}}')
    st.markdown(_build_css(mode), unsafe_allow_html=True)


def get_tokens(mode: Mode = "dark") -> dict:
    """
    Return the resolved token dictionary for the requested mode. Useful when
    you need to pass colors to Plotly / Altair / Matplotlib charts inside a
    Streamlit app so they match the surrounding shell.
    """
    if mode == "light":
        return {{**LIGHT_TOKENS, **SIGNAL_TOKENS, **LIGHT_SIGNAL_OVERRIDES, **MOTION_TOKENS}}
    return {{**DARK_TOKENS, **SIGNAL_TOKENS, **MOTION_TOKENS}}


__all__ = ["apply_monad_theme", "get_tokens",
           "DARK_TOKENS", "LIGHT_TOKENS", "SIGNAL_TOKENS", "MOTION_TOKENS"]
'''


# ─── README.md ───────────────────────────────────────────────────────────────

def create_streamlit_readme():
    today = datetime.now().strftime("%Y-%m-%d")
    return f"""\
# Monad System — Streamlit theme

Generated from `colors.json` on {today}.

Two artifacts ship in this directory:

| File                  | Purpose                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| `config.toml`         | Drop-in `.streamlit/config.toml` (default = Monad Dark, light reference)|
| `config-light.toml`   | Standalone Monad Light variant of the above                             |
| `monad_streamlit.py`  | Python helper — `apply_monad_theme("dark"\\|"light")` for full styling  |

## Quick start

```bash
mkdir -p your_app/.streamlit
cp config.toml         your_app/.streamlit/config.toml
cp monad_streamlit.py  your_app/
```

```python
# your_app/app.py
import streamlit as st
from monad_streamlit import apply_monad_theme

st.set_page_config(page_title="Monad app", layout="wide")
apply_monad_theme("dark")          # or "light"

st.title("Monad ✕ Streamlit")
st.write("All Strata tokens are now live as CSS custom properties.")
```

## What you get

- The native Streamlit theme system (`config.toml`) is configured so the
  app shell — sidebar, primary color, background, borders, code blocks —
  matches Monad without any custom code.
- `apply_monad_theme()` extends that with the full Strata token set
  (`--strata-*` custom properties), Atomos surface treatments
  (square corners, mono labels, focus rings on `--strata-interactive`,
  `prefers-reduced-motion` support), and styling for buttons, tabs,
  metrics, dataframes, alerts, and expanders.
- `get_tokens(mode)` returns a plain dict so you can hand the same colors
  to Plotly / Altair / Matplotlib charts inside the app.

## Theme switching

Streamlit's `config.toml` is read once at process start, so the *base*
theme is fixed per app. To toggle dark/light at runtime, rerun
`apply_monad_theme(mode)` based on a `st.toggle` or query param —
the helper rewrites the `<style>` block on every rerun.
"""
