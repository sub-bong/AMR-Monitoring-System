from datetime import datetime
import pytz

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import create_access_token, hash_password, verify_password, device_key_digest, verify_device_key
from app.models import User, Device
from app.schemas.auth import DeviceAuthIn, LoginIn, RegisterIn, TokenOut

seoul_tz = pytz.timezone('Asia/Seoul')  # 대한민국/서울 time zone

router = APIRouter(prefix="/auth", tags=["auth"])

'''
auth.py 토큰 발급 기능
'''


@router.post("/register", response_model=TokenOut)
async def register(payload: RegisterIn, db: AsyncSession = Depends(get_db)):
    '''
    회원가입 기능

    :param payload: email과 password만 전달 받음
    :type payload: RegisterIn
    :param db: 
    :type db: AsyncSession
    :return: user 토큰 발행
    :rtype: TokenOut
    '''
    existing = await db.execute(select(User).where(User.email == payload.email))  # 이메일 중복 확안을 위한 쿼리: db에 저장된 User.email과 전송된 email 데이터가 같은지 비교하는 쿼리문 값
    # 이미 존재하는 이메일인지 검증: existing 결과가 하나 혹은 비어있는 경우 None, 하나 이상이면 예외 발생
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="email_taken")
    # user 테이블에 저장할 값 지정
    user = User(
        email=payload.email,  # 전달된/입력된 email
        hashed_password=hash_password(payload.password),  # hash 처리된 password
        created_at=datetime.now(seoul_tz),  # kst
    )

    db.add(user)  # user의 값을 세션에 추가, db에 저장 X
    await db.commit()  # db에 반영
    await db.refresh(user)  # db 새로고침

    token = create_access_token(str(user.id), "user")  # user 토큰 생성

    return TokenOut(access_token=token)  # user 토큰 발급


@router.post("/login", response_model=TokenOut)
async def login(payload: LoginIn, db: AsyncSession = Depends(get_db)):
    '''
    ### 로그인 기능
    '''
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()

    # 로그인 실패 처리: 이메일이 없는지 혹은 비밀번호가 틀린지 검증
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_user_key")

    token = create_access_token(str(user.id), "user")  # user 토큰 생성

    return TokenOut(access_token=token)  # user 토큰 발급


@router.post("/device", response_model=TokenOut)
async def device_auth(payload: DeviceAuthIn, db: AsyncSession = Depends(get_db)):
    digest = device_key_digest(payload.device_key)
    result = await db.execute(select(Device).where(Device.device_key_digest == digest))
    device = result.scalar_one_or_none()

    # 디바이스(amr) 로그인: 디바이스 키 존재하지 않으면 인증 실패
    if not device or not verify_device_key(payload.device_key, device.device_key_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_device_key")

    token = create_access_token(str(device.id), "device")

    return TokenOut(access_token=token)
