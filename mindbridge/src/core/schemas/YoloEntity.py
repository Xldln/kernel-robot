from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field



class Detection(BaseModel):
    """单个检测目标"""
    id: int = Field(..., description="全局检测 ID")
    label: str = Field(..., description="类别名称")
    class_name: str = Field(..., alias="class", description="类别名称（兼容 JSON key 'class'）")
    class_id: int = Field(..., description="类别 ID")
    score: float = Field(..., ge=0.0, le=1.0, description="置信度")
    bbox: list[float] = Field(default_factory=list, description="边界框 [x1, y1, x2, y2]")
    mask_png_b64: Optional[str] = Field(None, description="分割掩码 PNG base64")


# ─── 请求体 ──────────────────────────────────────────────────────

class PredictRequest(BaseModel):
    """YOLO 推理请求"""
    request_id: str = Field(default="", description="请求 ID（唯一标识）")
    image_b64: str = Field(..., description="BGR 图像 base64 编码")
    conf: Optional[float] = Field(None, ge=0.0, le=1.0, description="置信度阈值，覆盖服务端默认值")
    tracker: Optional[str] = Field(None, description="跟踪器配置名，如 bytetrack.yaml")
    persist: Optional[bool] = Field(None, description="跟踪持久化")
    return_masks: Optional[bool] = Field(None, description="是否返回分割掩码")
    return_annotated_image: Optional[bool] = Field(None, description="是否返回标注图")
    show_window: Optional[bool] = Field(None, description="是否显示 OpenCV 窗口")
    prompts: list[str] = Field(default_factory=list, description="标签过滤（预留）")
    clear_previous: bool = Field(True, description="清除前序跟踪状态（接口兼容）")


# ─── 响应体 ──────────────────────────────────────────────────────

class PredictResponse(BaseModel):
    """YOLO 推理响应"""
    status: str = Field(..., description="状态，ok 或 error")
    request_id: str = Field(default="", description="对应请求 ID")
    num_detections: int = Field(0, description="检测目标数量")
    detections: list[Detection] = Field(default_factory=list, description="检测结果列表")
    annotated_image_b64: Optional[str] = Field(None, description="标注图像 base64 JPG")
    elapsed_sec: float = Field(0.0, description="服务端推理耗时（秒）")
    message: Optional[str] = Field(None, description="错误时携带错误信息")
