Reviewed: 36e0c8e6b6c51e2874abe196cede142ffc79722d

**Verified.** I checked that `git rev-parse HEAD` in the lane worktree prints 36e0c8e6b6c51e2874abe196cede142ffc79722d. I read the whole diff in scope and the WI-963 spec, then hunted three failure classes in order. First, fail-open suppression, where a row that should mint is dropped without notice. Second, refusals that lose rows. Third, regressions in callers of the reshaped `(records|drafts, refusal)` returns.

**Filter (`acceptance_record.settled_amendments`, `project-trajectory/scripts/acceptance_record.py:1118`).**
- A record is dropped only when both conditions hold:
  - its id is re-attested by an entry whose `seq` the `before` ledger lacks (`_new_entries`, which `_added_acts` now shares);
  - `split_changed_cells(copy, live)` at `head` shows no approved cell and no routed traced cell.
- The comparison is the whole row against its copy. The net diff is not consulted.
- Absent ledger, absent copy and absent row all lead to a mint. A listed blob that cannot be read, or text that does not parse, leads to a named refusal (`kitlib.git.git_show`'s `UnreadableBlob`). With no records, nothing is read.
- I drove the shipped routes in my own scratch repos:
  - A routed traced cell (`SN-Refs`) that moves after the act still mints WI-001 through `intake_after_merge`.
  - A malformed ledger refuses at both the post-merge arm and `intake.py sweep`.

**Red before the fix.**
- I ran the new `tests/test_intake_settled.py` against the base tree (`git archive 7f8e57192`). Six cases fail at their own assertions: D1, the malformed ledger, the unreadable ledger [after] and [before], the malformed copy and the unreadable copy. Eight characterization guards pass.
- Base `intake._routed_amendments` over the two pinned real landings returns `[LLR-019, LLR-020, LLR-140, LLR-300, SR-019, SR-020]` and `[LLR-207, TC-132, TC-205]`. At the tip, both return `([], None)`. So the replay regression is genuinely red before the fix.

**Callers.**
- `integrate.py:3457` already returns `mint_refusal`.
- `_cmd_sweep` passes the refusal to `_cli_result`.
- `scripts/coordinator/preview_mint.py`, `tests/test_intake.py`, `tests/test_adjudicate_brief.py` and `tests/test_stage_event_detectors_driven.py` all take the new tuple.
- `_ledger_acts` keeps its two-valued contract. An unreadable blob still reads as `[]` for the merge rung, as before.
- `staged_spine_findings` (the pre-commit warn) is untouched, so it reads the unfiltered walk. D1 asserts this.

**Interface and decomposition decisions (my independent reading).**
- IF-091 (provider `scripts/acceptance_record`) is the side that changed: its data cell now names `settled_amendments`. Its counterparts:
  - `scripts/intake` carries the matching change (`_routed_amendments` consumes the call and its refusal).
  - `scripts/integrate` is retained correctly: it reaches the filter only through `intake_after_merge`, and its refusal handling already passes a mint refusal through.
- IF-220 (ledger shape) and IF-123 (the snapshot producer) are retained: the filter only reads them, and redefines neither.
- LLR-342 is the one retained child under SR-178. Its independent decision is "which amendment records the trunk mint may omit". Splitting the refusal arm into its own LLR would add no independent value: the refusal is the filter's own read precondition, and it has no consumer of its own.
- LLR-153 and LLR-158 are amended by appending one sentence each. This is granted by the Done-when, and the approved prefixes are intact (word-diff checked).
- SR-178 (parent) is unchanged, and the filter is consistent with it: a row equal to its acceptance copy has not "moved away".

**Rubric.**
- K2: no SN or SR row changed.
- K3: every new `Implements: SR-178, LLR-342` tag sits in a module that LLR-342 names, on a symbol in its `code_symbol`.
- The skill change is synced: `.claude`, `.agents` and `project-trajectory/skills` copies are identical by `diff -r`.
- The RESYNC_PACK entry is anchored `[since 7f8e57192]`, following the pack's existing convention.

**Done-when map.**

| Done-when item | Covered by |
|---|---|
| D1, both routes | `test_a_row_reattested_in_range_and_equal_to_its_copy_mints_nothing` (sweep subprocess plus `intake_after_merge`) |
| Amended again after its act | `test_a_row_amended_again_after_its_act_still_mints`. Approved-cell arm only; see finding 1. |
| No act in the range | `test_an_amendment_with_no_act_in_range_still_mints` |
| Fail directions | `test_an_absent_ledger_filters_nothing`, `test_the_filter_is_not_consulted_without_amendment_records`, the malformed and unreadable ledger and copy cases, and `test_a_reattested_row_missing_from_its_copy_still_mints` |
| Restored cell | `test_a_cell_restored_after_the_act_still_mints` |
| Real-landing replay | `test_the_two_real_redundant_landings_mint_nothing` (ran, not skipped), plus the after-act fixture |
| LLR and TC rows | LLR-342 and TC-373 are present. In-lane adjudication of the set is still pending: the rows are Drafted and the range carries no act. The coordinator-cycle order puts the act after the review verdicts, so this is not counted as a finding. |
| Shared-walk restatement | `acceptance_record.py:265` comment and LLR-158 detail |
| Workaround removal | coordinator-cycle SKILL §4 step 3 and recipes §3 |
| RESYNC_PACK | `project-trajectory/RESYNC_PACK.md:9343` |
| Coverage bound | LLR-342 detail |

**Commands.**
- `git rev-parse HEAD` -> `36e0c8e6b6c51e2874abe196cede142ffc79722d`
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp <opus>/wi-963 tests/test_intake_settled.py tests/test_intake.py tests/test_adjudicate_brief.py tests/test_stage_event_detectors_driven.py tests/test_acceptance_record.py` -> `214 passed in 112.48s (0:01:52)`
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (963 work item(s), 846 done (88%), 33 cancelled, graph acyclic).`
- Base-tree red check: `pytest tests/test_intake_settled.py` on `git archive 7f8e57192` with the tip's test file -> `6 failed, 8 passed, 1 skipped` (the replay case skips with no git tree; I re-checked it directly against the lane repo with base `intake._routed_amendments`, which mints both landings' rows).
- Probe `<opus>/probe/test_probe.py` (my scratch, driving `intake_after_merge` and `intake.py sweep`) -> `2 passed`: the routed-traced change after the act mints, and the same-range sweep after a repair refuses again (see finding 3).
- Mutant probe `<opus>/probe/test_mutant.py` (`_row_settled` blind to traced cells, patched on `intake.acceptance_record`) -> all 11 committed cases run under it pass; only my routed-traced probe fails (`1 failed, 11 passed`).
- TC tier census over `docs/test/test-cases.toml` against `conftest.SLOW_MODULES` -> `['TC-373'] 163`.

- [MINOR] tests/test_intake_settled.py:247 -> No committed case pins the routed-traced half of the whole-row comparison that LLR-342 and TC-373 claim to verify. A `_row_settled` that ignores traced cells passes every committed case (my mutant probe: 11 passed, while an `SN-Refs` change made after the act would be silently suppressed). The shipped code is correct today; my probe mints. -> Add a case where a ROUTED traced cell (an SR's `SN-Refs`, or an LLR's `SR-Refs`) moves after the act and assert that the amendment row mints. Optionally, add its contrast: an unrouted traced cell (`Evidence`) moved after the act still settles. Rubric anchor: K1 (TC-373's Method claims the whole-row comparison). -> @owner
- [MINOR] docs/test/test-cases.toml:1539 -> TC-373 carries `tier = "Smoke"`, but its only evidence module, `test_intake_settled`, is in `tests/conftest.py` `SLOW_MODULES`, so it never runs in the smoke tier. PROCESS.md says "The `Tier` column is the source of truth". TC-373 is the only Smoke TC of the 164 whose evidence is entirely in SLOW_MODULES; the other 163 read Full. -> Set TC-373's tier to `Full` in the spine change, or move a pin into a smoke-tier module and cite it. Rubric anchor: K1 (the row's text must be true). -> @owner
- [MINOR] project-trajectory/scripts/intake.py:729 -> For a ledger or copy that DOES NOT PARSE, the refusal's recovery is "fix it in a reviewed commit, then run `intake.py sweep --before <before> --after <after>`". That sweep re-reads the same immutable blob at `<after>` and refuses again, with the identical message. I confirmed this by probe: after the fix commit, the same-range sweep returns rc 1, while `--after <fix commit>` returns rc 0, "nothing to mint". The same wording sits in LLR-342's detail (docs/requirements/low-level-requirements.toml:1552), in RESYNC_PACK (project-trajectory/RESYNC_PACK.md:9358) and in the spec's "A refusal on each route". The path is rare: a malformed ledger reaches trunk only through a partial or hand-made file. -> Word the parse-failure recovery as a sweep from `--before <before>` to `--after <the reviewed fix commit>`. If `<before>` is the malformed side, the range has to start at or past the fix. Keep "fetch, then re-sweep the same range" for the cannot-be-read arm only. Amend LLR-342 and the RESYNC entry with it. Rubric anchor: K1 (the LLR states a recovery that cannot succeed). -> @owner
- [MINOR] project-trajectory/scripts/acceptance_record.py:1083 -> This repeats existing code (PROCESS.md §3, "Consolidate, don't duplicate"):
  - `_snapshot_copy_rows` repeats `_spine_rows_at`'s carrier-preference loop (acceptance_record.py:296). It differs only in that it reports a listed-but-unreadable or unparseable carrier instead of reading it as absent.
  - `_reattested_added` (acceptance_record.py:1066) computes the same id set as `reattested_between` (acceptance_record.py:1155) over the same two ledger reads, differing only in how it reads an unreadable blob and in its message.

  The lane already applied the right pattern to the ledger (`_ledger_read` as the one tri-state reader, `_ledger_acts` as its older two-valued view) but not to these two pairs. -> Make `_snapshot_copy_rows`'s tri-state read the one carrier loop, with `_spine_rows_at` as its degrade view. Make `reattested_between` wrap `_reattested_added`, translating the failure into its merge-rung wording (and its unreadable-as-absent contract). -> @owner

VERDICT: CHANGES-REQUESTED findings=4
