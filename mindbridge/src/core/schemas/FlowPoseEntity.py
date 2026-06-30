"""FlowPose 6D姿态估计 请求 / 响应模型"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


# ─── 请求体 ──────────────────────────────────────────────────────

class FlowPosePredictRequest(BaseModel):
    """FlowPose 姿态估计推理请求"""
    request_id: str = Field(default="", description="请求 ID（唯一标识）")
    rgb_image: str = Field(..., description="RGB 图像 base64 编码")
    depth_image: str = Field(..., description="深度图像 16-bit PNG base64 编码")
    combined_mask: str = Field(..., description="实例分割掩码 base64 编码")
    obj_ids: list = Field(default_factory=list, description="物体 ID 列表，每个元素为 [class_id, instance_id]")
    class_names: list[str] = Field(default_factory=list, description="物体类别名称列表")
    instance_names: list[str] = Field(default_factory=list, description="实例名称列表（优先级高于 class_names）")


# ─── 物体位姿结果 ────────────────────────────────────────────────

class ObjectPose(BaseModel):
    """单个物体的 6D 姿态和尺寸"""
    name: str = Field(..., description="物体名称")
    pose: list[list[float]] = Field(..., description="4×4 位姿矩阵 (旋转 + 平移)")
    length: list[float] = Field(..., description="物体 3D 尺寸 [长, 宽, 高]")
    obj_id: list = Field(..., description="物体 ID")
    box_id: Optional[int] = Field(None, description="实例索引")


# ─── 响应体 ──────────────────────────────────────────────────────

class FlowPosePredictResponse(BaseModel):
    """FlowPose 姿态估计推理响应"""
    status: str = Field(..., description="状态，ok 或 error")
    request_id: str = Field(default="", description="对应请求 ID")
    objects: list[ObjectPose] = Field(default_factory=list, description="物体姿态列表")
    elapsed_sec: float = Field(0.0, description="服务端推理耗时（秒）")
    message: Optional[str] = Field(None, description="错误时携带错误信息")
    traceback: Optional[str] = Field(None, description="错误时携带 traceback 信息")
