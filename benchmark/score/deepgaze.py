"""DeepGaze++ scanpath model — load once, predict many.

Reimplements the loop from upstream `predict.py` as a proper Python module so
the DeepGazeIII network (DenseNet201 backbone + readout head) is constructed
exactly once. Inhibition-of-Return semantics are preserved verbatim.

Coordinates returned by `.scanpath()` are in the **input image's original**
pixel space (the model internally works in a 2.5×-downsampled canvas).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import List, Sequence, Tuple

import numpy as np
import torch
from PIL import Image
from scipy.ndimage import zoom
from scipy.special import logsumexp

# Pillow 10+ polyfill (upstream uses Image.ANTIALIAS in places we don't import,
# but keep it for safety in case downstream code touches it)
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

ROOT = Path(__file__).resolve().parent.parent
DG_DIR = ROOT / "ueyes" / "scanpath_models" / "DeepGaze++"
DEFAULT_CENTERBIAS = DG_DIR / "centerbias_mit1003.npy"

# `deepgaze_pytorch` is a vendored package — make it importable without chdir.
if str(DG_DIR) not in sys.path:
    sys.path.insert(0, str(DG_DIR))

import deepgaze_pytorch  # noqa: E402

# Match upstream predict.py: input is downsampled by this factor before
# feeding the model. Output coordinates are then upscaled back.
DOWNSAMPLE = 2.5
# IOR mask radius as a fraction of min(H,W)
IOR_RADIUS_FRAC = 0.2
# DeepGazeIII conditions on the last N fixations; upstream caps `fixations` at 4
MAX_FIXATIONS_HISTORY = 4


def _device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    # MPS rejects float64 centerbias; CPU is the path of least resistance.
    return "cpu"


def _create_ior_mask(h: int, w: int, fx: Sequence[int], fy: Sequence[int], radius: int) -> torch.Tensor:
    """Inhibition-of-return mask. Older fixations are partially decayed."""
    mask = torch.zeros(h, w)
    Y, X = np.ogrid[:h, :w]
    n = len(fx)
    for i in range(n):
        dist = np.sqrt((X - fx[i]) ** 2 + (Y - fy[i]) ** 2)
        # Older fixations (smaller i) get weaker suppression so the model can
        # eventually revisit them; mirrors upstream behavior exactly.
        weight = 1 - 1 / 10 * (n - i - 1)
        mask = torch.maximum(mask, torch.from_numpy(dist <= radius) * weight)
    return 1 - mask


class DeepGazePP:
    """DeepGaze++ scanpath predictor. Build once, call `.scanpath()` per image."""

    def __init__(self, centerbias: Path | str | None = None):
        centerbias = Path(centerbias) if centerbias else DEFAULT_CENTERBIAS
        if not centerbias.exists():
            raise FileNotFoundError(f"DeepGaze++ centerbias not found: {centerbias}")
        self.device = _device()
        print(f"[deepgaze++] using device: {self.device}")

        # DeepGazeIII takes a `fixations` arg that ramps from 1 to 4 as the
        # scanpath grows. Build all four variants up front so the per-image
        # loop never instantiates a model.
        print(f"[deepgaze++] building models (fixations=1..4) …")
        self._models = {}
        for n in range(1, MAX_FIXATIONS_HISTORY + 1):
            m = deepgaze_pytorch.DeepGazeIII(n, pretrained=True).to(self.device)
            m.eval()
            self._models[n] = m
        self._centerbias_template = np.load(str(centerbias))
        self.centerbias_path = centerbias

    def _centerbias_for(self, h: int, w: int) -> np.ndarray:
        cb = zoom(
            self._centerbias_template,
            (h / self._centerbias_template.shape[0], w / self._centerbias_template.shape[1]),
            order=0,
            mode="nearest",
        )
        cb -= logsumexp(cb)
        return cb

    @torch.inference_mode()
    def _predict_next(self, image_arr: np.ndarray, fx, fy, centerbias, fixations: int, mask: torch.Tensor):
        model = self._models[fixations]
        image_tensor = torch.tensor([image_arr[:, :, :3].transpose(2, 0, 1)]).to(self.device)
        centerbias_tensor = torch.tensor([centerbias]).to(self.device)
        # Note: upstream predict.py has a typo passing fixation_history_x for
        # both x_hist and y_hist. We keep behavior identical so results match.
        x_hist = torch.tensor([np.array(fx)[model.included_fixations]]).to(self.device)
        y_hist = torch.tensor([np.array(fx)[model.included_fixations]]).to(self.device)
        log_density = (100 + model(image_tensor, centerbias_tensor, x_hist, y_hist)) \
            * mask.to(self.device).unsqueeze(0).unsqueeze(0) \
            - (1 - mask.to(self.device)) * 1000
        brightest = (log_density == torch.max(log_density)).nonzero()[0].detach().cpu().numpy()
        return brightest  # [batch, channel, y, x]

    def scanpath(self, image_path: Path | str, n_fixations: int = 6) -> Tuple[List[Tuple[int, int]], Tuple[int, int]]:
        """Predict a scanpath of `n_fixations` fixations.

        Returns `(fixations, (W_orig, H_orig))` where `fixations` is a list of
        `(x, y)` tuples in the **original** image's pixel coordinates.
        """
        image_path = Path(image_path)
        pil = Image.open(str(image_path)).convert("RGB")
        W_orig, H_orig = pil.size

        pil_ds = pil.resize((int(W_orig / DOWNSAMPLE), int(H_orig / DOWNSAMPLE)), Image.Resampling.LANCZOS)
        image = np.array(pil_ds)
        h, w = image.shape[:2]

        centerbias = self._centerbias_for(h, w)

        # Start fixation: image center (matches upstream)
        fx = [w // 2]
        fy = [h // 2]
        fixations = 1

        radius = int(IOR_RADIUS_FRAC * min(w, h))

        while len(fx) < n_fixations:
            mask = _create_ior_mask(h, w, fx, fy, radius)
            masked = image * mask.unsqueeze(2).numpy().astype("uint8")
            brightest = self._predict_next(masked, fx, fy, centerbias, fixations, mask)
            fx.append(int(brightest[3]))
            fy.append(int(brightest[2]))
            if fixations < MAX_FIXATIONS_HISTORY:
                fixations += 1

        # Upscale back to original-image coordinates.
        scale = DOWNSAMPLE
        upscaled = [(int(round(x * scale)), int(round(y * scale))) for x, y in zip(fx, fy)]
        return upscaled, (W_orig, H_orig)

    @staticmethod
    def save_scanpath_overlay(image_path: Path | str, fixations: List[Tuple[int, int]], out_path: Path | str) -> None:
        """Render dots + connecting line + numeric indices on a copy of the image."""
        from PIL import ImageDraw, ImageFont

        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        img = Image.open(str(image_path)).convert("RGB")
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None

        # Lines first so dots draw on top
        for i in range(1, len(fixations)):
            draw.line([fixations[i - 1], fixations[i]], fill=(255, 64, 0), width=4)
        for i, (x, y) in enumerate(fixations):
            r = 14
            draw.ellipse([x - r, y - r, x + r, y + r], outline=(255, 64, 0), width=4, fill=(255, 255, 255))
            if font:
                draw.text((x - 4, y - 8), str(i + 1), fill=(0, 0, 0), font=font)
        img.save(str(out_path))
