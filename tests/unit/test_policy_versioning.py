from datetime import UTC, datetime, timedelta

import pytest

from trading_system.core.versioning import ConfigRegistry, VersionedConfig
from trading_system.governance.policy import PolicySnapshot


def test_policy_evaluation_and_version_registry_are_fail_closed() -> None:
    now = datetime(2026, 1, 1, tzinfo=UTC)
    policy = PolicySnapshot(
        policy_id="p",
        version="1",
        effective_at=now,
        expires_at=now + timedelta(days=1),
        rules={"mode": "PAPER"},
        approved=True,
    )
    assert policy.evaluate({"mode": "PAPER"}, at=now) == (True, ())
    assert policy.evaluate({"mode": "LIVE"}, at=now)[0] is False
    registry = ConfigRegistry()
    config = VersionedConfig("c", "1", "a" * 64, effective=True)
    registry.publish(config)
    assert registry.resolve("c", "1") == config
    with pytest.raises(ValueError):
        registry.publish(config)
