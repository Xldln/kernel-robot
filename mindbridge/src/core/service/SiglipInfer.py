"""SigLIP 推理服务封装"""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path

import cv2
import numpy as np
import torch
import torch.nn as nn
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
    decode_image_b64_to_bgr,
    decode_image_b64_to_pil,
    parse_center_feature,
    upload_visualization_frame,
)


# =============================================================================
# V2 Attention Pooler & Model（与 ZeroMQServer 保持一致）
# =============================================================================

class CrossViewAttentionPooler(nn.Module):
    """Cross-attention pooler: learnable queries attend to patch tokens."""

    def __init__(self, embed_dim=1152, num_queries=8, num_heads=8,
                 num_layers=2, dropout=0.0):
        super().__init__()
        self.embed_dim = embed_dim
        self.num_queries = num_queries

        self.query_tokens = nn.Parameter(torch.zeros(1, num_queries, embed_dim))

        self.layers = nn.ModuleList()
        for _ in range(num_layers):
            self.layers.append(nn.ModuleDict({
                'cross_attn': nn.MultiheadAttention(
                    embed_dim=embed_dim, num_heads=num_heads,
                    dropout=dropout, batch_first=True,
                ),
                'norm1': nn.LayerNorm(embed_dim),
                'norm2': nn.LayerNorm(embed_dim),
                'ffn': nn.Sequential(
                    nn.Linear(embed_dim, embed_dim * 4),
                    nn.GELU(),
                    nn.Dropout(dropout),
                    nn.Linear(embed_dim * 4, embed_dim),
                    nn.Dropout(dropout),
                ),
            }))

        self.output_ln = nn.LayerNorm(embed_dim)

    def forward(self, x):
        B = x.shape[0]
        queries = self.query_tokens.expand(B, -1, -1)

        for layer in self.layers:
            residual = queries
            queries = layer['norm1'](queries)
            queries = layer['cross_attn'](query=queries, key=x, value=x)[0] + residual

            residual = queries
            queries = layer['norm2'](queries)
            queries = layer['ffn'](queries) + residual

        output = queries.mean(dim=1)
        output = self.output_ln(output)
        return output


class SingleViewSigLIPModel(nn.Module):
    """V2 single-view: frozen SigLIP + CrossViewAttentionPooler on patch tokens."""

    def __init__(self, base_model, pooler, embed_dim=1152):
        super().__init__()
        self.base_model = base_model
        self.pooler = pooler
        self.config = base_model.config

    def encode(self, pixel_values):
        with torch.no_grad():
            vision_outputs = self.base_model.vision_model(pixel_values=pixel_values)
            patch_tokens = vision_outputs.last_hidden_state  # [B, 256, D]
        fused = self.pooler(patch_tokens)
        fused = fused / (fused.norm(dim=-1, keepdim=True) + 1e-12)
        return fused


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

        # EMA 平滑配置
        self.use_sim_ema = cfg.get("ema", {}).get("enabled", True)
        self.ema_beta = cfg.get("ema", {}).get("beta", 0.7)

        print(f"[SiglipInfer] 设备: {self.device}")
        print(f"[SiglipInfer] 加载基础模型: {self.model_path}")
        self.model, self.processor = self._load_model()
        print(f"[SiglipInfer] 加载训练权重: {self.checkpoint_path}")
        print(f"[SiglipInfer] EMA 平滑: {'开启' if self.use_sim_ema else '关闭'}"
              + (f", beta={self.ema_beta}" if self.use_sim_ema else ""))
        print("[SiglipInfer] 模型加载完成")

        print(f"[SiglipInfer] 加载类别中心: {self.graph_info_path}")
        self.centers, self.state_list = self._load_centers()
        print(f"[SiglipInfer] 类别数: {len(self.centers)}")

    # ── 模型构建 ────────────────────────────────────────────────

    def _load_model(self):
        """加载 SigLIP 基础模型 + 训练权重（支持 V1/V2 checkpoint 自动检测）"""
        print(f"[SiglipInfer] 加载基础模型: {self.model_path}")
        full_model = AutoModel.from_pretrained(self.model_path)
        processor = AutoProcessor.from_pretrained(self.model_path)

        print(f"[SiglipInfer] 加载训练权重: {self.checkpoint_path}")
        checkpoint = torch.load(self.checkpoint_path, map_location="cpu", weights_only=False)
        state_dict = checkpoint.get("model_state_dict", checkpoint)

        # 检测 V2 单视角 checkpoint: key 以 base_model. 和 pooler. 开头
        sample_key = next(iter(state_dict))
        is_v2 = sample_key.startswith('base_model.') and any(
            k.startswith('pooler.') for k in state_dict)

        if is_v2:
            embed_dim = full_model.config.vision_config.hidden_size
            # 从 checkpoint 推断 pooler 参数
            num_queries = state_dict['pooler.query_tokens'].shape[1]
            num_layers = sum(1 for k in state_dict if k.endswith('.cross_attn.in_proj_weight'))
            num_heads = 8  # 与训练配置一致

            pooler = CrossViewAttentionPooler(
                embed_dim=embed_dim, num_queries=num_queries,
                num_heads=num_heads, num_layers=num_layers, dropout=0.0)
            model = SingleViewSigLIPModel(full_model, pooler, embed_dim=embed_dim)
            model.load_state_dict(state_dict)
            model = model.to(self.device)
            model.eval()
            print(f"[SiglipInfer] V2 SingleView 模型加载完成 (queries={num_queries}, layers={num_layers})")
        else:
            # V1 路径: 直接加载到 full_model
            incompatible = full_model.load_state_dict(state_dict, strict=False)
            if getattr(incompatible, "missing_keys", None):
                print(f"[SiglipInfer] 缺失键: {incompatible.missing_keys}")
            if getattr(incompatible, "unexpected_keys", None):
                print(f"[SiglipInfer] 多余键: {incompatible.unexpected_keys}")
            model = full_model
            model = model.to(self.device)
            model.eval()
            print("[SiglipInfer] V1 模型加载完成")

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

        # V2: model.encode() / V1: model.vision_model()
        if hasattr(self.model, 'encode'):
            feature = self.model.encode(pixel_values)  # [1, D] already L2-normalized
        else:
            outputs = self.model.vision_model(pixel_values=pixel_values)
            feature = outputs.pooler_output
            feature = feature / (feature.norm(dim=-1, keepdim=True) + 1e-12)

        return feature[0].detach().cpu().numpy().astype(np.float32)

    def _calculate_similarity(self, feat_np: np.ndarray,
                               ema_state: np.ndarray | None = None):
        """计算相似度，支持 EMA 平滑。返回 (result_dict, updated_ema_state)。"""
        sim_keys = list(self.centers.keys())
        sim_vals = np.array([float(np.dot(feat_np, self.centers[k])) for k in sim_keys],
                            dtype=np.float32)

        # EMA 平滑
        if self.use_sim_ema:
            if ema_state is None:
                ema_state = sim_vals.copy()
            else:
                ema_state = self.ema_beta * ema_state + (1 - self.ema_beta) * sim_vals
            smoothed = ema_state
        else:
            smoothed = sim_vals

        sims = {k: float(smoothed[i]) for i, k in enumerate(sim_keys)}
        best = max(sims.items(), key=lambda x: x[1])
        topk = sorted(sims.items(), key=lambda x: x[1], reverse=True)[:self.topk]

        result = {
            "ok": True,
            "best_category": best[0],
            "best_similarity": best[1],
            "topk": [{"category": k, "similarity": v} for k, v in topk],
        }
        return result, ema_state

    def predict(self, req: PredictRequest, ema_state: np.ndarray | None = None) -> tuple[PredictResponse, np.ndarray | None]:
        """执行推理，返回 (PredictResponse, updated_ema_state)。"""
        t_start = time.time()
        request_id = req.request_id
        try:
            image = decode_image_b64_to_pil(req.image_b64)
            feat_np = self._encode_image(image)
            sim_result, new_ema = self._calculate_similarity(feat_np, ema_state=ema_state)

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
            ), new_ema

        except Exception as e:
            elapsed = round(time.time() - t_start, 4)
            return PredictResponse(
                status="error",
                request_id=request_id,
                ok=False,
                message=str(e),
                elapsed_sec=elapsed,
            ), ema_state

    # ── 可视化辅助（供 Controller 使用） ────────────────────────

    def build_vis_frame(self, image_bgr: np.ndarray, result: dict, fps: float | None = None) -> np.ndarray:
        return build_visualization_frame(image_bgr, result, self.state_list, fps=fps)
