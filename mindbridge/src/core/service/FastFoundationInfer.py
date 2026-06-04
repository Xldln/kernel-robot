"""Fast-Foundation Stereo 推理服务封装"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import cv2
import numpy as np
import torch
import yaml
from omegaconf import OmegaConf

from mindbridge.src.core.schemas.FastFoundationEntity import (
    StereoPredictRequest,
    StereoPredictResponse,
)
from mindbridge.src.core.tool.FastFoundationTools import (
    compute_depth_from_disparity,
    decode_bgr_from_base64,
    depth_float_m_to_uint16_mm,
    encode_array_to_base64,
    build_stereo_vis,
    encode_bgr_to_base64_jpg,
)


def _load_config(config_path: str | Path) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


class FastFoundationInfer:
    """Fast-Foundation Stereo 深度估计推理引擎"""

    def __init__(self, config_path: str | Path = "/workspace/mindbridge/src/core/config/fastfoundation-config.yaml"):
        cfg = _load_config(config_path)
        ff_cfg = cfg.get("fastfoundation", {})

        # ── 代码库路径 ──
        code_base = ff_cfg.get("code_base", "/workspace/mindbridge/models/Fast-FoundationStereo-master")
        if code_base and code_base not in sys.path:
            sys.path.insert(0, code_base)

        # ── 模型参数 ──
        self.ckpt_dir = ff_cfg["ckpt_dir"]
        self.valid_iters = int(ff_cfg.get("valid_iters", 8))

        # ── 相机默认内参 ──
        self.default_width = int(ff_cfg.get("width", 640))
        self.default_height = int(ff_cfg.get("height", 480))
        self.default_fx = float(ff_cfg.get("fx", 640.0))
        self.default_fy = float(ff_cfg.get("fy", 640.0))
        self.default_ppx = float(ff_cfg.get("ppx", 320.0))
        self.default_ppy = float(ff_cfg.get("ppy", 240.0))
        self.default_baseline = float(ff_cfg.get("baseline_m", 0.065))

        # ── 运行时默认值 ──
        self.scale = float(ff_cfg.get("scale", 1.0))
        self.z_far = float(ff_cfg.get("z_far", 10.0))
        self.remove_invisible = bool(int(ff_cfg.get("remove_invisible", 1)))

        # ── 加载模型 ──
        print(f"[FastFoundationInfer] 代码库: {code_base}")
        print(f"[FastFoundationInfer] 模型路径: {self.ckpt_dir}")
        print(f"[FastFoundationInfer] 默认内参: fx={self.default_fx}, fy={self.default_fy}, "
              f"ppx={self.default_ppx}, ppy={self.default_ppy}")
        print(f"[FastFoundationInfer] 基线: {self.default_baseline} m, "
              f"z_far={self.z_far}, scale={self.scale}, valid_iters={self.valid_iters}")

        t0 = time.time()
        self.model = self._load_model()
        print(f"[FastFoundationInfer] 模型加载完成 ({time.time() - t0:.2f}s)")

    # ── 模型加载 ────────────────────────────────────────────────

    def _load_model(self):
        """加载 Fast-Foundation Stereo 模型"""
        from Utils import set_logging_format, set_seed

        set_logging_format()
        set_seed(0)
        torch.autograd.set_grad_enabled(False)

        # 加载模型架构配置
        model_cfg_path = os.path.join(os.path.dirname(self.ckpt_dir), "cfg.yaml")
        model_cfg = OmegaConf.load(model_cfg_path)

        if "vit_size" not in model_cfg:
            model_cfg["vit_size"] = "vitl"

        model_cfg["ckpt_dir"] = self.ckpt_dir
        model_cfg["valid_iters"] = self.valid_iters
        model_cfg["width"] = self.default_width
        model_cfg["height"] = self.default_height
        model_cfg["scale"] = self.scale
        model_cfg["z_far"] = self.z_far
        model_cfg["remove_invisible"] = int(self.remove_invisible)

        args = OmegaConf.create(model_cfg)

        model = torch.load(self.ckpt_dir, map_location="cpu", weights_only=False)
        model.args.valid_iters = args.valid_iters
        model.args.max_disp = args.max_disp
        model.cuda()
        model.eval()

        return model

    # ── 核心推理（raw bytes，无 base64） ──────────────────────────

    def predict_from_arrays(
        self,
        left_bgr: np.ndarray,
        right_bgr: np.ndarray,
        *,
        request_id: str = "",
        scale: float | None = None,
        valid_iters: int | None = None,
        z_far: float | None = None,
        remove_invisible: bool | None = None,
        fx: float | None = None,
        fy: float | None = None,
        ppx: float | None = None,
        ppy: float | None = None,
        baseline: float | None = None,
        return_depth: bool = True,
        return_disparity: bool = False,
        return_color_jpg: bool = False,
        jpg_quality: int = 90,
    ) -> tuple[np.ndarray | None, np.ndarray | None, bytes | None, dict]:
        """直接接受 numpy 数组推理，返回 (depth_u16, disparity_f32, vis_jpg_bytes, meta)。

        Args:
            left_bgr: 左目 BGR 图像 (H, W, 3) uint8
            right_bgr: 右目 BGR 图像 (H, W, 3) uint8

        Returns:
            depth_u16: uint16 毫米深度图，或 None
            disparity_f32: float32 视差图，或 None
            vis_jpg_bytes: 可视化 JPG 字节，或 None
            meta: dict with keys status, request_id, depth_shape, elapsed_sec, message
        """
        t_start = time.time()

        try:
            # 确定推理参数
            _scale = scale if scale is not None else self.scale
            _valid_iters = valid_iters if valid_iters is not None else self.valid_iters
            _z_far = z_far if z_far is not None else self.z_far
            _remove_invisible = remove_invisible if remove_invisible is not None else self.remove_invisible
            _fx = fx if fx is not None else self.default_fx
            _fy = fy if fy is not None else self.default_fy
            _ppx = ppx if ppx is not None else self.default_ppx
            _ppy = ppy if ppy is not None else self.default_ppy
            _baseline = baseline if baseline is not None else self.default_baseline

            # 缩放
            if _scale != 1.0:
                left_bgr = cv2.resize(left_bgr, dsize=None, fx=_scale, fy=_scale)
                right_bgr = cv2.resize(right_bgr, dsize=None, fx=_scale, fy=_scale)

            H, W = left_bgr.shape[:2]

            # 转为 tensor 并推理
            from core.utils.utils import InputPadder

            img0_t = torch.as_tensor(left_bgr).cuda().float()[None].permute(0, 3, 1, 2)
            img1_t = torch.as_tensor(right_bgr).cuda().float()[None].permute(0, 3, 1, 2)

            padder = InputPadder(img0_t.shape, divis_by=32, force_square=False)
            img0_t, img1_t = padder.pad(img0_t, img1_t)

            with torch.cuda.amp.autocast(True):
                disp = self.model.forward(img0_t, img1_t, iters=_valid_iters, test_mode=True)

            disp = padder.unpad(disp.float())
            disp = disp.data.cpu().numpy().reshape(H, W)

            # 移除不可见区域
            if _remove_invisible:
                yy, xx = np.meshgrid(np.arange(H), np.arange(W), indexing="ij")
                us_right = xx - disp
                disp[us_right < 0] = np.inf

            # 计算深度
            K_effective = np.array([
                [_fx * _scale, 0, _ppx * _scale],
                [0, _fy * _scale, _ppy * _scale],
                [0, 0, 1],
            ], dtype=np.float32)

            depth_m = compute_depth_from_disparity(
                disp,
                fx=float(K_effective[0, 0]),
                baseline_m=float(_baseline),
                z_far=_z_far,
            )
            depth_u16 = depth_float_m_to_uint16_mm(depth_m)

            # 构建输出
            _depth_out = depth_u16 if return_depth else None
            _disp_out = disp.astype(np.float32) if return_disparity else None
            _vis_out: bytes | None = None
            if return_color_jpg:
                vis_bgr = build_stereo_vis(left_bgr, right_bgr, disp)
                ok, buf = cv2.imencode(".jpg", vis_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), int(jpg_quality)])
                _vis_out = buf.tobytes() if ok else None

            elapsed = round(time.time() - t_start, 4)
            meta = {
                "status": "ok",
                "request_id": request_id,
                "depth_shape": list(depth_u16.shape),
                "elapsed_sec": elapsed,
            }
            return _depth_out, _disp_out, _vis_out, meta

        except Exception as e:
            elapsed = round(time.time() - t_start, 4)
            meta = {
                "status": "error",
                "request_id": request_id,
                "message": str(e),
                "elapsed_sec": elapsed,
            }
            return None, None, None, meta

    # ── 核心推理（base64 版本，保留兼容） ────────────────────────

    def predict(self, req: StereoPredictRequest) -> StereoPredictResponse:
        t_start = time.time()
        request_id = req.request_id

        try:
            # 1. 解码输入图像
            left_bgr = decode_bgr_from_base64(req.left_image_b64)
            right_bgr = decode_bgr_from_base64(req.right_image_b64)

            # 2. 确定推理参数（请求覆盖 → 配置默认）
            scale = req.scale if req.scale is not None else self.scale
            valid_iters = req.valid_iters if req.valid_iters is not None else self.valid_iters
            z_far = req.z_far if req.z_far is not None else self.z_far
            remove_invisible = req.remove_invisible if req.remove_invisible is not None else self.remove_invisible

            fx = req.fx if req.fx is not None else self.default_fx
            fy = req.fy if req.fy is not None else self.default_fy
            ppx = req.ppx if req.ppx is not None else self.default_ppx
            ppy = req.ppy if req.ppy is not None else self.default_ppy
            baseline = req.baseline_m if req.baseline_m is not None else self.default_baseline

            # 3. 缩放
            if scale != 1.0:
                left_bgr = cv2.resize(left_bgr, dsize=None, fx=scale, fy=scale)
                right_bgr = cv2.resize(right_bgr, dsize=None, fx=scale, fy=scale)

            H, W = left_bgr.shape[:2]

            # 4. 转为 tensor 并推理
            from core.utils.utils import InputPadder

            img0_t = torch.as_tensor(left_bgr).cuda().float()[None].permute(0, 3, 1, 2)
            img1_t = torch.as_tensor(right_bgr).cuda().float()[None].permute(0, 3, 1, 2)

            padder = InputPadder(img0_t.shape, divis_by=32, force_square=False)
            img0_t, img1_t = padder.pad(img0_t, img1_t)

            with torch.cuda.amp.autocast(True):
                disp = self.model.forward(img0_t, img1_t, iters=valid_iters, test_mode=True)

            disp = padder.unpad(disp.float())
            disp = disp.data.cpu().numpy().reshape(H, W)

            # 5. 移除不可见区域
            if remove_invisible:
                yy, xx = np.meshgrid(np.arange(H), np.arange(W), indexing="ij")
                us_right = xx - disp
                disp[us_right < 0] = np.inf

            # 6. 计算深度
            K_effective = np.array([
                [fx * scale, 0, ppx * scale],
                [0, fy * scale, ppy * scale],
                [0, 0, 1],
            ], dtype=np.float32)

            depth_m = compute_depth_from_disparity(
                disp,
                fx=float(K_effective[0, 0]),
                baseline_m=float(baseline),
                z_far=z_far,
            )
            depth_u16 = depth_float_m_to_uint16_mm(depth_m)

            # 7. 构建响应
            response = StereoPredictResponse(
                status="ok",
                request_id=request_id,
                depth_shape=list(depth_u16.shape),
            )

            if req.return_depth:
                response.depth_u16_b64 = encode_array_to_base64(depth_u16)

            if req.return_disparity:
                disp_f32 = disp.astype(np.float32)
                response.disparity_b64 = encode_array_to_base64(disp_f32)
                response.disparity_shape = list(disp_f32.shape)

            if req.return_color_jpg:
                vis_bgr = build_stereo_vis(left_bgr, right_bgr, disp)
                response.vis_jpg_b64 = encode_bgr_to_base64_jpg(vis_bgr, quality=req.jpg_quality)

            response.elapsed_sec = round(time.time() - t_start, 4)
            return response

        except Exception as e:
            elapsed = round(time.time() - t_start, 4)
            return StereoPredictResponse(
                status="error",
                request_id=request_id,
                message=str(e),
                elapsed_sec=elapsed,
            )
