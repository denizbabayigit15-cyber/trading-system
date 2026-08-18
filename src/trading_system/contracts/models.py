from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from trading_system.core.ids import new_id
from trading_system.core.time import require_utc, utc_now

QUESTION_BANK_SHA256 = "87fdc3e6de9a9e5b76fe470faa310ed57a9392cf7d5ecfd3f672149bc35a5544"

type QuestionSourceLayer = Literal[
    "V2.2.5_BINDING_CORE",
    "V2.3.1_PROPOSED_EXTENSION",
]
type QuestionSourceStatus = Literal[
    "BINDING_CORE",
    "YENİ / ÖNERİLEN",
    "YENİ / KOŞULLU",
]


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
