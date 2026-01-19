from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models import Map, TelemetryLast
from app.services.auth_service import get_map_if_allowed

router = APIRouter(prefix="/telemetry", tags=["telemetry"])


@router.get("/maps/{map_id}/amr/{amr_id}/last")
async def get_last(
    map_id: str,
    amr_id: str,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    map_obj = await get_map_if_allowed(db, map_id, "user", user.id)

    if not map_obj:
        raise HTTPException(status_code=403, detail="map_access_denied")

    result = await db.execute(
        select(TelemetryLast).where(
            TelemetryLast.map_id == map_obj.id,
            TelemetryLast.amr_id == amr_id,
        )
    )

    row = result.scalar_one_or_none()

    if not row:
        raise HTTPException(status_code=404, detail="amr_not_found")

    return {"ok": True, "telemetry": row.payload}
