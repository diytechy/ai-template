## 2026-09-05 — Expand the redesign plan for independent cross-check

Expanded the [Codex plan](../ai-template-redesign-2026-09-05-codex/README.md)
with vision objective anchors, invocation accounting, fresh builder rework,
queued-work reconciliation, failure cases and implementation slice acceptance.
Prepared a [review brief](../ai-template-redesign-2026-09-05-codex/CROSSCHECK-BRIEF.md).
Corrected the inherited unconditional-test recommendation and Worktrunk
incompatibility rationale; historical Fable reviews and metadata are unchanged.

Scope/deviations: owner-requested planning sitting, no WI execution or live
policy/schema change. No budgeted document was edited (byte delta: 0).
No paid provider invocation, new independent review or runtime benchmark.

Validation on `fa17b85f` plus these documentation changes:

- Purpose mapping covers 27/27 needs and backlog mapping covers 18/18 queued
  WIs, with unique IDs. <!-- fig: Python tomllib parsed the need keys and queued WI frontmatter; set equality against Markdown table IDs; fa17b85f + this docs diff -->
- `.venv/bin/python -m pytest -q -n auto -m smoke`:
  `1638 passed, 4 skipped in 64.19s (0:01:04)`. <!-- fig: command on preceding line; fa17b85f + this docs diff -->
- `.venv/bin/python scripts/check_smoke_budget.py --mode enforce`:
  `1638 passed, 4 skipped in 61.81s (0:01:01)`; measured wall
  `62.0s vs 60s budget -> OVER`, exit 1. <!-- fig: command on preceding lines; fa17b85f + this docs diff -->
- `.venv/bin/python project-trajectory/scripts/check_docs.py --root . --stale`
  passed link validation; orphan and staleness warnings were reported.
- `.venv/bin/python project-trajectory/scripts/check_trajectory.py --root . --strict`
  exited clean with existing connectivity, trace and work-item warnings.
- `git diff --check` passed. Fable historical files match their HEAD bytes.

Both measured smoke runs exceeded the declared budget. The owner explicitly
authorized committing this documentation change despite the timing failure,
citing flaky smoke timing on this computer. That is a scoped exception, not a
passing timing result or a changed budget. No test re-tiering or budget
adjustment was made. No full-suite result is claimed.

Deferred open items: none — this sitting prepares proposal choices for the
next cross-check; it makes no live ruling and creates no new operational hold.
