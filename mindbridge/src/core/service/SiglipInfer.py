"""SigLIP 推理服务封装"""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path

import cv2
import numpy as np
import torch
import yaml
from PIL import Image
from transformers import AutoModel, AutoProcessor

from mindbridge.src.core.schemas.SiglipEntity import (
    PredictRequest,
    PredictResponse,
    StateItem,
    TopKItem,
)
from mindbridge.src.core.tool.SiglipTools import (
    build_visualization_frame,
    calculate_similarity,
    decode_image_b64_to_bgr,
    decode_image_b64_to_pil,
    parse_center_feature,
    upload_visualization_frame,
)


# =============================================================================
# 可视化输出线程
# =============================================================================

class VisualizationOutput:
    """异步可视化输出 worker（显示窗口 + dashboard 上传）"""

    def __init__(
        self,
        *,
        show: bool,
        window_name: str,
        enable_upload: bool,
        dashboard: str,
        title: str,
        source: str,
        api_paths: list[str],
        jpeg_quality: int,
        upload_max_width: int,
        upload_max_height: int,
    ):
        self.show = show
        self.window_name = window_name
        self.enable_upload = enable_upload
        self.dashboard = dashboard
        self.title = title
        self.source = source
        self.api_paths = api_paths
        self.jpeg_quality = jpeg_quality
        self.upload_max_width = upload_max_width
        self.upload_max_height = upload_max_height

        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.frame_ready = threading.Event()
        self.latest_frame = None
        self.frame_seq = 0
        self.last_uploaded_seq = -1
        self.log_counter = 0

    def submit(self, frame_bgr: np.ndarray):
        if not (self.show or self.enable_upload):
            return
        with self.lock:
            self.latest_frame = frame_bgr.copy()
            self.frame_seq += 1
        self.frame_ready.set()

    def request_stop(self):
        self.stop_event.set()
        self.frame_ready.set()

    def run(self):
        last_seen_seq = -1
        try:
            while not self.stop_event.is_set():
                self.frame_ready.wait(timeout=0.1)
                with self.lock:
                    frame = None if self.latest_frame is None else self.latest_frame.copy()
                    frame_seq = self.frame_seq
                    should_clear = frame_seq == last_seen_seq

                if should_clear:
                    self.frame_ready.clear()
                    continue
                if frame is None:
                    self.frame_ready.clear()
                    continue

                if self.show:
                    try:
                        cv2.imshow(self.window_name, frame)
                        if (cv2.waitKey(1) & 0xFF) == ord("q"):
                            print("[Visualization] 收到 q，关闭可视化并退出。")
                            self.request_stop()
                            break
                    except Exception as e:
                        print(f"[Visualization] 显示失败: {e}")

                if self.enable_upload and frame_seq != self.last_uploaded_seq:
                    try:
                        upload_visualization_frame(
                            frame,
                            dashboard=self.dashboard,
                            title=self.title,
                            source=self.source,
                            api_paths=self.api_paths,
                            jpeg_quality=self.jpeg_quality,
                            max_width=self.upload_max_width,
                            max_height=self.upload_max_height,
                        )
                        self.last_uploaded_seq = frame_seq
                        self.log_counter += 1
                    except Exception as e:
                        print(f"[Visualization] Dashboard 上传失败: {e}")

                last_seen_seq = frame_seq
                with self.lock:
                    if self.frame_seq == frame_seq:
                        self.frame_ready.clear()
        finally:
            if self.show:
                cv2.destroyAllWindows()


# =============================================================================
# 推理服务
# =============================================================================

def _load_config(config_path: str | Path) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


class SiglipInfer:

    def __init__(self, config_path: str | Path = "/workspace/mindbridge/src/core/config/siglip-config.yaml"):
        cfg = _load_config(config_path)
        model_cfg = cfg.get("model", {})

        self.model_path = model_cfg["path"]
        self.checkpoint_path = model_cfg["checkpoint"]
        self.graph_info_path = model_cfg.get("graph_info_file", model_cfg.get("cache_file", ""))
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.topk = int(model_cfg.get("topk", 5))

        print(f"[SiglipInfer] 设备: {self.device}")
        print(f"[SiglipInfer] 加载基础模型: {self.model_path}")
        self.model, self.processor = self._load_model()
        print(f"[SiglipInfer] 加载训练权重: {self.checkpoint_path}")
        print("[SiglipInfer] 模型加载完成")

        print(f"[SiglipInfer] 加载类别中心: {self.graph_info_path}")
        self.centers, self.state_list = self._load_centers()
        print(f"[SiglipInfer] 类别数: {len(self.centers)}")

    # ── 模型构建 ────────────────────────────────────────────────

    def _load_model(self):
        """加载 SigLIP 基础模型 + 训练权重"""
        model = AutoModel.from_pretrained(self.model_path)
        processor = AutoProcessor.from_pretrained(self.model_path)

        checkpoint = torch.load(self.checkpoint_path, map_location="cpu", weights_only=False)
        model_state = checkpoint.get("model_state_dict", checkpoint)

        incompatible = model.load_state_dict(model_state, strict=False)
        if getattr(incompatible, "missing_keys", None):
            print(f"[SiglipInfer] 缺失键: {incompatible.missing_keys}")
        if getattr(incompatible, "unexpected_keys", None):
            print(f"[SiglipInfer] 多余键: {incompatible.unexpected_keys}")

        model = model.to(self.device)
        model.eval()
        return model, processor

    def _load_centers(self):
        """从 graph_info_file 加载类别中心"""
        with open(self.graph_info_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        nodes = data.get("nodes", [])

        def _node_key(n):
            try:
                return int(n.get("node_id", 0))
            except Exception:
                return 10 ** 9

        nodes = sorted(nodes, key=_node_key)

        centers = {}
        state_list = []
        idx = 0
        for n in nodes:
            desc = str(n.get("state_description", "")).strip()
            center_raw = n.get("center_feature_siglip2", None)
            node_id = str(n.get("node_id", "")).strip()
            if not desc or center_raw is None:
                continue
            idx += 1
            cid = f"C{idx}"
            category_name = f"{cid}: {desc}"
            center = parse_center_feature(center_raw)
            centers[category_name] = center
            state_list.append({
                "id": cid,
                "node_id": node_id,
                "name": desc,
                "category": category_name,
            })

        if not centers:
            raise RuntimeError(f"未从 {self.graph_info_path} 读取到有效类别中心")
        return centers, state_list

    # ── 核心推理方法 ────────────────────────────────────────────

    @torch.inference_mode()
    def _encode_image(self, image: Image.Image) -> np.ndarray:
        inputs = self.processor(images=[image], return_tensors="pt")
        pixel_values = inputs["pixel_values"].to(self.device)

        outputs = self.model.get_image_features(pixel_values=pixel_values)
        feature = outputs.pooler_output
        feature = feature / feature.norm(dim=-1, keepdim=True).clamp(min=1e-12)

        return feature[0].detach().cpu().numpy().astype(np.float32)

    def predict(self, req: PredictRequest) -> PredictResponse:
        t_start = time.time()
        request_id = req.request_id
        try:
            image = decode_image_b64_to_pil(req.image_b64)
            feat_np = self._encode_image(image)
            sim_result = calculate_similarity(feat_np, self.centers, topk=self.topk)

            topk_items = [
                TopKItem(category=item["category"], similarity=item["similarity"])
                for item in sim_result.get("topk", [])
            ]
            state_items = [
                StateItem(id=s["id"], node_id=s["node_id"], name=s["name"], category=s["category"])
                for s in self.state_list
            ]

            elapsed = round(time.time() - t_start, 4)
            return PredictResponse(
                status="ok",
                request_id=request_id,
                ok=True,
                best_category=sim_result.get("best_category", ""),
                best_similarity=sim_result.get("best_similarity", 0.0),
                topk=topk_items,
                total_category=state_items,
                elapsed_sec=elapsed,
            )

        except Exception as e:
            elapsed = round(time.time() - t_start, 4)
            return PredictResponse(
                status="error",
                request_id=request_id,
                ok=False,
                message=str(e),
                elapsed_sec=elapsed,
            )

    # ── 可视化辅助（供 Controller 使用） ────────────────────────

    def build_vis_frame(self, image_bgr: np.ndarray, result: dict, fps: float | None = None) -> np.ndarray:
        return build_visualization_frame(image_bgr, result, self.state_list, fps=fps)
