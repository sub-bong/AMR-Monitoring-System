from typing import Tuple

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import SessionLocal
from app.models import User, Device

bearer = HTTPBearer()


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


def decode_token(token: str) -> Tuple[str, str]:
    try:
        payload = jwt.decode(token, settings.jwt_secret,
                             algorithms=[settings.jwt_alg])
        subject = str(payload.get("sub"))
        subject_type = str(payload.get("typ"))

        if not subject or subject_type not in ("user", "device"):
            raise ValueError("invalid token")

        return subject, subject_type

    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_token")


async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
) -> User:
    subject, subject_type = decode_token(creds.credentials)

    if subject_type != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="user_required")

    result = await db.execute(select(User).where(User.id == int(subject)))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="user_not_found")

    return user


async def get_current_device(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
) -> Device:
    subject, subject_type = decode_token(creds.credentials)

    if subject_type != "device":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="device_required")

    result = await db.execute(select(Device).where(Device.id == int(subject)))
    device = result.scalar_one_or_none()

    if not device:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="device_not_found")

    return device
