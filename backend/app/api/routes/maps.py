from datetime import datetime
import pytz

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models import Map, MapAccess
from app.schemas.map import MapCreate

seoul_tz = pytz.timezone('Asia/Seoul')

router = APIRouter(prefix="/maps", tags=["maps"])


@router.post("")
async def create_map(
    payload: MapCreate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    existing = await db.execute(select(Map).where(Map.map_id == payload.map_id))

    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="map_id_taken")

    m = Map(
        map_id=payload.map_id,
        name=payload.name,
        polygon=[p.model_dump() for p in payload.polygon],
        meta=payload.meta or {},
        created_at=datetime.now(seoul_tz),
    )

    db.add(m)
    await db.commit()
    await db.refresh(m)

    db.add(
        MapAccess(
            map_id=m.id,
            subject_type="user",
            subject_id=user.ig,
            created_at=datetime.now(seoul_tz),
        )
    )

    await db.commit()

    return {"ok": True, "map_id": m.map_id}


@router.get("/{map_id}")
async def get_map(
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

    return {"ok": True, "map": {"map_id": m.map_id, "name": m.name, "polygon": m.polygon, "meta": m.meta}}
