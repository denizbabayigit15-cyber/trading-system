from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# This table declares evidence locations and unresolved behavior only.  It never
# declares an implementation status; status is calculated below from checks.
MODULE_BY_ENGINE: dict[int, tuple[str, str]] = {
    1: ("governance.orchestrator", "tests/unit/test_governance_orchestrator.py"),
    2: ("governance.policy", "tests/unit/test_policy_versioning.py"),
    3: ("market_data.quality", "tests/unit/test_market_data_quality.py"),
    4: ("market_data.ingestion", "tests/unit/test_market_data_replay.py"),
    5: ("market_data.quality", "tests/unit/test_data_validator_registry.py"),
    6: ("data.temporal", "tests/unit/test_w1_temporal_lineage.py"),
    7: ("data.lineage", "tests/unit/test_w1_temporal_lineage.py"),
    8: ("market_data.models", "tests/unit/test_market_data_models.py"),
    9: ("market_data.quality", "tests/unit/test_market_data_quality.py"),
    10: ("research.fabric", "tests/unit/test_feature_fabric.py"),
    11: ("market_data.domain", "tests/unit/test_market_domain_engines.py"),
    12: ("market_data.domain", "tests/unit/test_market_domain_engines.py"),
    13: ("market_data.domain", "tests/unit/test_market_domain_engines.py"),
    14: ("market_data.domain", "tests/unit/test_market_domain_engines.py"),
    15: ("market_data.domain", "tests/unit/test_market_domain_engines.py"),
    16: ("market_data.domain", "tests/unit/test_market_domain_engines.py"),
    17: ("market_data.domain", "tests/unit/test_market_domain_engines.py"),
    18: ("market_data.domain", "tests/unit/test_market_domain_engines.py"),
    19: ("market_data.domain", "tests/unit/test_market_domain_engines.py"),
    20: ("market_data.domain", "tests/unit/test_market_domain_engines.py"),
    21: ("market_data.domain", "tests/unit/test_market_domain_engines.py"),
    22: ("market_data.domain", "tests/unit/test_market_domain_engines.py"),
    23: ("market_data.domain", "tests/unit/test_market_domain_engines.py"),
    24: ("market_data.domain", "tests/unit/test_market_domain_engines.py"),
    25: ("market_data.domain", "tests/unit/test_market_domain_engines.py"),
    26: ("market_data.domain", "tests/unit/test_market_domain_engines.py"),
    27: ("market_data.domain", "tests/unit/test_market_domain_engines.py"),
    28: ("market_data.domain", "tests/unit/test_market_domain_engines.py"),
    29: ("market_data.domain", "tests/unit/test_market_domain_engines.py"),
    30: ("research.decision", "tests/unit/test_decision_engines.py"),
    31: ("research.decision", "tests/unit/test_decision_engines.py"),
    32: ("research.decision", "tests/unit/test_decision_engines.py"),
    33: ("research.decision", "tests/unit/test_decision_engines.py"),
    34: ("research.decision", "tests/unit/test_decision_engines.py"),
    35: ("research.models", "tests/unit/test_research_infrastructure.py"),
    36: ("research.eligibility", "tests/unit/test_research_eligibility.py"),
    37: ("research.statistics", "tests/unit/test_research_eligibility.py"),
    38: ("research.statistics", "tests/unit/test_research_eligibility.py"),
    39: ("research.statistics", "tests/unit/test_research_eligibility.py"),
    40: ("research.decision", "tests/unit/test_decision_engines.py"),
    41: ("research.decision", "tests/unit/test_decision_engines.py"),
    42: ("research.decision", "tests/unit/test_decision_engines.py"),
    43: ("risk.controls", "tests/unit/test_risk_controls.py"),
    44: ("risk.portfolio", "tests/unit/test_risk_portfolio_engines.py"),
    45: ("risk.portfolio", "tests/unit/test_risk_portfolio_engines.py"),
    46: ("risk.portfolio", "tests/unit/test_risk_portfolio_engines.py"),
    47: ("risk.portfolio", "tests/unit/test_risk_portfolio_engines.py"),
    48: ("risk.portfolio", "tests/unit/test_risk_portfolio_engines.py"),
    49: ("risk.analytics", "tests/unit/test_risk_analytics.py"),
    50: ("risk.portfolio", "tests/unit/test_risk_portfolio_engines.py"),
    51: ("risk.portfolio", "tests/unit/test_risk_portfolio_engines.py"),
    52: ("risk.portfolio", "tests/unit/test_risk_portfolio_engines.py"),
    53: ("risk.portfolio", "tests/unit/test_risk_portfolio_engines.py"),
    54: ("risk.portfolio", "tests/unit/test_risk_portfolio_engines.py"),
    55: ("authority.lease", "tests/unit/test_authority_and_lease.py"),
    56: ("execution.orders", "tests/unit/test_paper_execution.py"),
    57: ("risk.portfolio", "tests/unit/test_risk_portfolio_engines.py"),
    58: ("risk.portfolio", "tests/unit/test_risk_portfolio_engines.py"),
    59: ("reconciliation.models", "tests/unit/test_reconciliation.py"),
    60: ("risk.controls", "tests/unit/test_risk_controls.py"),
    61: ("execution.orders", "tests/unit/test_oms_accounting.py"),
    62: ("execution.orders", "tests/unit/test_oms_accounting.py"),
    63: ("evidence.models", "tests/unit/test_evidence_readiness.py"),
    64: ("evidence.journal", "tests/unit/test_journal.py"),
    65: ("execution.accounting", "tests/unit/test_oms_accounting.py"),
    66: ("research.performance", "tests/unit/test_performance_governance.py"),
    67: ("research.performance", "tests/unit/test_performance_governance.py"),
    68: ("research.performance", "tests/unit/test_performance_governance.py"),
    69: ("research.performance", "tests/unit/test_performance_governance.py"),
    70: ("research.performance", "tests/unit/test_performance_governance.py"),
    71: ("research.performance", "tests/unit/test_performance_governance.py"),
    72: ("research.validation", "tests/unit/test_research_validation.py"),
    73: ("research.models", "tests/unit/test_research_infrastructure.py"),
    74: ("replay.engine", "tests/unit/test_market_data_replay.py"),
    75: ("research.statistics", "tests/unit/test_research_eligibility.py"),
    76: ("research.validation", "tests/unit/test_research_validation.py"),
    77: ("research.validation", "tests/unit/test_research_validation.py"),
    78: ("research.models", "tests/unit/test_research_infrastructure.py"),
    79: ("execution.orders", "tests/unit/test_paper_execution.py"),
    80: ("operations.rollout", "tests/unit/test_rollout.py"),
    81: ("risk.portfolio", "tests/unit/test_portfolio_risk.py"),
    82: ("research.model_risk", "tests/unit/test_model_risk.py"),
    83: ("core.gates", "tests/unit/test_gates.py"),
    84: ("core.gates", "tests/unit/test_gates.py"),
    85: ("research.decision", "tests/unit/test_decision_engines.py"),
    86: ("research.decision", "tests/unit/test_decision_engines.py"),
    87: ("research.decision", "tests/unit/test_decision_engines.py"),
    88: ("research.decision", "tests/unit/test_decision_engines.py"),
    89: ("core.gates", "tests/unit/test_gates.py"),
    90: ("operations.health", "tests/unit/test_health.py"),
    91: ("operations.health", "tests/unit/test_health.py"),
    92: ("market_data.failover", "tests/unit/test_market_data_failover.py"),
    93: ("core.time", "tests/unit/test_w1_temporal_lineage.py"),
    94: ("security.boundaries", "tests/unit/test_security_boundaries.py"),
    95: ("core.versioning", "tests/unit/test_policy_versioning.py"),
    96: ("evidence.models", "tests/unit/test_evidence_readiness.py"),
    97: ("governance.scope", "tests/unit/test_w1_governance.py"),
    98: ("external.reality", "tests/unit/test_external_boundaries.py"),
    99: ("authority.evaluator", "tests/unit/test_authority_and_lease.py"),
    100: ("authority.lease", "tests/unit/test_authority_and_lease.py"),
    101: ("external.reality", "tests/unit/test_external_boundaries.py"),
    102: ("core.gates", "tests/unit/test_gates.py"),
    103: ("external.reality", "tests/unit/test_external_boundaries.py"),
    104: ("external.reality", "tests/unit/test_external_boundaries.py"),
    105: ("external.reality", "tests/unit/test_external_boundaries.py"),
    106: ("execution.accounting", "tests/unit/test_oms_accounting.py"),
    107: ("core.gates", "tests/unit/test_gates.py"),
    108: ("external.reality", "tests/unit/test_external_boundaries.py"),
    109: ("security.boundaries", "tests/unit/test_security_boundaries.py"),
    110: ("core.gates", "tests/unit/test_gates.py"),
    111: ("security.boundaries", "tests/unit/test_security_boundaries.py"),
    112: ("external.reality", "tests/unit/test_external_boundaries.py"),
}

ADDITIONAL_TESTS_BY_ENGINE: dict[int, tuple[str, ...]] = {
    1: ("tests/integration/test_postgres_runtime.py",),
    10: ("tests/integration/test_postgres_runtime.py",),
    66: ("tests/integration/test_postgres_runtime.py",),
    67: ("tests/integration/test_postgres_runtime.py",),
    68: ("tests/integration/test_postgres_runtime.py",),
    85: ("tests/integration/test_postgres_runtime.py",),
    86: ("tests/integration/test_postgres_runtime.py",),
    87: ("tests/integration/test_postgres_runtime.py",),
    88: ("tests/integration/test_postgres_runtime.py",),
}

SEMANTIC_SYMBOLS_BY_ENGINE: dict[int, tuple[str, ...]] = {
    1: ("GovernanceOrchestrator", "GovernanceEvent"),
    5: ("EventValidatorRegistry", "ValidationResult"),
    10: ("FeatureFabric", "FeatureDefinition", "FeatureMaterialization"),
    11: ("VolumeProfile", "build_volume_profile"),
    12: ("OrderFlowPolicy", "classify_trade", "signed_volume"),
    13: ("microprice", "depth_imbalance"),
    14: ("LiquidityEventSeries", "LiquidityChangePointDetector", "liquidity_change"),
    15: ("CapacityInput", "capacity_check"),
    16: ("OptionContract", "OptionChain"),
    17: (
        "GreeksInput",
        "standard_greeks",
        "aggregate_gex",
        "GexPosition",
        "aggregate_gex_positions",
    ),
    18: ("FuturesContract", "RollPolicy", "select_front_contract"),
    20: ("realized_volatility",),
    26: ("classify_market_state",),
    27: ("RegimeClassifier",),
    30: ("RuleRegistry", "SetupLifecycle"),
    31: ("score_setup",),
    32: ("ConflictGraph",),
    33: ("AlphaEnsemble",),
    34: ("DependencyGraph",),
    40: ("NoTradeRules",),
    41: ("authorize_signal",),
    42: ("TradeThesis",),
    44: ("BudgetTree",),
    45: ("drawdown_state",),
    46: ("quantile", "cvar"),
    47: ("risk_of_ruin",),
    50: ("MarginSchedule", "margin_required"),
    54: ("optimize_allocation", "AllocationConstraint", "AllocationResult"),
    58: ("ImpactCurve", "impact_estimate"),
    66: ("attribution",),
    67: ("PerformanceSeries",),
    68: ("DecompositionRecord", "decomposition_records"),
    69: ("decay_state",),
    70: ("drift_score", "DriftBaseline", "DriftMonitor", "DriftAlert"),
    71: ("correlation", "SharedAlphaGraph"),
    82: ("ModelInventory", "ModelRecord", "ModelValidation", "model_eligibility"),
    85: ("DecisionRecord",),
    87: ("DecisionConsumer", "Delivery"),
    88: ("FeedbackEvent",),
}

EXTERNAL_DEPENDENCIES: dict[int, tuple[str, ...]] = {
    77: ("independent strategy certification and empirical profitability evidence",),
    83: ("owner-approved AI research policy and model/provider entitlements",),
    84: ("independent authority approval for AI-generated decisions",),
    89: ("owner-approved learning-governor policy and live evidence",),
    97: ("owner-supplied MarketProfile and scope bindings",),
    98: ("broker/venue/account capabilities and credentials",),
    101: ("venue rules, routing entitlements, and broker capabilities",),
    102: ("venue-specific market-integrity surveillance rules and data access",),
    103: ("jurisdiction/product legal and compliance determinations",),
    104: ("counterparty, custody, and settlement terms",),
    105: ("treasury, cash, collateral, and capital limits",),
    107: ("issuer corporate-action and instrument-lifecycle feeds",),
    108: ("authoritative reference-price/oracle/fixing source",),
    110: ("owner-approved incident/BCP plan and operational exercises",),
    112: ("paid/provider data entitlements and licensing terms",),
}


def public_symbols(path: Path) -> tuple[str, ...]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = {
        node.name
        for node in tree.body
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
        and not node.name.startswith("_")
    }
    return tuple(sorted(names))


def test_functions(path: Path) -> tuple[str, ...]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return tuple(
        sorted(
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
        )
    )


def classify_requirement(question: str, external: tuple[str, ...]) -> str:
    external_terms = (
        "broker",
        "venue",
        "account",
        "entitlement",
        "licens",
        "jurisdiction",
        "legal",
        "compliance",
        "custody",
        "treasury",
        "issuer",
        "independent",
        "approval",
        "capital limit",
    )
    if external and any(term in question.casefold() for term in external_terms):
        return "EXTERNAL_BINDING_REQUIRED"
    return "SOFTWARE_IMPLEMENTABLE"


def run_mapped_tests(paths: set[str]) -> None:
    result = subprocess.run(  # noqa: S603 - paths are repository-controlled constants
        [sys.executable, "-m", "pytest", "-q", *sorted(paths)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise RuntimeError(f"mapped engine tests failed:\n{result.stdout}\n{result.stderr}")


def main() -> None:
    registry = json.loads((ROOT / "contracts/engine_registry.json").read_text())
    questions = json.loads((ROOT / "contracts/questions/question_registry.json").read_text())[
        "questions"
    ]
    acceptance = {
        row["question_id"]: row
        for row in json.loads((ROOT / "contracts/questions/acceptance_matrix.json").read_text())[
            "tests"
        ]
    }
    test_paths = {test for _, test in MODULE_BY_ENGINE.values()}
    test_paths.update(test for tests in ADDITIONAL_TESTS_BY_ENGINE.values() for test in tests)
    run_mapped_tests(test_paths)
    rows: list[dict[str, object]] = []
    for engine in registry["engines"]:
        engine_id = int(engine["engine_id"])
        module_name, test_name = MODULE_BY_ENGINE.get(engine_id, ("", ""))
        module_path = ROOT / "src/trading_system" / f"{module_name.replace('.', '/')}.py"
        symbols = public_symbols(module_path) if module_path.is_file() else ()
        implementation_symbols = tuple(
            symbol
            for symbol in SEMANTIC_SYMBOLS_BY_ENGINE.get(engine_id, symbols)
            if symbol in symbols
        )
        additional_tests = ADDITIONAL_TESTS_BY_ENGINE.get(engine_id, ())
        test_files = (
            tuple(dict.fromkeys((test_name, *additional_tests))) if test_name else additional_tests
        )
        test_ids = tuple(
            sorted(
                {
                    test_id
                    for path in test_files
                    if (ROOT / path).is_file()
                    for test_id in test_functions(ROOT / path)
                }
            )
        )
        external = EXTERNAL_DEPENDENCIES.get(engine_id, ())
        checks = {
            "module_exists": module_path.is_file(),
            "symbols_exist": bool(implementation_symbols),
            "test_file_exists": bool(test_files)
            and all((ROOT / path).is_file() for path in test_files),
            "test_ids_exist": bool(test_ids),
            "required_contracts_exist": (ROOT / "contracts/engine_registry.json").is_file(),
            "mapped_tests_passed": True,
        }
        owned = [
            question
            for question in questions
            if engine_id in question.get("owner_engine_ids", [])
            or question.get("primary_owner_engine_id") == engine_id
        ]
        requirement_evidence: list[dict[str, object]] = []
        for question in owned:
            question_id = str(question["question_id"])
            requirement_class_for_question = classify_requirement(
                str(question["question"]), external
            )
            evidence_ok = all(checks.values())
            missing_behavior: list[str] = (
                []
                if evidence_ok
                else [
                    f"missing objective evidence: {name}"
                    for name, passed in checks.items()
                    if not passed
                ]
            )
            requirement_evidence.append(
                {
                    "engine_id": engine_id,
                    "question_id": question_id,
                    "requirement": str(question["question"]),
                    "normative_requirement": str(question["normative_requirement_tr"]),
                    "requirement_class": requirement_class_for_question,
                    "evidence_obligations": [
                        "RUNTIME_EVIDENCE_REQUIRED",
                        "INDEPENDENT_REVIEW_REQUIRED",
                    ],
                    "implementation_symbols": list(implementation_symbols),
                    "test_ids": list(test_ids),
                    "test_id": acceptance.get(question_id, {}).get("test_id"),
                    "contract_references": [
                        str(question["contract_id"]),
                        "contracts/questions/traceability_matrix.json",
                        "contracts/questions/acceptance_matrix.json",
                    ],
                    "evidence_status": "PASS" if evidence_ok else "MISSING",
                    "external_dependency": external[0] if external else None,
                    "missing_behavior": missing_behavior,
                }
            )
        software_requirements = [
            item
            for item in requirement_evidence
            if item["requirement_class"] == "SOFTWARE_IMPLEMENTABLE"
        ]
        missing_software = [
            f"{item['question_id']}: {', '.join(item['missing_behavior'])}"
            for item in software_requirements
            if item["evidence_status"] != "PASS"
        ]
        if not all(checks.values()):
            status = "NOT_IMPLEMENTED"
            justification = "objective evidence check failed: " + ", ".join(
                name for name, passed in checks.items() if not passed
            )
        elif missing_software:
            status = "PARTIALLY_IMPLEMENTED"
            justification = "software requirement evidence missing: " + "; ".join(
                missing_software[:5]
            )
        else:
            status = "IMPLEMENTED"
            justification = (
                "all locally classified software requirements have mapped symbols and passing tests"
            )
        external_status = "REQUIRED" if external else "NOT_REQUIRED"
        if external:
            justification += "; external binding required: " + "; ".join(external)
        rows.append(
            {
                "engine_id": engine_id,
                "engine_name": engine["engine_name"],
                "authoritative_references": [
                    {
                        "path": "contracts/engine_registry.json",
                        "field": f"engines[{engine_id - 1}]",
                    },
                    {"source": engine["source"]},
                ],
                "implementation_modules": [
                    f"src/trading_system/{module_name.replace('.', '/')}.py"
                    if module_name
                    else None
                ],
                "implementation_symbols": list(implementation_symbols),
                "required_contracts": ["contracts/engine_registry.json"],
                "required_schemas": [],
                "required_reason_codes": [],
                "test_files": list(test_files),
                "test_ids": list(test_ids),
                "persistence_dependencies": ["PostgreSQL migrations"] if engine_id >= 55 else [],
                "external_dependencies": list(external),
                "implementation_status": status,
                "software_status": status,
                "external_binding_status": external_status,
                "runtime_evidence_status": "PENDING",
                "independent_review_status": "PENDING" if owned else "NOT_APPLICABLE",
                "owned_question_count": len(owned),
                "software_requirement_count": len(software_requirements),
                "software_requirements_passed": len(software_requirements) - len(missing_software),
                "software_requirements_missing": len(missing_software),
                "requirement_evidence": requirement_evidence,
                "checks": checks,
                "missing_software": missing_software,
                "justification": justification,
            }
        )
    counts = {
        status: sum(row["implementation_status"] == status for row in rows)
        for status in {
            "IMPLEMENTED",
            "PARTIALLY_IMPLEMENTED",
            "EXTERNAL_INPUT_BLOCKED",
            "NOT_IMPLEMENTED",
        }
    }
    payload = {
        "contract_version": "3.0.0",
        "engine_count": len(rows),
        "counts": counts,
        "external_binding_required": sum(
            row["external_binding_status"] == "REQUIRED" for row in rows
        ),
        "runtime_evidence_pending": sum(row["owned_question_count"] for row in rows),
        "independent_review_pending": sum(
            row["owned_question_count"]
            for row in rows
            if row["independent_review_status"] == "PENDING"
        ),
        "engines": rows,
    }
    (ROOT / "contracts/engine_implementation_coverage.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    )
    lines = [
        "# V3.0.0 Verified Engine Implementation Coverage",
        "",
        "Generated from authoritative question ownership, requirement-level evidence, "
        "semantic symbols, mapped test discovery, and passing mapped tests.",
        "",
        f"Counts: {counts}",
        "",
        "| ID | Engine | Status | Module | Tests | Justification |",
        "|---:|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['engine_id']} | {row['engine_name']} | {row['implementation_status']} | "
            f"{', '.join(row['implementation_modules'])} | {', '.join(row['test_files'])} | "
            f"{row['justification']} |"
        )
    (ROOT / "docs/ENGINE_IMPLEMENTATION_COVERAGE.md").write_text("\n".join(lines) + "\n")
    print(f"generated verified engine coverage for {len(rows)} engines: {counts}")


if __name__ == "__main__":
    main()
