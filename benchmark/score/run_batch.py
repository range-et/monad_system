"""Batch-score every render in `benchmark/renders/` with UMSI++ and DeepGaze++.

Walks the tree:

    benchmark/renders/{system}/{form_factor}/{scenario}.png

For each PNG, runs both models (loaded exactly once each) and writes:

    benchmark/scores/{system}/{form_factor}/{scenario}.heatmap.png            (UMSI++)
    benchmark/scores/{system}/{form_factor}/{scenario}.heatmap_overlay.png    (UMSI++)
    benchmark/scores/{system}/{form_factor}/{scenario}.dgiie.heatmap.png         (DeepGazeIIE)
    benchmark/scores/{system}/{form_factor}/{scenario}.dgiie.heatmap_overlay.png (DeepGazeIIE)
    benchmark/scores/{system}/{form_factor}/{scenario}.scanpath.json
    benchmark/scores/{system}/{form_factor}/{scenario}.scanpath_overlay.png

Usage:
    python -m benchmark.score.run_batch                          # all systems, all models
    python -m benchmark.score.run_batch --system monad           # one system
    python -m benchmark.score.run_batch --n-fixations 8          # longer scanpaths
    python -m benchmark.score.run_batch --skip-existing          # resume mode
    python -m benchmark.score.run_batch --models umsipp          # only UMSI++ saliency
    python -m benchmark.score.run_batch --models dgiie           # only DeepGazeIIE saliency
    python -m benchmark.score.run_batch --models deepgaze        # only DeepGaze++ scanpath
    python -m benchmark.score.run_batch --models umsipp,dgiie    # saliency-only, both models

Run from the workspace root.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RENDERS_ROOT = ROOT / "renders"
SCORES_ROOT = ROOT / "scores"


def discover_renders(system_filter: str | None = None) -> list[tuple[str, str, str, Path]]:
    """Yield (system, form_factor, scenario, image_path) for every render."""
    out: list[tuple[str, str, str, Path]] = []
    if not RENDERS_ROOT.exists():
        return out
    for system_dir in sorted(RENDERS_ROOT.iterdir()):
        if not system_dir.is_dir() or system_dir.name.startswith("."):
            continue
        if system_filter and system_dir.name != system_filter:
            continue
        for ff_dir in sorted(system_dir.iterdir()):
            if not ff_dir.is_dir() or ff_dir.name.startswith("."):
                continue
            for png in sorted(ff_dir.glob("*.png")):
                scenario = png.stem
                out.append((system_dir.name, ff_dir.name, scenario, png))
    return out


def out_paths(system: str, form_factor: str, scenario: str) -> dict[str, Path]:
    base = SCORES_ROOT / system / form_factor
    return {
        "heatmap":               base / f"{scenario}.heatmap.png",
        "heatmap_overlay":       base / f"{scenario}.heatmap_overlay.png",
        "dgiie_heatmap":         base / f"{scenario}.dgiie.heatmap.png",
        "dgiie_heatmap_overlay": base / f"{scenario}.dgiie.heatmap_overlay.png",
        "scanpath_json":         base / f"{scenario}.scanpath.json",
        "scanpath_overlay":      base / f"{scenario}.scanpath_overlay.png",
    }


# Comma-separated list of model keys. "both" kept for back-compat = all three.
_MODEL_KEYS = {"umsipp", "dgiie", "deepgaze"}


def _parse_models(spec: str) -> set[str]:
    spec = (spec or "").strip().lower()
    if spec in ("", "all", "both"):
        return set(_MODEL_KEYS)
    chosen = {tok.strip() for tok in spec.split(",") if tok.strip()}
    unknown = chosen - _MODEL_KEYS
    if unknown:
        raise SystemExit(f"Unknown model(s): {', '.join(sorted(unknown))}. "
                         f"Choose from {', '.join(sorted(_MODEL_KEYS))} or 'all'.")
    return chosen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--system", default=None, help="Only score this system (default: all)")
    ap.add_argument("--n-fixations", type=int, default=6, help="DeepGaze++ scanpath length")
    ap.add_argument("--skip-existing", action="store_true", help="Skip renders whose outputs already exist")
    ap.add_argument("--models", default="all",
                    help="Comma-separated subset of {umsipp,dgiie,deepgaze}, or 'all' (default).")
    args = ap.parse_args()

    chosen_models = _parse_models(args.models)

    renders = discover_renders(args.system)
    if not renders:
        print(f"No renders found under {RENDERS_ROOT}" + (f" for system={args.system}" if args.system else ""))
        return

    print(f"Found {len(renders)} render(s) to score with models: {sorted(chosen_models)}")
    for s, ff, sc, _ in renders:
        print(f"  {s}/{ff}/{sc}.png")
    print()

    umsi = None
    dgiie = None
    dg = None
    if "umsipp" in chosen_models:
        from .umsipp import UMSIPP
        umsi = UMSIPP()
    if "dgiie" in chosen_models:
        from .deepgaze_iie import DeepGazeIIE
        dgiie = DeepGazeIIE()
    if "deepgaze" in chosen_models:
        from .deepgaze import DeepGazePP
        dg = DeepGazePP()

    print()
    t0 = time.time()

    for i, (system, ff, scenario, image_path) in enumerate(renders, 1):
        paths = out_paths(system, ff, scenario)

        t_img = time.time()
        print(f"[{i}/{len(renders)}] {system}/{ff}/{scenario}")

        if umsi is not None:
            if args.skip_existing and paths["heatmap"].exists() and paths["heatmap_overlay"].exists():
                print(f"    umsi++         skipped (already exists)")
            else:
                t = time.time()
                heat = umsi.heatmap(image_path)
                umsi.save_heatmap_png(heat, paths["heatmap"])
                umsi.save_overlay_png(image_path, heat, paths["heatmap_overlay"])
                print(f"    umsi++       {time.time() - t:5.1f}s  -> {paths['heatmap'].name}")

        if dgiie is not None:
            if args.skip_existing and paths["dgiie_heatmap"].exists() and paths["dgiie_heatmap_overlay"].exists():
                print(f"    deepgaze-iie   skipped (already exists)")
            else:
                t = time.time()
                heat = dgiie.heatmap(image_path)
                dgiie.save_heatmap_png(heat, paths["dgiie_heatmap"])
                dgiie.save_overlay_png(image_path, heat, paths["dgiie_heatmap_overlay"])
                print(f"    deepgaze-iie {time.time() - t:5.1f}s  -> {paths['dgiie_heatmap'].name}")

        if dg is not None:
            if args.skip_existing and paths["scanpath_json"].exists() and paths["scanpath_overlay"].exists():
                print(f"    deepgaze++   skipped (already exists)")
            else:
                t = time.time()
                fixations, (W, H) = dg.scanpath(image_path, n_fixations=args.n_fixations)
                paths["scanpath_json"].parent.mkdir(parents=True, exist_ok=True)
                paths["scanpath_json"].write_text(json.dumps({
                    "image": str(image_path.relative_to(ROOT.parent)),
                    "width": W,
                    "height": H,
                    "n_fixations": args.n_fixations,
                    "fixations": [{"x": x, "y": y, "index": idx} for idx, (x, y) in enumerate(fixations)],
                }, indent=2) + "\n")
                dg.save_scanpath_overlay(image_path, fixations, paths["scanpath_overlay"])
                print(f"    deepgaze++   {time.time() - t:5.1f}s  -> {paths['scanpath_json'].name}")

        print(f"  total {time.time() - t_img:5.1f}s")

    print(f"\nDone. {len(renders)} render(s) scored in {time.time() - t0:.1f}s")
    print(f"Outputs under {SCORES_ROOT}/")


if __name__ == "__main__":
    main()
