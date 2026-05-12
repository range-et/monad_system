# Monad → draw.io exporter

Styling for [draw.io](https://draw.io) diagrams using the Monad design system,
designed to interoperate with the [drawio-amp](https://github.com/range-et/drawio-amp)
Amp plugin.

## Files

| File | Purpose |
|---|---|
| `monad-drawio-styles.json`   | `{ dark, light }` → token → drawio style string. Look-up table for the agent when assembling diagram XML. |
| `monad-drawio-stylesheet.xml`| `<mxStylesheet>` snippet (dark theme). Embed inside `<mxfile>` or paste via Extras → Edit Diagram. |
| `monad-drawio-example.drawio`| Self-contained mxGraphModel showcasing every Monad style. Conforms to drawio-amp validation. |

## Usage with the drawio-amp plugin

The `drawio_create` tool accepts a raw `<mxGraphModel>` payload. To style cells
with Monad tokens, look up the token in `monad-drawio-styles.json` and use the
value as the cell's `style` attribute:

```python
import json
styles = json.load(open("monad-drawio-styles.json"))["dark"]
cell_style = styles["monad.layer-02"]
```

## Token reference

Surface containers:
  monad.surface, monad.layer-01, monad.layer-02, monad.layer-03

Signal-bearing nodes:
  monad.interactive, monad.info, monad.success, monad.warning, monad.error,
  monad.highlight, monad.disabled

Text-only labels:
  monad.text-primary, monad.text-secondary, monad.text-disabled

Edges:
  monad.edge, monad.edge-subtle, monad.edge-interactive, monad.edge-dashed

Movement (domain-specific — never repurpose for UI status):
  monad.move-start, monad.move-hand, monad.move-foot, monad.move-finish

## Design rules enforced

- `rounded=0`   — no border-radius
- `shadow=0`    — no decorative shadows
- `gradient=0`  — no gradients
- `strokeWidth=1`
- `edgeStyle=orthogonalEdgeStyle` for clean routing
