from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Literal, cast

from trading_system.contracts.models import (
    QuestionCatalogCandidate,
    QuestionCatalogRecord,
    QuestionSourceLayer,
    QuestionSourceStatus,
)

SOURCE_DOCUMENT: Literal[
    "docs/baseline/TRADING_SYSTEM_V3_0_0_PRECODE_QUESTION_BANK_ADOPTION_CANDIDATE.md"
] = "docs/baseline/TRADING_SYSTEM_V3_0_0_PRECODE_QUESTION_BANK_ADOPTION_CANDIDATE.md"
TARGET_DOCUMENT = "contracts/questions/question_catalog_candidate.json"

_HEADING_PATTERN = re.compile(r"^#{3,4}\s+(?P<section>.+?)\s*$")
_CORE_PATTERN = re.compile(
    r"^(?P<ordinal>[0-9]+)\.\s+`(?P<question_id>[A-Z][A-Z0-9]*-[0-9]{3})`\s+"
    r"(?P<question_text>.+?)\s*$"
)
_TABLE_PATTERN = re.compile(
    r"^\|\s*`?(?P<question_id>[A-Z][A-Z0-9]*-[0-9]{3})`?\s*\|\s*"
    r"(?P<question_text>.*?)\s*\|\s*(?P<source_status>.*?)\s*\|\s*$"
)
_PROPOSED_STATUSES = ("YENİ / ÖNERİLEN", "YENİ / KOŞULLU")


def _question_record(
    *,
    ordinal: int,
    question_id: str,
    question_text: str,
    source_section: str,
    source_line: int,
    source_status: QuestionSourceStatus,
) -> QuestionCatalogRecord:
    source_layer: QuestionSourceLayer = (
        "V2.2.5_BINDING_CORE" if source_status == "BINDING_CORE" else "V2.3.1_PROPOSED_EXTENSION"
    )
    return QuestionCatalogRecord(
        ordinal=ordinal,
        question_id=question_id,
        question_version="UNBOUND",
        source_layer=source_layer,
        source_section=source_section,
        source_line=source_line,
        question_text=question_text,
        source_status=source_status,
        scope_hash="UNBOUND",
        applicability="UNBOUND",
        criticality="UNBOUND",
        answer_status="UNKNOWN",
        execution_status="NOT_EXECUTED",
        information_class="UNKNOWN",
        evidence_id="UNBOUND",
        contract_id="UNBOUND",
        policy_id="UNBOUND",
        test_id="UNBOUND",
        scenario_id="UNBOUND",
        observation_window="UNBOUND",
        fail_action="UNBOUND",
        owner="UNBOUND",
        approver="UNBOUND",
        recertification_status="NOT_EXECUTED",
    )


def parse_question_bank(source_text: str) -> tuple[QuestionCatalogRecord, ...]:
    """Extract question text and source metadata without semantic inference."""

    records: list[QuestionCatalogRecord] = []
    current_section: str | None = None

    for source_line, line in enumerate(source_text.splitlines(), start=1):
        heading_match = _HEADING_PATTERN.match(line)
        if heading_match is not None:
            current_section = heading_match.group("section")
            continue

        core_match = _CORE_PATTERN.match(line)
        if core_match is not None:
            if current_section is None:
                raise ValueError(f"question at line {source_line} has no source section")
            source_ordinal = int(core_match.group("ordinal"))
            expected_ordinal = len(records) + 1
            if source_ordinal != expected_ordinal:
                raise ValueError(
                    f"binding-core ordinal mismatch at line {source_line}: "
                    f"expected {expected_ordinal}, got {source_ordinal}"
                )
            records.append(
                _question_record(
                    ordinal=source_ordinal,
                    question_id=core_match.group("question_id"),
                    question_text=core_match.group("question_text"),
                    source_section=current_section,
                    source_line=source_line,
                    source_status="BINDING_CORE",
                )
            )
            continue

        table_match = _TABLE_PATTERN.match(line)
        if table_match is None:
            continue
        if current_section is None:
            raise ValueError(f"question at line {source_line} has no source section")

        raw_status = table_match.group("source_status")
        if raw_status not in _PROPOSED_STATUSES:
            raise ValueError(f"unsupported source status at line {source_line}: {raw_status!r}")
        records.append(
            _question_record(
                ordinal=len(records) + 1,
                question_id=table_match.group("question_id"),
                question_text=table_match.group("question_text"),
                source_section=current_section,
                source_line=source_line,
                source_status=cast(QuestionSourceStatus, raw_status),
            )
        )

    return tuple(records)


def build_question_catalog(source_path: Path) -> QuestionCatalogCandidate:
    source_bytes = source_path.read_bytes()
    source_text = source_bytes.decode("utf-8")
    return QuestionCatalogCandidate(
        schema_version="1.0.0",
        contract_version="3.0.0",
        catalog_version="0.1.0",
        authority_status="NON_AUTHORITATIVE_CANDIDATE",
        source_document=SOURCE_DOCUMENT,
        source_sha256=hashlib.sha256(source_bytes).hexdigest(),
        authoritative_registry_path="contracts/questions/question_registry.json",
        authoritative_registry_materialized=False,
        expected_count=900,
        binding_core_count=237,
        proposed_extension_count=663,
        runtime_pass_count=0,
        unbound_count=900,
        live_authorized=False,
        questions=parse_question_bank(source_text),
    )


def render_question_catalog(catalog: QuestionCatalogCandidate) -> str:
    payload = catalog.model_dump(mode="json")
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
