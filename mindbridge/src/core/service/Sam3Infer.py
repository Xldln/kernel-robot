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
        self.default_prompts = [
            str(prompt).strip()
            for prompt in sam3_cfg.get("prompts", ["object"])
            if str(prompt).strip()
        ] or ["object"]

        # ── 加载模型 ──
        print(f"[Sam3Infer] 代码库: {code_base}")
        print(f"[Sam3Infer] 模型路径: {self.checkpoint_path}")
        print(f"[Sam3Infer] 默认提示词: {self.default_prompts}")
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
        box_prompts: dict[str, list[float]] | None = None,
    ) -> dict:
        """直接接受 PIL Image 推理（无 base64 开销）。

        Args:
            prompts: 文本提示列表
            box_prompts: {label: [x1, y1, x2, y2]} 用于 box-prompt 追踪，比文本匹配更鲁棒

        Returns:
            dict with keys: status, request_id, detections (list of dicts),
            mask_bytes (dict of {name: bytes}), elapsed_sec
        """
        import cv2
        t_start = time.time()

        if not prompts and not box_prompts:
            prompts = self.default_prompts

        try:
            _threshold = score_threshold if score_threshold is not None else self.score_threshold

            # 提取图像特征（只做一次）
            inference_state = self.processor.set_image(image)
            img_h = inference_state["original_height"]
            img_w = inference_state["original_width"]

            detections: list[dict] = []
            mask_bytes_dict: dict[str, bytes] = {}
            global_det_id = 1

            # ── 文本 prompt 检测 ──
            text_prompts = prompts or []
            for prompt in text_prompts:
                self.processor.reset_all_prompts(inference_state)
                output = self.processor.set_text_prompt(prompt=prompt, state=inference_state)
                self._extract_detections(
                    output, str(prompt), _threshold, global_det_id,
                    detections, mask_bytes_dict,
                )
                global_det_id = len(detections) + 1

            # ── box prompt 检测（追踪模式，不依赖文本匹配）──
            if box_prompts:
                for label, bbox in box_prompts.items():
                    if len(bbox) != 4:
                        continue
                    # [x1, y1, x2, y2] → [cx, cy, w, h] normalized to [0, 1]
                    cx = (bbox[0] + bbox[2]) / 2.0 / img_w
                    cy = (bbox[1] + bbox[3]) / 2.0 / img_h
                    w = max((bbox[2] - bbox[0]) / img_w, 0.01)
                    h = max((bbox[3] - bbox[1]) / img_h, 0.01)
                    box_norm = [cx, cy, w, h]

                    self.processor.reset_all_prompts(inference_state)
                    output = self.processor.add_geometric_prompt(
                        box=box_norm, label=True, state=inference_state,
                    )
                    self._extract_detections(
                        output, label, _threshold, global_det_id,
                        detections, mask_bytes_dict,
                    )
                    global_det_id = len(detections) + 1

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

    def _extract_detections(self, output: dict, label: str, threshold: float,
                            start_id: int, detections: list, mask_bytes_dict: dict):
        """Extract masks/boxes/scores from a processor output into detections list."""
        import cv2

        current_masks = output["masks"].cpu().numpy()
        current_boxes = output["boxes"].cpu().numpy()
        current_scores = output["scores"].cpu().numpy()

        for i in range(len(current_scores)):
            score = float(current_scores[i])
            if score <= threshold:
                continue

            box = current_boxes[i]
            mask = current_masks[i].squeeze()

            binary_mask = (mask > 0.5).astype(np.uint8) * 255
            ok, png_buf = cv2.imencode(".png", binary_mask, [cv2.IMWRITE_PNG_COMPRESSION, 3])
            det_id = start_id + len(detections)
            mask_name = f"mask_{det_id - 1}"
            if ok:
                mask_bytes_dict[mask_name] = png_buf.tobytes()

            detections.append({
                "id": det_id,
                "label": label,
                "score": score,
                "bbox": [float(v) for v in box.tolist()],
                "mask_file": mask_name if ok else "",
            })
