from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class JournalEntry:
    entry_id: str
    subject_id: str
    observed_at: datetime
    narrative: str
    evidence_ids: tuple[str, ...]


class Journal:
    def __init__(self) -> None:
        self._entries: dict[str, JournalEntry] = {}

    def append(self, entry: JournalEntry) -> None:
        if not entry.narrative.strip():
            raise ValueError("journal narrative is required")
        if entry.entry_id in self._entries:
            raise ValueError("journal entry IDs are immutable")
        self._entries[entry.entry_id] = entry

    def entries_for(self, subject_id: str) -> tuple[JournalEntry, ...]:
        return tuple(entry for entry in self._entries.values() if entry.subject_id == subject_id)
