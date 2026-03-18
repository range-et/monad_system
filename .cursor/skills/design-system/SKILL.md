---
name: design-system
description: Build UI with this project's design system — color tokens from colors.json, Carbon physical language (8px grid, Inter/JetBrains Mono/Lora typography, layering), Bootstrap-style component classes, and light/dark theming. Use for HTML/CSS/JS, Unity C#, and Python/matplotlib/seaborn work.
---

This skill governs all UI/UX work within this design system. It overrides generic color, typography, and spacing choices from other skills with the specific tokens, physical language, and component classes defined here. Read and follow every section.

---

## Single Source of Truth

All colors originate from `colors.json` at the repo root. The compiled artifacts in `build/` are generated from it:
- `build/design-system.css` — Bootstrap-style component library + both themes
- `build/ColorPalette.css` — raw CSS custom property tokens only
- `build/ColorPalette.cs` — Unity C# static color class
- `build/seaborn_palette.py` — Python/matplotlib/seaborn helpers

**Always reference `colors.json` for source values. Never hardcode hex values directly — use the token names.**

---

## Color Tokens

### Theme Architecture

Two complete token sets are built into `design-system.css`. Dark is the default. Light is opt-in via `data-theme="light"` on `<html>`.

```html
<!-- Dark (default, no attribute needed) -->
<html>

<!-- Light mode -->
<html data-theme="light">
```

A `prefers-color-scheme: light` media query provides OS-level fallback.

### Token Reference

**Theme-switched tokens** (values change between dark/light):

| CSS Token | Dark Value | Light Value | Role |
|---|---|---|---|
| `--color-bg` | `#121212` | `#f4f4f4` | Page background |
| `--color-layer-01` | `#1e1e1e` | `#ffffff` | First layer (cards, panels) |
| `--color-layer-02` | `#262626` | `#f4f4f4` | Second layer (nested elements) |
| `--color-layer-03` | `#333333` | `#e8e8e8` | Third layer (deeply nested) |
| `--color-text-primary` | `#E0E0E0` | `#161616` | Body text, headings |
| `--color-text-secondary` | `#B0B0B0` | `#525252` | Labels, captions, secondary |
| `--color-text-disabled` | `#757575` | `#8d8d8d` | Disabled/inactive text |
| `--color-border` | `#3d3d3d` | `#c6c6c6` | Dividers, input borders |
| `--color-border-subtle` | `#2a2a2a` | `#e0e0e0` | Subtle dividers |

**Shared tokens** (same in both themes):

| CSS Token | Value | Role |
|---|---|---|
| `--color-interactive` | `#03A9F4` | Primary actions, links, focus |
| `--color-interactive-hover` | `#0288d1` | Hover on interactive |
| `--color-interactive-active` | `#0277bd` | Active/pressed state |
| `--color-support-info` | `#00BCD4` | Neutral system status |
| `--color-support-info-alt` | `#03A9F4` | Secondary info / highlights |
| `--color-support-success` | `#8BC34A` | Positive / success |
| `--color-support-warning` | `#FFC107` | Caution / warning |
| `--color-support-error` | `#F44336` | Critical / error / alert |
| `--color-highlight` | `#FFEB3B` | Temporary emphasis / selection |
| `--color-disabled` | `#757575` | Disabled element fills |
| `--color-move-start` | `#4CAF50` | Start hold / waypoint |
| `--color-move-hand` | `#03A9F4` | Hand / upper body |
| `--color-move-foot` | `#FFEB3B` | Foot / lower body |
| `--color-move-finish` | `#9C27B0` | Finish hold / endpoint |
| `--color-overlay` | `rgba(0,0,0,0.5)` | Modal / drawer overlays |
| `--opacity-low` | `0.2` | Subtle fills, ghosts |
| `--opacity-high` | `0.8` | Near-opaque tints |

---

## Typography

This design system uses three Google Fonts typefaces — all widely available, no CDN lock-in:

| Role | Font | Why |
|---|---|---|
| **Sans / UI body** | Inter | Best-in-class legibility at small sizes; variable font; neutral but distinctive |
| **Mono / code** | JetBrains Mono | Excellent code legibility, ligature support, comfortable x-height |
| **Serif / editorial** | Lora | Elegant contrast to Inter; works well for display text, pull quotes, editorial sections |

`design-system.css` includes the Google Fonts `@import` automatically — no separate `<link>` tag needed. If you want to load them yourself for performance:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400;600&family=Lora:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
```

**Font stacks:**
```css
--font-sans:  'Inter', 'Helvetica Neue', Arial, sans-serif;
--font-mono:  'JetBrains Mono', 'Menlo', 'Courier New', monospace;
--font-serif: 'Lora', 'Georgia', Times, serif;
```

**Type scale (Carbon):**
| Step | rem | px | Usage |
|---|---|---|---|
| `--type-xs` | 0.75rem | 12px | Labels, captions |
| `--type-sm` | 0.875rem | 14px | Secondary body, helper text |
| `--type-base` | 1rem | 16px | Body text (default) |
| `--type-md` | 1.125rem | 18px | Lead paragraph |
| `--type-lg` | 1.25rem | 20px | Large body |
| `--type-xl` | 1.5rem | 24px | Section heading |
| `--type-2xl` | 1.75rem | 28px | Sub-page heading |
| `--type-3xl` | 2rem | 32px | Page heading |
| `--type-4xl` | 2.625rem | 42px | Display / hero |
| `--type-5xl` | 3.375rem | 54px | Large display |

**Weights:** Light (300), Regular (400), SemiBold (600) only. No bold (700).

---

## Grid & Spacing (Carbon 2x Grid)

**Base unit: 8px.** All spacing, sizing, and layout uses multiples of 8.

```css
--space-1:  8px;   /* 1x mini unit */
--space-2: 16px;   /* 2x — standard padding */
--space-3: 24px;   /* 3x */
--space-4: 32px;   /* 4x — section gap */
--space-6: 48px;   /* 6x — large gap */
--space-8: 64px;   /* 8x — section break */
--space-10: 80px;  /* 10x */
```

**Breakpoints:**
| Name | px | Columns | Margin |
|---|---|---|---|
| `sm` | 320 | 4 | 0 |
| `md` | 672 | 8 | 16px |
| `lg` | 1056 | 16 | 16px |
| `xl` | 1312 | 16 | 16px |
| `max` | 1584 | 16 | 24px |

**Grid classes:** `.ds-grid`, `.ds-row`, `.ds-col-1` through `.ds-col-16`.

---

## Component Classes (`design-system.css`)

Link once, use everywhere:
```html
<link rel="stylesheet" href="path/to/build/design-system.css">
```

### Buttons
```html
<button class="ds-btn ds-btn--primary">Primary</button>
<button class="ds-btn ds-btn--secondary">Secondary</button>
<button class="ds-btn ds-btn--danger">Danger</button>
<button class="ds-btn ds-btn--ghost">Ghost</button>
<button class="ds-btn ds-btn--primary" disabled>Disabled</button>
```

### Cards & Tiles
```html
<div class="ds-card">Standard card — layer-01 background</div>
<div class="ds-tile">Clickable tile variant</div>
<div class="ds-card ds-card--flat">No border/shadow variant</div>
```

### Tags & Badges
```html
<span class="ds-tag ds-tag--info">Info</span>
<span class="ds-tag ds-tag--success">Success</span>
<span class="ds-tag ds-tag--warning">Warning</span>
<span class="ds-tag ds-tag--error">Error</span>
<span class="ds-badge">12</span>
```

### Notifications
```html
<div class="ds-notification ds-notification--info">Info message</div>
<div class="ds-notification ds-notification--success">Success message</div>
<div class="ds-notification ds-notification--warning">Warning message</div>
<div class="ds-notification ds-notification--error">Error message</div>
```

### Forms
```html
<div class="ds-form-group">
  <label class="ds-label">Field label</label>
  <input class="ds-input" type="text" placeholder="Placeholder">
  <span class="ds-helper-text">Helper or error text</span>
</div>
```

### Data Table
```html
<table class="ds-table">...</table>
<table class="ds-table ds-table--zebra">...</table>
```

### Navigation Shell
```html
<header class="ds-header">
  <span class="ds-header__name">App Name</span>
  <nav class="ds-header__nav">...</nav>
</header>
<nav class="ds-sidenav">...</nav>
<main class="ds-content">...</main>
```

### Progress
```html
<div class="ds-progress">
  <div class="ds-progress__bar" style="--progress: 65%"></div>
</div>
```

### Movement Domain
```html
<span class="ds-hold ds-hold--start">Start</span>
<span class="ds-hold ds-hold--hand">Hand</span>
<span class="ds-hold ds-hold--foot">Foot</span>
<span class="ds-hold ds-hold--finish">Finish</span>
```

---

## Light/Dark Theme Toggle

Always include a theme toggle in interactive pages. Minimal implementation:

```html
<button class="ds-btn ds-btn--ghost ds-theme-toggle" id="theme-toggle"
  aria-label="Toggle color theme">
  <span class="ds-theme-toggle__icon">◑</span>
</button>

<script>
  (function() {
    const root = document.documentElement;
    const btn = document.getElementById('theme-toggle');
    const stored = localStorage.getItem('ds-theme');
    if (stored) root.dataset.theme = stored;
    btn?.addEventListener('click', () => {
      const next = root.dataset.theme === 'light' ? 'dark' : 'light';
      root.dataset.theme = next;
      localStorage.setItem('ds-theme', next);
    });
  })();
</script>
```

Persist the preference in `localStorage` so it survives page reloads.

---

## Platform: Unity C#

Use `build/ColorPalette.cs`. Copy it into `Assets/Scripts/Utility/`.

```csharp
using Utility;

// Dark theme (default)
renderer.material.color = ColorPalette.Information1;
text.color = ColorPalette.PrimaryText;

// Light theme
renderer.material.color = ColorPaletteLight.PrimaryText;
```

Rules:
- Use `ColorPalette` (dark) as the default scene theme
- Use `ColorPaletteLight` for light/bright scene contexts
- Never hardcode hex or RGB values — always use the static class
- Movement colors (`Start`, `Hand`, `Foot`, `Finish`) are shared between both classes

---

## Platform: Python / Seaborn / Matplotlib

Use `build/seaborn_palette.py`. Copy or import it.

```python
from seaborn_palette import (
    PALETTE_DARK, PALETTE_LIGHT,
    CATEGORICAL, STATUS_COLORS, MOVEMENT_COLORS,
    make_sequential_cmap
)
import seaborn as sns
import matplotlib.pyplot as plt

# Set global seaborn palette
sns.set_palette(CATEGORICAL)

# Status-colored bar chart
colors = [STATUS_COLORS['success'], STATUS_COLORS['warning'], STATUS_COLORS['error']]
plt.bar(labels, values, color=colors)

# Sequential colormap (dark theme)
cmap = make_sequential_cmap(dark=True)
plt.imshow(data, cmap=cmap)

# Light theme variant
sns.set_palette(list(PALETTE_LIGHT.values()))
```

Rules:
- Prefer `CATEGORICAL` for categorical data (preserves semantic meaning)
- Use `STATUS_COLORS` for status/severity data
- Use `MOVEMENT_COLORS` for movement/sequence data
- `make_sequential_cmap(dark=True)` for heatmaps in dark-background figures
- Set figure background to `PALETTE_DARK['bg']` or `PALETTE_LIGHT['bg']` for consistent theming

---

## Responsive

Always include both CSS and JS:
```html
<link rel="stylesheet" href="path/to/build/design-system.css">
<script src="path/to/build/design-system.js"></script>
```

`design-system.js` automatically handles: theme toggle, hamburger nav collapse, sidenav off-canvas drawer, and overlay backdrop. No configuration required — just add the right elements.

**Breakpoints:**
| Name | Width | Grid columns |
|---|---|---|
| `sm` | ≤ 672px | 4 |
| `md` | ≤ 1056px | 8 |
| `lg` | > 1056px | 16 |

**Responsive column overrides:**
```html
<!-- Stack full-width on mobile, half on tablet -->
<div class="ds-col-8 ds-col-sm-full ds-col-md-half">...</div>
```

**Show/hide utilities:**
```html
<span class="ds-hide-sm">Hidden on mobile</span>
<span class="ds-show-sm">Mobile only</span>
<span class="ds-hide-md">Hidden on tablet/mobile</span>
```

**Hamburger nav** — add `.ds-hamburger` button + `.ds-header__nav` nav inside your header. The JS wires them automatically:
```html
<button class="ds-hamburger" aria-label="Open navigation">
  <span class="ds-hamburger__bar"></span>
  <span class="ds-hamburger__bar"></span>
  <span class="ds-hamburger__bar"></span>
</button>
<nav class="ds-header__nav">...</nav>
```

**Sidenav drawer** — add `data-ds-nav-toggle` to any trigger button. The sidenav becomes off-canvas at ≤ 1056px:
```html
<button data-ds-nav-toggle aria-label="Open sidebar">☰</button>
<nav class="ds-sidenav">...</nav>
```

**Table overflow** — wrap tables in `.ds-table-wrap` for horizontal scroll on narrow viewports:
```html
<div class="ds-table-wrap">
  <table class="ds-table">...</table>
</div>
```

---

## Layering & Depth Rules

Follow Carbon's layering model — always maintain visual depth hierarchy:

**Dark theme:** Each layer is one value step lighter
- Page: `--color-bg` (#121212)
- Cards/Panels: `--color-layer-01` (#1e1e1e)
- Nested elements: `--color-layer-02` (#262626)
- Deeply nested: `--color-layer-03` (#333333)

**Light theme:** Layers alternate White / Gray-10
- Page: `--color-bg` (#f4f4f4)
- Cards/Panels: `--color-layer-01` (#ffffff)
- Nested elements: `--color-layer-02` (#f4f4f4)
- Deeply nested: `--color-layer-03` (#e8e8e8)

Never place a darker layer on top of a lighter layer (except intentional high-contrast moments).

---

## Interaction States

| State | Rule |
|---|---|
| Hover | Half-step lighter/darker; `--color-interactive-hover` for interactive elements |
| Active | Two full steps from enabled value; `--color-interactive-active` |
| Selected | One full step; add subtle left border in `--color-interactive` |
| Focus | 2px `--color-interactive` outline, 1px `--color-bg` inset gap |
| Disabled | All disabled elements use gray family only; no semantic color |

---

## Accessibility Rules

- Minimum 4.5:1 contrast for body text (< 24px)
- Minimum 3:1 contrast for large text (≥ 24px) and UI components
- Never rely on color alone — always pair with icons, labels, or patterns
- All interactive elements must have visible focus styles
- Movement colors must have text labels or icon supplements for colorblind users

---

## What Not To Do

- Do not use pure black (#000) or pure white (#fff) — always use the token values
- Do not hardcode colors from `colors.json` — reference tokens in CSS, class names in HTML
- Do not create new semantic colors — extend by adding to `colors.json` and regenerating
- Do not use the interactive cyan on dark backgrounds as body text — it is an action color
- Do not use movement colors for general UI status — they are domain-specific only
