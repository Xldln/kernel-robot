"""MindBridge Client — 纯 raw bytes 传输，零 base64 开销。

所有图片数据通过 multipart/form-data 或 multipart/mixed 传输，
不再使用 base64 编解码。
"""

from __future__ import annotations

import json as _json

import requests

from mindbridge.src.core.tool.multipart import parse_multipart_response


class MindBridgeClient:
    """Control Center 客户端，对接所有推理服务（raw bytes 传输）。"""

    def __init__(
        self,
        realsense_url: str = "http://127.0.0.1:8000",
        yolo_url: str = "http://127.0.0.1:8001",
        siglip_url: str = "http://127.0.0.1:8002",
        sam3_url: str = "http://127.0.0.1:8005",
        fastfoundation_url: str = "http://127.0.0.1:8004",
        flowpose_url: str = "http://127.0.0.1:8006",
    ):
        self.realsense_url = realsense_url.rstrip("/")
        self.yolo_url = yolo_url.rstrip("/")
        self.siglip_url = siglip_url.rstrip("/")
        self.sam3_url = sam3_url.rstrip("/")
        self.fastfoundation_url = fastfoundation_url.rstrip("/")
        self.flowpose_url = flowpose_url.rstrip("/")

    # ── Health ──────────────────────────────────────────────────────

    def health(self, names: set[str] | list[str] | tuple[str, ...] | None = None) -> dict:
        result: dict = {}
        wanted = set(names) if names is not None else None
        for name, url in [
            ("realsense", self.realsense_url),
            ("yolo", self.yolo_url),
            ("siglip", self.siglip_url),
            ("sam3", self.sam3_url),
            ("fastfoundation", self.fastfoundation_url),
            ("flowpose", self.flowpose_url),
        ]:
            if wanted is not None and name not in wanted:
                continue
            try:
                r = requests.get(f"{url}/health", timeout=2)
                payload = r.json()
                if name == "realsense" and payload.get("status") == "ok":
                    info = requests.get(f"{url}/realsense/info", timeout=2)
                    if info.status_code >= 400:
                        result[name] = {
                            "status": "engine_missing",
                            "error": info.text,
                        }
                    else:
                        result[name] = payload
                else:
                    result[name] = payload
            except Exception as e:
                result[name] = {"status": "unreachable", "error": str(e)}
        return result

    # ── RealSense Capture (raw bytes) ────────────────────────────────

    def capture(self) -> dict:
        """采集一帧，返回 raw bytes 图像数据。

        Returns:
            dict with keys:
                status, frame_id, baseline, K (3x3 list),
                color_jpg (bytes), depth_png (bytes),
                ir_left_jpg (bytes | None), ir_right_jpg (bytes | None),
                elapsed_sec
        """
        r = requests.post(f"{self.realsense_url}/realsense/capture/raw", timeout=30)

        status = r.headers.get("X-Status", "error")
        if status == "error":
            return {
                "status": "error",
                "frame_id": int(r.headers.get("X-Frame-Id", 0)),
                "message": r.headers.get("X-Error-Message", "unknown error"),
                "elapsed_sec": float(r.headers.get("X-Elapsed-Sec", 0)),
            }

        _, binary_parts = parse_multipart_response(r.content, r.headers.get("Content-Type", ""))

        try:
            K = _json.loads(r.headers.get("X-K", "[]"))
        except Exception:
            K = []
        try:
            ir_left_K = _json.loads(r.headers.get("X-IR-Left-K", "[]"))
        except Exception:
            ir_left_K = []
        try:
            ir_to_color_R = _json.loads(r.headers.get("X-IR-To-Color-R", "[]"))
        except Exception:
            ir_to_color_R = []
        try:
            ir_to_color_T = _json.loads(r.headers.get("X-IR-To-Color-T", "[]"))
        except Exception:
            ir_to_color_T = []

        return {
            "status": "ok",
            "frame_id": int(r.headers.get("X-Frame-Id", 0)),
            "baseline": float(r.headers.get("X-Baseline", 0)),
            "K": K,
            "ir_left_K": ir_left_K,
            "ir_to_color_R": ir_to_color_R,
            "ir_to_color_T": ir_to_color_T,
            "color_width": int(r.headers.get("X-Color-Width", 0)),
            "color_height": int(r.headers.get("X-Color-Height", 0)),
            "color_jpg": binary_parts.get("color_jpg"),
            "depth_png": binary_parts.get("depth_png"),
            "ir_left_jpg": binary_parts.get("ir_left_jpg"),
            "ir_right_jpg": binary_parts.get("ir_right_jpg"),
            "elapsed_sec": float(r.headers.get("X-Elapsed-Sec", 0)),
        }

    def capture_all(self) -> dict:
        """采集 primary（完整）+ 全部 color-only 相机，单次 multipart。

        Returns:
            dict：包含 capture() 的全部字段，外加
                aux (dict {cam_id: jpg_bytes})        # color-only 相机彩色帧
                aux_cameras (list[{id, name, part}])  # 顺序与名称
                mode (str)
        """
        r = requests.post(f"{self.realsense_url}/realsense/capture/all/raw", timeout=30)

        status = r.headers.get("X-Status", "error")
        if status == "error":
            return {
                "status": "error",
                "frame_id": int(r.headers.get("X-Frame-Id", 0)),
                "message": r.headers.get("X-Error-Message", "unknown error"),
                "elapsed_sec": float(r.headers.get("X-Elapsed-Sec", 0)),
                "aux": {},
                "aux_cameras": [],
            }

        _, binary_parts = parse_multipart_response(r.content, r.headers.get("Content-Type", ""))

        def _hdr_json(name: str):
            try:
                return _json.loads(r.headers.get(name, "[]"))
            except Exception:
                return []

        try:
            aux_cameras = _json.loads(r.headers.get("X-Aux-Cameras", "[]"))
        except Exception:
            aux_cameras = []

        aux: dict[str, bytes] = {}
        for cam in aux_cameras:
            part = cam.get("part") or f"aux_{cam.get('id')}_jpg"
            data = binary_parts.get(part)
            if data is not None:
                aux[cam.get("id")] = data

        return {
            "status": "ok",
            "mode": r.headers.get("X-Mode", "single"),
            "frame_id": int(r.headers.get("X-Frame-Id", 0)),
            "baseline": float(r.headers.get("X-Baseline", 0)),
            "K": _hdr_json("X-K"),
            "ir_left_K": _hdr_json("X-IR-Left-K"),
            "ir_to_color_R": _hdr_json("X-IR-To-Color-R"),
            "ir_to_color_T": _hdr_json("X-IR-To-Color-T"),
            "color_width": int(r.headers.get("X-Color-Width", 0)),
            "color_height": int(r.headers.get("X-Color-Height", 0)),
            "color_jpg": binary_parts.get("color_jpg"),
            "depth_png": binary_parts.get("depth_png"),
            "ir_left_jpg": binary_parts.get("ir_left_jpg"),
            "ir_right_jpg": binary_parts.get("ir_right_jpg"),
            "aux": aux,
            "aux_cameras": aux_cameras,
            "elapsed_sec": float(r.headers.get("X-Elapsed-Sec", 0)),
        }

    # ── YOLO Predict (raw bytes) ─────────────────────────────────────

    def predict(self, image_bytes: bytes, request_id: str = "",
                conf: float | None = None, return_masks: bool = True,
                return_annotated_image: bool = True) -> dict:
        """YOLO 目标检测（raw bytes 传输）。

        Args:
            image_bytes: JPEG/PNG 图像原始字节

        Returns:
            dict with keys: status, num_detections, detections (list of dicts),
            annotated_image (bytes | None), mask_bytes (dict {name: bytes}), elapsed_sec
        """
        files = {"image": ("image.jpg", image_bytes, "image/jpeg")}
        data = {"request_id": request_id, "return_masks": str(return_masks).lower(),
                "return_annotated_image": str(return_annotated_image).lower()}
        if conf is not None:
            data["conf"] = str(conf)

        r = requests.post(f"{self.yolo_url}/infer/predict/raw", files=files, data=data, timeout=30)

        status = r.headers.get("X-Status", "error")
        if status == "error":
            return {
                "status": "error",
                "request_id": request_id,
                "message": r.headers.get("X-Error-Message", "unknown error"),
                "elapsed_sec": float(r.headers.get("X-Elapsed-Sec", 0)),
            }

        json_result, binary_parts = parse_multipart_response(
            r.content, r.headers.get("Content-Type", ""),
        )

        if json_result is None:
            return {"status": "error", "request_id": request_id, "message": "Failed to parse response"}

        json_result["annotated_image"] = binary_parts.get("annotated")
        json_result["mask_bytes"] = {
            k: v for k, v in binary_parts.items() if k.startswith("mask_")
        }
        return json_result

    # ── SigLIP Classify (raw bytes) ──────────────────────────────────

    def classify_state(self, image_bytes: bytes, request_id: str = "") -> dict:
        """SigLIP 状态分类（raw bytes 传输）。

        Args:
            image_bytes: JPEG/PNG 图像原始字节

        Returns:
            dict with keys: status, ok, best_category, best_similarity, topk, total_category, elapsed_sec
        """
        files = {"image": ("image.jpg", image_bytes, "image/jpeg")}
        data = {"request_id": request_id}

        r = requests.post(f"{self.siglip_url}/infer/predict/raw", files=files, data=data, timeout=10)
        r.raise_for_status()
        return r.json()

    # ── SAM3 Detect (raw bytes) ──────────────────────────────────────

    def sam3_detect(self, image_bytes: bytes, prompts: list[str] | None = None,
                    score_threshold: float | None = None, request_id: str = "") -> dict:
        """SAM3 目标检测/分割（raw bytes 传输）。

        Args:
            image_bytes: JPEG/PNG 图像原始字节

        Returns:
            dict with keys: status, detections (list of dicts with mask_file keys),
            mask_bytes (dict {name: bytes}), elapsed_sec
        """
        files = {"image": ("image.jpg", image_bytes, "image/jpeg")}
        data = {"request_id": request_id}
        if prompts is not None:
            data["prompts"] = ",".join(prompts)
        if score_threshold is not None:
            data["score_threshold"] = str(score_threshold)

        r = requests.post(f"{self.sam3_url}/infer/detect/raw", files=files, data=data, timeout=30)

        status = r.headers.get("X-Status", "error")
        if status == "error":
            return {
                "status": "error",
                "request_id": request_id,
                "message": r.headers.get("X-Error-Message", "unknown error"),
                "elapsed_sec": float(r.headers.get("X-Elapsed-Sec", 0)),
            }

        json_result, binary_parts = parse_multipart_response(
            r.content, r.headers.get("Content-Type", ""),
        )

        if json_result is None:
            return {"status": "error", "request_id": request_id, "message": "Failed to parse response"}

        json_result["mask_bytes"] = {
            k: v for k, v in binary_parts.items() if k.startswith("mask_")
        }
        return json_result

    # ── FastFoundation Depth (raw bytes) ─────────────────────────────

    def fastfoundation_depth_raw(self, left_jpg_bytes: bytes, right_jpg_bytes: bytes,
                                 return_depth: bool = True, return_disparity: bool = False,
                                 request_id: str = "", **kwargs) -> dict:
        """双目深度估计（raw bytes 传输，无 base64 开销）。

        Args:
            left_jpg_bytes: 左目图像 JPEG/PNG 二进制数据
            right_jpg_bytes: 右目图像 JPEG/PNG 二进制数据
            **kwargs: 可选参数 (fx, fy, ppx, ppy, baseline_m, valid_iters, z_far, scale 等)

        Returns:
            dict with keys: status, depth_png (bytes), depth_shape, elapsed_sec, message
        """
        files = {
            "left_image": ("left.jpg", left_jpg_bytes, "image/jpeg"),
            "right_image": ("right.jpg", right_jpg_bytes, "image/jpeg"),
        }
        data = {
            "request_id": request_id,
            "return_depth": str(return_depth).lower(),
            "return_disparity": str(return_disparity).lower(),
        }
        for key in ("fx", "fy", "ppx", "ppy", "baseline_m", "valid_iters",
                     "z_far", "scale", "remove_invisible", "return_color_jpg", "jpg_quality",
                     "color_fx", "color_fy", "color_ppx", "color_ppy", "color_width",
                     "color_height", "ir_to_color_R", "ir_to_color_T"):
            if key in kwargs and kwargs[key] is not None:
                value = kwargs[key]
                data[key] = _json.dumps(value) if key in {"ir_to_color_R", "ir_to_color_T"} else str(value)

        r = requests.post(
            f"{self.fastfoundation_url}/infer/stereo/raw",
            files=files, data=data, timeout=30,
        )
        r.raise_for_status()

        status = r.headers.get("X-Status", "error")
        req_id = r.headers.get("X-Request-Id", request_id)
        elapsed = float(r.headers.get("X-Elapsed-Sec", 0))

        if status == "error":
            return {
                "status": "error",
                "request_id": req_id,
                "message": r.headers.get("X-Error-Message", "unknown error"),
                "elapsed_sec": elapsed,
            }

        depth_shape_str = r.headers.get("X-Depth-Shape", "[]")
        try:
            depth_shape = _json.loads(depth_shape_str)
        except Exception:
            depth_shape = []

        return {
            "status": "ok",
            "request_id": req_id,
            "depth_png": r.content,  # 原始 PNG 字节，不再 base64 编码
            "depth_shape": depth_shape,
            "elapsed_sec": elapsed,
        }

    # ── FlowPose Pose (raw bytes) ────────────────────────────────────

    def flowpose_pose(self, rgb_bytes: bytes, depth_bytes: bytes, mask_bytes: bytes,
                      obj_ids: list | None = None, class_names: list[str] | None = None,
                      instance_names: list[str] | None = None,
                      request_id: str = "") -> dict:
        """6D 姿态估计（raw bytes 传输）。

        Args:
            rgb_bytes: RGB 图像原始字节
            depth_bytes: 深度图 16-bit PNG 原始字节
            mask_bytes: 分割掩码 PNG 原始字节

        Returns:
            dict with keys: status, objects (list of pose dicts), elapsed_sec
        """
        if obj_ids is None:
            obj_ids = []
        if class_names is None:
            class_names = []
        if instance_names is None:
            instance_names = []

        files = {
            "rgb_file": ("rgb.jpg", rgb_bytes, "image/jpeg"),
            "depth_file": ("depth.png", depth_bytes, "image/png"),
            "mask_file": ("mask.png", mask_bytes, "image/png"),
        }
        data = {
            "request_id": request_id,
            "obj_ids_json": _json.dumps(obj_ids),
            "class_names_csv": ",".join(class_names),
            "instance_names_csv": ",".join(instance_names),
        }

        r = requests.post(f"{self.flowpose_url}/infer/pose/raw", files=files, data=data, timeout=30)
        r.raise_for_status()
        return r.json()

    def set_flowpose_visualization(self, enabled: bool) -> dict:
        """Enable/disable the FlowPose OpenCV visualization window."""
        value = "true" if enabled else "false"
        r = requests.post(f"{self.flowpose_url}/infer/visualization?enabled={value}", timeout=2)
        r.raise_for_status()
        return r.json()

    # ── Deprecated: base64 wrappers (kept for backward compat) ───────

    def fastfoundation_depth(self, left_image_b64: str, right_image_b64: str,
                             return_depth: bool = True, return_disparity: bool = False,
                             request_id: str = "") -> dict:
        """[DEPRECATED] base64 端点。请使用 fastfoundation_depth_raw()。"""
        import base64 as _b64
        left_bytes = _b64.b64decode(left_image_b64)
        right_bytes = _b64.b64decode(right_image_b64)
        return self.fastfoundation_depth_raw(
            left_bytes, right_bytes,
            return_depth=return_depth, return_disparity=return_disparity,
            request_id=request_id,
        )
