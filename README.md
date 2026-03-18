# Monad System

**Site:** [range-et.github.io/monad_system](https://range-et.github.io/monad_system/)

Source: `colors.json`. Build outputs go to `build/`.

## Tiers

| Tier | Scope |
|---|---|
| Strata | `--strata-*` tokens |
| Monad | `.monad-*` layout |
| Atomos | `.atomos-*` components |
| Threshold | `.threshold-*` nav / motion |

## Build

```bash
pip install -r requirements.txt
make
```

```bash
python src/compile_color.py --json_path colors.json --output_path build/
```

| Output | Target |
|---|---|
| `build/monad.css` | HTML/CSS — full system |
| `build/monad.js` | HTML/JS — theme + nav |
| `build/ColorPalette.css` | HTML/CSS — tokens only |
| `build/ColorPalette.cs` | Unity — dark |
| `build/ColorPaletteLight.cs` | Unity — light |
| `build/seaborn_palette.py` | Python / matplotlib |
| `build/themes/swiftui/MonadStrata.swift` | SwiftUI — Strata `Color` |
| `build/themes/vscode/` | VS Code / Cursor |
| `build/themes/ghostty/` | Ghostty |
| `build/themes/xcode/` | Xcode editor themes |

```bash
make serve          # localhost:8000
make dev            # build + serve + open
make clean
make install        # VS Code + Ghostty + Xcode themes
make install-vscode
make install-ghostty
make install-xcode
make package-vscode
```

## SwiftUI

Add `build/themes/swiftui/MonadStrata.swift` to the Xcode target.

```swift
Text("Title").foregroundStyle(MonadStrata.textPrimary)
Rectangle().fill(MonadStrata.layer01)
```

Adaptive colors follow system light/dark. Shared tokens (`interactive`, `info`, movement, etc.) are fixed hex. `MonadStrata.thresholdFastSeconds` is `0.08`.

## HTML

```html
<link rel="stylesheet" href="build/monad.css">
<script src="build/monad.js"></script>
```

Theme: dark default; light = `data-strata="light"`. Toggle: `data-mn-theme-toggle`.

## Unity

```csharp
ColorPalette.Background
ColorPaletteLight.Background
```

## Python

```python
from build.seaborn_palette import apply_dark_theme, CATEGORICAL
apply_dark_theme()
```

## Samples

| Path |
|---|
| `samples/components.html` |
| `samples/dashboard.html` |

## `colors.json`

- `Default_Colors` — dark ground + shared semantics
- `Light_Mode.General_UI_Colors` — light ground overrides

## Typography (CSS)

| Token | Stack |
|---|---|
| `--font-sans` | Inter |
| `--font-mono` | JetBrains Mono |
| `--font-serif` | Lora |

## Submodule / copy

```bash
git submodule add https://github.com/range-et/monad_system.git design-tokens
```

## Cursor skill

`.cursor/skills/monad-system/SKILL.md`
