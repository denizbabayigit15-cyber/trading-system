# Question registry blocker

The V3.0.0 baseline references `contracts/questions/question_registry.json` as
the authoritative 900-question mapping. That JSON artifact was not present in
the supplied baseline files. The retained question-bank Markdown is available
under `docs/baseline/`, but it is not an equivalent substitute for the missing
owner/policy/test/fail-action registry.

This package therefore records:

- expected questions: 900;
- runtime PASS: 0;
- runtime UNKNOWN/NOT_EXECUTED: 900;
- machine registry materialized: false;
- R1 impact: blocking.

Do not generate owner, policy, legal applicability, or fail-action mappings by
guessing. Restore the authoritative artifact or open change control.

