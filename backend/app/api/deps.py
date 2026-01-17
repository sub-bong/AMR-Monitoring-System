from typing import Tuple, AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import SessionLocal
from app.models import User, Device

bearer = HTTPBearer()

'''
deps.py user/device 토큰의 유효성 검사 기능 
'''


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


def decode_token(token: str) -> Tuple[str, str]:
    '''
    :param token: 토큰 값을 받아 디코딩
    :type token: str
    :return: (subject, subject_type)을 반환
    :rtype: Tuple[str,str]
    '''
    try:
        payload = jwt.decode(token, settings.jwt_secret,
                             algorithms=[settings.jwt_alg])
        # 입력 받은 토큰, 사용한 jwt key(env 값), 사용한 jwt 알고리즘
        subject = str(payload.get("sub"))
        subject_type = str(payload.get("typ"))

        # user나 device
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
    '''
    ### user 토큰의 유효성 검사
    '''
    subject, subject_type = decode_token(creds.credentials)

    # subject_type이 user인지 검사
    if subject_type != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="user_required")

    # users.id == subject 인 사용자 1건 조회
    result = await db.execute(select(User).where(User.id == int(subject)))
    user = result.scalar_one_or_none()  # 있으면 User 객체, 없으면 None

    # user 값이 존재하지 않으면 예외 발생
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="user_not_found")

    return user


async def get_current_device(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
) -> Device:
    '''
    ### device 토큰의 유효성 검사
    '''
    subject, subject_type = decode_token(creds.credentials)

    # subject_type이 device인지 검사
    if subject_type != "device":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="device_required")

    result = await db.execute(select(Device).where(Device.id == int(subject)))
    device = result.scalar_one_or_none()

    if not device:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="device_not_found")

    return device
