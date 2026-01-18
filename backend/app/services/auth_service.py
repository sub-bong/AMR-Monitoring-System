from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Map, MapAccess


async def get_map_if_allowed(db: AsyncSession, map_id: str,
                             subject_type: str, subject_id: int) -> Optional[Map]:
    result = await db.execute(select(Map).where(Map.map_id == map_id))
    map_obj = result.scalar_one_or_none()

    if not map_obj:
        return None

    access = await db.execute(
        select(MapAccess).where(
            MapAccess.map_id == map_obj.id,
            MapAccess.subject_type == subject_type,
            MapAccess.subject_id == subject_id,
        )
    )

    if not access.scalar_one_or_none():
        return None

    return map_obj
