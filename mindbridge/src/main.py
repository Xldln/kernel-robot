"""MindBridge Control Center — 从 RealSense 服务(8000) 持续采图并分发给 YOLO 服务(8001) 推理和 SigLIP 服务(8002) 状态分类。

所有图片数据通过 raw bytes 传输，零 base64 开销。

用法:
  python mindbridge/src/main.py                          # 显示窗口，无限采集
  python mindbridge/src/main.py --no-show --max-frames 100 --out-dir ./output
"""

from __future__ import annotations

import argparse
import os
import time
from typing import Optional
from .MindBridgeClient import MindBridgeClient
import cv2
import numpy as np
from mindbridge.src.core.tool.image import _draw_detections



def run(
    realsense_url: str = "http://127.0.0.1:8000",
    yolo_url: str = "http://127.0.0.1:8001",
    siglip_url: str = "http://127.0.0.1:8002",
    sam3_url: str = "http://127.0.0.1:8005",
    fastfoundation_url: str = "http://127.0.0.1:8004",
    flowpose_url: str = "http://127.0.0.1:8006",
    detector: str = "sam3",           # "sam3" | "yolo"
    pipeline: str = "full",           # "full" | "basic"
    sam3_prompts: Optional[str] = None,
    sam3_threshold: Optional[float] = None,
    show: bool = True,
    max_frames: Optional[int] = None,
    out_dir: Optional[str] = None,
    log_interval: int = 30,
) -> None:
    client = MindBridgeClient(realsense_url, yolo_url, siglip_url, sam3_url, fastfoundation_url, flowpose_url)
    _sam3_prompts = [p.strip() for p in sam3_prompts.split(",")] if sam3_prompts else None
    _detector = detector.lower()
    _full = pipeline.lower() == "full"
    if _detector not in ("yolo", "sam3"):
        raise ValueError(f"detector must be 'yolo' or 'sam3', got '{detector}'")

    print(f"[ControlCenter] Pipeline: {'FULL' if _full else 'BASIC'} | Detector: {_detector.upper()}")

    print("[ControlCenter] Waiting for services ...")
    for attempt in range(60):
        h = client.health()
        rs_ok = h.get("realsense", {}).get("status") == "ok"
        yolo_ok = h.get("yolo", {}).get("status") == "ok"
        siglip_ok = h.get("siglip", {}).get("status") == "ok"
        sam3_ok = h.get("sam3", {}).get("status") == "ok"

        ff_ok = h.get("fastfoundation", {}).get("status") == "ok" if _full else True
        fp_ok = h.get("flowpose", {}).get("status") == "ok" if _full else True

        if _detector == "yolo" and rs_ok and yolo_ok and siglip_ok and ff_ok and fp_ok:
            print(f"[ControlCenter] All services ready (YOLO {'full' if _full else 'basic'} pipeline)")
            break
        elif _detector == "sam3" and rs_ok and sam3_ok and siglip_ok and ff_ok and fp_ok:
            print(f"[ControlCenter] All services ready (SAM3 {'full' if _full else 'basic'} pipeline)")
            break

        if attempt % 10 == 0:
            print(f"[ControlCenter] Waiting... rs={rs_ok} yolo={yolo_ok} sam3={sam3_ok} siglip={siglip_ok}")
        time.sleep(1)
    else:
        print("[ControlCenter] WARNING: services not ready — will retry per frame")

    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    frame_count = 0
    running = True

    print("[ControlCenter] Starting capture → inference → classification loop ...")

    if show:
        win_title = f"RGB + {_detector.upper()} Detection"
        cv2.namedWindow(win_title, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(win_title, 640, 480)

    try:
        while running:
            if max_frames is not None and frame_count >= max_frames:
                break

            t_loop = time.time()

            # ── Step 1: Capture from RealSense (raw bytes) ──
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

            color_jpg = cap.get("color_jpg")
            if not color_jpg:
                print(f"[ControlCenter] Capture returned no color image: {cap.get('message', 'unknown')}")
                time.sleep(0.1)
                continue
            frame_id: int = cap.get("frame_id", 0)

            # ── Step 2 (full only): FastFoundation stereo depth ──
            ff_result: dict = {}
            ff_ms = 0.0
            depth_png_for_flowpose: bytes | None = cap.get("depth_png")
            if _full:
                ir_left_jpg = cap.get("ir_left_jpg")
                ir_right_jpg = cap.get("ir_right_jpg")
                if ir_left_jpg and ir_right_jpg:
                    t_ff = time.time()
                    try:
                        ff_result = client.fastfoundation_depth_raw(
                            ir_left_jpg, ir_right_jpg,
                            return_depth=True, request_id=str(frame_id),
                        )
                        if ff_result.get("status") == "ok" and ff_result.get("depth_png"):
                            depth_png_for_flowpose = ff_result["depth_png"]
                    except Exception as e:
                        print(f"[ControlCenter] FastFoundation failed: {e}")
                    ff_ms = (time.time() - t_ff) * 1000

            # ── Step 3: Detection (YOLO or SAM3, mutually exclusive) ──
            pred: dict = {"status": "ok", "num_detections": 0, "detections": [],
                          "annotated_image": None, "mask_bytes": {}}
            sam3_result: dict = {"status": "ok", "detections": [], "mask_bytes": {}}
            infer_ms = 0.0
            sam3_ms = 0.0

            if _detector == "yolo":
                t_infer_start = time.time()
                try:
                    pred = client.predict(color_jpg, request_id=str(frame_id))
                except Exception as e:
                    print(f"[ControlCenter] YOLO inference failed: {e}")
                    pred = {"status": "error", "num_detections": 0, "detections": [],
                            "annotated_image": None, "mask_bytes": {}}
                infer_ms = (time.time() - t_infer_start) * 1000

            elif _detector == "sam3":
                t_sam3_start = time.time()
                try:
                    sam3_result = client.sam3_detect(
                        color_jpg,
                        prompts=_sam3_prompts,
                        score_threshold=sam3_threshold,
                        request_id=str(frame_id),
                    )
                except Exception as e:
                    print(f"[ControlCenter] SAM3 inference failed: {e}")
                    sam3_result = {"status": "error", "detections": [], "mask_bytes": {}}
                sam3_ms = (time.time() - t_sam3_start) * 1000

            # ── Step 4 (full only): FlowPose 6D pose estimation ──
            flowpose_result: dict = {}
            flowpose_ms = 0.0
            if _full and depth_png_for_flowpose:
                # 从检测结果构建 mask
                mask_bytes_for_flowpose: bytes | None = None
                obj_ids_for_flowpose = []
                class_names_for_flowpose = []
                if _detector == "sam3" and sam3_result.get("status") == "ok":
                    for det in sam3_result.get("detections", []):
                        mask_file = det.get("mask_file", "")
                        if mask_file:
                            mask_data = sam3_result.get("mask_bytes", {}).get(mask_file)
                            if mask_data:
                                mask_bytes_for_flowpose = mask_data
                                obj_ids_for_flowpose.append([det.get("id", 1), det.get("id", 1)])
                                class_names_for_flowpose.append(det.get("label", "object"))
                elif _detector == "yolo" and pred.get("status") == "ok":
                    for i, det in enumerate(pred.get("detections", [])):
                        mask_file = det.get("mask_file", "")
                        if mask_file:
                            mask_data = pred.get("mask_bytes", {}).get(mask_file)
                            if mask_data:
                                mask_bytes_for_flowpose = mask_data
                                obj_ids_for_flowpose.append([i + 1, i + 1])
                                class_names_for_flowpose.append(det.get("class_name", det.get("label", "object")))

                if mask_bytes_for_flowpose and depth_png_for_flowpose:
                    t_fp = time.time()
                    try:
                        flowpose_result = client.flowpose_pose(
                            color_jpg, depth_png_for_flowpose, mask_bytes_for_flowpose,
                            obj_ids=obj_ids_for_flowpose,
                            class_names=class_names_for_flowpose,
                            request_id=str(frame_id),
                        )
                    except Exception as e:
                        print(f"[ControlCenter] FlowPose failed: {e}")
                    flowpose_ms = (time.time() - t_fp) * 1000

            # ── Step 5: SigLIP state classification ──
            t_siglip_start = time.time()
            state_result = {}
            try:
                state_result = client.classify_state(color_jpg, request_id=str(frame_id))
            except Exception as e:
                print(f"[ControlCenter] SigLIP classification failed: {e}")
                state_result = {"status": "error", "best_category": "", "best_similarity": 0.0}
            siglip_ms = (time.time() - t_siglip_start) * 1000

            if show:
                # ── 解码原始 RGB 图片 ──
                color_arr = np.frombuffer(color_jpg, dtype=np.uint8)
                original_rgb = cv2.imdecode(color_arr, cv2.IMREAD_COLOR)

                # ── 窗口1: RGB + 检测结果 ──
                if pred.get("status") == "ok" and pred.get("annotated_image"):
                    ann_arr = np.frombuffer(pred["annotated_image"], dtype=np.uint8)
                    yolo_display = cv2.imdecode(ann_arr, cv2.IMREAD_COLOR)
                else:
                    yolo_display = _draw_detections(
                        original_rgb.copy(),
                        pred.get("detections", []),
                    )

                # ── 叠加 SAM3 检测结果（蓝色 bbox + 半透明 mask） ──
                if sam3_result.get("status") == "ok":
                    for det in sam3_result.get("detections", []):
                        bbox = det.get("bbox", [])
                        label = det.get("label", "")
                        score = det.get("score", 0.0)
                        mask_file = det.get("mask_file", "")

                        if len(bbox) == 4:
                            x1, y1, x2, y2 = [int(v) for v in bbox]
                            cv2.rectangle(yolo_display, (x1, y1), (x2, y2), (255, 0, 0), 2)
                            cv2.putText(yolo_display, f"SAM3:{label} {score:.2f}",
                                        (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX,
                                        0.5, (255, 0, 0), 2)

                        if mask_file:
                            try:
                                mask_data = sam3_result.get("mask_bytes", {}).get(mask_file)
                                if mask_data:
                                    mask_arr = np.frombuffer(mask_data, dtype=np.uint8)
                                    mask_img = cv2.imdecode(mask_arr, cv2.IMREAD_GRAYSCALE)
                                    if mask_img is not None and mask_img.shape[:2] == yolo_display.shape[:2]:
                                        colored = np.zeros_like(yolo_display)
                                        colored[:, :, 0] = mask_img  # 蓝色通道
                                        yolo_display = cv2.addWeighted(yolo_display, 1.0, colored, 0.35, 0)
                            except Exception:
                                pass

                # ── 叠加 FlowPose 6D 姿态文字 ──
                if flowpose_result.get("status") == "ok":
                    objects = flowpose_result.get("objects", [])
                    y_offset = 60
                    for obj in objects[:5]:
                        name = obj.get("name", "?")
                        length = obj.get("length", [0, 0, 0])
                        text = f"{name}: {length[0]:.3f}x{length[1]:.3f}x{length[2]:.3f}m"
                        cv2.putText(yolo_display, text, (10, y_offset),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
                        y_offset += 16

                # 添加 SigLIP 简短信息到窗口
                if state_result.get("status") == "ok":
                    best_cat = state_result.get("best_category", "unknown")
                    best_sim = state_result.get("best_similarity", 0.0)
                    h, w = yolo_display.shape[:2]
                    cv2.putText(yolo_display, f"State: {best_cat}",
                                (10, h - 35),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(yolo_display, f"Sim: {best_sim:.3f}",
                                (10, h - 15),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                # 显示窗口
                cv2.imshow(win_title, yolo_display)

                if cv2.waitKey(5) & 0xFF == 27:
                    running = False

            # ── Save ──
            if out_dir and pred.get("status") == "ok" and pred.get("annotated_image"):
                out_path = f"{out_dir}/{frame_id:06d}_annotated.jpg"
                with open(out_path, "wb") as f:
                    f.write(pred["annotated_image"])

            # ── Log ──
            loop_ms = (time.time() - t_loop) * 1000
            if frame_count % log_interval == 0:
                n_det = pred.get("num_detections", 0)
                status = pred.get("status", "?")
                state_cat = state_result.get("best_category", "-")
                state_sim = state_result.get("best_similarity", 0.0)
                if _detector == "yolo":
                    det_tag = f"YOLO={n_det}"
                    det_ms = f"yolo={infer_ms:.1f}ms"
                else:
                    n_det = len(sam3_result.get("detections", []))
                    det_tag = f"SAM3={n_det}"
                    det_ms = f"sam3={sam3_ms:.1f}ms"
                n_poses = len(flowpose_result.get("objects", []))
                ff_str = f"ff={ff_ms:.1f}ms" if _full else ""
                fp_str = f"fp={flowpose_ms:.1f}ms poses={n_poses}" if _full else ""
                print(
                    f"[Frame {frame_id:05d}] {det_tag} | state={state_cat} ({state_sim:.3f}) | "
                    f"{det_ms} {ff_str} {fp_str} siglip={siglip_ms:.1f}ms | loop={loop_ms:.1f}ms | {status}"
                )

            frame_count += 1

    except KeyboardInterrupt:
        print("\n[ControlCenter] Interrupted by user")
    finally:
        cv2.destroyAllWindows()
        print(f"[ControlCenter] Done. Processed {frame_count} frames.")



def main() -> None:
    parser = argparse.ArgumentParser(
        description="MindBridge Control Center — RealSense → YOLO → SigLIP pipeline",
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
        "--siglip-url", default="http://127.0.0.1:8002",
        help="SigLIP 服务地址（默认 :8002）",
    )
    parser.add_argument(
        "--sam3-url", default="http://127.0.0.1:8005",
        help="SAM3 服务地址（默认 :8005）",
    )
    parser.add_argument(
        "--sam3-prompts", type=str, default=None,
        help="SAM3 文本提示，逗号分隔，如 'cat,dog'（默认 ['object']）",
    )
    parser.add_argument(
        "--sam3-threshold", type=float, default=None,
        help="SAM3 置信度阈值，默认使用服务端配置",
    )
    parser.add_argument(
        "--detector", type=str, default="sam3", choices=["yolo", "sam3"],
        help="检测器选择: sam3(默认) 或 yolo",
    )
    parser.add_argument(
        "--pipeline", type=str, default="full", choices=["basic", "full"],
        help="管线模式: full(默认，含 FastFoundation+FlowPose) 或 basic(仅 detection+siglip)",
    )
    parser.add_argument(
        "--fastfoundation-url", default="http://127.0.0.1:8004",
        help="FastFoundation 服务地址（默认 :8004）",
    )
    parser.add_argument(
        "--flowpose-url", default="http://127.0.0.1:8006",
        help="FlowPose 服务地址（默认 :8006）",
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
        siglip_url=args.siglip_url,
        sam3_url=args.sam3_url,
        fastfoundation_url=args.fastfoundation_url,
        flowpose_url=args.flowpose_url,
        detector=args.detector,
        pipeline=args.pipeline,
        sam3_prompts=args.sam3_prompts,
        sam3_threshold=args.sam3_threshold,
        show=not args.no_show,
        max_frames=args.max_frames,
        out_dir=args.out_dir,
        log_interval=args.log_interval,
    )


if __name__ == "__main__":
    main()
