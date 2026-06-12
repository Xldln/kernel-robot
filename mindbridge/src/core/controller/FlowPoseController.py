"""FlowPose 6D姿态估计 FastAPI Controller"""

from __future__ import annotations

import base64
import cv2
import json as _json
import numpy as np

from fastapi import APIRouter, HTTPException, UploadFile, File, Form

from mindbridge.src.core.schemas.FlowPoseEntity import (
    FlowPosePredictRequest,
    FlowPosePredictResponse,
)
from mindbridge.src.core.service.FlowPoseInfer import FlowPoseInfer

infer_router = APIRouter(prefix="/infer", tags=["FlowPose"])

infer_engine: FlowPoseInfer | None = None


def init_engine(config_path: str = "/workspace/mindbridge/src/core/config/flowpose-config.yaml"):
    """启动时初始化 FlowPose 模型。"""
    global infer_engine
    print(f"Loading FlowPose model from config: {config_path}")
    infer_engine = FlowPoseInfer(config_path)
    return infer_engine


def _bytes_to_array(data: bytes, flags: int) -> np.ndarray:
    arr = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(arr, flags)
    if img is None:
        raise ValueError("Failed to decode image from bytes")
    return img


@infer_router.post("/visualization")
def set_visualization(enabled: bool = True):
    """Enable or disable the OpenCV visualization window without restarting FlowPose."""
    if infer_engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    if enabled:
        infer_engine.visualize = True
    else:
        infer_engine.close_visualization()
    return {"status": "ok", "visualize": infer_engine.visualize}


# ── raw bytes 端点（推荐，无 base64 开销） ─────────────────────────

@infer_router.post("/pose/raw", response_model=FlowPosePredictResponse)
async def predict_pose_raw(
    rgb_file: UploadFile = File(..., description="RGB 图像文件（JPEG/PNG）"),
    depth_file: UploadFile = File(..., description="深度图像文件 (16-bit PNG)"),
    mask_file: UploadFile = File(..., description="实例分割掩码文件 (PNG)"),
    obj_ids_json: str = Form(default="[]", description="物体 ID 列表，JSON 数组"),
    class_names_csv: str = Form(default="", description="类别名称，逗号分隔"),
    instance_names_csv: str = Form(default="", description="实例名称，逗号分隔"),
    request_id: str = Form(default=""),
):
    """Raw bytes 6D 姿态估计推理（无 base64 开销）。

    接受 multipart/form-data 三通道图像原始字节，返回 JSON 位姿结果。
    """
    if infer_engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    rgb_bytes = await rgb_file.read()
    depth_bytes = await depth_file.read()
    mask_bytes = await mask_file.read()

    rgb = _bytes_to_array(rgb_bytes, cv2.IMREAD_COLOR).astype(np.uint8)
    depth = _bytes_to_array(depth_bytes, cv2.IMREAD_ANYDEPTH).astype(np.float32)
    combined_mask = _bytes_to_array(mask_bytes, cv2.IMREAD_GRAYSCALE).astype(np.uint8)

    try:
        obj_ids = _json.loads(obj_ids_json)
    except Exception:
        obj_ids = []

    class_names = [n.strip() for n in class_names_csv.split(",") if n.strip()]
    instance_names = [n.strip() for n in instance_names_csv.split(",") if n.strip()]

    return infer_engine.predict_from_arrays(
        rgb, depth, combined_mask,
        obj_ids=obj_ids,
        class_names=class_names,
        instance_names=instance_names,
        request_id=request_id,
    )


# ── base64 端点（保留向后兼容） ────────────────────────────────────

@infer_router.post("/pose", response_model=FlowPosePredictResponse)
async def predict_pose(body: FlowPosePredictRequest):
    """6D 姿态估计推理（base64 三通道图像）。"""
    if infer_engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return infer_engine.predict(body)


@infer_router.post("/pose/file", response_model=FlowPosePredictResponse)
async def predict_pose_file(
    rgb_file: UploadFile = File(..., description="RGB 图像文件"),
    depth_file: UploadFile = File(..., description="深度图像文件 (16-bit PNG)"),
    mask_file: UploadFile = File(..., description="实例分割掩码文件"),
    obj_ids_json: str = Form(default="[]", description="物体 ID 列表，JSON 数组"),
    class_names_csv: str = Form(default="", description="类别名称，逗号分隔"),
    instance_names_csv: str = Form(default="", description="实例名称，逗号分隔"),
):
    """6D 姿态估计推理（文件上传，三通道图像）。"""
    if infer_engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    rgb_bytes = await rgb_file.read()
    depth_bytes = await depth_file.read()
    mask_bytes = await mask_file.read()

    rgb = _bytes_to_array(rgb_bytes, cv2.IMREAD_COLOR).astype(np.uint8)
    depth = _bytes_to_array(depth_bytes, cv2.IMREAD_ANYDEPTH).astype(np.float32)
    combined_mask = _bytes_to_array(mask_bytes, cv2.IMREAD_GRAYSCALE).astype(np.uint8)

    try:
        obj_ids = _json.loads(obj_ids_json)
    except Exception:
        obj_ids = []

    class_names = [n.strip() for n in class_names_csv.split(",") if n.strip()]
    instance_names = [n.strip() for n in instance_names_csv.split(",") if n.strip()]

    return infer_engine.predict_from_arrays(
        rgb, depth, combined_mask,
        obj_ids=obj_ids,
        class_names=class_names,
        instance_names=instance_names,
    )
