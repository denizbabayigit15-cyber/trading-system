from __future__ import annotations

import pytest
from pydantic import ValidationError

from trading_system.settings import Settings


def test_live_trading_is_false_by_default() -> None:
    settings = Settings(_env_file=None)
    assert settings.live_trading_enabled is False
    assert settings.database_credentials_bound is False


def test_live_trading_cannot_be_enabled_in_scaffold() -> None:
    with pytest.raises(ValidationError, match="hard-locks"):
        Settings(_env_file=None, live_trading_enabled=True)
