"""RealSense 深度相机请求 / 响应模型"""

from __future__ import annotations

from typing import Optional

import numpy as np
from pydantic import BaseModel, ConfigDict, Field


# ─── 内部数据模型（service 层返回）──────────────────────────────

class CaptureData(BaseModel):
    """单帧原始数据 — service 层返回给 controller，不含序列化。"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    color_bgr: np.ndarray = Field(..., description="彩色图 (H,W,3) uint8")
    depth_m: np.ndarray = Field(..., description="深度图 (H,W) float32，单位米，已对齐到彩色")
    depth_u16: np.ndarray = Field(..., description="深度图 (H,W) uint16，单位毫米")
    ir_left: Optional[np.ndarray] = Field(None, description="红外左图 (H,W) uint8，供 FastFoundation 立体深度")
    ir_right: Optional[np.ndarray] = Field(None, description="红外右图 (H,W) uint8，供 FastFoundation 立体深度")
    K: np.ndarray = Field(..., description="彩色相机内参 (3,3) float32")
    ir_left_K: np.ndarray = Field(..., description="左 IR 相机内参 (3,3) float32")
    ir_to_color_R: np.ndarray = Field(..., description="左 IR 到彩色相机旋转矩阵 (3,3) float32")
    ir_to_color_T: np.ndarray = Field(..., description="左 IR 到彩色相机平移向量 (3,) float32，单位米")
    baseline: float = Field(..., description="立体基线（米）")
    frame_id: int = Field(..., description="帧编号")


# ─── 请求体 ──────────────────────────────────────────────────────

class CaptureRequest(BaseModel):
    """单帧采集请求（预留，后续可扩展 conf／曝光参数）"""
    request_id: str = Field(default="", description="请求 ID")


# ─── 响应体 ──────────────────────────────────────────────────────

class CaptureResponse(BaseModel):
    """单帧采集响应"""
    status: str = Field(..., description="状态，ok 或 error")
    frame_id: int = Field(..., description="帧编号")
    baseline: float = Field(..., description="立体相机基线（米）")
    K: list[list[float]] = Field(..., description="左 IR 相机内参矩阵 (3x3)")
    color_jpg_b64: str = Field(..., description="彩色图 JPEG base64")
    depth_u16_png_b64: str = Field(..., description="深度图（uint16 mm）PNG base64")
    ir_left_b64: Optional[str] = Field(None, description="红外左图 JPEG base64，供 FastFoundation")
    ir_right_b64: Optional[str] = Field(None, description="红外右图 JPEG base64，供 FastFoundation")
    elapsed_sec: float = Field(0.0, description="采集+推理耗时（秒）")
    message: Optional[str] = Field(None, description="错误时携带错误信息")


class CameraInfoResponse(BaseModel):
    """相机参数响应"""
    status: str = Field(..., description="状态")
    image_size: list[int] = Field(..., description="图像宽高 [width, height]")
    baseline: float = Field(..., description="立体相机基线（米）")
    frame_id: int = Field(..., description="当前帧编号")
    K: list[list[float]] = Field(..., description="左 IR 相机内参矩阵 (3x3)")


class ShutdownResponse(BaseModel):
    """关闭引擎响应"""
    status: str = Field(..., description="shutdown 或 already closed")
