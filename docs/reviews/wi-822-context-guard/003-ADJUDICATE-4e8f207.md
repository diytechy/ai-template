# ADJUDICATE (first approval): WI-822, SR-229, SR-230, LLR-300, LLR-301, TC-315..TC-318 at 4e8f207

An independent in-lane spine adjudicator (Claude Opus) judged these rows. It wrote none of them
and none of the earlier verdicts: GPT Terra authored the rows, Claude Opus builders wrote the
code, Codex Sol reviewed it. The brief is the kit's composed first-approval brief
(`review-tmp/wave15/brief-wi822-first-r2.md`). The rows are judged as committed at 4e8f2079,
the lane rebased onto trunk eae1f486. This verdict replaces `001-ADJUDICATE-c1fd783.md`, which
returned all eight rows. Codex Sol round 4 (`sol-review-r4.md`, SOUND at 4e8f2079) arrived while
this ran. I read it after my own probes, and it changes no ruling.

## Basis (probed, not trusted)

**What was read.** The chain read was SN-027, SR-156 (the chain TC-317 now joins), SR-229,
SR-230, LLR-140, LLR-300, LLR-301, TC-315..TC-318 and IF-271..IF-281. The code read was all of
`coordinator_guard.py`, `integrate.claim`'s guard rung, `session_keep.primary_out_dir`,
`store_dir`, `store_lock` and `dir_lock`, and both launchers. Both test modules were read whole.
Also read: the WI row and its Done-when, decisions D-001..D-014, Sol reviews 1 to 4,
`001`/`002`, the spine-authoring skill and PROCESS.md §3, §4 and §8.

**The text checks.**

- Every cell of all eight rows at HEAD appears verbatim in the brief, so the brief shows what is
  committed.
- 001's Fixes 1 to 6 and Fix A are byte-exact at HEAD. Fix 4's LLR-301 `detail` gained one
  clause after it: the lock held from acquisition to confirmation or restoration. That clause is
  true of `session_end` since 65027b36: the `with dir_lock` block encloses `_launch_or_restore`,
  and `_restore` does not reacquire the lock.
- Fix 7's `Verifies` gained SR-156 beside LLR-140. That is the SR/LLR pairing the integrator's
  own TC-132 uses.
- Fix 8's evidence dropped `test_a_windows_root_with_spaces_keeps_every_part_quoted`. Nothing is
  lost: the cited e2e `test_the_windows_launcher_runs_the_guards_claude_step_in_the_root` runs
  the guard's exact command line from a root with spaces, and the cited
  `test_the_launcher_runs_detached_in_the_repo_root` pins the all-parts-quoted form.
- R2: neither SR's `Requirement` or `AcceptanceCriteria` names a script, command, file or
  function. Both speak in capability voice ("the delivered work-item admission", "the delivered
  coordination support"). The one environment-variable name sits in LLR-300, where design names
  belong.
- Each SR has one `shall` and states one decision: admission bound to one lease holder until a
  latched drain, and one successor at the holder's exit. Each is labelled DERIVED, argues its
  lens in `Hat-Refs` and `Rationale`, and feeds back to SN-027.
- Pairing: every TC that verifies an LLR also names that LLR's parent SR.
- Tiers: TC-315 and TC-316 cite only `test_coordinator_guard.py`, a smoke module, and are Smoke.
  TC-317 and TC-318 cite `test_coordinator_guard_e2e.py`, which is in `SLOW_MODULES`, and are
  Full. Each tier is honest.

**Probes.** Each probe was one mutation of a clean `git archive` export of 4e8f2079 under
`review-tmp/adj822-r2-mut/`, reverted before the next and checked byte-identical after the last.
Each mutation ran against the evidence its TC cites, and then against the whole of
`test_coordinator_guard.py`, `test_coordinator_guard_e2e.py` and `test_session_keep.py`
(baseline: 74 cited cases and 141 module cases passed).

| # | Mutation | Cited evidence | Whole modules |
|---|---|---|---|
| P1 | a claim with no lease held is admitted | caught (TC-316) | caught |
| P2 / P3 | release / clear stops recording its reason | caught (TC-316) | caught |
| P4 | a lane worktree resolves its own `out/` | caught (TC-317) | caught |
| P5 | PreCompact never sees a pending request | caught (TC-316) | caught |
| P6 | a sidechain record can be the live tip | caught (TC-315) | caught |
| P7 | the CLI's `clear` arm does nothing | caught (TC-318) | caught |
| P8 | the hook CLI raises on unparsable stdin | caught (TC-317) | caught |
| P9 | the ladder runs before the guard | caught (TC-317) | caught |
| P10 | only `OSError` restores a failed launch | caught (TC-318) | caught |
| P11 / P12 | restoration keeps the prompt file / the successor token | caught (TC-318) | caught |
| P13 | admission compares a rounded reading | caught (TC-315) | caught |
| P14 | the dispatcher's route consults the guard | caught (TC-317) | caught |
| P15 | the guard, off, still creates its state directory | caught (TC-317) | caught |
| P16 | a `clear` SessionEnd launches | caught (TC-318) | caught |
| P17 | a launcher exiting non-zero counts as confirmed | caught (TC-318) | caught |
| P18 | the lock is released before the launch (the round-3 MAJOR) | caught (TC-318) | caught |
| P19 | the guard reads its claimant from `CLAUDE_SESSION_ID` instead of `CLAUDE_CODE_SESSION_ID` | **survives** | **survives** |
| P20 | the guard reads the successor token from `PT_COORDINATOR_TOKEN`, while both launchers still export `PT_COORDINATOR_TAKE` | **survives** | **survives** |
| P21 | a CLI refusal exits 3 | caught (TC-318) | caught |
| P22 | a CLI refusal prints no reason on stderr | **survives** | **survives** |
| P23 | a latch-time hook response carries `permissionDecision: deny` | caught (TC-317) | caught |
| P24 | a non-holder's relaunch request is accepted | caught (TC-318) | caught |
| P25 | a lower reading UNLATCHES drain (`latch_reading`, the hook path) | **survives** | **survives** |
| P26 | the claim never reads the transcript itself | caught (TC-317) | caught |
| P27b | a heading inside the prompt fence ends capture | caught (TC-318) | caught |
| P28 | cache-creation tokens are not counted | caught (TC-315) | caught |
| P29 | a successor take keeps the latch | caught (TC-316) | caught |
| P30 | a CLI usage error exits 0 | **survives** | **survives** |
| P31 | the hook CLI exits 1 on unparsable stdin | caught only by TC-317's citation, which TC-318 does not cite | caught |
| P32 | any successor token takes the lease | caught (TC-316) | caught |

What the five survivors mean:

- **P25 breaks SR-229's core property with every test green.** A holder hook event after
  compaction re-reads the low post-compaction occupancy. Under the mutation that event clears the
  latch, and the holder's next claim reads the low number and is admitted. TC-316's latch tests
  drive only `claim_refusal`, which skips `latch_reading` once drain is latched. So LLR-300's
  "retains it through lower readings" and SR-229's "survives a lower reading" are never exercised
  on the path the hooks take every turn. The code is correct today. The verification is missing.
- **P19 and P20 are the two premise seams.** Every test addresses the session variable and the
  successor-token variable through `guard.SESSION_ENV` and `guard.TAKE_ENV`, never by the name
  the agent CLI exports or the name the launchers set. Renaming either constant breaks every real
  claim (P19) or every successor take (P20) and no test notices.
  - P19 leaves LLR-300's "(CLAUDE_CODE_SESSION_ID)" and TC-316's IF-277 link unheld. That
    variable is D-003, the decision record's high-risk premise.
  - P20 leaves TC-318's IF-278 link unheld on the guard's side. The launchers' side is pinned by
    the two e2e launcher tests.
- **P22, P30 and P31 are IF-281's clauses**, which TC-318 claims to verify: the reason on stderr
  after "coordinator guard: ", the usage error's exit 2, and the hook's exit 0. The hook clause
  is held only by a test TC-318 does not cite.

**The owed tests are feasible.** I wrote them as a scratch module in the export
(`tests/test_adj_owed.py`, never in the lane). They pass at 4e8f2079, and each one kills its
survivor: P19, P20, P22, P25 and P30 each go red.

## Rulings

- [APPROVE] SR-229 -> the obligation: while the declared guard is on, every work-item admission route but the unattended dispatcher's admits a claim only from the coordinator lease holder whose drain is not latched; the drain latches at the declared threshold and holds across compaction and resume until the owner's recorded clear or release, or a relaunched successor's take -> the chain: UPWARD, a labelled derived row whose two lenses (UNATTENDED-OPS, a silent degrade; INTEGRITY-RECOVERABILITY, a recovery path written only for the unattended run and ambiguous claim authority) are named in `Hat-Refs` and argued, with feedback to SN-027. Every acceptance clause (guard off reads and writes nothing, the three refusals naming their recovery, the dispatcher untouched, inclusive post-compaction occupancy, unknown is not zero, the latch's lifetime) is true of the code. DOWNWARD, LLR-300 and LLR-140 decompose it, and TC-315, TC-316 and TC-317 verify it directly (P1, P13, P14, P15, P26, P28, P29 caught) -> ready. Its one unverified clause, the latch surviving a hook-measured lower reading (P25), is TC-316's to hold; the text is right. Non-blocking: the row is "unclassified" (no `DA-Refs`, `Delivered-With` or `Coincident`). With `assumption_gate = false` that is an advisory, and the agent-CLI premises it rests on deserve an assumption row (as 001 recommended).
- [APPROVE] SR-230 -> the obligation: while the guard is on, when the lease holder that requested a relaunch from its handoff ends in an exit state, exactly one successor starts from that handoff -> the chain: UPWARD, labelled derived through the integrity lens and fed back to SN-027. The event-triggered EARS form `Where ..., when ...` is right. DOWNWARD, LLR-301 decomposes it. Every acceptance clause is true of the code and held by TC-318: guard off launches nothing, a single launch in the declared root, clear, resume, a non-holder, a subagent and a foreign request launch nothing, one consumption under concurrency, and restoration on any failure, including lock contention (P10, P16, P17, P18, P24 caught) -> ready.
- [APPROVE] LLR-300 -> the obligation: the occupancy reader, the primary-checkout lease, take, release and clear with recorded reasons, the successor-token take, holder-only measurement, the latch and its three ends, the claim boundary keyed on `CLAUDE_CODE_SESSION_ID` that reads the transcript itself, bounded non-refusing hook responses, and compaction telemetry -> the chain: UPWARD, it decomposes SR-229 and adds the design SR-229 leaves open. All three omissions 001 named are now stated: the session variable, the successor token, and release ending the latch. SIDEWAYS, it is SR-229's only design child, and LLR-140 owns the rung's place in the claim ladder. Every clause matches `coordinator_guard.py` at 4e8f2079, and every `code_symbol` name exists and carries `Implements: SR-229, LLR-300` -> ready. Two of its clauses are not yet verified, the variable name (P19) and retention through a hook-measured lower reading (P25). Both are TC-316's return, not defects in this text.
- [APPROVE] LLR-301 -> the obligation: the fenced-prompt extraction, the holder-only atomic request, exit acquisition by rename under a lock held through confirmation or restoration, the successor token and prompt file, full restoration on any failure, the grace-period confirmation, and both launchers' root, token export and one-argument prompt -> the chain: UPWARD, it decomposes SR-230. SIDEWAYS, the launchers now have their `Module` home. Every clause matches the code, including the round-3 lock hold (P18) -> ready. Non-blocking wording note: `request_relaunch` also refuses an existing handoff that carries no session prompt, which "an existing handoff" leaves implicit. The row's first sentence already makes the prompt what a handoff carries, so a builder is not misled.
- [APPROVE] TC-315 -> the obligation: verify the occupancy reader -> the chain: all 13 cited tests exist and pass, the recorded 2.1.289 compaction fixture among them. The reader's clauses are held: inclusive counting (P28), the live branch and the sidechain rule (P6), unrounded admission (P13), malformed and partial records, unknown never zero, and bounded tail widening. `Verifies` (SR-229, LLR-300) no longer claims IF-274 -> ready.
- [RETURN] TC-316 -> the obligation: verify single ownership of admission and the latch's lifetime -> the chain: the ownership half is held (P1, P2, P3, P5, P29, P32 caught). The lifetime half is not: the latch's survival of a LOWER READING is driven only through a claim, which never re-reads once drain is latched, so the hook path that re-reads every turn can unlatch with every test green (P25). `Verifies` names IF-277, and nothing pins the claimant to the variable the agent CLI exports (P19) -> not ready: Fix 1.
- [APPROVE] TC-317 -> the obligation: verify that every guarded route to a claim refuses while draining, without blocking close-out -> the chain: the hook, import, CLI and wrapper routes are each driven by the holder at the crossing reading and with no hook run (P9, P26 caught). The dispatcher's route is untouched (P14), guard-off is inert (P15), close-out passes, the hook CLI's stdin and stdout contract is held (P8, P31), and a lane worktree shares the lease (P4). `Verifies` names SR-156 beside LLR-140, which is honest: the claim rung LLR-140 now states, and the dispatcher's and close-out's availability, are SR-156's lane lifecycle -> ready.
- [RETURN] TC-318 -> the obligation: verify the owned request, exit acquisition, restoration and both launchers -> the chain: the request, acquisition, restoration and launcher halves are held (P7, P10, P11, P12, P16, P17, P18, P21, P24, P27b caught). `Verifies` names IF-278 and IF-281, and neither is held whole. The guard's side of the successor-token variable is never pinned to the name the launchers export (P20). Of IF-281's exit codes, the refusal reason on stderr (P22), the usage error's 2 (P30) and the hook's 0 (P31, held only by a test this TC does not cite) are unverified here -> not ready: Fix 2.


## Fixes: byte-exact replacement cells

Each cell below replaces the named cell whole, and every cell not named stays as committed. The
new test names are the names the replacement `Evidence` cells cite, so the tests must be written
under those names. `Verifies`, `Expected`, `Tier` and `Level` stay as committed for both rows.

### Fix 1: TC-316

`Method`:

```text
Drive holder, other-session and subagent hook payloads and guarded claims with controlled transcript readings and lease state. Assert that a claim identifies its caller by the session variable the agent CLI exports, and refuses, naming its recovery action, with no lease held and from another or an unnamed session; that the holder below the threshold may claim; that a silent holder retains ownership; that the owner's release and clear each require and record their reason; that release and successor take transfer the lease; that the latch survives a lower reading measured by a hook or by a claim, compaction and resume, and ends only by the owner's clear or release or a successor take; that reminders are bounded; and that compaction telemetry records trigger, occupancy, latch and request state and is classified.
```

`Evidence`:

```text
tests/test_coordinator_guard.py::test_a_subagent_and_another_sessions_hook_calls_are_no_ops;tests/test_coordinator_guard.py::test_a_claim_names_its_caller_by_claude_code_session_id;tests/test_coordinator_guard.py::test_with_no_lease_held_a_claim_refuses_naming_the_take;tests/test_coordinator_guard.py::test_a_non_holders_claim_refuses_naming_the_holder_and_the_release;tests/test_coordinator_guard.py::test_the_holders_claim_below_threshold_passes;tests/test_coordinator_guard.py::test_a_silent_live_holder_keeps_the_lease_however_long_it_is_quiet;tests/test_coordinator_guard.py::test_the_owners_release_frees_the_lease_and_is_recorded;tests/test_coordinator_guard.py::test_the_relaunched_successor_takes_the_lease_at_session_start;tests/test_coordinator_guard.py::test_the_latch_holds_after_a_compaction_drops_the_reading;tests/test_coordinator_guard.py::test_the_latch_survives_a_resumed_session_and_is_restated;tests/test_coordinator_guard.py::test_only_the_owners_recorded_clear_or_the_successor_unlatches;tests/test_coordinator_guard.py::test_the_instruction_comes_once_at_the_latch_then_bounded_reminders;tests/test_coordinator_guard.py::test_pre_compact_records_trigger_occupancy_and_guard_state;tests/test_coordinator_guard.py::test_the_handoff_classifies_each_compaction
```

Test changes:

- Write `test_a_claim_names_its_caller_by_claude_code_session_id`. With the holder's lease taken
  below the threshold, it asserts that `claim_refusal(root, env={"CLAUDE_CODE_SESSION_ID": COORD})`
  is None and that `claim_refusal(root, env={"CLAUDE_SESSION_ID": COORD})` refuses as an
  `unknown` caller. Both keys are literal strings, never `guard.SESSION_ENV`. This kills P19.
- Extend `test_the_latch_holds_after_a_compaction_drops_the_reading`. After the 5% post-compaction
  reply, fire a holder `PostToolUse` hook on the transcript, then assert the lease's `draining`
  is still True and the claim still refuses with `drain mode is latched`. This kills P25.

### Fix 2: TC-318

`Method`:

```text
Drive relaunch requests and session-end payloads with a stub launcher, and the guard's command line. Assert holder and handoff validation, clear and resume refusal, single atomic acquisition under concurrent exit handlers, restoration after a launch failure of any kind, including while another handler waits on the store lock, foreign-request refusal, detached launch arguments, both platform launchers and the successor-token variable they export being the one the guard takes the lease by, the command line's take, request-relaunch, release and clear with its exit codes - success, a refusal with its reason on standard error, a usage error, and a hook call that always succeeds - and the dry run.
```

`Evidence`:

```text
tests/test_coordinator_guard.py::test_the_session_prompt_is_the_fenced_block_under_its_heading;tests/test_coordinator_guard.py::test_a_heading_inside_the_prompt_fence_is_prompt_text;tests/test_coordinator_guard.py::test_only_the_holder_requests_a_relaunch_naming_a_real_handoff;tests/test_coordinator_guard.py::test_clear_and_resume_never_launch;tests/test_coordinator_guard.py::test_an_exit_launches_once_in_the_declared_root_with_the_prompt;tests/test_coordinator_guard.py::test_a_non_holders_or_subagents_end_never_launches;tests/test_coordinator_guard.py::test_two_concurrent_end_handlers_launch_once;tests/test_coordinator_guard.py::test_a_failed_launch_restores_the_request;tests/test_coordinator_guard.py::test_a_failed_token_save_restores_the_request;tests/test_coordinator_guard.py::test_a_failed_launch_restores_while_another_handler_wants_the_lock;tests/test_coordinator_guard.py::test_a_failed_prompt_write_restores_the_request;tests/test_coordinator_guard.py::test_a_launcher_that_exits_non_zero_restores_the_request;tests/test_coordinator_guard.py::test_a_launch_failing_with_any_error_restores_the_request;tests/test_coordinator_guard.py::test_a_foreign_request_is_refused_and_reported;tests/test_coordinator_guard.py::test_the_launcher_runs_detached_in_the_repo_root;tests/test_coordinator_guard.py::test_exec_claude_passes_the_prompt_as_one_argument;tests/test_coordinator_guard.py::test_the_successor_takes_the_lease_through_pt_coordinator_take;tests/test_coordinator_guard.py::test_end_to_end_dry_run;tests/test_coordinator_guard_e2e.py::test_the_guard_cli_takes_requests_releases_and_clears;tests/test_coordinator_guard_e2e.py::test_the_hook_cli_reads_stdin_and_prints_its_output;tests/test_coordinator_guard_e2e.py::test_the_posix_launcher_runs_claude_in_the_root_with_the_prompt;tests/test_coordinator_guard_e2e.py::test_the_windows_launcher_runs_the_guards_claude_step_in_the_root
```

Test changes:

- Write `test_the_successor_takes_the_lease_through_pt_coordinator_take`. With a lease recording
  `successor_token = "tok"`, a `SessionStart` hook from another session with
  `env={"PT_COORDINATOR_TAKE": "tok"}` (a literal key, never `guard.TAKE_ENV`) installs that
  session as holder. Together with the two cited launcher tests, which pin the name the
  launchers export, this closes IF-278 on both sides and kills P20.
- Extend `test_the_guard_cli_takes_requests_releases_and_clears`. The refused `take` from
  `OTHER` asserts its stderr starts with `coordinator guard: ` and names the holder. A `release`
  with no `--reason` asserts exit 2. This kills P22 and P30.
- No new code for the hook's exit 0: `test_the_hook_cli_reads_stdin_and_prints_its_output`
  already holds it (P31). The replacement `Evidence` cites it here because TC-318 is the TC that
  verifies IF-281.

## Owed to the builder

The four test changes above. Each was proven feasible in the scratch export (green at 4e8f2079;
P19, P20, P22, P25 and P30 each red). No code change is owed. Every survivor is a missing
assertion over correct code.

Non-blocking, for the code review: `session_keep.primary_out_dir` and `dir_lock` (IF-272 and
IF-273) carry no `Implements:` line.

## Aftermath

No Status is flipped and no snapshot is taken in this pass: the coordinator resumes this
adjudicator to take the act. Two equivalent routes:

**(a) One act, after the returns are answered.** Recommended: the lane is in hand, and the two
fixes are small. Terra applies Fixes 1 and 2 byte-exact, and a builder writes the four test
changes under the cited names. I re-judge TC-316 and TC-318 only. Then one reviewed commit,
after the verdict commits (each ending with the trailer `WI: WI-822`):

1. Flip `status` from `Drafted` to `Approved` on SR-229 and SR-230
   (`docs/requirements/system-requirements.toml`), LLR-300 and LLR-301
   (`docs/requirements/low-level-requirements.toml`), and TC-315, TC-316, TC-317 and TC-318
   (`docs/test/test-cases.toml`), and nothing else. LLR-140 and LLR-270 stay `Approved`.
2. Run, from the lane root, with the quotes kept:

       python project-trajectory/scripts/intake.py snapshot --approves "docs/requirements/low-level-requirements.toml=WI-822;docs/requirements/system-requirements.toml=WI-822;docs/test/test-cases.toml=WI-822" --reattests LLR-140,LLR-270

**(b) Approve the six now, the two later.** If the coordinator wants the approved rows anchored
before the returns are answered:

1. First commit: flip only SR-229, SR-230, LLR-300, LLR-301, TC-315 and TC-317, then run the
   same command as in (a). Each registry keeps one approved row, so all three tokens stay, and
   TC-316 and TC-318 stay `Drafted` inside the test-case copy.
2. Second commit, after the re-judgement: flip TC-316 and TC-318, then run:

       python project-trajectory/scripts/intake.py snapshot --approves "docs/test/test-cases.toml=WI-822"

The command differs from the brief's `python scripts/intake.py`, which is the path in an
adopter's repo. In this repo the script is `project-trajectory/scripts/intake.py`. The stem form
the coordinator quoted (`low-level-requirements.toml=WI-822;...`) resolves to the same three
registries, checked against `baseline_snapshot.parse_approves`. `--reattests LLR-140,LLR-270` is
`004-ADJUDICATE-4e8f207.md`'s MEANING-and-blessed re-attestation, which shares the LLR registry,
so it rides the same snapshot. `--verdict` is not needed because the rungs are released
(`human_approval_through = "DevStg-Boundary"`). If the snapshot refuses, naming any other row,
stop and report it: that is another act's drift, never something to add to `--reattests`.

OUTCOME: RETURN rows=8
