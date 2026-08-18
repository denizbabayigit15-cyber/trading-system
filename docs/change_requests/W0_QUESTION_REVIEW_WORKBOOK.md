# W0 first-wave question review workbook

This slice adds a human-editable Excel input template for all 150 first-wave
questions while preserving the fail-closed decision boundary.

- Source question fields are populated from the reviewed queue and visually
  separated from editable cells.
- Editable decision statuses are only `DRAFT` and `READY_FOR_REVIEW`.
- Dropdown validation is provided for applicability, criticality, information
  class, and recertification status.
- Formula-driven readiness checks report `BOŞ`, `EKSİK`, or
  `İNCELEMEYE_HAZIR`.
- The workbook begins with zero decisions, approvals, adoptions, runtime PASS
  results, and live authority.
- A manifest binds the workbook bytes to the reviewed queue with SHA-256.

The workbook is an input aid only. Independent approval must still pass the
separate decision-ledger contract and cannot create live authority.
