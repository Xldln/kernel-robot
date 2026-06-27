"""FlowPose 6D姿态估计 推理服务封装"""

from __future__ import annotations

import os
import sys
import time
from argparse import Namespace
from pathlib import Path
from types import SimpleNamespace

import cv2
import numpy as np
import yaml

from mindbridge.src.core.schemas.FlowPoseEntity import (
    FlowPosePredictRequest,
    FlowPosePredictResponse,
    ObjectPose,
)
from mindbridge.src.core.tool.FlowPoseTools import (
    decode_image_b64,
    to_jsonable,
    unpack_infer_output,
    build_objects,
    save_latest_response,
)


def _load_config(config_path: str | Path) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


class FlowPoseInfer:
    """FlowPose 6D 姿态估计推理引擎"""

    def __init__(self, config_path: str | Path = "/workspace/mindbridge/src/core/config/flowpose-config.yaml"):
        cfg = _load_config(config_path)
        fp_cfg = cfg.get("flowpose", {})

        # ── 路径配置 ──
        paths_cfg = fp_cfg.get("paths", {})
        py_runner_path = paths_cfg.get("py_runner_path", "/workspace/mindbridge/models/flowpose_dino/FlowPose/py_runners")
        if py_runner_path not in sys.path:
            sys.path.insert(0, py_runner_path)

        # ── DINOv2 本地配置 ──
        # meanflow_inference.py 硬编码了 /workspace/model/facebookresearch_dinov2_main/
        # 用软链接指向实际位置，避免修改 FlowPose 源码
        dinov2_code_path = paths_cfg.get("dinov2_code_path", "")
        hardcoded_dino = "/workspace/model/facebookresearch_dinov2_main"
        if dinov2_code_path:
            os.makedirs("/workspace/model", exist_ok=True)
            if not os.path.islink(hardcoded_dino) and not os.path.isdir(hardcoded_dino):
                os.symlink(dinov2_code_path, hardcoded_dino)
                print(f"[FlowPoseInfer] DINOv2 软链接: {dinov2_code_path} → {hardcoded_dino}")
            else:
                print(f"[FlowPoseInfer] DINOv2 软链接已存在")

        # ── 模型路径 ──
        self.pretrained_flow_model_path = paths_cfg.get("pretrained_flow_model_path", "")
        self.pretrained_scale_model_path = paths_cfg.get("pretrained_scale_model_path", "")

        # ── 可视化配置 ──
        vis_cfg = fp_cfg.get("visualization", {})
        self.visualize = bool(fp_cfg.get("visualize", False))
        self.vis_wait = max(1, int(fp_cfg.get("vis_wait", 30)))
        self.fx = float(vis_cfg.get("fx", 606.965))
        self.fy = float(vis_cfg.get("fy", 606.133))
        self.cx = float(vis_cfg.get("cx", 323.882))
        self.cy = float(vis_cfg.get("cy", 257.623))
        self.width = int(vis_cfg.get("width", 640))
        self.height = int(vis_cfg.get("height", 480))
        self.window_width = int(vis_cfg.get("window_width", 640))
        self.window_height = int(vis_cfg.get("window_height", 480))
        self.axis_len = float(vis_cfg.get("axis_len", 0.08))
        self._vis_window = "FlowPose Visualization"
        self._vis_window_created = False

        # ── 调试 ──
        self.save_response = bool(fp_cfg.get("save_response", False))
        self.response_save_path = fp_cfg.get("response_save_path", "latest_response.json")

        # ── 导入 FlowPose 内部模块 ──
        safe_argv = sys.argv[:]
        sys.argv = [sys.argv[0]]

        from api_runner import PoseInferenceSession
        from inference.inference_helper import Flow
        from utils.yomni_vis import visualize_detections

        sys.argv = safe_argv
        self.visualize_detections_func = visualize_detections

        # ── 构建 args ──
        model_cfg = fp_cfg.get("model", {})
        inference_cfg = fp_cfg.get("inference", {})
        debug_cfg = fp_cfg.get("debug", {})

        args = Namespace(
            pretrained_flow_model_path=self.pretrained_flow_model_path,
            pretrained_scale_model_path=self.pretrained_scale_model_path,
            device=inference_cfg.get("device", "cuda"),
            img_size=int(fp_cfg.get("img_size", 224)),
            n_pts=int(fp_cfg.get("n_pts", 1024)),
            frame_gap_threshold=int(fp_cfg.get("frame_gap_threshold", 10)),
            eval_repeat_num=int(fp_cfg.get("eval_repeat_num", 25)),
            retain_ratio=float(fp_cfg.get("retain_ratio", 0.4)),
            enable_tracking=bool(inference_cfg.get("tracking", True)),
            seed=int(debug_cfg.get("seed", 0)),
            dropout=int(fp_cfg.get("dropout", 0)),
            use_edm_aug=bool(fp_cfg.get("use_edm_aug", False)),
            log_dir=debug_cfg.get("log_dir", "debug"),
            use_pretrain=bool(fp_cfg.get("use_pretrain", False)),
            is_train=bool(fp_cfg.get("is_train", False)),
            pose_mode=fp_cfg.get("pose_mode", "rot_matrix"),
            optimizer=fp_cfg.get("optimizer", "Adam"),
            lr=float(fp_cfg.get("lr", 1e-2)),
            lr_decay=float(fp_cfg.get("lr_decay", 0.98)),
            num_points=int(fp_cfg.get("num_points", 1024)),
            scale_embedding=int(fp_cfg.get("scale_embedding", 180)),
            ema_rate=float(fp_cfg.get("ema_rate", 0.999)),
            repeat_num=int(fp_cfg.get("repeat_num", 20)),
            clustering=int(fp_cfg.get("clustering", 1)),
            clustering_eps=float(fp_cfg.get("clustering_eps", 0.05)),
            clustering_minpts=float(fp_cfg.get("clustering_minpts", 0.1667)),
        )

        # ── 加载模型 ──
        print(f"[FlowPoseInfer] Flow 模型路径: {self.pretrained_flow_model_path}")
        print(f"[FlowPoseInfer] Scale 模型路径: {self.pretrained_scale_model_path}")
        print(f"[FlowPoseInfer] 可视化: {'ON' if self.visualize else 'OFF'}")

        t0 = time.time()
        print("[FlowPoseInfer] Loading Flow...")
        self.flow = Flow(args)

        print("[FlowPoseInfer] Creating PoseInferenceSession...")
        self.inferencer = PoseInferenceSession(self.flow, args)

        print(f"[FlowPoseInfer] 模型加载完成 ({time.time() - t0:.2f}s)")

    # ── 相机内参 ────────────────────────────────────────────────

    def _build_cam_intrinsics(self) -> SimpleNamespace:
        data = SimpleNamespace()
        data.fx = self.fx
        data.fy = self.fy
        data.cx = self.cx
        data.cy = self.cy
        data.width = self.width
        data.height = self.height

        K = np.array([
            [self.fx, 0.0, self.cx],
            [0.0, self.fy, self.cy],
            [0.0, 0.0, 1.0],
        ], dtype=np.float32)

        data.intrinsic_matrix = K
        data.K = K
        return data

    # ── 核心推理 ────────────────────────────────────────────────

    def predict(self, req: FlowPosePredictRequest) -> FlowPosePredictResponse:
        rgb = decode_image_b64(req.rgb_image, cv2.IMREAD_COLOR).astype(np.uint8)
        depth = decode_image_b64(req.depth_image, cv2.IMREAD_ANYDEPTH).astype(np.float32)
        combined_mask = decode_image_b64(req.combined_mask, cv2.IMREAD_GRAYSCALE).astype(np.uint8)
        return self.predict_from_arrays(
            rgb, depth, combined_mask,
            obj_ids=req.obj_ids,
            class_names=req.class_names,
            instance_names=req.instance_names,
            request_id=req.request_id,
        )

    def predict_from_arrays(
        self,
        rgb: np.ndarray,
        depth: np.ndarray,
        combined_mask: np.ndarray,
        *,
        obj_ids: list | None = None,
        class_names: list[str] | None = None,
        instance_names: list[str] | None = None,
        request_id: str = "",
    ) -> FlowPosePredictResponse:
        """直接接受 numpy 数组推理（无 base64 开销）。"""
        t_start = time.time()

        if obj_ids is None:
            obj_ids = []
        if class_names is None:
            class_names = []
        if instance_names is None:
            instance_names = []

        try:
            # 推理
            pose_out, length_out = self.inferencer.infer(rgb, depth, combined_mask, obj_ids)
            pose_all, length_all = unpack_infer_output(pose_out, length_out)

            # 可视化（可选）
            if self.visualize:
                try:
                    vis = rgb.copy()
                    valid_output = (
                        pose_all is not None
                        and length_all is not None
                        and len(pose_all) > 0
                        and len(length_all) > 0
                    )
                    if valid_output:
                        all_final_pose = np.asarray(pose_all, dtype=np.float32)
                        all_final_length = np.asarray(length_all, dtype=np.float32)
                        cam_intrinsics = self._build_cam_intrinsics()

                        vis = self.visualize_detections_func(
                            vis,
                            all_final_pose,
                            all_final_length,
                            cam_intrinsics,
                            color=(0, 255, 0),
                            thickness=2,
                            alpha=0.1,
                        )
                    if request_id:
                        cv2.putText(
                            vis, f"request_id: {request_id}",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (255, 255, 255), 2, cv2.LINE_AA,
                        )
                    cv2.putText(
                        vis, f"Elapsed: {time.time() - t_start:.2f}s",
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (255, 255, 255), 2, cv2.LINE_AA,
                    )
                    if not self._vis_window_created:
                        cv2.namedWindow(self._vis_window, cv2.WINDOW_NORMAL)
                        cv2.resizeWindow(self._vis_window, self.window_width, self.window_height)
                        try:
                            cv2.startWindowThread()
                        except Exception:
                            pass
                        self._vis_window_created = True
                    cv2.imshow(self._vis_window, vis)
                    key = cv2.waitKey(self.vis_wait)
                    key_low = key & 0xFF if key >= 0 else -1
                    try:
                        window_closed = cv2.getWindowProperty(self._vis_window, cv2.WND_PROP_VISIBLE) < 1
                    except Exception:
                        window_closed = False
                    if key in (27, ord("q"), ord("Q")) or key_low in (27, ord("q"), ord("Q")) or window_closed:
                        self.close_visualization()
                except Exception as e:
                    print(f"[WARN] Visualization failed: {e}")

            # 空结果处理
            if pose_all is None or length_all is None:
                response = FlowPosePredictResponse(
                    status="ok",
                    request_id=request_id,
                    objects=[],
                    elapsed_sec=round(time.time() - t_start, 4),
                )
                if self.save_response:
                    save_latest_response(response.model_dump(), self.response_save_path)
                return response

            # 组装物体列表
            objects_raw = build_objects(
                pose_all=pose_all,
                length_all=length_all,
                obj_ids=obj_ids,
                class_names=class_names,
                instance_names=instance_names,
            )

            objects = [
                ObjectPose(
                    name=obj["name"],
                    pose=obj["pose"],
                    length=obj["length"],
                    obj_id=obj["obj_id"],
                    box_id=obj["box_id"],
                )
                for obj in objects_raw
            ]

            response = FlowPosePredictResponse(
                status="ok",
                request_id=request_id,
                objects=objects,
                elapsed_sec=round(time.time() - t_start, 4),
            )

            if self.save_response:
                save_latest_response(response.model_dump(), self.response_save_path)

            return response

        except Exception as e:
            elapsed = round(time.time() - t_start, 4)
            return FlowPosePredictResponse(
                status="error",
                request_id=request_id,
                message=str(e),
                elapsed_sec=elapsed,
            )

    def close_visualization(self) -> None:
        self.visualize = False
        if self._vis_window_created:
            try:
                cv2.destroyWindow(self._vis_window)
            except Exception:
                cv2.destroyAllWindows()
            finally:
                self._vis_window_created = False
        print("[FlowPoseInfer] Visualization closed")
