"""Application configuration via environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """CRM API configuration.

    All values have defaults for local development.
    Override via environment variables or .env file.
    """

    app_name: str = "CRM API"
    app_version: str = "1.0.0"
    debug: bool = False

    # Database
    database_url: str = "sqlite+aiosqlite:///./crm.db"
    database_url_sync: str = "sqlite:///./crm.db"

    # Auth
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 60

    # API
    allowed_origins: list[str] = ["*"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
