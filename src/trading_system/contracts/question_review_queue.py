from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Literal, cast

from trading_system.contracts.models import (
    FirstWaveQuestionFamily,
    ProposedQuestionSourceStatus,
    QuestionCatalogCandidate,
    QuestionReviewQueue,
    QuestionReviewQueueItem,
)

SOURCE_CATALOG: Literal["contracts/questions/question_catalog_candidate.json"] = (
    "contracts/questions/question_catalog_candidate.json"
)
TARGET_QUEUE = "contracts/questions/first_wave_review_queue.json"
FIRST_WAVE_FAMILIES: tuple[FirstWaveQuestionFamily, ...] = (
    "SV",
    "EP",
    "MI",
    "VC",
    "CY",
    "OR",
)


def build_question_review_queue(
    catalog: QuestionCatalogCandidate,
    *,
    source_catalog_sha256: str,
) -> QuestionReviewQueue:
    selected = [
        question
        for question in catalog.questions
        if question.question_id.split("-", maxsplit=1)[0] in FIRST_WAVE_FAMILIES
    ]
    items = tuple(
        QuestionReviewQueueItem(
            review_ordinal=review_ordinal,
            catalog_ordinal=question.ordinal,
            question_id=question.question_id,
            family=cast(
                FirstWaveQuestionFamily,
                question.question_id.split("-", maxsplit=1)[0],
            ),
            question_version="UNBOUND",
            source_section=question.source_section,
            question_text=question.question_text,
            source_status=cast(ProposedQuestionSourceStatus, question.source_status),
            review_status="REVIEW_REQUIRED",
            applicability="UNBOUND",
            criticality="UNBOUND",
            scope_hash="UNBOUND",
            information_class="UNKNOWN",
            answer_status="UNKNOWN",
            execution_status="NOT_EXECUTED",
            contract_id="UNBOUND",
            policy_id="UNBOUND",
            test_id="UNBOUND",
            scenario_id="UNBOUND",
            evidence_id="UNBOUND",
            observation_window="UNBOUND",
            fail_action="UNBOUND",
            owner="UNBOUND",
            approver="UNBOUND",
            independent_approval_status="NOT_EXECUTED",
            decision_record_id="UNBOUND",
            recertification_status="NOT_EXECUTED",
        )
        for review_ordinal, question in enumerate(selected, start=1)
    )
    return QuestionReviewQueue(
        schema_version="1.0.0",
        contract_version="3.0.0",
        queue_version="0.1.0",
        queue_id="W0-FIRST-WAVE-QUESTION-REVIEW",
        authority_status="NON_AUTHORITATIVE_REVIEW_QUEUE",
        source_catalog_path=SOURCE_CATALOG,
        source_catalog_sha256=source_catalog_sha256,
        family_order=FIRST_WAVE_FAMILIES,
        expected_count=150,
        review_required_count=150,
        approved_count=0,
        adopted_count=0,
        runtime_pass_count=0,
        live_authorized=False,
        items=items,
    )


def build_question_review_queue_from_path(catalog_path: Path) -> QuestionReviewQueue:
    catalog_bytes = catalog_path.read_bytes()
    value: object = json.loads(catalog_bytes)
    catalog = QuestionCatalogCandidate.model_validate(value)
    return build_question_review_queue(
        catalog,
        source_catalog_sha256=hashlib.sha256(catalog_bytes).hexdigest(),
    )


def render_question_review_queue(queue: QuestionReviewQueue) -> str:
    return json.dumps(queue.model_dump(mode="json"), indent=2, ensure_ascii=False) + "\n"
