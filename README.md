# Monad System

A personal design language built on `colors.json`.

> "Form follows Function. Every element earns its place."

This is not Carbon. Not shadcn. It is an **engineered framework** — orthogonal, materially honest, and multi-platform.

---

## Tiers

| Tier | Role | Scope |
|---|---|---|
| **Strata** | Connective state — CSS tokens, theme | `--strata-*` |
| **Monad** | Structural layout — root containers | `.monad-*` |
| **Atomos** | Primitive components — indivisible units | `.atomos-*` |
| **Threshold** | Navigation & transitions | `.threshold-*` |

---

## Build Artifacts

Run the compile script to regenerate all artifacts from `colors.json`:

```bash
python src/compile_color.py --json_path colors.json --output_path build/
```

| File | Platform | Theme | Description |
|---|---|---|---|
| `build/monad.css` | HTML / CSS | Dark + Light | Full Monad System — Strata tokens, Atomos components, Monad layout, Threshold nav |
| `build/monad.js` | HTML / JS | — | Strata toggle, Threshold nav, Rail drawer runtime |
| `build/ColorPalette.css` | HTML / CSS | Dark | Raw CSS token variables only |
| `build/ColorPalette.cs` | Unity C# | Dark | Static color class — dark Strata |
| `build/ColorPaletteLight.cs` | Unity C# | Light | Static color class — light Strata |
| `build/seaborn_palette.py` | Python | Dual | matplotlib / seaborn palette helpers |

---

## Samples

| File | Description |
|---|---|
| `samples/components.html` | Atomos showcase — all components |
| `samples/dashboard.html` | Monad shell — full app dashboard |

---

## Visual Principles

1. **Orthogonal** — No border-radius. Softness is decoration.
2. **Materially Honest** — No gradients. No decorative shadows. Depth via layered borders.
3. **Haptic** — Transitions are `80ms linear`. Motion is predictable, not expressive.
4. **High-contrast states** — Hover/active swap color completely, not fade opacity.
5. **Mono for data** — Numeric values, overlines, IDs use JetBrains Mono.

---

## HTML / CSS / JS Usage

```html
<link rel="stylesheet" href="path/to/build/monad.css">
<script src="path/to/build/monad.js"></script>
```

### Theming

Dark is default (`:root`). Light is `[data-strata="light"]`.

```html
<button data-mn-theme-toggle>◑</button>
```

`monad.js` persists choice to `localStorage` and respects `prefers-color-scheme`.

### Layout Shell

```html
<header class="monad-header">
  <button class="threshold-toggle" data-mn-rail-toggle>☰</button>
  <span class="monad-header__name">App</span>
  <nav class="threshold-nav">
    <a href="#" class="active">Overview</a>
  </nav>
  <div class="monad-header__actions">
    <button class="strata-toggle" data-mn-theme-toggle>◑</button>
  </div>
</header>

<div class="monad-layout">
  <nav class="monad-rail">
    <div class="monad-rail__section">Main</div>
    <a class="monad-rail__item active" href="#">Dashboard</a>
  </nav>
  <main class="monad-content">
    <!-- content -->
  </main>
</div>
```

### Key Components

```html
<!-- Buttons -->
<button class="atomos-btn atomos-btn--primary">Action</button>
<button class="atomos-btn atomos-btn--secondary">Secondary</button>
<button class="atomos-btn atomos-btn--ghost">Ghost</button>

<!-- Card -->
<div class="atomos-card">
  <div class="atomos-card__header">
    <span class="atomos-card__title">Title</span>
  </div>
  <div class="atomos-card__body">Content here.</div>
</div>

<!-- Stat / KPI -->
<div class="atomos-stat atomos-stat--signal">
  <div class="atomos-stat__eyebrow">Metric</div>
  <div class="atomos-stat__value">2,847</div>
  <div class="atomos-stat__delta atomos-stat__delta--up">↑ 12%</div>
</div>

<!-- Tags -->
<span class="atomos-tag atomos-tag--success">ok</span>
<span class="atomos-tag atomos-tag--error">error</span>

<!-- Notice -->
<div class="atomos-notice atomos-notice--warning">
  <span class="atomos-notice__icon">!</span>
  <div class="atomos-notice__body">
    <div class="atomos-notice__title">Warning</div>
    <div class="atomos-notice__msg">Something needs attention.</div>
  </div>
</div>

<!-- Form -->
<div class="atomos-field">
  <label class="atomos-label">Field</label>
  <input class="atomos-input" type="text" placeholder="...">
</div>

<!-- Table -->
<div class="atomos-table-wrap">
  <table class="atomos-table">
    <thead><tr><th>Col</th></tr></thead>
    <tbody><tr><td>Row</td></tr></tbody>
  </table>
</div>

<!-- Progress -->
<div class="atomos-progress">
  <div class="atomos-progress__fill" style="--progress:72%"></div>
</div>
```

### Grid

```html
<div class="monad-grid">
  <div class="monad-col-8">Half</div>
  <div class="monad-col-8">Half</div>
</div>
```

16 columns → 8 (≤1056px) → 4 (≤672px).

### Custom Styles

Reference only Strata tokens:

```css
.my-component {
  background: var(--strata-layer-01);
  border: 1px solid var(--strata-border);
  color: var(--strata-text-primary);
  transition: background var(--threshold-fast);
}
```

---

## Unity C#

```csharp
// Dark Strata
Color bg = ColorPalette.Background;
Color signal = ColorPalette.Information2;

// Light Strata
Color bgLight = ColorPaletteLight.Background;
```

---

## Python / Seaborn / Matplotlib

```python
from build.seaborn_palette import (
    PALETTE_DARK, PALETTE_LIGHT,
    CATEGORICAL, STATUS_COLORS, MOVEMENT_COLORS,
    make_sequential_cmap, apply_dark_theme, apply_light_theme
)

apply_dark_theme()

import matplotlib.pyplot as plt
import seaborn as sns
sns.barplot(x=..., y=..., palette=CATEGORICAL)
```

---

## Color Architecture

Defined in `colors.json`. Two sections:

- `Default_Colors` — dark Strata ground + all shared semantic colors
- `Light_Mode` — light Strata ground overrides

Shared across both themes: interactive, status, movement domain colors.

### Dark Strata

| Token | Hex | Role |
|---|---|---|
| `--strata-bg` | `#121212` | Ground |
| `--strata-layer-01` | `#1e1e1e` | Raised surface |
| `--strata-layer-02` | `#262626` | Double-raised |
| `--strata-layer-03` | `#333333` | Triple-raised |
| `--strata-interactive` | `#03A9F4` | Signal blue |
| `--strata-success` | `#8BC34A` | |
| `--strata-warning` | `#FFC107` | |
| `--strata-error` | `#F44336` | |

### Light Strata

| Token | Hex | Role |
|---|---|---|
| `--strata-bg` | `#f4f4f4` | Ground |
| `--strata-layer-01` | `#ffffff` | Raised surface |
| `--strata-layer-02` | `#f4f4f4` | Double-raised |
| `--strata-layer-03` | `#e8e8e8` | Triple-raised |

---

## Typography

| Stack | Variable | Use |
|---|---|---|
| Inter | `--font-sans` | All UI text |
| JetBrains Mono | `--font-mono` | Labels, overlines, data, code |
| Lora | `--font-serif` | Editorial / longform only |

All loaded from Google Fonts.

---

## AI Skill

The Cursor / Gemini skill is at `.cursor/skills/monad-system/SKILL.md`.

It defines:
- All tier names and class prefixes
- Component reference with exact HTML
- Visual rules (no radius, no shadow, haptic transitions)
- What NOT to do

---

## Clone Into Another Project

```bash
# Add as remote
git remote add monad https://github.com/YOUR/default_colors.git
git fetch monad

# Copy build artifacts
cp monad/build/monad.css  your-project/static/
cp monad/build/monad.js   your-project/static/

# Or submodule
git submodule add https://github.com/YOUR/default_colors.git design-tokens
```

Reference `design-tokens/build/monad.css` in your HTML.

---

## What NOT to Do

- Do not use `ds-*` classes — retired
- Do not hardcode hex colors in components — use `--strata-*`
- Do not add `border-radius` to Atomos
- Do not use movement hold colors for generic UI status
- Do not use `box-shadow` for depth
- Do not use `ease` timing — use `var(--threshold-fast)` (80ms linear)
