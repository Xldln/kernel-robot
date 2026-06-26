"""SigLIP FastAPI Controller"""

from __future__ import annotations

import base64

import numpy as np
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse

from mindbridge.src.core.schemas.SiglipEntity import PredictRequest, PredictResponse
from mindbridge.src.core.service.SiglipInfer import SiglipInfer

infer_router = APIRouter(prefix="/infer", tags=["SigLIP Inference"])

infer_engine: SiglipInfer | None = None
_ema_state: np.ndarray | None = None  # 相似度 EMA 状态，跨请求持续累积


def init_engine(config_path: str = "/workspace/mindbridge/src/core/config/siglip-config.yaml"):
    """启动时初始化 SigLIP 模型。"""
    global infer_engine
    print(f"Loading SigLIP model from config: {config_path}")
    infer_engine = SiglipInfer(config_path)
    return infer_engine


def _do_predict(req: PredictRequest) -> PredictResponse:
    """执行推理并维护 EMA 状态。"""
    global _ema_state
    result, new_ema = infer_engine.predict(req, ema_state=_ema_state)
    _ema_state = new_ema
    return result


# ── raw bytes 端点（推荐，无 base64 开销） ──────────────────────

@infer_router.post("/predict/raw")
async def predict_raw(
    request_id: str = Form(default="", description="请求 ID"),
    image: UploadFile = File(..., description="RGB 图像（JPEG/PNG 二进制）"),
):
    """SigLIP 状态分类推理（raw bytes 传输，无 base64 开销）。

    接收 multipart/form-data 中的原始 JPEG/PNG 图像字节，
    返回 JSON 格式的分类结果。
    """
    if infer_engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    # 读取上传的原始图像字节
    image_bytes = await image.read()

    # 编码为 base64 以复用现有推理管线
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    req = PredictRequest(request_id=request_id, image_b64=image_b64)
    result = _do_predict(req)

    # 返回 JSON 响应（client.classify_state() 期望 r.json()）
    return JSONResponse(content=result.model_dump())


# ── base64 端点（保留向后兼容） ────────────────────────────────

@infer_router.post("/predict", response_model=PredictResponse)
async def predict(body: PredictRequest):
    """base64 图片推理（特征匹配）。"""
    if infer_engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return _do_predict(body)


@infer_router.post("/predict/file", response_model=PredictResponse)
async def predict_file(
    file: UploadFile = File(...),
):
    """上传图片文件推理。"""
    if infer_engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    image_bytes = await file.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    req = PredictRequest(image_b64=image_b64)
    return _do_predict(req)
