# Monad System — Perception Benchmark

A benchmark that measures **whether a design system's stylistic choices direct user attention to the intended focal target**, using eye-tracking-based saliency models.

## Status

| Phase | State | Artifacts |
|---|---|---|
| **Phase 0** — NASA extraction | ✅ Done | [docs/nasa_design_manual.md](docs/nasa_design_manual.md) (77KB, 12k words, 9 sections), [benchmark/nasa_system.json](benchmark/nasa_system.json) (5 colors, 4 type families, grid, logo, applications), [src/extract_nasa.py](src/extract_nasa.py) re-runnable script. Cost: ~$0.20 via Gemini 2.5 Pro. |
| **Phase 1 prep** — UEyes setup | ✅ Done | UEyes cloned to `benchmark/ueyes/` (gitignored). UMSI++ and DeepGaze++ both verified running on the climbing underlay. Smoke-test outputs in [benchmark/ueyes_smoketest/](benchmark/ueyes_smoketest/). Weights (401MB) downloaded to `benchmark/ueyes_smoketest/weights_dl/`. |
| **Phase 1** — Monad pilot | ✅ Done | 3 scenario specs in [benchmark/content_spec/](benchmark/content_spec/); 9 Monad HTML layouts in [benchmark/layouts/monad/](benchmark/layouts/monad/); 9 PNG renders in [benchmark/renders/monad/](benchmark/renders/monad/); per-render focal-target bboxes in [benchmark/focal_targets.json](benchmark/focal_targets.json). |
| **Refactor** — batch scoring | ✅ Done | [benchmark/score/](benchmark/score/) package: `UMSIPP` + `DeepGazePP` load once, infer many. Verified end-to-end on the 9 Monad renders: **9 scored in 12.3 s** (was ~13 min). Outputs (heatmaps, scanpaths, overlays) in [benchmark/scores/](benchmark/scores/). |
| **Phase 1.5** — NASA-pure | ✅ Done | 9 NASA-pure layouts in [benchmark/layouts/nasa/](benchmark/layouts/nasa/) with shared [_tokens.css](benchmark/layouts/nasa/_tokens.css); 9 renders in [benchmark/renders/nasa/](benchmark/renders/nasa/); bboxes merged into [focal_targets.json](benchmark/focal_targets.json). **Cross-validation:** JPL Explorer-1 uses `#e4002b` as `red.500` (exact match to our extracted NASA Red) and Helvetica Now as its display family — both confirm the 1976-manual extraction. Reference clones in `benchmark/refs/` (gitignored). |
| **Token shift** — Monad system NASA-fied | ✅ Done | Source-of-truth change: [colors.json](colors.json) `Alert_1` `#D64C45` → **`#E4002B`** (NASA Red, PMS 179); [css_template.py](src/templates/css_template.py) `--strata-on-error` now `{bg_light}` (off-white), giving white-on-red as the system default for stop-now signaling. Rule documented in [AGENTS.md](AGENTS.md). All 54 unit tests pass. The override `#focal-target { --strata-on-error: #FFFFFF }` previously in the 3 monad warning layouts is now redundant — removed. **Re-scored monad warnings: 83.6% / 85.7% / 84.6% mass-on-target** across ski-AR / climb-AR / device-only (vs ~82% with brick red), with all 9 monad heatmaps regenerated from the new build. |
| **Phase 1.6** — Fan-out layouts | ✅ Done | Apple HIG, Material 3, Carbon: 3 systems × 9 renders = 27 more. (Monad+NASA collapsed into Monad after the token shift — it's now the same artifact.) All in [benchmark/layouts/{apple,material,carbon}/](benchmark/layouts/). |
| **Phase 2** — Score all 45 | ✅ Done | 45 renders scored in **60 s** via `python -m benchmark.score.run_batch`. Heatmaps + scanpaths + overlays in [benchmark/scores/](benchmark/scores/). |
| **Phase 3** — Report | ✅ Done | [benchmark/report.md](benchmark/report.md) — 9-cell results table, per-scenario averages, win counts, honest findings (thesis partially falsified — Material 3 wins 5/9 cells; Monad wins on `device-only` warning, second overall). |

### Phase 0 findings worth noting

- **NASA's palette is austere.** Only 5 colors total: NASA Red (`#E4002B` PMS 179), Warm Gray (`#5A5A5A` Fed Std 16165), Black, White, Vehicle Blue (`#0047AB`). This means **"Monad+NASA" synthesis will be mostly about *layout / typography / grid / restraint principles* — not color additions**. The contribution from NASA is the discipline of the system, not new colors.
- **Typography is specific:** Helvetica primary, Futura secondary sans, Garamond primary serif, Times Roman secondary serif. Mostly weights + roles rather than exhaustive size scale.
- **Grid is 1/2/3-column with documented use cases.** Usable.
- **Logo construction rules and 7 forbidden modifications** captured — useful as an *evaluation reference* (NASA-pure layouts that violate these are misrepresentations).

### Phase 1 prep technicals

- **UMSI++** required wrapping: upstream notebook depends on Keras-2 internals that don't exist in Keras 3 / Python 3.13. Subagent rebuilt the architecture against `tf_keras` and loaded weights via `by_name=True`. Works. ([benchmark/ueyes_smoketest/umsipp_infer.py](benchmark/ueyes_smoketest/umsipp_infer.py))
- **DeepGaze++** required two upstream patches (CUDA→CPU since MPS rejects float64 centerbias, and `Image.ANTIALIAS`→`Image.Resampling.LANCZOS`). Patched in the wrapper. ([benchmark/ueyes_smoketest/run_deepgaze.py](benchmark/ueyes_smoketest/run_deepgaze.py))
- **Weights provenance:** https://userinterfaces.aalto.fi/ueyeschi23/model_weights.zip (not in any README — discovered by the prep subagent; documented in [benchmark/ueyes_smoketest/README.md](benchmark/ueyes_smoketest/README.md)).
- **Open TODO before Phase 1 batch scoring:** refactor both wrappers so model construction happens once outside the per-image loop (currently 14s/image UMSI++ rebuild; should be ~1s after refactor → 54 images in ~1 min vs ~13 min).

---

## Thesis

Outdoor athletic UIs (climbing, skiing) operate in high-stakes, attention-constrained conditions. We test how well five design systems — including a NASA-informed extension of Monad — direct first-second attention to a designer-declared focal target across calm / alert / warning scenarios, in three form factors (AR ski overlay, AR climb overlay, no-underlay handheld device).

**Falsifiable thesis:** Monad, when extended with principles extracted from NASA's 1976 Graphics Standards Manual, directs first-second attention to the intended focal target more reliably than Apple HIG, Material, Carbon, or NASA-pure tokens — across all three scenarios.

The test can be wrong. That's the point.

---

## What we are NOT doing (and why)

- **Not using TRIBE v2.** It's a brain-encoder predicting fMRI responses to video — wrong tool for "rate this UI's intent legibility." Output is ~20k cortical vertices, not a usable score.
- **Not running an optimization loop** that tunes tokens against the saliency model. Goodhart's law: optimizers find degenerate solutions (gray everything, micro-text) that win the metric and fail the design. The judge cannot be the optimizer.
- **Not pretending this is component-vs-component fairness.** We test each system's idiomatic, best-effort answer at the token + component layer, *as it would be shipped*. The report says so.

---

## Pipeline

```diagram
NASA PDF ──▶ OCR + extract ──▶ docs/nasa_design_manual.md
                                + benchmark/nasa_system.json
                                       │
colors.json (Monad) ──────────────────▶ benchmark/monad_nasa.json (synthesis)
                                       │
                                       ▼
        ╭──────────────────────────────────────────────╮
        │ 5 systems × 3 form factors × 3 scenarios     │
        │ = 45 idiomatic layouts                       │
        │ × theme variants (8 total) = 72 renders      │
        ╰──────────────────┬───────────────────────────╯
                           ▼
              Playwright headless → PNG
                           │
                           ▼
        ╭──────────────────────────────────────────────╮
        │ UEyes scoring (UMSI++ + DeepGaze++, 1s)      │
        │  - mass-on-target = Σ saliency in bbox /     │
        │                     total saliency mass      │
        │  - first-fixation-hit = bool per scanpath    │
        ╰──────────────────┬───────────────────────────╯
                           ▼
                  benchmark/report.md
```

---

## Locked decisions

### Metric — attention efficiency
For each render:
1. Designer declares a **focal target bbox** before rendering (the element the user *should* look at first, given the scenario).
2. UMSI++ produces a 1-second saliency heatmap.
3. DeepGaze++ produces a 1-second scanpath.
4. **Primary score** — `mass_on_target = Σ saliency_inside_bbox / Σ saliency_total`, range [0,1].
5. **Secondary score** — `first_fixation_hit_rate` = % of scanpath samples whose first fixation lies in the bbox. Computed over **N=20 stochastic DeepGaze++ samples per render** (cheap; supports paired statistical tests).

Higher is better. "Better" = the eye went where the designer wanted it to go.

### Form factors (3)

| Code | Canvas | Underlay | Purpose |
|---|---|---|---|
| `ski-AR` | 1920×1080 landscape | `benchmark/underlay_skiing.png` (scale-to-cover) | UI competes with snow glare + open vista |
| `climb-AR` | 1920×1080 landscape | `benchmark/underlay_rockclimbing.png` (scale-to-cover) | UI competes with rock texture + foliage |
| `device-only` | 390×844 portrait (phone) | none | UI's own hierarchy without environmental noise |

Underlay normalization: photos scaled so 1080 height fills, excess width cropped (matches how AR goggles SDKs handle camera passthrough).

### Systems (6, all light theme for v1)

| System | Theme | Source |
|---|---|---|
| Monad | light | `colors.json` → compiler |
| Monad + NASA | light | Synthesis from `colors.json` + extracted NASA tokens |
| Apple HIG | light | Reimplemented as CSS-only token layer |
| Material 3 | light | Google's Material tokens |
| Carbon (IBM) | light | `@carbon/styles` tokens |
| NASA-pure | light | Single theme per 1976 manual |

**Total renders:** 6 systems × 3 form factors × 3 scenarios = **54 renders** (and 54 unique layouts, since one theme per system).

**Dark theme variants deferred to v2** — the compiler can produce them mechanically when needed, but v1 holds the theme axis constant to keep the experiment clean.

### Scenarios (3)

| Scenario | Activity bias (AR only) | Designer intent | Focal target |
|---|---|---|---|
| `calm` | Ski (open vista, nominal pacing) | At-a-glance status; nothing wrong | Primary metric tile (e.g., speed/altitude) |
| `alert` | Climb (decision point) | One subsystem flagged amber | The flagged item |
| `warning` | Climb (critical state) | Master-alarm equivalent | The warning callout |

`device-only` uses a neutral background; same focal-target convention.

### Build strategy — pilot then fan out

**Phase 0 — NASA extraction (parallel, non-blocking)**
- OCR [docs/nasa_graphics_manual_nhb_1430-2_jan_1976.pdf](docs/nasa_graphics_manual_nhb_1430-2_jan_1976.pdf) using Gemini (native PDF support, better on 1976 scans than OpenAI).
- Output `docs/nasa_design_manual.md` (human-readable reference).
- Extract `benchmark/nasa_system.json` (colors, type, spacing, grid rules).

**Phase 1 — Monad + Monad+NASA pilot (validates pipeline)**
- Synthesize `benchmark/monad_nasa.json` — *additive* extension of Monad with NASA's rules where Monad is silent. Do not override Monad tokens without an explicit, recorded reason.
- Build 9 layouts: Monad × 3 form factors × 3 scenarios.
- Re-skin to Monad+NASA via token swap → 9 more layouts. Total Phase 1: **18 renders**.
- Score all 18 with UEyes. Inspect the heatmaps. Decide if `mass_on_target` actually produces interpretable, non-degenerate rankings.
- **Gate:** if Phase 1 reveals the metric is broken or the pipeline is brittle, stop and re-grill. Do not fan out blindly.

**Phase 2 — Fan out**
- Apple, Material, Carbon, NASA-pure: 4 systems × 3 × 3 = **36 renders**.
- Score everything. Grand total: **54 renders**.

**Phase 3 — Report**
- `benchmark/report.md` with per-cell heatmap overlays in `benchmark/renders/`.
- **9-cell results table** (3 form factors × 3 scenarios). Each cell:
  - `first_fixation_hit_rate` per system with **paired bootstrap 95% CI** over N=20 DeepGaze++ samples (primary statistical claim).
  - `mass_on_target` per system as a deterministic corroborating ranking.
  - Heatmap overlay thumbnail per system.
- When the two metrics agree per cell → strong claim. When they disagree → flagged as a distinct finding worth its own paragraph.
- No across-cell aggregation, no overall leaderboard. The story is per-cell.

---

## Tooling

- **OCR / VLM:** Gemini (primary, native PDF), OpenAI (cross-check) — keys in `.env` (note: `GEMENI_KEY` spelling preserved).
- **Saliency:** UEyes UMSI++ (https://github.com/YueJiang-nj/UEyes-CHI2023, `saliency_models/UMSI++/`).
- **Scanpath:** UEyes DeepGaze++ (`scanpath_models/DeepGaze++/`).
- **Headless render:** Playwright Chromium at 1920×1080 (workspace already has `.playwright-mcp/`).
- **Monad compiler:** existing `src/compile_color.py` pipeline produces CSS for any token JSON we feed it — handles the 8 theme variants per layout for free.

---

## Planned repository layout

```
benchmark/
├── underlay_skiing.png            # existing
├── underlay_rockclimbing.png      # existing
├── nasa_system.json               # Phase 0 output
├── monad_nasa.json                # Phase 1 output
├── content_spec/                  # 3 scenario specs, shared across all systems
│   ├── calm.md
│   ├── alert.md
│   └── warning.md
├── layouts/
│   ├── monad/{ski-AR,climb-AR,device-only}/{calm,alert,warning}.html
│   ├── monad_nasa/...
│   ├── apple/...
│   ├── material/...
│   ├── carbon/...
│   └── nasa/...
├── focal_targets.json             # bbox + intent label per layout
├── renders/                       # PNG outputs (72)
├── scores/                        # UMSI++ heatmaps + DeepGaze++ scanpaths
└── report.md
```

---

## Operational defaults (locked)

| # | Topic | Decision |
|---|---|---|
| 1 | OCR tool primary | **Gemini** (native PDF, better on 1976 scans); OpenAI used as audit on disputed extractions |
| 2 | NASA token schema | Sibling file `benchmark/nasa_system.json`, *not* extending `colors.json` — keeps NASA extraction independently re-runnable |
| 3 | Reference doc format | Markdown — `docs/nasa_design_manual.md` |
| 4 | License audit | Verify UMSI++ weight license before publishing renders; NASA 1976 manual is US Govt → public domain (no clearance needed) |
| 5 | Report location | `benchmark/report.md` (Markdown, in-repo). HTML site is a v2 nicety. |
| 6 | Scenarios count | **3** (calm / alert / warning) — max signal separation per cell |
| 7 | Build strategy | **Pilot then fan out** — Phase 1 validates pipeline on Monad + Monad+NASA before fanning to other 4 systems |

---

## History / decisions journal

- **TRIBE v2 dropped.** It's a brain-encoder (predicts fMRI from video), not a UI perception model. Output is ~20k cortical vertices that would have required hand-picked ROIs and neuroscience interpretation. Replaced with UEyes saliency + designer-declared focal targets.
- **Optimization loop dropped.** Tuning tokens against the saliency model invites Goodhart-degenerate solutions and contaminates the judge. Benchmarking only.
- **Domain pivoted** from generic dashboards / mission-control to outdoor athletic overlays. Reason: the underlay photos make the saliency test ecologically valid — the UI has to fight real-world visual noise, which is the actual job of climbing/skiing overlay UI.
- **Form factors expanded** from 1 to 3 (ski-AR, climb-AR, device-only) at user direction, to test how each system handles both noise-rich and clean canvases.
- **Theme variants enumerated** (8 total) to account for systems shipping multiple modes (Monad/Carbon/Material have light+dark; Apple and NASA-pure have one).
