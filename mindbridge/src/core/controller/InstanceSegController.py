
from __future__ import annotations

import base64
from io import BytesIO

import cv2
import numpy as np
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import Response
from PIL import Image

from mindbridge.src.core.schemas.YoloEntity import PredictRequest, PredictResponse
from mindbridge.src.core.service.InstanceSegmentInfer import YOLOInfer
from mindbridge.src.core.tool.multipart import build_multipart_response

infer_router = APIRouter(prefix="/infer", tags=["YOLO Inference"])

infer_engine: YOLOInfer | None = None


def init_engine(config_path: str = "/workspace/mindbridge/src/core/config/yolo-config.yaml"):
    """启动时初始化 YOLO 模型。"""
    global infer_engine
    print(f"Loading YOLO model from config: {config_path}")
    infer_engine = YOLOInfer(config_path)
    return infer_engine


# ── raw bytes 端点（推荐，无 base64 开销） ─────────────────────────

@infer_router.post("/predict/raw")
async def predict_raw(
    image: UploadFile = File(..., description="RGB 图像文件（JPEG/PNG）"),
    request_id: str = Form(default=""),
    conf: float | None = Form(None),
    return_masks: str = Form(default="true"),
    return_annotated_image: str = Form(default="true"),
):
    """Raw bytes 目标检测推理（无 base64 开销）。

    返回 multipart/mixed：JSON 检测结果 + 标注图 + 掩码 PNG。
    """
    if infer_engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    image_bytes = await image.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    _return_masks = return_masks.lower() != "false"
    _return_annotated = return_annotated_image.lower() != "false"

    req = PredictRequest(
        image_b64=image_b64,
        conf=conf,
        return_masks=_return_masks,
        return_annotated_image=_return_annotated,
        request_id=request_id,
    )
    result = infer_engine.predict(req)

    if result.status == "error":
        headers = {
            "X-Status": "error",
            "X-Error-Message": result.message or "unknown error",
            "X-Elapsed-Sec": str(result.elapsed_sec),
        }
        return Response(content=b"", media_type="text/plain", headers=headers, status_code=500)

    # 构建 multipart/mixed 响应
    detections_json = []
    binary_parts: list[tuple[str, bytes, str]] = []

    # 标注图
    if result.annotated_image_b64:
        ann_bytes = base64.b64decode(result.annotated_image_b64)
        binary_parts.append(("annotated", ann_bytes, "image/jpeg"))

    # 掩码图 + 检测结果（添加 mask_file 关联）
    for i, det in enumerate(result.detections):
        det_dict = det.model_dump()
        mask_name = f"mask_{i}"
        if det.mask_png_b64:
            mask_bytes = base64.b64decode(det.mask_png_b64)
            binary_parts.append((mask_name, mask_bytes, "image/png"))
            det_dict["mask_file"] = mask_name
        else:
            det_dict["mask_file"] = ""
        detections_json.append(det_dict)

    json_part = {
        "status": result.status,
        "request_id": result.request_id,
        "num_detections": result.num_detections,
        "detections": detections_json,
        "elapsed_sec": result.elapsed_sec,
    }

    body, content_type = build_multipart_response(
        json_part=json_part,
        binary_parts=binary_parts,
    )

    headers = {
        "X-Status": "ok",
        "X-Elapsed-Sec": str(result.elapsed_sec),
    }
    return Response(content=body, media_type=content_type, headers=headers)


@infer_router.post("/predict", response_model=PredictResponse)
async def predict(body: PredictRequest):
    """base64 图片推理。"""
    if infer_engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return infer_engine.predict(body)


@infer_router.post("/predict/file", response_model=PredictResponse)
async def predict_file(
    file: UploadFile = File(...),
    conf: float | None = Form(None),
    return_masks: bool = Form(True),
    return_annotated_image: bool = Form(True),
):
    """上传图片文件推理。"""
    if infer_engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    image_bytes = await file.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    req = PredictRequest(
        image_b64=image_b64,
        conf=conf,
        return_masks=return_masks,
        return_annotated_image=return_annotated_image,
    )
    return infer_engine.predict(req)
