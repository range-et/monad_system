"""Saliency / scanpath scoring package for the Monad perception benchmark.

Two thin model classes — `UMSIPP` and `DeepGazePP` — load weights once and
expose per-image inference methods so a batch run over N renders pays the model
construction cost exactly once.
"""

from .umsipp import UMSIPP
from .deepgaze import DeepGazePP
from .deepgaze_iie import DeepGazeIIE

__all__ = ["UMSIPP", "DeepGazePP", "DeepGazeIIE"]
