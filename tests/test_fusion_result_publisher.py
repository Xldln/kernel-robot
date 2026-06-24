from __future__ import annotations

import numpy as np

from mindbridge.src.core.service.FusionResultPublisher import (
    build_siglip_payload,
    build_tf_payload_from_flowpose_result,
    pose_item_to_pose7,
)


def test_pose_item_to_pose7_converts_matrix_translation_and_quaternion() -> None:
    pose = np.eye(4, dtype=np.float32)
    pose[:3, 3] = [0.1, 0.2, 0.3]

    pose7 = pose_item_to_pose7(pose)

    assert pose7 is not None
    assert np.allclose(pose7[:3], [0.1, 0.2, 0.3])
    assert np.isclose(np.linalg.norm(pose7[3:]), 1.0)


def test_build_tf_payload_names_repeated_objects() -> None:
    pose = np.eye(4, dtype=np.float32).tolist()
    payload = {
        "status": "ok",
        "objects": [
            {"name": "green small box", "pose": pose},
            {"name": "green small box", "pose": pose},
        ],
    }

    transforms = build_tf_payload_from_flowpose_result(payload, frame_id="camera_rgb_link")

    assert [item["child_frame_id"] for item in transforms] == [
        "green small box_1",
        "green small box_2",
    ]
    assert all(item["frame_id"] == "camera_rgb_link" for item in transforms)


def test_build_tf_payload_ignores_failed_flowpose_result() -> None:
    assert build_tf_payload_from_flowpose_result({"status": "error", "objects": []}) == []


def test_build_siglip_payload_uses_marvin_fields() -> None:
    payload = build_siglip_payload(
        {"status": "ok", "best_category": "box free and closed", "best_similarity": 0.91},
        frame_id=7,
    )

    assert payload == {
        "frame_id": 7,
        "ok": True,
        "best_category": "box free and closed",
        "best_similarity": 0.91,
    }
