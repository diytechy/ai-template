Reviewed: 897ea6ef65e6367e9bc4a6f906eb523dd223a2d7

Verified: The checkout is the reviewed commit. I hunted these failure classes first: fail-open (a commit that is not a re-claim closing the window), silent wrong content (the slot and `check-lane` reading a lane differently), and regressions in the held-status rung and the person's-lane `None` contract. I drove the real code paths (`integrate._loop_trailer_refusal`, `integrate._loop_window`, `integrate._held_status_refusal`, `overnight_legs.lane_refusal`) on real git repositories, using the lane's own fixtures plus probes of my own in a scratch copy:
- A re-claim whose parent is the trunk tip, a boundary commit, is read correctly through `--boundary`.
- Trunk advancing after the re-claim, and an unmarked merge refresh after it, both leave the window closed.
- A second re-claim and a re-claim with a body and an unrelated trailer behave as specified.
- A re-claim in a never-marked lane followed by a loop-writer mark leaves the later commits judged.

`_reclaim` denies by default: it requires one parent, the parent's tree in the map, a tree equal to the parent's, the exact subject and no `Loop-Session` trailer.

Red-before: I ran the new tests against the base versions of `kitlib/provenance.py`, `integrate.py` and `overnight_legs.py`, adding only a `reclaim_subject` stub so the reader's behaviour is what gets tested. All 7 new provenance tests and `check-lane[after-the-reclaim]` fail there, each on its genuine re-claim control ("commit 'reclaim: wi-401 (attended)' carries no Loop-Session trailer"). The deny-side checks pass both before and after, as they should.

Done-when map:
- Claimed lane, re-claim, then work: `test_a_reclaim_closes_a_marked_claims_window_for_the_commits_after_it`.
- Lane marked by telemetry, then re-claimed: `test_a_lane_marked_by_a_sitting_is_judged_from_its_telemetry_and_a_reclaim_clears_it`.
- Trailer or other-branch subject: `test_a_reclaim_carrying_a_trailer_or_naming_another_branch_is_not_one`.
- Changed tree or two parents: `test_a_reclaim_subject_on_a_commit_that_changes_the_tree_or_merges_is_refused_naming_it`.
- Re-open: `test_a_marked_loop_writer_commit_after_a_reclaim_reopens_the_window`.
- Never marked, and held-status judged whole: `test_a_lane_never_marked_stays_a_persons_and_the_held_status_rung_judges_a_reclaimed_lane_whole`.
- Literal WI-917 subject: `test_a_reclaim_written_literally_by_wi_917s_recipe_is_read_as_a_composed_one`.
- Launcher: `tests/test_overnight_legs_git.py::test_check_lane_reads_a_reclaim_as_the_merge_slot_does`, plus the `LANE_CASES` re-claim cases.
- Spine rows: SR-209 acceptance, LLR-248, TC-242 and IF-194 are amended, with no Status flip. K2 holds: the SR cell names no carrier. K3 holds: `reclaim_subject` and `_reclaim` carry `Implements: SR-209, LLR-248` and sit in LLR-248's `code_symbol`, whose `module` includes `provenance.py`.
- The act: not independently checked, because the act record sits in the excluded docs/decisions path. It is left to the slot's text-then-act rung.
- RESYNC: exactly one entry, with no migration.
- Skill copies: `.claude/` and `.agents/` are byte-identical to the kit source.
- Plan gate: `pass.toml` is present.
- Bar: `check_trajectory --strict` is clean and `trace.py --strict` exits 0. The smoke tier was not run, per the round facts.
- Size ratchet: the `integrate.py` 1554 bump passes `test_module_size_ratchet.py`.

Not a finding: a marked process cannot forge a re-claim through porcelain, because `core.hooksPath` points at `.githooks/commit-msg` in this repo.

Commands:
- `git rev-parse HEAD` -> 897ea6ef65e6367e9bc4a6f906eb523dd223a2d7
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../gate-opus/wi-918 tests/test_loop_provenance.py tests/test_overnight_legs.py tests/test_overnight_legs_git.py` -> 91 passed, 1 skipped in 102.14s (the skip is the posix-shell gate)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> check_trajectory: clean (945 work item(s), 830 done (88%), 30 cancelled, graph acyclic).
- `python project-trajectory/scripts/trace.py --strict-integrity` -> Traceability: SN=31 SR=131 LLR=304 TC=318 orphans=0 integrity=0 ... interface-findings=0 ac-advisories=1 paraphrase-advisories=3.
- `python project-trajectory/scripts/trace.py --strict` -> exit=0, the same summary line
- the same three test files in a pre-fix copy (base provenance/integrate/overnight_legs, plus a `reclaim_subject` stub), `-k reclaim` -> 8 failed, 2 passed (every new re-claim test red, at its genuine-re-claim control)
- `python -m pytest tests/test_zz_probe.py` (a scratch copy; the boundary parent, trunk advance plus merge refresh, a body plus Signed-off-by, closed-then-marked, a double re-claim) -> 4 passed
- `python -m pytest tests/test_zz_probe.py -k parallel` (a scratch copy) -> 1 passed, printing `REFUSAL: None` for the side-line case below
- `python -m pytest tests/test_module_size_ratchet.py` -> 4 passed in 1.57s

Findings:
- [MINOR] project-trajectory/scripts/kitlib/provenance.py:299 -> the window's state is advanced in `--topo-order` position, not along ancestry. In a loop lane holding a lane-local side line merged back in, an unmarked commit on the side line that does not descend from the re-claim is listed after the re-claim and exempted. Confirmed by running it: telemetry commit C0; side line `W` (unmarked, parent C0); the re-claim on C0; `merge --no-ff side`. The order prints `telemetry, reclaim, unmarked side commit, join`, and `_loop_trailer_refusal` returns None, where the code before this change refused W. This is reachable only by merging a divergent lane-local line, which the kit's rebase/merge-refresh lanes do not produce, so MINOR (K1/B1) -> derive each record's window state from its parents' states (open when any parent's state is open, with boundary parents open iff the loop claimed the lane, and a re-claim closing only its own descendants) instead of from list position. This is a construction change, not an added guard: it makes "exempted but not after the re-claim" unrepresentable -> @owner
- [MINOR] docs/requirements/system-requirements.toml:1460 -> for clarity: SR-209's rationale still says the merge floor "judges every commit of a loop lane, a person's included" and gives no reason for the exception the amended acceptance now carries: an attended re-claim ends the loop's window for the commits after it. The row now reads as rationale and acceptance disagreeing (K1) -> at the row's next amendment through its authority (the spec granted this lane the acceptance cell only, K3), add one rationale sentence: after the attended coordinator's re-claim the lane is a person's again, and the held-status rule still judges it whole -> @owner
- [MINOR] docs/requirements/interfaces.toml:1910 -> for clarity: IF-194's `data` cell now spells three symbols in brace-expansion shorthand (`loop_{trailer_refusal,writer_commit,lane_window}`). A grep for `loop_lane_window` or `loop_writer_commit`, the contract this lane changes, no longer finds the row. No length limit forces this, since other `data` cells in the file reach 791 characters (K3, back-links) -> spell each name out, as the cell did before -> @owner

VERDICT: APPROVE findings=3
