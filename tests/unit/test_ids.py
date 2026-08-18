from __future__ import annotations

import uuid

import pytest

from trading_system.core.ids import new_id


def test_new_id_uses_uuid7() -> None:
    value = new_id("evt")
    parsed = uuid.UUID(hex=value.removeprefix("evt_"))
    assert parsed.version == 7


def test_invalid_prefix_is_rejected() -> None:
    with pytest.raises(ValueError):
        new_id("Bad Prefix")
