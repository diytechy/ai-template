## 2026-11-21 — WI-1036: the history readers audited; four calls recompute a past decision

Deferred open items: none. The row is read-only research; the class (c)
rows are the coordinator's to file on trunk, and no operator decision was
taken.

Review: pending (the coordinator).

Built on the maintenance branch `maint/wi-1036` from `1aa6c439a`, with the
commit hooks on. No code changed. The record is in the row's Deliverable
(`../archive/work/complete/WI-1036-history-reader-audit.md`).

- **The note** (`7047e36c8`), `docs/reviews/2026-11-history-readers/README.md`:
  every history call under `project-trajectory/scripts/` by the spec's
  closed definition, each with its line, its git command, its class and a
  reason. 69 calls in 25 files: 45 class (a), 20 class (b), 4 class (c);
  twelve marked borderline with the reason.
  <!-- fig: derived="the counts the note docs/reviews/2026-11-history-readers/README.md declares, read at 1aa6c439a by the method its 'What counts' section states" -->
- **Class (c):** `baseline_snapshot.acceptance_stamp` and
  `_risk_first_written`, and `check_test_first`'s two acceptance walks
  (lines 278 and 314, one decision). The last two sites' behaviour is stated
  by Accepted LLRs (LLR-239, LLR-257), so rows against them amend those
  LLRs.
- **The recount:** 25 files, not the 21 named at filing. `held_status`
  matched only on a docstring; `agent_loop`, `dispatch`, `handback`,
  `id_carrier` and `review_brief` call `merge-base` or diff a range.
- **Deviations from the spec:** none.
- **Tests:** `trace.py --strict`: `orphans=0 integrity=0`, exit 0;
  `check_trajectory.py --strict`: clean, exit 0; the commit hook passed.
  `run_menu.py smoke` was not run (no code changed).
- **Byte deltas:** no budgeted file touched; the note is new (20,496 bytes).
- **Acts owed:** none by this row.
