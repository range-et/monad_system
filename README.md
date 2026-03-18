# Default Colors — Design System

A personal, multi-platform design system built on a single source of truth: `colors.json`. Fuses your color palette with **Carbon Design System**'s physical language (8px grid, IBM Plex typography, token layering model) into a portable, cross-platform toolkit.

**Platforms covered:** HTML/CSS/JS · Unity C# · Python / Matplotlib / Seaborn

---

![Color Palette](assets/default_colors_main.png)

---

## What's Included

| File | Platform | Description |
|---|---|---|
| `build/design-system.css` | HTML/CSS/JS | Bootstrap-style component library with light + dark themes |
| `build/ColorPalette.css` | HTML/CSS | Raw CSS custom property tokens (dark) |
| `build/ColorPalette.cs` | Unity C# | Static color class — dark theme |
| `build/ColorPaletteLight.cs` | Unity C# | Static color class — light theme |
| `build/seaborn_palette.py` | Python | matplotlib/seaborn palette helpers + colormaps |
| `.cursor/skills/design-system/SKILL.md` | Cursor / AI | AI skill for building UIs with this system |

---

## Samples

| Sample | Description |
|---|---|
| [`samples/components.html`](samples/components.html) | Full component showcase — palette, typography, buttons, cards, tags, notifications, forms, tables, progress |
| [`samples/dashboard.html`](samples/dashboard.html) | General-purpose app dashboard — header, sidenav, stat cards, activity feed, data table, status panels |

Both samples include a light/dark theme toggle (top-right corner). Open directly in a browser — no build step needed.

---

## Color Palette

### General UI Colors

| Category | Name | Hex | RGB |
|---|---|---|---|
| **General UI** | Primary Background | `#121212` | (18, 18, 18) |
| | Primary Text | `#E0E0E0` | (224, 224, 224) |
| | Secondary Text | `#B0B0B0` | (176, 176, 176) |
| **Information** | Information 1 (Cyan) | `#00BCD4` | (0, 188, 212) |
| | Information 2 (Blue) | `#03A9F4` | (3, 169, 244) |
| | Information 3 (Green) | `#8BC34A` | (139, 195, 74) |
| **Warnings** | Warning 1 (Amber) | `#FFC107` | (255, 193, 7) |
| | Alert 1 (Red) | `#F44336` | (244, 67, 54) |
| **Highlights** | Highlight (Yellow) | `#FFEB3B` | (255, 235, 59) |
| | Disabled (Gray) | `#757575` | (117, 117, 117) |
| **Movement** | Start Holds (Green) | `#4CAF50` | (76, 175, 80) |
| | Hand Holds (Blue) | `#03A9F4` | (3, 169, 244) |
| | Foot Holds (Yellow) | `#FFEB3B` | (255, 235, 59) |
| | Finish Holds (Purple) | `#9C27B0` | (156, 39, 176) |

---

## Light & Dark Theming

All build artifacts include both themes. The dark theme (your original palette) is the default. The light theme derives from Carbon's White-theme approach.

| Token | Dark | Light |
|---|---|---|
| `--color-bg` | `#121212` | `#f4f4f4` |
| `--color-layer-01` | `#1e1e1e` | `#ffffff` |
| `--color-layer-02` | `#262626` | `#f4f4f4` |
| `--color-layer-03` | `#333333` | `#e8e8e8` |
| `--color-text-primary` | `#E0E0E0` | `#161616` |
| `--color-text-secondary` | `#B0B0B0` | `#525252` |
| `--color-border` | `#3d3d3d` | `#c6c6c6` |

Accent and semantic colors (`--color-interactive`, status colors, movement colors) are shared across both themes.

---

## HTML / CSS / JS

### Using the component library

Link a single CSS file — both themes included automatically:

```html
<link rel="stylesheet" href="build/design-system.css">
```

Set the initial theme via `data-theme` on `<html>`:

```html
<html data-theme="light">   <!-- light theme -->
<html>                      <!-- dark theme (default) -->
```

Add a theme toggle anywhere:

```html
<button id="theme-toggle">◑</button>

<script>
  (function () {
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

`prefers-color-scheme` media query also applied automatically as an OS-level fallback.

### Component class examples

```html
<!-- Buttons -->
<button class="ds-btn ds-btn--primary">Primary</button>
<button class="ds-btn ds-btn--secondary">Secondary</button>
<button class="ds-btn ds-btn--danger">Danger</button>
<button class="ds-btn ds-btn--ghost">Ghost</button>

<!-- Cards -->
<div class="ds-card">
  <div class="ds-card__title">Card title</div>
  <div class="ds-card__body">Content on layer-01.</div>
</div>

<!-- Status tags -->
<span class="ds-tag ds-tag--success">Operational</span>
<span class="ds-tag ds-tag--warning">Degraded</span>
<span class="ds-tag ds-tag--error">Down</span>

<!-- Notifications -->
<div class="ds-notification ds-notification--warning">
  <span class="ds-notification__icon">⚠</span>
  <div class="ds-notification__body">
    <div class="ds-notification__title">Warning title</div>
    <div class="ds-notification__msg">Warning message here.</div>
  </div>
</div>

<!-- Progress -->
<div class="ds-progress">
  <div class="ds-progress__bar" style="--progress: 65%"></div>
</div>

<!-- Movement holds (domain-specific) -->
<span class="ds-hold ds-hold--start">Start</span>
<span class="ds-hold ds-hold--hand">Hand</span>
<span class="ds-hold ds-hold--foot">Foot</span>
<span class="ds-hold ds-hold--finish">Finish</span>
```

### Typography

Three Google Fonts typefaces — loaded via `@import` inside `design-system.css`, no extra `<link>` needed:

| Role | Font | Usage |
|---|---|---|
| `--font-sans` | Inter | Body text, UI labels, headings |
| `--font-mono` | JetBrains Mono | Code, tokens, monospace labels |
| `--font-serif` | Lora | Editorial text, pull quotes, display sections |

Type scale follows Carbon's steps from 12px → 54px.

```css
font-family: var(--font-sans);   /* Inter */
font-family: var(--font-mono);   /* JetBrains Mono */
font-family: var(--font-serif);  /* Lora */
font-size: var(--type-base);     /* 16px */
font-size: var(--type-3xl);      /* 32px heading */
```

### Grid (Carbon 2x Grid)

```html
<div class="ds-grid">
  <div class="ds-col-8">Half width</div>
  <div class="ds-col-8">Half width</div>
</div>

<div class="ds-grid">
  <div class="ds-col-4">Quarter</div>
  <div class="ds-col-12">Three quarters</div>
</div>
```

---

## Unity C#

Copy the generated files to your project:

```bash
cp build/ColorPalette.cs      Assets/Scripts/Utility/
cp build/ColorPaletteLight.cs Assets/Scripts/Utility/
```

Usage:

```csharp
using Utility;

// Dark theme (default)
renderer.material.color = ColorPalette.Information1;
text.color              = ColorPalette.PrimaryText;
background.color        = ColorPalette.Background;

// Light theme
renderer.material.color = ColorPaletteLight.Background;
text.color              = ColorPaletteLight.PrimaryText;

// Movement / domain colors (same in both classes)
holdRenderer.color = ColorPalette.Start;   // #4CAF50
holdRenderer.color = ColorPalette.Hand;    // #03A9F4
holdRenderer.color = ColorPalette.Foot;    // #FFEB3B
holdRenderer.color = ColorPalette.Finish;  // #9C27B0
```

Both `ColorPalette` and `ColorPaletteLight` live in the `Utility` namespace and expose `ColorFromHex(string hexCode)` as a public helper.

---

## Python / Matplotlib / Seaborn

Copy or import the generated palette helper:

```bash
cp build/seaborn_palette.py your_project/utils/
```

```python
from utils.seaborn_palette import (
    PALETTE_DARK, PALETTE_LIGHT,
    CATEGORICAL, STATUS_COLORS, MOVEMENT_COLORS,
    make_sequential_cmap, make_diverging_cmap, make_status_cmap,
    apply_dark_theme, apply_light_theme,
)
import seaborn as sns
import matplotlib.pyplot as plt

# --- Categorical plot with design system palette ---
sns.set_palette(CATEGORICAL)
sns.barplot(data=df, x="category", y="value")

# --- Status-colored chart ---
colors = [STATUS_COLORS['success'], STATUS_COLORS['warning'], STATUS_COLORS['error']]
plt.bar(labels, values, color=colors)

# --- Sequential heatmap (dark theme) ---
cmap = make_sequential_cmap(dark=True)
sns.heatmap(matrix, cmap=cmap)

# --- Apply dark theme styling to a figure ---
fig, ax = plt.subplots()
apply_dark_theme(fig, ax)
ax.plot(x, y, color=PALETTE_DARK['interactive'])

# --- Diverging colormap (error → neutral → success) ---
cmap_div = make_diverging_cmap()
sns.heatmap(corr_matrix, cmap=cmap_div, center=0)

# --- Movement colors for sequence data ---
for i, phase in enumerate(['start', 'hand', 'foot', 'finish']):
    ax.scatter(x[i], y[i], color=MOVEMENT_COLORS[phase], s=100)
```

---

## Cursor / AI Skill

The `.cursor/skills/design-system/SKILL.md` skill activates automatically when you ask Cursor or Gemini to build UI elements. It teaches the AI to:

- Use the correct CSS tokens (never hardcode hex values)
- Follow Carbon's 2x grid (8px base unit) and IBM Plex type scale
- Use `.ds-*` component classes from `design-system.css`
- Always implement both light and dark themes
- Include the JS theme toggle with `localStorage` persistence
- Apply the correct conventions per platform (HTML, Unity C#, Python viz)
- Use movement colors only for domain-specific contexts

The skill references the existing `frontend-design` skill for aesthetic direction, but overrides color, spacing, and typography with this system.

---

## Using in Other Projects

Clone this repo as a submodule or standalone dependency:

```bash
# As a standalone clone
git clone https://github.com/you/default_colors design-system

# Link the CSS in HTML
<link rel="stylesheet" href="./design-system/build/design-system.css">

# Copy Unity files
cp design-system/build/ColorPalette.cs      Assets/Scripts/Utility/
cp design-system/build/ColorPaletteLight.cs Assets/Scripts/Utility/

# Copy Python helpers
cp design-system/build/seaborn_palette.py   src/utils/

# As a git submodule (recommended for keeping in sync)
git submodule add https://github.com/you/default_colors design-system
git submodule update --init
```

The Cursor skill also works cross-project: copy `.cursor/skills/design-system/` to any project's `.cursor/skills/` folder.

---

## Regenerating Build Artifacts

After editing `colors.json`, regenerate all artifacts:

```bash
cd default_colors
python src/compile_color.py --json_path colors.json --output_path build/
```

This will regenerate all five files in `build/` plus the color palette preview image.

### Requirements

```bash
pip install pillow
```

---

## Design Language Principles

This system adopts Carbon Design System's physical language:

- **Grid**: 8px mini unit base, 16px standard padding, Carbon breakpoints (320 / 672 / 1056 / 1312 / 1584px)
- **Typography**: IBM Plex Sans / Mono / Serif; weights 300 / 400 / 600 only
- **Layering**: Each depth level is one step lighter (dark) or alternates white/gray-10 (light); depth is always visible
- **Tokens**: Role-based — `--color-interactive`, `--color-support-warning`, `--color-text-primary`. Never hardcode hex
- **Interaction states**: hover (half-step), active (two-step), focus (2px interactive ring), disabled (gray family only)
- **Accessibility**: 4.5:1 contrast for body text, 3:1 for large text/UI, always pair color with labels or icons

### Integration Guidelines

1. **Separation of concerns**: UI status colors and movement domain colors must not be mixed
2. **Contrast**: Always verify text against its background using the token system
3. **Colorblind accessibility**: Supplement movement colors with text labels and shapes
4. **Single source**: All changes go to `colors.json` first, then regenerate — never patch build files directly
