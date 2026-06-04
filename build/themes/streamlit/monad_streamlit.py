"""
monad_streamlit.py
==================

Apply the Monad System design language to a Streamlit app.

Generated from colors.json on 2026-06-03.

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

DARK_TOKENS = {
    "background":       "#0F1113",
    "layer-01":         "#171A1E",
    "layer-02":         "#1F242B",
    "layer-03":         "#2A313A",
    "text-primary":     "#EEF2F6",
    "text-secondary":   "#B6BFCC",
    "text-disabled":    "#7D8794",
    "border":           "#3A434F",
    "border-subtle":    "#2B323A",
}

LIGHT_TOKENS = {
    "background":       "#F2F4F7",
    "layer-01":         "#ffffff",
    "layer-02":         "#EDF1F5",
    "layer-03":         "#E3E8EE",
    "text-primary":     "#141A22",
    "text-secondary":   "#4F5A69",
    "text-disabled":    "#7E8998",
    "border":           "#BCC6D2",
    "border-subtle":    "#D8DFE7",
}

SIGNAL_TOKENS = {
    "interactive":         "#1E88C8",
    "interactive-hover":   "#1973AA",
    "interactive-active":  "#166696",
    "support-info":        "#2B9ED1",
    "support-success":     "#6EAD45",
    "support-warning":     "#D7A12A",
    "support-error":       "#E4002B",
    "highlight":           "#FFEB3B",
    "disabled":            "#757575",
}

LIGHT_SIGNAL_OVERRIDES = {
    "interactive":         "#1973AA",
}

MOTION_TOKENS = {
    "threshold-fast": "80ms linear",
    "threshold-base": "160ms linear",
    "threshold-slow": "280ms linear",
}


# ── CSS builder ──────────────────────────────────────────────────────────────

def _root_block(surface: dict, signals: dict) -> str:
    lines = []
    for k, v in surface.items():
        lines.append(f"  --strata-{k}: {v};")
    for k, v in signals.items():
        lines.append(f"  --strata-{k}: {v};")
    for k, v in MOTION_TOKENS.items():
        lines.append(f"  --{k}: {v};")
    return "\n".join(lines)


def _build_css(mode: str) -> str:
    if mode == "light":
        surface = LIGHT_TOKENS
        signals = {**SIGNAL_TOKENS, **LIGHT_SIGNAL_OVERRIDES}
    else:
        surface = DARK_TOKENS
        signals = SIGNAL_TOKENS

    root = _root_block(surface, signals)

    return f"""
<style>
:root {{
{root}
}}

/* ── App canvas ────────────────────────────────────────────────────────── */
html, body, [data-testid="stApp"], .stApp,
[data-testid="stAppViewContainer"] > .main {{
  background-color: var(--strata-background) !important;
  color: var(--strata-text-primary) !important;
  font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
}}

/* ── Sidebar ────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {{
  background-color: var(--strata-layer-01) !important;
  border-right: 1px solid var(--strata-border-subtle);
}}
section[data-testid="stSidebar"] * {{
  color: var(--strata-text-primary);
}}

/* ── Headings ──────────────────────────────────────────────────────────── */
h1, h2, h3, h4, h5, h6 {{
  color: var(--strata-text-primary);
  font-weight: 600;
  letter-spacing: -0.01em;
}}

/* ── Body text ─────────────────────────────────────────────────────────── */
p, span, label, li, .stMarkdown {{
  color: var(--strata-text-primary);
}}
small, .caption, [data-testid="stCaptionContainer"] {{
  color: var(--strata-text-secondary);
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}}

/* ── Inputs (Atomos surface tier) ──────────────────────────────────────── */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stDateInput input,
.stTimeInput input,
.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div {{
  background-color: var(--strata-layer-01) !important;
  color: var(--strata-text-primary) !important;
  border: 1px solid var(--strata-border) !important;
  border-radius: 0 !important;
  transition: border-color var(--threshold-fast),
              box-shadow var(--threshold-fast);
}}
.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {{
  outline: none !important;
  border-color: var(--strata-interactive) !important;
  box-shadow: 0 0 0 2px var(--strata-interactive) !important;
}}

/* ── Buttons ───────────────────────────────────────────────────────────── */
.stButton > button,
.stDownloadButton > button,
.stFormSubmitButton > button {{
  background-color: var(--strata-layer-02);
  color: var(--strata-text-primary);
  border: 1px solid var(--strata-border);
  border-radius: 0;
  font-weight: 500;
  transition: background-color var(--threshold-fast),
              border-color    var(--threshold-fast),
              color           var(--threshold-fast);
}}
.stButton > button:hover,
.stDownloadButton > button:hover,
.stFormSubmitButton > button:hover {{
  background-color: var(--strata-interactive);
  border-color:     var(--strata-interactive);
  color: #ffffff;
}}
.stButton > button:active,
.stDownloadButton > button:active,
.stFormSubmitButton > button:active {{
  background-color: var(--strata-interactive-active);
  border-color:     var(--strata-interactive-active);
}}
.stButton > button:focus-visible {{
  outline: 2px solid var(--strata-interactive);
  outline-offset: 2px;
}}

/* Primary button (kind="primary") */
.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {{
  background-color: var(--strata-interactive);
  border-color:     var(--strata-interactive);
  color: #ffffff;
}}
.stButton > button[kind="primary"]:hover {{
  background-color: var(--strata-interactive-hover);
  border-color:     var(--strata-interactive-hover);
}}

/* ── Sliders, checkboxes, radios — accent only ─────────────────────────── */
input[type="range"],
input[type="checkbox"],
input[type="radio"] {{
  accent-color: var(--strata-interactive);
}}

/* ── Tabs ──────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {{
  border-bottom: 1px solid var(--strata-border-subtle);
  gap: 0;
}}
.stTabs [data-baseweb="tab"] {{
  background: transparent;
  border: none;
  color: var(--strata-text-secondary);
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 0.75rem;
}}
.stTabs [aria-selected="true"] {{
  color: var(--strata-text-primary) !important;
  border-bottom: 2px solid var(--strata-interactive) !important;
}}

/* ── Code, pre, kbd ────────────────────────────────────────────────────── */
code, pre, kbd, samp, .stCode {{
  background-color: var(--strata-layer-01) !important;
  color: var(--strata-text-primary) !important;
  border: 1px solid var(--strata-border-subtle);
  border-radius: 0;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}}

/* ── Tables / dataframes ───────────────────────────────────────────────── */
[data-testid="stDataFrame"], [data-testid="stTable"] {{
  border: 1px solid var(--strata-border-subtle);
}}
[data-testid="stDataFrame"] th {{
  background-color: var(--strata-layer-02) !important;
  color: var(--strata-text-secondary) !important;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  font-size: 0.72rem;
}}

/* ── Metrics ───────────────────────────────────────────────────────────── */
[data-testid="stMetric"] {{
  background-color: var(--strata-layer-01);
  border: 1px solid var(--strata-border-subtle);
  padding: 0.75rem 1rem;
}}
[data-testid="stMetricLabel"] {{
  color: var(--strata-text-secondary) !important;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 0.7rem;
}}
[data-testid="stMetricValue"] {{
  color: var(--strata-text-primary) !important;
  font-weight: 600;
}}

/* ── Status surfaces (alerts) ──────────────────────────────────────────── */
[data-testid="stAlert"] {{
  border-radius: 0 !important;
  border-left-width: 3px !important;
}}
[data-baseweb="notification"][kind="info"]    {{ border-color: var(--strata-support-info)    !important; }}
[data-baseweb="notification"][kind="positive"]{{ border-color: var(--strata-support-success) !important; }}
[data-baseweb="notification"][kind="warning"] {{ border-color: var(--strata-support-warning) !important; }}
[data-baseweb="notification"][kind="negative"]{{ border-color: var(--strata-support-error)   !important; }}

/* ── Dividers & expanders ──────────────────────────────────────────────── */
hr, [data-testid="stDivider"] {{
  border-color: var(--strata-border-subtle);
}}
[data-testid="stExpander"] {{
  border: 1px solid var(--strata-border-subtle) !important;
  border-radius: 0 !important;
  background-color: var(--strata-layer-01);
}}

/* ── Reduced motion ────────────────────────────────────────────────────── */
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{
    transition-duration: 0ms !important;
    animation-duration: 0ms !important;
  }}
}}
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
        raise ValueError(f'mode must be "dark" or "light", got {mode!r}')
    st.markdown(_build_css(mode), unsafe_allow_html=True)


def get_tokens(mode: Mode = "dark") -> dict:
    """
    Return the resolved token dictionary for the requested mode. Useful when
    you need to pass colors to Plotly / Altair / Matplotlib charts inside a
    Streamlit app so they match the surrounding shell.
    """
    if mode == "light":
        return {**LIGHT_TOKENS, **SIGNAL_TOKENS, **LIGHT_SIGNAL_OVERRIDES, **MOTION_TOKENS}
    return {**DARK_TOKENS, **SIGNAL_TOKENS, **MOTION_TOKENS}


__all__ = ["apply_monad_theme", "get_tokens",
           "DARK_TOKENS", "LIGHT_TOKENS", "SIGNAL_TOKENS", "MOTION_TOKENS"]
