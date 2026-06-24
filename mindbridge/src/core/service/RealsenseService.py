"""RealSense camera depth capture service (built-in depth, no external model)."""

from __future__ import annotations

import os

import cv2
import numpy as np
import pyrealsense2 as rs
import yaml

from mindbridge.src.core.schemas.RealsenseEntity import CaptureData

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"


def _depth_float_m_to_uint16_mm(depth_m: np.ndarray) -> np.ndarray:
    """Convert depth in meters to uint16 in millimeters."""
    depth = depth_m.copy()
    depth[~np.isfinite(depth)] = 0
    depth[depth < 0] = 0
    return np.clip(depth * 1000.0, 0, 65535).astype(np.uint16)


class RealsenseService:
    """RealSense camera depth capture using built-in hardware depth computation."""

    def __init__(self, config_path: str = "/workspace/mindbridge/src/core/config/realsense-config.yaml"):
        with open(config_path) as f:
            cfg = yaml.safe_load(f)
        self.cfg = cfg
        self._frame_id = 0
        self._init_camera(cfg)

    # ── Camera initialization ──────────────────────────────────────────────

    def _init_camera(self, cfg: dict) -> None:
        w, h = int(cfg["camera"]["width"]), int(cfg["camera"]["height"])
        fps = int(cfg["camera"]["fps"])
        self.image_size = (w, h)

        self.pipeline = rs.pipeline()
        rs_cfg = rs.config()
        rs_cfg.enable_stream(rs.stream.depth, w, h, rs.format.z16, fps)
        rs_cfg.enable_stream(rs.stream.color, w, h, rs.format.bgr8, fps)
        rs_cfg.enable_stream(rs.stream.infrared, 1, w, h, rs.format.y8, fps)
        rs_cfg.enable_stream(rs.stream.infrared, 2, w, h, rs.format.y8, fps)
        profile = self.pipeline.start(rs_cfg)

        depth_sensor = profile.get_device().first_depth_sensor()
        if depth_sensor.supports(rs.option.emitter_enabled):
            depth_sensor.set_option(
                rs.option.emitter_enabled, int(cfg["camera"]["disable_emitter"]),
            )

        # Align depth frames to color camera
        self.align = rs.align(rs.stream.color)

        # Warm up: discard frames until auto-exposure stabilises
        warmup_frames = 30
        for i in range(warmup_frames):
            try:
                self.pipeline.wait_for_frames(timeout_ms=10000)
            except RuntimeError:
                print(f"Warmup frame {i+1}/{warmup_frames} timed out, retrying...")
                continue

        # ── Camera intrinsics ──────────────────────────────────────────────
        color = profile.get_stream(rs.stream.color).as_video_stream_profile()
        left_ir = profile.get_stream(rs.stream.infrared, 1).as_video_stream_profile()
        right_ir = profile.get_stream(rs.stream.infrared, 2).as_video_stream_profile()
        self.color_intr = color.get_intrinsics()
        self.left_ir_intr = left_ir.get_intrinsics()
        self.K = np.array([
            [self.color_intr.fx, 0, self.color_intr.ppx],
            [0, self.color_intr.fy, self.color_intr.ppy],
            [0, 0, 1],
        ], dtype=np.float32)
        self.ir_left_K = np.array([
            [self.left_ir_intr.fx, 0, self.left_ir_intr.ppx],
            [0, self.left_ir_intr.fy, self.left_ir_intr.ppy],
            [0, 0, 1],
        ], dtype=np.float32)

        stereo_extr = left_ir.get_extrinsics_to(right_ir)
        ir_to_color_extr = left_ir.get_extrinsics_to(color)
        self.baseline = abs(float(stereo_extr.translation[0]))
        self.ir_to_color_R = np.array(ir_to_color_extr.rotation, dtype=np.float32).reshape(3, 3).T
        self.ir_to_color_T = np.array(ir_to_color_extr.translation, dtype=np.float32)

    # ── Property ───────────────────────────────────────────────────────────

    @property
    def frame_id(self) -> int:
        return self._frame_id

    # ── Capture ────────────────────────────────────────────────────────────

    def capture(self) -> CaptureData:
        """Capture and return one aligned depth-color frame pair."""
        frames = self.pipeline.wait_for_frames(timeout_ms=10000)
        aligned = self.align.process(frames)

        depth_frame = aligned.get_depth_frame()
        color_frame = aligned.get_color_frame()
        ir_left_frame = frames.get_infrared_frame(1)
        ir_right_frame = frames.get_infrared_frame(2)
        if not depth_frame or not color_frame:
            raise RuntimeError("Failed to get aligned frames")

        # RealSense depth is in mm by default → convert to meters
        depth_mm = np.asanyarray(depth_frame.get_data())
        depth_m = depth_mm.astype(np.float32) / 1000.0
        color = np.asanyarray(color_frame.get_data())
        ir_left = np.asanyarray(ir_left_frame.get_data()) if ir_left_frame else None
        ir_right = np.asanyarray(ir_right_frame.get_data()) if ir_right_frame else None

        self._frame_id += 1

        return CaptureData(
            color_bgr=color,
            depth_m=depth_m,
            depth_u16=_depth_float_m_to_uint16_mm(depth_m),
            ir_left=ir_left,
            ir_right=ir_right,
            K=self.K,
            ir_left_K=self.ir_left_K,
            ir_to_color_R=self.ir_to_color_R,
            ir_to_color_T=self.ir_to_color_T,
            baseline=self.baseline,
            frame_id=self._frame_id,
        )


    def close(self):
        cv2.destroyAllWindows()
        pipeline = getattr(self, "pipeline", None)
        if pipeline is not None:
            try:
                pipeline.stop()
            except Exception as exc:
                print(f"[RealSense] pipeline.stop ignored: {exc}")
            finally:
                self.pipeline = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
