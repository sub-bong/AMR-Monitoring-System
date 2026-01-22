from datetime import datetime
import pytz
import secrets

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.security import device_key_digest, hash_device_key
from app.models import Device, Map, MapAccess
from app.schemas.device import DeviceCreate, DeviceKeyOut

seoul_tz = pytz.timezone("Asia/Seoul")

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("")
async def list_devices(admin=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    rows = await db.execute(select(Device))
    items = rows.scalars().all()
    return {
        "ok": True,
        "items": [{"id": d.id, "name": d.name, "is_active": d.is_active} for d in items]
    }


@router.post("", response_model=DeviceKeyOut)
async def create_device(
    payload: DeviceCreate,
    admin=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    plain_key = secrets.token_urlsafe(32)
    digest = device_key_digest(plain_key)
    hashed = hash_device_key(plain_key)

    d = Device(
        name=payload.name,
        device_key_digest=digest,
        device_key_hash=hashed,
        is_active=True,
        created_at=datetime.now(seoul_tz),
    )
    db.add(d)
    await db.commit()
    await db.refresh(d)

    if payload.map_id:
        result = await db.execute(select(Map).where(Map.map_id == payload.map_id))
        m = result.scalar_one_or_none()
        if not m:
            raise HTTPException(status_code=404, detail="map_not_found")
        db.add(
            MapAccess(
                map_id=m.id,
                subject_type="device",
                subject_id=d.id,
                created_at=datetime.now(seoul_tz),
            )
        )
        await db.commit()

    return DeviceKeyOut(device_id=d.id, device_key=plain_key)


@router.patch("/{device_id}/revoke")
async def revoke_device(
    device_id: int,
    admin=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    d = await db.get(Device, device_id)
    if not d:
        raise HTTPException(status_code=404, detail="device_not_found")
    d.is_active = False
    d.revoked_at = datetime.now(seoul_tz)
    await db.commit()
    return {"ok": True}
