"""DeepGazeIIE free-viewing saliency model — load once, predict many.

Why this exists alongside UMSI++:
    UMSI++ is trained on UEyes (web/mobile/poster/movie/game UI screenshots).
    Its training distribution biases its predictions toward whatever looks
    like a contemporary UI in that dataset. DeepGazeIIE is trained on
    MIT1003 — free-viewing of natural images by human observers. Two
    independent training distributions = a triangulation check on every
    mass-on-target claim. If a design wins under both models, the lift is
    likely real; if it wins under only one, it's likely a dataset artifact.

Returns: float32 saliency map (probability density, exp'd from log-density),
in the source image's native pixel resolution.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import cv2
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from scipy.ndimage import zoom
from scipy.special import logsumexp

ROOT = Path(__file__).resolve().parent.parent
DG_DIR = ROOT / "ueyes" / "scanpath_models" / "DeepGaze++"
DEFAULT_CENTERBIAS = DG_DIR / "centerbias_mit1003.npy"

if str(DG_DIR) not in sys.path:
    sys.path.insert(0, str(DG_DIR))

import deepgaze_pytorch  # noqa: E402

# Same downsample convention as the scanpath module for parity.
DOWNSAMPLE = 2.5


def _device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


class DeepGazeIIE:
    """DeepGazeIIE saliency predictor. Build once, call `.heatmap()` per image."""

    def __init__(self, centerbias: Path | str | None = None):
        centerbias = Path(centerbias) if centerbias else DEFAULT_CENTERBIAS
        if not centerbias.exists():
            raise FileNotFoundError(f"DeepGazeIIE centerbias not found: {centerbias}")
        self.device = _device()
        print(f"[deepgaze-iie] using device: {self.device}")
        print(f"[deepgaze-iie] building mixture model (pretrained on MIT1003) …")
        self._model = deepgaze_pytorch.DeepGazeIIE(pretrained=True).to(self.device)
        self._model.eval()
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
    def heatmap(self, image_path: Path | str) -> np.ndarray:
        """Return a float32 saliency map at the source image's native resolution."""
        image_path = Path(image_path)
        pil = Image.open(str(image_path)).convert("RGB")
        W_orig, H_orig = pil.size

        pil_ds = pil.resize(
            (int(W_orig / DOWNSAMPLE), int(H_orig / DOWNSAMPLE)),
            Image.Resampling.LANCZOS,
        )
        image_arr = np.array(pil_ds)
        h, w = image_arr.shape[:2]

        centerbias = self._centerbias_for(h, w)
        image_tensor = torch.tensor([image_arr[:, :, :3].transpose(2, 0, 1)], dtype=torch.float32).to(self.device)
        centerbias_tensor = torch.tensor([centerbias], dtype=torch.float32).to(self.device)

        log_density = self._model(image_tensor, centerbias_tensor)  # [1, 1, h, w]
        density = torch.exp(log_density)[0, 0].detach().cpu().numpy().astype(np.float32)

        # Upsample back to the source image's native resolution.
        return cv2.resize(density, (W_orig, H_orig))

    @staticmethod
    def save_heatmap_png(heat: np.ndarray, out_path: Path | str) -> None:
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        fmin, fmax = float(heat.min()), float(heat.max())
        if fmax > fmin:
            u8 = ((heat - fmin) / (fmax - fmin) * 255).astype(np.uint8)
        else:
            u8 = np.zeros_like(heat, dtype=np.uint8)
        cv2.imwrite(str(out_path), u8)

    @staticmethod
    def save_overlay_png(image_path: Path | str, heat: np.ndarray, out_path: Path | str) -> None:
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        src = cv2.imread(str(image_path))
        fmin, fmax = float(heat.min()), float(heat.max())
        if fmax > fmin:
            u8 = ((heat - fmin) / (fmax - fmin) * 255).astype(np.uint8)
        else:
            u8 = np.zeros_like(heat, dtype=np.uint8)
        heat_color = cv2.applyColorMap(u8, cv2.COLORMAP_JET)
        overlay = cv2.addWeighted(src, 0.5, heat_color, 0.5, 0.0)
        cv2.imwrite(str(out_path), overlay)
