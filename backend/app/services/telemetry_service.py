from datetime import datetime
import pytz

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TelemetryLast, TelemetryHistory
from app.schemas.telemetry import TelemetryIn

seoul_tz = pytz.timezone("Asia/Seoul")


async def save_telemetry(
        db: AsyncSession, map_pk: int, payload: TelemetryIn):
    now = datetime.now(seoul_tz)
    ts = (
        datetime.fromtimestamp(
            payload.ts / 1000, tz=seoul_tz) if payload.ts else now
    )

    data = payload.model_dump()

    upsert = insert(TelemetryLast).values(
        map_id=map_pk,
        amr_id=payload.amr_id,
        payload=data,
        updated_at=now,
    ).on_conflict_do_update(
        index_elements=["map_id", "amr_id"],
        set_={"payload": data, "updated_at": now},
    )

    await db.execute(upsert)

    db.add(
        TelemetryHistory(
            map_id=map_pk,
            amr_id=payload.amr_id,
            payload=data,
            ts=ts,
        )
    )

    await db.commit()
