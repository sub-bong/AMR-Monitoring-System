import numpy as np
from scipy.spatial import ConvexHull
import alphashape


def plane_basis(normal):
    # u,v 축 생성
    n = normal / np.linalg.norm(normal)
    tmp = np.array([1, 0, 0]) if abs(n[0]) < 0.9 else np.array([0, 1, 0])
    u = np.cross(n, tmp)
    u = u / np.linalg.norm(u)
    v = np.cross(n, u)
    return u, v


def project_to_2d(points, normal):
    u, v = plane_basis(normal)
    xy = np.stack([points @ u, points @ v], axis=-1)
    return xy


def to_polygon(points_2d, method="convex_hull", alpha=1.0):
    if method == "alpha":
        poly = alphashape.alphashape(points_2d, alpha)
        coords = list(poly.exterior.coords)
    else:
        hull = ConvexHull(points_2d)
        coords = points_2d[hull.vertices].tolist()
        coords.append(coords[0])  # 닫기

    return [{"x": float(x), "y": float(y)} for x, y in coords]
