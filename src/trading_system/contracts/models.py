from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from trading_system.core.ids import new_id
from trading_system.core.time import require_utc, utc_now

QUESTION_BANK_SHA256 = "87fdc3e6de9a9e5b76fe470faa310ed57a9392cf7d5ecfd3f672149bc35a5544"
QUESTION_CATALOG_SHA256 = "7b78496dbf66f8f09ef6458635b5d8c6902a722d0bc38ff271ec988d522ea1c8"

type QuestionSourceLayer = Literal[
    "V2.2.5_BINDING_CORE",
    "V2.3.1_PROPOSED_EXTENSION",
]
type QuestionSourceStatus = Literal[
    "BINDING_CORE",
    "YENİ / ÖNERİLEN",
    "YENİ / KOŞULLU",
]
type ProposedQuestionSourceStatus = Literal["YENİ / ÖNERİLEN", "YENİ / KOŞULLU"]
type FirstWaveQuestionFamily = Literal["SV", "EP", "MI", "VC", "CY", "OR"]


class EngineRecord(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    engine_id: int = Field(ge=1, le=112)
    engine_name: str = Field(min_length=1)
    orchestrator: str = Field(min_length=1)
    source: Literal["V2.2.5_RETAINED", "V3.0.0_ADDED"]
    primary_output: str = Field(min_length=1)
    runtime_status: Literal["NOT_IMPLEMENTED"]


class EngineRegistry(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: Literal["1.0.0"]
    contract_version: Literal["3.0.0"]
    expected_count: Literal[112]
    engines: tuple[EngineRecord, ...]

    @model_validator(mode="after")
    def validate_complete_catalog(self) -> Self:
        ids = [engine.engine_id for engine in self.engines]
        if ids != list(range(1, 113)):
            raise ValueError("engine registry must contain ordered unique IDs 1..112")
        return self


class QuestionCatalogRecord(BaseModel):
    """A source-faithful question record without invented operational bindings."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    ordinal: int = Field(ge=1, le=900)
    question_id: str = Field(pattern=r"^[A-Z][A-Z0-9]*-[0-9]{3}$")
    question_version: Literal["UNBOUND"]
    source_layer: QuestionSourceLayer
    source_section: str = Field(min_length=1)
    source_line: int = Field(ge=1)
    question_text: str = Field(min_length=1)
    source_status: QuestionSourceStatus
    scope_hash: Literal["UNBOUND"]
    applicability: Literal["UNBOUND"]
    criticality: Literal["UNBOUND"]
    answer_status: Literal["UNKNOWN"]
    execution_status: Literal["NOT_EXECUTED"]
    information_class: Literal["UNKNOWN"]
    evidence_id: Literal["UNBOUND"]
    contract_id: Literal["UNBOUND"]
    policy_id: Literal["UNBOUND"]
    test_id: Literal["UNBOUND"]
    scenario_id: Literal["UNBOUND"]
    observation_window: Literal["UNBOUND"]
    fail_action: Literal["UNBOUND"]
    owner: Literal["UNBOUND"]
    approver: Literal["UNBOUND"]
    recertification_status: Literal["NOT_EXECUTED"]


class QuestionCatalogCandidate(BaseModel):
    """Non-authoritative extraction of the retained 900-question Markdown bank."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: Literal["1.0.0"]
    contract_version: Literal["3.0.0"]
    catalog_version: Literal["0.1.0"]
    authority_status: Literal["NON_AUTHORITATIVE_CANDIDATE"]
    source_document: Literal[
        "docs/baseline/TRADING_SYSTEM_V3_0_0_PRECODE_QUESTION_BANK_ADOPTION_CANDIDATE.md"
    ]
    source_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    authoritative_registry_path: Literal["contracts/questions/question_registry.json"]
    authoritative_registry_materialized: Literal[False]
    expected_count: Literal[900]
    binding_core_count: Literal[237]
    proposed_extension_count: Literal[663]
    runtime_pass_count: Literal[0]
    unbound_count: Literal[900]
    live_authorized: Literal[False]
    questions: tuple[QuestionCatalogRecord, ...]

    @model_validator(mode="after")
    def validate_complete_candidate(self) -> Self:
        if self.source_sha256 != QUESTION_BANK_SHA256:
            raise ValueError("question-bank source hash is not the reviewed baseline hash")
        if len(self.questions) != self.expected_count:
            raise ValueError("question catalog must contain exactly 900 records")

        ordinals = [record.ordinal for record in self.questions]
        if ordinals != list(range(1, 901)):
            raise ValueError("question catalog must contain ordered ordinals 1..900")

        question_ids = [record.question_id for record in self.questions]
        if len(question_ids) != len(set(question_ids)):
            raise ValueError("question IDs must be unique")

        source_lines = [record.source_line for record in self.questions]
        if source_lines != sorted(source_lines) or len(source_lines) != len(set(source_lines)):
            raise ValueError("question source lines must be strictly increasing")

        core = self.questions[: self.binding_core_count]
        proposed = self.questions[self.binding_core_count :]
        if any(record.source_layer != "V2.2.5_BINDING_CORE" for record in core):
            raise ValueError("the first 237 records must be the retained binding core")
        if any(record.source_status != "BINDING_CORE" for record in core):
            raise ValueError("binding-core source status is inconsistent")
        if any(record.source_layer != "V2.3.1_PROPOSED_EXTENSION" for record in proposed):
            raise ValueError("the final 663 records must be proposed extensions")

        proposed_statuses = [record.source_status for record in proposed]
        if proposed_statuses.count("YENİ / ÖNERİLEN") != 596:
            raise ValueError("expected 596 proposed extension records")
        if proposed_statuses.count("YENİ / KOŞULLU") != 67:
            raise ValueError("expected 67 conditional extension records")
        return self


class QuestionReviewQueueItem(BaseModel):
    """A first-wave question awaiting explicit human and change-control review."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    review_ordinal: int = Field(ge=1, le=150)
    catalog_ordinal: int = Field(ge=688, le=837)
    question_id: str = Field(pattern=r"^(SV|EP|MI|VC|CY|OR)-[0-9]{3}$")
    family: FirstWaveQuestionFamily
    question_version: Literal["UNBOUND"]
    source_section: str = Field(min_length=1)
    question_text: str = Field(min_length=1)
    source_status: ProposedQuestionSourceStatus
    review_status: Literal["REVIEW_REQUIRED"]
    applicability: Literal["UNBOUND"]
    criticality: Literal["UNBOUND"]
    scope_hash: Literal["UNBOUND"]
    information_class: Literal["UNKNOWN"]
    answer_status: Literal["UNKNOWN"]
    execution_status: Literal["NOT_EXECUTED"]
    contract_id: Literal["UNBOUND"]
    policy_id: Literal["UNBOUND"]
    test_id: Literal["UNBOUND"]
    scenario_id: Literal["UNBOUND"]
    evidence_id: Literal["UNBOUND"]
    observation_window: Literal["UNBOUND"]
    fail_action: Literal["UNBOUND"]
    owner: Literal["UNBOUND"]
    approver: Literal["UNBOUND"]
    independent_approval_status: Literal["NOT_EXECUTED"]
    decision_record_id: Literal["UNBOUND"]
    recertification_status: Literal["NOT_EXECUTED"]


class QuestionReviewQueue(BaseModel):
    """Fail-closed review queue for the baseline-designated first wave."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: Literal["1.0.0"]
    contract_version: Literal["3.0.0"]
    queue_version: Literal["0.1.0"]
    queue_id: Literal["W0-FIRST-WAVE-QUESTION-REVIEW"]
    authority_status: Literal["NON_AUTHORITATIVE_REVIEW_QUEUE"]
    source_catalog_path: Literal["contracts/questions/question_catalog_candidate.json"]
    source_catalog_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    family_order: tuple[FirstWaveQuestionFamily, ...]
    expected_count: Literal[150]
    review_required_count: Literal[150]
    approved_count: Literal[0]
    adopted_count: Literal[0]
    runtime_pass_count: Literal[0]
    live_authorized: Literal[False]
    items: tuple[QuestionReviewQueueItem, ...]

    @model_validator(mode="after")
    def validate_complete_review_queue(self) -> Self:
        expected_families: tuple[FirstWaveQuestionFamily, ...] = (
            "SV",
            "EP",
            "MI",
            "VC",
            "CY",
            "OR",
        )
        if self.source_catalog_sha256 != QUESTION_CATALOG_SHA256:
            raise ValueError("review queue source catalog hash is not the reviewed catalog hash")
        if self.family_order != expected_families:
            raise ValueError("first-wave family order must be SV, EP, MI, VC, CY, OR")
        if len(self.items) != self.expected_count:
            raise ValueError("first-wave review queue must contain exactly 150 items")

        review_ordinals = [item.review_ordinal for item in self.items]
        if review_ordinals != list(range(1, 151)):
            raise ValueError("review queue must contain ordered ordinals 1..150")

        catalog_ordinals = [item.catalog_ordinal for item in self.items]
        if catalog_ordinals != list(range(688, 838)):
            raise ValueError("review queue must preserve source catalog ordinals 688..837")

        expected_ids = [
            f"{family}-{number:03d}" for family in expected_families for number in range(1, 26)
        ]
        actual_ids = [item.question_id for item in self.items]
        if actual_ids != expected_ids:
            raise ValueError("review queue must contain ordered IDs 001..025 for each family")
        if any(item.family != item.question_id.split("-", maxsplit=1)[0] for item in self.items):
            raise ValueError("question family must match its question ID")

        statuses = [item.source_status for item in self.items]
        if statuses.count("YENİ / ÖNERİLEN") != 132:
            raise ValueError("expected 132 proposed first-wave questions")
        if statuses.count("YENİ / KOŞULLU") != 18:
            raise ValueError("expected 18 conditional first-wave questions")
        return self


def _payload_hash(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


class EventEnvelope(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    event_id: str = Field(default_factory=lambda: new_id("evt"), pattern=r"^evt_[0-9a-f]{32}$")
    event_type: str = Field(pattern=r"^[a-z0-9_]+\.[a-z0-9_]+\.(succeeded|failed)\.v[0-9]+$")
    event_version: int = Field(default=1, ge=1)
    schema_version: str = Field(default="1.0.0", pattern=r"^[0-9]+\.[0-9]+\.[0-9]+$")
    occurred_at: datetime
    produced_at: datetime = Field(default_factory=utc_now)
    producer: str = Field(min_length=1)
    correlation_id: str = Field(min_length=1)
    causation_id: str | None = None
    decision_id: str | None = None
    lineage_id: str | None = None
    scope_hash: str | None = None
    payload: dict[str, Any]
    payload_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")

    @field_validator("occurred_at", "produced_at")
    @classmethod
    def timestamps_must_be_utc(cls, value: datetime) -> datetime:
        return require_utc(value)

    @model_validator(mode="after")
    def bind_payload_hash(self) -> Self:
        expected = _payload_hash(self.payload)
        if self.payload_sha256 is not None and self.payload_sha256 != expected:
            raise ValueError("payload_sha256 does not match canonical payload")
        object.__setattr__(self, "payload_sha256", expected)
        return self
