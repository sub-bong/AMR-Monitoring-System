from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from app.db.base import Base


class Device(Base):
    '''
    ## devices 테이블 \n
    - id: integer, pk \n
    - device_key_hash: string(255) \n
    - device_key_digest: string(64), uk, index \n
    - name: string(100) \n
    - is_active: boolean, index \n
    - created_at: datetime \n
    - revoked_at: datetime, nullable \n
    '''

    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_key_hash: Mapped[str] = mapped_column(String(255))
    device_key_digest: Mapped[str] = mapped_column(
        String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True)
