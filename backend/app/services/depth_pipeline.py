import asyncio
from datetime import datetime, timezone

import numpy as np
from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import Map, MapBuildJob, Snapshot
from app.services.depth_model import load_depth_model, infer_depth
from app.services.image_utils import decode_data_url
from app.services.pointcloud import backproject, apply_pose
from app.services.plane_fit import fit_plane_ransac
from app.services.polygon import project_to_2d, to_polygon


async def run_build_job(job_id: int):
    async with SessionLocal() as db:
        job = await db.get(MapBuildJob, job_id)
        if not job:
            return
        job.status = "running"
        await db.commit()

        m = await db.get(Map, job.map_id)
        snaps = await db.execute(select(Snapshot).where(Snapshot.map_id == m.id))
        items = snaps.scalars().all()

    try:
        result = await asyncio.to_thread(run_depth_pipeline_sync, items)
    except Exception as exc:
        async with SessionLocal() as db:
            job = await db.get(MapBuildJob, job_id)
            if job:
                job.status = "failed"
                job.error = str(exc)
                job.finished_at = datetime.now(timezone.utc)
                await db.commit()
        return

    async with SessionLocal() as db:
        job = await db.get(MapBuildJob, job_id)
        m = await db.get(Map, job.map_id)
        if job and m:
            job.status = "done"
            job.result_meta = result.get("meta", {})
            job.finished_at = datetime.now(timezone.utc)
            m.polygon = result["polygon"]
            m.meta = {**(m.meta or {}), "build": result.get("meta", {})}
            await db.commit()


def run_depth_pipeline_sync(snapshots):
    model = load_depth_model()
    all_points = []

    for s in snapshots:
        img = decode_data_url(s.image_url)
        depth = infer_depth(model, img)  # (H, W)

        fx = s.intrinsics["fx"]
        fy = s.intrinsics["fy"]
        cx = s.intrinsics["cx"]
        cy = s.intrinsics["cy"]

        pts = backproject(depth, fx, fy, cx, cy)

        pos = s.pose["pos"]
        rot = s.pose["rot"]
        pts_w = apply_pose(pts, pos, rot)

        # 다운샘플링
        if pts_w.shape[0] > 20000:
            idx = np.random.choice(len(pts_w), 20000, replace=False)
            pts_w = pts_w[idx]

        all_points.append(pts_w)

    pts = np.concatenate(all_points, axis=0)

    plane, inliers = fit_plane_ransac(pts, iterations=300, threshold=0.03)
    if plane is None:
        raise RuntimeError("plane_fit_failed")

    normal, d = plane
    xy = project_to_2d(inliers, normal)

    polygon = to_polygon(xy, method="convex_hull")

    return {
        "polygon": polygon,
        "meta": {
            "snapshot_count": len(snapshots),
            "points": len(inliers),
            "algo": "convex_hull"
        },
    }
