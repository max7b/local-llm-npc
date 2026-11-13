from pydantic_settings import BaseSettings, SettingsConfigDict

from app.constants.paths import BASEDIR


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=BASEDIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
