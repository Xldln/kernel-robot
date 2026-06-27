"""RGB frame sources for the control center."""

from __future__ import annotations

import time
from typing import Protocol

import cv2

from mindbridge.src.MindBridgeClient import MindBridgeClient


class RGBFrameSource(Protocol):
    """Uniform RGB frame source contract."""

    def capture(self) -> dict:
        """Return a frame dict containing at least status, frame_id, and color_jpg."""

    def close(self) -> None:
        """Release resources held by the source."""


class RealSenseRGBSource:
    """RGB source backed by the existing RealSense service.

    multi=True 时使用 /capture/all/raw，返回帧中附带 aux（color-only 相机彩色帧）。
    """

    def __init__(self, client: MindBridgeClient, multi: bool = False):
        self.client = client
        self.multi = multi

    def capture(self) -> dict:
        frame = self.client.capture_all() if self.multi else self.client.capture()
        frame["source"] = "realsense"
        frame.setdefault("timestamp", time.time())
        return frame

    def close(self) -> None:
        pass


class OpenCVRGBSource:
    """RGB source backed by a local OpenCV camera device."""

    def __init__(
        self,
        camera_index: int = 0,
        *,
        width: int | None = None,
        height: int | None = None,
        fps: int | None = None,
    ):
        self.camera_index = camera_index
        self.frame_id = 0
        self.cap = cv2.VideoCapture(camera_index)
        if width:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        if height:
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        if fps:
            self.cap.set(cv2.CAP_PROP_FPS, fps)

    def capture(self) -> dict:
        if not self.cap.isOpened():
            return {
                "status": "error",
                "frame_id": self.frame_id,
                "message": f"OpenCV camera {self.camera_index} is not opened",
                "source": "usb",
                "timestamp": time.time(),
            }

        ok, bgr = self.cap.read()
        if not ok or bgr is None:
            return {
                "status": "error",
                "frame_id": self.frame_id,
                "message": f"Failed to read from OpenCV camera {self.camera_index}",
                "source": "usb",
                "timestamp": time.time(),
            }

        encode_ok, jpg = cv2.imencode(".jpg", bgr, [cv2.IMWRITE_JPEG_QUALITY, 90])
        if not encode_ok:
            return {
                "status": "error",
                "frame_id": self.frame_id,
                "message": "Failed to encode camera frame as JPEG",
                "source": "usb",
                "timestamp": time.time(),
            }

        self.frame_id += 1
        h, w = bgr.shape[:2]
        return {
            "status": "ok",
            "frame_id": self.frame_id,
            "color_jpg": jpg.tobytes(),
            "color_width": int(w),
            "color_height": int(h),
            "source": "usb",
            "timestamp": time.time(),
        }

    def close(self) -> None:
        self.cap.release()
