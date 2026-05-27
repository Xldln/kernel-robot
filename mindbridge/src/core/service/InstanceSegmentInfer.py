from __future__ import annotations

import time
from pathlib import Path

import cv2
import numpy as np
import yaml
from ultralytics import YOLO

from mindbridge.src.core.schemas.YoloEntity import (
    Detection,
    PredictRequest,
    PredictResponse,
)
from mindbridge.src.core.tool.image import (
    decode_bgr_from_base64,
    encode_bgr_to_base64_jpg,
    encode_mask_to_base64_png,
)


def _load_config(config_path: str | Path) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


class YOLOInfer:

    def __init__(self, config_path: str | Path = "/workspace/mindbridge/src/core/config/yolo-config.yaml"):
        cfg = _load_config(config_path)
        yolo_cfg = cfg.get("yolo", {})

        model_path = yolo_cfg.get("model_path")
        self.score_threshold = float(yolo_cfg.get("score_threshold", 0.4))

        print(f"Loading YOLO model: {model_path},and set score_threshold={self.score_threshold}")
        t0 = time.time()
        self.model = YOLO(str(model_path))
        self.model_task = getattr(self.model, "task", "detect")
        print(f"Model loaded ({time.time() - t0:.2f}s), task={self.model_task}")

    def predict(self, req: PredictRequest) -> PredictResponse:
        t_start = time.time()
        request_id = req.request_id
        try:
            bgr = decode_bgr_from_base64(req.image_b64)
            conf = req.conf if req.conf is not None else self.score_threshold
            return_masks = req.return_masks if req.return_masks is not None else True
            return_annotated = req.return_annotated_image if req.return_annotated_image is not None else True
            if self.model_task == "classify":
                results = self.model.predict(bgr, verbose=False, conf=conf)
            else:
                results = self.model.track(
                    bgr,
                    persist=req.persist if req.persist is not None else True,
                    tracker=req.tracker or "bytetrack.yaml",
                    verbose=False,
                    conf=conf,
                )
            result0 = results[0] if results else None
            annotated_bgr = result0.plot() if result0 is not None else bgr.copy()
            annotated_image_b64 = encode_bgr_to_base64_jpg(annotated_bgr) if return_annotated else None
            detections: list[Detection] = []
            det_id = 1
            if self.model_task == "classify":
                detections = self._parse_classify(result0)
            elif result0 is not None and result0.boxes is not None:
                detections = self._parse_detections(result0, bgr, return_masks)

            elapsed = round(time.time() - t_start, 4)
            return PredictResponse(
                status="ok",
                request_id=request_id,
                num_detections=len(detections),
                detections=detections,
                annotated_image_b64=annotated_image_b64,
                elapsed_sec=elapsed,
            )

        except Exception as e:
            elapsed = round(time.time() - t_start, 4)
            return PredictResponse(
                status="error",
                request_id=request_id,
                message=str(e),
                elapsed_sec=elapsed,
            )


    def _parse_classify(self, result0) -> list[Detection]:
        detections: list[Detection] = []
        names = result0.names if hasattr(result0, "names") else self.model.names
        probs = result0.probs if result0 is not None else None
        if probs is None or not hasattr(probs, "top5"):
            return detections
        for class_id, score in zip(probs.top5, probs.top5conf.tolist()):
            class_id = int(class_id)
            label = str(names[class_id]) if isinstance(names, dict) else str(class_id)
            detections.append(Detection(
                id=len(detections) + 1,
                label=label,
                class_name=label,
                class_id=class_id,
                score=float(score),
            ))
        return detections

    def _parse_detections(self, result0, bgr: np.ndarray, return_masks: bool) -> list[Detection]:
        detections: list[Detection] = []
        boxes = result0.boxes
        masks = result0.masks
        names = result0.names if hasattr(result0, "names") else self.model.names

        xyxy = boxes.xyxy.cpu().numpy() if boxes.xyxy is not None else None
        cls = boxes.cls.cpu().numpy() if boxes.cls is not None else None
        scores = boxes.conf.cpu().numpy() if boxes.conf is not None else None
        mask_data = masks.data.cpu().numpy() if (masks is not None and masks.data is not None) else None

        for i in range(len(boxes)):
            class_id = int(cls[i]) if cls is not None else -1
            score = float(scores[i]) if scores is not None else 0.0
            label = str(names[class_id]) if isinstance(names, dict) else str(class_id)

            mask_b64: str | None = None
            if return_masks and mask_data is not None and i < len(mask_data):
                binary = (mask_data[i] > 0.5).astype(np.uint8) * 255
                mask_b64 = encode_mask_to_base64_png(binary)
            elif return_masks and xyxy is not None:
                x1, y1, x2, y2 = [int(round(v)) for v in xyxy[i].tolist()]
                h, w = bgr.shape[:2]
                x1, x2 = max(0, min(x1, w - 1)), max(0, min(x2, w))
                y1, y2 = max(0, min(y1, h - 1)), max(0, min(y2, h))
                if x2 > x1 and y2 > y1:
                    binary = np.zeros((h, w), dtype=np.uint8)
                    binary[y1:y2, x1:x2] = 255
                    mask_b64 = encode_mask_to_base64_png(binary)

            detections.append(Detection(
                id=len(detections) + 1,
                label=label,
                class_name=label,
                class_id=class_id,
                score=score,
                bbox=[float(v) for v in xyxy[i].tolist()] if xyxy is not None else [],
                mask_png_b64=mask_b64,
            ))

        return detections
