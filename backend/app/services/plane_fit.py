import numpy as np


def fit_plane_ransac(points, iterations=200, threshold=0.02):
    best_inliers = []
    best_plane = None

    n = points.shape[0]
    if n < 3:
        return None

    for _ in range(iterations):
        idx = np.random.choice(n, 3, replace=False)
        p1, p2, p3 = points[idx]

        v1 = p2 - p1
        v2 = p3 - p1
        normal = np.cross(v1, v2)
        if np.linalg.norm(normal) < 1e-6:
            continue
        normal = normal / np.linalg.norm(normal)

        d = -np.dot(normal, p1)
        dist = np.abs(points @ normal + d)
        inliers = points[dist < threshold]

        if len(inliers) > len(best_inliers):
            best_inliers = inliers
            best_plane = (normal, d)

    return best_plane, np.array(best_inliers)
