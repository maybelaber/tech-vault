"""App settings — Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    app_name: str = "TechVault"
    debug: bool = False

    # DB (env: DATABASE_URL)
    database_url: str = "postgresql+asyncpg://techvault:techvault_secret@localhost:5432/techvault"

    # Telegram (Login Widget hash validation)
    telegram_bot_token: str = ""

    # JWT (env: SECRET_KEY)
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days

    # Local dev only: allow POST /api/auth/dev-login (set ALLOW_DEV_LOGIN=true)
    allow_dev_login: bool = False


settings = Settings()
