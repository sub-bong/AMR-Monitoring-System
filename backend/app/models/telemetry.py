from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base import Base


class TelemetryLast(Base):
    '''
    ## telemetry_last 테이블 \n
    - id: integer, pk \n
    - map_id: integer, fk(maps.id), index \n
    - amr_id: string(64), index \n
    - payload: JSONB \n
    - updated_at: datetime\n
    '''

    __tablename__ = "telemetry_last"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    map_id: Mapped[int] = mapped_column(ForeignKey("maps.id"), index=True)
    amr_id: Mapped[str] = mapped_column(String(64), index=True)
    payload: Mapped[dict] = mapped_column(JSONB)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        Index("ix_last_map_amr", "map_id", "amr_id", unique=True),
    )


class TelemetryHistory(Base):
    '''
    ## telemetry_history 테이블 \n
    - id: integer, pk \n
    - map_id: integer, fk(maps.id), index \n
    - amr_id: string(64), index \n
    - payload: JSONB \n
    - ts: datetime \n
    '''

    __tablename__ = "telemetry_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    map_id: Mapped[int] = mapped_column(ForeignKey("maps.id"), index=True)
    amr_id: Mapped[str] = mapped_column(String(64), index=True)
    payload: Mapped[dict] = mapped_column(JSONB)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        Index("ix_hist_map_amr_ts", "map_id", "amr_id", "ts"),
    )
