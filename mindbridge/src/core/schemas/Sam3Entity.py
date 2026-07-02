"""SAM3 目标检测 / 分割 请求 / 响应模型"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


# ─── 请求体 ──────────────────────────────────────────────────────

class Sam3PredictRequest(BaseModel):
    """SAM3 推理请求"""
    request_id: str = Field(default="", description="请求 ID（唯一标识）")
    image_b64: str = Field(..., description="RGB 图像 base64 编码")
    prompts: list[str] = Field(default_factory=list, description="文本提示列表，如 ['cat', 'dog']")
    score_threshold: Optional[float] = Field(None, ge=0.0, le=1.0, description="置信度阈值（不传则使用配置默认值）")
    box_prompts: Optional[dict[str, list[float]]] = Field(
        None, description="box 提示 {label: [x1, y1, x2, y2]}，用 bbox 替代文本匹配更鲁棒"
    )


# ─── 检测结果 ────────────────────────────────────────────────────

class Detection(BaseModel):
    """单个检测结果"""
    id: int = Field(..., description="检测 ID")
    label: str = Field(..., description="类别名称（prompt 文本）")
    score: float = Field(..., ge=0.0, le=1.0, description="置信度分数")
    bbox: list[float] = Field(default_factory=list, description="边界框 [x1, y1, x2, y2]")
    mask_png_b64: Optional[str] = Field(None, description="分割掩码 PNG base64")


# ─── 响应体 ──────────────────────────────────────────────────────

class Sam3PredictResponse(BaseModel):
    """SAM3 推理响应"""
    status: str = Field(..., description="状态，ok 或 error")
    request_id: str = Field(default="", description="对应请求 ID")
    detections: list[Detection] = Field(default_factory=list, description="检测结果列表")
    elapsed_sec: float = Field(0.0, description="服务端推理耗时（秒）")
    message: Optional[str] = Field(None, description="错误时携带错误信息")
