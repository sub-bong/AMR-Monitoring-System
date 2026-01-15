from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base import Base


class Snapshot(Base):
    '''
    ## snapshots 테이블 \n
    - id: integer, pk \n
    - map_id: integer, fk(maps.id), index \n
    - image_url: string(500) \n
    - pose: JSONB \n
    - intrinsics: JSONB \n
    - created_at: datetime\n
    '''

    __tablename__ = "snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    map_id: Mapped[int] = mapped_column(ForeignKey("maps.id"), index=True)
    image_url: Mapped[str] = mapped_column(String(500))
    pose: Mapped[dict] = mapped_column(JSONB)
    intrinsics: Mapped[dict] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
