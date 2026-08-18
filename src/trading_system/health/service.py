from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from trading_system.db.session import get_engine
from trading_system.settings import get_settings


class HealthReport(BaseModel):
    model_config = ConfigDict(frozen=True)

    status: Literal["ALIVE", "READY", "DEGRADED"]
    database: Literal["NOT_CHECKED", "AVAILABLE", "UNBOUND", "UNAVAILABLE"]
    live_authorized: Literal[False] = False
    reason_code: str


def liveness() -> HealthReport:
    return HealthReport(
        status="ALIVE",
        database="NOT_CHECKED",
        reason_code="AUTH_LIVE_DISABLED",
    )


def readiness() -> HealthReport:
    settings = get_settings()
    if not settings.database_credentials_bound:
        return HealthReport(
            status="DEGRADED",
            database="UNBOUND",
            reason_code="AUTH_UNBOUND_EXTERNAL",
        )
    try:
        with get_engine().connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        return HealthReport(
            status="DEGRADED",
            database="UNAVAILABLE",
            reason_code="DATABASE_UNAVAILABLE",
        )
    return HealthReport(
        status="READY",
        database="AVAILABLE",
        reason_code="AUTH_LIVE_DISABLED",
    )
