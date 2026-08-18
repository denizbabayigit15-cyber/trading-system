from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_PATH = ROOT / ".github/workflows/ci.yml"
PINNED_ACTION_PATTERN = re.compile(r"^[^@]+@[0-9a-f]{40}$")


def load_workflow() -> dict[str, Any]:
    value: object = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_ci_triggers_are_safe_and_permissions_are_read_only() -> None:
    workflow = load_workflow()
    triggers = workflow["on"]
    assert isinstance(triggers, dict)
    assert set(triggers) == {"push", "pull_request", "workflow_dispatch"}
    assert "pull_request_target" not in triggers
    assert workflow["permissions"] == {"contents": "read"}


def test_ci_actions_are_immutable_sha_pinned() -> None:
    workflow = load_workflow()
    steps = workflow["jobs"]["contract-quality"]["steps"]
    action_references = [step["uses"] for step in steps if "uses" in step]
    assert len(action_references) == 2
    assert all(PINNED_ACTION_PATTERN.fullmatch(reference) for reference in action_references)
    assert steps[0]["with"]["persist-credentials"] is False


def test_ci_executes_every_local_quality_gate_with_frozen_runs() -> None:
    workflow = load_workflow()
    steps = workflow["jobs"]["contract-quality"]["steps"]
    commands = [step["run"] for step in steps if "run" in step]

    assert "uv python install 3.14.7" in commands
    assert "uv sync --locked --all-groups" in commands
    assert "uv run --frozen python scripts/generate_question_catalog.py --check" in commands
    assert "uv run --frozen python scripts/verify_contracts.py" in commands
    assert "uv run --frozen pytest" in commands
    assert "uv run --frozen ruff check ." in commands
    assert "uv run --frozen ruff format --check ." in commands
    assert "uv run --frozen mypy src" in commands
