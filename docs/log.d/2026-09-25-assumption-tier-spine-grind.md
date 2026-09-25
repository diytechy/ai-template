## 2026-09-25 — The assumption tier's spine, derived down to test cases (a stand-in grind)

An attended grind, run while the owner is absent, after the owner accepted the
[C1 sitting package](../plans/2026-09-25-c1-sitting-package.md). A Fable
reviewer stands in for the owner's spine approvals, and a codex Sol review
(medium effort) runs on each iteration. The decomposition record, plan coverage
and every assumption or decision made along the way are in
[the spine map](../plans/2026-09-25-assumption-tier-spine-map.md) (§6, D1 onward).

Deferred open items: none — the owner-reserved decisions are numbered in the
spine map §6 for the owner's return; none holds a gate or blocks a queue.

### Iteration 1 — needs and system requirements

- **Rows, all Drafted, phase 6:** SN-041 to SN-044 (the vision's two headline
  needs as the owner accepted them, SN-042's acceptance then amended on the
  stand-in's authority; two new needs, SN-043 and SN-044) and SR-187 to SR-219.
- **Sol review:** NOT YET SOUND, 1 blocker (SR-217's undefined event and silent
  narrowing of SN-042), 6 major, 1 minor. All applied.
- **Stand-in review:** APPROVE-WITH-CHANGES, 1 blocker (SR-209 conditioned on
  wall-clock time rather than authorship), 7 major, 6 minor, all applied; the
  fixes were CONFIRMED with one residual major (SR-217's quantifier) and three
  minor, all applied.
- **Codebase research** (four read-only passes) changed SR-204 (activation
  derived from the first approval, since the stage may not read the policy
  file), SR-207 (scoped to tiers the kit compares, since need-text drift is not
  built and the owner deferred it) and SR-208 (refusal before the change lands,
  since a session's staging cannot be intercepted).
- **Commit bar for iteration 1:** smoke **1681 passed, 3 skipped** in 173.2 s.
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=4b191e76 -->
  Seconds **FAIL**: that run alone is 173.2 s against the 60 s budget, so the
  enforce step was not re-run to measure the same breach again. The change is
  registry rows and documents only. `check_docs --stale` OK (0 broken, 3 orphan
  warnings, all pre-existing); `check_trajectory --strict` clean; `trace.py
  --strict-integrity` 0 integrity, 0 orphans; the open-items view regenerated,
  since it counts the new Drafted rows.
