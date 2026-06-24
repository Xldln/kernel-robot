"""SigLIP2 多视角训练/推理共用的图像增广工具 (重建版)。

仅包含推理服务用到的 ``apply_background_mask``, 语义参考自
``test_video_siglip2_multiview_recursive.py`` 中对拼接图顶部按比例遮盖背景。
"""

from __future__ import annotations

import numpy as np
from PIL import Image


def apply_background_mask(image: Image.Image, ratio: float) -> Image.Image:
    """将拼接图顶部 ``ratio`` 比例的区域置黑 (遮盖背景/头部干扰)。

    Args:
        image: PIL Image (整张拼接图, 在 split_image_to_views 之前调用)
        ratio: 顶部遮盖比例, 取值 [0, 1); <=0 时不做处理
    Returns:
        处理后的新 PIL Image (不修改输入)
    """
    if ratio is None or ratio <= 0:
        return image

    image = image.convert("RGB")
    w, h = image.size
    cutoff = int(h * ratio)
    if cutoff <= 0:
        return image

    arr = np.array(image)
    arr[:cutoff, :, :] = 0
    return Image.fromarray(arr)
