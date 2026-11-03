Reviewed: d3d6ca74647f38f056b422017aee1645948d0b1d

**Verified.** This is a FULL-LANE review of WI-963 (range 25a7e4599..d3d6ca746, convergence stance). I checked that HEAD = d3d6ca746 before running anything. I read the diff of `acceptance_record.py`, `intake.py`, `scripts/coordinator/preview_mint.py` and `tests/test_intake_settled.py`, plus the spine rows LLR-153, LLR-158, LLR-364, TC-403 and IF-091 (and IF-220, IF-123 and SR-178 as counterparts), the coordinator-cycle skill, its recipes and RESYNC_PACK.

Worst failure class: fail-open, meaning an amendment row the mint should file is silently dropped. I hunted that first. The reverse direction is fail-closed: `_ledger_read` keeps the three outcomes apart (absent, unreadable, unparseable). `_ledger_acts` still maps an unreadable blob to `[]`, as the merge rung did before. `_snapshot_copy_rows` refuses a listed copy it cannot read or parse. A missing copy or missing row mints. The refusal threads through `_amendment_drafts`, `intake_after_merge` and `preview_mint`. Every caller of the changed return shape is updated (grep).

Red-before: I ran the new test file against an exported copy of the pre-fix tree (`git archive 25a7e4599`). 14 tests fail there: every settle and refusal arm. The 9 characterization guards pass there, as their docstrings say they should. The real-landings test skips there (no history). So I ran the pre-fix `intake._routed_amendments` directly on the two pinned landings: it returns `SR-019, SR-020, LLR-019, LLR-020, LLR-140, LLR-300` and `LLR-207, TC-132, TC-205`. The fixed code returns `([], None)` for both. TC-403's evidence list matches the module's 17 test functions one to one.

Done-when map:
- (1) Settled row, both routes: `test_a_row_reattested_in_range_and_equal_to_its_copy_mints_nothing`.
- (2) Amended again after the act: `test_a_row_amended_again_after_its_act_still_mints`.
- (3) No act in range: `test_an_amendment_with_no_act_in_range_still_mints`.
- (4) Absent ledger: `test_an_absent_ledger_filters_nothing`. Not consulted without records: `test_the_filter_is_not_consulted_without_amendment_records`. Malformed or unreadable ledger or copy: the four refusal tests. Missing copy: `test_a_reattested_row_missing_from_its_copy_still_mints`.
- (5) Restored cell: `test_a_cell_restored_after_the_act_still_mints` covers an approved cell with no later writer. It is UNCOVERED for a routed traced cell under a later writer, and that case fails open (finding 1).
- (6) Real landings: `test_the_two_real_redundant_landings_mint_nothing`.
- (7) Spine rows: LLR-364 and TC-403 are Drafted, and their texts match the code (K1). LLR-153's detail gains the one trigger-(a) sentence, which the spec grants. The in-lane act is a landing step not in this range: `docs/archive` is untouched. Under the convergence stance I read no sitting record.
- (8) Shared-walk restatement: the comment above `AMENDMENT_CSVS` and LLR-158's detail both state it. `staged_spine_findings` is unchanged.
- (9) Skill and recipes: the workaround is dropped, and the three skill copies are identical (`diff -r`).
- (10) RESYNC_PACK: one entry, anchored `[since 25a7e4599]`, no migration.

Counterpart decisions (brief para. 2):
- IF-091 (owner `acceptance_record`) gains the `settled_amendments` call. Its requestor `scripts/intake` is already listed. TC-403 now verifies IF-091. The counterpart is retained, correctly.
- IF-220 already declares `copied` and lists `acceptance_record` as a consumer, so it needs no change. Retained.
- IF-123 is unchanged and the filter reads no new `copy_live` surface. Retained.
- SR-178 ("text that has moved away from its acceptance record is reported") is retained. A row equal to the copy its own re-attesting act wrote has not moved away. The one exception is the absorbed-copy case in finding 1.
- LLR-364 is a separate child of SR-178. It is an independent filtering obligation with its own fail directions, separate from LLR-153's mint invariant, and splitting it further would only separate the ledger read from the copy comparison that the one decision needs together.
- TC-403 is the single integration TC across both mint routes. Splitting it per arm adds no independent verification purpose, since every arm drives the same `intake_after_merge` path.

**Commands.**
- `git rev-parse HEAD` -> `d3d6ca74647f38f056b422017aee1645948d0b1d`
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../revB/wi-963 tests/test_intake_settled.py tests/test_intake.py tests/test_acceptance_record.py tests/test_adjudicate_brief.py tests/test_module_size_ratchet.py tests/test_stage_event_detectors_driven.py` -> `280 passed in 252.36s (0:04:12)`
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (990 work item(s), 879 done (89%), 34 cancelled, graph acyclic).` (exit 0; WARNs only)
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=138 LLR=330 TC=357 orphans=0 integrity=0 ... interface-findings=0 ...` (exit 0). It rewrote the gitignored `docs/test/report.md` in the worktree. `git status` stays clean.
- Pre-fix red check, run from an exported copy of 25a7e4599 with the new test file added: `pytest tests/test_intake_settled.py` -> `14 failed, 9 passed, 1 skipped`.
- The pinned landings through the pre-fix `intake._routed_amendments` -> `['SR-019', 'SR-020', 'LLR-019', 'LLR-020', 'LLR-140', 'LLR-300']` and `['LLR-207', 'TC-132', 'TC-205']`.
- Probe `revB/probe/probe_restore.py` (the real `copy_live` acts, the real `_routed_amendments`). The scenario: SR-001 is amended and its `SN-Refs` re-pointed, then act A re-attests SR-001. `SN-Refs` is then restored to its pre-range value. With no later act, the result is `nolater routed after filter: ['SR-001'] None`. With a later act B that re-attests only SR-002 in the same registry, the result is `later routed after filter: [] None`.

**Findings.**

- [MAJOR] project-trajectory/scripts/acceptance_record.py:1226 -> The `_routed_unmoved` escape settles a row whose routed traced cell moved after its act, which is fail-open.
  - Scenario: a lane amends SR-001 and re-points its `SN-Refs`, and act A re-attests both. The lane then restores `SN-Refs` to its pre-range value, an edit nobody judged. A later act B re-attests another row of the same registry, so its copy absorbs the restore (traced refreshes need no flag in `copy_live`). At `after` the row equals its copy, and its routed cells equal those at `before`, so `_settled_row` returns True and the mint drops SR-001.
  - That combination (new requirement text traced to the old need) was never judged. The pre-fix code minted it, and the same range without act B still mints it (probe output above).
  - This breaks Done-when item 5 ("edited after its act and restored to its pre-range text in one cell, still mints") and D-013. The route is supported: multi-act ranges with edits between acts are the pattern `test_a_later_act_copying_the_registry_does_not_settle_a_row_it_did_not_reattest` already treats as in scope.
  - Base-versus-after equality cannot tell "never moved" from "moved and restored" once the act's own copy has been overwritten.
  - Fix: delete the `_routed_unmoved` arm so that any later entry writing the row's registry leaves the row unsettled. That costs one redundant row in the `test_a_later_writer_leaves_a_row_with_unmoved_routed_cells_settled` case, which is today's behaviour, and that test flips to assert the mint. Add the restore-under-a-later-writer case to TC-403, and drop the second arm from LLR-364's detail and from RESYNC_PACK.
  - The alternative needs an IF-220 format change: each entry records its re-attested rows' routed cell values, so the act's own copy is recoverable on a squashed range.
  - The fix is a deletion, not an added guard. Anchor K1 (LLR-364's detail asserts that the second arm proves "nothing routed moved for a later copy to absorb", which is false for a restore).
  - @owner convergence-class: yes

- [MINOR] docs/requirements/low-level-requirements.toml:1551 -> LLR-364's `code_symbol` names `_new_entries`, which is defined nowhere in the repo (grep over all `*.py` finds no match). The CodeSymbol crosscheck only tests tag-site containment, so nothing catches it. Drop `_new_entries` from the cell. K3. @owner

- [MINOR] project-trajectory/scripts/acceptance_record.py:1150 -> `_reattested_ids` carries `Implements: SR-178, LLR-364` and is listed in LLR-364's `code_symbol`, but its only caller is `reattested_between` (line 1283), which is LLR-278's merge-rung reader. The filter never calls it. Retag it to `SR-178, LLR-278` and move it into LLR-278's `code_symbol`, or inline it back into `reattested_between`. K3. @owner

- [MINOR] project-trajectory/scripts/acceptance_record.py:1109 -> `_reattested_added` repeats the work of `_added_acts` (line 1334) and of `reattested_between`'s body (line 1275): each reads the ledger at `base` and `head` and takes `added_ledger_entries`, differing only in failure policy (refuse versus collapse to `[]` versus a merge-rung refusal message). That makes three readers of "the entries the range added", against PROCESS.md §3 "Consolidate, don't duplicate". Make `_added_acts` and `reattested_between` views over `_reattested_added`, the way this change already made `_ledger_acts` a view over `_ledger_read`. Separately, `_routed_unmoved` re-implements `_row_settled`'s traced half; it goes away if finding 1 deletes it. @owner

VERDICT: CHANGES-REQUESTED findings=4
