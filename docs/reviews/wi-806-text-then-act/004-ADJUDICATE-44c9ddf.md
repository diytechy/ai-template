# 004 — ADJUDICATE (independent, Claude Opus) — WI-806 amended approved rows at `44c9ddfd`

Adjudicator: independent Claude Opus, a fresh session. I wrote none of WI-806's
code or rows and none of the earlier verdicts. The question is the brief's
(`review-tmp/wave15/brief-wi806-amend-r2.md`): MEANING or CLARITY, and for a
MEANING row on a released rung, whether I would bless the new text. Anchors:
`docs/archive/last_approved/` for LLR and TC, copied at `7e001ccc`. The basis
shared with the first approval (lane bar, the 21 mutants, the residue
reproduction, the scratch check of the replacement text) is in
`003-ADJUDICATE-44c9ddf.md`. This file adds only what bears on the amendments.

## Basis (probed, not trusted)

- **What moved against the anchor** (`git diff cde27048 44c9ddfd`):
  - LLR-173: `detail` and `rationale`.
  - LLR-245: `detail` and `code_symbol`.
  - LLR-298: `code_symbol` only.
  - TC-173: `method`, `expected`, `evidence` and `verifies`.
  - LLR-302 is new.
  - No `Status` changed and no SR cell changed. IF-129 is unchanged: its only
    contract cell is `data = "split_changed_cells: ..."`, at the anchor and at
    HEAD alike.
- **LLR-245's `detail` is 002's replacement byte for byte.** I re-read the code
  it describes:
  - `_ledger_live_rows` absorbs a row only when `_claims_approval(before)`, and
    `_removed_rows` only rows whose copy claims approval.
  - A flip is `not _claims_approval(before) and _claims_approval(row)`, so a
    flipped row is never absorbed. `_unattested_rows` no longer subtracts flips.
  - The parenthetical states that invariant, which is what makes the dropped
    subtraction a no-op (D-006, confirmed).
  - `code_symbol` adds `_ledger_live_rows`, tagged `Implements: SR-207,
    LLR-245`.
- **LLR-173's `rationale` is 002's replacement byte for byte.**
- **LLR-173's `detail` deviates from 002 in the pointer sentence only.** It
  reads "Except for the root and a verified squash landing that LLR-302
  admits, ...". The exceptions are forced by the code, as Sol's round-1 MINOR
  found:
  - a root commit is not judged, so a first signing can seed rows and record
    together;
  - an exempt squash carries text and act together.

  But "a verified squash landing" names the landing, and the exemption is wider:
  an abandoned squash's next commit gets it too (reproduced in 003). That commit
  writes the copy while changing text, and it is not a squash landing. So the
  sentence as written is false of a commit LLR-302 admits. The fix is to point
  at the exemption, not at the landing.
- **TC-173's deviations from 002 are forced, but two clauses of the new `method`
  are not right.**
  - The forced parts:
    - the merge clause gained "a row only one parent carried judged by its cell
      values" (builder round 1, Sol's round-1 BLOCKER);
    - the squash clause was restated for builder round 2;
    - `evidence` enumerates nodes instead of citing the file, because Terra's
      round required every entry to name an existing function. All 24 nodes
      exist, and each LLR-302 clause has a cited node that kills its mutant
      (003), except M15.
  - (i) "then every commit it folds in passes before the index is exempt"
    reads as a claim that the folded commits pass. The obligation is a
    condition: the squash is admitted only when they pass. A test author
    cannot tell which to check.
  - (ii) "a stale message or other mismatch judges the index plainly" is false
    of the residue under its natural reading. A stale message whose tip contains
    HEAD, with the tip's own spine and record staged, exempts the index. The
    cited `test_a_stale_squash_message_exempts_no_other_commit` asserts exactly
    that (`== []`), so the method contradicts its own evidence.
  - The M15 clause ("a record only one parent wrote") has no test. 003 owes
    one, and the `evidence` replacement below cites it.
  - `expected` is 002's ruled text, unchanged. `verifies`
    (`SR-179;LLR-178;SR-140;LLR-302`) is correct.
- **LLR-298: `code_symbol` only** (`+_commit_parents`, `+_each_lane_commit`).
  It is a traced cell, both helpers carry `Implements: SR-148, ... LLR-298`, it
  is not drift by `is_drifted`, and it is not in the brief. It owes no
  re-attestation, and it must not be named in `--reattests`.

## Rulings

- [MEANING] LLR-173 detail -> before: the record's copy contract, the unanchored rule, three refusals, a git-derived stamp and SR-140's two record fields, with nothing about when the recorded text was committed -> after: adds that the approval-act rows' text was committed before the act that writes the copy, which changes only Status and adds or removes none, except for the root and an exempt squash -> MEANING: a copy taken in an amend-plus-flip commit satisfied the old text and fails the new. The `rationale` change is clarity, as 002 ruled. Not blessed as written, for one cause: "a verified squash landing that LLR-302 admits" leaves out the commit after an abandoned squash, which LLR-302's exemption also admits. **[RETURN]** Replacement `detail` (it differs from the live text in one phrase, "a verified squash landing that LLR-302 admits" -> "a commit that LLR-302's squash exemption admits"); `rationale` stands:
```text
The approval RECORD SR-140 requires, sited: LLR-158's comparison basis (SR-178's drift rule) and LLR-178's mirror invariant (SR-179's refusal) are its two readers, and what make it worth recording. copy_live(root, seed=False) mirrors the snapshotted registries (the four spine tiers, interfaces/external/components, which carry human-only approval and state cells, and assumptions) BYTE FOR BYTE into docs/archive/last_approved/, preserving repo-relative paths so spine_carrier.resolve/carriers/stem resolve under the snapshot root verbatim, carrier fallback included; the stale other-carrier file for a stem is deleted in the same act, or the next read raises "exists under BOTH carriers". Except for the root and a commit that LLR-302's squash exemption admits, the approval-act rows' text the copy records was committed before the act that writes the copy, which changes only their Status and adds or removes none; the off-spine registries the copy also records are outside that ordering. Whole files rather than extracted rows is what makes "snapshot file == live file at the copy commit" DECIDABLE - LLR-178 carries that mirror invariant - and it is also what makes the UNANCHORED rule decidable, because the copy keeps each row's own Status cell, so a live row claiming approval whose snapshot copy reads below it is an approval that never rode a copy. unanchored_findings asks that of every tier SNAPSHOT_TIERS lists, the needs file's needs and stakeholders included, and reads the needs registry's copy under its legacy markdown carrier as present. Three refusals are load-bearing and each is the opposite of a convenient degrade: copy_live REFUSES to CREATE the directory without seed=True, because the first snapshot blesses whatever text is in the tree and must ride the owner's reviewed signing commit (reachable only from `intake.py snapshot --seed`); load_all returns None for an absent directory and RAISES on a file that exists and will not parse, because {} and None are opposite claims and the empty one reads as "re-bless everything with no diff shown"; and rows_for is the ONE place the None sentinel is collapsed, so no caller invents its own `or {}`. is_drifted/drifted_cells delegate the cell comparison to LLR-158's split_changed_cells and arm on the APPROVED half only. stamp() is advisory and derived FROM GIT rather than from a file, so it can never quietly become the ledger this mechanism replaced; every arm degrades to ("", ""). SR-140's two remaining record fields come from the same two places and neither is a cell: the TRANSITION is the copy's Status read against live's (the comparison above), and the ACTING REVIEWER is the AUTHOR of the commit that wrote the copy - which is why the copy must ride the approval commit and why the author is queried from git rather than stamped, since a stamped reviewer is a claim and a commit author is a record. unanchored_findings joins the integrity failure set, so it fails the always-on --strict-integrity floor at every stage; it is vacuous until the record holds a registry, so a tree that has signed nothing is never redded by it.
```

- [MEANING] LLR-245 detail -> before: absorbed rows ("approved text drifted from the recorded copy") minus the rows the act flips minus the rows named by --reattests -> after: absorbed rows (a recorded copy claiming approval whose approved cells moved or whose row the live registry dropped; a flipped row's copy reads below approval, so it is never absorbed) minus the rows named by --reattests -> MEANING, as 002 ruled. The flip subtraction is gone, and absorption is now defined rather than glossed. A correct implementation of the old text that read "drifted" as "live claims approval and differs from the copy" fails the new one. **Blessed:** the text is 002's replacement byte for byte, and it is true of `_ledger_live_rows`, `_removed_rows` and `_unattested_rows` at HEAD. It is re-attested in the act. `code_symbol` (`+_ledger_live_rows`) is a traced cell and is true.

- [MEANING] TC-173 method/evidence -> before: the mirror-invariant suite, items (a) to (e), verifying SR-179 via LLR-178 -> after: adds (f), the text-then-act suite, and verifies LLR-302 -> MEANING (a new acceptance condition and a new row verified; `expected` and `verifies` are as 002 ruled). Not blessed as written, for three causes:
  - (i) the squash clause states as fact what is a condition;
  - (ii) "a stale message or other mismatch judges the index plainly" contradicts the cited test's residue assertion;
  - (iii) the record-path half of "judged by what neither parent carried" is unverified (M15).

  **[RETURN]** Replacement cells. In `method`, (a) to (e) and the rest of (f) are unchanged, and only the merge and squash clauses change. `evidence` appends 003's owed test:
  - `method`:
```text
Run the mirror-invariant half of the baseline-snapshot suite over real temp repos - the half TC-167 no longer covers, which is the record's own contents. (a) A clean copy passes, so the rule is silent on the legitimate act it exists to permit. (b) A HAND-EDITED record file fails, and (c) a PARTIAL copy fails - the two forgeries the single byte-identity comparison catches without a second detector. (d) THE DELETION ASYMMETRY, both arms executed rather than argued: a record file deleted WHILE THE REST OF THE RECORD STANDS fails (the cheap laundering - removing the page the unanchored rule reads), while deleting the WHOLE record is SILENT (retirement and wholesale replacement are legitimate). (e) The prose README inside the record is exempt, because it is not a recorded registry and has no live counterpart to be identical to. (f) Run the text-then-act suite over real temp repos: a commit that writes the record while changing an approval-act row's cell other than Status, a traced cell included, or adding or removing such a row, is refused, while a commit that writes no record is not judged; text followed by a Status-and-copy act passes; the pre-commit hook runs the step and the merge slot's ladder consults the rung; a no-verify lane commit is refused at the landing; a merge, a refresh merge included, is judged by what neither parent carried, with a row only one parent carried judged by its cell values and a record only one parent wrote not the merge's own, so a refresh merge that combines two text commits beside trunk's act on another registry passes, and a merge's own text beside the record is still refused; a squash whose SQUASH_MSG tip contains HEAD, with the approval-act registries and record in the index byte-equal to the tip's, is exempt from judging the index and is admitted only when every commit it folds in passes; when either condition fails the index is judged plainly, so a lane not containing HEAD, including one whose squash git combines from two judged cell values into a third, is refused with the rebase hint only when ordinary judging finds mixed text and act; a refreshed lane's squash passes; a SQUASH_MSG an abandoned squash left behind exempts a direct commit staging the tip's own registries and record, judges plainly one staging any other spine text beside them, and is gone after the next commit; a commit whose parent the repository cannot read, and a diff git cannot read, are reported rather than skipped; and a root commit passes.
```

  - `evidence`:
```text
tests/test_baseline_snapshot.py::test_a_clean_copy_satisfies_the_mirror_invariant; tests/test_baseline_snapshot.py::test_a_HAND_EDITED_snapshot_fails_the_mirror_invariant; tests/test_baseline_snapshot.py::test_a_PARTIAL_copy_fails_the_mirror_invariant; tests/test_baseline_snapshot.py::test_a_snapshot_file_DELETED_while_the_record_STANDS_fails_the_mirror; tests/test_baseline_snapshot.py::test_deleting_the_WHOLE_record_is_SILENT; tests/test_baseline_snapshot.py::test_the_README_is_prose_and_is_exempt_from_the_mirror; tests/test_text_then_act.py::test_a_mixed_commit_is_refused_at_pre_commit; tests/test_text_then_act.py::test_the_two_commit_form_is_accepted; tests/test_text_then_act.py::test_a_row_added_or_removed_beside_the_act_is_refused; tests/test_text_then_act.py::test_a_traced_cell_beside_the_act_is_text_too; tests/test_text_then_act.py::test_a_commit_that_writes_no_record_is_never_judged; tests/test_text_then_act.py::test_a_no_verify_lane_commit_is_refused_at_the_landing; tests/test_text_then_act.py::test_the_merge_ladder_consults_the_text_then_act_rung; tests/test_text_then_act.py::test_a_refresh_merge_is_judged_by_what_neither_side_carried; tests/test_text_then_act.py::test_a_squash_landing_is_admitted_only_when_its_lane_commits_pass; tests/test_text_then_act.py::test_a_first_commit_has_nothing_before_it; tests/test_text_then_act.py::test_the_pre_commit_hook_runs_the_text_then_act_step; tests/test_text_then_act.py::test_a_commit_whose_parent_cannot_be_read_is_refused_by_name; tests/test_text_then_act.py::test_a_diff_git_cannot_read_is_reported_not_skipped; tests/test_text_then_act.py::test_a_row_only_one_parent_carried_is_judged_by_its_cell_values; tests/test_text_then_act.py::test_a_stale_squash_message_exempts_no_other_commit; tests/test_text_then_act.py::test_a_squash_combining_two_judged_cells_into_a_third_is_refused; tests/test_text_then_act.py::test_a_squash_of_a_lane_not_containing_head_is_refused_with_the_rebase_hint; tests/test_text_then_act.py::test_a_refreshed_lanes_squash_is_admitted; tests/test_text_then_act.py::test_a_refresh_merge_combining_two_text_commits_beside_trunks_act_passes
```

  - The `evidence` cell names a test that does not exist yet (003, "Owed to the builder"). The test lands before or with this text.

## Not ruled here, and owing no act

- **LLR-298** changed only a traced cell; see Basis.
- **TC-167** stays unamended: 002's ruling upheld. With LLR-173's sentence a pointer to LLR-302, LLR-173 states no clause TC-167 would owe.

## Aftermath (not taken; the coordinator resumes this adjudication after rebasing the lane)

LLR and TC sit on a rung the declared gate authority releases. All three rows
are MEANING. LLR-245 is blessed as it stands. LLR-173 and TC-173 would be blessed
with the replacement cells above. The sequence:

1. The replacement cells (here and in 003) land byte-exact in a text commit,
   with 003's owed test, after the lane is rebased onto trunk.
2. A fresh ruling on the landed text, on the rebased lane.
3. Then one act commit, changing only `Status`:
   - LLR-302 flips `Drafted` -> `Approved`;
   - LLR-173, LLR-245 and TC-173 are re-attested.

   The test-cases registry enters the act's scope through TC-173's
   re-attestation, so `--approves` names only the registry that holds the
   flip:

```text
python project-trajectory/scripts/intake.py snapshot --approves "docs/requirements/low-level-requirements.toml=WI-806" --reattests LLR-173,LLR-245,TC-173 --verdict docs/reviews/wi-806-text-then-act/<the fresh amendment verdict>.md
```

VERDICT: MEANING rows=3
OUTCOME: RETURN rows=3
