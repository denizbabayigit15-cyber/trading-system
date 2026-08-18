from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from datetime import datetime
from decimal import Decimal
from enum import Enum


def _json_value(value: object) -> object:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (set, frozenset)):
        items = [_json_value(item) for item in value]
        return sorted(items, key=lambda item: json.dumps(item, sort_keys=True, ensure_ascii=False))
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_json_value(item) for item in value]
    if value is None or isinstance(value, (str, int, bool)):
        return value
    raise TypeError(f"unsupported canonical JSON value: {type(value).__name__}")


def canonical_json(value: object) -> bytes:
    """Serialize a contract value deterministically for hashing and signatures."""
    return json.dumps(
        _json_value(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()


def sha256_digest(value: object) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()
