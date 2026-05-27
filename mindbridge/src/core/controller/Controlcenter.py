from __future__ import annotations
import time
from pathlib import Path
import cv2
import numpy as np
from fastapi import APIRouter
from mindbridge.src.core.service.RealsenseService import RealsenseClient


control_router = APIRouter(prefix="/control", tags=["Control Center"])

_capture_running = False


def run_capture_loop(
    config_path: str | Path = "/workspace/config.yaml",
    max_frames: int | None = None,
    publish_callback=None,
):
    """连续捕获 RealSense 图像并处理。

    Parameters
    ----------
    config_path : str | Path
        相机/模型配置文件路径。
    max_frames : int or None
        最大捕获帧数，None 表示无限。
    publish_callback : callable or None
        每帧回调，签名 publish_callback(data: dict) -> None。
    """
    global _capture_running
    _capture_running = True

    with RealsenseClient(config_path) as cam:
        frame_count = 0

        while _capture_running:
            if max_frames is not None and frame_count >= max_frames:
                break

            data = cam.capture()

            if publish_callback:
                publish_callback(data)

            # 可视化
            cv2.imshow("Color", data["color_bgr"])
            depth_vis = data["depth_m"].copy()
            depth_vis[~np.isfinite(depth_vis) | (depth_vis <= 0)] = 0
            depth_vis_mm = np.clip(depth_vis * 1000.0, 0, 10000).astype(np.uint16)
            depth_color = cv2.applyColorMap(
                cv2.convertScaleAbs(depth_vis_mm, alpha=255.0 / 10000),
                cv2.COLORMAP_JET,
            )
            cv2.imshow("Depth", depth_color)

            if cam.frame_id % 30 == 0:
                print(f"[CAPTURE] frame_id={cam.frame_id}")

            if cv2.waitKey(1) & 0xFF == 27:  # ESC
                break

            frame_count += 1

    _capture_running = False
    cv2.destroyAllWindows()


@control_router.post("/start")
def start_capture(config_path: str = "/workspace/config.yaml"):
    """启动连续捕获（后台运行）。"""
    import threading
    t = threading.Thread(
        target=run_capture_loop,
        args=(config_path,),
        daemon=True,
    )
    t.start()
    return {"status": "started"}


@control_router.post("/stop")
def stop_capture():
    """停止连续捕获。"""
    global _capture_running
    _capture_running = False
    return {"status": "stopped"}


if __name__ == "__main__":
    run_capture_loop()
