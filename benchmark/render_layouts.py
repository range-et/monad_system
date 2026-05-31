"""Render benchmark layouts to PNG and capture focal-target bboxes.

Walks `benchmark/layouts/<system>/<form-factor>/<scenario>.html`, screenshots
each at the form-factor's canonical viewport, and records the bbox of the
`#focal-target` element in `benchmark/focal_targets.json` (merged, not
overwritten — re-running for one system leaves other systems intact).

Usage:
    python benchmark/render_layouts.py                    # all systems
    python benchmark/render_layouts.py --system nasa      # one system
    python benchmark/render_layouts.py --system monad nasa
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
LAYOUTS_ROOT = ROOT / "layouts"
RENDERS_ROOT = ROOT / "renders"
TARGETS_FILE = ROOT / "focal_targets.json"

FORM_FACTORS = [
    ("ski-AR",       1920, 1080),
    ("climb-AR",     1920, 1080),
    ("device-only",  390,  844),
]
SCENARIOS = ["calm", "alert", "warning"]

INTENT = {
    ("ski-AR",      "calm"):    "primary speed tile",
    ("ski-AR",      "alert"):   "HR-zone amber flag",
    ("ski-AR",      "warning"): "warning callout headline",
    ("climb-AR",    "calm"):    "primary cadence tile (HR at-a-glance)",
    ("climb-AR",    "alert"):   "HR-zone amber flag",
    ("climb-AR",    "warning"): "warning callout headline",
    ("device-only", "calm"):    "primary speed tile",
    ("device-only", "alert"):   "HR-zone amber flag",
    ("device-only", "warning"): "warning callout headline",
}


def discover_systems() -> list[str]:
    """Every subdirectory of layouts/ is a system."""
    if not LAYOUTS_ROOT.exists():
        return []
    return sorted(
        d.name for d in LAYOUTS_ROOT.iterdir()
        if d.is_dir() and not d.name.startswith(".") and not d.name.startswith("_")
    )


def load_existing_targets() -> dict:
    if TARGETS_FILE.exists():
        try:
            return json.loads(TARGETS_FILE.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def render_system(system: str, browser) -> dict:
    """Render all 9 layouts for one system; return its bbox dict."""
    print(f"\n=== {system} ===")
    out: dict = {ff: {} for ff, _, _ in FORM_FACTORS}

    for form_factor, vw, vh in FORM_FACTORS:
        render_dir = RENDERS_ROOT / system / form_factor
        render_dir.mkdir(parents=True, exist_ok=True)

        context = browser.new_context(
            viewport={"width": vw, "height": vh},
            device_scale_factor=1,
        )
        page = context.new_page()

        for scenario in SCENARIOS:
            html_path = LAYOUTS_ROOT / system / form_factor / f"{scenario}.html"
            if not html_path.exists():
                print(f"  SKIP {form_factor}/{scenario} (no {html_path.name})")
                continue

            url = html_path.resolve().as_uri()
            page.goto(url, wait_until="networkidle")
            page.wait_for_function(
                "Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)"
            )

            locator = page.locator("#focal-target")
            locator.wait_for(state="visible")
            box = locator.bounding_box()
            if box is None:
                raise RuntimeError(f"#focal-target not visible in {html_path}")

            out_png = render_dir / f"{scenario}.png"
            page.screenshot(path=str(out_png), full_page=False)

            out[form_factor][scenario] = {
                "bbox": [round(box["x"], 2), round(box["y"], 2),
                         round(box["width"], 2), round(box["height"], 2)],
                "intent": INTENT[(form_factor, scenario)],
            }
            print(
                f"  {form_factor}/{scenario}.png  "
                f"bbox=({box['x']:.0f},{box['y']:.0f},"
                f"{box['width']:.0f},{box['height']:.0f})"
            )

        context.close()

    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--system", nargs="*", default=None,
                    help="System names to render (default: all under layouts/)")
    args = ap.parse_args()

    available = discover_systems()
    if args.system:
        systems = args.system
        missing = [s for s in systems if s not in available]
        if missing:
            raise SystemExit(f"Unknown system(s): {missing}. Available: {available}")
    else:
        systems = available
        if not systems:
            raise SystemExit(f"No systems found under {LAYOUTS_ROOT}")

    print(f"Rendering systems: {systems}")

    existing = load_existing_targets()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            for system in systems:
                existing[system] = render_system(system, browser)
        finally:
            browser.close()

    TARGETS_FILE.write_text(json.dumps(existing, indent=2) + "\n")
    print(f"\nWrote {TARGETS_FILE}")


if __name__ == "__main__":
    main()
