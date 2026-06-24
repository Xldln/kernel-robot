"""SAM3 工具函数（纯函数，无副作用）"""

from __future__ import annotations

import base64
import io

import cv2
import numpy as np
from PIL import Image


# ── 图像编解码 ───────────────────────────────────────────────────

def decode_rgb_from_base64(image_b64: str) -> Image.Image:
    """从 base64 字符串解码为 PIL RGB Image"""
    image_data = base64.b64decode(image_b64)
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    return image


def decode_numpy_rgb_from_base64(image_b64: str) -> np.ndarray:
    """从 base64 字符串解码为 RGB numpy 数组"""
    image = decode_rgb_from_base64(image_b64)
    return np.array(image)


def encode_mask_to_base64_png(mask: np.ndarray) -> str:
    """将二值掩码编码为 base64 PNG 字符串"""
    if mask.dtype != np.uint8:
        mask = mask.astype(np.uint8)
    success, buf = cv2.imencode(".png", mask, [cv2.IMWRITE_PNG_COMPRESSION, 3])
    if not success:
        raise RuntimeError("Failed to encode mask to PNG.")
    return base64.b64encode(buf.tobytes()).decode("utf-8")
