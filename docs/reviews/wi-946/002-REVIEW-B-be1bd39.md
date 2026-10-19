Reviewed: be1bd397ca161dbf138e1e3a0027b8d0a889ff42

Verified. I read the whole diff (e57e647d2...be1bd397c, with the brief's excludes) against the WI-946 spec, its specref (WI-917 Trust) and the registry rows it cites (SR-209, LLR-246, LLR-248, TC-242, IF-065). I hunted the worst failure classes first: fail-open at the audit, `check-lane` or the slot, and silent wrong content.

What I found right:
- Trunk is bound once (`bind_trunk`, through `agent_common.trunk_name`), and the launcher's own reader is gone.
- `pre_leg` refuses a snapshot without the bound ref, then compares the checkout.
- `audit` judges trunk, then the archive, then the lanes, then the checkout last, so a refused commit is named first (in-process `test_the_audit_names_a_refused_commit_before_the_checkout`).
- `judge_descent` folds the trunk and archive rules into one function. Present before and gone after, or not an ancestor, is a stop naming the pre-leg tip. `merge-base` is read checked, so exit 128 is a stop. Absent before is judged over the commits no pre-leg branch reaches.
- The log line prints the bound trunk's tips from the two snapshots. Both always hold the trunk: `pre_leg` and `judge_descent` refuse otherwise.
- `agent_common.loop_claimed` keeps the slot's old reading exactly: the same grep, the newest claim-subject match first, the same trailer parse. It adds the `%H` record check and returns `(None, why)` on a failed or unparseable read.
- `_loop_window` returns the "nothing was merged" refusal on that answer, so `_loop_trailer_refusal` and `_held_status_refusal` both refuse. The launcher raises AuditStop on it.
- `Implements: SR-209, LLR-248` on `loop_claimed` matches LLR-248's module and code_symbol (K3).
- Spine rows (K1, K3):
  - LLR-248's and TC-242's amended cells keep the approved text verbatim and add only the unreadable-claim sentence the spec grants. That sentence is true to the code. No Status flips.
  - IF-065's data names `loop_claimed`, and `scripts/integrate` is already a requestor.
  - SR-209 is unchanged, and the new sentences do not contradict its acceptance.
- Counterpart decision: LLR-246, the held-status rung under SR-208, is retained unamended. The rung reaches the claim only through `_loop_window`. LLR-248's new sentence is slot-wide ("at the merge slot"). LLR-246 states no failure rule that the change contradicts.
- The RESYNC entry names the two shipped files and forces no migration. The path convention matches its neighbours.
- The skill copies are byte-identical to the kit source.

Done-when coverage:
- Checkout left off trunk: `test_a_leg_that_leaves_the_primary_checkout_off_trunk_stops_the_run`, plus the in-process `test_the_checkout_must_stay_on_the_bound_trunk` (4 states).
- The bind: `test_the_run_binds_trunk_once_and_logs_it` and `test_the_bind_reads_trunk_once_and_logs_it`.
- A refusing reader: `test_a_refusing_trunk_reader_stops_the_run_before_any_leg` and `test_a_value_error_from_the_trunk_reader_stops_the_run`.
- A name no local branch holds (pin): `test_a_bound_name_no_local_branch_holds_stops_before_the_leg` and `test_a_snapshot_without_the_bound_trunk_stops_before_the_leg`.
- `check-lane` from the lane's worktree: `test_check_lane_from_the_lanes_own_worktree_judges_from_the_kits_trunk`, plus the two in-process cannot-judge tests.
- Archive rewind, reset and delete: `test_a_leg_that_rewinds_resets_or_deletes_archive_lanes_stops_the_run` x3, plus the in-process `test_the_archive_must_descend_from_its_pre_leg_tip`.
- Archive pins: `test_a_marked_archive_commit_on_an_existing_archive_runs_the_next_leg`, the created-archive cases and `test_a_failed_archive_descent_read_stops_the_run_naming_it`.
- Claim-read pins: the `claim` cases in the failed-read tests and `test_an_unparseable_claim_record_stops_the_audit`.
- Log line: the real-git and in-process log-line tests.
- Slot, unreadable claim log: `test_an_unreadable_claim_log_is_refused_by_the_trailer_rung_naming_the_read` (through `integrate_one`; HEAD unchanged) and `..._by_the_held_status_rung`.
- Unparseable record: `test_an_unparseable_claim_record_is_unreadable_never_unclaimed`.
- Readable-log pins: `test_the_claim_reader_answers_as_before_on_a_readable_log` (6 cases).
- One reader: `test_the_slot_and_the_launcher_share_one_claim_reader`.

Red-before. I ran the new test files against the base code: `git archive e57e647d2` into my scratch dir, with the lane's four test files copied over it. All 7 regression tests fail on the pre-fix code at their behavioural assertions, not on imports:
- the checkout-off-trunk case (`code == 3` fails: the run went on);
- the three archive cases;
- `check-lane` from the lane worktree (passed before);
- both slot unreadable-claim rungs (`refusal` was None, so the old slot passed the lane).

Real-path probe. I drove the shipped `check-lane` CLI on a scratch repo: a loop-claimed lane with one unmarked commit, and a linked lane worktree.
- Primary on main, `--repo` the lane worktree: exit 3, refused, naming the commit.
- Primary detached, `--repo` the primary: exit 3, cannot judge (refs/heads/HEAD).
- Primary detached, `--repo` the lane worktree: exit 0, "passes (window 0)". This is the finding below.

Commands:
- `git rev-parse HEAD` -> be1bd397ca161dbf138e1e3a0027b8d0a889ff42
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r1-946-opus/wi-946 tests/test_loop_provenance.py tests/test_overnight_legs.py tests/test_overnight_legs_git.py` -> 127 passed, 1 skipped in 336.09s (posix-shell gate)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> check_trajectory: clean (946 work item(s), 832 done (88%), 30 cancelled, graph acyclic). The five overlap WARNs are about other rows and are pre-existing.
- Red-before run of the 7 regression tests, on a `git archive` of e57e647d2 with the lane's test files -> 7 failed in 36.72s, each at its behavioural assertion
- Scratch-repo probe of `overnight_legs.py check-lane wi-1 --repo <lane worktree>` with the primary checkout detached -> "check-lane wi-1: passes (window 0)", exit 0

Findings:

- [MINOR] scripts/coordinator/overnight_legs.py:440 -> `check-lane` with `--repo` at a lane worktree while the primary checkout is detached reads trunk through `agent_common.trunk_name`'s middle fallback. That fallback is `git branch --show-current` of the `--repo` checkout, which is the lane itself. So it judges the lane from its own tip: an empty range. It prints "passes (window 0)", exit 0, for a lane holding an unmarked commit (reproduced on a scratch repo above). The spec's Trust lists only two failed shapes ("raises" or "no local branch holds"). The docstring's bound (overnight_legs.py:91, "the branch the primary checkout is on at that moment") misstates this case. It is off procedure: a detached primary plus a non-default `--repo`. -> Either have `check_lane` answer "cannot judge" when the trunk name equals the judged branch, or widen the docstring bound and the Trust text to name this fallback. Why it can't be unrepresentable here: the structural fix is WI-925's declared trunk name, which deletes the fallback chain. That is outside this row's scope, so any guard here is interim. (K1, B1) -> @owner

Coverage-extension note (no severity): with the primary detached and `--repo` the primary, the run and `check-lane` both fail closed, on refs/heads/HEAD.

VERDICT: APPROVE findings=1
