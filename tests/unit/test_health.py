from datetime import UTC, datetime

from trading_system.operations.health import HealthCheck, HealthStatus, aggregate_health


def test_health_aggregation_fails_closed_on_unknown() -> None:
    result = aggregate_health(
        (
            HealthCheck("feed", HealthStatus.HEALTHY, datetime(2026, 1, 1, tzinfo=UTC)),
            HealthCheck("broker", HealthStatus.UNKNOWN, datetime(2026, 1, 1, tzinfo=UTC)),
        )
    )
    assert result.status is HealthStatus.UNKNOWN
    assert result.reason_codes == ("HEALTH_CHECK_UNKNOWN",)
