from datetime import datetime
import pytz

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_device, get_current_user, get_db
from app.models import Map, MapAccess, Snapshot
from app.schemas.snapshot import SnapshotCreate

seoul_tz = pytz.timezone("Asia/Seoul")

router = APIRouter(prefix="/snapshots", tags=["snapshots"])


@router.post("")
async def create_snapshot(
    payload: SnapshotCreate,
    device=Depends(get_current_device),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Map).where(Map.map_id == payload.map_id))
    m = result.scalar_one_or_none()

    if not m:
        raise HTTPException(status_code=404, detail="map_not_found")

    access = await db.execute(
        select(MapAccess).where(
            MapAccess.map_id == m.id,
            MapAccess.subject_type == "device",
            MapAccess.subject_id == device.id,
        )
    )

    if not access.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="map_access_denied")

    s = Snapshot(
        map_id=m.id,
        image_url=payload.image_url,
        pose=payload.pose,
        intrinsics=payload.intrinsics,
        created_at=datetime.now(seoul_tz),
    )

    db.add(s)
    await db.commit()
    await db.refresh(s)

    return {"ok": True, "snapshot_id": s.id}


@router.get("/maps/{map_id}")
async def list_snapshots(
    map_id: str,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Map).where(Map.map_id == map_id))
    m = result.scalar_one_or_none()

    if not m:
        raise HTTPException(status_code=404, detail="map_not_found")

    access = await db.execute(
        select(MapAccess).where(
            MapAccess.map_id == m.id,
            MapAccess.subject_type == "user",
            MapAccess.subject_id == user.id,
        )
    )

    if not access.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="map_access_denied")

    rows = await db.execute(select(Snapshot).where(Snapshot.map_id == m.id))
    items = rows.scalars().all()

    return {
        "ok": True,
        "items": [
            {
                "id": s.id,
                "map_id": map_id,
                "image_url": s.image_url,
                "pose": s.pose,
                "intrinsics": s.intrinsics,
            }
            for s in items
        ],
    }
