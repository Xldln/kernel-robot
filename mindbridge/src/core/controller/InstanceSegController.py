from __future__ import annotations

from pathlib import Path

import numpy as np
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel

from mindbridge.src.core.client.InstanceSegment import InstanceSegmentClient
from mindbridge.src.core.schemas.YoloEntity import PredictResponse

instance_router = APIRouter(
    prefix="/instance",
    tags=["Instance Segmentation API"],
)

SERVICE_URL = "http://127.0.0.1:8001"


class PredictFileInput(BaseModel):
    conf: float | None = None
    return_masks: bool = True
    return_annotated_image: bool = True


@instance_router.post("/predict/file", response_model=PredictResponse)
async def predict_from_file(
    file: UploadFile = File(...),
    conf: float | None = Form(None),
    return_masks: bool = Form(True),
    return_annotated_image: bool = Form(True),
):
    """上传图片文件进行 YOLO 推理"""
    image_bytes = await file.read()
    bgr = np.frombuffer(image_bytes, dtype=np.uint8)

    with InstanceSegmentClient(base_url=SERVICE_URL) as client:
        resp = client.predict(
            bgr,
            conf=conf,
            return_masks=return_masks,
            return_annotated_image=return_annotated_image,
        )

    if resp.status == "error":
        raise HTTPException(status_code=500, detail=resp.message)

    return resp


@instance_router.post("/predict", response_model=PredictResponse)
async def predict(body: PredictFileInput):
    """JSON 体推理（base64 图片传入）"""
    raise HTTPException(status_code=501, detail="Not implemented: use /predict/file with multipart upload")
