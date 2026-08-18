from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/baseline/ENGINE_CATALOG_112_V3_0_0.md"
TARGET = ROOT / "contracts/engine_registry.json"
ROW = re.compile(
    r"^\|\s*(?P<id>\d+)\s*\|\s*(?P<name>.*?)\s*\|\s*(?P<orchestrator>.*?)\s*\|"
    r"\s*(?P<source>.*?)\s*\|\s*(?P<output>.*?)\s*\|\s*(?P<runtime>.*?)\s*\|$"
)


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    table, _, _details = text.partition("## New-engine detailed contracts")
    engines: list[dict[str, object]] = []
    for line in table.splitlines():
        match = ROW.match(line)
        if match is None:
            continue
        engines.append(
            {
                "engine_id": int(match.group("id")),
                "engine_name": match.group("name"),
                "orchestrator": match.group("orchestrator"),
                "source": match.group("source"),
                "primary_output": match.group("output"),
                "runtime_status": match.group("runtime").replace(" ", "_"),
            }
        )

    ids = [engine["engine_id"] for engine in engines]
    if ids != list(range(1, 113)):
        raise SystemExit(f"expected ordered engine IDs 1..112, got {ids}")
    if any(engine["runtime_status"] != "NOT_IMPLEMENTED" for engine in engines):
        raise SystemExit("baseline engine runtime status must remain NOT_IMPLEMENTED")

    payload = {
        "schema_version": "1.0.0",
        "contract_version": "3.0.0",
        "expected_count": 112,
        "engines": engines,
    }
    TARGET.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"generated {TARGET.relative_to(ROOT)} with {len(engines)} engines")


if __name__ == "__main__":
    main()
