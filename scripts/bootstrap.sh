#!/usr/bin/env bash
set -euo pipefail

uv sync --all-groups

if [[ ! -f .env ]]; then
  uv run python scripts/generate_local_env.py
fi

docker compose up -d
uv run alembic upgrade head
uv run python scripts/verify_environment.py
uv run python scripts/verify_contracts.py
uv run pytest

echo "Foundation bootstrap complete. LIVE_AUTHORIZED remains false."

