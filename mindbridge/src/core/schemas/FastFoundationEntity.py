"""Fast-Foundation Stereo 深度估计请求 / 响应模型"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


# ─── 请求体 ──────────────────────────────────────────────────────

class StereoPredictRequest(BaseModel):
    """Stereo 深度估计推理请求"""
    request_id: str = Field(default="", description="请求 ID（唯一标识）")
    left_image_b64: str = Field(..., description="左目图像 base64 编码（BGR）")
    right_image_b64: str = Field(..., description="右目图像 base64 编码（BGR）")

    # 相机内参覆盖（不传则使用 config 默认值）
    fx: Optional[float] = Field(None, description="左目焦距 fx（像素）")
    fy: Optional[float] = Field(None, description="左目焦距 fy（像素）")
    ppx: Optional[float] = Field(None, description="左目光心 cx（像素）")
    ppy: Optional[float] = Field(None, description="左目光心 cy（像素）")
    baseline_m: Optional[float] = Field(None, description="双目基线（米）")

    # 推理参数覆盖
    valid_iters: Optional[int] = Field(None, description="RAFT 迭代次数")
    z_far: Optional[float] = Field(None, description="深度远裁剪面（米）")
    remove_invisible: Optional[bool] = Field(None, description="是否移除左目不可见区域的视差")
    scale: Optional[float] = Field(None, description="图像缩放比例")

    # 输出控制
    return_depth: bool = Field(True, description="是否返回深度图")
    return_disparity: bool = Field(False, description="是否返回视差图")
    return_color_jpg: bool = Field(False, description="是否返回拼接可视化 JPG")
    jpg_quality: int = Field(90, ge=1, le=100, description="JPG 压缩质量")


# ─── 响应体 ──────────────────────────────────────────────────────

class StereoPredictResponse(BaseModel):
    """Stereo 深度估计推理响应"""
    status: str = Field(..., description="状态，ok 或 error")
    request_id: str = Field(default="", description="对应请求 ID")
    # 深度
    depth_u16_b64: Optional[str] = Field(None, description="uint16 毫米深度图 base64")
    depth_shape: list[int] = Field(default_factory=list, description="深度图形状 [H, W]")
    # 视差
    disparity_b64: Optional[str] = Field(None, description="float32 视差图 base64 编码")
    disparity_shape: list[int] = Field(default_factory=list, description="视差图形状 [H, W]")
    # 可视化（左右拼接 + 视差着色）
    vis_jpg_b64: Optional[str] = Field(None, description="可视化拼接图 base64 JPG")
    # 元信息
    elapsed_sec: float = Field(0.0, description="服务端推理耗时（秒）")
    message: Optional[str] = Field(None, description="错误时携带错误信息")
