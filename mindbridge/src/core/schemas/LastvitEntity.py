"""LAST-ViT 特征匹配请求 / 响应模型"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class TopKItem(BaseModel):
    """Top-K 相似度结果"""
    category: str = Field(..., description="类别名称")
    similarity: float = Field(..., description="余弦相似度")


class StateItem(BaseModel):
    """状态节点信息"""
    id: str = Field(..., description="状态 ID")
    node_id: str = Field(..., description="原始节点 ID")
    name: str = Field(..., description="状态描述")
    category: str = Field(..., description="类别全名")


# ─── 请求体 ──────────────────────────────────────────────────────

class PredictRequest(BaseModel):
    """LAST-ViT 特征推理请求"""
    request_id: str = Field(default="", description="请求 ID（唯一标识）")
    image_b64: str = Field(..., description="RGB 图像 base64 编码")


# ─── 响应体 ──────────────────────────────────────────────────────

class PredictResponse(BaseModel):
    """LAST-ViT 特征推理响应"""
    status: str = Field(..., description="状态，ok 或 error")
    request_id: str = Field(default="", description="对应请求 ID")
    ok: bool = Field(True, description="兼容旧字段，表示推理是否成功")
    best_category: str = Field(default="", description="最佳匹配类别")
    best_similarity: float = Field(0.0, description="最佳匹配余弦相似度")
    topk: list[TopKItem] = Field(default_factory=list, description="Top-K 相似度列表")
    total_category: list[StateItem] = Field(default_factory=list, description="所有可用状态节点")
    elapsed_sec: float = Field(0.0, description="服务端推理耗时（秒）")
    message: Optional[str] = Field(None, description="错误时携带错误信息")
