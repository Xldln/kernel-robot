"""RealSense 深度相机控制层 — 提供 /realsense 路由（使用硬件内置深度）。"""

from __future__ import annotations

import base64
import time

import cv2
from fastapi import APIRouter, HTTPException

from mindbridge.src.core.schemas.RealsenseEntity import (
    CameraInfoResponse,
    CaptureData,
    CaptureResponse,
    ShutdownResponse,
)
from mindbridge.src.core.service.RealsenseService import RealsenseService

realsense_router = APIRouter(prefix="/realsense", tags=["RealSense Depth"])

engine: RealsenseService | None = None


def init_engine(
    config_path: str = "/workspace/mindbridge/src/core/config/realsense-config.yaml",
) -> RealsenseService:
    """启动时初始化 RealSense 相机。"""
    global engine
    print(f"Initializing RealSense from config: {config_path}")
    engine = RealsenseService(config_path)
    return engine


@realsense_router.post("/capture", response_model=CaptureResponse)
def capture():
    """采集一帧，返回彩色图（JPG）与深度图（16bit PNG）的 base64。"""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    t_start = time.time()
    data: CaptureData = engine.capture()

    try:
        # 彩色 → base64 JPG
        ok_jpg, buf_jpg = cv2.imencode(".jpg", data.color_bgr, [cv2.IMWRITE_JPEG_QUALITY, 90])
        if not ok_jpg:
            raise RuntimeError("Failed to encode color image")
        color_jpg_b64 = base64.b64encode(buf_jpg.tobytes()).decode("utf-8")

        # 深度（uint16 mm）→ base64 PNG
        ok_png, buf_png = cv2.imencode(
            ".png", data.depth_u16, [cv2.IMWRITE_PNG_COMPRESSION, 3],
        )
        if not ok_png:
            raise RuntimeError("Failed to encode depth image")
        depth_png_b64 = base64.b64encode(buf_png.tobytes()).decode("utf-8")

        elapsed = round(time.time() - t_start, 4)

        return CaptureResponse(
            status="ok",
            frame_id=data.frame_id,
            baseline=data.baseline,
            K=data.K.tolist(),
            color_jpg_b64=color_jpg_b64,
            depth_u16_png_b64=depth_png_b64,
            elapsed_sec=elapsed,
        )

    except Exception as e:
        elapsed = round(time.time() - t_start, 4)
        return CaptureResponse(
            status="error",
            frame_id=data.frame_id,
            baseline=data.baseline,
            K=data.K.tolist(),
            color_jpg_b64="",
            depth_u16_png_b64="",
            elapsed_sec=elapsed,
            message=str(e),
        )


@realsense_router.get("/info", response_model=CameraInfoResponse)
def info():
    """返回相机参数。"""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")

    return CameraInfoResponse(
        status="ok",
        image_size=list(engine.image_size),
        baseline=engine.baseline,
        frame_id=engine.frame_id,
        K=engine.K.tolist(),
    )


@realsense_router.post("/shutdown", response_model=ShutdownResponse)
def shutdown():
    """释放相机资源并关闭引擎。"""
    global engine
    if engine is not None:
        engine.close()
        engine = None
        return ShutdownResponse(status="shutdown")
    return ShutdownResponse(status="already closed")
