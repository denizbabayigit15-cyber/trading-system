from __future__ import annotations

from fastapi.testclient import TestClient

from trading_system.api import app
from trading_system.health import service as health_service
from trading_system.settings import Settings


def test_liveness_never_implies_trading_authority() -> None:
    response = TestClient(app).get("/health/live")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ALIVE",
        "database": "NOT_CHECKED",
        "live_authorized": False,
        "reason_code": "AUTH_LIVE_DISABLED",
    }


def test_readiness_is_degraded_when_database_secret_is_unbound(monkeypatch) -> None:
    monkeypatch.setattr(
        health_service,
        "get_settings",
        lambda: Settings(_env_file=None),
    )
    response = TestClient(app).get("/health/ready")
    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "DEGRADED"
    assert body["database"] == "UNBOUND"
    assert body["live_authorized"] is False
