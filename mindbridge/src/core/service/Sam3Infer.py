"""SAM3 目标检测 / 分割 推理服务封装"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import torch
import yaml

from mindbridge.src.core.schemas.Sam3Entity import (
    Detection,
    Sam3PredictRequest,
    Sam3PredictResponse,
)
from mindbridge.src.core.tool.Sam3Tools import (
    decode_rgb_from_base64,
    encode_mask_to_base64_png,
)


def _load_config(config_path: str | Path) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


class Sam3Infer:
    """SAM3 目标检测 / 分割 推理引擎"""

    def __init__(self, config_path: str | Path = "/workspace/mindbridge/src/core/config/sam3-config.yaml"):
        cfg = _load_config(config_path)
        sam3_cfg = cfg.get("sam3", {})

        # ── 代码库路径 ──
        code_base = sam3_cfg.get("code_base", "/workspace/mindbridge/models/sam3-main")
        if code_base and code_base not in sys.path:
            sys.path.insert(0, code_base)

        # ── 模型参数 ──
        self.checkpoint_path = sam3_cfg["checkpoint_path"]
        self.score_threshold = float(sam3_cfg.get("score_threshold", 0.4))

        # ── 加载模型 ──
        print(f"[Sam3Infer] 代码库: {code_base}")
        print(f"[Sam3Infer] 模型路径: {self.checkpoint_path}")
        print(f"[Sam3Infer] 置信度阈值: {self.score_threshold}")

        t0 = time.time()
        self.model, self.processor = self._load_model()
        print(f"[Sam3Infer] 模型加载完成 ({time.time() - t0:.2f}s)")

    # ── 模型加载 ────────────────────────────────────────────────

    def _load_model(self):
        """加载 SAM3 模型和处理器"""
        from sam3.model_builder import build_sam3_image_model
        from sam3.model.sam3_image_processor import Sam3Processor

        model = build_sam3_image_model(
            checkpoint_path=self.checkpoint_path,
            load_from_HF=False,
            enable_segmentation=True,
        )
        processor = Sam3Processor(model)
        return model, processor

    # ── 核心推理 ────────────────────────────────────────────────

    def predict(self, req: Sam3PredictRequest) -> Sam3PredictResponse:
        image = decode_rgb_from_base64(req.image_b64)
        score_threshold = req.score_threshold if req.score_threshold is not None else self.score_threshold

        raw_result = self.predict_from_pil(
            image,
            prompts=req.prompts,
            score_threshold=score_threshold,
            request_id=req.request_id,
        )

        if raw_result["status"] == "error":
            return Sam3PredictResponse(
                status="error",
                request_id=req.request_id,
                message=raw_result.get("message", ""),
                elapsed_sec=raw_result["elapsed_sec"],
            )

        # Convert raw bytes back to base64 for backward compat
        detections: list[Detection] = []
        for det_dict in raw_result["detections"]:
            mask_b64 = None
            mask_file = det_dict.get("mask_file", "")
            if mask_file:
                mask_bytes = raw_result.get("mask_bytes", {}).get(mask_file)
                if mask_bytes:
                    import base64 as _b64
                    mask_b64 = _b64.b64encode(mask_bytes).decode("utf-8")
            detections.append(Detection(
                id=det_dict["id"],
                label=det_dict["label"],
                score=det_dict["score"],
                bbox=det_dict.get("bbox", []),
                mask_png_b64=mask_b64,
            ))

        return Sam3PredictResponse(
            status="ok",
            request_id=req.request_id,
            detections=detections,
            elapsed_sec=raw_result["elapsed_sec"],
        )

    def predict_from_pil(
        self,
        image,
        *,
        prompts: list[str] | None = None,
        score_threshold: float | None = None,
        request_id: str = "",
    ) -> dict:
        """直接接受 PIL Image 推理（无 base64 开销）。

        Returns:
            dict with keys: status, request_id, detections (list of dicts),
            mask_bytes (dict of {name: bytes}), elapsed_sec
        """
        import cv2
        t_start = time.time()

        if prompts is None:
            prompts = ["object"]

        try:
            _threshold = score_threshold if score_threshold is not None else self.score_threshold

            # 提取图像特征
            inference_state = self.processor.set_image(image)

            # 遍历 prompts 进行推理
            detections: list[dict] = []
            mask_bytes_dict: dict[str, bytes] = {}
            global_det_id = 1

            for prompt in prompts:
                output = self.processor.set_text_prompt(state=inference_state, prompt=prompt)

                current_masks = output["masks"].cpu().numpy()
                current_boxes = output["boxes"].cpu().numpy()
                current_scores = output["scores"].cpu().numpy()

                for i in range(len(current_scores)):
                    score = float(current_scores[i])
                    if score <= _threshold:
                        continue

                    box = current_boxes[i]
                    mask = current_masks[i].squeeze()

                    # 二值化掩码
                    binary_mask = (mask > 0.5).astype(np.uint8) * 255

                    # Encode mask to PNG bytes
                    ok, png_buf = cv2.imencode(".png", binary_mask, [cv2.IMWRITE_PNG_COMPRESSION, 3])
                    mask_name = f"mask_{global_det_id - 1}"
                    if ok:
                        mask_bytes_dict[mask_name] = png_buf.tobytes()

                    detections.append({
                        "id": global_det_id,
                        "label": str(prompt),
                        "score": score,
                        "bbox": [float(v) for v in box.tolist()],
                        "mask_file": mask_name if ok else "",
                    })
                    global_det_id += 1

            elapsed = round(time.time() - t_start, 4)
            return {
                "status": "ok",
                "request_id": request_id,
                "detections": detections,
                "mask_bytes": mask_bytes_dict,
                "elapsed_sec": elapsed,
            }

        except Exception as e:
            elapsed = round(time.time() - t_start, 4)
            return {
                "status": "error",
                "request_id": request_id,
                "message": str(e),
                "elapsed_sec": elapsed,
            }
