from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from trading_system.contracts.models import (
    EngineRegistry,
    QuestionCatalogCandidate,
    QuestionReviewQueue,
)


def repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def load_json(relative_path: str) -> dict[str, Any]:
    path = (repository_root() / relative_path).resolve()
    root = repository_root().resolve()
    if not path.is_relative_to(root):
        raise ValueError("contract path escapes repository root")
    with path.open(encoding="utf-8") as handle:
        value: object = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object in {relative_path}")
    return value


@lru_cache(maxsize=1)
def load_engine_registry() -> EngineRegistry:
    return EngineRegistry.model_validate(load_json("contracts/engine_registry.json"))


@lru_cache(maxsize=1)
def load_question_catalog_candidate() -> QuestionCatalogCandidate:
    return QuestionCatalogCandidate.model_validate(
        load_json("contracts/questions/question_catalog_candidate.json")
    )


@lru_cache(maxsize=1)
def load_question_review_queue() -> QuestionReviewQueue:
    return QuestionReviewQueue.model_validate(
        load_json("contracts/questions/first_wave_review_queue.json")
    )
