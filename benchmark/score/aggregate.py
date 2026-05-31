"""Aggregate per-cell metrics from saved heatmaps.

For each (system, form_factor, scenario), reads the focal bbox from
`benchmark/focal_targets.json` and computes:

    UMSI++       mass_on_target  +  nss_on_target
    DeepGazeIIE  mass_on_target  +  nss_on_target

Writes one big JSON to `benchmark/scores/aggregate.json` and prints a
human-readable triangulated table.

Usage:
    python -m benchmark.score.aggregate
    python -m benchmark.score.aggregate --metric nss
    python -m benchmark.score.aggregate --metric mass --model dgiie
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .metrics import mass_on_target, nss_on_target

ROOT = Path(__file__).resolve().parent.parent
SCORES_ROOT = ROOT / "scores"
FOCALS = ROOT / "focal_targets.json"

SYSTEMS = ["monad", "nasa", "apple", "material", "carbon"]
FORMS = ["ski-AR", "climb-AR", "device-only"]
SCENARIOS = ["calm", "alert", "warning"]


def collect() -> dict:
    focals = json.loads(FOCALS.read_text())
    out = {}
    for system in SYSTEMS:
        out[system] = {}
        for form in FORMS:
            out[system][form] = {}
            for scen in SCENARIOS:
                cell_out = {}
                try:
                    bbox = focals[system][form][scen]["bbox"]
                except KeyError:
                    out[system][form][scen] = None
                    continue
                base = SCORES_ROOT / system / form

                umsi_png = base / f"{scen}.heatmap.png"
                if umsi_png.exists():
                    cell_out["umsi_mass"] = mass_on_target(umsi_png, bbox)
                    cell_out["umsi_nss"]  = nss_on_target(umsi_png, bbox)

                dgiie_png = base / f"{scen}.dgiie.heatmap.png"
                if dgiie_png.exists():
                    cell_out["dgiie_mass"] = mass_on_target(dgiie_png, bbox)
                    cell_out["dgiie_nss"]  = nss_on_target(dgiie_png, bbox)

                cell_out["bbox"] = bbox
                cell_out["intent"] = focals[system][form][scen].get("intent", "")
                out[system][form][scen] = cell_out
    return out


def print_table(agg: dict, model_prefix: str, metric: str, label: str, fmt: str):
    """Print per-cell table for one (model, metric) pair."""
    key = f"{model_prefix}_{metric}"
    print(f"\n## {label}")
    header = f"{'form':<14}{'scen':<10}" + "".join(f"{s:>10}" for s in SYSTEMS)
    print(header)
    print("-" * len(header))
    # Track per-cell winners
    for form in FORMS:
        for scen in SCENARIOS:
            row = f"{form:<14}{scen:<10}"
            vals = {}
            for sys in SYSTEMS:
                cell = agg.get(sys, {}).get(form, {}).get(scen) or {}
                v = cell.get(key)
                vals[sys] = v
            if any(v is not None for v in vals.values()):
                winner = max((s for s in SYSTEMS if vals.get(s) is not None),
                             key=lambda s: vals[s])
            else:
                winner = None
            for sys in SYSTEMS:
                v = vals.get(sys)
                if v is None:
                    cell_s = f"{'—':>10}"
                else:
                    star = " ★" if sys == winner else "  "
                    cell_s = f"{format(v, fmt):>8}{star}"
                row += cell_s
            print(row)

    # Per-system averages
    print()
    print(f"{'system':<14}{'avg':>14}")
    for sys in SYSTEMS:
        vals = [agg[sys][f][s][key]
                for f in FORMS for s in SCENARIOS
                if agg.get(sys, {}).get(f, {}).get(s) and agg[sys][f][s].get(key) is not None]
        if not vals: continue
        avg = sum(vals) / len(vals)
        print(f"{sys:<14}{format(avg, fmt):>14}")


def win_counts(agg: dict, model_prefix: str, metric: str) -> dict[str, int]:
    key = f"{model_prefix}_{metric}"
    counts = {s: 0 for s in SYSTEMS}
    for form in FORMS:
        for scen in SCENARIOS:
            vals = {}
            for sys in SYSTEMS:
                cell = agg.get(sys, {}).get(form, {}).get(scen) or {}
                v = cell.get(key)
                if v is not None:
                    vals[sys] = v
            if vals:
                winner = max(vals, key=vals.get)
                counts[winner] += 1
    return counts


def triangulated_summary(agg: dict):
    """Show the four (model, metric) lenses side by side, then overall ranking."""
    print("\n" + "=" * 70)
    print("TRIANGULATED RANKING — agreement across models and metrics")
    print("=" * 70)
    overall_rank = {s: {"wins_total": 0, "avg_rank": []} for s in SYSTEMS}

    for model in ["umsi", "dgiie"]:
        for metric in ["mass", "nss"]:
            label = f"{model.upper()} / {metric}"
            key = f"{model}_{metric}"
            wins = win_counts(agg, model, metric)
            # Per-system avg of the metric across all 9 cells
            sys_avgs = {}
            for sys in SYSTEMS:
                vals = [agg[sys][f][s][key]
                        for f in FORMS for s in SCENARIOS
                        if agg.get(sys, {}).get(f, {}).get(s) and agg[sys][f][s].get(key) is not None]
                if vals:
                    sys_avgs[sys] = sum(vals) / len(vals)
            # Rank highest-first
            ranked = sorted(SYSTEMS, key=lambda s: sys_avgs.get(s, float("-inf")), reverse=True)
            for rank, sys in enumerate(ranked, 1):
                overall_rank[sys]["avg_rank"].append(rank)
            for sys, n in wins.items():
                overall_rank[sys]["wins_total"] += n
            fmt = ".3f" if metric == "nss" else ".1%"
            print(f"\n[{label}]   per-cell wins (out of 9) + 9-cell average")
            for sys in ranked:
                avg = sys_avgs.get(sys)
                avg_s = format(avg, fmt) if avg is not None else "—"
                print(f"   {sys:<10}  wins={wins[sys]:>2}   avg={avg_s:>8}   rank #{ranked.index(sys)+1}")

    print()
    print("=" * 70)
    print("OVERALL — averaged rank across the 4 (model, metric) lenses")
    print("=" * 70)
    rows = []
    for sys in SYSTEMS:
        ar = overall_rank[sys]["avg_rank"]
        if not ar: continue
        rows.append((sys, sum(ar) / len(ar), overall_rank[sys]["wins_total"]))
    rows.sort(key=lambda r: (r[1], -r[2]))
    print(f"{'rank':<6}{'system':<12}{'avg-rank':>12}{'wins (of 36)':>16}")
    for i, (sys, avg, wins) in enumerate(rows, 1):
        print(f"{i:<6}{sys:<12}{avg:>12.2f}{wins:>16}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metric", choices=["mass", "nss", "both"], default="both")
    ap.add_argument("--model", choices=["umsi", "dgiie", "both"], default="both")
    ap.add_argument("--write", action="store_true", help="Write aggregate.json")
    args = ap.parse_args()

    agg = collect()

    if args.write:
        out_path = SCORES_ROOT / "aggregate.json"
        out_path.write_text(json.dumps(agg, indent=2) + "\n")
        print(f"wrote {out_path}")

    models = ["umsi", "dgiie"] if args.model == "both" else [args.model]
    metrics = ["mass", "nss"] if args.metric == "both" else [args.metric]
    for model in models:
        for metric in metrics:
            label = f"{model.upper()}++ — {'mass-on-target' if metric == 'mass' else 'NSS-on-target'}"
            fmt = ".3f" if metric == "nss" else ".1%"
            print_table(agg, model, metric, label, fmt)

    if args.model == "both" and args.metric == "both":
        triangulated_summary(agg)


if __name__ == "__main__":
    main()
