"""LAST-ViT 推理服务封装"""

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
from torchvision.transforms import functional as F, InterpolationMode

from mindbridge.src.core.schemas.LastvitEntity import (
    PredictRequest,
    PredictResponse,
    StateItem,
    TopKItem,
)
from mindbridge.src.core.tool.LastvitTools import (
    apply_padding_head,
    build_visualization_frame,
    calculate_similarity,
    decode_image_b64_to_bgr,
    decode_image_b64_to_pil,
    load_centers,
    parse_center_feature,
    upload_visualization_frame,
)


# =============================================================================
# 模型定义（与训练脚本保持一致）
# =============================================================================

class QuickGELU(torch.nn.Module):
    def forward(self, x):
        return x * torch.sigmoid(1.702 * x)


class ResidualAttentionBlock(torch.nn.Module):
    def __init__(self, d_model, n_head, mlp_ratio=4.0):
        super().__init__()
        self.attn = torch.nn.MultiheadAttention(d_model, n_head, batch_first=True)
        self.ln_1 = torch.nn.LayerNorm(d_model)
        self.mlp = torch.nn.Sequential(
            torch.nn.Linear(d_model, int(d_model * mlp_ratio)),
            QuickGELU(),
            torch.nn.Linear(int(d_model * mlp_ratio), d_model),
        )
        self.ln_2 = torch.nn.LayerNorm(d_model)

    def forward(self, x, attn_mask=None):
        attn_out, _ = self.attn(
            self.ln_1(x), self.ln_1(x), self.ln_1(x),
            attn_mask=attn_mask, need_weights=False,
        )
        x = x + attn_out
        x = x + self.mlp(self.ln_2(x))
        return x


class LASTViTVisionEncoder(torch.nn.Module):
    """ViT-B/16 + LAST-ViT 频域 token 选择"""

    def __init__(self, embed_dim=512, image_size=224, patch_size=16,
                 width=768, layers=12, heads=12, mlp_ratio=4.0):
        super().__init__()
        self.image_size = image_size
        self.patch_size = patch_size
        self.grid_size = image_size // patch_size
        self.width = width
        scale = width ** -0.5

        self.conv1 = torch.nn.Conv2d(3, width, kernel_size=patch_size, stride=patch_size, bias=False)
        num_patches = self.grid_size * self.grid_size
        self.class_embedding = torch.nn.Parameter(scale * torch.randn(width))
        self.positional_embedding = torch.nn.Parameter(scale * torch.randn(num_patches + 1, width))
        self.ln_pre = torch.nn.LayerNorm(width)
        self.transformer = torch.nn.Sequential(*[
            ResidualAttentionBlock(width, heads, mlp_ratio) for _ in range(layers)
        ])
        self.ln_post = torch.nn.LayerNorm(width)
        self.proj = torch.nn.Parameter(scale * torch.randn(width, embed_dim))
        self.register_buffer('_cached_gaussian', None, persistent=False)

    def _build_gaussian_kernel(self, device):
        w = self.width
        kernel = torch.exp(-0.5 * (torch.arange(-w // 2 + 1, w // 2 + 1, device=device).float() / (w ** 0.5)) ** 2)
        return (kernel / kernel.max()).unsqueeze(0).unsqueeze(0)

    def forward(self, x):
        x = self.conv1(x)
        B, C, H, W = x.shape
        x = x.reshape(B, C, H * W).permute(0, 2, 1).contiguous()
        cls_token = self.class_embedding.view(1, 1, -1).expand(B, -1, -1)
        x = torch.cat([cls_token, x], dim=1) + self.positional_embedding.unsqueeze(0)
        x = self.ln_pre(x)
        x = self.transformer(x)

        # LAST-ViT: frequency-domain token selection
        if self._cached_gaussian is None or self._cached_gaussian.device != x.device:
            self._cached_gaussian = self._build_gaussian_kernel(x.device)
        x_detach = x[:, 1:]
        x_f = torch.fft.fftshift(torch.fft.fft(x_detach, dim=-1), dim=-1)
        x_smooth = torch.fft.ifft(torch.fft.ifftshift(x_f * self._cached_gaussian, dim=-1), dim=-1).real
        diff = x_detach / torch.abs(x_smooth - x_detach).clamp(min=1e-8)
        _, idx = torch.topk(diff, k=1, dim=1, largest=True)
        x = torch.mean(torch.gather(x_detach, 1, idx), dim=1)
        x = self.ln_post(x)
        return x @ self.proj if self.proj is not None else x


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


class LastvitInfer:

    def __init__(self, config_path: str | Path = "/workspace/mindbridge/src/core/config/last-vit-config.yaml"):
        cfg = _load_config(config_path)
        model_cfg = cfg.get("model", {})

        self.checkpoint_path = model_cfg["checkpoint"]
        self.graph_info_path = model_cfg.get("graph_info_file", model_cfg.get("cache_file", ""))
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.topk = int(model_cfg.get("topk", 5))

        print(f"[LastvitInfer] 设备: {self.device}")
        print(f"[LastvitInfer] 加载模型权重: {self.checkpoint_path}")
        self.model = self._load_model()
        print("[LastvitInfer] 模型加载完成")

        print(f"[LastvitInfer] 加载类别中心: {self.graph_info_path}")
        self.centers, self.state_list = self._load_centers()
        print(f"[LastvitInfer] 类别数: {len(self.centers)}")

    # ── 模型构建 ────────────────────────────────────────────────

    def _load_model(self) -> LASTViTVisionEncoder:
        model = LASTViTVisionEncoder(embed_dim=512)
        checkpoint = torch.load(self.checkpoint_path, map_location="cpu", weights_only=False)
        state_dict = checkpoint.get("model_state_dict", checkpoint)

        vis_state_dict = {}
        for k, v in state_dict.items():
            if k.startswith("vision_encoder."):
                vis_state_dict[k[len("vision_encoder."):]] = v

        missing, unexpected = model.load_state_dict(vis_state_dict, strict=False)
        if missing:
            filtered = [k for k in missing if "cached" not in k]
            if filtered:
                print(f"[LastvitInfer] 缺失键: {filtered[:5]}")
        if unexpected:
            print(f"[LastvitInfer] 多余键: {unexpected[:5]}")

        model = model.to(self.device)
        model.eval()
        return model

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
            center_raw = n.get("center_feature_lastvit", None)
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

    # ── 图像预处理 ──────────────────────────────────────────────

    def _preprocess_image(self, image: Image.Image, image_size=224):
        """CLIP 标准预处理"""
        img = F.resize(image, [image_size, image_size], interpolation=InterpolationMode.BICUBIC)
        img = F.to_tensor(img)
        img = F.normalize(img, mean=[0.48145466, 0.4578275, 0.40821073],
                          std=[0.26862954, 0.26130258, 0.27577711])
        return img.unsqueeze(0)

    # ── 核心推理方法 ────────────────────────────────────────────

    @torch.inference_mode()
    def _encode_image(self, image: Image.Image) -> np.ndarray:
        pixel_values = self._preprocess_image(image).to(self.device)
        feature = self.model(pixel_values)
        feature = feature / feature.norm(dim=-1, keepdim=True).clamp(min=1e-12)
        return feature[0].detach().cpu().numpy().astype(np.float32)

    def predict(self, req: PredictRequest) -> PredictResponse:
        t_start = time.time()
        request_id = req.request_id
        try:
            image = decode_image_b64_to_pil(req.image_b64)
            image = apply_padding_head(image)
            feat_np = self._encode_image(image)
            sim_result = calculate_similarity(feat_np, self.centers, topk=self.topk)

            # 构建响应 — 兼容旧字段
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
