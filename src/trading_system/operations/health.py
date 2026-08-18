from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class HealthStatus(StrEnum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class HealthCheck:
    component: str
    status: HealthStatus
    checked_at: datetime
    reason_codes: tuple[str, ...] = ()


def aggregate_health(checks: tuple[HealthCheck, ...]) -> HealthCheck:
    if not checks:
        raise ValueError("at least one health check is required")
    if any(check.status is HealthStatus.UNKNOWN for check in checks):
        status = HealthStatus.UNKNOWN
        reasons: tuple[str, ...] = ("HEALTH_CHECK_UNKNOWN",)
    elif any(check.status is HealthStatus.DEGRADED for check in checks):
        status = HealthStatus.DEGRADED
        reasons = tuple(dict.fromkeys(reason for check in checks for reason in check.reason_codes))
    else:
        status = HealthStatus.HEALTHY
        reasons = ()
    return HealthCheck("system", status, max(check.checked_at for check in checks), reasons)
