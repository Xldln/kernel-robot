"""siglip2_trainer: 多视角 SigLIP2 模型与增广工具 (仓库内重建版)。

对外导出与参考脚本一致的接口, 供 SigLIP 推理服务复用。
"""

from mindbridge.siglip2_trainer.augmentation import apply_background_mask
from mindbridge.siglip2_trainer.multiview_models import (
    CrossViewAttentionPooler,
    MultiViewSigLIPModel,
    split_image_to_views,
)

__all__ = [
    "CrossViewAttentionPooler",
    "MultiViewSigLIPModel",
    "split_image_to_views",
    "apply_background_mask",
]
