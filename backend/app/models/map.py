from datetime import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base import Base


class Map(Base):
    '''
    ## maps 테이블 \n
    - id: integer, pk \n
    - map_id: string(64), uk, index \n
    - name: string(100) \n
    - polygon: pg의 JSONB \n
    - meta: pg의 JSONB \n
    - created_at: datetime\n
    '''

    __tablename__ = "maps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    map_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    polygon: Mapped[dict] = mapped_column(JSONB)  # 형태: [{"x": ...}, ...]
    meta: Mapped[dict] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
