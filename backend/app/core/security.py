from datetime import datetime, timedelta
import pytz
from typing import Any, Optional

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

seoul_tz = pytz.timezone("Asia/Seoul")  # 대한민국/서울 time zone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

'''
security.py 토큰 생성과 비밀번호 검증 기능
'''


def hash_password(password: str) -> str:
    '''
    ### password 해싱 기능(bcrypt)
    '''
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    '''
    ### password 해싱 검증
    prams: plain, hashed
    '''
    return pwd_context.verify(plain, hashed)


def create_access_token(
        subject: str,
        subject_type: str,
        expires_min: Optional[int] = None,
) -> str:
    '''
    ### 토큰 생성 기능
    ### 데이터 구조
    sub: id
    typ: user/device 구분
    iat: 토큰 발급 시간
    exp: 토큰 만료 시간
    {
      "sub": "123",
      "typ": "user",
      "iat": 1736851200,
      "exp": 1736858400
    }
    '''
    now = datetime.now(seoul_tz)
    exp = now + timedelta(minutes=expires_min or settings.jwt_expires_min)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": subject_type,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }

    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)
