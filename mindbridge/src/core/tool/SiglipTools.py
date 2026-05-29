"""LAST-ViT 纯工具函数（无状态、无模型依赖）"""

from __future__ import annotations

import ast
import base64
import json
from io import BytesIO
from urllib import error, request

import cv2
import numpy as np
from PIL import Image


# ─── 图像编解码 ───────────────────────────────────────────────────

def decode_image_b64_to_pil(image_b64: str) -> Image.Image:
    """base64 → PIL RGB"""
    try:
        image_bytes = base64.b64decode(image_b64)
    except Exception as e:
        raise ValueError(f"图片 base64 解码失败: {e}") from e
    try:
        return Image.open(BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        raise ValueError(f"图片解码失败: {e}") from e


def decode_image_b64_to_bgr(image_b64: str) -> np.ndarray:
    """base64 → OpenCV BGR"""
    try:
        image_bytes = base64.b64decode(image_b64)
    except Exception as e:
        raise ValueError(f"图片 base64 解码失败: {e}") from e
    img_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image_bgr = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise ValueError("OpenCV 图片解码失败")
    return image_bgr


def encode_image_bytes_to_base64(image_bytes: bytes) -> str:
    """bytes → base64 string"""
    return base64.b64encode(image_bytes).decode("utf-8")


# ─── 图像预处理 ───────────────────────────────────────────────────

def apply_padding_head(image: Image.Image) -> Image.Image:
    """将图像顶部 25% 区域填充为黑色（消除头部干扰）"""
    w, h = image.size
    cutoff = int(h * 0.25)
    if cutoff <= 0:
        return image
    pixels = image.load()
    for y in range(cutoff):
        for x in range(w):
            pixels[x, y] = (0, 0, 0)
    return image


# ─── 向量 / 特征处理 ─────────────────────────────────────────────

def parse_center_feature(value) -> np.ndarray:
    """解析 center feature，支持 JSON / literal_eval，并 L2 归一化"""
    if isinstance(value, str):
        text = value.strip()
        try:
            value = json.loads(text)
        except Exception:
            value = ast.literal_eval(text)

    arr = np.array(value, dtype=np.float32)
    if arr.ndim != 1:
        raise ValueError(f"center feature 必须为 1D，当前 shape={arr.shape}")

    norm = np.linalg.norm(arr)
    if norm > 0:
        arr = arr / norm
    return arr


def calculate_similarity(feat_np: np.ndarray, centers: dict, topk: int = 5):
    """计算特征与所有类中心的余弦相似度，返回 best + topk"""
    sims = {k: float(np.dot(feat_np, v)) for k, v in centers.items()}
    best = max(sims.items(), key=lambda x: x[1])
    topk_items = sorted(sims.items(), key=lambda x: x[1], reverse=True)[:topk]

    return {
        "ok": True,
        "best_category": best[0],
        "best_similarity": best[1],
        "topk": [{"category": k, "similarity": v} for k, v in topk_items],
    }


def get_current_state_id(result: dict, states: list) -> str | None:
    """从推理结果中解析当前命中的 state ID"""
    if not result or not result.get("ok"):
        return None

    category = str(result.get("best_category", "")).strip()
    if not category:
        return None

    if ":" in category:
        maybe_id = category.split(":", 1)[0].strip()
        if any(str(s.get("id", "")) == maybe_id for s in states):
            return maybe_id

    for state in states:
        if str(state.get("name", "")).strip() == category:
            return str(state.get("id", ""))
    for state in states:
        if str(state.get("category", "")).strip() == category:
            return str(state.get("id", ""))
    return None


# ─── 可视化 ──────────────────────────────────────────────────────

def create_state_diagram(
    states: list, current_state_id: str | None = None,
    width: int = 640, height: int = 400,
) -> np.ndarray:
    """生成状态节点环形图 + 右侧列表"""
    diagram = np.ones((height, width, 3), dtype=np.uint8) * 255
    if not states:
        cv2.putText(diagram, "No states loaded", (20, height // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (90, 90, 90), 2, cv2.LINE_AA)
        return diagram

    n_states = len(states)
    split_x = int(width * 0.56)
    cv2.line(diagram, (split_x, 10), (split_x, height - 10), (220, 220, 220), 1)

    left_w = split_x
    cx, cy = left_w // 2, height // 2
    rx = int(left_w * 0.33)
    ry = int(height * 0.30)
    node_r = 20

    positions = []
    for i in range(n_states):
        angle = -90 + (360.0 * i / n_states)
        rad = np.deg2rad(angle)
        x = int(cx + rx * np.cos(rad))
        y = int(cy + ry * np.sin(rad))
        positions.append((x, y))

    for i in range(n_states):
        x1, y1 = positions[i]
        x2, y2 = positions[(i + 1) % n_states]
        cv2.line(diagram, (x1, y1), (x2, y2), (205, 205, 205), 2)

        dx, dy = x2 - x1, y2 - y1
        dist = max(np.hypot(dx, dy), 1e-6)
        ex = int(x2 - dx / dist * node_r)
        ey = int(y2 - dy / dist * node_r)
        sx = int(x2 - dx / dist * (node_r + 8))
        sy = int(y2 - dy / dist * (node_r + 8))
        px = int(-dy / dist * 6)
        py = int(dx / dist * 6)
        cv2.line(diagram, (sx - px, sy - py), (ex, ey), (165, 165, 165), 2)
        cv2.line(diagram, (sx + px, sy + py), (ex, ey), (165, 165, 165), 2)

    for st, (x, y) in zip(states, positions):
        sid = str(st.get("id", ""))
        is_cur = sid == current_state_id
        if is_cur:
            cv2.circle(diagram, (x, y), node_r + 8, (0, 200, 255), 2)
            cv2.circle(diagram, (x, y), node_r, (0, 140, 255), -1)
            txt_color = (255, 255, 255)
            txt_thick = 2
        else:
            cv2.circle(diagram, (x, y), node_r, (185, 185, 185), 2)
            cv2.circle(diagram, (x, y), node_r - 3, (245, 245, 245), -1)
            txt_color = (90, 90, 90)
            txt_thick = 1

        label = sid if sid else "?"
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, txt_thick)
        cv2.putText(diagram, label, (x - tw // 2, y + th // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, txt_color, txt_thick, cv2.LINE_AA)

    cv2.putText(diagram, "States", (split_x + 12, 24),
                cv2.FONT_HERSHEY_SIMPLEX, 0.52, (60, 60, 60), 1, cv2.LINE_AA)

    right_x = split_x + 12
    right_w = width - right_x - 8
    top_y = 46
    usable_h = height - top_y - 10
    line_h = max(16, int(usable_h / max(n_states, 1)))
    font_scale = min(0.45, max(0.30, line_h / 48.0))

    def _fit_text(text, max_w, scale, thickness):
        if cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, scale, thickness)[0][0] <= max_w:
            return text
        lo, hi = 0, len(text)
        best = "..."
        while lo <= hi:
            mid = (lo + hi) // 2
            cand = text[:mid] + "..."
            w = cv2.getTextSize(cand, cv2.FONT_HERSHEY_SIMPLEX, scale, thickness)[0][0]
            if w <= max_w:
                best = cand
                lo = mid + 1
            else:
                hi = mid - 1
        return best

    for i, st in enumerate(states):
        y = top_y + i * line_h
        if y > height - 6:
            break
        sid = str(st.get("id", ""))
        name = str(st.get("name", ""))
        raw_text = f"{sid} : {name}"
        is_cur = sid == current_state_id
        color = (0, 140, 255) if is_cur else (85, 85, 85)
        thickness = 2 if is_cur else 1
        if is_cur:
            cv2.rectangle(diagram, (right_x - 4, y - 12), (width - 8, y + 5), (235, 245, 255), -1)
        cv2.putText(diagram, _fit_text(raw_text, right_w, font_scale, thickness),
                    (right_x, y), cv2.FONT_HERSHEY_SIMPLEX, font_scale,
                    color, thickness, cv2.LINE_AA)

    return diagram


def draw_result_on_frame(frame: np.ndarray, result: dict, fps: float | None = None) -> np.ndarray:
    """在图像上绘制推理结果"""
    vis = frame.copy()
    if result and result.get("ok"):
        category = str(result.get("best_category", "unknown"))
        similarity = float(result.get("best_similarity", 0.0))
        cv2.putText(vis, f"State: {category}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(vis, f"Confidence: {similarity:.3f}", (10, 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    else:
        err = result.get("error", "unknown") if isinstance(result, dict) else "unknown"
        cv2.putText(vis, f"Error: {err}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    if fps is not None:
        cv2.putText(vis, f"FPS: {float(fps):.2f}", (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 180, 0), 2)
    return vis


def build_visualization_frame(
    image_bgr: np.ndarray, result: dict, state_list: list, fps: float | None = None,
) -> np.ndarray:
    """拼接结果标注 + 状态图"""
    vis = draw_result_on_frame(image_bgr, result, fps=fps)
    diagram = create_state_diagram(
        state_list,
        current_state_id=get_current_state_id(result, state_list),
        width=vis.shape[1],
        height=400,
    )
    return np.vstack([vis, diagram])


# ─── Dashboard 上传工具 ─────────────────────────────────────────

def build_dashboard_endpoint(dashboard: str, api_path: str) -> str:
    """构造完整的 dashboard URL"""
    dashboard = dashboard.rstrip("/")
    if not dashboard:
        raise ValueError("dashboard 不能为空")
    if api_path.startswith(("http://", "https://")):
        return api_path
    return f"{dashboard}/{api_path.lstrip('/')}"


def parse_dashboard_paths(primary_path: str, fallback_paths: str) -> list[str]:
    """解析 dashboard 上传路径列表"""
    paths = []
    for item in [primary_path, *fallback_paths.split(",")]:
        path = item.strip()
        if not path or path in paths:
            continue
        paths.append(path)
    return paths


def post_video_stream_frame(
    dashboard: str,
    *,
    title: str,
    frame_base64: str,
    mime_type: str,
    source: str,
    api_paths: list[str],
):
    """向 dashboard 推送一帧"""
    payload = {
        "title": title,
        "frame_base64": frame_base64,
        "mime_type": mime_type,
        "source": source,
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    last_http_error = None
    last_exception = None
    for api_path in api_paths:
        endpoint = build_dashboard_endpoint(dashboard, api_path)
        req = request.Request(
            endpoint,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=5.0) as resp:
                body = resp.read().decode("utf-8")
                result = json.loads(body) if body else {}
                if isinstance(result, dict):
                    result["_endpoint"] = endpoint
                return result
        except error.HTTPError as e:
            body = ""
            try:
                body = e.read().decode("utf-8", errors="ignore")
            except Exception:
                pass
            if e.code != 404:
                message = f"HTTP {e.code} @ {endpoint}"
                if body:
                    message = f"{message} | {body[:500]}"
                raise RuntimeError(message) from e
            last_http_error = (endpoint, e.code, body[:500])
        except Exception as e:
            last_exception = (endpoint, e)

    if last_http_error is not None:
        endpoint, code, body = last_http_error
        message = f"HTTP {code} @ {endpoint}"
        if body:
            message = f"{message} | {body}"
        raise RuntimeError(message)

    if last_exception is not None:
        endpoint, exc = last_exception
        raise RuntimeError(f"request failed @ {endpoint}: {exc}") from exc

    raise RuntimeError("没有可用的 dashboard 上传路径")


def upload_visualization_frame(
    frame_bgr: np.ndarray,
    *,
    dashboard: str,
    title: str,
    source: str,
    api_paths: list[str],
    jpeg_quality: int,
    max_width: int,
    max_height: int,
):
    """编码并上传可视化帧到 dashboard"""
    frame_to_upload = resize_for_upload(frame_bgr, max_width=max_width, max_height=max_height)
    ok, buf = cv2.imencode(".jpg", frame_to_upload,
                          [int(cv2.IMWRITE_JPEG_QUALITY), int(jpeg_quality)])
    if not ok:
        raise RuntimeError("可视化图像 JPEG 编码失败")

    return post_video_stream_frame(
        dashboard,
        title=title,
        frame_base64=encode_image_bytes_to_base64(buf.tobytes()),
        mime_type="image/jpeg",
        source=source,
        api_paths=api_paths,
    )


def resize_for_upload(frame_bgr: np.ndarray, *, max_width: int, max_height: int) -> np.ndarray:
    """按最大宽高缩放图像（仅缩小不放大）"""
    h, w = frame_bgr.shape[:2]
    if max_width <= 0 and max_height <= 0:
        return frame_bgr

    scale_w = 1.0 if max_width <= 0 else max_width / max(w, 1)
    scale_h = 1.0 if max_height <= 0 else max_height / max(h, 1)
    scale = min(scale_w, scale_h, 1.0)
    if scale >= 1.0:
        return frame_bgr

    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))
    return cv2.resize(frame_bgr, (new_w, new_h), interpolation=cv2.INTER_AREA)
