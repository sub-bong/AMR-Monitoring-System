from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(title=settings.app_name)


@app.get("/health_ck")
def health_ck():
    return {"ok": True}
