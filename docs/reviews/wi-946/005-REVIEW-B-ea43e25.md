Reviewed: ea43e256002f121fe0f8d20a2d466e711a454b9d

**Verified.** Full-lane review in the convergence stance. I read no earlier verdict, no decisions record and no lane commit message. I confirmed `git rev-parse HEAD` = ea43e256002f121fe0f8d20a2d466e711a454b9d before running anything.

The failure classes this change admits, worst first:
- (1) fail-open: the after-leg audit or `check-lane` passing a leg it should stop, by judging the wrong trunk, missing an archive rewind or deletion, or reading an unreadable claim as unclaimed;
- (2) fail-open at the merge slot: an unreadable claim log reading as a person's lane;
- (3) a regression in the readable-claim reading.

I hunted them in that order.

**Red before the fix.** I extracted the reviewed tree to a scratch directory outside the repo, put back the pre-fix `overnight_legs.py`, `agent_common.py` and `integrate.py` from cab3b2a76, and ran the new tests there. Each behavioural regression test fails on the pre-fix code for the behavioural reason, not only because an interface changed:
- the trailer rung and the held-status rung with an unreadable claim log return `None` (`assert (None)`, test_loop_provenance.py:743 and :756);
- the checkout-left-off-trunk run ends `0 == 3`;
- the archive rewind, the unrelated reset and the deletion each end `0 == 3`;
- `check-lane` from the lane's own worktree ends `0 == 3`.

The pins pass on both sides, as marked: the marked archive commit, the log line, and the claim-read cases in check-lane and the audit.

**Real code paths.** I drove `agent_common.loop_claimed` on a real repository with a missing object. It answers `(None, "git log --first-parent ... failed (exit 128): error: Could not read ...")`, so an unreadable answer names the read and is never unclaimed.

**Code reading.** Every launcher reading of trunk now uses the bound ref:
- the trunk rule (`judge_descent`, may_create=False);
- the exclusion from the lane loop;
- the lane base `post[trunk_ref]`;
- the log line `pre[trunk_ref]`/`post[trunk_ref]`.

`checkout_refusal` runs in `pre_leg` and last in `audit`, after the refs are judged. The archive's five transitions (absent/absent, created, unmoved, descendant, other) match S3. `judge_descent` is the one function over two refs that the plan chose. `integrate._loop_claimed` and `lane_claimed` are deleted, and `_loop_window` refuses an unreadable claim, so both rungs refuse it.

**Rubric anchors.**
- K3: `loop_claimed` carries `Implements: SR-209, LLR-248`. LLR-248's module lists agent_common.py and its code_symbol now names `loop_claimed`. No Status flipped.
- K2: no SN or SR cell changed. SR-209 is unchanged.
- K1: the LLR-248, TC-242 and IF-065 amendments state what the code does.

**Other checks.**
- The skill copies match the kit source byte for byte.
- `test_overnight_legs_git` is in `tests/conftest.py` SLOW_MODULES.
- The module-size ratchet passes.
- The RESYNC entry is anchored at the landing's parent (cab3b2a76) and names the two kit-owned files.

**Counterpart decisions.**
- **LLR-248 (changed) against SR-209 (parent):** SR-209 is retained. Its acceptance already makes the floor judge every loop lane's commits. Refusing an unread claim is an LLR-tier reading of "the floor sees commits", and no SR text is owed.
- **LLR-248 against TC-242:** carried. The method and expected cells gain the unreadable-claim case, and the evidence file holds tests that fail before the fix.
- **IF-065 data (changed):** carried into the requestor `scripts/integrate`, which was already listed, and into agent_common's `Contract IF-065:` docstring. The TC rows that verify IF-065 (TC rows at test-cases.toml:3004 and :3049) are retained. They verify other members of a Drafted row, and `loop_claimed`'s behaviour is verified under TC-242's evidence.
- **LLR-246 against the held-status rung's new refusal:** see the MINOR finding below.
- No decomposition: no child row was added.

**Done-when coverage.**
- Checkout left off trunk: `test_a_leg_that_leaves_the_primary_checkout_off_trunk_stops_the_run` (real git), and in process `test_the_checkout_must_stay_on_the_bound_trunk` (4 cases) and `test_the_audit_names_a_refused_commit_before_the_checkout`.
- Bind once and log it, no own reader: `test_the_run_binds_trunk_once_and_logs_it`, `test_the_bind_reads_trunk_once_and_logs_it`.
- Refusing reader, exit 2: `test_a_refusing_trunk_reader_stops_the_run_before_any_leg`, `test_a_value_error_from_the_trunk_reader_stops_the_run`.
- Name no branch holds (pin): `test_a_bound_name_no_local_branch_holds_stops_before_the_leg`, `test_a_snapshot_without_the_bound_trunk_stops_before_the_leg`.
- `check-lane` from the lane's worktree: `test_check_lane_from_the_lanes_own_worktree_judges_from_the_kits_trunk`. Its reader refusing or naming no branch: the two in-process `check_lane_cannot_judge` tests.
- Archive rewind, reset and delete: the 3-way parametrized real-git test and `test_the_archive_must_descend_from_its_pre_leg_tip`.
- Archive pins:
  - marked on top: `test_a_marked_archive_commit_on_an_existing_archive_runs_the_next_leg`;
  - created: the existing archive_unmarked case;
  - failed descent read: `test_a_failed_archive_descent_read_stops_the_run_naming_it`;
  - failed claim read in the audit and in check-lane: the `("claim", "--grep")` cases.
- Log line: the real-git and in-process log-line tests.
- Slot with an unreadable log: the trailer-rung and held-status tests. Unparseable record: `test_an_unparseable_claim_record_is_unreadable_never_unclaimed`. Readable pins: `test_the_claim_reader_answers_as_before_on_a_readable_log` (6 cases). One reader: `test_the_slot_and_the_launcher_share_one_claim_reader`.
- Docstrings, skill sync, spine amendments, RESYNC entry, ratchet: present, as checked above.
- Covered elsewhere and not by me: the smoke-tier budget and `trace.py --strict`, which the round facts did not ask me to run, and the act record for the LLR-248/TC-242 amendment, which sits under docs/decisions and is out of my reading scope in this stance.

**Coverage-extension note (no severity).** With the primary checkout detached and `--repo` at a lane's worktree, `check-lane` reads that lane as trunk and passes it on an empty range. The spec records this as off procedure and unguarded until WI-925, and the docstring states it in `**The bound.**`. The recipe runs `check-lane` without `--repo`, from the primary checkout (layout.REPO), so no supported workflow reaches it.

Commands:
- `git rev-parse HEAD` -> ea43e256002f121fe0f8d20a2d466e711a454b9d
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../gate-opus/wi-946 tests/test_loop_provenance.py tests/test_overnight_legs.py tests/test_overnight_legs_git.py` -> `127 passed, 1 skipped in 203.38s` (the skip is the posix-shell environment gate)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (946 work item(s), 832 done (88%), 30 cancelled, graph acyclic).`
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=131 LLR=304 TC=318 orphans=0 integrity=0 ... interface-findings=0 ...`
- `python -m pytest -q tests/test_module_size_ratchet.py` -> `4 passed in 2.44s`
- Red-before run: the new tests, run on the reviewed tree with the three pre-fix sources restored, outside the repo -> `38 failed, 6 passed` (the 6 are the marked pins). The behavioural subset -> `7 failed` with `assert (None)` / `0 == 3`.
- `diff` of the coordinator-cycle SKILL.md across the kit source, `.claude/skills/` and `.agents/skills/` -> identical.
- A real-git probe of `agent_common.loop_claimed` on a repository with a missing object -> `(None, 'git log ... failed (exit 128): error: Could not read ...')`.

- [MINOR] docs/requirements/low-level-requirements.toml:2590 -> for clarity (K1): the held-status rung (`_held_status_refusal`, LLR-246) now refuses a lane whose claim log cannot be read, because the refusal comes back through `_loop_window`. LLR-246's detail still ends "a lane that is not the loop's is not judged at the slot" and does not state the new refusal. Only LLR-248, under SR-209, carries it, as "At the merge slot ...". A reader of LLR-246 alone cannot tell that an unread claim is refused, not treated as a person's lane. -> when LLR-246 is next amended through its authority, add the same sentence it now inherits ("a lane whose claim record cannot be read is refused, naming the read, and nothing is merged"), or cross-reference LLR-248. No code change. -> @owner

VERDICT: APPROVE findings=1
