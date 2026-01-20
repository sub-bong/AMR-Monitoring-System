from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio

from app.core.config import settings

from app.api.routes import auth, telemetry, ws, maps, snapshots
from app.services.retention_service import retention_loop


@asynccontextmanager
async def start_retention(app: FastAPI):
    task = asyncio.create_task(retention_loop())

    try:
        yield
    finally:
        task.cancel()

app = FastAPI(title=settings.app_name, lifespan=start_retention)

# CORS Middleware 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip()
                   for origin in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router)
app.include_router(telemetry.router)
app.include_router(ws.router)
app.include_router(maps.router)
app.include_router(snapshots.router)


@app.get("/")
def health_ck():
    return {"ok": True}
