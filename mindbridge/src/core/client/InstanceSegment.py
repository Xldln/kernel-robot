from __future__ import annotations

import uuid
from pathlib import Path

import numpy as np

from mindbridge.src.core.schemas.YoloEntity import PredictRequest, PredictResponse
from mindbridge.src.core.tool.image import ImageProcessor


class InstanceSegmentClient:

    def __init__(self, base_url: str = "http://127.0.0.1:8000", timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.img_proc = ImageProcessor()
        self.client = httpx.Client(base_url=self.base_url, timeout=timeout)

    def predict(
        self,
        image: np.ndarray | str | Path,
        conf: float | None = None,
        return_masks: bool = True,
        return_annotated_image: bool = True,
        **kwargs,
    ) -> PredictResponse:
        """发送推理请求并返回结果

        Args:
            image: BGR numpy 数组 或 图片文件路径
            conf: 置信度阈值，None 则走服务端默认
            return_masks: 是否返回分割掩码
            return_annotated_image: 是否返回标注图
            **kwargs: 透传给 PredictRequest 的其他参数（tracker, persist 等）

        Returns:
            PredictResponse
        """
        if isinstance(image, (str, Path)):
            image_b64 = self.img_proc.encode_file_to_base64(Path(image))
        elif isinstance(image, np.ndarray):
            image_b64 = self.img_proc.encode_bgr_to_base64_jpg(image)
        else:
            raise TypeError(f"Unsupported image type: {type(image)}")

        request = PredictRequest(
            request_id=str(uuid.uuid4()),
            image_b64=image_b64,
            conf=conf,
            return_masks=return_masks,
            return_annotated_image=return_annotated_image,
            **kwargs,
        )

        resp = self.client.post(
            "/predict",
            json=request.model_dump(exclude_none=True),
        )
        resp.raise_for_status()
        return PredictResponse(**resp.json())

    def close(self):
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
