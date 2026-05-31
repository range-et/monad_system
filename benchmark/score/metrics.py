"""Per-bbox metrics for saliency heatmaps.

Two metrics, deliberately complementary:

    mass_on_target  =  Σ s(p inside bbox) / Σ s(p over image)
        Range [0, 1]. Intuitive ("what fraction of attention falls on the
        focal element"), but inflated when a design colours the whole canvas
        — a tonal-pastel system can win this metric by having more saturated
        non-focal regions that absorb mass evenly, not because the focal
        itself is more salient. Matches the original benchmark metric.

    nss_on_target   =  mean( z_score(s)[inside bbox] )
        Z-scores the saliency map first (subtract mean, divide by std) and
        then averages the standardised values inside the bbox. Invariant to
        global brightness/saturation — measures how much *more salient than
        average* the focal region is. This is the standard Normalised
        Scanpath Saliency metric from the MIT Saliency Benchmark, adapted
        to a bbox region instead of a fixation map.

If a focal cell wins on both metrics, the win is real. If it wins on
mass-on-target but loses on NSS, the design just paints loudly elsewhere.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


def _load_heatmap_gray(path: Path | str) -> np.ndarray:
    h = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if h is None:
        raise ValueError(f"Unreadable heatmap: {path}")
    return h.astype(np.float32)


def _bbox_slice(bbox, H: int, W: int) -> tuple[slice, slice] | None:
    x, y, w, hh = bbox
    x = int(round(x)); y = int(round(y))
    w = int(round(w)); hh = int(round(hh))
    x1 = max(0, x); y1 = max(0, y)
    x2 = min(W, x + w); y2 = min(H, y + hh)
    if x2 <= x1 or y2 <= y1:
        return None
    return slice(y1, y2), slice(x1, x2)


def mass_on_target(heatmap_path: Path | str, bbox) -> float:
    """Fraction of total heatmap mass that falls inside the bbox."""
    h = _load_heatmap_gray(heatmap_path)
    H, W = h.shape
    sl = _bbox_slice(bbox, H, W)
    total = float(h.sum())
    if total <= 0 or sl is None:
        return 0.0
    return float(h[sl].sum()) / total


def nss_on_target(heatmap_path: Path | str, bbox) -> float:
    """Mean of z-scored saliency inside the bbox.

    Positive ⇒ focal region is more salient than the image average.
    Negative ⇒ focal region is *less* salient than the image average.
    Scale-invariant: a uniformly-bright image and a uniformly-dim image both
    yield NSS ≈ 0 inside any bbox, so this metric is not gameable by
    flooding the canvas with saturated colour.
    """
    h = _load_heatmap_gray(heatmap_path)
    H, W = h.shape
    sl = _bbox_slice(bbox, H, W)
    std = float(h.std())
    if std <= 1e-6 or sl is None:
        return 0.0
    z = (h - float(h.mean())) / std
    return float(z[sl].mean())
