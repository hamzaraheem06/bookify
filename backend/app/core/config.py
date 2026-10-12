from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):
    database_url: str = "sqlite:///./bookpilot.db"
    jwt_secret: str = "change-me-in-local-env"
    jwt_expire_minutes: int = 1440
    storage_root: Path = ROOT / "storage"
    max_upload_bytes: int = 25 * 1024 * 1024
    tts_provider: str = "mock"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    model_config = SettingsConfigDict(env_file=ROOT / ".env", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [value.strip() for value in self.cors_origins.split(",") if value.strip()]

settings = Settings()
