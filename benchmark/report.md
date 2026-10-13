# Monad System — Perception benchmark

This report answers one question. Does the styling of each design system send the first second of visual attention to the element that the designer marked as the focal target?

**Last run:** 13 October 2026. This run uses the current Monad type: Helvetica, sentence case and Medium-weight labels. The previous run (May 2026) used Inter and uppercase mono labels. The section "Change from the previous run" compares the two runs.

## Method

1. A script renders each layout to PNG (`benchmark/render_layouts.py`). Each layout marks one element as `#focal-target`. The script records the bounding box of that element.
2. Two saliency models score each render:
   - **UMSI++**, trained on UEyes user-interface data.
   - **DeepGazeIIE**, trained on MIT1003 free-viewing data of natural images.
3. Two metrics read each saliency map inside the focal bounding box:
   - **Mass-on-target** is the share of all predicted saliency that falls inside the box. The range is 0 to 1.
   - **NSS-on-target** is the mean z-scored saliency inside the box. This metric corrects for the size of the box.
4. The two models and the two metrics give four lenses. For each lens, the script ranks the five systems by their mean over 9 cells. The overall rank is the mean of the four lens ranks.
5. DeepGaze++ predicts a 6-fixation scanpath for each render. This gives the secondary metric.

**Coverage:** 5 systems × 3 form factors × 3 scenarios = **45 renders**.

## Result — overall ranking

| Rank | System | Mean rank (4 lenses) | Cell wins (of 36) |
|---|---|---:|---:|
| 1 | **Monad** | **2.00** | **11** |
| 2 | Material 3 | 2.25 | 8 |
| 3 | Apple HIG | 3.00 | 6 |
| 4 | NASA (1976 manual) | 3.25 | 8 |
| 5 | Carbon | 4.50 | 3 |

| Lens | 1st | 2nd | 3rd | 4th | 5th |
|---|---|---|---|---|---|
| UMSI++ / mass | Material 47.3% | Monad 45.0% | Apple 43.8% | NASA 39.6% | Carbon 36.4% |
| UMSI++ / NSS | NASA 1.540 | Apple 1.437 | Monad 1.406 | Carbon 1.381 | Material 1.308 |
| DeepGazeIIE / mass | Material 61.0% | Monad 55.9% | Apple 54.0% | Carbon 50.3% | NASA 48.8% |
| DeepGazeIIE / NSS | Monad 1.792 | Material 1.544 | NASA 1.516 | Apple 1.441 | Carbon 1.422 |

Monad ranks first on mean rank and on cell wins. Monad is first on one lens and in the top three on all four lenses. Material 3 is first on both mass-on-target lenses.

## Change from the previous run

| Value | May 2026 | October 2026 |
|---|---:|---:|
| Monad overall rank | 1, tied with Material (2.25) | **1 (2.00)** |
| Monad cell wins | 10 / 36 | 11 / 36 |
| Material cell wins | 9 / 36 | 8 / 36 |
| Monad UMSI++ mass, mean | 44.2% | 45.0% |
| Monad UMSI++ mass, warning | 84.6% | 86.2% |
| Monad UMSI++ mass, alert | 29.6% | 30.4% |
| Monad UMSI++ NSS, mean | 1.376 (rank 4) | 1.406 (rank 3) |
| Monad DeepGazeIIE mass, mean | 56.1% | 55.9% |
| Monad DeepGazeIIE NSS, mean | 1.790 | 1.792 |

The rank changed because Monad moved above Carbon on UMSI++ / NSS.

**Render noise.** The layouts of the other four systems did not change between the runs. Their scores still moved by up to 1.1 percentage points (Apple, device-only warning: 65.6% → 66.7%), because of browser and font rendering. Treat a difference of 1 point or less as noise. Most Monad changes in the table are at or near this limit. The warning mean (+1.6 points) is the largest change.

## Per-cell results

Bold marks the highest value in each row.

### UMSI++ mass-on-target (%)

| Form factor | Scenario | Monad | NASA | Apple | Material | Carbon |
|---|---|---:|---:|---:|---:|---:|
| ski-AR | calm | 9.9 | 11.0 | 16.6 | **19.7** | 11.9 |
| ski-AR | alert | 25.0 | 23.9 | **35.5** | 28.8 | 31.6 |
| ski-AR | warning | 86.0 | 77.6 | 79.0 | **87.5** | 67.1 |
| climb-AR | calm | 5.9 | 4.8 | 13.3 | **16.7** | 7.8 |
| climb-AR | alert | 15.2 | 11.3 | **24.5** | 16.5 | 16.8 |
| climb-AR | warning | 87.1 | 71.9 | 82.0 | **89.4** | 58.9 |
| device-only | calm | **39.5** | 37.8 | 31.1 | 33.2 | 30.6 |
| device-only | alert | 50.9 | 44.3 | 45.5 | **51.7** | 33.8 |
| device-only | warning | **85.6** | 74.2 | 66.7 | 82.5 | 68.7 |
| **Mean** | | 45.0 | 39.6 | 43.8 | 47.3 | 36.4 |

### UMSI++ NSS-on-target

| Form factor | Scenario | Monad | NASA | Apple | Material | Carbon |
|---|---|---:|---:|---:|---:|---:|
| ski-AR | calm | 1.790 | **2.293** | 2.039 | 1.497 | 1.816 |
| ski-AR | alert | 3.146 | **3.887** | 2.536 | 2.264 | 3.082 |
| ski-AR | warning | **1.344** | 1.170 | 1.158 | 1.338 | 1.343 |
| climb-AR | calm | 1.007 | 0.680 | 1.257 | **1.771** | 1.139 |
| climb-AR | alert | 1.762 | **1.992** | 1.974 | 1.446 | 1.587 |
| climb-AR | warning | 1.245 | 1.074 | 1.259 | 1.389 | **1.487** |
| device-only | calm | 0.635 | **0.710** | 0.496 | 0.551 | 0.527 |
| device-only | alert | 0.868 | **0.956** | 0.789 | 0.688 | 0.423 |
| device-only | warning | 0.859 | 1.102 | **1.431** | 0.829 | 1.027 |
| **Mean** | | 1.406 | 1.540 | 1.437 | 1.308 | 1.381 |

### DeepGazeIIE mass-on-target (%)

| Form factor | Scenario | Monad | NASA | Apple | Material | Carbon |
|---|---|---:|---:|---:|---:|---:|
| ski-AR | calm | 10.9 | 7.4 | 16.2 | **37.2** | 7.3 |
| ski-AR | alert | 39.9 | 43.7 | **69.1** | 58.1 | 58.9 |
| ski-AR | warning | **96.2** | 96.1 | 95.8 | 94.2 | 90.8 |
| climb-AR | calm | 13.5 | 6.3 | 18.9 | **37.9** | 6.7 |
| climb-AR | alert | 43.4 | 36.3 | **60.5** | 45.4 | 47.2 |
| climb-AR | warning | 94.8 | 94.8 | **94.8** | 91.2 | 89.4 |
| device-only | calm | **43.2** | 34.3 | 32.5 | 34.8 | 33.6 |
| device-only | alert | **68.9** | 40.9 | 52.2 | 65.8 | 47.3 |
| device-only | warning | **92.2** | 79.3 | 45.5 | 84.6 | 71.9 |
| **Mean** | | 55.9 | 48.8 | 54.0 | 61.0 | 50.3 |

### DeepGazeIIE NSS-on-target

| Form factor | Scenario | Monad | NASA | Apple | Material | Carbon |
|---|---|---:|---:|---:|---:|---:|
| ski-AR | calm | **2.192** | 1.217 | 1.796 | 2.188 | 0.897 |
| ski-AR | alert | 3.470 | **3.770** | 2.520 | 2.531 | 3.018 |
| ski-AR | warning | 1.287 | 1.146 | 1.153 | 1.262 | **1.614** |
| climb-AR | calm | **2.629** | 0.870 | 1.747 | 2.445 | 0.636 |
| climb-AR | alert | 3.053 | **3.267** | 2.282 | 2.345 | 2.680 |
| climb-AR | warning | 1.201 | 1.051 | 1.216 | 1.229 | **1.580** |
| device-only | calm | **0.599** | 0.567 | 0.579 | 0.470 | 0.580 |
| device-only | alert | **0.984** | 0.699 | 0.868 | 0.753 | 0.824 |
| device-only | warning | 0.717 | **1.058** | 0.811 | 0.671 | 0.967 |
| **Mean** | | 1.792 | 1.516 | 1.441 | 1.544 | 1.422 |

### UMSI++ mass-on-target by scenario (%)

| System | Calm | Alert | Warning | Mean |
|---|---:|---:|---:|---:|
| Monad | 18.4 | 30.4 | 86.2 | 45.0 |
| NASA | 17.9 | 26.5 | 74.6 | 39.6 |
| Apple | 20.3 | 35.2 | 75.9 | 43.8 |
| Material | 23.2 | 32.3 | 86.4 | 47.3 |
| Carbon | 16.8 | 27.4 | 64.9 | 36.4 |

## Secondary metric — first fixation in the box

The table shows which fixation in the 6-fixation DeepGaze++ scanpath is the first to land inside the focal box. "Never" means that no fixation lands inside the box.

| Form factor | Scenario | Monad | NASA | Apple | Material | Carbon |
|---|---|---|---|---|---|---|
| ski-AR | calm | #3 | never | #3 | #2 | never |
| ski-AR | alert | #3 | #3 | #2 | #3 | #3 |
| ski-AR | warning | #1 | #1 | #1 | #1 | #1 |
| climb-AR | calm | #3 | never | #3 | #3 | #6 |
| climb-AR | alert | #3 | #3 | #3 | #3 | #3 |
| climb-AR | warning | #1 | #1 | #1 | #1 | #1 |
| device-only | calm | #2 | #3 | #2 | #2 | #2 |
| device-only | alert | #2 | #2 | #2 | #2 | #2 |
| device-only | warning | #1 | #2 | #2 | #2 | #2 |

DeepGaze++ puts fixation #1 at the image centre. In the AR form factors, the warning is at the centre, so every system gets #1 there. The calm and alert rows are more useful, because their focal targets are away from the centre.

## Findings

### 1. Monad ranks first, by a small margin

Monad has the best mean rank (2.00) and the most cell wins (11 of 36). Material 3 is 0.25 behind on mean rank. Material has higher mass-on-target on both models: 47.3% against 45.0% on UMSI++, and 61.0% against 55.9% on DeepGazeIIE.

### 2. The original thesis is still not fully supported

The pre-registered claim was: "Monad, when extended with principles from NASA's 1976 Graphics Standards Manual, directs attention to the intended focal target more reliably than Apple HIG, Material 3, Carbon or NASA-pure, across all three scenarios."

The data does not support "across all three scenarios". Material 3 has the highest mean UMSI++ mass in the calm scenario (23.2%). Apple has the highest mean UMSI++ mass in the alert scenario (35.2%). Monad is first in neither scenario.

### 3. The warning callout performs at the level of Material 3

In the warning scenario, Monad's mean UMSI++ mass is 86.2%. Material's mean is 86.4%. The difference is 0.2 points, which is less than the render noise. On device-only, Monad has the highest warning score on both models: 85.6% against Material's 82.5% on UMSI++, and 92.2% against 84.6% on DeepGazeIIE.

### 4. Visual restraint costs mass-on-target

NASA-pure and Carbon have the lowest mass-on-target means on both models. Their square corners, single typeface and limited colour give less predicted saliency. NASA-pure ranks first on UMSI++ / NSS, so the cost depends on the metric. This report does not decide whether maximum saliency is the correct goal for an interface.

### 5. Calm and alert results vary a lot

Mass-on-target in calm and alert cells is between 6% and 69%. In the AR layouts, the photo underlay competes with the interface. The NSS lenses correct for box size but not for the underlay.

### 6. Limits of this benchmark

- The models predict approximately the first second of attention. They do not measure decision time.
- The benchmark does not measure comprehension or correct action.
- The benchmark does not measure aesthetics, brand fit, ergonomics or accessibility.
- The models learned from human fixation data. They do not replace an eye-tracking study with real participants.

## Reproducibility

Run these commands from the repository root. The benchmark needs Python 3.13, because TensorFlow 2.21 has no wheels for later versions. `make bench-venv` creates `.venv-benchmark` on uv-managed Python 3.13 and installs [benchmark/requirements.txt](requirements.txt).

```bash
# 1. Create the benchmark environment (one time)
make bench-venv

# 2. Build the CSS, render all 45 layouts, score them (approximately 140 s on an M-series CPU)
#    and write scores/aggregate.json
make bench
```

Inputs: [colors.json](../colors.json), [benchmark/nasa_system.json](nasa_system.json), [benchmark/content_spec/](content_spec/) and [benchmark/focal_targets.json](focal_targets.json). Outputs: `benchmark/renders/` (45 PNGs) and `benchmark/scores/` (heatmaps, scanpaths and `aggregate.json`). Git ignores both output folders.
