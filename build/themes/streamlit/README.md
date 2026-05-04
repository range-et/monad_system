# Monad System — Streamlit theme

Generated from `colors.json` on 2026-05-04.

Two artifacts ship in this directory:

| File                  | Purpose                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| `config.toml`         | Drop-in `.streamlit/config.toml` (default = Monad Dark, light reference)|
| `config-light.toml`   | Standalone Monad Light variant of the above                             |
| `monad_streamlit.py`  | Python helper — `apply_monad_theme("dark"\|"light")` for full styling  |

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
