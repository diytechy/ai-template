# ADJUDICATE (first approval): WI-822, SR-229, SR-230, LLR-300, LLR-301, TC-315..TC-318 at c1fd783

An independent in-lane spine adjudicator (Claude Opus) judged these rows. It wrote none of them
(GPT Terra authored the rows, a Claude Opus builder wrote the code). The brief is the kit's
composed first-approval brief (`review-tmp/wave14/brief-wi822-first.md`). The rows are judged as
committed at c1fd7837. While this ran, the coordinator committed b08a1925, the round-2 build after
Sol review 2. It changes code and tests only and leaves every registry cell as c1fd7837 has it, so
these rulings hold at b08a1925. Fix 8 also cites b08a1925's two new tests. Sol review 2 reported
two of these findings independently, as MINORs it handed to the adjudicator: TC-315's IF-274
link, and the IF mark leaving IF-276 free.

**What was read.** The chain read was SN-027 (and SN-006, SN-025, SN-029 as candidate parents),
SR-229, SR-230, LLR-300, LLR-301, TC-315..TC-318, IF-271..IF-275 and the sibling precedents
SR-156, SR-170, SR-194, SR-225 and SR-227. The code read was `coordinator_guard.py`,
`integrate.claim`, the `session_keep` extraction, both launchers, `.claude/settings.json` and both
test modules. Also read: the spec of record, the WI row, decisions D-001..D-013, Sol review 1,
Terra's two reports, the spine-authoring skill and PROCESS.md §3 and §8.

## Probes

Each probe was one mutation of a clean `git archive` export of c1fd7837 under
`review-tmp/wave14/adj822-mut/`, reverted before the next. Each mutation ran twice: once against
the evidence TC-315..TC-318 cite, and once against the whole of `test_coordinator_guard.py`,
`test_coordinator_guard_e2e.py` and `test_session_keep.py`. The unmutated baseline gave 135
passed.

| # | Mutation | Cited evidence | Whole modules |
|---|---|---|---|
| M1 | a claim with no lease held is admitted | **survives** | caught by uncited `test_with_no_lease_held_a_claim_refuses_naming_the_take` |
| M2 | a non-holder's claim is admitted | caught (e2e wrapper test only) | caught |
| M3 | release stops recording its reason | **survives** | **survives** |
| M4 | clear stops recording its reason | **survives** | **survives** |
| M5 | a malformed threshold reads as 50 | caught | caught |
| M6 | `primary_out_dir` ignores the git common directory (a lane worktree gets its own `out/`) | **survives** | **survives** |
| M7 | PreCompact always records "no relaunch requested" | **survives** | **survives** |
| M8 | a sidechain record can be the live tip | **survives** | caught by uncited `test_a_sidechain_record_is_never_the_live_tip` |
| M9 | `dir_lock` excludes nobody | caught in one run of two (concurrency test, nondeterministic) | caught by `test_session_keep` lock tests |
| M10 | release keeps the drain flag for the next taker | caught | caught |
| M11 | the guard's CLI `clear` arm does nothing (`main` dispatch) | **survives** | **survives** |
| M12 | the hook CLI raises on unparsable stdin | **survives** | caught by uncited e2e `test_the_hook_cli_reads_stdin_and_prints_its_output` |
| M13 | the claim never reads the transcript itself | caught | caught |
| M14 | the claimant's session id is ignored | caught (e2e wrapper test only) | caught |

Two direct probes on the same export:

- **A launch that raises anything but `OSError` strands the request.** A `ValueError`, as
  `Popen` raises for an embedded NUL, propagates out of `session_end`. It leaves
  `relaunch.<token>.consumed`, no `relaunch.json`, and the successor token installed.
  `_launch_or_restore` catches `OSError` only.
- **The owner's release ends a latched drain.** The holder takes, crosses the threshold
  (draining), the owner releases, and the same session re-takes. The result is
  `draining = False`. The code and `test_the_owners_release_frees_the_lease_and_is_recorded` (M10)
  both pin this. SR-229's and LLR-300's "only a clear or a successor take" says otherwise.

## Rulings

- [RETURN] SR-229 -> the obligation: while the guard is on, a work-item claim on every route but the dispatcher's is admitted only from the lease holder, and only until its occupancy latches drain; the latch survives compaction and resume -> the chain: UPWARD, SN-027 asks that a declared pause stop claiming and drain, and never double-assign. It names nothing about the coordinating session's own context. A blind derivation from SN-027 does not produce this row. The Rationale opens "SN-027 requires claiming to drain safely and recoverably", which paraphrases into the need what it does not say. Every comparable row in this registry (SR-220..SR-227) is labelled "A DERIVED requirement, and labelled so", argues its lens and feeds back to the need; this one silently traces a derived row to a parent (spine-authoring §2(c)). The lenses do exist: UNATTENDED-OPS listens for a silent degrade, and INTEGRITY-RECOVERABILITY for a recovery path written only for the unattended run. The Requirement reads "refuse a new claim from a session other than its live ... holder and after that holder's ... occupancy reaches the threshold". Read literally, that refuses only a claim meeting both conditions. It also never states the no-lease case, and "live" implies a liveness check the design deliberately never makes (a dead holder keeps the lease until the owner releases it). The latch's end omits the owner's release, which the code and its test (M10) end it on. `Form = "cross-cutting"` is false by SR-194's own definition, "a property of every delivered capability at once": this row is met at one seam, the work-item admission (IF-271), and at the agent-CLI crossings its own Boundary-Refs name. DOWNWARD, the acceptance's "no lease ... refuse with the recovery action named" is held by no cited test (M1) -> not ready; Fix 1.
- [RETURN] SR-230 -> the obligation: at the lease holder's true exit after a relaunch request, exactly one successor session starts from that holder's handoff -> the chain: UPWARD, as SR-229. SN-027 never names a coordinator handing over to a successor, and "SN-027 requires a recoverable lifecycle rather than a half-integrated stop" attributes to the need what is the integrity lens's. The opening `Where` is the optional-feature keyword. The row is started by a discrete event (the holder's exit), so EARS takes `When`, with the guard's dial as the `Where` (PROCESS.md §3 statement pattern). Its guard-off behaviour, nothing launches (pinned by `test_off_means_off_claims_pass_and_hooks_do_nothing`), is unstated. `Form = "cross-cutting"` is false, as for SR-229. DOWNWARD, the "failed launch restores the request" clause holds only for `OSError` failures (the probe above) -> not ready; Fix 2.
- [RETURN] LLR-300 -> the obligation: the design of the occupancy reader, lease, latch, hooks and claim admission -> the chain: SIDEWAYS, it is the only child of SR-229 and overlaps nothing. As a decomposition it leaves three design decisions unstated, and a builder working from the row could not implement them. First, how a claim knows its caller is the holder: the `CLAUDE_CODE_SESSION_ID` environment variable, recorded as high-risk D-003 and stated in no row. Second, how a successor is recognised: the successor token D-005, which LLR-301 already refers to as "the successor token" although no row defines it. Third, that the owner's release ends the latch: the row says it ends "only through an owner's clear or a successor take", which the code and its pinning test contradict (M10). DOWNWARD, "release and clear require and record the owner's reason" is pinned for require and not for record (M3 and M4 survive the whole suite) -> not ready; Fix 3.
- [RETURN] LLR-301 -> the obligation: the design of the owned relaunch request, its atomic acquisition at exit and the platform launch -> the chain: UPWARD, it decomposes SR-230 correctly. SIDEWAYS, the two launchers `scripts/coordinator-relaunch.cmd` and `.sh` hold no Module home in any row. They are the code that enters the declared root, exports `PT_COORDINATOR_TAKE` and starts `claude`, and TC-318 cites their tests. The token `session_end` writes and passes is mentioned only on the failure path. DOWNWARD, "restores ... on any failure before launch confirmation" holds for `OSError` only (the probe above: a code defect against a correct row), and "main dispatches the guard operations" is verified by nothing (M11) -> not ready; Fix 4. The code defect and the missing test sit with TC-318's fix.
- [RETURN] TC-315 -> the obligation: verify the occupancy reader -> the chain: the evidence verifies the reader well (M13 caught), but `Verifies` names IF-274. IF-274 is the hook-event JSON on stdin, and none of the twelve tests drives a hook payload; each calls `read_occupancy`. The sidechain rule LLR-300's "live branch" relies on is pinned only by the uncited `test_a_sidechain_record_is_never_the_live_tip` (M8) -> not ready; Fix 5.
- [RETURN] TC-316 -> the obligation: verify single ownership of admission and the latch's lifetime -> the chain: SR-229's acceptance says a claim with no lease and a claim from another session each refuse, naming the recovery action. The tests that hold those clauses exist (`test_with_no_lease_held_a_claim_refuses_naming_the_take`, `test_a_non_holders_claim_refuses_naming_the_holder_and_the_release`, `test_the_holders_claim_below_threshold_passes`), and no TC cites them, so M1 survives the cited evidence. The recorded reason of a release or clear is asserted nowhere (M3, M4). The "request state" PreCompact records is asserted only as False (M7). The latch-lifetime claim omits release -> not ready; Fix 6.
- [RETURN] TC-317 -> the obligation: verify every guarded claim route refuses while draining, without blocking close-out -> the chain: `Verifies` names IF-272 and IF-273. Nothing in its evidence, or anywhere in the suite, tests `primary_out_dir`'s git-common-dir resolution: M6 makes a lane worktree resolve its own `out/` and survives every module. That is the very split IF-272's rationale exists to prevent. `test_a_wrapper_importing_integrate_is_refused` drives a non-holder (`OTHER`) and asserts the ownership refusal, so the wrapper route's drain refusal, which the Expected claims, is not what it tests. The hook CLI's stdin and stdout contract (IF-274, IF-275) is held only by an uncited e2e test (M12). The guard rung LLR-140 now states has its tests here, but this TC does not name LLR-140 -> not ready; Fix 7.
- [RETURN] TC-318 -> the obligation: verify the owned request, exit acquisition, restoration and both launchers -> the chain: LLR-301 says `main` dispatches the guard operations. That includes `request-relaunch`, the command the latch instruction tells the coordinator to run. No test drives the guard's command line (M11 survives every module). The restoration it claims for "launch failure" holds only for `OSError` (the probe above) -> not ready; Fix 8.

OUTCOME: RETURN rows=8

## Fixes: byte-exact replacement cells

Each cell below replaces the named cell whole; every cell not named stays as committed. A fix that
also needs a test or code change says so. The new test names below are the names the replacement
Evidence cells cite, so the tests must be written under those names.

### Fix 1: SR-229

`Requirement`:

```text
Where the declared coordinator context guard is enabled, the delivered work-item admission, on every route but the unattended dispatcher's own, shall admit a new claim only from the current coordinator lease holder while that holder's drain is not latched, the drain latching once the holder's context occupancy reaches the declared threshold and holding across compaction and resume until the owner records a clear or a release or a relaunched successor takes the lease.
```

`Rationale`:

```text
A DERIVED requirement, and labelled so. SN-027 asks that a declared pause stop claiming and drain what is already in flight, and that recovery never double-assign work; it does not name the coordinating session's own context, so this obligation arrives through two lenses rather than through the need's text. The unattended-operations lens listens for a silent degrade: a coordinator whose context has crossed its declared limit keeps claiming after compaction has degraded the context it needs to close the work it already holds, and nothing pages anyone. The integrity lens listens for a recovery path written only for the unattended run when the same corruption is reachable attended, and for a claim nothing can reclaim once its holder is gone: a retained adjudicator session already drains on occupancy while the attended coordinator does not, and a second or missing holder leaves claim authority ambiguous, so one lease names the coordinator and only the owner's recorded release frees a lease whose holder has gone. A latched single-holder admission boundary was chosen over a one-time event observation because every claim must remain protected when an event is missed or the transcript later reports a lower reading. Fed back to the need: SN-027's acceptance could name the coordinating session's own capacity as a declared reason to stop claiming and drain; until it does, this row is derived and says so.
```

`AcceptanceCriteria`:

```text
With the guard off, admission proceeds without reading or writing guard state; with it on, the holder below the threshold may claim, while a claim with no lease held, a claim from another session or from a caller naming no session, and a claim from a holder at or above the threshold each refuse, naming the recovery action. The unattended dispatcher's own admission remains available without consulting this guard. Occupancy counts the newest valid post-compaction usage on the live branch, including cached input, and unknown usage is not zero. A latched drain survives a lower reading, compaction and resume, and ends only when the owner records a clear or a release, or a relaunched successor takes the lease.
```

`Form`: `interface`. The assumption gate is off here (`[checks] assumption_gate = false`), so the
interface-form allocation reads as advisories, which are then the honest list of the tie-backs the
rows owe. The new advisory "SR-229/SR-230 unclassified" (no DA-Refs, Delivered-With or
Coincident) has the same root. The row's delivery rests on version-dependent premises about the
agent CLI (it exports the session id to tool processes, records per-reply usage in its
transcript, and uses the SessionEnd reason vocabulary). An assumption row is their home, per
SN-043. That is recommended, and it is not part of this return.

### Fix 2: SR-230

`Requirement`:

```text
Where the declared coordinator context guard is enabled, when the coordinator lease holder that has requested a relaunch from its handoff ends its session in an exit state, the delivered coordination support shall start exactly one successor session from that handoff.
```

`Rationale`:

```text
A DERIVED requirement, and labelled so. SN-027 asks that claiming drain what is already in flight and that a crash at any lifecycle boundary recover without double-assignment; it does not name a coordinating session handing over to its successor, so this obligation arrives through the integrity lens rather than through the need's text. That lens asks what the next reader finds when a holder is gone: a close-out that loses its handoff strands the next coordinator, and one that can launch twice creates competing claim authority. An atomic, owned request consumed once was chosen over treating every session-end event as a relaunch because clear and resume do not end the coordinator and a failed launch must remain recoverable. Fed back to the need: SN-027's acceptance could name an orderly handover of the coordinating role as part of a drain; until it does, this row is derived and says so.
```

`AcceptanceCriteria`:

```text
With the guard off, no exit launches anything. A request from the holder for an existing handoff launches once at an exit in the declared repository and starts from that handoff. Clear, resume, a non-holder, a subagent and a foreign request launch nothing; concurrent exit handling consumes one request once; and a launch that fails for any reason restores the request.
```

`Form`: `interface` (as Fix 1).

### Fix 3: LLR-300

`Detail`:

```text
guard_config reads the declared coordinator threshold and window: a non-positive, out-of-range or malformed threshold is off and a malformed window reads as the default. read_occupancy reads the newest valid assistant usage after the live transcript branch's latest compaction boundary, never a sidechain record, counting input and cached input; a record whose usage is malformed, partial or zero is skipped, and no valid usage reads as unknown, never zero. A primary-checkout lease names one coordinator session and its transcript. take refuses another holder; release frees the lease and clear unlatches it, each requiring and recording the owner's reason; elapsed time never transfers ownership. on_session_start installs a session as holder, unlatched, only when it presents the successor token the holder's exit wrote into the lease, and restates a latched drain to the holder's own resumed start. Only the holder's own hook payload on the holder's transcript is measured, never a subagent's. latch_reading latches drain when the unrounded reading reaches the threshold and retains it through lower readings, compaction and resume; it ends only through the owner's clear, the owner's release or a successor take. claim_refusal identifies the claimant by the session id the agent CLI exports to its tool processes (CLAUDE_CODE_SESSION_ID), refuses with no lease held or a claimant that is not the holder, and reads and latches the holder's transcript itself, so a refusal never depends on a hook having run; a claim holding the dispatch lock never calls it. Hook responses inject the latch instruction once and bounded reminders thereafter, and never refuse a tool call. PreCompact records trigger, occupancy and latch/request state; classify_compaction reports missed-threshold, manual and during-drain cases.
```

Test change, needed by Fix 6: the release and clear tests assert the recorded reason.

### Fix 4: LLR-301

`Module`:

```text
project-trajectory/scripts/coordinator_guard.py;scripts/coordinator-relaunch.cmd;scripts/coordinator-relaunch.sh
```

`Detail`:

```text
session_prompt extracts the one fenced session prompt from a handoff, preserving headings inside that fence as prompt text. request_relaunch accepts only the lease holder and an existing handoff, then writes a same-session request atomically. session_end acts only for a true exit by that holder in its declared repository, rejects a foreign request, and atomically renames one request to acquire it. It writes a fresh successor token into the lease and the handoff prompt to a file, invokes the platform launcher detached in the declared root with that file and token, and on any failure before launch confirmation restores the request and removes the successor token and the prompt file. launch_command selects the Windows or POSIX launcher; launch_detached waits through its grace period and confirms only a still-running launcher or one that exits zero. Each launcher enters the declared root, exports the token as PT_COORDINATOR_TAKE for the successor's SessionStart take, and starts claude with the prompt as one argument: the POSIX one in a new terminal, the Windows one through exec_claude, which invokes claude with the extracted prompt. main dispatches the guard operations.
```

### Fix 5: TC-315

`Verifies`: `["SR-229", "LLR-300"]` (IF-274 moves to TC-316 and TC-317).

`Evidence`:

```text
tests/test_coordinator_guard.py::test_occupancy_counts_input_cache_read_and_cache_creation;tests/test_coordinator_guard.py::test_a_branched_transcript_reads_the_live_branch;tests/test_coordinator_guard.py::test_a_sidechain_record_is_never_the_live_tip;tests/test_coordinator_guard.py::test_after_compaction_only_usage_after_the_last_boundary_counts;tests/test_coordinator_guard.py::test_the_recorded_compaction_fixture_is_claude_code_2_1_289;tests/test_coordinator_guard.py::test_a_recorded_compaction_reads_the_reply_after_the_boundary;tests/test_coordinator_guard.py::test_a_recorded_compaction_never_reads_a_preserved_messages_old_usage;tests/test_coordinator_guard.py::test_after_a_resume_the_newest_usage_counts_whatever_session_wrote_it;tests/test_coordinator_guard.py::test_malformed_and_partial_usage_is_skipped_to_the_newest_valid;tests/test_coordinator_guard.py::test_no_valid_usage_reads_unknown_never_zero;tests/test_coordinator_guard.py::test_a_mismatched_window_is_flagged_with_its_percent;tests/test_coordinator_guard.py::test_admission_compares_unrounded_occupancy;tests/test_coordinator_guard.py::test_the_reader_reads_the_tail_and_widens_only_to_resolve
```

### Fix 6: TC-316

`Verifies`: `["SR-229", "LLR-300", "IF-274", "IF-275"]`

`Method`:

```text
Drive holder, other-session and subagent hook payloads and guarded claims with controlled transcript readings and lease state. Assert that a claim refuses, naming its recovery action, with no lease held and from another or an unnamed session; that the holder below the threshold may claim; that a silent holder retains ownership; that the owner's release and clear each require and record their reason; that release and successor take transfer the lease; that the latch survives compaction and resume and ends only by the owner's clear or release or a successor take; that reminders are bounded; and that compaction telemetry records trigger, occupancy, latch and request state and is classified.
```

`Expected`:

```text
Exactly one coordinator owns admission, a claim without its lease refuses naming the recovery action, and the drain state remains latched until the declared recovery action.
```

`Evidence`:

```text
tests/test_coordinator_guard.py::test_a_subagent_and_another_sessions_hook_calls_are_no_ops;tests/test_coordinator_guard.py::test_with_no_lease_held_a_claim_refuses_naming_the_take;tests/test_coordinator_guard.py::test_a_non_holders_claim_refuses_naming_the_holder_and_the_release;tests/test_coordinator_guard.py::test_the_holders_claim_below_threshold_passes;tests/test_coordinator_guard.py::test_a_silent_live_holder_keeps_the_lease_however_long_it_is_quiet;tests/test_coordinator_guard.py::test_the_owners_release_frees_the_lease_and_is_recorded;tests/test_coordinator_guard.py::test_the_relaunched_successor_takes_the_lease_at_session_start;tests/test_coordinator_guard.py::test_the_latch_holds_after_a_compaction_drops_the_reading;tests/test_coordinator_guard.py::test_the_latch_survives_a_resumed_session_and_is_restated;tests/test_coordinator_guard.py::test_only_the_owners_recorded_clear_or_the_successor_unlatches;tests/test_coordinator_guard.py::test_the_instruction_comes_once_at_the_latch_then_bounded_reminders;tests/test_coordinator_guard.py::test_pre_compact_records_trigger_occupancy_and_guard_state;tests/test_coordinator_guard.py::test_the_handoff_classifies_each_compaction
```

Test changes, under the same names:

- `test_the_owners_release_frees_the_lease_and_is_recorded` asserts the release event's `reason`.
- `test_only_the_owners_recorded_clear_or_the_successor_unlatches` asserts the clear event's
  `reason`.
- `test_pre_compact_records_trigger_occupancy_and_guard_state` also covers a pending relaunch
  request (`relaunch_requested` True).

These kill M3, M4 and M7.

### Fix 7: TC-317

`Verifies`: `["SR-229", "LLR-300", "LLR-140", "IF-271", "IF-272", "IF-273", "IF-274", "IF-275"]`

`Method`:

```text
Drive the claim boundary through hook, direct import, CLI and wrapper routes at the crossing reading and with no prior hook call, the hook command line through its standard input and output, and the lease from a linked lane worktree. Assert that the live dispatcher and close-out operations remain available, that the guard-off and malformed-threshold paths are inert, that each route's claim by the holder refuses while draining, that the hook command line answers a parsed event on its output and an unparsable one with nothing, and that a lane worktree reads and locks the primary checkout's lease.
```

`Evidence`:

```text
tests/test_coordinator_guard.py::test_off_means_off_claims_pass_and_hooks_do_nothing;tests/test_coordinator_guard.py::test_a_malformed_threshold_leaves_the_guard_off;tests/test_coordinator_guard.py::test_the_crossing_replys_claim_refuses_via_the_pre_tool_use_reading;tests/test_coordinator_guard.py::test_the_crossing_replys_claim_refuses_with_no_hook_run;tests/test_coordinator_guard.py::test_the_live_dispatchers_claim_route_is_untouched;tests/test_coordinator_guard.py::test_only_the_claim_consults_the_guard_so_close_out_passes;tests/test_coordinator_guard.py::test_a_draining_pre_tool_use_never_denies_a_close_out_command;tests/test_coordinator_guard_e2e.py::test_the_cli_claim_refuses_while_draining;tests/test_coordinator_guard_e2e.py::test_a_wrapper_importing_integrate_is_refused;tests/test_coordinator_guard_e2e.py::test_close_out_git_operations_pass_while_draining;tests/test_coordinator_guard_e2e.py::test_the_hook_cli_reads_stdin_and_prints_its_output;tests/test_coordinator_guard_e2e.py::test_a_lane_worktree_shares_the_primary_checkouts_lease;tests/test_session_keep.py::test_the_store_lock_excludes_a_second_holder
```

Test changes:

- `test_a_wrapper_importing_integrate_is_refused` drives the holder's session (`COORD`) and
  asserts `drain mode is latched`. The non-holder case is held in-process by Fix 6's evidence.
- Write `test_a_lane_worktree_shares_the_primary_checkouts_lease`. It takes the lease from a
  `git worktree add` lane of the `draining` repo, then asserts that `lease_dir(lane) ==
  lease_dir(primary)` and that the primary's claim sees the lane's lease. This kills M6.

### Fix 8: TC-318

`Method`:

```text
Drive relaunch requests and session-end payloads with a stub launcher, and the guard's command line. Assert holder and handoff validation, clear and resume refusal, single atomic acquisition under concurrent exit handlers, restoration after a launch failure of any kind, foreign-request refusal, detached launch arguments, both platform launchers, the command line's take, request-relaunch, release and clear, and the dry run.
```

`Evidence`:

```text
tests/test_coordinator_guard.py::test_the_session_prompt_is_the_fenced_block_under_its_heading;tests/test_coordinator_guard.py::test_a_heading_inside_the_prompt_fence_is_prompt_text;tests/test_coordinator_guard.py::test_only_the_holder_requests_a_relaunch_naming_a_real_handoff;tests/test_coordinator_guard.py::test_clear_and_resume_never_launch;tests/test_coordinator_guard.py::test_an_exit_launches_once_in_the_declared_root_with_the_prompt;tests/test_coordinator_guard.py::test_a_non_holders_or_subagents_end_never_launches;tests/test_coordinator_guard.py::test_two_concurrent_end_handlers_launch_once;tests/test_coordinator_guard.py::test_a_failed_launch_restores_the_request;tests/test_coordinator_guard.py::test_a_failed_prompt_write_restores_the_request;tests/test_coordinator_guard.py::test_a_failed_token_save_restores_the_request;tests/test_coordinator_guard.py::test_a_launcher_that_exits_non_zero_restores_the_request;tests/test_coordinator_guard.py::test_a_launch_failing_with_any_error_restores_the_request;tests/test_coordinator_guard.py::test_a_foreign_request_is_refused_and_reported;tests/test_coordinator_guard.py::test_the_launcher_runs_detached_in_the_repo_root;tests/test_coordinator_guard.py::test_a_windows_root_with_spaces_keeps_every_part_quoted;tests/test_coordinator_guard.py::test_exec_claude_passes_the_prompt_as_one_argument;tests/test_coordinator_guard.py::test_end_to_end_dry_run;tests/test_coordinator_guard_e2e.py::test_the_guard_cli_takes_requests_releases_and_clears;tests/test_coordinator_guard_e2e.py::test_the_posix_launcher_runs_claude_in_the_root_with_the_prompt;tests/test_coordinator_guard_e2e.py::test_the_windows_launcher_runs_the_guards_claude_step_in_the_root
```

Code and test changes:

- `_launch_or_restore` restores on any exception, not `OSError` alone, as LLR-301 already says.
  `test_a_launch_failing_with_any_error_restores_the_request` drives a launch raising
  `ValueError`.
- `test_the_guard_cli_takes_requests_releases_and_clears` (e2e) runs `coordinator_guard.py take`,
  `request-relaunch --handoff`, `release --reason` and `clear --reason` as subprocesses with
  `CLAUDE_CODE_SESSION_ID` set. It asserts the exit codes and the lease and request files. This
  kills M11.

## The interface rows and D-013 (no act owed; findings)

- **IF-271, IF-272 and IF-273 are true.** Owner, far side, channel and data match the code and
  the `Contracts:` bodies. IF-272 is untested anywhere (M6); Fix 7 covers that.
- **IF-274's channel is wrong.** It declares `bytes`, which the closed vocabulary defines as
  opaque content. The payload is a typed JSON object, and the precedent for the same kind of
  crossing (IF-151, the subagent gate's PreToolUse stdin) uses `cli`. The data cell is accurate.
- **IF-275 says "optional additionalContext", which overstates the shape.** The guard prints no
  response without context, and every response it prints carries both keys, as its own
  `Contract IF-275` body says. Suggested data: `hook response JSON, printed only when there is
  context to add: hookSpecificOutput with hookEventName and additionalContext`.
- **Undeclared crossings remain.** None of these has a row:
  - `CLAUDE_CODE_SESSION_ID`: the agent CLI sets it and `claim_refusal` reads it. It is the
    high-risk D-003 premise.
  - `PT_COORDINATOR_TAKE`: the launcher sets it and SessionStart reads it.
  - The launchers' argv (`REPO_ROOT PROMPT_FILE TOKEN`), which the guard requests.
  - The guard's own command line and its exit code. The operator and the Windows launcher use
    it, and every refusal names it as the recovery action. PROCESS.md §8 makes a CLI's arguments
    and its exit code two rows.
- **D-013 removed IF-276 rightly in substance, but two of its statements are false.** The
  `out/coordinator/` layout is the guard's private state.
  - **"The relaunch launchers only call the guard's CLI".** The POSIX launcher reads the prompt
    file itself (`claude "$(cat "$2")"`). The module header's "only this module reads or writes
    it" is false for `relaunch-prompt.<token>.txt` in the same way. The honest seam is the
    launcher-argv row above, whose second argument names a text file holding the prompt.
  - **"The id stays retired (the watermark never falls)".** IF-276 was never committed. Commit
    c1fd7837 moved the IF mark from 270 to 275, so the next IF mint takes IF-276 and re-points
    the IF-276 citations in `terra-spine-r2.md`, D-013 and c1fd7837's message. Either D-013 must
    say so, or the mark must reach 276 by a ruled `--correct-mark`.

## Other code findings (for the code review, not row rulings)

- `coordinator_guard.py` carries no `Implements:` back-link to SR-229, SR-230, LLR-300 or LLR-301.
  `integrate.claim` still names only SR-156 and LLR-140.
- The non-`OSError` stranding above is still present at b08a1925, which widened the restore to
  the successor-token save but kept `except OSError` around the prompt write and the launch. A
  `TypeError` from writing a `None` prompt (a handoff that vanished after validation) strands the
  request the same way. Its fix is in Fix 8.

## Aftermath

This is a RETURN, so no Status changes and no snapshot is taken. The coordinator holds the act
until the code review is SOUND. After the fixes land and are re-judged, the act is the flips plus
one snapshot. Fix 7 and the amendment verdict `002-ADJUDICATE-c1fd783.md` together put LLR-140 and
LLR-270 in the same act:

    python project-trajectory/scripts/intake.py snapshot --approves "docs/requirements/low-level-requirements.toml=WI-822;docs/requirements/system-requirements.toml=WI-822;docs/test/test-cases.toml=WI-822" --reattests LLR-140,LLR-270
