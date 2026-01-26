import numpy as np


def backproject(depth, fx, fy, cx, cy):
    h, w = depth.shape
    xs, ys = np.meshgrid(np.arange(w), np.arange(h))
    z = depth
    x = (xs - cx) / fx * z
    y = (ys - cy) / fy * z
    pts = np.stack([x, y, z], axis=-1).reshape(-1, 3)
    return pts


def apply_pose(points, pos, rot):
    # rot = [x,y,z,w] quaternion
    x, y, z, w = rot
    q = np.array([w, x, y, z], dtype=np.float32)

    # 회전 행렬
    qw, qx, qy, qz = q
    R = np.array([
        [1-2*qy*qy-2*qz*qz, 2*qx*qy-2*qz*qw, 2*qx*qz+2*qy*qw],
        [2*qx*qy+2*qz*qw, 1-2*qx*qx-2*qz*qz, 2*qy*qz-2*qx*qw],
        [2*qx*qz-2*qy*qw, 2*qy*qz+2*qx*qw, 1-2*qx*qx-2*qy*qy]
    ], dtype=np.float32)

    t = np.array(pos, dtype=np.float32)
    return (points @ R.T) + t
