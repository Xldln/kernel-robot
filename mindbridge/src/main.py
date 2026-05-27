"""MindBridge Control Center — 从 RealSense 服务(8000) 持续采图并分发给 YOLO 服务(8001) 推理。

用法:
  python mindbridge/src/main.py                          # 显示窗口，无限采集
  python mindbridge/src/main.py --no-show --max-frames 100 --out-dir ./output
"""

from __future__ import annotations

import argparse
import base64
import os
import time
from pathlib import Path
from typing import Optional
from .MindBridgeClient import MindBridgeClient
import cv2
import numpy as np
from mindbridge.src.core.tool.image import _draw_detections



def run(
    realsense_url: str = "http://127.0.0.1:8000",
    yolo_url: str = "http://127.0.0.1:8001",
    show: bool = True,
    max_frames: Optional[int] = None,
    out_dir: Optional[str] = None,
    log_interval: int = 30,
) -> None:
    client = MindBridgeClient(realsense_url, yolo_url)

    print("[ControlCenter] Waiting for services ...")
    for attempt in range(60):
        h = client.health()
        rs_ok = h.get("realsense", {}).get("status") == "ok"
        yolo_ok = h.get("yolo", {}).get("status") == "ok"
        if rs_ok and yolo_ok:
            print("[ControlCenter] Both services ready")
            break
        time.sleep(1)
    else:
        print("[ControlCenter] WARNING: services not ready — will retry per frame")

    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    frame_count = 0
    running = True

    print("[ControlCenter] Starting capture → inference loop ...")

    try:
        while running:
            if max_frames is not None and frame_count >= max_frames:
                break

            t_loop = time.time()

            # ── Step 1: Capture from RealSense ──
            try:
                cap = client.capture()
            except Exception as e:
                print(f"[ControlCenter] Capture failed: {e}")
                time.sleep(0.2)
                continue

            if cap.get("status") != "ok":
                print(f"[ControlCenter] Capture error: {cap.get('message')}")
                time.sleep(0.1)
                continue

            color_jpg_b64: str = cap["color_jpg_b64"]
            frame_id: int = cap["frame_id"]

            # ── Step 2: Inference by YOLO ──
            t_infer_start = time.time()
            try:
                pred = client.predict(color_jpg_b64, request_id=str(frame_id))
            except Exception as e:
                print(f"[ControlCenter] Inference failed: {e}")
                pred = {"status": "error", "num_detections": 0, "detections": []}
            infer_ms = (time.time() - t_infer_start) * 1000

            # ── Step 3: Display ──
            if show:
                if pred.get("status") == "ok" and pred.get("annotated_image_b64"):
                    img_bytes = base64.b64decode(pred["annotated_image_b64"])
                    img_arr = np.frombuffer(img_bytes, dtype=np.uint8)
                    display = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
                else:
                    img_bytes = base64.b64decode(color_jpg_b64)
                    img_arr = np.frombuffer(img_bytes, dtype=np.uint8)
                    color_bgr = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
                    display = _draw_detections(
                        color_bgr,
                        pred.get("detections", []),
                    )

                cv2.imshow("Control Center — Color + YOLO", display)
                if cv2.waitKey(1) & 0xFF == 27:
                    running = False

            # ── Step 4: Save ──
            if out_dir and pred.get("status") == "ok" and pred.get("annotated_image_b64"):
                ann_bytes = base64.b64decode(pred["annotated_image_b64"])
                out_path = f"{out_dir}/{frame_id:06d}_annotated.jpg"
                with open(out_path, "wb") as f:
                    f.write(ann_bytes)

            # ── Log ──
            loop_ms = (time.time() - t_loop) * 1000
            if frame_count % log_interval == 0:
                n_det = pred.get("num_detections", 0)
                status = pred.get("status", "?")
                print(
                    f"[Frame {frame_id:05d}] {n_det} detections | "
                    f"infer={infer_ms:.1f}ms | loop={loop_ms:.1f}ms | {status}"
                )

            frame_count += 1

    except KeyboardInterrupt:
        print("\n[ControlCenter] Interrupted by user")
    finally:
        cv2.destroyAllWindows()
        print(f"[ControlCenter] Done. Processed {frame_count} frames.")



def main() -> None:
    parser = argparse.ArgumentParser(
        description="MindBridge Control Center — RealSense → YOLO pipeline",
    )
    parser.add_argument(
        "--realsense-url", default="http://127.0.0.1:8000",
        help="RealSense 服务地址（默认 :8000）",
    )
    parser.add_argument(
        "--yolo-url", default="http://127.0.0.1:8001",
        help="YOLO 服务地址（默认 :8001）",
    )
    parser.add_argument(
        "--no-show", action="store_true",
        help="不显示 OpenCV 窗口（无头模式）",
    )
    parser.add_argument(
        "--max-frames", type=int, default=None,
        help="最大处理帧数，默认无限",
    )
    parser.add_argument(
        "--out-dir", type=str, default=None,
        help="保存标注结果图到指定目录",
    )
    parser.add_argument(
        "--log-interval", type=int, default=30,
        help="日志输出间隔（帧数），默认 30",
    )

    args = parser.parse_args()

    run(
        realsense_url=args.realsense_url,
        yolo_url=args.yolo_url,
        show=not args.no_show,
        max_frames=args.max_frames,
        out_dir=args.out_dir,
        log_interval=args.log_interval,
    )


if __name__ == "__main__":
    main()
