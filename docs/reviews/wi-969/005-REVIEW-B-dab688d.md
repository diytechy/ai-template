Reviewed: dab688d602621cb65a69491306b67e442a49113e

Independent full-lane review of WI-969 (range 254e609c58d473d14b23600668dc9ef73df4060d...dab688d602621cb65a69491306b67e442a49113e, the brief's exclusions applied), rubric docs/rubrics/kit-change-review.md.

## Verified

Failure classes hunted first, worst first: (1) fail-open, meaning a record that no close validated reaches trunk and the sweep re-points dependents from it; (2) the supported close refused, which is sitting 016's class: a real close_adjudication refused at the slot or the hook; (3) silent wrong content in the mint's lineage join; (4) the tightened fence grammar refusing sections already on trunk.

- **Close.** `handback._archive_one_adjudication_row` parses the section once. It validates through `adoption_record.validate_at(wt, "HEAD", ...)` before any move. Under a multi-row close nothing commits between validation and `_loop_commit`, so the lane HEAD really is the closing commit's parent. The record goes into the same rewrite that clears `specref`. A consolidation verdict refuses an adoption before its first write. A handback-form or spot-check title refuses through `disposed_id`.
- **Commit rule (`kitlib.adoption.record_change` with `adoption_record._spec_refusal`).** I traced each branch of the table by hand:
  - a record removed, changed, or written outside the close: refused;
  - a carried record whose request changed: refused;
  - a requesting move into complete/ with no record: refused;
  - a merge: judged only on paths that differ from every parent.
  The close test is `kitlib.verdict.mechanical_close`. Without the oracle it reads exactly as before, so the peel is unchanged. With the oracle it admits an M entry outside docs/work only when `spec_move.exact_relink` accepts it.
- **Sitting 016's FIX regression test fails on the pre-fix code.** I monkeypatched `mechanical_close` to drop the oracle, which is the pre-fix close test, and ran `test_a_real_close_relinking_a_file_outside_docs_work_passes_the_rider_and_the_squash_hook`: it FAILS. The control test, `test_the_closes_own_commit_passes`, passes.
- **Sweep.** `_merged_dispositions` reads no git history and no state of the adopted row. It refuses each request/record mismatch and an unreadable merged spec. Recorded pairs join `_apply_supersedes` beside the drafts.
- **Mint.** `_standing_successors` resolves title identity and lineage together, and refuses a mismatch before any write. `_mint_scope` takes the whole registry directory, so a re-point-only mint stays inside its scope.
- **Fence grammar against trunk.** My own scan of every tracked docs/**.md file carrying `\n## Dispositions` (68 files) found zero fence refusals. A strict `_spec_at` read of all 967 specs under both spec roots raised nothing.
- **Readers left alone.** `agent_loop.dispositions_drafted` and `integrate._verdict_owed` still read drafts only: an adoption-only section owes no review, and a malformed one stays review-owed.
- **Implements tags (K3).** The new and changed tags name LLRs whose `module` holds the file and whose `code_symbol` lists the function.
- **No approved-row Status flips.**
- **Spine Done-when items not yet met at this tip.** These are owed at the checkpoint that follows this counted round, per the coordinator-cycle skill §3, so they are not findings:
  - SR-148, LLR-153, LLR-161, LLR-312, TC-147, TC-156 and TC-254 carry amended text but have not been re-sat;
  - LLR-335, LLR-345, TC-360 and TC-383 are Drafted;
  - the diff carries no act rows, so the lane's acts 113 to 117 do not reach trunk.

Requirement/interface counterparts. Each changed side is named with its counterpart and my decision:
- **SR-148 AC (amended)** to its parent SN refs: retain. The need, "next work derives from tracked records", is unchanged, and an adoption is a form of the existing successor exit.
- **SR-148 AC** to its child rows:
  - LLR-161: carried.
  - LLR-335 and LLR-345: carried (new rows).
  - TC-147, TC-156 and TC-254: partly carried. Each has `verifies` +SR-148. TC-254's method is carried. TC-147's and TC-156's `expected` cells are not carried (finding below).
- **LLR-153 detail (amended)** to TC-147: method not carried (finding below).
- **LLR-161 detail** to TC-156: method carried.
- **LLR-312 detail** to TC-254: method and evidence carried.
- **LLR-302 code_symbol** (+`_with_text_then_act_remedy`) to TC-173: retain. The slot refusal for text then act is unchanged; only the remedy text is now scoped to the rider that refused.
- **IF-175 data and requestors** to the verdict.py contract docstring: carried. To its TCs: retain, since the peel is characterized unchanged by `test_the_peel_still_refuses_a_close_whose_relink_leaves_docs_work`.
- **IF-294** to the kitlib/adoption contract docstring: not carried (finding below). TC-360 cites IF-294.
- **IF-303 and IF-304** to the adoption_record docstrings: carried. TC-383 cites both.
- **Decomposition of SR-148's new obligation:**
  - LLR-335's independent decision is what a valid adoption is, plus how its record is produced at the close and trusted by the sweep. TC-360 verifies it.
  - LLR-345's independent decision is which commits may change that record, including the relink-admitting close test. TC-383 verifies it.
  - Splitting LLR-335 further, into parser, close and sweep rows, would restate one request/record contract that all three already consume through kitlib.adoption, so it adds no independent verification purpose. LLR-335's last sentence, however, already duplicates LLR-345 (finding below).

Done-when coverage:
- **Adoption discharges the successor obligation; close records it; sweep re-points and mints nothing; neither-nor still refused by both:** test_handback.py::test_an_adoption_of_a_superseding_row_closes_and_writes_the_record, test_intake.py::test_a_recorded_adoption_re_points_a_dependents_needs, and the existing empty-section refusals.
- **OI-73 scope kept:** the same tests, plus the prompt text.
- **Close refusals:**
  - missing, closed, unreadable or non-superseding row: test_handback.py::test_an_adoption_that_is_not_accepted_refuses_the_close;
  - untokened title, repeated adoption, consolidation verdict: their named tests;
  - draft beside an adoption: test_a_drafted_successor_beside_an_adoption_still_mints.
- **Commit check, every listed case:** test_adoption_record.py, as cited in TC-383.
- **Sweep:**
  - late dependent and full set: test_a_replay_re_points_a_late_dependent_to_the_full_successor_set;
  - shallow clone: test_a_shallow_clone_sweeps_a_recorded_adoption;
  - mismatches and unreadable spec: their named tests;
  - "still does so after its successor completes": weakly covered (finding below).
- **Parser reproduction, at the close and the sweep, for an adoption and a draft:** covered.
- **No trunk section fails the grammar:** test_disposition_adoption.py::test_every_dispositions_section_in_the_repository_passes_the_fence_grammar, plus my scan.
- **RESYNC entry names the three tightenings:** present.
- **Spine sitting:** owed at the checkpoint (see above).
- **Bar on the landing tip:** smoke not run (the brief forbids it). check_trajectory --strict is clean, and trace --strict-integrity exits 0.

Coverage-extension notes (inputs outside the declared set, all of which fail closed):
- A disposition titled in the legacy "handed back" form cannot adopt: it has no event token, so the close refuses.
- A non-adjudication spec whose body carries a `## Dispositions` heading with a malformed section is refused by the record step when it moves into complete/. No such spec exists on trunk today.
- A lane rebased onto a trunk where its adopted successor has since completed is refused at the squash hook. The spec states this ("checked again on its new parent").

## Commands

- `git rev-parse HEAD` (wi-969 worktree) -> dab688d602621cb65a69491306b67e442a49113e
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r2b/wi-969 tests/test_disposition_adoption.py tests/test_adoption_record.py tests/test_intake.py tests/test_handback.py` -> `261 passed in 731.78s (0:12:11)`; 0 skips from the posix-shell gate
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (966 work item(s), 850 done (88%), 34 cancelled, graph acyclic).` exit 0
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=134 LLR=312 TC=338 orphans=0 integrity=0 ... interfaces=251 interface-findings=0 ...` exit 0; worktree still clean afterwards
- Pre-fix probe: the two tests above under a plugin that strips `relinked` from `kitlib.verdict.mechanical_close` -> `1 failed, 1 passed` (the FIX regression test red, the control green)
- Fence-grammar scan over every tracked docs/**.md carrying `## Dispositions` through `intake.parse_disposition_section` -> `files 68 fence-refused 0`
- Strict `_spec_at` read of every spec `adoption_record._spec_paths(HEAD)` lists -> `specs 967 unreadable 0`

## Findings

- [MINOR] docs/requirements/interfaces.toml:2718 -> IF-294's `data` names `parse_disposition_section`, which is intake's function (a requestor), not one of the owner's. kitlib/adoption actually provides `parse_block`, `disposed_id`, `row_refusal`, `record_ids` and `record_change`, as its own Contract IF-294 docstring states. So the row and the owner's contract disagree about the seam (K1) -> name `parse_block(data, at)` in place of `parse_disposition_section` in IF-294's `data` -> @owner
- [MINOR] docs/requirements/interfaces.toml:2713 -> IF-294, IF-303 (line 2723) and IF-304 (line 2733) carry no `status` cell. Every other one of the 251 interface rows carries `status = "Drafted"`, and registries/interfaces.template.toml does not mark `status` OPTIONAL (it marks component, carried_by and the boundary cells OPTIONAL). The three new seams therefore have no stated maturity for the sitting to approve (K1) -> add `status = "Drafted"` to the three rows -> @owner
- [MINOR] docs/requirements/low-level-requirements.toml:3565 -> for clarity: LLR-345's detail limits the requesting-move rule to "docs/work/complete". The code (`adoption_record._SPEC_PATH` and `_in_complete`) also refuses a requesting move into docs/archive/work/complete without a record, and judges archive-root records the same way, so the row is narrower than the rule it states (K1) -> state "a complete folder of either spec root (docs/work or docs/archive/work)" -> @owner
- [MINOR] docs/requirements/low-level-requirements.toml:3553 -> for clarity: LLR-335's detail ends "A record changes only in the close that created it or remains unchanged with its request". That is LLR-345's admission rule, so the rule now has two homes that can drift apart (sweep for overlap) -> drop the sentence from LLR-335 and leave it to LLR-345 -> @owner
- [MINOR] docs/requirements/system-requirements.toml:642 -> for clarity: SR-148's amended AC reads "names an already-open item that supersedes it as its successor". There "it" binds to the unresolved handback, but the rule the close enforces is that the item supersedes the closed work item. The phrase "resolves the record" earlier in the same clause also now collides with the adoption "record" (K1, K2-compliant wording) -> reword to "names an already-open item that supersedes the closed work item as that item's successor" -> @owner
- [MINOR] docs/test/test-cases.toml:1458 -> TC-147 (and TC-156 at line 1557) gained SR-148 in `verifies`, and TC-147 gained evidence entries for the standing-successor lineage, the title-lineage refusal and the adoption re-point. Yet TC-147's `expected` still reads "Satisfies SR-174 ... via the LLR-153 detail contract", TC-156's reads "Satisfies SR-144 ...", and TC-147's Method describes none of the new LLR-153 behaviour its evidence now proves. The verification text no longer says what the row verifies (K1) -> at the checkpoint, amend TC-147's Method with the LLR-153 lineage clauses and both rows' `expected` to name SR-148 through their authority -> @owner
- [MINOR] tests/test_intake.py:1679 -> `test_a_consumed_adoption_replays_after_its_successor_completes` does not witness the Done-when's "still does so after its successor completes". Its only dependent, WI-021, was re-pointed by the first sweep before WI-020 completed. So an implementation that silently drops a recorded adoption whose successor is no longer open would still exit 0 with WI-021 unchanged, and the test would pass (confirmed by reading its assertions) -> after WI-020 moves to complete/, file a new dependent that needs WI-005, then assert the bare sweep re-points it to WI-020 -> @owner
- [MINOR] project-trajectory/scripts/adoption_record.py:275 -> `_spec_paths` repeats in intent `acceptance_record._tree_specs` (`{WI id: path}` across docs/work and docs/archive/work, for a rev or the index), and this module already imports from acceptance_record. Within this new module, `tree_specs`/`_tree_text` (lines 106 and 130) and `_spec_paths`/`_spec_at` (lines 275 and 364) are also two separate listing-plus-strict-UTF-8-read pairs over the same trees (PROCESS.md §3, consolidate) -> keep one tree-spec reader, extending `_tree_specs` to report duplicate ids, and build both the validation listing and the commit-rule listing from it -> @owner
- [MINOR] project-trajectory/scripts/adoption_record.py:434 -> `_squash_walk`, and the SQUASH_MSG/`merge-base --is-ancestor` admission in `staged_adoption_record_lines`, repeat `text_then_act.lane_commit_walk` and `_squash_lines` (a third copy beside plan_gate's). The stated reason is an import cycle, and that cycle exists only because `LANE_COMMIT_RIDERS` lives in text_then_act and imports this module (PROCESS.md §3, consolidate) -> move the rider tuple to its one consumer (integrate) or to a leaf module, so adoption_record can call the one lane-commit walk -> @owner

VERDICT: APPROVE findings=9
