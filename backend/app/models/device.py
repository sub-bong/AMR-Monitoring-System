from datetime import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Device(Base):
    '''
    ## devices 테이블 \n
    - id: integer, pk \n
    - device_key_hash: string(255) \n
    - device_key_digest: string(64), uk, index \n
    - name: string(100) \n
    - created_at: datetime\n
    '''

    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_key_hash: Mapped[str] = mapped_column(String(255))
    device_key_digest: Mapped[str] = mapped_column(
        String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
