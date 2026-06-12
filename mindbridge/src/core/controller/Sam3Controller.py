"""SAM3 目标检测 / 分割 FastAPI Controller"""

from __future__ import annotations

import base64
import json as _json
from io import BytesIO

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import Response
from PIL import Image

from mindbridge.src.core.schemas.Sam3Entity import (
    Sam3PredictRequest,
    Sam3PredictResponse,
)
from mindbridge.src.core.service.Sam3Infer import Sam3Infer
from mindbridge.src.core.tool.multipart import build_multipart_response

infer_router = APIRouter(prefix="/infer", tags=["SAM3"])

infer_engine: Sam3Infer | None = None


def init_engine(config_path: str = "/workspace/mindbridge/src/core/config/sam3-config.yaml"):
    """启动时初始化 SAM3 模型。"""
    global infer_engine
    print(f"Loading SAM3 model from config: {config_path}")
    infer_engine = Sam3Infer(config_path)
    return infer_engine


# ── raw bytes 端点（推荐，无 base64 开销） ─────────────────────────

@infer_router.post("/detect/raw")
async def detect_raw(
    image: UploadFile = File(..., description="RGB 图像文件（JPEG/PNG）"),
    prompts: str | None = Form(default=None, description="文本提示，逗号分隔；不传则使用配置默认值"),
    score_threshold: float | None = Form(None, ge=0.0, le=1.0),
    request_id: str = Form(default=""),
):
    """Raw bytes 目标检测 / 分割推理（无 base64 开销）。

    返回 multipart/mixed：JSON 检测结果 + 掩码 PNG。
    """
    if infer_engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    image_bytes = await image.read()
    pil_image = Image.open(BytesIO(image_bytes)).convert("RGB")
    prompt_list = [p.strip() for p in prompts.split(",") if p.strip()] if prompts else None

    result = infer_engine.predict_from_pil(
        pil_image,
        prompts=prompt_list,
        score_threshold=score_threshold,
        request_id=request_id,
    )

    if result["status"] == "error":
        headers = {
            "X-Status": "error",
            "X-Error-Message": result.get("message", "unknown error"),
            "X-Elapsed-Sec": str(result.get("elapsed_sec", 0)),
        }
        return Response(content=b"", media_type="text/plain", headers=headers, status_code=500)

    # 构建 multipart/mixed 响应
    json_part = {
        "status": result["status"],
        "request_id": result["request_id"],
        "detections": result["detections"],
        "elapsed_sec": result["elapsed_sec"],
    }
    binary_parts: list[tuple[str, bytes, str]] = []
    for name, mask_data in result.get("mask_bytes", {}).items():
        binary_parts.append((name, mask_data, "image/png"))

    body, content_type = build_multipart_response(
        json_part=json_part,
        binary_parts=binary_parts,
    )

    headers = {
        "X-Status": "ok",
        "X-Elapsed-Sec": str(result.get("elapsed_sec", 0)),
    }
    return Response(content=body, media_type=content_type, headers=headers)


# ── base64 端点（保留向后兼容） ────────────────────────────────────

@infer_router.post("/detect", response_model=Sam3PredictResponse)
async def detect(body: Sam3PredictRequest):
    """目标检测 / 分割推理（base64 图片）。"""
    if infer_engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return infer_engine.predict(body)


@infer_router.post("/detect/file", response_model=Sam3PredictResponse)
async def detect_file(
    file: UploadFile = File(..., description="RGB 图像文件"),
    prompts: str = Form(..., description="文本提示，逗号分隔，如 'cat,dog'"),
    score_threshold: float | None = Form(None, ge=0.0, le=1.0),
):
    """目标检测 / 分割推理（文件上传）。"""
    if infer_engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    import base64 as _b64
    image_bytes = await file.read()
    image_b64 = _b64.b64encode(image_bytes).decode("utf-8")
    prompt_list = [p.strip() for p in prompts.split(",") if p.strip()]

    req = Sam3PredictRequest(
        image_b64=image_b64,
        prompts=prompt_list,
        score_threshold=score_threshold,
    )
    return infer_engine.predict(req)
