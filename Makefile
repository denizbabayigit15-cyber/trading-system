.PHONY: sync env catalog review-queue infra-up infra-down db-upgrade verify test lint format api status

sync:
	uv sync --all-groups

env:
	uv run python scripts/generate_local_env.py

catalog:
	uv run python scripts/generate_question_catalog.py

review-queue:
	uv run python scripts/generate_question_review_queue.py

infra-up:
	docker compose up -d

infra-down:
	docker compose down

db-upgrade:
	uv run alembic upgrade head

verify:
	uv run python scripts/verify_environment.py
	uv run python scripts/generate_question_catalog.py --check
	uv run python scripts/generate_question_review_queue.py --check
	uv run python scripts/verify_contracts.py

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run mypy src

format:
	uv run ruff format .

api:
	uv run uvicorn trading_system.api:app --reload

status:
	docker compose ps
