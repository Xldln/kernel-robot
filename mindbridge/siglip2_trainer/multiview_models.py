"""SigLIP2 多视角(Multi-View) 模型与拼接图拆分工具。

================================================================
说明: 本文件是根据参考脚本 ``test_video_siglip2_multiview_recursive.py``
的接口语义 **重建** 而来 (原训练工程 ``siglip2_trainer`` 不在本仓库中)。

提供与参考脚本一致的对外接口:
    - ``CrossViewAttentionPooler(embed_dim, num_queries, num_heads, num_layers, dropout)``
    - ``MultiViewSigLIPModel(base_model, pooler, num_views, embed_dim)``
        · ``model.encode_views(pixel_values)`` : [N=B*V, C, H, W] -> [B, D] (L2 归一化)
    - ``split_image_to_views(pil_image)`` : 将拼接图拆分为多视角 PIL 列表

⚠ 重要: pooler 内部的子模块命名是重建实现, 与真实训练 checkpoint 的
``state_dict`` 键可能不完全一致。``base_model.*`` 键来自 HuggingFace
SiglipModel, 可正常加载; 而 ``pooler.*`` 键若与训练实现不符, 加载时会
作为 missing/unexpected key 报出 (见 SiglipInfer 的加载日志)。若需精确
对齐, 请以原始 ``fine_tuning_siglip2_multiview.py`` 的模块结构为准。
================================================================
"""

from __future__ import annotations

import torch
import torch.nn as nn
from PIL import Image


# =============================================================================
# 拼接图 -> 多视角拆分
# =============================================================================

def split_image_to_views(image: Image.Image) -> list[Image.Image]:
    """将一张拼接图拆分为多个视角子图。

    依据宽高比自动推断拼接方式:
      - 近似正方形 (0.75 <= W/H <= 1.4): 视为 2x2 grid, 返回 4 个视角
      - 其余: 视为 1xN 水平拼接, N = round(W/H), 沿宽度等分, 返回 N 个视角

    控制中心将三路相机水平拼接 (1x3), 因此通常返回 3 个视角。
    """
    if not isinstance(image, Image.Image):
        raise TypeError(f"split_image_to_views 需要 PIL.Image, 收到 {type(image)}")

    image = image.convert("RGB")
    w, h = image.size
    ratio = w / max(h, 1)

    views: list[Image.Image] = []

    if 0.75 <= ratio <= 1.4:
        # 2x2 grid -> 4 个视角 (左上, 右上, 左下, 右下)
        hw, hh = w // 2, h // 2
        boxes = [
            (0, 0, hw, hh),
            (hw, 0, w, hh),
            (0, hh, hw, h),
            (hw, hh, w, h),
        ]
        for box in boxes:
            views.append(image.crop(box))
    else:
        # 1xN 水平拼接
        n = max(1, round(ratio))
        step = w // n
        for i in range(n):
            left = i * step
            right = w if i == n - 1 else (i + 1) * step
            views.append(image.crop((left, 0, right, h)))

    return views


# =============================================================================
# 跨视角注意力池化
# =============================================================================

class CrossViewAttentionPooler(nn.Module):
    """跨视角注意力池化头。

    以一组可学习的 query token 通过多层交叉注意力聚合 V 个视角的特征,
    将 [B, V, D] 融合为单个 [B, D] 表征。
    """

    def __init__(
        self,
        embed_dim: int,
        num_queries: int = 8,
        num_heads: int = 8,
        num_layers: int = 2,
        dropout: float = 0.0,
    ):
        super().__init__()
        self.embed_dim = embed_dim
        self.num_queries = num_queries

        # 可学习 query token
        self.query = nn.Parameter(torch.randn(num_queries, embed_dim) * 0.02)

        decoder_layer = nn.TransformerDecoderLayer(
            d_model=embed_dim,
            nhead=num_heads,
            dim_feedforward=embed_dim * 4,
            dropout=dropout,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )
        self.decoder = nn.TransformerDecoder(decoder_layer, num_layers=num_layers)
        self.norm = nn.LayerNorm(embed_dim)

    def forward(self, view_features: torch.Tensor) -> torch.Tensor:
        """[B, V, D] -> [B, D]"""
        b = view_features.size(0)
        q = self.query.unsqueeze(0).expand(b, -1, -1)  # [B, Q, D]
        out = self.decoder(tgt=q, memory=view_features)  # [B, Q, D]
        out = self.norm(out)
        return out.mean(dim=1)  # [B, D]


# =============================================================================
# 多视角 SigLIP2 模型
# =============================================================================

class MultiViewSigLIPModel(nn.Module):
    """冻结的 SigLIP2 base + 跨视角注意力池化。

    Args:
        base_model: HuggingFace SiglipModel (提供 get_image_features)
        pooler: CrossViewAttentionPooler
        num_views: 每个样本的视角数 (用于将 [B*V, ...] 还原为 [B, V, ...])
        embed_dim: 视觉特征维度 (= vision_config.hidden_size)
    """

    def __init__(self, base_model, pooler: CrossViewAttentionPooler,
                 num_views: int = 3, embed_dim: int | None = None):
        super().__init__()
        self.base_model = base_model
        self.pooler = pooler
        self.num_views = num_views
        self.embed_dim = embed_dim

        # 冻结 base model (推理服务无需训练)
        for p in self.base_model.parameters():
            p.requires_grad = False

    def encode_views(self, pixel_values: torch.Tensor) -> torch.Tensor:
        """将多视角图像编码为融合特征。

        Args:
            pixel_values: [N, C, H, W], N = B * num_views,
                          视角顺序按样本连续排列 (样本0的所有视角, 样本1的所有视角, ...)
        Returns:
            [B, D] L2 归一化的融合特征
        """
        # 逐视角提取 SigLIP2 图像特征
        feats = self.base_model.get_image_features(pixel_values=pixel_values)  # [N, D]
        d = feats.size(-1)

        if feats.size(0) % self.num_views != 0:
            raise ValueError(
                f"视角总数 {feats.size(0)} 不是 num_views={self.num_views} 的整数倍"
            )

        feats = feats.view(-1, self.num_views, d)  # [B, V, D]
        fused = self.pooler(feats)  # [B, D]
        fused = fused / fused.norm(dim=-1, keepdim=True).clamp(min=1e-12)
        return fused

    def forward(self, pixel_values: torch.Tensor) -> torch.Tensor:
        return self.encode_views(pixel_values)
