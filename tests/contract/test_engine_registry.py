from __future__ import annotations

from trading_system.contracts.loader import load_engine_registry


def test_catalog_contains_exactly_112_unimplemented_engines() -> None:
    registry = load_engine_registry()
    assert registry.expected_count == 112
    assert len(registry.engines) == 112
    assert [engine.engine_id for engine in registry.engines] == list(range(1, 113))
    assert all(engine.runtime_status == "NOT_IMPLEMENTED" for engine in registry.engines)


def test_v3_added_engine_range_is_present() -> None:
    registry = load_engine_registry()
    added = [engine for engine in registry.engines if engine.source == "V3.0.0_ADDED"]
    assert [engine.engine_id for engine in added] == list(range(97, 113))
