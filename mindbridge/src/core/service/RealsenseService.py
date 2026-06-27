"""RealSense camera depth capture service (built-in depth, no external model).

结构:
  _FullCamera      — primary 相机：彩色 + 深度 + IR 立体（完整能力）。
  _ColorCamera     — 仅彩色相机：multi 模式下作为 SigLIP 等模型的额外视角。
  RealsenseService — 管理器，按 config 的 mode 管理 primary（+ 若干 color-only）。

single 模式行为与历史完全一致：一台 primary 相机，所有旧属性/方法保持不变。
"""

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


class _FullCamera:
    """Primary 相机：彩色 + 深度 + IR 立体（含内参/外参）。"""

    def __init__(self, cam_cfg: dict, cam_id: str = "default", cam_name: str = ""):
        self.cam_id = cam_id
        self.cam_name = cam_name or cam_id
        self.serial = str(cam_cfg.get("serial", "") or "")
        self._frame_id = 0
        self.capture_timeout_ms = int(cam_cfg.get("capture_timeout_ms", 300))
        self._init_camera(cam_cfg)

    def _init_camera(self, cfg: dict) -> None:
        w, h = int(cfg["width"]), int(cfg["height"])
        fps = int(cfg["fps"])
        self.image_size = (w, h)

        self.pipeline = rs.pipeline()
        rs_cfg = rs.config()
        if self.serial:
            rs_cfg.enable_device(self.serial)
        rs_cfg.enable_stream(rs.stream.depth, w, h, rs.format.z16, fps)
        rs_cfg.enable_stream(rs.stream.color, w, h, rs.format.bgr8, fps)
        rs_cfg.enable_stream(rs.stream.infrared, 1, w, h, rs.format.y8, fps)
        rs_cfg.enable_stream(rs.stream.infrared, 2, w, h, rs.format.y8, fps)
        profile = self.pipeline.start(rs_cfg)

        try:
            self.serial = profile.get_device().get_info(rs.camera_info.serial_number)
        except Exception:
            pass

        depth_sensor = profile.get_device().first_depth_sensor()
        if depth_sensor.supports(rs.option.emitter_enabled):
            depth_sensor.set_option(
                rs.option.emitter_enabled, int(cfg.get("disable_emitter", 0)),
            )

        # Align depth frames to color camera.
        self.align = rs.align(rs.stream.color)

        warmup_frames = 30
        for i in range(warmup_frames):
            try:
                self.pipeline.wait_for_frames(timeout_ms=10000)
            except RuntimeError:
                print(f"[{self.cam_id}] Warmup frame {i+1}/{warmup_frames} timed out, retrying...")
                continue

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

    @property
    def frame_id(self) -> int:
        return self._frame_id

    def capture(self) -> CaptureData:
        """Capture and return one aligned depth-color frame pair (+ IR)."""
        frames = self.pipeline.wait_for_frames(timeout_ms=10000)
        aligned = self.align.process(frames)

        depth_frame = aligned.get_depth_frame()
        color_frame = aligned.get_color_frame()
        ir_left_frame = frames.get_infrared_frame(1)
        ir_right_frame = frames.get_infrared_frame(2)
        if not depth_frame or not color_frame:
            raise RuntimeError("Failed to get aligned frames")

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
        pipeline = getattr(self, "pipeline", None)
        if pipeline is not None:
            try:
                pipeline.stop()
            except Exception as exc:
                print(f"[RealSense:{self.cam_id}] pipeline.stop ignored: {exc}")
            finally:
                self.pipeline = None


class _ColorCamera:
    """仅彩色相机：multi 模式下提供额外视角（无深度/IR）。"""

    def __init__(self, cam_cfg: dict, cam_id: str, cam_name: str = ""):
        self.cam_id = cam_id
        self.cam_name = cam_name or cam_id
        self.serial = str(cam_cfg.get("serial", "") or "")
        self._frame_id = 0
        self._init_camera(cam_cfg)

    def _init_camera(self, cfg: dict) -> None:
        w, h = int(cfg["width"]), int(cfg["height"])
        fps = int(cfg["fps"])
        self.image_size = (w, h)

        self.pipeline = rs.pipeline()
        try:
            rs_cfg = rs.config()
            if self.serial:
                rs_cfg.enable_device(self.serial)
            rs_cfg.enable_stream(rs.stream.color, w, h, rs.format.bgr8, fps)
            profile = self.pipeline.start(rs_cfg)

            try:
                self.serial = profile.get_device().get_info(rs.camera_info.serial_number)
            except Exception:
                pass

            color = profile.get_stream(rs.stream.color).as_video_stream_profile()
            self.color_intr = color.get_intrinsics()
            self.K = np.array([
                [self.color_intr.fx, 0, self.color_intr.ppx],
                [0, self.color_intr.fy, self.color_intr.ppy],
                [0, 0, 1],
            ], dtype=np.float32)
        except Exception:
            self.close()
            raise

    @property
    def frame_id(self) -> int:
        return self._frame_id

    def capture_color(self) -> np.ndarray:
        """采集一帧彩色图 (H,W,3) bgr uint8。"""
        frames = self.pipeline.wait_for_frames(timeout_ms=self.capture_timeout_ms)
        color_frame = frames.get_color_frame()
        if not color_frame:
            raise RuntimeError(f"[{self.cam_id}] Failed to get color frame")
        self._frame_id += 1
        return np.asanyarray(color_frame.get_data())

    def close(self):
        pipeline = getattr(self, "pipeline", None)
        if pipeline is not None:
            try:
                pipeline.stop()
            except Exception as exc:
                print(f"[RealSense:{self.cam_id}] pipeline.stop ignored: {exc}")
            finally:
                self.pipeline = None


class RealsenseService:
    """RealSense 相机管理器（single = 一台 primary；multi = primary + color-only）。"""

    def __init__(self, config_path: str = "/workspace/mindbridge/src/core/config/realsense-config.yaml"):
        with open(config_path) as f:
            cfg = yaml.safe_load(f)
        env_mode = str(os.environ.get("REALSENSE_MODE", "")).lower()
        if env_mode in {"single", "multi"}:
            cfg["mode"] = env_mode
        self.cfg = cfg
        self.mode = str(cfg.get("mode", "single")).lower()

        self.primary: _FullCamera
        self.aux_cameras: dict[str, _ColorCamera] = {}
        self.aux_errors: dict[str, str] = {}
        self._init_cameras(cfg)

    def _init_cameras(self, cfg: dict) -> None:
        if self.mode == "multi":
            cam_list = cfg.get("cameras") or []
            if not cam_list:
                raise RuntimeError("mode=multi 但 config 中未配置 cameras 列表")
            fallback = cfg.get("camera", {})

            primary_entry = next(
                (c for c in cam_list if str(c.get("role", "")).lower() == "primary"),
                cam_list[0],
            )
            primary_cfg = {**fallback, **primary_entry}
            pid = str(primary_entry.get("id", "primary"))
            pname = str(primary_entry.get("name", pid))
            print(f"Initializing primary camera [{pid}] serial={primary_cfg.get('serial') or '<first>'}")
            self.primary = _FullCamera(primary_cfg, cam_id=pid, cam_name=pname)

            for entry in cam_list:
                if entry is primary_entry:
                    continue
                cid = str(entry.get("id"))
                cname = str(entry.get("name", cid))
                merged = {**fallback, **entry}
                print(f"Initializing color camera [{cid}] serial={merged.get('serial') or '<first>'}")
                try:
                    self.aux_cameras[cid] = _ColorCamera(merged, cam_id=cid, cam_name=cname)
                except Exception as exc:
                    message = f"{type(exc).__name__}: {exc}"
                    self.aux_errors[cid] = message
                    print(f"[RealSense:{cid}] WARNING: auxiliary camera disabled: {message}")
        else:
            cam_cfg = cfg.get("camera", {})
            print(f"Initializing single camera serial={cam_cfg.get('serial') or '<first>'}")
            self.primary = _FullCamera(cam_cfg, cam_id="default", cam_name="default")

    @property
    def image_size(self):
        return self.primary.image_size

    @property
    def K(self) -> np.ndarray:
        return self.primary.K

    @property
    def baseline(self) -> float:
        return self.primary.baseline

    @property
    def frame_id(self) -> int:
        return self.primary.frame_id if getattr(self, "primary", None) is not None else 0

    def capture(self) -> CaptureData:
        """采集 primary 相机一帧（完整 彩色+深度+IR）。"""
        return self.primary.capture()

    def capture_aux(self) -> dict[str, np.ndarray]:
        """采集全部 color-only 相机各一帧彩色图，返回 {cam_id: color_bgr}。"""
        frames: dict[str, np.ndarray] = {}
        for cid, cam in list(self.aux_cameras.items()):
            try:
                frames[cid] = cam.capture_color()
            except Exception as exc:
                message = f"{type(exc).__name__}: {exc}"
                self.aux_errors[cid] = message
                print(f"[RealSense:{cid}] WARNING: capture skipped: {message}")
        return frames

    def aux_meta(self) -> list[dict]:
        return [
            {"id": c.cam_id, "name": c.cam_name, "serial": c.serial, "role": "color"}
            for c in self.aux_cameras.values()
        ]

    def cameras_meta(self) -> list[dict]:
        meta = [{
            "id": self.primary.cam_id,
            "name": self.primary.cam_name,
            "serial": self.primary.serial,
            "role": "primary",
        }]
        meta.extend(self.aux_meta())
        return meta

    def close(self):
        cv2.destroyAllWindows()
        for cam in self.aux_cameras.values():
            cam.close()
        self.aux_cameras.clear()
        if getattr(self, "primary", None) is not None:
            self.primary.close()
            self.primary = None  # type: ignore[assignment]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
