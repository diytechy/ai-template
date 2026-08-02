## 2026-08-01 — WI-394: a Verified spine row can no longer cite a file that never existed

**Summary.** The R2 ruling (option (c), the file-existence half only) built:
`check_doc_refs.py`'s `::` guard is re-scoped at both sites so the FILE half of
a pytest node id is judged like any path, and a new **registry tier** walks the
spine's four Evidence-class cells (TC `Evidence`; LLR
`Module`/`CodeSymbol`/`TestRefs`) — the pointers OUT of the registries that no
gate had ever checked — with stdlib `Path.exists`, warn-first, gating at the
`--strict` `doc-refs` step. The `::node` selector is ruled PROSE and recorded
as an **accepted gap** in [enforcement-audit.md](../enforcement-audit.md), so a
renamed-but-present test node is never implied as covered. The deliberate,
comment-and-test-guarded exclusion the spec mapped was amended, not deleted:
the guard comment now states the re-scoped rule with its ruling, and the named
regression test survives with its joined-lists half intact and its node-id half
flipped to pin the new behavior both ways.

- **Deliverables:** `project-trajectory/scripts/check_doc_refs.py` (guard
  re-scope at `is_path_shaped` + the stat-side strip, the shared `judge_token`
  classifier, `registry_findings` + `SPINE_CELLS`/`CELL_JOIN`, tier-3
  docstring); `tests/test_check_doc_refs.py` (7 new/amended tests, watched red
  first); the enforcement-audit row; the citation triage (below); the WI spec
  closed to `docs/work/complete/` with `specref` cleared (R-F).
- **The census, quoted (check_doc_refs --root . --strict).** Before: **13
  dangling**. After: **0 dangling, rc=0** (untraced 873 → 876, the three
  reclassified `report.md` references). The 6 true registry findings and their
  triage:
  1. `TC-076` Evidence `tests/test_agent_loop_dualplan.py::test_full_round_unattended_selects_and_files` <!-- path-ok: the dead citations this row triaged, quoted as record -->
     → same node in `tests/test_dual_plan_round.py` (preserved verbatim by
     31ad569d's "preserved before deletion" clause).
  2. `TC-076` Evidence `…dualplan.py::test_arbiter_disagreement_pages` → same
     node in `tests/test_dual_plan_round.py`.
  3. `TC-076` Evidence `…dualplan.py::test_missing_rubric_pages_honestly` →
     same node in `tests/test_dual_plan_round.py`.
  4. `TC-091` Evidence `tests/test_agent_loop_dispatch.py::test_unclassified_wi_fails_closed_without_stopping_others` <!-- path-ok: module deleted 2026-07-29 by 31ad569d -->
     (this row's original find; module deleted by 31ad569d) → dead sibling
     REMOVED — WI-383's four live `tests/test_schedule.py` nodes stand as the
     row's evidence.
  5. `LLR-096` Module `project-trajectory/scripts/agent_dispatch.py` <!-- path-ok: the deleted dispatcher, quoted as record --> →
     dropped from the joined list; the surviving `agent_loop.py` entry stands.
  6. `LLR-132` Module — same triage as LLR-096.
  The remaining 7: 4 were the WI's spec-of-record (now archived at
  `docs/archive/specs/WI-394.2026-08-01.md`) quoting its own driven
  evidence (marked `path-ok` with reasons; the invented files were never
  created), 3 were the pre-existing trunk red on `docs/test/report.md` —
  declared LIFECYCLE in `docs/declared-absences`, which is candidate two of
  the prior lane's finding 1 (this log, 2026-08-01, "check_doc_refs --strict
  cannot pass on a fresh lane worktree"), and closes that finding.
- **Deviations from spec:** the spec's "not in scope: repairing the individual
  dead citations" was superseded by the ruling's execution direction — the
  triage is IN this row so the bar ends green, with the before-list quoted
  above as the preserved evidence. The `check_dupes` census red on the copied
  classification chain was resolved by lifting `judge_token` rather than by a
  census line (net less duplicated code, the same messages byte-for-byte).
  RATIFIED cells naming deleted inputs (TC-091 Description/Method, SR-094
  AcceptanceCriteria, LLR-096/132 Detail) deliberately untouched — WI-390's
  program close. **Two `docs/log.md` link TARGETS redirected at the spec's
  archival** (`specs/WI-394.md` → `archive/specs/WI-394.2026-08-01.md`, text
  untouched): `check_trajectory --strict`'s R-F remedy demands the archive
  move, and moving without redirecting inbound links is the exact defect
  WI-288 named ("one indivisible ritual — no caller can do half of it") — its
  `_relink_archived_specs` machinery died with the dispatcher (31ad569d), so
  the ritual was applied by hand, target-only per the WI-288 convention.
  `check_docs` measured back at its pre-existing 4 broken links, none added.
- **Byte deltas on budgeted files:** none (no budgeted doc touched).
- **Verification (watched):** `pytest -q tests/test_check_doc_refs.py
  tests/test_dupes_census_audit.py` — **39 passed**; smoke tier
  (`pytest -q -n auto -m smoke`) — **578 passed, 6 skipped in 8.96s**; full
  unfiltered suite (`pytest -q -n auto`) — **1802 passed, 10 skipped in
  276.37s (0:04:36)**; `trace.py --strict-integrity` rc=0;
  `check_doc_refs --root . --strict` rc=0. Pre-existing and NOT this lane's:
  `check_docs.py --stale` reds on 4 broken links in old `docs/work/complete/`
  specs (reproduced with this branch's changes stashed).
