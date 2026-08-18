from __future__ import annotations

from functools import lru_cache
from typing import Literal, Self

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        frozen=True,
    )

    app_env: Literal["development", "test", "staging", "production"] = "development"
    live_trading_enabled: bool = False

    postgres_host: str = "127.0.0.1"
    postgres_port: int = Field(default=5432, ge=1, le=65535)
    postgres_db: str = "trading_system"
    postgres_user: str = "trading_app"
    postgres_password: SecretStr = SecretStr("UNBOUND_REQUIRED")

    @model_validator(mode="after")
    def enforce_scaffold_authority_lock(self) -> Self:
        if self.live_trading_enabled:
            raise ValueError("package 0.1.0 hard-locks LIVE_TRADING_ENABLED=false")
        return self

    @property
    def database_url(self) -> URL:
        return URL.create(
            "postgresql+psycopg",
            username=self.postgres_user,
            password=self.postgres_password.get_secret_value(),
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        )

    @property
    def database_credentials_bound(self) -> bool:
        return self.postgres_password.get_secret_value() != "UNBOUND_REQUIRED"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
