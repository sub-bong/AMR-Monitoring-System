import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[3]
load_dotenv(ROOT_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "your_app_name")
    api_host: str = os.getenv("API_HOST", "your_host")
    api_port: int = int(os.getenv("API_PORT", "5432"))
    database_url: str = os.getenv(
        "DATABASE_URL",
        "your_db_url",
    )
    jwt_secret: str = os.getenv("JWT_SECRET", "your_jwt_secret")
    jwt_alg: str = os.getenv("JWT_ALG", "your_jwt_alg")
    jwt_expires_min: int = int(os.getenv("JWT_EXPIRES_MIN", "120"))
    retention_days: int = int(
        os.getenv("RETENTION_DAYS", "1"))

    device_token_secret: str = os.getenv(
        "DEVICE_TOKEN_SECRET", "your_token_device")

    cors_origins: str = os.getenv("CORS_ORIGINS", "yor_cors_url")


settings = Settings()
