## 2026-09-05 — Third Fable review: cross-check of the expanded redesign plan

Answered the [cross-check brief](../ai-template-redesign-2026-09-05-codex/CROSSCHECK-BRIEF.md)
in [FABLE-REVIEW-3-CROSSCHECK.md](../ai-template-redesign-2026-09-05-codex/FABLE-REVIEW-3-CROSSCHECK.md):
executable for P0a/P0b with named corrections, all applied to the active plan
documents. The corrections run one way — toward the smaller form: objective
anchors as README prose (no `objective_refs` carrier, P1b/P9b deferred); a
minimum per-invocation record plus three rules (the fuller metrics contract
deferred); one `[step:smoke]` at `from-stage = DevStg-Tests` instead of a
six-row validation selector; the hats sweep dispositioned (H1 a targeted
repair, H2–H5 into the disposition manifest, no seventeenth hat). Codex's two
corrections to the second review accepted in an addendum there.

Scope/deviations: owner-requested review sitting; docs under the redesign
folder only. No WI, dial, registry, queue or runtime change. Budgeted-document
byte delta: 0. No provider call.

Validation at `360a075a` plus these docs changes:

- `.venv/bin/python -m pytest -q -n auto -m smoke`:
  `1638 passed, 4 skipped in 56.00s`. <!-- fig: command on preceding line; 360a075a + this docs diff -->
- `.venv/bin/python scripts/check_smoke_budget.py --mode enforce`:
  `1638 passed, 4 skipped in 56.18s`; `smoke wall-clock budget: 56.4s vs 60s
  budget -> within`, exit 0. <!-- fig: command on preceding lines; 360a075a + this docs diff -->
- A first smoke run failed `test_stage_ladder.py::test_this_repo_is_clean_at_the_ERROR_severity`
  because this review's gap findings were labelled `G1`–`G4`, the retired gate
  vocabulary; renamed to `GAP-1`–`GAP-4` and re-run green above.
- Relative links and anchors across the seven touched files resolve (0 bad).

Deferred open items: none new. GAP-2 in the review (docs-only diffs owing the
hook floor rather than the timed smoke run) is a proposed working-agreement
change for the owner, not applied.
