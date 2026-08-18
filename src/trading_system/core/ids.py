from __future__ import annotations

import re
import uuid

_PREFIX = re.compile(r"^[a-z][a-z0-9_]{1,31}$")


def new_id(prefix: str) -> str:
    """Return a sortable UUIDv7 identifier with a governed type prefix."""
    if _PREFIX.fullmatch(prefix) is None:
        raise ValueError("identifier prefix must be lowercase snake_case")
    return f"{prefix}_{uuid.uuid7().hex}"
