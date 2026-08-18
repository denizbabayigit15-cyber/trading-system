from __future__ import annotations

from datetime import UTC, datetime


def utc_now() -> datetime:
    return datetime.now(UTC)


def require_utc(value: datetime) -> datetime:
    """Reject naive timestamps and normalize aware timestamps to UTC."""
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("decision-bearing timestamps must be timezone-aware")
    return value.astimezone(UTC)
