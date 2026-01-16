import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "your_app_name")
    api_host: str = os.getenv("API_HOST", "your_host")
    api_port: int = int(os.getenv("API_PORT", "your_port"))
    database_url: str = os.getenv(
        "DATABASE_URL",
        "your_db_url",
    )
    jwt_secret: str = os.getenv("JWT_SECRET", "your_jwt_secret")
    jwt_alg: str = os.getenv("JWT_ALG", "your_jwt_alg")
    jwt_expires_min: int = int(os.getenv("JWT_EXPIRES_MIN", "your_jwt_exp"))
    retention_days: int = int(
        os.getenv("RETENTION_DAYS", "your_retention_days"))


settings = Settings()
