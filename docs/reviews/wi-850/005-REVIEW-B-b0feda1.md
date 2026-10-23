Reviewed: b0feda11394964cb9762c2c3be545888930e6218

**Verified.** Full-lane review of WI-850 (ad67e4b3f..b0feda113, three-dot diff with the brief's exclusions), against the spec `docs/work/active/wi-850/WI-850-child-approved-after-parent.md` (Trust section and Done-when), PROCESS.md and the rubric `docs/rubrics/kit-change-review.md`. HEAD confirmed as b0feda113 before running anything. The failure classes I hunted first, worst first: (1) fail-open, where a commit leaves an approved child under an unapproved parent and is not refused; (2) a false refusal that blocks the sanctioned act flow; (3) silent wrong content in the standing finding.

- **The rule.** `kitlib.spine.parent_first_findings` is one pure rule with one approval pair, `claims_approval`. `acceptance_record._claims_approval` is bound to it by identity, which the test pins. Its edges are SR to SN, LLR to SR, and TC to SR and LLR. IF, DA, undeclared and `-000` ids are not judged. Statuses compare case-insensitively, as `is_approved` and `is_founded` already do.
- **The commit judgement.** It reads the commit-side tree through `git_show` and `tier_rows_from_text`, not `_spine_rows_at`. It refuses a commit-side registry that cannot be read or does not parse, and it refuses a diff git cannot list. A parent side that fails to read counts every status as moved. It can only refuse a tree the standing rule itself flags, apart from those read failures, so it adds no false refusals of its own.
- **Driving the real code.**
  - `check.py --run-steps parent-first` (the hook's batched path, not only `--parent-first`) in a fresh temporary repo with a staged LLR flipped to Approved under a Drafted SR printed `FAIL parent-first the index: LLR-001 (Approved) is approved under SR-001 (Drafted) ...`, exit 1. So the batched step runs whatever the stage.
  - `commit_parent_first_lines` over all 26 lane commits refused none, and all three `LANE_COMMIT_RIDERS` over the lane refused none. The lane's own text-then-act sequence is clean: SR-224's text was answered in ab4b6d8c2 and 97f2e64e5, and the act came alone in cd5292585 (acts.toml seq 154, snapshot copy for SR-224 only).
  - The rider over the 300 trunk commits before the base refused none, in 47 s.
- **Mutations, run on an exported copy of the tree in my scratch area, never in the worktree.**
  - Making `_status_moved` always true reds `test_a_commit_moving_neither_row_passes_over_a_standing_case` and `test_a_parent_side_that_does_not_parse_counts_every_status_as_moved`. The moved filter is pinned.
  - Running the pre-change `test_every_declared_sn_status_leaves_the_enum_floor_silent` against the new code fails with `parent-first: SR-001 (Approved) is approved under SN-001 (Drafted)`. So the SN edge does work end to end through `reg.raw_sns`, even though no committed test pins it (finding 1).
- **Done-when coverage map.**
  1. SR-224's chain is settled: SR-224 is Approved through its own act. `trace.py --strict-integrity` on the reviewed tree reads integrity=0, so the standing LLR-281/TC-291 case is cleared.
  2. Commit refusal at pre-commit for each tier pair: `test_parent_first_git::test_staging_an_approved_child_under_a_drafted_parent_is_refused[4 pairs]`. On each lane commit: `test_a_no_verify_lane_commit_with_a_violation_is_refused_at_the_slot`.
  3. The standing finding: `test_trace_rules::test_an_approved_llr_under_a_drafted_sr_reds_strict_integrity` and `::test_a_drafted_llr_whose_citing_tcs_are_approved_is_an_integrity_finding`. The SN edge is covered only in the pure rule (finding 1).
  4. The skill names its enforcers: SKILL.md and in-lane.md, with the three skill copies byte-identical.
  5. The rows are one change set: SR-245, LLR-357 and LLR-358, TC-396 and TC-397, IF-308, all Drafted. Their combined sitting is owed at the coordinator-cycle checkpoint that follows a clean counted round, not at this tip.
  6. Tests: each pair; Founded on both sides; parent demotion refused; the standing finding.
  7. The review bar is process.
  8. RESYNC_PACK carries an entry anchored at ad67e4b3f. It names the forced migration and both remedies, and lists every changed kit-owned file.
- **Requirement-row sweep.**
  - SR-245 is a labelled derived SR. SR-178, the drift rule, does not demand this rule, so a derived row is the right home. No other SR states approval order, and no registry row or TC evidence cited the retired `llr_status_advisories` or its three deleted tests.
  - K2: no SR cell names a script. "strict integrity" has a precedent at SR row line 274.
  - K3: every new `Implements:` tag names LLR-357 or LLR-358, whose `module` holds that file and whose `code_symbol` lists the function.
- **Counterpart decision for the changed SR-224.** SR-224's Requirement gained the shipped-descriptions clause. I retain LLR-281 and TC-291 unchanged:
  - The new clause is a property of the shipped data, not a mechanism, so LLR-281 (the refusal mechanism) needs no counterpart change.
  - TC-291's (b) arm ("short_descriptions over the kit's own skills returns nothing") and its Expected ("every shipped skill clears it") already verify that clause.
  - SR-224's acceptance criteria are unchanged.
- **Decomposition of SR-245.** I retain both LLRs:
  - LLR-357 is the pure classification plus the standing report (CMP-006).
  - LLR-358 is the two-tree commit judgement and its wiring (CMP-008), with an independent failure surface: git reads, read failures and merge parents.
  - Splitting LLR-358 further, into a staged form and a rider form, would add no independent value, since both call `parent_first_lines`.
- **Consolidation.** `_tree_tiers`, `_parent_statuses` and `_status_moved` sit beside `committed_status_moves` and `_spine_row_sides`. The spec's Trust section deliberately forbids reading through `_spine_rows_at`, which takes a failed read for an absent registry. `_tier_reads` is the carried WI-963 reader, not a new copy. So none of these is a duplicate.

Coverage notes (outside the finding count):
- `staged_parent_first_lines` reads a failed `rev-parse HEAD` as "no HEAD yet". That is reachable only in a damaged repository, and the standing finding at `registry-integrity` still reads the working tree.
- `_parent_statuses` keeps the last row of a duplicated id, while `_declared_rows` keeps the first. A duplicated id is already an integrity finding.
- The commit judgement does not refuse a commit that retargets an approved child's parent reference without moving a status. That is the spec's bound ("where the commit moved either row's status"), and `registry-integrity` catches the resulting standing case on the working tree.

Commands:
- `git rev-parse HEAD` -> `b0feda11394964cb9762c2c3be545888930e6218`
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r1b/wi-850 tests/test_parent_first.py tests/test_parent_first_git.py tests/test_trace_rules.py tests/test_text_then_act.py tests/test_acceptance_record.py` -> `109 passed in 122.24s (0:02:02)` (0 environment-gated skips)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (969 work item(s), 855 done (88%), 34 cancelled, graph acyclic).` exit 0
- `python project-trajectory/scripts/trace.py --strict-integrity`, run on a `git archive` export of b0feda113 in r1b/tree so the worktree is untouched -> `Traceability: SN=31 SR=137 LLR=325 TC=352 orphans=0 integrity=0 ...`
- `check.py --run-steps parent-first` in the r1b/probe/repo1 temporary repo, with a staged violation -> `FAIL parent-first the index: LLR-001 (Approved) is approved under SR-001 (Drafted) ...`, exit 1
- Probe `commit_parent_first_lines` over ad67e4b3f..b0feda113 -> `walked 26 refused 0`. Over ad67e4b3f~300..ad67e4b3f -> `walked 300 refused 0`
- Probe all `LANE_COMMIT_RIDERS` over ad67e4b3f..b0feda113 -> `walked 26 commits x 3 riders`, no refusal
- Mutation: drop `SN=reg.raw_sns` from `integrity_sweep`, then run test_trace_interfaces.py, test_trace_rules.py and test_parent_first.py -> `111 passed` (the mutation survives)
- Mutation: `staged_parent_first_lines` reads HEAD only, then run `test_parent_first_git.py -k merge` -> `1 passed` (the mutation survives)
- Mutation: `_status_moved` returns True, then run test_parent_first_git.py and test_parent_first.py -> `2 failed, 30 passed` (killed)
- The pre-change `test_every_declared_sn_status_leaves_the_enum_floor_silent` against the new code -> `1 failed` with `parent-first: SR-001 (Approved) is approved under SN-001 (Drafted)`. The SN edge works end to end.

- [MINOR] tests/test_trace_rules.py:641 -> The standing finding's SR-to-SN edge has no committed test at the trace level. `integrity_sweep` (project-trajectory/scripts/trace.py:5387) reads the SN tier through a separate reader, `reg.raw_sns`, and a mutation dropping `SN=reg.raw_sns` passes test_trace_interfaces.py, test_trace_rules.py and test_parent_first.py (111 passed). Yet TC-396's Expected claims that each tier pair "produces one named parent-first integrity finding ... and strict integrity fails" (K1: a TC cell must be true against its evidence) -> Add a scaffold test beside the two at :641 and :652: an Approved SR under a Drafted SN in stakeholder-needs, `--strict-integrity` exits 1 naming `SR-001 (Approved) is approved under SN-001 (Drafted)`, and list it in TC-396's evidence -> @owner
- [MINOR] tests/test_parent_first_git.py:158 -> `test_a_merge_assembling_a_violation_from_two_sides_is_refused` does not tell a merge-aware judgement from a HEAD-only one. With `staged_parent_first_lines` mutated to read HEAD alone (project-trajectory/scripts/acceptance_record.py:2362), the test still passes, because the merged LLR's status moved against HEAD anyway. The MERGE_HEAD base is observable only when HEAD itself carries the pair unchanged, so the test's docstring overstates what it pins. That weakens TC-397's "merge parents" claim (K1) -> Add a case where HEAD already holds the approved-child/Drafted-parent pair and the merged side does not, asserting refusal, or narrow the docstring and TC-397's method to what the test discriminates -> @owner
- [MINOR] project-trajectory/scripts/acceptance_record.py:318 -> The `_spine_rows_at` docstring (:318) and the `_tier_reads` docstring (:325-331) name `_snapshot_copy_rows` as "the reader that refuses one", and `_tier_reads` carries an `under` parameter "(the snapshot's copies)". No such function exists in this tree, and no caller passes `under`. Until the held WI-963 lands, the docstrings describe code that does not exist, and the parameter is dead. That misleads the next reader, human or agent (no rubric anchor; CLAUDE.md "readable for humans and agents"). The coordinator kept this deliberately, to ease WI-963's rebase -> Either trim the dangling sentence and the unused parameter here and let WI-963 add them back, or record in WI-963's spec that its rebase owns making them true -> @owner

VERDICT: APPROVE findings=3
