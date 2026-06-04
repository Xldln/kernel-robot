"""Fast-Foundation Stereo FastAPI Controller"""

from __future__ import annotations

import json

import cv2
import numpy as np
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import Response

from mindbridge.src.core.schemas.FastFoundationEntity import (
    StereoPredictRequest,
    StereoPredictResponse,
)
from mindbridge.src.core.service.FastFoundationInfer import FastFoundationInfer

infer_router = APIRouter(prefix="/infer", tags=["Fast-Foundation Stereo"])

infer_engine: FastFoundationInfer | None = None


def init_engine(config_path: str = "/workspace/mindbridge/src/core/config/fastfoundation-config.yaml"):
    """启动时初始化 Fast-Foundation Stereo 模型。"""
    global infer_engine
    print(f"Loading Fast-Foundation Stereo model from config: {config_path}")
    infer_engine = FastFoundationInfer(config_path)
    return infer_engine


# ── raw bytes 端点（推荐，无 base64 开销） ──────────────────────

@infer_router.post("/stereo/raw")
async def predict_stereo_raw(
    request_id: str = Form(default="", description="请求 ID"),
    left_image: UploadFile = File(..., description="左目图像（JPEG/PNG 二进制）"),
    right_image: UploadFile = File(..., description="右目图像（JPEG/PNG 二进制）"),
    fx: float | None = Form(None),
    fy: float | None = Form(None),
    ppx: float | None = Form(None),
    ppy: float | None = Form(None),
    baseline_m: float | None = Form(None),
    valid_iters: int | None = Form(None),
    z_far: float | None = Form(None),
    remove_invisible: bool | None = Form(None),
    scale: float | None = Form(None),
    return_depth: bool = Form(True),
    return_disparity: bool = Form(False),
    return_color_jpg: bool = Form(False),
    jpg_quality: int = Form(90),
):
    """双目深度估计推理（raw bytes 传输，无 base64 开销）。

    返回 depth 为 PNG 格式的 uint16 毫米深度图原始字节。
    元数据通过 HTTP headers 返回：
    - X-Status: ok / error
    - X-Depth-Shape: JSON 数组 [H, W]
    - X-Elapsed-Sec: 推理耗时
    - X-Request-Id: 请求 ID
    - X-Error-Message: 错误信息（仅 error 时）
    """
    if infer_engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    # 读取上传的二进制图像
    left_bytes = await left_image.read()
    right_bytes = await right_image.read()

    # 解码 JPEG/PNG → numpy BGR
    left_arr = np.frombuffer(left_bytes, dtype=np.uint8)
    right_arr = np.frombuffer(right_bytes, dtype=np.uint8)
    left_bgr = cv2.imdecode(left_arr, cv2.IMREAD_COLOR)
    right_bgr = cv2.imdecode(right_arr, cv2.IMREAD_COLOR)

    if left_bgr is None:
        raise HTTPException(status_code=400, detail="Failed to decode left image")
    if right_bgr is None:
        raise HTTPException(status_code=400, detail="Failed to decode right image")

    # 推理
    depth_u16, disp_f32, vis_jpg, meta = infer_engine.predict_from_arrays(
        left_bgr, right_bgr,
        request_id=request_id,
        scale=scale,
        valid_iters=valid_iters,
        z_far=z_far,
        remove_invisible=remove_invisible,
        fx=fx,
        fy=fy,
        ppx=ppx,
        ppy=ppy,
        baseline=baseline_m,
        return_depth=return_depth,
        return_disparity=return_disparity,
        return_color_jpg=return_color_jpg,
        jpg_quality=jpg_quality,
    )

    # 构建响应 headers
    headers = {
        "X-Status": meta["status"],
        "X-Request-Id": meta.get("request_id", ""),
        "X-Elapsed-Sec": str(meta.get("elapsed_sec", 0)),
    }

    if meta["status"] == "error":
        headers["X-Error-Message"] = meta.get("message", "unknown error")
        return Response(content=b"", media_type="image/png", headers=headers)

    if depth_u16 is not None:
        headers["X-Depth-Shape"] = json.dumps(list(depth_u16.shape))
        # 编码为 PNG 原始字节
        ok, depth_png = cv2.imencode(".png", depth_u16, [cv2.IMWRITE_PNG_COMPRESSION, 3])
        if not ok:
            return Response(content=b"", media_type="image/png", headers={
                **headers, "X-Status": "error", "X-Error-Message": "Failed to encode depth PNG",
            })
        return Response(content=depth_png.tobytes(), media_type="image/png", headers=headers)

    return Response(content=b"", media_type="image/png", headers=headers)


# ── base64 端点（保留向后兼容） ────────────────────────────────

@infer_router.post("/stereo", response_model=StereoPredictResponse)
async def predict_stereo(body: StereoPredictRequest):
    """双目深度估计推理（base64 图片，保留兼容）。"""
    if infer_engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return infer_engine.predict(body)
