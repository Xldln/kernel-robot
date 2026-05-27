
import argparse
import base64
import json
import time
import uuid
from pathlib import Path

import cv2
import numpy as np



def decode_bgr_from_base64(image_b64: str) -> np.ndarray:
    image_data = base64.b64decode(image_b64)
    image_array = np.frombuffer(image_data, dtype=np.uint8)
    image_bgr = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise ValueError("Failed to decode input image from base64.")
    return image_bgr


def encode_mask_to_base64_png(mask: np.ndarray) -> str:
    if mask.dtype != np.uint8:
        mask = mask.astype(np.uint8)
    success, buf = cv2.imencode(".png", mask, [cv2.IMWRITE_PNG_COMPRESSION, 3])
    if not success:
        raise RuntimeError("Failed to encode mask to PNG.")
    return base64.b64encode(buf.tobytes()).decode("utf-8")


def encode_bgr_to_base64_jpg(image_bgr: np.ndarray, quality: int = 90) -> str:
    success, buf = cv2.imencode(".jpg", image_bgr, [cv2.IMWRITE_JPEG_QUALITY, int(quality)])
    if not success:
        raise RuntimeError("Failed to encode image to JPG.")
    return base64.b64encode(buf.tobytes()).decode("utf-8")




def _draw_detections(bgr: np.ndarray, detections: list[dict]) -> np.ndarray:
    canvas = bgr.copy()
    for d in detections:
        bbox = d.get("bbox", [])
        if len(bbox) == 4:
            x1, y1, x2, y2 = [int(v) for v in bbox]
            cv2.rectangle(canvas, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{d.get('label', '?')}: {d.get('score', 0):.2f}"
            cv2.putText(
                canvas, label, (x1, max(y1 - 5, 15)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1,
            )
    return canvas