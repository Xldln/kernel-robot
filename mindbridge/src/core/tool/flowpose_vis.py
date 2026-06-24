"""FlowPose 3D 位姿可视化 — 在图上绘制 3D 包围盒和坐标轴。"""

import cv2
import numpy as np


def get_3d_bbox(size):
    w, h, d = size[0], size[1], size[2]
    return np.array([
        [+w/2, +w/2, -w/2, -w/2, +w/2, +w/2, -w/2, -w/2],
        [+h/2, +h/2, +h/2, +h/2, -h/2, -h/2, -h/2, -h/2],
        [+d/2, -d/2, +d/2, -d/2, +d/2, -d/2, +d/2, -d/2]
    ])


def _transform(coords, pose):
    h = np.vstack([coords, np.ones((1, coords.shape[1]))])
    t = pose @ h
    return t[:3, :] / t[3, :]


def _project(coords_3d, fx, fy, cx, cy):
    K = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
    p = K @ coords_3d
    return (p[:2, :] / p[2, :]).T.astype(np.int32)


def draw_3d_bbox(img, pose, size, fx, fy, cx, cy,
                 color=(0, 255, 0), thickness=2, alpha=0.3):
    corners = _transform(get_3d_bbox(size), pose)
    pts = _project(corners, fx, fy, cx, cy)

    faces = [
        [0, 1, 3, 2], [4, 5, 7, 6],
        [0, 1, 5, 4], [2, 3, 7, 6],
        [0, 2, 6, 4], [1, 3, 7, 5],
    ]
    for fi in faces:
        overlay = img.copy()
        cv2.fillPoly(overlay, [pts[fi]], color)
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

    lo = (int(color[0]*0.3), int(color[1]*0.3), int(color[2]*0.3))
    mi = (int(color[0]*0.6), int(color[1]*0.6), int(color[2]*0.6))
    for i, j in zip([4, 5, 6, 7], [5, 7, 4, 6]):
        cv2.line(img, tuple(pts[i]), tuple(pts[j]), lo, thickness)
    for i, j in zip(range(4), range(4, 8)):
        cv2.line(img, tuple(pts[i]), tuple(pts[j]), mi, thickness)
    for i, j in zip([0, 1, 2, 3], [1, 3, 0, 2]):
        cv2.line(img, tuple(pts[i]), tuple(pts[j]), color, thickness)

    # 坐标轴
    ax = _transform(np.array([[0, 0.08, 0, 0], [0, 0, 0.08, 0], [0, 0, 0, 0.08]]), pose)
    ap = _project(ax, fx, fy, cx, cy)
    o = tuple(ap[0])
    cv2.line(img, o, tuple(ap[1]), (0, 0, 255), thickness)   # X=red
    cv2.line(img, o, tuple(ap[2]), (0, 255, 0), thickness)   # Y=green
    cv2.line(img, o, tuple(ap[3]), (255, 0, 0), thickness)   # Z=blue

    return img


def draw_all_poses(img, objects, fx, fy, cx, cy, **kw):
    for obj in objects:
        pose = np.array(obj["pose"], dtype=np.float32)
        length = np.array(obj["length"], dtype=np.float32)
        draw_3d_bbox(img, pose, length, fx, fy, cx, cy, **kw)
    return img
