# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Monad System is a multi-platform design system built from a single source of truth (`colors.json`). A Python compiler transforms color definitions into artifacts for 8+ platforms: CSS/JS (web), Unity C#, Python/Seaborn, VS Code themes, Ghostty terminal themes, Xcode themes, SwiftUI, and header-only C++/Arduino (TFT, OLED, e-ink).

Core philosophy: "Form follows Function. If it doesn't facilitate a function, delete it."

## Build & Development Commands

```bash
# Install Python dependencies
pip install -r requirements.txt

# Build all artifacts (colors.json → build/)
make                    # or: make build

# Build + serve + open browser
make dev

# Run tests
python -m unittest discover -s tests -p 'test_*.py' -v

# Run a single test
python -m unittest tests.test_compile_color_pipeline.CompileColorPipelineTests.test_name

# Install themes locally (VS Code, Ghostty, Xcode)
make install

# Clean build artifacts
make clean
```

## Architecture

### Compilation Pipeline

```
colors.json → src/compile_color.py → src/templates/*_template.py → build/
```

- `colors.json` — All color definitions (dark default + light overrides)
- `src/compile_color.py` — Main compiler, color math utilities (`_darken`, `_blend`, `_shift_bg`, `_rgba_alpha`), and `prepare_templates()` orchestrator
- `src/templates/` — Per-platform generators (css, js, c_sharp, python, vscode, ghostty, xcode, swiftui, cpp, motion, texture)
- `src/gen_icon.py` — PNG icon generator
- `src/preview_render.py` — Palette visualization renderer
- `build/` — All generated output (17 artifacts across platform subdirectories)

### Four-Tier Design System

| Tier | Role | CSS Scope |
|---|---|---|
| **Strata** | Tokens, theme, context | `--strata-*` custom properties |
| **Monad** | Structural layout, shell | `.monad-*` classes |
| **Atomos** | Primitive components | `.atomos-*` classes |
| **Threshold** | Navigation, transitions | `.threshold-*` classes |

### Key Conventions

- Components NEVER hardcode hex colors — always use `--strata-*` tokens
- Dark theme is `:root` default; light theme uses `[data-strata="light"]`
- No border-radius, no decorative shadows, no gradients
- All transitions use `var(--threshold-fast)` (80ms linear)
- Mono font (`--font-mono`) for data, labels, overlines, numeric values
- Movement hold colors (`atomos-hold--*`) are domain-specific — never repurpose for UI status
- `ds-*` classes are retired — do not use

### Testing

Tests (`tests/test_compile_color_pipeline.py`) verify cross-platform color propagation: that tokens from `colors.json` appear correctly in CSS, C#, Python, SwiftUI, VS Code, Ghostty, Xcode, and C++/Arduino output. Tests call `prepare_templates()` and inspect the returned artifact dictionary.

