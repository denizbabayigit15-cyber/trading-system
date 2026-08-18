from __future__ import annotations

import hashlib
import html
import re
import zipfile
from pathlib import Path

from trading_system.contracts.models import QuestionReviewQueue, QuestionReviewWorkbookManifest


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sheet_names(path: Path) -> tuple[str, ...]:
    with zipfile.ZipFile(path) as archive:
        workbook_xml = archive.read("xl/workbook.xml").decode("utf-8")
    return tuple(
        html.unescape(name)
        for name in re.findall(r'<(?:[A-Za-z0-9_]+:)?sheet\b[^>]*\bname="([^"]+)"', workbook_xml)
    )


def validate_question_review_workbook(
    manifest: QuestionReviewWorkbookManifest,
    queue: QuestionReviewQueue,
    repository_root: Path,
) -> None:
    root = repository_root.resolve()
    path = (root / manifest.workbook_path).resolve()
    if not path.is_relative_to(root):
        raise ValueError("workbook path escapes repository root")
    if not path.is_file():
        raise ValueError("review workbook is missing")
    if sha256(path) != manifest.workbook_sha256:
        raise ValueError("review workbook hash does not match its manifest")

    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise ValueError("review workbook contains a corrupt ZIP member")
        xml_text = "\n".join(
            archive.read(name).decode("utf-8", errors="replace")
            for name in archive.namelist()
            if name.endswith(".xml")
        )

    if sheet_names(path) != manifest.sheet_names:
        raise ValueError("review workbook sheet names do not match its manifest")
    missing_ids = [item.question_id for item in queue.items if item.question_id not in xml_text]
    if missing_ids:
        raise ValueError(f"review workbook is missing queue IDs: {missing_ids}")
