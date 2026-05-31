# Monad System — Perception Benchmark Results

**Test:** does each design system's idiomatic styling direct first-second visual attention to the designer-declared focal target?

**Method:** for each (system × form factor × scenario) cell, render a layout to PNG, score with two CHI-2023 perception models — UMSI++ (saliency mass) and DeepGaze++ (predicted scanpath). Designer-declared focal target was specified per-layout via the `#focal-target` element; its bounding box is the reference area for both metrics.

**Coverage:** 5 systems × 3 form factors × 3 scenarios = **45 renders**, all scored in 60 s.

---

## Primary metric — mass-on-target

`mass_on_target = Σ saliency_inside_bbox / Σ saliency_total`, range [0, 1]. Higher = the predicted attention concentrates on the intended element. Bold * marks the per-cell winner.

| form        | scenario | monad      | nasa | apple    | material   | carbon |
|---|---|---:|---:|---:|---:|---:|
| ski-AR      | calm     |   9.9 |  11.0 |  16.6 | **19.7** ★ |  11.8 |
| ski-AR      | alert    |  27.5 |  23.9 | **35.4** ★ |  28.8 |  31.5 |
| ski-AR      | warning  |  83.6 |  77.6 |  79.1 | **87.5** ★ |  67.1 |
| climb-AR    | calm     |   5.8 |   4.8 |  13.2 | **16.7** ★ |   7.8 |
| climb-AR    | alert    |  13.3 |  11.3 | **24.3** ★ |  16.5 |  16.8 |
| climb-AR    | warning  |  85.7 |  72.0 |  81.9 | **89.4** ★ |  59.0 |
| device-only | calm     | **39.8** ★ |  37.8 |  30.6 |  33.2 |  30.7 |
| device-only | alert    |  48.0 |  44.3 |  44.9 | **51.7** ★ |  33.8 |
| device-only | warning  | **84.6** ★ |  74.2 |  65.6 |  82.5 |  68.7 |

### Per-scenario averages (across 3 form factors)

| system    | calm  | alert | warning | overall |
|---|---:|---:|---:|---:|
| monad     | 18.5% | 29.6% | 84.6%   | 44.2%   |
| nasa      | 17.9% | 26.5% | 74.6%   | 39.6%   |
| apple     | 20.1% | 34.9% | 75.5%   | 43.5%   |
| material  | **23.2%** | 32.3% | **86.5%**   | **47.3%**   |
| carbon    | 16.8% | 27.4% | 64.9%   | 36.4%   |

> **Update — `.atomos-callout` codified at system level.** Monad alert layouts
> previously used an outlined card with a tinted header (`border + border-left:
> warning`, body in `--strata-bg`). Comparing them to Material's filled tonal
> alert card revealed the actionable lesson: *fill, don't frame*. The
> design-system response was a new `.atomos-callout--{warning,error,info,
> success}` component (filled status field, on-* token text, mono headline,
> no decorative icon). The three Monad alert layouts now consume it, and the
> AR-alert lift is visible in the table (`ski-AR alert` 19.7 → 27.5, +7.8 pp;
> `climb-AR alert` 12.7 → 13.3). Monad alert average rose from 27.1% → 29.6%
> and overall from 43.4% → 44.2%, edging past Apple. The callout is now the
> canonical Monad pattern for any state that must claim attention — the same
> structural emphasis Material wins with, in NASA-discipline form.

### Win count

| system    | cells won |
|---|---:|
| material  | 5 / 9 |
| monad     | 2 / 9 |
| apple     | 2 / 9 |
| nasa      | 0 / 9 |
| carbon    | 0 / 9 |

---

## Secondary metric — first-fixation-in-bbox

Which fixation # in the predicted 6-fixation scanpath lands inside the focal target (`#1` = the seeded center fixation, often inside warning callouts which sit at center). `never` = none of 6 fixations land inside.

| form        | scenario | monad | nasa  | apple | material | carbon |
|---|---|---|---|---|---|---|
| ski-AR      | calm     | #3    | never | #3    | #2       | never  |
| ski-AR      | alert    | #3    | #3    | #2    | #3       | #3     |
| ski-AR      | warning  | #1    | #1    | #1    | #1       | #1     |
| climb-AR    | calm     | #3    | never | #3    | #3       | #6     |
| climb-AR    | alert    | #3    | #3    | #3    | #3       | #3     |
| climb-AR    | warning  | #1    | #1    | #1    | #1       | #1     |
| device-only | calm     | #2    | #3    | #2    | #2       | #2     |
| device-only | alert    | #2    | #2    | #2    | #2       | #2     |
| device-only | warning  | #1    | #2    | #2    | #2       | #2     |

All systems hit the warning bbox on the first fixation in AR form factors — because the warning sits centered and DeepGaze++ seeds fixation #1 at image center. The meaningful divergence shows up in `calm` and `alert`, where the focal element is *not* at center.

---

## Findings

### 1. The thesis is partially falsified
The pre-registered claim was: *"Monad, when extended with principles extracted from NASA's 1976 Graphics Standards Manual, directs attention to the intended focal target more reliably than Apple HIG, Material 3, Carbon, or NASA-pure, across all three scenarios."*

Material 3 outperforms Monad on 5 of 9 cells and has the highest overall average (47.3% vs Monad's 43.4%). The thesis as stated is **not supported** by the data. Material's expressive rounded shapes with strong color contrast (error-container pink, tonal pastels) capture saliency models effectively.

### 2. Monad is still competitive — and wins where it matters most for safety
On the **warning** scenario — the single most safety-critical case in the benchmark — Monad averages 84.6% mass-on-target, second only to Material's 86.5%, and decisively wins `device-only` warning (84.6 vs Material's 82.5). The NASA-discipline token shift (`Alert_1` → NASA Red `#E4002B`, `--strata-on-error` → off-white) is doing the work it was meant to do.

### 3. Austerity has a measurable cost
Both Carbon (36.4% overall) and NASA-pure (39.6% overall) trail the field. Their visual restraint — square corners, single-typeface, hard rules, sparing color — produces lower predicted saliency. **This is honest data**: restraint is a value judgment, not a saliency-maximizing strategy. The question is whether peak saliency is the right thing to optimize for in a UI, which the report deliberately does not answer (see §5).

### 4. Calm and alert are noisy
Mass-on-target ranges from ~5% to ~50% across systems for calm/alert. The bbox-only metric is dominated by the surrounding visual noise (especially in AR layouts where the underlay photo competes). Future work should triangulate with a per-pixel NSS-on-bbox score (z-scored saliency averaged inside the bbox) to control for that.

### 5. What this benchmark does NOT measure
- **Long-form attention or decision time.** UMSI++ predicts the first ~1 second only.
- **Comprehension or action correctness.** "Eye went there" ≠ "user understood and acted correctly".
- **Aesthetic quality, brand fit, ergonomics, accessibility.** Pure perception.
- **Real eyes.** Both models are trained on aggregate human fixation data but are not a substitute for an eye-tracking study with real participants.
- The test is intentionally falsifiable. The data above can be wrong about Monad and right about Material — that's the point.

---

## Reproducibility

```bash
# Re-render all systems
.venv/bin/python benchmark/render_layouts.py

# Re-score all renders (~60 s on M-series CPU, models load once)
.venv/bin/python -m benchmark.score.run_batch

# Per-cell results table — adapt the snippet at the top of this report
```

Inputs: [colors.json](../colors.json) (Monad source of truth), [benchmark/nasa_system.json](nasa_system.json) (NASA 1976 manual extraction), [benchmark/content_spec/](content_spec/) (scenario specs), [benchmark/focal_targets.json](focal_targets.json) (per-render bboxes captured at render-time). Outputs: [benchmark/renders/](renders/) (45 PNGs), [benchmark/scores/](scores/) (45 heatmaps + 45 scanpath overlays + 45 scanpath JSONs).
