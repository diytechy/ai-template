Reviewed: d2004bf62b54cf1f84efafa8b1f40e1f25d0d90d

Verified. `git rev-parse HEAD` in the lane worktree printed the reviewed commit. I read the full-lane diff (7c59c67d1...d2004bf62, with the brief's exclusions), the WI-918 spec, decisions D-015 and D-017 (coordinator-2026-10-14) and D-005 C4 (coordinator-2026-10-18), and the rubric docs/rubrics/kit-change-review.md. Worst failure classes for this change: a fail-open (a commit that is not a genuine re-claim closes the trailer window, or the window stays closed after a loop writer marks the lane again), and the slot and the launcher reading the same lane differently. I hunted these first.

- `provenance._reclaim` denies by default, and all four conditions hold at the shipped code: one parent, the parent's tree equal to the commit's tree (looked up in-range or in the `--boundary` map), the exact subject for this branch, and no `Loop-Session` trailer. A malformed trailer (empty value, or a value outside the session grammar) and a lower-case trailer key both read as a trailer through `_last_loop_value`, so neither counts as a re-claim. `loop_lane_window` keeps `None` for a lane that was never marked and returns a list (possibly empty) otherwise, so `_held_status_refusal`'s `window is None` test reads as before.
- `git log --boundary --format=%m...` on git 2.49 prints `-` for boundary commits and `>` for range commits, which is what both parsers expect. The integrate parser and the launcher's strict `lane_records` hand the reader the same records.
- I mutated the shipped code paths in a scratch export of the tip and re-ran the re-claim tests. Each mutation was caught:
  - dropping the one-parent test: the merge case fails;
  - dropping the tree test: the slot test and the launcher's tree case fail;
  - dropping the no-trailer test: the trailer test fails;
  - matching any branch's subject: the other-branch test fails;
  - stopping a loop writer from re-opening the window: the re-open test fails;
  - dropping integrate's boundary map: 6 slot tests fail;
  - dropping the launcher's boundary map: the `LANE_CASES` re-claim case fails.
- Red before the fix: I put the base (7c59c67d1) `provenance.py`, `integrate.py` and `overnight_legs.py` back, plus only a `reclaim_subject` shim so the tests could reach their semantics. 8 of the 10 re-claim tests failed on behaviour, including `test_check_lane_reads_a_reclaim_as_the_merge_slot_does[after-the-reclaim]`. The 2 that passed are the before-the-reclaim control and the composer pin, which are expected to pass.
- Other checks:
  - The three skill copies are byte-identical.
  - The new `Implements: SR-209, LLR-248` tags name LLR-248, whose `module` holds provenance.py, and whose `code_symbol` gains `reclaim_subject/_reclaim` (K3). `code_symbol` is a pointer cell (acceptance_record.py:383-384), so editing it on an Approved row moves no meaning cell.
  - The RESYNC entry names the overwritten kit files and the caller-visible signature change.
  - `test_module_size_ratchet.py` passes at the new stamp (integrate.py 1554).

Done-when map:
- (1) Deliverables in targets, citing rulings: covered. provenance.py cites revision 36, D-015 and D-017; integrate.py and the skill cite D-017; overnight_legs.py cites D-005 C4.
- (2a) Claimed under the marker, then re-claimed: test_a_reclaim_closes_a_marked_claims_window_for_the_commits_after_it.
- (2b) Marked by a sitting's telemetry commit: test_a_lane_marked_by_a_sitting_is_judged_from_its_telemetry_and_a_reclaim_clears_it.
- (2c) Trailer, malformed trailer, another branch: test_a_reclaim_carrying_a_trailer_or_naming_another_branch_is_not_one.
- (2d) Changed tree, two parents: test_a_reclaim_subject_on_a_commit_that_changes_the_tree_or_merges_is_refused_naming_it.
- (2e) A loop writer re-opens the window: test_a_marked_loop_writer_commit_after_a_reclaim_reopens_the_window.
- (2f) A lane never marked; the held-status rung judges the lane whole: test_a_lane_never_marked_stays_a_persons_and_the_held_status_rung_judges_a_reclaimed_lane_whole.
- (2g) WI-917's literal subject: test_a_reclaim_written_literally_by_wi_917s_recipe_is_read_as_a_composed_one.
- (3) The launcher: test_check_lane_reads_a_reclaim_as_the_merge_slot_does, both orders. It also asserts the slot agrees on the same repository.
- (4) Trace rows: UNCOVERED at this tip. SR-209's acceptance, LLR-248's `detail`, TC-242 and IF-194's `data`/`rationale` are not yet amended; LLR-248's detail still states the pre-change window. The coordinator-cycle procedure defers spine authoring to the checkpoint that follows a counted round with no BLOCKER or MAJOR (plan row P7), so I record this as the checkpoint's owed work, not as a finding of this round. The checkpoint gate must see these rows.
- (5) RESYNC entry: covered, project-trajectory/RESYNC_PACK.md.
- (6) Skill copies synced: covered (byte-identical).
- (7) Plan gate: the plan, critique 1 and the pass record are present under docs/plans/WI-918/.
- (8) Landing bar: only the round's declared slice was run here (below); the smoke tier and the full suite are not this round's.

A note outside the finding lines: `trace.py --strict-integrity` wrote its gitignored report, docs/test/report.md, into the lane worktree when I ran it as the brief directs. It is ignored, and `git status` is otherwise clean.

Commands:
- `git rev-parse HEAD` -> d2004bf62b54cf1f84efafa8b1f40e1f25d0d90d
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r1-opus/wi-918 tests/test_loop_provenance.py tests/test_overnight_legs.py tests/test_overnight_legs_git.py` -> `91 passed, 1 skipped in 105.61s` (the skip is the posix-shell environment gate)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (944 work item(s), 828 done (88%), 30 cancelled, graph acyclic).`
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=131 LLR=304 TC=318 orphans=0 integrity=0 ... interface-findings=0 ac-advisories=1 paraphrase-advisories=3.`
- `python -m pytest -q tests/test_module_size_ratchet.py` -> `4 passed in 1.53s`
- Mutation runs over a `git archive` export of the tip (r1-opus/tools/mutate.py, `-k "reclaim or re_claim or lane_rule or unparseable"`), with these results:
  - M1-two-parents: 1 failed
  - M2-tree: 2 failed
  - M3-trailer: 1 failed
  - M4-branch: 1 failed
  - M6-no-reopen: 1 failed
  - M7-integ-boundary: 6 failed
  - M8-ol-boundary: 1 failed
- Pre-fix run (base provenance/integrate/overnight_legs plus a `reclaim_subject` shim, `-k reclaim`) -> `8 failed, 2 passed`

- [MINOR] project-trajectory/scripts/kitlib/provenance.py:54 -> for clarity (K1, IF-194 contract text): "A marked process cannot write one through porcelain: the floor refuses its commit without the trailer" is stated without a condition. The same narrative says at line 26 that hooks are opt-in per checkout, and the merge slot, which the module also calls the floor, does NOT refuse an unmarked re-claim: it closes the window on it. So the guarantee holds only where the commit-msg hook is installed, as it is here through the repository's core.hooksPath. -> Qualify the sentence: "where the commit-msg hook runs, a marked process cannot write one through porcelain ...", and name the hook rather than "the floor" there. -> @owner

VERDICT: APPROVE findings=1
