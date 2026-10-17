# WI-931 plan, revision 1: the session kill drops its launch-window and late-spawn guards

Planner: fresh session, 2026-10-16, revision mode. Inputs read: the spec
`docs/work/active/wi-931/WI-931-session-kill-guards-removed.md` in full, its
specref `docs/plans/2026-10-11-review-churn/audit-contrived-guards-2026-10-15.md`
(the wi-881 rows 002 F1, 006 F1 and 007 F1, and pattern 6), the earlier plan
(`docs/plans/WI-931/plan.md`), critique 1 (`docs/plans/WI-931/critique-1.md`),
the owner's ruling on F1's route (`docs/decisions/wi-931.toml` D-002), and the
code at the lane tip `e148d0d15`. The code at that tip is the claim base's: the
lane's merge base with trunk `refactor_again` is `785b29e11`, and the lane's
commits so far touch only `docs/plans/WI-931/`. Code read:
`project-trajectory/scripts/agent_session.py`, `session_service.py`,
`session_keep.py`, `agent_loop.py`, `dispatch.py`, `plan_runner.py`,
`coordinator_adjudicate.py`, `tests/test_session_stdin.py`,
`tests/test_session_keep.py`, `tests/conftest.py`, `pytest.ini`,
`.github/workflows/test.yml`, and the pre-D-006 `_spawn_session`
(`git show d30097e3d^`). Spine read: SR-238
(`docs/requirements/system-requirements.toml`), LLR-026 and LLR-270
(`docs/requirements/low-level-requirements.toml`), TC-026, TC-268 and TC-351,
the three TCs that verify SR-238 (`docs/test/test-cases.toml`), IF-064
(`docs/requirements/interfaces.toml`), CMP-008
(`docs/requirements/components.toml`), `docs/runtime-flows.md`, and
`project-trajectory/RESYNC_PACK.md` §4.

## Finding F1, judged

**Confirmed.** The Done-when says the kept ordinary-kill tests "pass unchanged
on Windows and POSIX" and "pass both before and after the change". The
earlier P7 ran both legs on Windows only. Its POSIX evidence was
optional ("If the coordinator wants POSIX evidence before landing ...") and
left to CI after a push. `.github/workflows/test.yml` runs on a push and tests
the pushed revision only. Nothing on the earlier route produces a POSIX
result at the claim base, and nothing stops the landing without one. So the
lane could close with D3 and D11 unmet on POSIX.

**Answer (owner ruling D-002).** The POSIX legs run on this workstation's WSL
Ubuntu distro: Python 3.12.3, pytest 7.4.4, git 2.43.0, no pytest-xdist, so
serial. Nothing is installed. The coordinator clones the repository into
WSL's own filesystem and runs the kept selection at the claim base (new row
P0) and at the implementation tip (P7). It records both results with their
platform skips. The completion check (new row P8) compares all four records,
Windows and Linux at base and tip, with the expected outcomes below, and the
lane does not land until they match. Linux is the "POSIX" of the Done-when.
macOS is left to CI after the owner's push and is not a completion condition.

The route was checked read-only in this session, with nothing written:

- `wsl -l -v` lists `podman-machine-default` as the default distro, so every
  command names `-d Ubuntu`.
- WSL Ubuntu runs as root (`HOME=/root`) and can read the shared repository's
  refs: `git ls-remote /mnt/c/Projects/ai-template refs/heads/wi-931` answered.
- WSL cannot use the lane worktree itself, because its `.git` file names a
  Windows path.
- WSL's pytest 7.4.4 collects the exact selection below as 15 items under this
  repo's `pytest.ini`. The run was `--collect-only -p no:cacheprovider` with
  `PYTHONDONTWRITEBYTECODE=1`.

## Other corrections from the earlier plan

- **Exact selection.** The kept selection is a fixed list of node ids, not a
  `-k` expression, so a renamed or missing test errors loudly. Each record
  shows the same 15 collected items.
- **D1 grep lines.** P1's grep finds lines 241 (a comment naming
  `SetInformationJobObject`), 291, 334, 335, 531, 546, 554 and 557. The
  earlier plan missed 241 and 335.
- **The census is complete.** P4 now lists every `OSError`, `Exception` and
  `BaseException` handler in the modules that reach a session, with off-path
  rows included. The `plan_runner` budget-parse handler is at L336, not L362.
- **TC-026's evidence module.** P7's module run adds `tests/test_agent_loop.py`,
  which TC-026 names as evidence.
- **D2's red.** D2's red is taken inside P3 by writing the assertion before the
  class change, instead of by stashing.

## Architectural delta

The revision adds evidence steps only, so the answer stands. The row removes
four things:

- a state: a job closed to new members by an active-process limit;
- a check: D-005's IsProcessInJob;
- two launch-cleanup functions;
- `TreeNotEnded`'s out-of-band `BaseException` standing.

It adds no state, no value to any domain, no new input to any output, and
crosses no new boundary. `TreeNotEnded` keeps its name and module, so these
are unchanged:

- IF-064, whose data names `build_argv`, `run_session`, `parse_json_result` and
  the renderers, not the error class;
- WI-895's carrier in `session_service` (LLR-270, TC-268);
- CMP-008's membership (`agent_session` stays in "the agent_* family").

`docs/runtime-flows.md` names neither the kill nor the error. The error rejoins
the `OSError` family it belonged to before D-007.

DELTA: none

## Steps

Build order follows the spec's call 4: the late-spawn and PID-reuse removals
(the spec's scope deliverable D2, code deliverables 2 and 3) land first, then
the launch window (code deliverable 1). Each code step carries the spine cells
its change forces in the same commit: LLR-026's CodeSymbol, and the test names
in TC-026's Method and Evidence. That keeps `trace.py --strict-integrity`
clean at every commit. The prose amendments ride in P5. Evidence brackets the
build: P0 before any code change, P7 at the implementation tip, and P8 makes
completion depend on both.

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P0 | Claim-base evidence: the kept selection on Windows and on WSL Ubuntu, before any code change, recorded with its skips | D3; D4; D5; D6; D7; D8; D9; D10; D11; F1; SR-238; TC-026; TC-268 | IF-064 (exercised at the claim base, not changed) |  |
| P1 | Late-spawn close removed: `_terminate_job` snapshots, then terminates | D1; D12; SR-238; TC-026 | intra-module (agent_session's private Windows kill; no exported name changes) | P0 |
| P2 | D-005's PID-reuse check removed: `_in_job`, `IsProcessInJob`, the query bit | D1; D12; D14; SR-238; TC-026 | intra-module (agent_session's private member snapshot) | P1 |
| P3 | Launch window removed: `_spawn_session` catches `OSError` only; `_end_launch` and `_end_suspended` deleted; `TreeNotEnded` becomes an `OSError`; D2's assertion | D1; D2; D8; D12; SR-238; TC-026 | IF-064 (a `run_session` requestor now sees an error with a different base class and the same name; `session_service` is a listed requestor) | P2 |
| P4 | Handler census between `run_session`'s `finally` and the run's exit | D13; SR-238; TC-268 | IF-064 (agent_session to session_service, plan_runner, agent_loop); intra-module for the callers' own chains | P3 |
| P5 | Spine amendments: SR-238, LLR-026, TC-026 | D12; D14; SR-238; TC-026 | no interface (registry text only) | P3; P4 |
| P6 | RESYNC_PACK entry | D15; SR-238 | no interface (adopter-facing prose) | P3; P5 |
| P7 | Tip evidence: the kept selection and D2's test on Windows and on WSL Ubuntu at the implementation tip; module runs; the commit bar; REVIEW-A | D2; D3; D4; D5; D6; D7; D8; D9; D10; D11; D16; F1; SR-238; TC-026; TC-268; TC-351 | IF-064 (exercised, not changed) | P0; P1; P2; P3; P4; P5; P6 |
| P8 | Completion check: the four kept-selection records and the kept tests' bodies compared with the expected outcomes; the lane lands only on a match | D3; D11; F1; SR-238; TC-026; TC-268 | no interface (a comparison of recorded results) | P0; P7 |

**Where clauses are covered by more than one row**, each row does a separate
part:

- **D3 to D11 and F1:** P0 makes the before record, P7 the after record, and
  P8 compares them.
- **D1 and D12:** each removal step deletes its own symbols and tests, and P5
  runs the checks.
- **D2:** P3 shows the red and then the green on Windows; P7 runs the test
  on both platforms at the tip.
- **D8:** P3 edits the test's comment only; P0 and P7 run it.
- **D14:** P2 trims the CodeSymbol, and P5 makes the prose amendments and
  holds the sitting.

### The kept selection (P0, P7, P8)

This block is shared by every leg. Each leg is one PowerShell invocation that
begins with this definition, because shell state does not persist between
calls:

```powershell
$kept = @(
  'tests/test_session_stdin.py::test_an_uncontainable_child_errors_before_it_runs'
  'tests/test_session_stdin.py::test_a_deadline_kill_ends_the_grandchild'
  'tests/test_session_stdin.py::test_an_interruption_ends_the_grandchild'
  'tests/test_session_stdin.py::test_a_member_the_kill_cannot_open_makes_it_raise'
  'tests/test_session_stdin.py::test_an_ordinary_launch_error_still_returns_the_session_error'
  'tests/test_session_stdin.py::test_run_session_idle_deadline_kills_a_silent_child'
  'tests/test_session_stdin.py::test_run_session_wall_timeout_keeps_its_historical_shape'
  'tests/test_session_keep.py::test_a_ping_whose_tree_cannot_be_ended_is_recorded_then_raised'
  'tests/test_session_keep.py::test_over_a_dirty_trunk_the_unended_tree_is_raised_unrecorded'
  'tests/test_session_keep.py::test_a_failed_recording_never_replaces_the_unended_tree'
  'tests/test_session_keep.py::test_an_ordinary_ping_failure_is_still_recorded_and_swallowed'
)
```

The selection collects 15 items, because three of the tests are
parametrized. The table below is the expected outcome of each item on each
platform, the same at the claim base and at the tip. The Linux skips are the
tests' own `skipif` marks; they are the documented platform skips, and the
records preserve them.

| Done-when | Item | Windows | Linux (WSL Ubuntu) |
|---|---|---|---|
| D4 | `test_an_uncontainable_child_errors_before_it_runs` | passed | skipped: "job containment is Windows" |
| D5 | `test_a_deadline_kill_ends_the_grandchild[python-parent]` | passed | passed |
| D5 | `test_a_deadline_kill_ends_the_grandchild[cmd-shim]` | passed | skipped: "a .cmd shim is Windows" |
| D6 | `test_an_interruption_ends_the_grandchild[python-parent]` | passed | passed |
| D6 | `test_an_interruption_ends_the_grandchild[cmd-shim]` | passed | skipped: "a .cmd shim is Windows" |
| D7 | `test_a_member_the_kill_cannot_open_makes_it_raise` | passed | skipped: "the job snapshot is Windows" |
| D8 | `test_an_ordinary_launch_error_still_returns_the_session_error` | passed | passed |
| D9 | `test_run_session_idle_deadline_kills_a_silent_child` | passed | passed |
| D9 | `test_run_session_wall_timeout_keeps_its_historical_shape` | passed | passed |
| D10 | `test_a_ping_whose_tree_cannot_be_ended_is_recorded_then_raised[tick]`, `[finish]` | passed, passed | passed, passed |
| D10 | `test_over_a_dirty_trunk_the_unended_tree_is_raised_unrecorded[tick]`, `[finish]` | passed, passed | passed, passed |
| D10 | `test_a_failed_recording_never_replaces_the_unended_tree` | passed | passed |
| D10 | `test_an_ordinary_ping_failure_is_still_recorded_and_swallowed` | passed | passed |
| (summary) | the run's last line | `15 passed` | `11 passed, 4 skipped` |

**Where the records go.** Each leg's record goes into the lane's log fragment,
`docs/log.d/WI-931-session-kill-guards-removed.md`, under a heading
"Kept-test evidence (D3–D11)". A record holds:

- the platform;
- the interpreter and pytest versions;
- the `git rev-parse HEAD` of the checkout it ran in;
- the full `-v -rs` output: one line per item, the skip summary with reasons,
  and the final line.

`docs/log.d/` is a record path outside the tree a review verdict names, so a
record committed after the final review round costs no further round.

### P0: claim-base evidence (F1; D3 to D11, before the change)

The coordinator runs P0 after this plan passes its gate and before the builder
edits anything. The claim base is `BASE = 785b29e11e53f65cc5fc8530f8ac0da485f6c4de`,
the lane's merge base with trunk, which is
`git -C C:/Projects/ai-template merge-base wi-931 refactor_again`.

**Windows leg.** Run in the lane worktree. Its code is the claim base's, and
the first command proves it before the run:

```powershell
$kept = @( ...the selection above... )
Set-Location C:/Projects/ai-template.wt/wi-931
git diff --quiet 785b29e11e53f65cc5fc8530f8ac0da485f6c4de HEAD -- project-trajectory tests conftest.py pytest.ini; if ($LASTEXITCODE) { throw 'lane code differs from the claim base' }
git rev-parse HEAD; git status --porcelain -- project-trajectory tests conftest.py pytest.ini
& C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -v -rs -p no:cacheprovider @kept
```

Expected: `15 passed`.

**Linux leg (WSL Ubuntu).** The coordinator makes a clone once, in WSL's own
filesystem, from the shared repository. The lane branch lives in that
repository's refs. `git clone` refuses an existing non-empty target, so a stale
directory stops the step loudly:

```powershell
wsl -d Ubuntu -- bash -c "git clone --quiet /mnt/c/Projects/ai-template ~/wi-931-posix && git -C ~/wi-931-posix checkout --quiet --detach 785b29e11e53f65cc5fc8530f8ac0da485f6c4de"
```

Then it runs the selection at the claim base:

```powershell
$kept = @( ...the selection above... )
wsl -d Ubuntu -- bash -c "cd ~/wi-931-posix && git checkout --quiet --detach 785b29e11e53f65cc5fc8530f8ac0da485f6c4de && git rev-parse HEAD && git status --porcelain && python3 --version && python3 -m pytest --version && python3 -m pytest -v -rs -p no:cacheprovider $($kept -join ' ')"
```

Expected: `11 passed, 4 skipped`, with the four skips and reasons in the
table.

**A deviation at the claim base.** A failure, a different skip, or a count
other than 15 is a pre-existing red. The Done-when's "pass before" is then
false on that platform. The coordinator records it and brings it to the owner
before dispatching the builder; the lane does not proceed around it.

### P1: late-spawn close removed (wi-881 D-004)

`project-trajectory/scripts/agent_session.py`:

- Delete `_close_job`, `_JobBasicLimit`, `_JOB_BASIC_LIMIT`, and
  `_JOB_LIMIT_ACTIVE_PROCESS` with its two-line comment block (L241, which
  names `SetInformationJobObject`). Delete the `k32.SetInformationJobObject`
  prototype in `_win32` (L334–335).
- `_terminate_job`: the `try` body becomes
  `_open_job_members(job, members, unopened)` alone, and the `finally` still
  terminates.
- `_terminate_job`'s docstring drops "close the job to new members" and the
  sentences "Once the active-process limit is set ... complete." and "A member
  that left the list earlier did so by its own exit ...". It keeps three
  things:
  - the measured reason the handles are taken before the terminate (D-003);
  - the rule that the terminate runs even on a failure;
  - the raise for an unopenable member (S3).
- `_kill_tree`'s docstring: "close the job every descendant was born into to
  new members, take a handle on each member, then terminate the job" becomes
  "take a handle on each member of the job every descendant was born into,
  then terminate the job".

`tests/test_session_stdin.py`: delete
`test_a_member_spawned_during_the_kill_has_ended_when_it_returns`,
`LATE_SPAWNER` and `_late_spawn_round`. Each is referenced only there.
`_Watched` stays, because kept tests use it.

In the same commit, the forced spine cells change:

- LLR-026's CodeSymbol drops `_close_job`.
- TC-026's Method drops the deleted test's sentence, and its Evidence drops
  the test's entry.

Tests added: none. The D1 grep, red before the change:

```
grep -nE "_close_job|_JobBasicLimit|SetInformationJobObject" project-trajectory/scripts/agent_session.py
```

At the claim base it finds lines 241, 291, 334, 335, 531, 546, 554 and 557.
After the change it finds nothing.

### P2: PID-reuse check removed (wi-881 D-005, coordinator D-018)

- Delete `_in_job` and the `k32.IsProcessInJob` prototype (L341–342).
- `_open_job_members`: drop the `if not _in_job(...)` block and the docstring
  sentence "A handle whose process is no longer in the job ... (D-005)".
- `_MEMBER_ACCESS = _SYNCHRONIZE`. Its comment (L236–238) drops
  PROCESS_QUERY_LIMITED_INFORMATION and IsProcessInJob, and keeps the
  ERROR_INVALID_PARAMETER note. The name stays: that is the smallest change.
- LLR-026's CodeSymbol drops `_in_job` in this commit. This is D14's CodeSymbol
  part.

Grep check: `grep -nE "def _in_job|not _in_job|IsProcessInJob"` finds L237,
341, 342, 586, 591 and 598 at the claim base, and nothing after the change.
The plain pattern `_in_job` would also match `_contain_in_job`, which stays.

Tests: none pins the check and none changes (spec deliverable 3).
`test_a_member_the_kill_cannot_open_makes_it_raise` still passes, because it
stubs `OpenProcess`, which `_open_job_members` still calls first.

### P3: launch window removed (wi-881 D-006, D-007)

`agent_session.py`:

- `_spawn_session`, Windows branch, returns to the pre-D-006 shape
  (`git show d30097e3d^`, L386–392):

  ```python
  try:
      _contain_in_job(proc)
  except OSError:
      with proc:  # closes the pipes and reaps the never-run child
          proc.kill()
      raise
  return proc
  ```

  The child is still suspended (or never resumed, when `NtResumeProcess`
  failed), so the kill and the reap are enough, and D-001's refusal is
  unchanged. The docstring returns to "a child that cannot be contained is
  killed before it ever runs and the OSError propagates". Three sentences go:
  "owns the child until it returns", the interruption sentence, and the
  TreeNotEnded sentence.
- Delete `_end_launch` and `_end_suspended`.
- `class TreeNotEnded(OSError)`. Docstring: "A session's process tree could
  not be ended, or could not be shown to have ended, within
  _TREE_END_SECONDS. A writer may still be running, so the run must stop;
  callers let it propagate. The machinery's own OSError is kept as its
  cause." The BaseException rationale and the narrow-review-007 sentence go.
- `_kill_tree`: the code is unchanged; it still wraps the machinery's
  `OSError` as `TreeNotEnded ... from exc`. Its docstring drops "This is the
  one place where such an OSError is classified (WI-881 narrow review 007)".
- `_contain_in_job`'s docstring drops "so whoever ends a failed launch can end
  the job (WI-881 gate review 006)". The job is still published before the
  resume; the code is unchanged, and nothing now depends on that order.
- `run_session`'s comments change in two places:
  - The sentence at L927–928, "Set up before the launch, so nothing runs
    between ...", goes, because it claims the hand-off window.
  - The comment at L947 becomes: "From here run_session supervises the child.
    The `finally` is the one place the tree is ended: at a deadline, on an
    interruption, or when the I/O setup fails, but never after a natural
    exit." The existing C3 sentences follow it.

`tests/test_session_stdin.py`:

- **D2's assertion, written first.** Before the class change, add this after
  the `pytest.raises` block of `test_a_tree_not_ended_within_the_bound_raises`:

  ```python
  assert isinstance(raised.value, OSError), type(raised.value).__mro__
  ```

  Then run
  `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q tests/test_session_stdin.py::test_a_tree_not_ended_within_the_bound_raises`
  and paste the red: `TreeNotEnded` derives from `BaseException`, so the
  assertion fails, and the message shows the MRO. Then make the class change,
  re-run, and paste the green.
- Delete these tests, and the helpers referenced only by them (`_marker_child`,
  `_session_outcome`, `_InterruptingThread`):
  - `test_an_interruption_after_the_resume_ends_the_launching_child`
  - `test_an_interruption_before_the_job_ends_the_suspended_child`
  - `test_an_interruption_in_supervision_ends_the_child` (both stages)
  - `test_an_interrupted_launch_whose_tree_cannot_be_verified_raises`
  - `test_a_launch_cleanup_that_cannot_terminate_raises`

  Together with P1's deletions, that makes the six tests and five helpers of
  the deliverables table.
- `test_an_ordinary_launch_error_still_returns_the_session_error`: the comment
  becomes "A launch that never created a child (a missing executable) returns
  the ordinary session-error result.", with no D-007 or round-5 cite. The
  body is unchanged.

In the same commit:

- LLR-026's CodeSymbol drops `_end_launch` and `_end_suspended`.
- TC-026's Method and Evidence drop the five tests deleted here.

The D1 grep:
`grep -nE "_end_launch|_end_suspended|except BaseException" project-trajectory/scripts/agent_session.py`
finds L409, 410, 415, 427 and 436 before the change and nothing after. L409 is
the only `except BaseException` in the file, and it sits in `_spawn_session`.

### P4: handler census (D13)

**Scope.** The census covers every handler of `OSError` or `Exception` in the
kit scripts on the path from `run_session`'s `finally` to the run's exit. That
`finally` is at L958, where `_kill_tree` raises `TreeNotEnded`. Handlers of
`BaseException` are included, since they catch both.

**Method.**

- Walk each caller of `session_service.run_session`. `agent_session.run_session`
  is reached only through `session_service._launch` (L248, `call.runner or
  run_session`). `run_attached` serves attached sittings and never reaches
  `_kill_tree`.
- Cross-check with an AST sweep of every `except` in the modules that reach a
  session, for handlers naming `OSError`, `Exception`, `BaseException`,
  `IOError` or `EnvironmentError`. Those modules are `agent_session`,
  `session_service`, `session_keep`, `agent_loop`, `dispatch`, `plan_runner`
  and `coordinator_adjudicate`.
- No other kit script reaches a session. `agent_brief` and `agent_common`
  import `agent_session` only for `build_argv` and `split_cmd`, so no handler
  elsewhere is on the path.

Line numbers are at the claim base.

**On the path, or bordering it**

| # | Handler | Encloses the tree end? | Verdict |
|---|---|---|---|
| 1 | `agent_session.run_session` `except (OSError, ValueError)` (L945, the launch conversion) | Before the change, yes: through `_spawn_session`, `_end_launch` and `_kill_tree` (the reason D-007 existed). After P3, no: `_spawn_session` never ends a tree, and the `finally` is outside this `try`. | Carries, by construction after P3; pinned by D1's grep and D8's test |
| 2 | `agent_session._spawn_session` `except BaseException` (L409), replaced by P3's `except OSError` | Containment failure only; no tree end inside after P3 | Re-raises (bare `raise`) |
| 3 | `agent_session._end_suspended` `except (OSError, TimeoutExpired)` (L446) | Part of the launch cleanup | Deleted in P3 |
| 4 | `agent_session._kill_tree` `except OSError` (L479) | The kill machinery itself | Re-raises as `TreeNotEnded ... from exc` (the classification) |
| 5 | `session_service.act` `except BaseException` (L398) | Yes, around `_launch` | Re-raises: it accounts metrics and `keep_abandon`, then a bare `raise` |
| 6 | `session_service.call` `except KeyboardInterrupt` (L606), then `finally: _record_call` | Yes | Not an OSError or Exception handler. The `finally` records and the error carries. A recording failure raised there replaces the in-flight error with it as context, and still stops the run; that is the same under both base classes. |
| 7 | `session_service.KeepWarmer._ping` `except agent_session.TreeNotEnded` (L1306), then `except BaseException` (L1308) | Yes | Carries. The specific clause comes first, so an `OSError`-based `TreeNotEnded` is still captured as `unended` and raised on the dispatcher's thread, by `_record_finished` (`try/finally: raise unended`) or by `_raise_unended`. The broad clause sees only other failures. Pinned by TC-268's four tests (D10). |
| 8 | `session_service.through_blackout` `except BlackoutRefused` (L523) | Yes | Carries (`BlackoutRefused` is not an OSError) |
| 9 | `agent_loop.launch_session` `except session_service.SigninRefused` (L2774) | Yes | Carries |
| 10 | `agent_loop.probe_route` `except ValueError` (L2929) | Yes (the recovery probe) | Carries (`TreeNotEnded` is not a ValueError) |
| 11 | `agent_loop.run_iteration`, `routed_session`, `route_session`, `draw_session_route`, `select_with_probe`, `run_loop`, `main`, `_drive_entry`, `_dual_plan_entry` | Yes | No handler; carries to `sys.exit(main())`, a traceback and a nonzero exit |
| 12 | `plan_runner._dp_session` (L190, `through_blackout(lambda: call(asked))`) and `run_dual_plan_round` | Yes, through the dispatch step | No OSError or Exception handler on that path; carries |
| 13 | `coordinator_adjudicate.adjudicate` `except SigninRefused` (L299), `except BlackoutRefused` (L324) | L324, yes | Carries; `main` passes it to `sys.exit` |
| 14 | `dispatch.run` and `dispatch._keep_warm` | Yes (the keep-warm tick raises the carried error) | No handler; carries to `agent_loop.main` |
| 15 | Handlers that run in the cleanup while the error is in flight: `session_keep` store, record and marker I/O `except OSError` (L324, L339, L452, L668, L860, L927, L981), `session_service._write_raw` `except OSError` (L536) | Each wraps its own I/O, not the in-flight error | Not converting. A failure there handles its own write, or raises out of the `except`/`finally` and still stops the run. |

**Off the path** (none encloses a session call or the kill; verdict: not on
the path)

- `agent_session`: `_stdout_is_tty` L729 and `_enable_windows_vt` L756, both
  `except Exception` around console probes. The reader and feeder threads:
  `_pump_stdout` L810 `except Exception` around the renderer, and
  `_feed_stdin` L856 and L861 `except (OSError, ValueError)` around the stdin
  write.
- `session_service`: `cli_version` L659, `_read_token` L862 and
  `signin_status` L1144. These are pre-launch probes and token reads, and
  each probe's subprocess is its own, not the session's.
- `agent_loop`: `map_preflight` L1287, `build_worker_assignment` L1427,
  `_subagent_gate_log_count` L1498, `complete_review_round` L2120 (around
  `score_reviews.record_round` only), and `write_review_owed`,
  `read_review_owed` and `clear_review_owed` (L3082, L3099, L3183). All are
  file I/O.
- `coordinator_adjudicate`: `reserve_verdict` L167 and L176, `bind_requested`
  L195, `_release` L216 and `_inputs` L231. These are the verdict reservation
  and inputs, before the call or inside the refusal branches.
- `plan_runner`: `run_dual_plan_round` L311 `except OSError` (the hat-template
  build), and L336 and L577 `except ValueError` (the budget parse and the
  plan filer).
- `dispatch`: `_branch_exclusive` L514 `except (OSError, ValueError)` (a spec's
  frontmatter read).

**Result.** None converts a failed tree end into a continuing run, and no
handler is fixed in this row. This agrees with the 2026-10-10 sitting 004
check.

Two notes for the reviewer, neither a finding of this row:

- A worker's uncaught `TreeNotEnded` ends that worker process nonzero, and the
  dispatcher reads the exit code across a process boundary. The base-class
  move does not change that, because the error was uncaught there under both
  bases.
- `KeepWarmer.finish` has no caller in the kit scripts today, only tests. That
  is also unchanged.

**Re-check at P3's tip.** The builder re-runs the sweep there and records any
new hit with its verdict in the build note. A hit that converts is fixed in
this row (D13's rule). The sweep:

```
grep -rnE "except +\(?[A-Za-z_., ]*(OSError|Exception|BaseException|IOError|EnvironmentError)" project-trajectory/scripts
```

It is filtered to the seven modules above.

### P5: spine amendments (D14)

The text is exactly as the spec's deliverable 5 states, and the edits stay
in-lane.

- **SR-238** (`docs/requirements/system-requirements.toml`):
  - `acceptance_criteria` is replaced by the spec's text.
  - `rationale`'s last sentence ("An interruption inside platform process
    creation ... is not covered.") is replaced by the spec's two-windows
    residue sentence.
  - SN-006, `requirement`, `boundary_refs` and `hat_refs` are unchanged.
- **LLR-026** (`docs/requirements/low-level-requirements.toml`):
  - Detail gets the spec's four substitutions:
    - the launch-ownership sentence is replaced;
    - "after Popen returns the child" becomes "while the coordinator
      supervises the session";
    - "first closes the job to new members, then takes a handle" becomes
      "takes a handle";
    - the TreeNotEnded sentence becomes "A failure to end the tree, or to
      show that it ended, raises the named tree-end error."
  - Rationale drops "Closing the Windows job before its member snapshot makes
    that snapshot complete, and".
  - CodeSymbol was already trimmed in P1–P3.
- **TC-026** (`docs/test/test-cases.toml`):
  - Method and Evidence were already trimmed of the six tests in P1 and P3.
    For D12, a grep of TC-026 for each deleted test or helper name finds
    none.
  - Expected is replaced by the spec's text.
- **Checked, and unchanged:**
  - SN-006 and SR-026;
  - IF-064 (`docs/requirements/interfaces.toml`), whose data names no error
    class;
  - LLR-270, TC-268 and TC-351 (WI-895's carrier keeps its key, D-018);
  - `docs/requirements/components.toml`: CMP-008 owns the agent_* family, and
    no membership changes;
  - `docs/runtime-flows.md`: no flow names the kill or `TreeNotEnded`.
- **Generated views.** `components.derived.toml`, `PROJECT_STATE.html` and
  `docs/open-items.html` are regenerated by the coordinator at landing, never
  on the work branch.
- **Checks.** Run `python project-trajectory/scripts/trace.py --strict-integrity`
  and `python project-trajectory/scripts/check_trajectory.py --strict`. Both
  must be clean, with the output pasted (D12).
- **The checkpoint sitting.** The three rows are blessed or approved at the
  lane's checkpoint sitting, and their acts are recorded. The sitting and the
  acts are the coordinator's, run on this step's commit.

### P6: RESYNC_PACK entry (D15)

`project-trajectory/RESYNC_PACK.md` gets a new `###` entry, appended as the
last entry of §4, before §5 "Promotion". Today it would follow "The store and
lease lock reads an access-denied create as held". It is anchored
`[since <sha>]` at the landing's parent on trunk, which the coordinator fills
at landing and never with a lane-only sha. The entry says:

- **Kit-owned files, overwrite:** `scripts/agent_session.py`.
- `TreeNotEnded` is an `OSError` again, so an adopter's own `except OSError`
  or `except Exception` around a session catches a failed tree end again; let
  it stop the run. A handler that follows the earlier advice (catch
  `BaseException` and re-raise) keeps working.
- The two residual windows, in SR-238's words:
  - an interruption while the session is still being launched can leave a
    running child;
  - a process that joins the job while the kill takes its member list is
    terminated with the job, but can still be ending for milliseconds when
    the coordinator continues.

  The Windows kill no longer refuses a process started during the kill.
- No setting, registry or migration is forced.

The WI-881 entry's text is history and stays as written.

### P7: tip evidence and the commit bar (F1; D2 to D11 after the change; D16)

**The implementation tip.** This is the lane commit whose `project-trajectory/`,
`tests/`, `conftest.py` and `pytest.ini` are final: the tree the last
full-lane REVIEW-A round names. Call its sha `TIP`. A later commit that
changes any of those paths, such as a review fix or a rebase, makes it a new
`TIP`, and P7's two legs run again there. Commits that change only records,
such as the log fragment, the spec move or the decisions file, leave `TIP`
valid; P8 checks this.

**Windows leg.** Run in the lane worktree at `TIP`, which is clean under
those paths:

```powershell
$kept = @( ...the selection above... )
Set-Location C:/Projects/ai-template.wt/wi-931
git rev-parse HEAD; git status --porcelain -- project-trajectory tests conftest.py pytest.ini
& C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -v -rs -p no:cacheprovider @kept
& C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -v -rs -p no:cacheprovider tests/test_session_stdin.py::test_a_tree_not_ended_within_the_bound_raises
```

Expected: `15 passed`, then `1 passed`.

**Linux leg (WSL Ubuntu).** Run in P0's clone, fetched forward to `TIP`:

```powershell
$kept = @( ...the selection above... )
wsl -d Ubuntu -- bash -c "cd ~/wi-931-posix && git fetch --quiet origin && git checkout --quiet --detach <TIP> && git rev-parse HEAD && git status --porcelain && python3 --version && python3 -m pytest --version && python3 -m pytest -v -rs -p no:cacheprovider $($kept -join ' ') && python3 -m pytest -v -rs -p no:cacheprovider tests/test_session_stdin.py::test_a_tree_not_ended_within_the_bound_raises"
```

Expected: `11 passed, 4 skipped`, with the table's skips and reasons, then
`1 passed`. That last run is D2's assertion on the `os.killpg` branch.

The coordinator runs both legs and records them in the log fragment, with the
same fields as P0's records.

**Module runs (Windows, at `TIP`).** The whole of three modules:

- `tests/test_session_stdin.py`: TC-026's evidence. It sits in `SLOW_MODULES`,
  so the smoke tier skips it.
- `tests/test_agent_loop.py`: TC-026's evidence module.
- `tests/test_session_keep.py`: the evidence of TC-268 and TC-351.

The command is
`C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -n auto tests/test_session_stdin.py tests/test_agent_loop.py tests/test_session_keep.py`,
with the real output pasted.

**Complexity and coverage.** Run `check_complexity` (enforce) and the coverage
floor for `agent_session.py` (`docs/coverage-floors`, 72). Deleted code and
deleted tests move together; the builder reports the measured figure.

**The commit bar (D16).** `run.cmd smoke`
(`python project-trajectory/scripts/run_menu.py smoke` from a shell) must be
green within its 60 s budget, with the real output pasted. Review bar A is one
cross-family REVIEW-A on the lane, scheduled by the coordinator.

### P8: completion check (F1; D3 and D11 read)

The coordinator runs P8 last, before taking the lane to the landing. The lane
is not declared complete, and the landing does not start, until every check
below holds and the fragment carries P8's verdict line.

1. **Four records.** The fragment carries the four records: Windows at `BASE`,
   Linux at `BASE`, Windows at `TIP`, and Linux at `TIP`. Each lists the same
   15 items, and each item's outcome matches the expected-outcome table,
   skip reasons included. Any other outcome means the Done-when is not met: a
   failure, an extra or missing skip, a changed reason, or a count other than
   15.
2. **The records still describe the landing.** Neither the base nor the tip
   has moved under the records. Both of these must be silent:

   ```
   git -C C:/Projects/ai-template diff --quiet <BASE> $(git -C C:/Projects/ai-template merge-base wi-931 refactor_again) -- project-trajectory tests conftest.py pytest.ini
   git -C C:/Projects/ai-template diff --quiet <TIP> wi-931 -- project-trajectory tests conftest.py pytest.ini
   ```

   If the base check fails, the lane was rebased onto a trunk that changed
   that code, and P0's legs re-run at the new base. If the tip check fails,
   P7's legs re-run at the new tip.
3. **"Unchanged" holds for the kept tests' bodies.** Two diffs:
   - `git diff <BASE> <TIP> -- tests/test_session_keep.py` is empty.
   - `git diff <BASE> <TIP> -- tests/test_session_stdin.py` touches only three
     things: the six deleted tests and five deleted helpers, the one D2
     assertion line, and D8's comment lines.
4. **The verdict line.** The coordinator writes it into the fragment: "D3–D11
   met: Windows 15 passed at <BASE> and <TIP>; Linux 11 passed, 4 skipped as
   documented at <BASE> and <TIP>; kept bodies unchanged."
5. **On any mismatch.** The WI stays active and does not land. The coordinator
   brings the deviating record to the owner.

macOS is not a condition here (D-002). CI's macOS job runs after the owner
pushes, and a red there is filed as its own finding.

**Which record each Done-when clause reads**

| Clause | Read from |
|---|---|
| D1 | P1's, P2's and P3's grep output, before and after |
| D2 | P3's red then green (Windows), and P7's `1 passed` on both platforms |
| D3 | P8 checks 1 to 3, over all four records |
| D4 | The `test_an_uncontainable_child_errors_before_it_runs` lines: passed in both Windows records, skipped "job containment is Windows" in both Linux records |
| D5 | The `test_a_deadline_kill_ends_the_grandchild` lines: both parameters passed on Windows; `[python-parent]` passed and `[cmd-shim]` skipped "a .cmd shim is Windows" on Linux; at base and tip |
| D6 | The `test_an_interruption_ends_the_grandchild` lines, as D5 |
| D7 | The `test_a_member_the_kill_cannot_open_makes_it_raise` lines: passed on Windows, skipped "the job snapshot is Windows" on Linux; at base and tip |
| D8 | Its line: passed in all four records |
| D9 | The idle and wall lines: passed in all four records |
| D10 | The six `test_session_keep.py` items: passed in all four records |
| D11 | P8's verdict line: the same outcomes before and after, on both platforms |
| D12 | P5's `trace.py --strict-integrity` and `check_trajectory.py --strict` output, and P5's grep of TC-026 |
| D13 | P4's census tables, and the P3-tip re-check in the build note |
| D14 | P5's diffs and the checkpoint sitting's recorded acts |
| D15 | P6's entry |
| D16 | P7's `run_menu.py smoke` output, and the REVIEW-A round file |

## Clauses and findings not delivered by code in this lane

None is left out. D14's checkpoint sitting, D16's REVIEW-A, and F1's POSIX
legs and completion check are run by the coordinator on the lane's commits
(P0, P5, P7, P8). The rows above prepare exactly what each needs and name the
commands.
