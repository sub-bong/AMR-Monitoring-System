import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "amr-monitoring")
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://test:test@localhost:5432/test",
    )
    jwt_secret: str = os.getenv("JWT_SECRET", "your_jwt_secret")
    jwt_alg: str = os.getenv("JWT_ALG", "HS256")
    jwt_expires_min: int = int(os.getenv("JWT_EXPIRES_MIN", "120"))
    retention_days: int = int(os.getenv("RETENTION_DAYS", "1"))


settings = Settings()
