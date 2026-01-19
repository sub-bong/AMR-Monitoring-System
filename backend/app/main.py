from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from app.core.config import settings

from app.api.routes import auth, telemetry, ws
from app.services.retention_service import retention_loop


@asynccontextmanager
async def start_retention(app: FastAPI):
    task = asyncio.create_task(retention_loop())

    try:
        yield
    finally:
        task.cancel()

app = FastAPI(title=settings.app_name, lifespan=start_retention)

app.include_router(auth.router)
app.include_router(telemetry.router)
app.include_router(ws.router)


@app.get("/")
def health_ck():
    return {"ok": True}
