# Monad System

> **Form follows Function.** Every color earns its place.

A dark and light theme pair derived from the **Monad System** — a precision
design language built on a single `colors.json` source of truth. Every color
in this theme is generated programmatically; nothing is hand-tweaked.

---

## Variants

| Theme | Type | Background | Foreground |
|---|---|---|---|
| **Monad Dark** | Dark | <img src="https://placehold.co/14x14/121212/121212.png" width="14" height="14" alt="Background" title="Background #121212"> `#121212` | <img src="https://placehold.co/14x14/E0E0E0/E0E0E0.png" width="14" height="14" alt="Text" title="Text #E0E0E0"> `#E0E0E0` |
| **Monad Light** | Light | <img src="https://placehold.co/14x14/f4f4f4/f4f4f4.png" width="14" height="14" alt="Background" title="Background #f4f4f4"> `#f4f4f4` | <img src="https://placehold.co/14x14/161616/161616.png" width="14" height="14" alt="Text" title="Text #161616"> `#161616` |

---

## Dark Palette

| Role | Color |
|---|---|
| Background | <img src="https://placehold.co/14x14/121212/121212.png" width="14" height="14" alt="bg" title="bg #121212"> `#121212` |
| Layer 01 | <img src="https://placehold.co/14x14/242424/242424.png" width="14" height="14" alt="layer01" title="layer01 #242424"> `#242424` |
| Layer 02 | <img src="https://placehold.co/14x14/2C2C2C/2C2C2C.png" width="14" height="14" alt="layer02" title="layer02 #2C2C2C"> `#2C2C2C` |
| Layer 03 | <img src="https://placehold.co/14x14/333333/333333.png" width="14" height="14" alt="layer03" title="layer03 #333333"> `#333333` |
| Primary Text | <img src="https://placehold.co/14x14/E0E0E0/E0E0E0.png" width="14" height="14" alt="text_primary" title="text_primary #E0E0E0"> `#E0E0E0` |
| Secondary Text | <img src="https://placehold.co/14x14/B0B0B0/B0B0B0.png" width="14" height="14" alt="text_secondary" title="text_secondary #B0B0B0"> `#B0B0B0` |
| Disabled Text | <img src="https://placehold.co/14x14/757575/757575.png" width="14" height="14" alt="text_disabled" title="text_disabled #757575"> `#757575` |
| Interactive (blue) | <img src="https://placehold.co/14x14/03A9F4/03A9F4.png" width="14" height="14" alt="interactive" title="interactive #03A9F4"> `#03A9F4` |
| Info (cyan) | <img src="https://placehold.co/14x14/00BCD4/00BCD4.png" width="14" height="14" alt="info" title="info #00BCD4"> `#00BCD4` |
| Success (green) | <img src="https://placehold.co/14x14/8BC34A/8BC34A.png" width="14" height="14" alt="success" title="success #8BC34A"> `#8BC34A` |
| Warning (amber) | <img src="https://placehold.co/14x14/FFC107/FFC107.png" width="14" height="14" alt="warning" title="warning #FFC107"> `#FFC107` |
| Error (red) | <img src="https://placehold.co/14x14/F44336/F44336.png" width="14" height="14" alt="error" title="error #F44336"> `#F44336` |
| Highlight (yellow) | <img src="https://placehold.co/14x14/FFEB3B/FFEB3B.png" width="14" height="14" alt="highlight" title="highlight #FFEB3B"> `#FFEB3B` |

### Domain Colors (Movement)

| Role | Color |
|---|---|
| Start | <img src="https://placehold.co/14x14/4CAF50/4CAF50.png" width="14" height="14" alt="start" title="start #4CAF50"> `#4CAF50` |
| Hand | <img src="https://placehold.co/14x14/03A9F4/03A9F4.png" width="14" height="14" alt="hand" title="hand #03A9F4"> `#03A9F4` |
| Foot | <img src="https://placehold.co/14x14/FFEB3B/FFEB3B.png" width="14" height="14" alt="foot" title="foot #FFEB3B"> `#FFEB3B` |
| Finish | <img src="https://placehold.co/14x14/9C27B0/9C27B0.png" width="14" height="14" alt="finish" title="finish #9C27B0"> `#9C27B0` |

---

## Design Principles

- **No border-radius** — orthogonal, structural, undecorated
- **No box-shadow depth** — layering via 1px borders and background steps
- **No gradients** — flat fills only; color is information, not texture
- **Haptic transitions** — 80ms linear; motion is predictable, not expressive
- **Mono for data** — numeric values, labels, and overlines use JetBrains Mono

---

## Installation

Search **"Monad System"** in the VS Code Extension Marketplace, or install via CLI:

```bash
code --install-extension monad-system.monad-system-theme
```

Then open the theme picker:

```
Cmd+K  Cmd+T  →  Monad Dark  /  Monad Light
```

---

## Source

This theme is **generated** from `colors.json` — the single source of truth
for the entire Monad System (CSS, C#, Python/seaborn, Ghostty, and VS Code).

To regenerate after editing colors:

```bash
make install
```
