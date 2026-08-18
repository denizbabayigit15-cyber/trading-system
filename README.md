# Trading System — W0/W1 Foundation Scaffold

This repository starts software construction under the V3.0.0 pre-code contract.
It is a **fail-closed development scaffold**, not a strategy, broker integration,
profitability claim, or live-trading release.

## Canonical status

| State | Value |
|---|---|
| Contract baseline | V3.0.0 review candidate |
| Implementation slice | W0 foundation + non-authoritative question catalog candidate |
| Python | 3.14.7 |
| PostgreSQL | 18.6 Bookworm |
| pgAdmin | 9.17 |
| Engine catalog | 112 entries; all `NOT_IMPLEMENTED` |
| Question catalog | 900 source-faithful candidates; all `UNKNOWN / NOT_EXECUTED` |
| First-wave review | 150 queued; all `REVIEW_REQUIRED / UNBOUND` |
| Pull-request gates | GitHub CI: contracts, tests, Ruff, formatting, and Mypy |
| Runtime tests | Only scaffold tests included |
| R1 code-ready | `FALSE` |
| Live authorized | `FALSE` and database-constrained |

## First local start

```bash
uv sync --all-groups
uv run python scripts/generate_local_env.py
uv run python scripts/generate_question_catalog.py --check
uv run python scripts/generate_question_review_queue.py --check
docker compose up -d
uv run alembic upgrade head
uv run python scripts/verify_contracts.py
uv run pytest
uv run uvicorn trading_system.api:app --reload
```

Open:

- API health: <http://127.0.0.1:8000/health/live>
- API readiness: <http://127.0.0.1:8000/health/ready>
- pgAdmin: <http://127.0.0.1:5050>

The pgAdmin PostgreSQL host is `postgres` when connecting from pgAdmin. From
the WSL host, the PostgreSQL host is `127.0.0.1`.

## Non-negotiable boundaries

- Financial truth uses `Decimal`; floats are rejected at the canonical boundary.
- Unknown, stale, missing, or mismatched authority inputs deny new risk.
- No strategy is active.
- No external broker, venue, account, capital, fee, threshold, or legal value is invented.
- pgAdmin is inspection tooling; Alembic is the only schema authority.
- Direct database edits may not create trading authority.
- Every future implementation slice follows `CONTRACT → CODE → TEST → RUN → EVIDENCE → AUDIT → ACCEPT → NEXT`.

## Important documentation

- `docs/STATUS.md` — honest implementation status.
- `docs/baseline/` — retained V3.0.0 source documents.
- `docs/runbooks/LOCAL_DEVELOPMENT.md` — detailed local operation.
- `contracts/engine_registry.json` — the 112-engine catalog, not implementation evidence.
- `contracts/questions/question_catalog_candidate.json` — deterministic 900-question extraction.
- `contracts/questions/first_wave_review_queue.json` — fail-closed 150-item review queue.
- `contracts/questions/README.md` — explicit blocker for the missing authoritative mappings.

## Developer completion statement

> I implemented only approved behavior, preserved UNBOUND external inputs, did
> not activate a strategy, did not claim runtime PASS without evidence, and did
> not grant live authority.
