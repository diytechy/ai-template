+++
id = "WI-106"
title = "Micro-fix batch - hook step count + predicate word-bounds + dup-malformed message + retire launcher IMPROVEMENT_PLAN.md refs (M7/L2/L4/L9)"
workstream = "scripts"
order = 105
+++

## Deliverable

WI-106 (2026-07-12, deep-review-b micro-fix batch): (M7) hooks/pre-commit step-1 comment dropped the stale hand-maintained "six" count (it ran seven steps) - now numberless ("the independent floor checks ... a separate --run-step/script call per check"). (L2) trace.py PREDICATE_MARKERS split into word-boundary-matched _PREDICATE_WORDS + literal _PREDICATE_SYMBOLS (compiled _PREDICATE_RE), so "per"/"within" pin a comparative AC but "proper"/"wrapper"/"notwithstanding" no longer silently suppress the warn-only advisory. (L4) trace.integrity_findings checks duplication before malformed, so a malformed id seen twice now reports "duplicated" for the repeat (well-formed-dup path unchanged). (L9) the meta root agent-resume.sh/.cmd twins retired their archived IMPROVEMENT_PLAN.md scope refs - AGENT_PROMPT scopes work to docs/requirements/work-items.csv + docs/status.md Next action and logs to docs/log.md; the header context list swapped to the live surfaces. Tests: test_trace.py::test_predicate_markers_are_word_bounded + ::test_duplicate_of_malformed_id_reports_duplicated. No spine change, no byte-budgeted file touched. Commit bar: pytest 669 passed/1 skipped -n auto; check_docs --stale exit 0.
