# Local development runbook

## Prerequisites

- Windows 11 + WSL 2
- Ubuntu 24.04
- VS Code WSL extension
- Docker Desktop with Ubuntu-24.04 integration
- uv 0.12.5
- Python 3.14.7 managed by uv

## Bootstrap

Run from the repository root in the WSL terminal:

```bash
uv sync --all-groups
uv run python scripts/generate_local_env.py
docker compose up -d
docker compose ps
uv run alembic upgrade head
uv run python scripts/verify_environment.py
uv run python scripts/verify_contracts.py
uv run pytest
```

## pgAdmin connection

Open <http://127.0.0.1:5050> and use the email/password generated in `.env`.
Register a server with:

| Field | Value |
|---|---|
| Name | Trading System Local |
| Host | `postgres` |
| Port | `5432` |
| Maintenance DB | Value of `POSTGRES_DB` in `.env` |
| Username | Value of `POSTGRES_USER` in `.env` |
| Password | Value of `POSTGRES_PASSWORD` in `.env` |

Never send or commit `.env`.

## Stop and start

```bash
docker compose stop
docker compose start
```

To remove containers while retaining database volumes:

```bash
docker compose down
```

Do not use `docker compose down -v` unless the local database is intentionally
being destroyed and a recovery plan exists.

## Schema changes

Only Alembic migrations may modify the schema:

```bash
uv run alembic revision -m "change description"
uv run alembic upgrade head
```

Do not use pgAdmin to make persistent schema changes.

