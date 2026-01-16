from fastapi import FastAPI

from app.core.config import settings

from app.api.routes import auth

app = FastAPI(title=settings.app_name)

app.include_router(auth.router)


@app.get("/health_ck")
def health_ck():
    return {"ok": True}
