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


class MultiViewSigLIPModel(nn.Module):
    """Frozen SigLIP2 base + per-view positional embedding + cross-view pooler."""

    def __init__(self, base_model, pooler, num_views=3, embed_dim=1152):
        super().__init__()
        self.base_model = base_model
        self.pooler = pooler
        self.num_views = num_views
        self.embed_dim = embed_dim
        self.config = base_model.config
        self.view_pos_embed = nn.Parameter(torch.zeros(num_views, 1, embed_dim))

    def encode_views(self, pixel_values: torch.Tensor) -> torch.Tensor:
        """[N=B*V, C, H, W] -> [B, D] (L2-normalized)."""
        with torch.no_grad():
            vision_outputs = self.base_model.vision_model(pixel_values=pixel_values)
            patch_tokens = vision_outputs.last_hidden_state

        n, p, d = patch_tokens.shape
        if n % self.num_views != 0:
            raise ValueError(f"view count {n} is not a multiple of num_views={self.num_views}")
        b = n // self.num_views

        patch_tokens = patch_tokens.view(b, self.num_views, p, d)
        patch_tokens = patch_tokens + self.view_pos_embed.unsqueeze(0)
        tokens = patch_tokens.reshape(b, self.num_views * p, d)

        fused = self.pooler(tokens)
        fused = fused / (fused.norm(dim=-1, keepdim=True) + 1e-12)
        return fused


def _split_image_to_views(image: Image.Image, num_views: int) -> list[Image.Image]:
    """Split one horizontally stitched image into fixed-width views."""
    if num_views <= 1:
        return [image]
    w, h = image.size
    view_w = w // num_views
    if view_w <= 0:
        return [image]
    views = []
    for idx in range(num_views):
        left = idx * view_w
        right = w if idx == num_views - 1 else (idx + 1) * view_w
        views.append(image.crop((left, 0, right, h)))
    return views


def _apply_background_mask(image: Image.Image, ratio: float) -> Image.Image:
    """Mask the top part of a stitched image, matching the old multiview scripts."""
    if ratio <= 0:
        return image
    arr = np.array(image.convert("RGB"), copy=True)
    cutoff = int(arr.shape[0] * min(max(ratio, 0.0), 1.0))
    if cutoff > 0:
        arr[:cutoff, :, :] = 0
    return Image.fromarray(arr).convert("RGB")


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
        self.num_views = int(model_cfg.get("num_views", 3))
        self.num_query_tokens = int(model_cfg.get("num_query_tokens", 8))
        self.pooler_num_layers = int(model_cfg.get("pooler_num_layers", 2))
        self.pooler_num_heads = int(model_cfg.get("pooler_num_heads", 8))
        self.background_mask_ratio = float(model_cfg.get("background_mask_ratio", 0))
        self.force_multiview = bool(model_cfg.get("multiview", False))
        self.is_multiview = False

        # EMA 平滑配置
        self.use_sim_ema = cfg.get("ema", {}).get("enabled", True)
        self.ema_beta = cfg.get("ema", {}).get("beta", 0.7)
        self.ema_adaptive = cfg.get("ema", {}).get("adaptive", False)
        self.ema_adaptive_beta = cfg.get("ema", {}).get("adaptive_beta", 0.2)

        print(f"[SiglipInfer] 设备: {self.device}")
        print(f"[SiglipInfer] 加载基础模型: {self.model_path}")
        self.model, self.processor = self._load_model()
        print(f"[SiglipInfer] 加载训练权重: {self.checkpoint_path}")
        print(f"[SiglipInfer] EMA 平滑: {'开启' if self.use_sim_ema else '关闭'}"
              + (f", beta={self.ema_beta}" if self.use_sim_ema else "")
              + (f", adaptive_beta={self.ema_adaptive_beta}" if self.use_sim_ema and self.ema_adaptive else ""))
        print("[SiglipInfer] 模型加载完成")

        print(f"[SiglipInfer] 加载类别中心: {self.graph_info_path}")
        self.centers, self.state_list = self._load_centers()
        print(f"[SiglipInfer] 类别数: {len(self.centers)}")

    # ── 模型构建 ────────────────────────────────────────────────

    def _load_model(self):
        """加载 SigLIP 基础模型 + 训练权重（支持 V1/V2/MultiView checkpoint 自动检测）"""
        print(f"[SiglipInfer] 加载基础模型: {self.model_path}")
        full_model = AutoModel.from_pretrained(self.model_path)
        processor = AutoProcessor.from_pretrained(self.model_path)

        print(f"[SiglipInfer] 加载训练权重: {self.checkpoint_path}")
        checkpoint = torch.load(self.checkpoint_path, map_location="cpu", weights_only=False)
        state_dict = checkpoint.get("model_state_dict", checkpoint)

        is_multiview = self.force_multiview or any(k == "view_pos_embed" for k in state_dict)
        # 检测 V2 单视角 checkpoint: key 以 base_model. 和 pooler. 开头
        sample_key = next(iter(state_dict))
        is_v2 = sample_key.startswith('base_model.') and any(
            k.startswith('pooler.') for k in state_dict)

        if is_multiview:
            embed_dim = full_model.config.vision_config.hidden_size
            num_queries = (
                state_dict["pooler.query_tokens"].shape[1]
                if "pooler.query_tokens" in state_dict
                else self.num_query_tokens
            )
            num_layers = sum(1 for k in state_dict if k.endswith(".cross_attn.in_proj_weight"))
            if num_layers <= 0:
                num_layers = self.pooler_num_layers
            num_views = (
                state_dict["view_pos_embed"].shape[0]
                if "view_pos_embed" in state_dict
                else self.num_views
            )

            pooler = CrossViewAttentionPooler(
                embed_dim=embed_dim,
                num_queries=num_queries,
                num_heads=self.pooler_num_heads,
                num_layers=num_layers,
                dropout=0.0,
            )
            model = MultiViewSigLIPModel(
                full_model,
                pooler,
                num_views=num_views,
                embed_dim=embed_dim,
            )
            incompatible = model.load_state_dict(state_dict, strict=False)
            missing = getattr(incompatible, "missing_keys", []) or []
            unexpected = getattr(incompatible, "unexpected_keys", []) or []
            if missing:
                print(f"[SiglipInfer] MultiView 缺失键: {missing}")
            if unexpected:
                print(f"[SiglipInfer] MultiView 多余键: {unexpected}")
            model = model.to(self.device)
            model.eval()
            self.num_views = num_views
            self.is_multiview = True
            print(
                "[SiglipInfer] MultiView 模型加载完成 "
                f"(views={num_views}, queries={num_queries}, layers={num_layers})"
            )
        elif is_v2:
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
        if self.is_multiview and hasattr(self.model, "encode_views"):
            if self.background_mask_ratio > 0:
                image = _apply_background_mask(image, self.background_mask_ratio)
            views = _split_image_to_views(image, self.num_views)
            if len(views) != self.num_views:
                print(f"[SiglipInfer] multiview split got {len(views)} views, expected {self.num_views}")
            inputs = self.processor(images=views, return_tensors="pt")
            pixel_values = inputs["pixel_values"].to(self.device)
            feature = self.model.encode_views(pixel_values)
        else:
            inputs = self.processor(images=[image], return_tensors="pt")
            pixel_values = inputs["pixel_values"].to(self.device)

        # V2: model.encode() / V1: model.vision_model()
        if not self.is_multiview and hasattr(self.model, 'encode'):
            feature = self.model.encode(pixel_values)  # [1, D] already L2-normalized
        elif not self.is_multiview:
            outputs = self.model.vision_model(pixel_values=pixel_values)
            feature = outputs.pooler_output
            feature = feature / (feature.norm(dim=-1, keepdim=True) + 1e-12)

        return feature[0].detach().cpu().numpy().astype(np.float32)

    def _calculate_similarity(self, feat_np: np.ndarray,
                               ema_state: np.ndarray | None = None):
        """计算相似度，支持自适应 EMA 平滑。

        自适应策略：当原始 top-1 类别与平滑后 top-1 类别不一致时（状态切换），
        使用更低的 adaptive_beta 加速过渡；状态稳定时保持正常 beta 以过滤噪声。
        """
        sim_keys = list(self.centers.keys())
        sim_vals = np.array([float(np.dot(feat_np, self.centers[k])) for k in sim_keys],
                            dtype=np.float32)

        if self.use_sim_ema:
            if ema_state is None:
                ema_state = sim_vals.copy()
                beta_used = self.ema_beta
            else:
                # 自适应 beta：检测 top-1 类别是否发生变化
                if self.ema_adaptive:
                    raw_best_idx = int(np.argmax(sim_vals))
                    smooth_best_idx = int(np.argmax(ema_state))
                    if raw_best_idx != smooth_best_idx:
                        beta_used = self.ema_adaptive_beta
                    else:
                        beta_used = self.ema_beta
                else:
                    beta_used = self.ema_beta
                ema_state = beta_used * ema_state + (1 - beta_used) * sim_vals
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
