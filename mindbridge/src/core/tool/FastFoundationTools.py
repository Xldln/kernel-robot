"""Fast-Foundation Stereo 工具函数（纯函数，无副作用）"""

from __future__ import annotations

import base64
from pathlib import Path

import cv2
import numpy as np


# ── 图像编解码 ───────────────────────────────────────────────────

def encode_color_jpg(color_bgr: np.ndarray, jpg_quality: int = 90) -> bytes:
    """将 BGR 图像编码为 JPG 字节流"""
    ok, buf = cv2.imencode(".jpg", color_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), int(jpg_quality)])
    if not ok:
        raise RuntimeError("Failed to encode color image to JPG.")
    return buf.tobytes()


def encode_bgr_to_base64_jpg(image_bgr: np.ndarray, quality: int = 90) -> str:
    """将 BGR 图像编码为 base64 JPG 字符串"""
    buf = encode_color_jpg(image_bgr, jpg_quality=quality)
    return base64.b64encode(buf).decode("utf-8")


def decode_bgr_from_base64(image_b64: str) -> np.ndarray:
    """从 base64 字符串解码为 BGR numpy 数组"""
    image_data = base64.b64decode(image_b64)
    image_array = np.frombuffer(image_data, dtype=np.uint8)
    image_bgr = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise ValueError("Failed to decode input image from base64.")
    return image_bgr


def encode_array_to_base64(arr: np.ndarray) -> str:
    """将 numpy 数组编码为 base64 字符串（原始字节）"""
    return base64.b64encode(arr.tobytes()).decode("utf-8")


# ── 深度格式转换 ─────────────────────────────────────────────────

def depth_float_m_to_uint16_mm(depth_m: np.ndarray) -> np.ndarray:
    """把 float32 米制深度转换为 uint16 毫米深度"""
    depth_mm = depth_m.copy()
    depth_mm[~np.isfinite(depth_mm)] = 0
    depth_mm[depth_mm < 0] = 0
    depth_mm = np.clip(depth_mm * 1000.0, 0, 65535).astype(np.uint16)
    return depth_mm


def compute_depth_from_disparity(
    disp: np.ndarray, fx: float, baseline_m: float, z_far: float = 10.0,
) -> np.ndarray:
    """从视差图计算深度图（米）"""
    with np.errstate(divide="ignore", invalid="ignore"):
        depth = fx * baseline_m / disp
    depth = depth.astype(np.float32, copy=False)
    depth[~np.isfinite(depth)] = 0
    depth[depth < 0] = 0
    if z_far > 0:
        depth[depth > z_far] = 0
    return depth


# ── 图像处理 ─────────────────────────────────────────────────────

def ensure_bgr(frame: np.ndarray) -> np.ndarray:
    """确保图像为 BGR 三通道"""
    if frame.ndim == 2:
        return cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    if frame.ndim == 3 and frame.shape[2] == 4:
        return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    return frame


def center_crop(img: np.ndarray, target_w: int, target_h: int) -> np.ndarray:
    """中心裁剪"""
    h, w = img.shape[:2]
    if w < target_w or h < target_h:
        raise ValueError(f"View size {w}x{h} is smaller than crop size {target_w}x{target_h}.")
    x0 = (w - target_w) // 2
    y0 = (h - target_h) // 2
    return img[y0:y0 + target_h, x0:x0 + target_w]


def split_and_crop_quad_views(
    frame: np.ndarray,
    *,
    expected_width: int,
    expected_height: int,
    crop_width: int,
    crop_height: int,
    top_extra_rows: int,
) -> dict[str, np.ndarray]:
    """将四宫格帧切分为四个独立视图并中心裁剪"""
    h, w = frame.shape[:2]
    if w != expected_width or h != expected_height:
        raise ValueError(f"Expected ZMQ frame size {expected_width}x{expected_height}, got {w}x{h}.")

    half_w = w // 2
    half_h = h // 2

    left_eye = frame[0:half_h + top_extra_rows, 0:half_w]
    right_eye = frame[0:half_h + top_extra_rows, half_w:w]
    right_hand = frame[half_h:h, 0:half_w]
    left_hand = frame[half_h:h, half_w:w]

    return {
        "left_eye": center_crop(left_eye, crop_width, crop_height),
        "right_eye": center_crop(right_eye, crop_width, crop_height),
        "right_hand": center_crop(right_hand, crop_width, crop_height),
        "left_hand": center_crop(left_hand, crop_width, crop_height),
    }


def stitch_quad_views(views: dict[str, np.ndarray]) -> np.ndarray:
    """将四个视图拼接为 2x2 网格"""
    top = cv2.hconcat([views["left_eye"], views["right_eye"]])
    bottom = cv2.hconcat([views["right_hand"], views["left_hand"]])
    return cv2.vconcat([top, bottom])


def preprocess_webrtc_frame(frame_bgr: np.ndarray) -> np.ndarray:
    """WebRTC 帧预处理 hook（当前为直通）"""
    return frame_bgr


# ── 相机标定与畸变校正 ───────────────────────────────────────────

def load_quad_calibration(calibration_yaml: str) -> dict[str, dict[str, np.ndarray]]:
    """从 YAML 加载四视图相机标定参数"""
    yaml_path = Path(calibration_yaml).expanduser()
    if not yaml_path.exists():
        raise FileNotFoundError(f"Calibration yaml not found: {yaml_path}")

    fs = cv2.FileStorage(str(yaml_path), cv2.FILE_STORAGE_READ)
    if not fs.isOpened():
        raise RuntimeError(f"Failed to open calibration yaml: {yaml_path}")

    try:
        result: dict[str, dict[str, np.ndarray]] = {}
        for view_name in ("left_eye", "right_eye", "right_hand", "left_hand"):
            k = fs.getNode(f"{view_name}_K").mat()
            d = fs.getNode(f"{view_name}_D").mat()
            if k is None or d is None:
                raise ValueError(f"Calibration yaml missing {view_name}_K or {view_name}_D: {yaml_path}")

            d_flat = d.reshape(-1)
            if d_flat.size < 5:
                raise ValueError(f"{view_name}_D requires at least 5 coeffs, got {d_flat.size}")

            result[view_name] = {
                "K": k.astype(np.float64),
                "D5": d_flat[:5].astype(np.float64),
            }
        return result
    finally:
        fs.release()


def build_undistort_maps(
    k: np.ndarray, d8: np.ndarray, width: int, height: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """为给定相机参数构建畸变校正映射"""
    new_k, _ = cv2.getOptimalNewCameraMatrix(k, d8, (width, height), 0.0)
    map1, map2 = cv2.initUndistortRectifyMap(k, d8, None, new_k, (width, height), cv2.CV_16SC2)
    return map1, map2, new_k


def undistort_quad_views(
    views: dict[str, np.ndarray],
    calib: dict[str, dict[str, np.ndarray]],
    undistort_state: dict,
) -> dict[str, np.ndarray]:
    """对四视图进行畸变校正（带缓存）"""
    undistorted: dict[str, np.ndarray] = {}
    maps_cache = undistort_state.setdefault("maps", {})
    shapes_cache = undistort_state.setdefault("shapes", {})
    new_ks = undistort_state.setdefault("new_k", {})

    for name, img in views.items():
        h, w = img.shape[:2]
        rebuild = name not in maps_cache or shapes_cache.get(name) != (w, h)
        if rebuild:
            map1, map2, new_k = build_undistort_maps(calib[name]["K"], calib[name]["D5"], w, h)
            maps_cache[name] = (map1, map2)
            shapes_cache[name] = (w, h)
            new_ks[name] = new_k.astype(np.float32)

        map1, map2 = maps_cache[name]
        undistorted[name] = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR)

    return undistorted


# ── 可视化 ───────────────────────────────────────────────────────

def build_stereo_vis(
    left_bgr: np.ndarray,
    right_bgr: np.ndarray,
    disparity: np.ndarray | None = None,
) -> np.ndarray:
    """构建左右拼接 + 视差着色可视化图"""
    h, w = left_bgr.shape[:2]
    # 如果右图尺寸不匹配则 resize
    if right_bgr.shape[:2] != (h, w):
        right_bgr = cv2.resize(right_bgr, (w, h))

    top = cv2.hconcat([left_bgr, right_bgr])

    if disparity is not None:
        # 归一化视差用于显示
        disp_display = disparity.copy()
        disp_display[~np.isfinite(disp_display)] = 0
        disp_display[disp_display < 0] = 0
        valid = disp_display > 0
        if valid.any():
            disp_display[valid] = disp_display[valid] / disp_display[valid].max() * 255
        disp_display = disp_display.astype(np.uint8)
        disp_color = cv2.applyColorMap(disp_display, cv2.COLORMAP_JET)
        if disp_color.shape[:2] != (h, w):
            disp_color = cv2.resize(disp_color, (w, h))
        bottom = cv2.hconcat([disp_color, disp_color])
    else:
        bottom = np.zeros_like(top)

    return cv2.vconcat([top, bottom])


def apply_depth_colormap(depth_m: np.ndarray, z_far: float = 10.0) -> np.ndarray:
    """将深度图（米）转换为 JET 着色图用于可视化"""
    depth_display = depth_m.copy()
    depth_display[~np.isfinite(depth_display)] = 0
    depth_display[depth_display < 0] = 0
    if z_far > 0:
        depth_display[depth_display > z_far] = 0
    valid = depth_display > 0
    if valid.any():
        max_val = depth_display[valid].max()
        if max_val > 0:
            depth_display[valid] = depth_display[valid] / max_val * 255
    depth_display = depth_display.astype(np.uint8)
    return cv2.applyColorMap(depth_display, cv2.COLORMAP_JET)
