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
from mindbridge.src.core.service.FusionResultPublisher import FusionResultPublisher
from mindbridge.src.core.service.RGBFrameSource import OpenCVRGBSource, RealSenseRGBSource
from mindbridge.src.core.tool.image import _draw_detections
from mindbridge.src.fusion.ui_client import FusionUiClient


def _build_multiview_jpg(color_jpg: bytes, aux_jpgs: list[bytes]) -> bytes:
    """将 primary 彩色帧与各 color 相机帧横向拼接为一张 JPEG（供 SigLIP 多视角）。

    无 aux 帧时原样返回 color_jpg。
    """
    imgs = []
    for raw in [color_jpg, *aux_jpgs]:
        if not raw:
            continue
        arr = np.frombuffer(raw, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is not None:
            imgs.append(img)
    if len(imgs) <= 1:
        return color_jpg
    h = min(i.shape[0] for i in imgs)
    resized = [cv2.resize(i, (int(i.shape[1] * h / i.shape[0]), h)) for i in imgs]
    montage = cv2.hconcat(resized)
    ok, buf = cv2.imencode(".jpg", montage, [cv2.IMWRITE_JPEG_QUALITY, 90])
    return buf.tobytes() if ok else color_jpg


# Object tracking for box-prompt mode: label -> {"bbox": [x1,y1,x2,y2], "miss_count": int}
_tracked_objects: dict[str, dict] = {}
_TRACK_MAX_MISS = 5  # revert to text prompt after this many consecutive misses


def _get_sam3_prompts(labels: list[str]) -> tuple[list[str], dict[str, list[float]]]:
    """Tracked labels get BOTH text and box prompts.

    Box prompt is spatially constrained and robust to rotation.
    Text prompt runs in parallel — if the object moved beyond the box region,
    text can re-discover it and update the tracking bbox.
    NMS naturally deduplicates overlapping text/box results.
    """
    text_prompts = list(labels)
    box_prompts = {label: _tracked_objects[label]["bbox"]
                   for label in labels if label in _tracked_objects}
    return text_prompts, box_prompts


def _update_tracking(detections: list[dict]):
    """Keep tracking state from current frame detections, age out lost objects."""
    seen = set()
    for det in detections:
        label = det.get("label", "")
        bbox = det.get("bbox", [])
        if len(bbox) == 4:
            _tracked_objects[label] = {"bbox": [float(v) for v in bbox], "miss_count": 0}
            seen.add(label)
    for label in list(_tracked_objects.keys()):
        if label not in seen:
            _tracked_objects[label]["miss_count"] += 1
            if _tracked_objects[label]["miss_count"] > _TRACK_MAX_MISS:
                del _tracked_objects[label]


def _nms_sam3_detections(detections: list, mask_bytes: dict, iou_thresh: float = 0.5):
    """Simple NMS: keep highest-score box for overlapping pairs across all labels."""
    if len(detections) <= 1:
        return detections, mask_bytes

    boxes = np.array([[
        float(d.get("bbox", [0, 0, 0, 0])[j]) for j in range(4)
    ] for d in detections])
    scores = np.array([float(d.get("score", 0.0)) for d in detections])

    order = scores.argsort()[::-1]
    keep = []
    while len(order) > 0:
        idx = order[0]
        keep.append(idx)
        if len(order) == 1:
            break
        x1 = np.maximum(boxes[idx, 0], boxes[order[1:], 0])
        y1 = np.maximum(boxes[idx, 1], boxes[order[1:], 1])
        x2 = np.minimum(boxes[idx, 2], boxes[order[1:], 2])
        y2 = np.minimum(boxes[idx, 3], boxes[order[1:], 3])
        inter = np.maximum(0, x2 - x1) * np.maximum(0, y2 - y1)
        area = (boxes[order[1:], 2] - boxes[order[1:], 0]) * (boxes[order[1:], 3] - boxes[order[1:], 1])
        area_idx = (boxes[idx, 2] - boxes[idx, 0]) * (boxes[idx, 3] - boxes[idx, 1])
        iou = inter / (area + area_idx - inter + 1e-6)
        order = order[1:][iou <= iou_thresh]

    filtered_dets = [detections[i] for i in keep]
    filtered_masks = {}
    for det in filtered_dets:
        mf = det.get("mask_file", "")
        if mf and mf in mask_bytes:
            filtered_masks[mf] = mask_bytes[mf]

    return filtered_dets, filtered_masks


def _build_labeled_multiview_jpg(views: list[tuple[str, bytes]]) -> bytes:
    """Build a horizontally stitched JPEG with per-view labels for UI display."""
    imgs: list[np.ndarray] = []
    labels: list[str] = []
    for label, raw in views:
        if not raw:
            continue
        arr = np.frombuffer(raw, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is not None:
            imgs.append(img)
            labels.append(label)
    if not imgs:
        return b""
    h = min(i.shape[0] for i in imgs)
    resized = [cv2.resize(i, (int(i.shape[1] * h / i.shape[0]), h)) for i in imgs]
    labeled = []
    for label, img in zip(labels, resized):
        canvas = img.copy()
        cv2.rectangle(canvas, (0, 0), (canvas.shape[1], 28), (0, 0, 0), -1)
        cv2.putText(canvas, label, (8, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
        labeled.append(canvas)
    montage = cv2.hconcat(labeled)
    ok, buf = cv2.imencode(".jpg", montage, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return buf.tobytes() if ok else b""


def _build_siglip_multiview_vis_jpg(
    primary_jpg: bytes,
    aux_views: list[tuple[str, bytes]],
    *,
    expected_views: int = 3,
) -> bytes:
    """Build the SigLIP UI montage, including placeholders for missing aux views."""
    decoded: list[tuple[str, np.ndarray]] = []
    for label, raw in [("Primary", primary_jpg), *aux_views]:
        if not raw:
            continue
        arr = np.frombuffer(raw, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is not None:
            decoded.append((label, img))

    if not decoded:
        return b""

    ref_h, ref_w = decoded[0][1].shape[:2]
    while len(decoded) < expected_views:
        missing_idx = len(decoded) + 1
        placeholder = np.zeros((ref_h, ref_w, 3), dtype=np.uint8)
        cv2.putText(
            placeholder,
            f"Missing view {missing_idx}",
            (24, max(40, ref_h // 2)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (180, 180, 180),
            2,
        )
        decoded.append((f"Missing {missing_idx}", placeholder))

    h = min(img.shape[0] for _, img in decoded)
    labeled = []
    for label, img in decoded[:expected_views]:
        resized = cv2.resize(img, (int(img.shape[1] * h / img.shape[0]), h))
        canvas = resized.copy()
        cv2.rectangle(canvas, (0, 0), (canvas.shape[1], 28), (0, 0, 0), -1)
        cv2.putText(canvas, label, (8, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
        labeled.append(canvas)

    montage = cv2.hconcat(labeled)
    ok, buf = cv2.imencode(".jpg", montage, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return buf.tobytes() if ok else b""


def _ordered_aux_jpgs(cap: dict) -> list[tuple[str, bytes]]:
    """Return aux camera JPEGs in the order declared by RealSense metadata."""
    aux_frames = cap.get("aux") or {}
    aux_meta = cap.get("aux_cameras") or []
    ordered: list[tuple[str, bytes]] = []
    seen: set[str] = set()
    for item in aux_meta:
        cam_id = str(item.get("id", ""))
        data = aux_frames.get(cam_id)
        if data:
            ordered.append((item.get("name") or cam_id, data))
            seen.add(cam_id)
    for cam_id, data in aux_frames.items():
        if cam_id not in seen and data:
            ordered.append((cam_id, data))
    return ordered


def run(
    realsense_url: str = "http://127.0.0.1:8000",
    yolo_url: str = "http://127.0.0.1:8001",
    siglip_url: str = "http://127.0.0.1:8002",
    sam3_url: str = "http://127.0.0.1:8005",
    fastfoundation_url: str = "http://127.0.0.1:8004",
    flowpose_url: str = "http://127.0.0.1:8006",
    rgb_source: str = "realsense",
    camera_mode: str = "multi",      # "single" | "multi"
    camera_index: int = 0,
    camera_width: Optional[int] = None,
    camera_height: Optional[int] = None,
    camera_fps: Optional[int] = None,
    detector: str = "sam3",           # "sam3" | "yolo"
    pipeline: str = "full",           # "full" | "basic"
    mode: str = "pipeline",           # "pipeline" | "yolo-only" | "sam3-only" | "siglip-only" | "flowpose-only"
    sam3_prompts: Optional[str] = None,
    sam3_threshold: Optional[float] = None,
    show: bool = True,
    max_frames: Optional[int] = None,
    out_dir: Optional[str] = None,
    log_interval: int = 30,
    fastfoundation_interval: int = 3,
    flowpose_interval: int = 3,
    siglip_interval: int = 1,
    fusion_ui_interval: int = 3,
    fusion_pub: bool = False,
    fusion_pub_addr: str = "tcp://0.0.0.0:8899",
    fusion_ui_url: Optional[str] = None,
) -> None:
    client = MindBridgeClient(realsense_url, yolo_url, siglip_url, sam3_url, fastfoundation_url, flowpose_url)
    _sam3_prompts = [p.strip() for p in sam3_prompts.split(",")] if sam3_prompts else None
    _detector = detector.lower()
    _full = pipeline.lower() == "full"
    _mode = mode.lower()
    _rgb_source = rgb_source.lower()
    _camera_mode = camera_mode.lower()
    if _detector not in ("yolo", "sam3"):
        raise ValueError(f"detector must be 'yolo' or 'sam3', got '{detector}'")
    if _mode not in ("pipeline", "yolo-only", "sam3-only", "siglip-only", "flowpose-only"):
        raise ValueError(f"mode must be pipeline/yolo-only/sam3-only/siglip-only/flowpose-only, got '{mode}'")
    if _rgb_source not in ("realsense", "usb"):
        raise ValueError(f"rgb_source must be 'realsense' or 'usb', got '{rgb_source}'")
    if _camera_mode not in ("single", "multi"):
        raise ValueError(f"camera_mode must be 'single' or 'multi', got '{camera_mode}'")
    if _camera_mode == "multi" and _rgb_source != "realsense":
        print("[ControlCenter] camera-mode=multi only applies to realsense source; ignoring")
        _camera_mode = "single"
    if _rgb_source == "usb" and _full:
        print("[ControlCenter] USB RGB source does not provide stereo/depth; using BASIC pipeline")
        _full = False

    if _mode == "yolo-only":
        _detector = "yolo"
        _full = False
    elif _mode == "sam3-only":
        _detector = "sam3"
        _full = False
    elif _mode == "flowpose-only":
        _full = True

    print(f"[ControlCenter] Mode: {_mode} | Pipeline: {'FULL' if _full else 'BASIC'} | "
          f"Detector: {_detector.upper()} | Camera: {_camera_mode}")
    if _rgb_source == "realsense":
        frame_source = RealSenseRGBSource(client, multi=(_camera_mode == "multi"))
        require_rs = True
    else:
        frame_source = OpenCVRGBSource(
            camera_index,
            width=camera_width,
            height=camera_height,
            fps=camera_fps,
        )
        require_rs = False

    required_services = set()
    if require_rs:
        required_services.add("realsense")
    if _mode == "yolo-only":
        required_services.add("yolo")
    elif _mode == "sam3-only":
        required_services.add("sam3")
    elif _mode == "siglip-only":
        required_services.add("siglip")
    elif _mode == "flowpose-only":
        required_services.update({"fastfoundation", "flowpose"})
    elif _mode == "pipeline":
        required_services.add(_detector)
        required_services.add("siglip")
        if _full:
            required_services.update({"fastfoundation", "flowpose"})

    print("[ControlCenter] Waiting for services ...")
    for attempt in range(60):
        h = client.health(required_services)
        rs_ok = h.get("realsense", {}).get("status") == "ok" if require_rs else True
        yolo_ok = h.get("yolo", {}).get("status") == "ok" if "yolo" in required_services else True
        siglip_ok = h.get("siglip", {}).get("status") == "ok" if "siglip" in required_services else True
        sam3_ok = h.get("sam3", {}).get("status") == "ok" if "sam3" in required_services else True

        ff_ok = h.get("fastfoundation", {}).get("status") == "ok" if _full else True
        fp_ok = h.get("flowpose", {}).get("status") == "ok" if _full else True

        if _mode == "yolo-only" and rs_ok and yolo_ok:
            print("[ControlCenter] All services ready (YOLO only)")
            break
        elif _mode == "sam3-only" and rs_ok and sam3_ok:
            print("[ControlCenter] All services ready (SAM3 only)")
            break
        elif _mode == "siglip-only" and rs_ok and siglip_ok:
            print("[ControlCenter] All services ready (SigLIP only)")
            break
        elif _mode == "flowpose-only" and rs_ok and ff_ok and fp_ok:
            print("[ControlCenter] All services ready (FlowPose only)")
            break
        elif _mode == "pipeline" and _detector == "yolo" and rs_ok and yolo_ok and siglip_ok and ff_ok and fp_ok:
            print(f"[ControlCenter] All services ready (YOLO {'full' if _full else 'basic'} pipeline)")
            break
        elif _mode == "pipeline" and _detector == "sam3" and rs_ok and sam3_ok and siglip_ok and ff_ok and fp_ok:
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
    fastfoundation_interval = max(1, int(fastfoundation_interval))
    flowpose_interval = max(1, int(flowpose_interval))
    siglip_interval = max(1, int(siglip_interval))
    fusion_ui_interval = max(1, int(fusion_ui_interval))
    last_depth_png: bytes | None = None
    last_flowpose_result: dict = {}
    last_state_result: dict = {}
    siglip_win_title = ""

    def _close_flowpose_visualization() -> None:
        try:
            client.set_flowpose_visualization(False)
        except Exception:
            pass

    print("[ControlCenter] Starting capture → inference → classification loop ...")
    if _full:
        print(
            "[ControlCenter] Full pipeline intervals: "
            f"FastFoundation={fastfoundation_interval}, "
            f"FlowPose={flowpose_interval}, SigLIP={siglip_interval}"
        )

    if show:
        if not os.environ.get("DISPLAY"):
            print("[ControlCenter] DISPLAY is not set; OpenCV window disabled")
            show = False
        else:
            win_title = f"MindBridge {_mode if _mode != 'pipeline' else _detector.upper()}"
            cv2.namedWindow(win_title, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(win_title, 640, 480)
            if _camera_mode == "multi":
                siglip_win_title = "SigLIP MultiView"
                cv2.namedWindow(siglip_win_title, cv2.WINDOW_NORMAL)
                cv2.resizeWindow(siglip_win_title, 960, 320)

    fusion_publisher = None
    if fusion_pub:
        try:
            fusion_publisher = FusionResultPublisher(fusion_pub_addr)
            print(f"[ControlCenter] Fusion ZMQ publisher: {fusion_pub_addr}")
        except Exception as e:
            print(f"[ControlCenter] Fusion ZMQ publisher disabled: {e}")

    fusion_ui_client = FusionUiClient(fusion_ui_url) if fusion_ui_url else None

    try:
        while running:
            if max_frames is not None and frame_count >= max_frames:
                break

            t_loop = time.time()

            # ── Step 1: Capture from RealSense (raw bytes) ──
            try:
                cap = frame_source.capture()
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
            color_arr = np.frombuffer(color_jpg, dtype=np.uint8)
            original_rgb = cv2.imdecode(color_arr, cv2.IMREAD_COLOR)
            aux_view_jpgs = _ordered_aux_jpgs(cap) if _camera_mode == "multi" else []
            if _camera_mode == "multi" and frame_count % log_interval == 0 and len(aux_view_jpgs) < 2:
                print(
                    "[ControlCenter] WARNING: Camera=multi but aux views missing "
                    f"(got {len(aux_view_jpgs)} aux views, expected 2)."
                )
            siglip_multiview_jpg = (
                _build_multiview_jpg(color_jpg, [raw for _, raw in aux_view_jpgs])
                if aux_view_jpgs else color_jpg
            )

            # ── Step 2: SigLIP state classification (run early for low-latency state) ──
            state_result = last_state_result if _mode == "pipeline" else {}
            siglip_ms = 0.0
            run_siglip = (
                _mode == "siglip-only"
                or (
                    _mode == "pipeline"
                    and (frame_count == 0 or frame_count % siglip_interval == 0 or not last_state_result)
                )
            )
            if run_siglip:
                t_siglip_start = time.time()
                siglip_input = siglip_multiview_jpg if _camera_mode == "multi" else color_jpg
                try:
                    state_result = client.classify_state(siglip_input, request_id=str(frame_id))
                    if _mode == "pipeline":
                        last_state_result = state_result
                except Exception as e:
                    print(f"[ControlCenter] SigLIP classification failed: {e}")
                    state_result = {"status": "error", "best_category": "", "best_similarity": 0.0}
                siglip_ms = (time.time() - t_siglip_start) * 1000

            # 每帧都发布 siglip 结果（含跳帧时的缓存值），避免 ZMQ 空洞导致 watcher 断流
            if fusion_publisher and state_result:
                try:
                    fusion_publisher.publish_siglip(
                        frame_id=frame_id,
                        state_result=state_result,
                    )
                except Exception as e:
                    print(f"[ControlCenter] SigLIP publish failed: {e}")

            # ── Step 3 (full only): FastFoundation stereo depth ──
            ff_result: dict = {}
            ff_ms = 0.0
            depth_png_for_flowpose: bytes | None = cap.get("depth_png")
            if _full:
                ir_left_jpg = cap.get("ir_left_jpg")
                ir_right_jpg = cap.get("ir_right_jpg")
                run_ff = frame_count == 0 or frame_count % fastfoundation_interval == 0 or last_depth_png is None
                if ir_left_jpg and ir_right_jpg and run_ff:
                    t_ff = time.time()
                    try:
                        ff_result = client.fastfoundation_depth_raw(
                            ir_left_jpg, ir_right_jpg,
                            return_depth=True,
                            request_id=str(frame_id),
                            fx=cap["ir_left_K"][0][0] if cap.get("ir_left_K") else None,
                            fy=cap["ir_left_K"][1][1] if cap.get("ir_left_K") else None,
                            ppx=cap["ir_left_K"][0][2] if cap.get("ir_left_K") else None,
                            ppy=cap["ir_left_K"][1][2] if cap.get("ir_left_K") else None,
                            baseline_m=cap.get("baseline"),
                            color_fx=cap["K"][0][0] if cap.get("K") else None,
                            color_fy=cap["K"][1][1] if cap.get("K") else None,
                            color_ppx=cap["K"][0][2] if cap.get("K") else None,
                            color_ppy=cap["K"][1][2] if cap.get("K") else None,
                            color_width=cap.get("color_width"),
                            color_height=cap.get("color_height"),
                            ir_to_color_R=cap.get("ir_to_color_R"),
                            ir_to_color_T=cap.get("ir_to_color_T"),
                        )
                        # NOTE: RealSense hardware depth is already aligned to color and
                        # more complete than FastFoundation's stereo depth for FlowPose.
                        # If you want to use FastFoundation depth instead, uncomment below:
                        # if ff_result.get("status") == "ok" and ff_result.get("depth_png"):
                        #     depth_png_for_flowpose = ff_result["depth_png"]
                        #     last_depth_png = depth_png_for_flowpose
                    except Exception as e:
                        print(f"[ControlCenter] FastFoundation failed: {e}")
                    ff_ms = (time.time() - t_ff) * 1000
                # elif last_depth_png is not None:
                #     depth_png_for_flowpose = last_depth_png

            # ── Step 4: Detection (YOLO or SAM3, mutually exclusive) ──
            pred: dict = {"status": "ok", "num_detections": 0, "detections": [],
                          "annotated_image": None, "mask_bytes": {}}
            sam3_result: dict = {"status": "ok", "detections": [], "mask_bytes": {}}
            infer_ms = 0.0
            sam3_ms = 0.0

            if _mode in ("pipeline", "yolo-only") and _detector == "yolo":
                t_infer_start = time.time()
                try:
                    pred = client.predict(color_jpg, request_id=str(frame_id))
                except Exception as e:
                    print(f"[ControlCenter] YOLO inference failed: {e}")
                    pred = {"status": "error", "num_detections": 0, "detections": [],
                            "annotated_image": None, "mask_bytes": {}}
                infer_ms = (time.time() - t_infer_start) * 1000

            elif _mode in ("pipeline", "sam3-only") and _detector == "sam3":
                t_sam3_start = time.time()
                try:
                    text_prompts, box_prompts = _get_sam3_prompts(_sam3_prompts)
                    sam3_result = client.sam3_detect(
                        color_jpg,
                        prompts=text_prompts,
                        score_threshold=sam3_threshold,
                        request_id=str(frame_id),
                        box_prompts=box_prompts if box_prompts else None,
                    )
                    if sam3_result.get("status") == "ok":
                        _update_tracking(sam3_result.get("detections", []))
                except Exception as e:
                    print(f"[ControlCenter] SAM3 inference failed: {e}")
                    sam3_result = {"status": "error", "detections": [], "mask_bytes": {}}
                sam3_ms = (time.time() - t_sam3_start) * 1000

            # ── Step 5 (full only): FlowPose 6D pose estimation ──
            flowpose_result: dict = last_flowpose_result if _full else {}
            flowpose_ms = 0.0
            run_flowpose = (
                _full
                and depth_png_for_flowpose
                and (frame_count == 0 or frame_count % flowpose_interval == 0 or not last_flowpose_result)
            )
            if run_flowpose:
                # 从检测结果构建合并 mask（多个物体的 mask 合并为一张图）
                masks_to_combine: list[np.ndarray] = []
                obj_ids_for_flowpose = []
                class_names_for_flowpose = []

                def _collect_masks(detections: list, mask_bytes_dict: dict, is_yolo: bool = False):
                    for i, det in enumerate(detections):
                        mask_file = det.get("mask_file", "")
                        if mask_file:
                            mask_data = mask_bytes_dict.get(mask_file)
                            if mask_data:
                                mask_arr = np.frombuffer(mask_data, dtype=np.uint8)
                                mask_img = cv2.imdecode(mask_arr, cv2.IMREAD_GRAYSCALE)
                                if mask_img is not None:
                                    masks_to_combine.append(mask_img)
                                obj_id = det.get("id", i + 1) if not is_yolo else (i + 1)
                                obj_ids_for_flowpose.append([obj_id, obj_id])
                                class_names_for_flowpose.append(
                                    det.get("class_name", det.get("label", "object"))
                                )

                mask_bytes_for_flowpose: bytes | None = None
                if _mode == "flowpose-only" and original_rgb is not None:
                    mask = np.ones(original_rgb.shape[:2], dtype=np.uint8)
                    ok, whole_mask_png = cv2.imencode(".png", mask, [cv2.IMWRITE_PNG_COMPRESSION, 3])
                    if ok:
                        mask_bytes_for_flowpose = whole_mask_png.tobytes()
                        obj_ids_for_flowpose.append([1, 1])
                        class_names_for_flowpose.append("object")
                elif _detector == "sam3" and sam3_result.get("status") == "ok":
                    # NMS dedup: keep highest-score box for overlapping detections
                    sam3_dets = sam3_result.get("detections", [])
                    sam3_masks = sam3_result.get("mask_bytes", {})
                    if len(sam3_dets) > 1:
                        sam3_dets, sam3_masks = _nms_sam3_detections(sam3_dets, sam3_masks)
                        sam3_result["detections"] = sam3_dets
                        sam3_result["mask_bytes"] = sam3_masks
                    _collect_masks(sam3_dets, sam3_masks)
                elif _detector == "yolo" and pred.get("status") == "ok":
                    _collect_masks(pred.get("detections", []), pred.get("mask_bytes", {}), is_yolo=True)

                # 合并所有 mask 为一张图，每个物体分配不同值（0=背景，1,2,3...=各物体）
                # FlowPose 通过 obj_ids 中的 mask_value 区分不同物体
                if mask_bytes_for_flowpose is None and masks_to_combine:
                    combined_mask = np.zeros_like(masks_to_combine[0], dtype=np.uint8)
                    for idx, m in enumerate(masks_to_combine):
                        obj_val = idx + 1  # 物体 1、2、3... 对应 mask 值 1、2、3...
                        combined_mask[m > 0] = obj_val
                    ok, combined_png = cv2.imencode(".png", combined_mask, [cv2.IMWRITE_PNG_COMPRESSION, 3])
                    if ok:
                        mask_bytes_for_flowpose = combined_png.tobytes()

                if mask_bytes_for_flowpose and depth_png_for_flowpose:
                    t_fp = time.time()
                    try:
                        flowpose_result = client.flowpose_pose(
                            color_jpg, depth_png_for_flowpose, mask_bytes_for_flowpose,
                            obj_ids=obj_ids_for_flowpose,
                            class_names=class_names_for_flowpose,
                            request_id=str(frame_id),
                        )
                        last_flowpose_result = flowpose_result
                    except Exception as e:
                        print(f"[ControlCenter] FlowPose failed: {e}")
                    flowpose_ms = (time.time() - t_fp) * 1000

            yolo_display = None

            if show or fusion_ui_client:
                if original_rgb is not None:
                    yolo_display = original_rgb.copy()
                if pred.get("status") == "ok" and pred.get("annotated_image"):
                    ann_arr = np.frombuffer(pred["annotated_image"], dtype=np.uint8)
                    yolo_display = cv2.imdecode(ann_arr, cv2.IMREAD_COLOR)
                elif original_rgb is not None:
                    yolo_display = _draw_detections(
                        original_rgb.copy(),
                        pred.get("detections", []),
                    )

                if yolo_display is not None and sam3_result.get("status") == "ok":
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
                                        colored[:, :, 0] = mask_img
                                        yolo_display = cv2.addWeighted(yolo_display, 1.0, colored, 0.35, 0)
                            except Exception:
                                pass

                if yolo_display is not None and state_result.get("status") == "ok":
                    best_cat = state_result.get("best_category", "unknown")
                    best_sim = state_result.get("best_similarity", 0.0)
                    h, _w = yolo_display.shape[:2]
                    cv2.putText(yolo_display, f"State: {best_cat}",
                                (10, h - 35),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(yolo_display, f"Sim: {best_sim:.3f}",
                                (10, h - 15),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                if yolo_display is not None and _mode == "flowpose-only":
                    n_poses = len(flowpose_result.get("objects", []))
                    msg = flowpose_result.get("message") or f"poses={n_poses}"
                    cv2.putText(yolo_display, f"FlowPose: {msg}",
                                (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 180, 255), 2)

            if fusion_publisher:
                try:
                    fusion_publisher.publish_tf(
                        frame_id=frame_id,
                        flowpose_result=flowpose_result,
                    )
                except Exception as e:
                    print(f"[ControlCenter] TF publish failed: {e}")

            siglip_vis_jpg = b""
            if _camera_mode == "multi":
                siglip_vis_jpg = (
                    _build_siglip_multiview_vis_jpg(
                        color_jpg,
                        aux_view_jpgs,
                        expected_views=3,
                    )
                    or siglip_multiview_jpg
                )

            if show:
                if _camera_mode == "multi" and siglip_vis_jpg:
                    siglip_arr = np.frombuffer(siglip_vis_jpg, dtype=np.uint8)
                    siglip_display = cv2.imdecode(siglip_arr, cv2.IMREAD_COLOR)
                    if siglip_display is not None:
                        cv2.imshow(siglip_win_title, siglip_display)
                if yolo_display is not None:
                    cv2.imshow(win_title, yolo_display)
                key = cv2.waitKey(5)
                if key >= 0 and (key & 0xFF) == 27:
                    _close_flowpose_visualization()
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
                if _mode == "siglip-only":
                    det_tag = "SigLIP"
                    det_ms = ""
                    status = state_result.get("status", "?")
                elif _mode == "flowpose-only":
                    det_tag = f"FlowPose={len(flowpose_result.get('objects', []))}"
                    det_ms = ""
                    status = flowpose_result.get("status", "?")
                elif _detector == "yolo":
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
        frame_source.close()
        if fusion_publisher:
            fusion_publisher.close()
        _close_flowpose_visualization()
        if show:
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
        "--mode",
        type=str,
        default="pipeline",
        choices=["pipeline", "yolo-only", "sam3-only", "siglip-only", "flowpose-only"],
        help="运行模式: pipeline 或单模型可视化模式",
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
        "--rgb-source", choices=["realsense", "usb"], default="realsense",
        help="RGB 来源: realsense(默认) 或 usb",
    )
    parser.add_argument(
        "--camera-mode", choices=["single", "multi"], default="multi",
        help="RealSense 相机模式: single(默认) 或 multi(primary 完整 + 其余仅彩色，拼接送 SigLIP)",
    )
    parser.add_argument("--camera-index", type=int, default=0, help="USB 摄像头编号")
    parser.add_argument("--camera-width", type=int, default=None, help="USB 摄像头宽度")
    parser.add_argument("--camera-height", type=int, default=None, help="USB 摄像头高度")
    parser.add_argument("--camera-fps", type=int, default=None, help="USB 摄像头 FPS")
    show_group = parser.add_mutually_exclusive_group()
    show_group.add_argument(
        "--show", action="store_true",
        help="显示 OpenCV 窗口",
    )
    show_group.add_argument(
        "--no-show", action="store_true",
        help="不显示 OpenCV 窗口（无头模式）",
    )
    parser.add_argument(
        "--fusion-pub", action="store_true",
        help="发布 Fusion ZMQ 结果",
    )
    parser.add_argument(
        "--fusion-pub-addr", default="tcp://0.0.0.0:8899",
        help="Fusion ZMQ PUB 地址",
    )
    parser.add_argument(
        "--fusion-ui-url", default=None,
        help="Fusion UI 地址，用于推送视频帧",
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
    parser.add_argument(
        "--fastfoundation-interval", type=int, default=3,
        help="Full 模式下 FastFoundation 运行间隔帧数，默认 3",
    )
    parser.add_argument(
        "--flowpose-interval", type=int, default=3,
        help="Full 模式下 FlowPose 运行间隔帧数，默认 3",
    )
    parser.add_argument(
        "--siglip-interval", type=int, default=1,
        help="Pipeline 模式下 SigLIP 运行间隔帧数，默认 1",
    )
    parser.add_argument(
        "--fusion-ui-interval", type=int, default=3,
        help="Fusion UI 视频推流间隔帧数，默认 3（越大越省带宽/CPU）",
    )

    args = parser.parse_args()

    run(
        realsense_url=args.realsense_url,
        yolo_url=args.yolo_url,
        siglip_url=args.siglip_url,
        sam3_url=args.sam3_url,
        fastfoundation_url=args.fastfoundation_url,
        flowpose_url=args.flowpose_url,
        rgb_source=args.rgb_source,
        camera_mode=args.camera_mode,
        camera_index=args.camera_index,
        camera_width=args.camera_width,
        camera_height=args.camera_height,
        camera_fps=args.camera_fps,
        detector=args.detector,
        pipeline=args.pipeline,
        mode=args.mode,
        sam3_prompts=args.sam3_prompts,
        sam3_threshold=args.sam3_threshold,
        show=not args.no_show,
        max_frames=args.max_frames,
        out_dir=args.out_dir,
        log_interval=args.log_interval,
        fastfoundation_interval=args.fastfoundation_interval,
        flowpose_interval=args.flowpose_interval,
        siglip_interval=args.siglip_interval,
        fusion_ui_interval=args.fusion_ui_interval,
        fusion_pub=args.fusion_pub,
        fusion_pub_addr=args.fusion_pub_addr,
        fusion_ui_url=args.fusion_ui_url,
    )


if __name__ == "__main__":
    main()
