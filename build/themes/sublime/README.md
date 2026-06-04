# Monad System — Sublime Text

Color schemes **and** UI theme generated from `colors.json`.

| File | What it skins |
|---|---|
| `Monad Dark.sublime-color-scheme`  | Editor canvas, gutter, syntax (dark)  |
| `Monad Light.sublime-color-scheme` | Editor canvas, gutter, syntax (light) |
| `Monad.sublime-theme`              | Sidebar, tabs, status bar (dark UI)   |
| `Monad Light.sublime-theme`        | Sidebar, tabs, status bar (light UI)  |
| `textures/*.png`                   | Tiled patterns layered on the sidebar |

> **Color scheme** ≠ **Theme.** Sublime separates editor colors from window chrome.
> You set them independently. Both ship here so the editor and the surrounding UI
> stay coherent.

---

## Install

Copy this whole folder into Sublime's `Packages/` directory as a folder named
`Monad`:

```
macOS    ~/Library/Application Support/Sublime Text/Packages/Monad/
Linux    ~/.config/sublime-text/Packages/Monad/
Windows  %APPDATA%\Sublime Text\Packages\Monad\
```

The fastest way:

```
Sublime Text → Preferences → Browse Packages…
```

Drop the `Monad` folder in there. Sublime hot-reloads — no restart needed.

---

## Activate

**Color scheme** (editor):

```
Preferences → Color Scheme → Monad → Monad Dark   (or Monad Light)
```

**Theme** (UI chrome):

```
Preferences → Theme → Monad → Monad.sublime-theme   (or Monad Light)
```

Or edit `Preferences.sublime-settings` directly:

```json
{
    "color_scheme": "Packages/Monad/Monad Dark.sublime-color-scheme",
    "theme":        "Monad.sublime-theme"
}
```

---

## Textures

Sublime UI themes can layer tiled PNG textures onto any panel via
`layer{0..3}.texture`. The default sidebar in this theme uses `dot.png` at
~8 % opacity tinted with `text_disabled` — a quiet stipple that breaks up
flat surfaces without competing with code.

To swap textures, edit `Monad.sublime-theme` and change:

```json
"layer1.texture": "Monad/textures/dot.png"
```

to any of the available textures:

```
textures/dot.png
textures/hatch-v.png
textures/hatch-h.png
textures/hatch-x.png
textures/hatch-fwd.png
textures/hatch-bwd.png
```

Or remove the `layer1.*` block entirely for a flat sidebar.

---

## Font

**Sublime themes cannot set the font.** Font face and size live in the
user's `Preferences.sublime-settings`:

```
Sublime Text → Preferences → Settings
```

Add to the **right-hand pane** (user overrides):

```json
{
    "font_face": "JetBrains Mono",
    "font_size": 13,
    "line_padding_top":    2,
    "line_padding_bottom": 2
}
```

Pick any monospace face you have installed. The Monad System uses a mono
for code and data; matching it here keeps the rendered output consistent
with the rest of the system.

---

## Customising syntax highlighting

Sublime maps **TextMate scopes** → colors. To change which color a token
type gets:

1. Put your caret on the token you want to recolor.
2. Run `Tools → Developer → Show Scope Name`
   (macOS `Ctrl+Shift+P`, Win/Linux `Ctrl+Alt+Shift+P`).
3. A popup shows the full scope stack — e.g. `source.python meta.function.python
   entity.name.function.python`. Copy the most specific selector you want
   to target.
4. Create `Packages/User/Monad Dark.sublime-color-scheme` (same filename,
   under `User/`) — Sublime auto-merges your overrides on top of ours:

   ```json
   {
       "rules": [
           {
               "name":       "Python function name — magenta",
               "scope":      "entity.name.function.python",
               "foreground": "#FF00AA",
               "font_style": "bold"
           }
       ]
   }
   ```

Editing the generated `Packages/Monad/Monad Dark.sublime-color-scheme`
directly works too, but your edits get clobbered on the next `make`.
The `User/` override file is the safe place.

### Adding entirely new tokens

The same workflow works for languages we don't cover yet — just add more
entries to `rules`. Sublime live-reloads color schemes; you'll see the
change as soon as you save.

---

## Rebuild from source

This package is generated. Edit `colors.json` and rebuild:

```bash
make
```

Outputs land in `build/themes/sublime/` — copy them back into `Packages/Monad/`.
