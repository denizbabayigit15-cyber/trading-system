from datetime import UTC, datetime

import pytest

from trading_system.evidence.journal import Journal, JournalEntry


def test_journal_is_append_only_and_evidence_linked() -> None:
    journal = Journal()
    entry = JournalEntry("j1", "order-1", datetime(2026, 1, 1, tzinfo=UTC), "decision", ("e1",))
    journal.append(entry)
    assert journal.entries_for("order-1") == (entry,)
    with pytest.raises(ValueError):
        journal.append(entry)
