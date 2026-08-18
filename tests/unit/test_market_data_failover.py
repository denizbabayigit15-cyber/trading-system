import pytest

from trading_system.market_data.failover import ProviderHealth, ProviderState, choose_provider


def test_failover_selects_highest_known_sequence() -> None:
    selected = choose_provider(
        (
            ProviderHealth("a", ProviderState.HEALTHY, 3),
            ProviderHealth("b", ProviderState.HEALTHY, 4),
        )
    )
    assert selected.provider_id == "b"


def test_failover_fails_closed_without_healthy_provider() -> None:
    with pytest.raises(RuntimeError):
        choose_provider((ProviderHealth("a", ProviderState.UNKNOWN, None),))
