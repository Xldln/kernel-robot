from __future__ import annotations

import base64
from typing import Any

import requests


class FusionUiClient:
    def __init__(self, base_url: str, *, timeout_sec: float = 1.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_sec = timeout_sec

    def post_video_frame(
        self,
        frame_bytes: bytes,
        *,
        title: str = "MindBridge Camera",
        mime_type: str = "image/jpeg",
        source: str = "MindBridge",
        metadata: dict[str, Any] | None = None,
    ) -> None:
        payload = {
            "title": title,
            "frame_base64": base64.b64encode(frame_bytes).decode("ascii"),
            "mime_type": mime_type,
            "source": source,
        }
        if metadata:
            payload["metadata"] = metadata
        requests.post(
            f"{self.base_url}/api/video-stream",
            json=payload,
            timeout=self.timeout_sec,
        )
