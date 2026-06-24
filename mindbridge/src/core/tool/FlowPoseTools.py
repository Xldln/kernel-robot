"""FlowPose 纯工具函数 — 图像编解码 / 类型转换 / 位姿组装"""

from __future__ import annotations

import base64
import json

import cv2
import numpy as np
import torch


# ═══════════════════════════════════════════════════════════════════
#  图像编解码
# ═══════════════════════════════════════════════════════════════════

def decode_image_b64(image_b64: str, flags: int) -> np.ndarray:
    """将 base64 字符串解码为 OpenCV 图像 (numpy array)。"""
    raw = base64.b64decode(image_b64)
    arr = np.frombuffer(raw, dtype=np.uint8)
    img = cv2.imdecode(arr, flags)
    if img is None:
        raise ValueError("Failed to decode image from base64.")
    return img


# ═══════════════════════════════════════════════════════════════════
#  类型转换
# ═══════════════════════════════════════════════════════════════════

def to_jsonable(obj):
    """递归将 torch.Tensor / np.ndarray 转换为 JSON 可序列化类型。"""
    if isinstance(obj, torch.Tensor):
        return obj.detach().cpu().tolist()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (list, tuple)):
        return [to_jsonable(x) for x in obj]
    if isinstance(obj, dict):
        return {k: to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    return obj


# ═══════════════════════════════════════════════════════════════════
#  推理输出解析
# ═══════════════════════════════════════════════════════════════════

def unpack_infer_output(pose_out, length_out):
    """从推理输出元组中解包 pose 和 length 为 JSON 可序列化列表。"""
    if pose_out is None or length_out is None:
        return None, None

    if isinstance(pose_out, (list, tuple)):
        if len(pose_out) == 0 or pose_out[0] is None:
            return None, None
        pose_all = pose_out[0]
    else:
        pose_all = pose_out

    if isinstance(length_out, (list, tuple)):
        if len(length_out) == 0 or length_out[0] is None:
            return None, None
        length_all = length_out[0]
    else:
        length_all = length_out

    pose_all = to_jsonable(pose_all)
    length_all = to_jsonable(length_all)

    if pose_all is None or length_all is None:
        return None, None

    return pose_all, length_all


# ═══════════════════════════════════════════════════════════════════
#  位姿对象组装
# ═══════════════════════════════════════════════════════════════════

def build_objects(
    pose_all,
    length_all,
    obj_ids,
    class_names=None,
    instance_names=None,
) -> list[dict]:
    """将 pose / length / obj_ids 组装为物体位姿列表。"""
    if pose_all is None or length_all is None or obj_ids is None:
        return []

    if class_names is None:
        class_names = []
    if instance_names is None:
        instance_names = []

    n = min(len(pose_all), len(length_all), len(obj_ids))
    objects = []

    for i in range(n):
        obj_id = obj_ids[i]

        box_id = None
        if isinstance(obj_id, (list, tuple)) and len(obj_id) >= 2:
            try:
                box_id = int(obj_id[1])
            except Exception:
                box_id = None

        # 优先使用 instance_names，其次 class_names
        if i < len(instance_names) and instance_names[i]:
            name = str(instance_names[i])
        elif i < len(class_names) and class_names[i]:
            name = str(class_names[i])
        elif box_id is not None:
            name = f"obj_{box_id}"
        else:
            name = f"obj_{i + 1}"

        objects.append({
            "name": name,
            "pose": pose_all[i],
            "length": length_all[i],
            "obj_id": obj_id,
            "box_id": box_id,
        })

    return objects


# ═══════════════════════════════════════════════════════════════════
#  调试 / 日志
# ═══════════════════════════════════════════════════════════════════

def save_latest_response(response: dict, save_path: str = "latest_response.json"):
    """将响应保存为 JSON 文件，方便调试。"""
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=2, ensure_ascii=False)
