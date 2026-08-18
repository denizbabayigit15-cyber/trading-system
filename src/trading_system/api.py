from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from trading_system import __version__
from trading_system.health.service import HealthReport, liveness, readiness

app = FastAPI(
    title="Trading System Foundation API",
    version=__version__,
    description="Fail-closed W0/W1 scaffold. No trading endpoint exists.",
)


@app.get("/", response_model=dict[str, str | bool])
def root() -> dict[str, str | bool]:
    return {
        "service": "trading-system-foundation",
        "version": __version__,
        "live_authorized": False,
    }


@app.get("/health/live", response_model=HealthReport)
def health_live() -> HealthReport:
    return liveness()


@app.get("/health/ready", response_model=HealthReport)
def health_ready() -> HealthReport | JSONResponse:
    report = readiness()
    if report.status != "READY":
        return JSONResponse(status_code=503, content=report.model_dump(mode="json"))
    return report
