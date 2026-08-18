from __future__ import annotations

from functools import lru_cache

from sqlalchemy import Engine, create_engine

from trading_system.settings import get_settings


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    settings = get_settings()
    return create_engine(settings.database_url, pool_pre_ping=True, future=True)
