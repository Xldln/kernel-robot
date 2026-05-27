"""RealSense camera + FoundationStereo depth estimation service."""

from __future__ import annotations

import os
from pathlib import Path

import cv2
import numpy as np
import pyrealsense2 as rs
import torch
from omegaconf import OmegaConf

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"


def _depth_float_m_to_uint16_mm(depth_m: np.ndarray) -> np.ndarray:
    """Convert depth in meters to uint16 in millimeters."""
    depth = depth_m.copy()
    depth[~np.isfinite(depth)] = 0
    depth[depth < 0] = 0
    return np.clip(depth * 1000.0, 0, 65535).astype(np.uint16)


class RealsenseService:
    """RealSense stereo camera + FoundationStereo depth inference."""

    def __init__(
        self,
        config_path: str | Path = "/workspace/mindbridge/src/core/config/realsense-config.yaml",
    ):
        cfg = OmegaConf.load(config_path)
        self.cfg = cfg
        self._frame_id = 0

        self._load_model(cfg)
        self._init_camera(cfg)

    # ── Model loading ──────────────────────────────────────────────────────

    def _load_model(self, cfg) -> None:
        ckpt_dir = cfg.model.ckpt_dir
        model_cfg = OmegaConf.load(f"{Path(ckpt_dir).parent}/cfg.yaml")
        model_cfg.setdefault("vit_size", "vitl")
        for key in (
            "ckpt_dir", "out_dir", "width", "height", "fps",
            "scale", "z_far", "valid_iters", "remove_invisible",
        ):
            model_cfg[key] = (
                cfg.model.get(key)
                or cfg.runtime.get(key)
                or cfg.camera.get(key)
                or cfg.paths.get(key)
                or model_cfg[key]
            )

        model_cfg.ckpt_dir = ckpt_dir
        model_cfg.out_dir = cfg.paths.out_dir
        model_cfg.width = cfg.camera.width
        model_cfg.height = cfg.camera.height
        model_cfg.fps = cfg.camera.fps
        model_cfg.scale = cfg.runtime.scale
        model_cfg.z_far = cfg.runtime.z_far
        model_cfg.valid_iters = cfg.model.valid_iters
        model_cfg.remove_invisible = cfg.runtime.remove_invisible

        self.model_args = model_cfg
        self.model = torch.load(ckpt_dir, map_location="cpu", weights_only=False)
        self.model.args.valid_iters = self.model_args.valid_iters
        self.model.args.max_disp = self.model_args.get("max_disp", 256)
        self.model.cuda()
        self.model.eval()

        self.scale = float(cfg.runtime.scale)

    # ── Camera initialization ──────────────────────────────────────────────

    def _init_camera(self, cfg) -> None:
        self.image_size = (int(cfg.camera.width), int(cfg.camera.height))
        self.pipeline = rs.pipeline()
        rs_cfg = rs.config()
        rs_cfg.enable_stream(
            rs.stream.infrared, 1, *self.image_size, rs.format.y8, int(cfg.camera.fps),
        )
        rs_cfg.enable_stream(
            rs.stream.infrared, 2, *self.image_size, rs.format.y8, int(cfg.camera.fps),
        )
        rs_cfg.enable_stream(
            rs.stream.color, *self.image_size, rs.format.bgr8, int(cfg.camera.fps),
        )
        profile = self.pipeline.start(rs_cfg)

        depth_sensor = profile.get_device().first_depth_sensor()
        if depth_sensor.supports(rs.option.emitter_enabled):
            depth_sensor.set_option(
                rs.option.emitter_enabled, int(cfg.camera.disable_emitter),
            )

        # ── Camera intrinsics ──────────────────────────────────────────────
        left = profile.get_stream(rs.stream.infrared, 1).as_video_stream_profile()
        right = profile.get_stream(rs.stream.infrared, 2).as_video_stream_profile()
        color = profile.get_stream(rs.stream.color).as_video_stream_profile()

        self.K = np.array([
            [left.get_intrinsics().fx, 0, left.get_intrinsics().ppx],
            [0, left.get_intrinsics().fy, left.get_intrinsics().ppy],
            [0, 0, 1],
        ], dtype=np.float32)
        self.K[:2] *= float(cfg.runtime.scale)

        extr = left.get_extrinsics_to(right)
        self.baseline = abs(extr.translation[0])

        ir_to_color = left.get_extrinsics_to(color)
        self.R_ext = np.array(ir_to_color.rotation).reshape(3, 3).T
        self.T_ext = np.array(ir_to_color.translation)

        self.color_intr = color.get_intrinsics()

    # ── Property ───────────────────────────────────────────────────────────

    @property
    def frame_id(self) -> int:
        return self._frame_id

    # ── Capture ────────────────────────────────────────────────────────────

    def capture(self) -> dict:
        """Capture and process one stereo pair → depth map.

        Returns
        -------
        dict with keys:
            color_bgr    (H,W,3) uint8   – color image
            depth_m      (H,W) float32   – depth in meters (aligned to color)
            depth_u16    (H,W) uint16    – depth in mm
            K            (3,3) float32   – left IR intrinsics
            baseline     float           – stereo baseline in meters
            frame_id     int
        """
        frames = self.pipeline.wait_for_frames()
        left = np.asanyarray(frames.get_infrared_frame(1).get_data())
        right = np.asanyarray(frames.get_infrared_frame(2).get_data())
        color = np.asanyarray(frames.get_color_frame().get_data())

        img0 = cv2.cvtColor(left, cv2.COLOR_GRAY2BGR)
        img1 = cv2.cvtColor(right, cv2.COLOR_GRAY2BGR)

        if self.scale != 1.0:
            img0 = cv2.resize(img0, dsize=None, fx=self.scale, fy=self.scale)
            img1 = cv2.resize(img1, dsize=None, fx=self.scale, fy=self.scale)

        from core.utils.utils import InputPadder

        H, W = img0.shape[:2]
        img0_t = torch.as_tensor(img0).cuda().float()[None].permute(0, 3, 1, 2)
        img1_t = torch.as_tensor(img1).cuda().float()[None].permute(0, 3, 1, 2)

        padder = InputPadder(img0_t.shape, divis_by=32, force_square=False)
        img0_t, img1_t = padder.pad(img0_t, img1_t)

        with torch.cuda.amp.autocast(True):
            disp = self.model.forward(
                img0_t, img1_t,
                iters=self.model.args.valid_iters,
                test_mode=True,
            )

        disp = padder.unpad(disp.float()).data.cpu().numpy().reshape(H, W)

        if self.cfg.runtime.remove_invisible:
            yy, xx = np.meshgrid(np.arange(H), np.arange(W), indexing="ij")
            us_right = xx - disp
            disp[us_right < 0] = np.inf

        # Depth from disparity: Z = fx * baseline / disp
        depth_ir = self.K[0, 0] * self.baseline / disp

        # Align depth IR → color
        valid = (depth_ir > 0) & np.isfinite(depth_ir)
        y_ir, x_ir = np.nonzero(valid)
        z_ir = depth_ir[valid]
        X_ir = (x_ir - self.K[0, 2]) * z_ir / self.K[0, 0]
        Y_ir = (y_ir - self.K[1, 2]) * z_ir / self.K[1, 1]

        P_color = self.R_ext @ np.stack((X_ir, Y_ir, z_ir), axis=0) + self.T_ext[:, None]

        x_c = np.round(
            P_color[0] / P_color[2] * self.color_intr.fx + self.color_intr.ppx,
        ).astype(int)
        y_c = np.round(
            P_color[1] / P_color[2] * self.color_intr.fy + self.color_intr.ppy,
        ).astype(int)
        mask = (
            (x_c >= 0) & (x_c < self.color_intr.width)
            & (y_c >= 0) & (y_c < self.color_intr.height)
            & (P_color[2] > 0)
        )

        depth_aligned = np.zeros(
            (self.color_intr.height, self.color_intr.width), dtype=np.float32,
        )
        order = np.argsort(P_color[2][mask])[::-1]
        depth_aligned[y_c[mask][order], x_c[mask][order]] = P_color[2][mask][order]

        self._frame_id += 1

        return {
            "color_bgr": color,
            "depth_m": depth_aligned,
            "depth_u16": _depth_float_m_to_uint16_mm(depth_aligned),
            "K": self.K,
            "baseline": self.baseline,
            "frame_id": self._frame_id,
        }

    # ── Lifecycle ──────────────────────────────────────────────────────────

    def close(self):
        cv2.destroyAllWindows()
        self.pipeline.stop()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
