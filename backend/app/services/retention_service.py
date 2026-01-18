import asyncio
from datetime import datetime, timedelta
import pytz

from sqlalchemy import delete

from app.core.config import settings
from app.db.session import SessionLocal
from app.models import TelemetryHistory

seoul_tz = pytz.timezone("Asia/Seoul")


async def purge_old_history():
    cutoff = datetime.now(seoul_tz) - timedelta(days=settings.retention_days)
    async with SessionLocal() as db:
        await db.execute(delete(TelemetryHistory).where(TelemetryHistory.ts < cutoff))
        await db.commit()


async def retention_loop():
    while True:
        await purge_old_history()
        await asyncio.sleep(3600)
