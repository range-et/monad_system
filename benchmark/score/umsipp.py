"""UMSI++ saliency model — load once, predict many.

Architecture is rebuilt against `tf_keras` (Keras-2 API on TF 2.x) so the
upstream hdf5 weights load by name on Python 3.13. See the original smoke-test
file `benchmark/ueyes_smoketest/umsipp_infer.py` for the porting notes.
"""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
os.environ.setdefault("TF_USE_LEGACY_KERAS", "1")

import cv2
import numpy as np

import tf_keras as keras
from tf_keras import layers
from tf_keras.models import Model

SHAPE_R = 256
SHAPE_C = 256
NUM_CLASSES = 6

DEFAULT_WEIGHTS = (
    Path(__file__).resolve().parent.parent
    / "ueyes_smoketest"
    / "weights_dl"
    / "model_weights"
    / "saliency_models"
    / "UMSI++"
    / "umsi++.hdf5"
)


# ---------------------------------------------------------------------------
# Custom Xception (stride-1 in blocks 4 / 13 / 13_pool — 256x256 -> 32x32)
# ---------------------------------------------------------------------------
def _build_custom_xception(input_tensor):
    x = layers.Conv2D(32, (3, 3), strides=(2, 2), use_bias=False, name="block1_conv1")(input_tensor)
    x = layers.BatchNormalization(name="block1_conv1_bn")(x)
    x = layers.Activation("relu", name="block1_conv1_act")(x)
    x = layers.Conv2D(64, (3, 3), use_bias=False, name="block1_conv2")(x)
    x = layers.BatchNormalization(name="block1_conv2_bn")(x)
    x = layers.Activation("relu", name="block1_conv2_act")(x)

    residual = layers.Conv2D(128, (1, 1), strides=(2, 2), padding="same", use_bias=False, name="conv2d_1")(x)
    residual = layers.BatchNormalization(name="batch_normalization_1")(residual)
    x = layers.SeparableConv2D(128, (3, 3), padding="same", use_bias=False, name="block2_sepconv1")(x)
    x = layers.BatchNormalization(name="block2_sepconv1_bn")(x)
    x = layers.Activation("relu", name="block2_sepconv2_act")(x)
    x = layers.SeparableConv2D(128, (3, 3), padding="same", use_bias=False, name="block2_sepconv2")(x)
    x = layers.BatchNormalization(name="block2_sepconv2_bn")(x)
    x = layers.MaxPooling2D((3, 3), strides=(2, 2), padding="same", name="block2_pool")(x)
    x = layers.add([x, residual])

    residual = layers.Conv2D(256, (1, 1), strides=(2, 2), padding="same", use_bias=False, name="conv2d_2")(x)
    residual = layers.BatchNormalization(name="batch_normalization_2")(residual)
    x = layers.Activation("relu", name="block3_sepconv1_act")(x)
    x = layers.SeparableConv2D(256, (3, 3), padding="same", use_bias=False, name="block3_sepconv1")(x)
    x = layers.BatchNormalization(name="block3_sepconv1_bn")(x)
    x = layers.Activation("relu", name="block3_sepconv2_act")(x)
    x = layers.SeparableConv2D(256, (3, 3), padding="same", use_bias=False, name="block3_sepconv2")(x)
    x = layers.BatchNormalization(name="block3_sepconv2_bn")(x)
    x = layers.MaxPooling2D((3, 3), strides=(2, 2), padding="same", name="block3_pool")(x)
    x = layers.add([x, residual])

    # Block 4 — UMSI++ stride (2,2) -> (1,1)
    residual = layers.Conv2D(728, (1, 1), strides=(1, 1), padding="same", use_bias=False, name="conv2d_3")(x)
    residual = layers.BatchNormalization(name="batch_normalization_3")(residual)
    x = layers.Activation("relu", name="block4_sepconv1_act")(x)
    x = layers.SeparableConv2D(728, (3, 3), padding="same", use_bias=False, name="block4_sepconv1")(x)
    x = layers.BatchNormalization(name="block4_sepconv1_bn")(x)
    x = layers.Activation("relu", name="block4_sepconv2_act")(x)
    x = layers.SeparableConv2D(728, (3, 3), padding="same", use_bias=False, name="block4_sepconv2")(x)
    x = layers.BatchNormalization(name="block4_sepconv2_bn")(x)
    x = layers.MaxPooling2D((3, 3), strides=(1, 1), padding="same", name="block4_pool")(x)
    x = layers.add([x, residual])

    for i in range(8):
        residual = x
        prefix = "block" + str(i + 5)
        x = layers.Activation("relu", name=prefix + "_sepconv1_act")(x)
        x = layers.SeparableConv2D(728, (3, 3), padding="same", use_bias=False, name=prefix + "_sepconv1")(x)
        x = layers.BatchNormalization(name=prefix + "_sepconv1_bn")(x)
        x = layers.Activation("relu", name=prefix + "_sepconv2_act")(x)
        x = layers.SeparableConv2D(728, (3, 3), padding="same", use_bias=False, name=prefix + "_sepconv2")(x)
        x = layers.BatchNormalization(name=prefix + "_sepconv2_bn")(x)
        x = layers.Activation("relu", name=prefix + "_sepconv3_act")(x)
        x = layers.SeparableConv2D(728, (3, 3), padding="same", use_bias=False, name=prefix + "_sepconv3")(x)
        x = layers.BatchNormalization(name=prefix + "_sepconv3_bn")(x)
        x = layers.add([x, residual])

    # Block 13 — UMSI++ stride (2,2) -> (1,1)
    residual = layers.Conv2D(1024, (1, 1), strides=(1, 1), padding="same", use_bias=False, name="conv2d_4")(x)
    residual = layers.BatchNormalization(name="batch_normalization_4")(residual)
    x = layers.Activation("relu", name="block13_sepconv1_act")(x)
    x = layers.SeparableConv2D(728, (3, 3), padding="same", use_bias=False, name="block13_sepconv1")(x)
    x = layers.BatchNormalization(name="block13_sepconv1_bn")(x)
    x = layers.Activation("relu", name="block13_sepconv2_act")(x)
    x = layers.SeparableConv2D(1024, (3, 3), padding="same", use_bias=False, name="block13_sepconv2")(x)
    x = layers.BatchNormalization(name="block13_sepconv2_bn")(x)
    x = layers.MaxPooling2D((3, 3), strides=(1, 1), padding="same", name="block13_pool")(x)
    x = layers.add([x, residual])

    x = layers.SeparableConv2D(1536, (3, 3), padding="same", use_bias=False, name="block14_sepconv1")(x)
    x = layers.BatchNormalization(name="block14_sepconv1_bn")(x)
    x = layers.Activation("relu", name="block14_sepconv1_act")(x)
    x = layers.SeparableConv2D(2048, (3, 3), padding="same", use_bias=False, name="block14_sepconv2")(x)
    x = layers.BatchNormalization(name="block14_sepconv2_bn")(x)
    x = layers.Activation("relu", name="block14_sepconv2_act")(x)
    return x


def _build_umsi(input_shape=(SHAPE_R, SHAPE_C, 3)):
    import tensorflow as tf

    inp = keras.Input(shape=input_shape)
    xc_out = _build_custom_xception(inp)

    # ASPP
    c0 = layers.Conv2D(256, (1, 1), padding="same", use_bias=False, name="aspp_csep0")(xc_out)
    c6 = layers.DepthwiseConv2D((3, 3), dilation_rate=(6, 6), padding="same", use_bias=False, name="aspp_csepd6_depthwise")(xc_out)
    c12 = layers.DepthwiseConv2D((3, 3), dilation_rate=(12, 12), padding="same", use_bias=False, name="aspp_csepd12_depthwise")(xc_out)
    c18 = layers.DepthwiseConv2D((3, 3), dilation_rate=(18, 18), padding="same", use_bias=False, name="aspp_csepd18_depthwise")(xc_out)
    c6 = layers.BatchNormalization(name="aspp_csepd6_depthwise_BN")(c6)
    c12 = layers.BatchNormalization(name="aspp_csepd12_depthwise_BN")(c12)
    c18 = layers.BatchNormalization(name="aspp_csepd18_depthwise_BN")(c18)
    c6 = layers.Activation("relu", name="activation_2")(c6)
    c12 = layers.Activation("relu", name="activation_4")(c12)
    c18 = layers.Activation("relu", name="activation_6")(c18)
    c6 = layers.Conv2D(256, (1, 1), padding="same", use_bias=False, name="aspp_csepd6_pointwise")(c6)
    c12 = layers.Conv2D(256, (1, 1), padding="same", use_bias=False, name="aspp_csepd12_pointwise")(c12)
    c18 = layers.Conv2D(256, (1, 1), padding="same", use_bias=False, name="aspp_csepd18_pointwise")(c18)
    c0 = layers.BatchNormalization(name="aspp0_BN")(c0)
    c6 = layers.BatchNormalization(name="aspp_csepd6_pointwise_BN")(c6)
    c12 = layers.BatchNormalization(name="aspp_csepd12_pointwise_BN")(c12)
    c18 = layers.BatchNormalization(name="aspp_csepd18_pointwise_BN")(c18)
    c0 = layers.Activation("relu", name="aspp0_activation")(c0)
    c6 = layers.Activation("relu", name="activation_3")(c6)
    c12 = layers.Activation("relu", name="activation_5")(c12)
    c18 = layers.Activation("relu", name="activation_7")(c18)
    concat1 = layers.Concatenate(name="concatenate_1")([c0, c6, c12, c18])

    # Classifier head
    x = layers.Conv2D(256, (3, 3), strides=(3, 3), padding="same", use_bias=False, name="global_conv")(xc_out)
    x = layers.BatchNormalization(name="global_BN")(x)
    x = layers.Activation("relu", name="activation_1")(x)
    x = layers.Dropout(0.3, name="dropout_1")(x)
    x = layers.GlobalAveragePooling2D(name="global_average_pooling2d_1")(x)
    x = layers.Dense(256, name="global_dense")(x)
    classif = layers.Dropout(0.3, name="dropout_2")(x)
    out_classif = layers.Dense(NUM_CLASSES, activation="softmax", name="out_classif")(classif)

    # Fuse class info back into the spatial stream
    x = layers.Dense(256, name="dense_fusion")(classif)

    def lambda_layer_function(x):
        x = tf.reshape(x, (tf.shape(x)[0], 1, 1, 256))
        con = tf.concat([x for _ in range(32)], axis=1)
        con = tf.concat([con for _ in range(32)], axis=2)
        return con

    x = layers.Lambda(lambda_layer_function, name="lambda_1")(x)
    concat2 = layers.Concatenate(name="concatenate_2")([concat1, x])

    # Decoder
    x = layers.Conv2D(256, (1, 1), padding="same", use_bias=False, name="concat_projection")(concat2)
    x = layers.BatchNormalization(name="concat_projection_BN")(x)
    x = layers.Activation("relu", name="activation_8")(x)
    x = layers.Dropout(0.3, name="dropout_3")(x)
    x = layers.Conv2D(256, (3, 3), padding="same", use_bias=False, name="dec_c1")(x)
    x = layers.Conv2D(256, (3, 3), padding="same", use_bias=False, name="dec_c2")(x)
    x = layers.Dropout(0.3, name="dec_dp1")(x)
    x = layers.UpSampling2D(size=(2, 2), interpolation="bilinear", name="dec_ups1")(x)
    x = layers.Conv2D(128, (3, 3), padding="same", use_bias=False, name="dec_c3")(x)
    x = layers.Conv2D(128, (3, 3), padding="same", use_bias=False, name="dec_c4")(x)
    x = layers.Dropout(0.3, name="dec_dp2")(x)
    x = layers.UpSampling2D(size=(2, 2), interpolation="bilinear", name="dec_ups2")(x)
    x = layers.Conv2D(64, (3, 3), padding="same", use_bias=False, name="dec_c5")(x)
    x = layers.Dropout(0.3, name="dec_dp3")(x)
    x = layers.UpSampling2D(size=(4, 4), interpolation="bilinear", name="dec_ups3")(x)
    out_heatmap = layers.Conv2D(1, (1, 1), padding="same", use_bias=False, name="dec_c_cout")(x)

    return Model(inp, [out_heatmap, out_classif], name="umsi_pp")


# ---------------------------------------------------------------------------
# Preprocess / postprocess
# ---------------------------------------------------------------------------
def _padding(img, shape_r, shape_c, channels=3):
    img_padded = np.zeros((shape_r, shape_c, channels), dtype=np.uint8)
    h, w = img.shape[:2]
    rows_rate = h / shape_r
    cols_rate = w / shape_c
    if rows_rate > cols_rate:
        new_cols = (w * shape_r) // h
        img = cv2.resize(img, (new_cols, shape_r))
        new_cols = min(new_cols, shape_c)
        off = (shape_c - new_cols) // 2
        img_padded[:, off:off + new_cols] = img[:, :new_cols]
    else:
        new_rows = (h * shape_c) // w
        img = cv2.resize(img, (shape_c, new_rows))
        new_rows = min(new_rows, shape_r)
        off = (shape_r - new_rows) // 2
        img_padded[off:off + new_rows, :] = img[:new_rows, :]
    return img_padded


def _preprocess(path: Path, shape_r=SHAPE_R, shape_c=SHAPE_C):
    img = cv2.imread(str(path))
    if img is None:
        raise ValueError(f"Unreadable image: {path}")
    padded = _padding(img, shape_r, shape_c, 3).astype(np.float32)
    # VGG-style BGR mean subtraction
    padded[..., 0] -= 103.939
    padded[..., 1] -= 116.779
    padded[..., 2] -= 123.68
    return padded[None], img.shape


def _undo_padding_and_resize(heatmap: np.ndarray, orig_h: int, orig_w: int) -> np.ndarray:
    h256 = cv2.resize(heatmap, (SHAPE_C, SHAPE_R))
    rows_rate = orig_h / SHAPE_R
    cols_rate = orig_w / SHAPE_C
    if rows_rate > cols_rate:
        new_cols = (orig_w * SHAPE_R) // orig_h
        off = (SHAPE_C - new_cols) // 2
        cropped = h256[:, off:off + new_cols]
    else:
        new_rows = (orig_h * SHAPE_C) // orig_w
        off = (SHAPE_R - new_rows) // 2
        cropped = h256[off:off + new_rows, :]
    return cv2.resize(cropped, (orig_w, orig_h))


# ---------------------------------------------------------------------------
# Public class
# ---------------------------------------------------------------------------
class UMSIPP:
    """UMSI++ saliency model. Build + load weights once; call `.heatmap()` per image."""

    def __init__(self, weights: Path | str | None = None):
        weights = Path(weights) if weights else DEFAULT_WEIGHTS
        if not weights.exists():
            raise FileNotFoundError(f"UMSI++ weights not found: {weights}")
        print(f"[umsi++] building model …")
        self._model = _build_umsi()
        print(f"[umsi++] loading weights from {weights}")
        # by_name + skip_mismatch: stock-Xception ImageNet sub-weights are
        # overwritten by umsi++.hdf5 anyway; any name skews silently skip.
        self._model.load_weights(str(weights), by_name=True, skip_mismatch=True)
        self.weights_path = weights

    def heatmap(self, image_path: Path | str) -> np.ndarray:
        """Return a float32 saliency map at the source image's native resolution."""
        image_path = Path(image_path)
        x, orig_shape = _preprocess(image_path)
        H, W = orig_shape[:2]
        heat, _classif = self._model.predict(x, verbose=0)
        heat = np.squeeze(heat).astype(np.float32)
        return _undo_padding_and_resize(heat, H, W)

    def heatmap_and_class(self, image_path: Path | str):
        """Same as heatmap() but also returns the 6-class classifier probs."""
        image_path = Path(image_path)
        x, orig_shape = _preprocess(image_path)
        H, W = orig_shape[:2]
        heat, classif = self._model.predict(x, verbose=0)
        heat = np.squeeze(heat).astype(np.float32)
        return _undo_padding_and_resize(heat, H, W), classif[0]

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
