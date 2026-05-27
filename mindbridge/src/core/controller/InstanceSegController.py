
from __future__ import annotations

import base64

import numpy as np
from fastapi import APIRouter, HTTPException, UploadFile, File, Form

from mindbridge.src.core.schemas.YoloEntity import PredictRequest, PredictResponse
from mindbridge.src.core.service.InstanceSegmentInfer import YOLOInfer

infer_router = APIRouter(prefix="/infer", tags=["YOLO Inference"])

infer_engine: YOLOInfer | None = None


def init_engine(config_path: str = "/workspace/mindbridge/src/core/config/yolo-config.yaml"):
    """启动时初始化 YOLO 模型。"""
    global infer_engine
    print(f"Loading YOLO model from config: {config_path}")
    infer_engine = YOLOInfer(config_path)
    return infer_engine


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
