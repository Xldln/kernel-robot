"""LAST-ViT FastAPI Controller"""

from __future__ import annotations

import base64

import numpy as np
from fastapi import APIRouter, HTTPException, UploadFile, File, Form

from mindbridge.src.core.schemas.LastvitEntity import PredictRequest, PredictResponse
from mindbridge.src.core.service.LastvitInfer import LastvitInfer
from mindbridge.src.core.tool.LastvitTools import decode_image_b64_to_bgr

infer_router = APIRouter(prefix="/infer", tags=["LAST-ViT Inference"])

infer_engine: LastvitInfer | None = None


def init_engine(config_path: str = "/workspace/mindbridge/src/core/config/last-vit-config.yaml"):
    """启动时初始化 LAST-ViT 模型。"""
    global infer_engine
    print(f"Loading LAST-ViT model from config: {config_path}")
    infer_engine = LastvitInfer(config_path)
    return infer_engine


@infer_router.post("/predict", response_model=PredictResponse)
async def predict(body: PredictRequest):
    """base64 图片推理（特征匹配）。"""
    if infer_engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return infer_engine.predict(body)


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
    return infer_engine.predict(req)
