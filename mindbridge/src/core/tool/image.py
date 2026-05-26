
import argparse
import base64
import json
import time
import uuid
from pathlib import Path

import cv2
import numpy as np



class ImageProcessor:

    def __init__(self, config: dict | None = None):
        self.config = config or {}

    def encode_file_to_base64(path: Path) -> str:
        return base64.b64encode(path.read_bytes()).decode("utf-8")


    def encode_rgb_to_base64_png(image_rgb: np.ndarray) -> str:
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        ok, buffer = cv2.imencode(".png", image_bgr)
        if not ok:
            raise RuntimeError("Failed to encode generated RGB image as PNG.")
        return base64.b64encode(buffer.tobytes()).decode("utf-8")


    def decode_base64_image_to_bgr(image_b64: str) -> np.ndarray:
        image_bytes = base64.b64decode(image_b64)
        array = np.frombuffer(image_bytes, dtype=np.uint8)
        image_bgr = cv2.imdecode(array, cv2.IMREAD_COLOR)
        if image_bgr is None:
            raise RuntimeError("Failed to decode annotated_image_b64.")
        return image_bgr


    def decode_mask_png_b64_to_gray(mask_b64: str) -> np.ndarray:
        mask_bytes = base64.b64decode(mask_b64)
        mask_arr = np.frombuffer(mask_bytes, dtype=np.uint8)
        mask_gray = cv2.imdecode(mask_arr, cv2.IMREAD_GRAYSCALE)
        if mask_gray is None:
            raise RuntimeError("Failed to decode mask_png_b64.")
        return mask_gray


    def draw_mask_overlay(base_bgr: np.ndarray, masks: list[np.ndarray], alpha: float = 0.45) -> np.ndarray:
        overlay = base_bgr.copy()
        rng = np.random.default_rng(2026)
        for mask in masks:
            if mask is None:
                continue
            color = rng.integers(40, 255, size=3, dtype=np.uint8)
            binary = mask > 0
            overlay[binary] = (
                (1.0 - alpha) * overlay[binary].astype(np.float32)
                + alpha * color.astype(np.float32)
            ).astype(np.uint8)
        return overlay


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
    
    def load_or_create_rgb_b64(args: argparse.Namespace) -> str:
        if args.rgb:
            image_path = Path(args.rgb).expanduser().resolve()
            if not image_path.exists():
                raise FileNotFoundError(f"RGB image not found: {image_path}")
            print(f"[INFO] Using RGB file: {image_path}")
            return encode_file_to_base64(image_path)

        rgb = build_dummy_rgb(args.dummy_width, args.dummy_height)
        print(f"[INFO] Using auto-generated RGB image: {args.dummy_width}x{args.dummy_height}")
        return encode_rgb_to_base64_png(rgb)