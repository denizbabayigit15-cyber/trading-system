from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "contracts/integrity_manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    paths = [
        *sorted((ROOT / "docs/baseline").glob("*.md")),
        *sorted(path for path in (ROOT / "contracts").rglob("*.json") if path != TARGET),
        *sorted((ROOT / "schemas").glob("*.json")),
    ]
    files = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "size_bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in paths
    ]
    payload = {
        "schema_version": "1.0.0",
        "contract_version": "3.0.0",
        "algorithm": "sha256",
        "files": files,
    }
    TARGET.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"generated {TARGET.relative_to(ROOT)} with {len(files)} hashes")


if __name__ == "__main__":
    main()
