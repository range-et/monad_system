"""
draw.io exporter for the Monad System.

Designed to interoperate with the `drawio-amp` Amp plugin
(https://github.com/range-et/drawio-amp), whose `drawio_create` tool consumes
raw `<mxGraphModel>` XML.

This module produces three artifacts:

  - monad-drawio-styles.json
        { "dark": { token: style_string }, "light": { ... } }
        Look-up table of Monad-styled draw.io style strings, keyed by semantic
        token name. Use the value as the `style="..."` attribute on `<mxCell>`.

  - monad-drawio-stylesheet.xml
        `<mxStylesheet>` snippet that can be embedded inside an `<mxfile>` to
        register named styles with the draw.io editor. Comment-free.

  - monad-drawio-example.drawio
        A self-contained `<mxGraphModel>` document that exercises every
        Monad-styled style and conforms to the drawio-amp plugin's validation
        rules (no XML comments, edges include
        `<mxGeometry relative="1" as="geometry" />`).

Style strings follow the Monad design rules:
  - rounded=0   (no border-radius)
  - shadow=0    (no decorative shadows)
  - gradient=0  (no gradients)
  - strokeWidth=1
"""

import json


# ── Style assembly ──────────────────────────────────────────────────────────

# Common base for every node style. Encodes Monad's "no rounded corners,
# no shadows, no gradients, 1px stroke" rules.
_NODE_BASE = "rounded=0;whiteSpace=wrap;html=1;shadow=0;gradient=0;strokeWidth=1"

# Common base for every edge style. Orthogonal routing without rounded joins.
_EDGE_BASE = (
    "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;"
    "jettySize=auto;html=1;strokeWidth=1;endArrow=classic;endFill=1"
)

# Text-only label style (no fill, no stroke).
_TEXT_BASE = "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle"


def _node(fill, stroke, font, extra=""):
    parts = [
        _NODE_BASE,
        f"fillColor={fill}",
        f"strokeColor={stroke}",
        f"fontColor={font}",
    ]
    if extra:
        parts.append(extra)
    return ";".join(parts) + ";"


def _edge(stroke, extra=""):
    parts = [_EDGE_BASE, f"strokeColor={stroke}"]
    if extra:
        parts.append(extra)
    return ";".join(parts) + ";"


def _text(font, extra=""):
    parts = [_TEXT_BASE, f"fontColor={font}"]
    if extra:
        parts.append(extra)
    return ";".join(parts) + ";"


def _build_palette(
    background,
    layer01,
    layer02,
    layer03,
    text_primary,
    text_secondary,
    text_disabled,
    border,
    border_subtle,
    interactive,
    support_info,
    support_success,
    support_warning,
    support_error,
    highlight,
    disabled,
    on_strong,
    move_start,
    move_hand,
    move_foot,
    move_finish,
):
    """Return an ordered dict of Monad token → drawio style string."""
    return {
        # Surface containers
        "monad.surface":     _node(background, border, text_primary),
        "monad.layer-01":    _node(layer01, border_subtle, text_primary),
        "monad.layer-02":    _node(layer02, border_subtle, text_primary),
        "monad.layer-03":    _node(layer03, border_subtle, text_primary),

        # Signal-bearing nodes
        "monad.interactive": _node(interactive, interactive, on_strong),
        "monad.info":        _node(support_info, support_info, on_strong),
        "monad.success":     _node(support_success, support_success, on_strong),
        "monad.warning":     _node(support_warning, support_warning, on_strong),
        "monad.error":       _node(support_error, support_error, on_strong),
        "monad.highlight":   _node(highlight, highlight, text_primary),
        "monad.disabled":    _node(disabled, border_subtle, text_disabled),

        # Text-only labels
        "monad.text-primary":   _text(text_primary),
        "monad.text-secondary": _text(text_secondary),
        "monad.text-disabled":  _text(text_disabled),

        # Edges
        "monad.edge":             _edge(border),
        "monad.edge-subtle":      _edge(border_subtle),
        "monad.edge-interactive": _edge(interactive),
        "monad.edge-dashed":      _edge(border, extra="dashed=1"),

        # Movement (domain-specific — never repurpose for UI status)
        "monad.move-start":  _node(move_start, move_start, on_strong),
        "monad.move-hand":   _node(move_hand, move_hand, on_strong),
        "monad.move-foot":   _node(move_foot, move_foot, text_primary),
        "monad.move-finish": _node(move_finish, move_finish, on_strong),
    }


# ── Public artifacts ────────────────────────────────────────────────────────

def create_drawio_styles_json(
    bg_dark, layer01_dark, layer02_dark, layer03_dark,
    text_primary_dark, text_secondary_dark, text_disabled_dark,
    border_dark, border_subtle_dark,
    bg_light, layer01_light, layer02_light, layer03_light,
    text_primary_light, text_secondary_light, text_disabled_light,
    border_light, border_subtle_light,
    interactive, support_info, support_success, support_warning, support_error,
    highlight, disabled,
    move_start, move_hand, move_foot, move_finish,
):
    """Return a JSON string mapping {dark,light} → token → style string."""
    dark = _build_palette(
        background=bg_dark,
        layer01=layer01_dark, layer02=layer02_dark, layer03=layer03_dark,
        text_primary=text_primary_dark,
        text_secondary=text_secondary_dark,
        text_disabled=text_disabled_dark,
        border=border_dark, border_subtle=border_subtle_dark,
        interactive=interactive,
        support_info=support_info, support_success=support_success,
        support_warning=support_warning, support_error=support_error,
        highlight=highlight, disabled=disabled,
        on_strong=bg_dark,
        move_start=move_start, move_hand=move_hand,
        move_foot=move_foot, move_finish=move_finish,
    )
    light = _build_palette(
        background=bg_light,
        layer01=layer01_light, layer02=layer02_light, layer03=layer03_light,
        text_primary=text_primary_light,
        text_secondary=text_secondary_light,
        text_disabled=text_disabled_light,
        border=border_light, border_subtle=border_subtle_light,
        interactive=interactive,
        support_info=support_info, support_success=support_success,
        support_warning=support_warning, support_error=support_error,
        highlight=highlight, disabled=disabled,
        on_strong=bg_dark,
        move_start=move_start, move_hand=move_hand,
        move_foot=move_foot, move_finish=move_finish,
    )
    return json.dumps({"dark": dark, "light": light}, indent=2) + "\n"


def _style_to_xml_entries(style_string):
    """Convert 'k1=v1;k2=v2;' → '<add as="k1" value="v1"/><add as="k2" value="v2"/>'."""
    entries = []
    for pair in style_string.rstrip(";").split(";"):
        if not pair or "=" not in pair:
            continue
        k, v = pair.split("=", 1)
        entries.append(f'        <add as="{k}" value="{v}"/>')
    return "\n".join(entries)


def create_drawio_stylesheet(
    bg_dark, layer01_dark, layer02_dark, layer03_dark,
    text_primary_dark, text_secondary_dark, text_disabled_dark,
    border_dark, border_subtle_dark,
    interactive, support_info, support_success, support_warning, support_error,
    highlight, disabled,
    move_start, move_hand, move_foot, move_finish,
):
    """Return an `<mxStylesheet>` XML snippet for the dark Monad palette.

    Embed inside an `<mxfile>` document or paste into Extras → Edit Diagram →
    diagram stylesheet to register the Monad styles.
    """
    palette = _build_palette(
        background=bg_dark,
        layer01=layer01_dark, layer02=layer02_dark, layer03=layer03_dark,
        text_primary=text_primary_dark,
        text_secondary=text_secondary_dark,
        text_disabled=text_disabled_dark,
        border=border_dark, border_subtle=border_subtle_dark,
        interactive=interactive,
        support_info=support_info, support_success=support_success,
        support_warning=support_warning, support_error=support_error,
        highlight=highlight, disabled=disabled,
        on_strong=bg_dark,
        move_start=move_start, move_hand=move_hand,
        move_foot=move_foot, move_finish=move_finish,
    )

    style_blocks = []
    for name, style in palette.items():
        entries = _style_to_xml_entries(style)
        style_blocks.append(
            f'    <add as="{name}">\n{entries}\n    </add>'
        )

    return (
        '<mxStylesheet>\n'
        '  <styles>\n'
        + "\n".join(style_blocks) + "\n"
        '  </styles>\n'
        '</mxStylesheet>\n'
    )


def create_drawio_example_diagram(
    bg_dark, layer01_dark, layer02_dark, layer03_dark,
    text_primary_dark, text_secondary_dark, text_disabled_dark,
    border_dark, border_subtle_dark,
    interactive, support_info, support_success, support_warning, support_error,
    highlight, disabled,
    move_start, move_hand, move_foot, move_finish,
):
    """Return a self-contained `<mxGraphModel>` document showcasing every
    Monad-styled style. Conforms to drawio-amp plugin validation:

      - Starts with <mxGraphModel>
      - Contains zero XML comments
      - Every edge cell has <mxGeometry relative="1" as="geometry" />
      - All mxCell ids are unique
    """
    palette = _build_palette(
        background=bg_dark,
        layer01=layer01_dark, layer02=layer02_dark, layer03=layer03_dark,
        text_primary=text_primary_dark,
        text_secondary=text_secondary_dark,
        text_disabled=text_disabled_dark,
        border=border_dark, border_subtle=border_subtle_dark,
        interactive=interactive,
        support_info=support_info, support_success=support_success,
        support_warning=support_warning, support_error=support_error,
        highlight=highlight, disabled=disabled,
        on_strong=bg_dark,
        move_start=move_start, move_hand=move_hand,
        move_foot=move_foot, move_finish=move_finish,
    )

    # Lay nodes out in a 4-column grid so the example renders cleanly when
    # opened in draw.io Desktop.
    node_tokens = [k for k in palette.keys()
                   if not k.startswith("monad.edge")
                   and not k.startswith("monad.text")]

    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
    cell_id = 2
    cols = 4
    cell_w, cell_h = 160, 60
    gap_x, gap_y = 40, 40
    pad = 20

    for idx, token in enumerate(node_tokens):
        col = idx % cols
        row = idx // cols
        x = pad + col * (cell_w + gap_x)
        y = pad + row * (cell_h + gap_y)
        label = token.replace("monad.", "")
        style = palette[token]
        cells.append(
            f'<mxCell id="{cell_id}" value="{label}" style="{style}" '
            f'vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" '
            f'as="geometry"/>'
            f'</mxCell>'
        )
        cell_id += 1

    # One edge per edge style. Edges connect the first two surface nodes so
    # they have somewhere to anchor; in the example they float as labels.
    edge_y = pad + ((len(node_tokens) // cols) + 1) * (cell_h + gap_y)
    for idx, token in enumerate(["monad.edge", "monad.edge-subtle",
                                 "monad.edge-interactive", "monad.edge-dashed"]):
        x1 = pad + idx * 180
        x2 = x1 + 140
        style = palette[token]
        cells.append(
            f'<mxCell id="{cell_id}" value="{token.replace("monad.", "")}" '
            f'style="{style}" edge="1" parent="1">'
            f'<mxGeometry relative="1" as="geometry">'
            f'<mxPoint x="{x1}" y="{edge_y}" as="sourcePoint"/>'
            f'<mxPoint x="{x2}" y="{edge_y}" as="targetPoint"/>'
            f'</mxGeometry>'
            f'</mxCell>'
        )
        cell_id += 1

    indented = "\n    ".join(cells)
    return (
        '<mxGraphModel adaptiveColors="auto">\n'
        '  <root>\n'
        f'    {indented}\n'
        '  </root>\n'
        '</mxGraphModel>\n'
    )


def create_drawio_readme():
    return """# Monad → draw.io exporter

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
"""
