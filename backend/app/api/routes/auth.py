from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models import User, Device
from app.schemas.auth import DeviceAuthIn, LoginIn, RegisterIn, TokenOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenOut)
async def register(payload: RegisterIn, db: AsyncSession = Depends(get_db)) -> TokenOut:
    existing = await db.execute(select(User).where(User.email == payload.email))

    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="emil_taken")

    user = User(
        email=payload.email,
        hash_password=hash_password(payload.password),
        create_at=datetime.now(timezone.utc),
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token(str(user.id), "user")

    return TokenOut(access_token=token)


@router.post("/login", response_model=TokenOut)
async def login(payload: LoginIn, db: AsyncSession = Depends(get_db)) -> TokenOut:
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_device_key")

    token = create_access_token(str(user.id), "user")

    return TokenOut(access_token=token)


@router.post("/device", response_model=TokenOut)
async def device_auth(payload: DeviceAuthIn, db: AsyncSession = Depends(get_db)) -> TokenOut:
    result = await db.execute(select(Device).where(Device.device_key == payload.device_key))
    device = result.scalar_one_or_none()

    if not device:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_device_key")

    token = create_access_token(str(device.id), "device")

    return TokenOut(access_token=token)
