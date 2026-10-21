# WI-940 implementation plan: no bar fails on the smoke tier's seconds; the audit judges its CPU-seconds

Spec: `docs/work/active/wi-940/WI-940-cpu-time-smoke-budget.md`. Specref:
`docs/decisions/coordinator-2026-10-17.toml` (D-004, D-005, D-007; the owner
re-scope is coordinator-2026-10-20 D-014; the two other enforce callers are
coordinator-2026-10-21 D-001).

**Revision 2** (the plan's one revision) answers the round-1 critique
(`docs/plans/WI-940/critique-1.md`), one finding. F1 is confirmed and
adopted: D-007 Q3 (a) reads "the Windows job-object code moves first into one
shared kit module, in a behaviour-preserving commit, which the session kill,
the root conftest and the budget step all import". Deliverable 6 says what
moves out of `agent_session`. It does not revoke the conftest's import, and
round 1's open point 2 was wrong to leave it out. P2 now has the root conftest
take its kernel32 prototypes from the shared module, with its cap and priority
unchanged, and a test that bites if the conftest builds its own. The open
point is withdrawn. No other row's scope changes. P3 loses one bullet (the
`GetCurrentProcess` prototype now arrives in P2).

DELTA: within

The architectural-delta answer: the WI does all four, and this plan carries
each change as a row of the table.

- **New state.** The step's own Windows job (P3, P4) and the conftest's
  private-job mode (P2).
- **New domain values.** `[smoke-budget]` loses `seconds` and gains
  `cpu-seconds` and `wall-seconds` (P4, P6). `[run]` gains `audit` (P7).
  `PYTEST_CPU_CAP_JOB` gets one recognised value, `private` (P2).
- **New input to an output.** The verdict now depends on the OS's CPU
  accounting (P3, P4) and, in enforce mode, on a collect-only count (P7).
- **New boundary.** A new kit module, `kitlib/winjob.py`, is called by
  `agent_session` (P1), by the root conftest (P2) and by the step (P3, P4).

No refactor this WI does not own is needed. The move is this WI's first
commit (D-007 Q3 (a)), and every other change stays inside the step, the root
conftest, `[smoke-budget]`/`[run]`/`[step:smoke]`, the CI job and the doc
homes.

**One divergence from the spec, measured, for the coordinator.** The spec says
"No LLR, TC or IF row is amended" and "No component or IF row changes". A
probe refutes that for the move. The probe was a scratch clone of the lane at
7f8e57192 under `%TEMP%`, with the repository untouched. It did deliverable
6's move as P1 states it. `tests/test_session_stdin.py` stayed green
(29 passed). `check_trajectory.py --strict` then gave three findings:

- ERROR: "docs/knowledge/ holds 15 pack(s) but 1 arch-map module(s) are in
  no CMP-### component (scripts/kitlib/winjob)".
- Two WARNs: the moved `Implements: ... LLR-026` tags sit in a module that
  LLR-026's `module` cell does not name.
- WARN: "connectivity undeclared: module 'scripts/kitlib/winjob' is in the
  arch-map but no IF-### row names it".

Adding `project-trajectory/scripts/kitlib/winjob.py` to LLR-026's `module`
cell, and renaming the two moved symbols in its `code_symbol` cell, cleared
the ERROR and both tag WARNs. Only the connectivity WARN was left. So P1
does two things the spec did not expect:

- **LLR-026's pointer cells.** It updates LLR-026's traced `module` and
  `code_symbol` cells. Under the §A5.1 cell split, these are "traced, not
  approved", so a pointer that follows moved code does not arm
  amend-without-flip, and the row's approved text is unchanged.
- **One new Drafted IF row** for the new module, so the connectivity check
  has a declaration to read.

Without the first edit the landing tip is not `--strict` clean (D15). The
second is what the delta question asks for when the WI crosses a new boundary.

## Cited registries (checked; unchanged unless a row says otherwise)

- **SR rows** (`docs/requirements/system-requirements.toml`): the item
  declares none (`sr_refs = []`). Its anchor is SN-007 ("The declared bar is
  green before a change lands"). SN-008 rules out a silent fallback. No SR
  row changes. The performance-budget layer (SR-015, SR-167) is not used,
  for the reason the spec's S4 gives.
- **TCs** (`docs/test/test-cases.toml`): no TC verifies an SR of the item.
  P1 *runs* TC-026 (it verifies SR-026, SR-238 and LLR-026, the session
  kill whose job code moves). Its method names `tests/test_session_stdin.py`
  cases, and they pass unchanged. No TC text changes.
- **Interfaces** (`docs/requirements/interfaces.toml`):
  - IF-064 (`scripts/agent_session`'s session-launch surface and its
    re-export guarantee) is crossed by P1 and stays unchanged.
  - IF-297 (`scripts/kitlib/commit_hooks`, a kitlib module called by
    CMP-008 scripts) is the nearest existing row to the proposed winjob row.
  - IF-049 (`[run]`: "one name = command line per capability, plus a desc
    line") takes P7's and P8's values, with its shape unchanged.
  - IF-022 (`docs/stack.ini` sections, `bars` and `step:NAME` among them)
    takes P7's `[step:smoke]` value; its shape is unchanged and `[bars]
    review` is untouched. IF-022 does not cover `[smoke-budget]`.
  - One new row is proposed in P1.
- **Components** (`docs/requirements/components.toml`): CMP-008 holds
  `agent_session` through LLR-026. Under P1, the new module joins CMP-008
  through LLR-026's `module` cell, so both ends of the new call are in one
  component and no cross-component seam or `docs/kernel-modules-allow` entry
  is owed. `scripts/check_smoke_budget.py` and the root `conftest.py` are
  outside the arch map (`[paths] src` is `project-trajectory/scripts`). No
  CMP row changes.
- **Runtime flows** (`docs/runtime-flows.md`): Flows 1 to 6 draw no smoke
  budget, bar step or job object (grep: `smoke`, `budget`, `job`), so they
  stay as they are.

## Plan table

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | The job-code move into `kitlib/winjob.py`, its own behaviour-preserving commit (deliverables 6 and 5) | D1; D10; TC-026 | IF-064; Proposed: a new Drafted row, owner `scripts/kitlib/winjob`, requestors `scripts/agent_session`, channel call, component CMP-008; the nearest existing row is IF-297 (also a kitlib module called by CMP-008 scripts), which declares `hooks_refusal` and cannot carry the job helpers | |
| P2 | The root conftest imports the shared module for its job prototypes, then gains its private-job input (D-007 Q3 (a); deliverable 2) | D1; D4; F1 | Proposed: P1's winjob row gains the conftest's prototypes (`SetInformationJobObject`, `IsProcessInJob`, `GetCurrentProcess`, `SetPriorityClass`) in its data cell; the nearest existing row is IF-297, as in P1; the root `conftest.py` that calls them is outside the arch map, and its new environment input is read in-process | P1 |
| P3 | The shared module's job reading: create-and-join and CPU seconds (deliverable 1, Windows) | D1; D2 | Proposed: P1's winjob row gains `create_joined_job` and `job_cpu_seconds` in its data cell; the nearest existing row is IF-297, as in P1; the step that calls them is outside the arch map | P1 |
| P4 | The step: three keys, the meter, the tier's environment, the verdict line, the exit precedence; `--elapsed` retires (deliverables 1 and 3) | D1; D5; D6; D7; D8 | no interface: `scripts/check_smoke_budget.py` is outside the arch map, and `[smoke-budget]` is outside IF-022 (spec, "The anchor"); intra-module | P2; P3 |
| P5 | The platform readings and the outside-process case, in a new slow module (deliverables 1 and 2) | D1; D2; D3; D4 | no interface: tests only (intra-module) | P4 |
| P6 | The stamped values: readings, `fig:` lines, `seconds` retired, the `[smoke-budget]` header (deliverable 3) | D9 | no interface: `[smoke-budget]` values and comments only (intra-module) | P5 |
| P7 | The audit's smoke part: `[run] audit`, and the count shared with the membership ratchet (re-scope "The audit judges"; deliverable 3 "The count") | D1; D13; D14 | IF-049 (a new `audit` value and its `.desc`; the section's shape is unchanged) | P6 |
| P8 | Every bar and caller in warn mode: `[run] smoke`, `[step:smoke]`, the CI `smoke-budget` job, and the step-list test (re-scope "Neither bar fails on seconds"; D-001) | D1; D8; D11; D12 | IF-049 (the `[run] smoke` value and `.desc`); IF-022 (the `[step:smoke]` command value; `[bars] review` is unchanged and resolves through `[run] smoke`) | P7 |
| P9 | The doc homes, and the paired procedure's retirement (deliverable 4; re-scope "Doc homes") | D9 | no interface: prose, skill copies and docstrings only (intra-module) | P8 |
| P10 | The landing: two commits, the RESYNC re-anchor, and the tip's checks (coordinator) | D10; D15 | no interface: landing mechanics only (intra-module) | P9 |

Commits in the lane, in build order:

1. **P1 alone**, the behaviour-preserving move (PROCESS.md §3, 0→A→B).
2. **P2 to P6**, piece B: the meter, the isolation, the keys and their values.
3. **P7**, piece D: the audit.
4. **P8 and P9**, piece C and the docs that describe the split.

D lands before C on purpose. While the bars are in warn mode, the audit
already exists at every lane commit, so the seconds are never judged nowhere.
That is the gap the spec's S1 "Why B, C and D stay together" names. Each
commit passes `run.cmd smoke` as the tree stands at that commit. A row's new
tests are committed with its code. The D1 evidence is each named test's red
run against the pre-change tree (the code reverted in a scratch copy), pasted
into the lane fragment.

## Rows in detail

### P1: the move (commit 1)

**Moves** from `project-trajectory/scripts/agent_session.py` to a new
`project-trajectory/scripts/kitlib/winjob.py`, verbatim apart from the public
names:

- the prototype loader `_win32` becomes `win32`, still
  `functools.lru_cache`d;
- `_JobAccounting` becomes `JobAccounting`;
- the reader `_job_active_processes` becomes `job_active_processes`;
- the `_JOB_BASIC_ACCOUNTING` class number moves with them.

Their docstrings keep their `Implements:` tags. The module docstring carries
`Contracts: IF-<new>`, the row proposed in the table. The module imports only
`ctypes` and `functools`. It touches kernel32 only when `win32()` is called,
so it imports clean on POSIX. Everything else stays in `agent_session` because
its other job code is the kill itself: `_JobPidList`, `_contain_in_job`,
`_terminate_job`, `_open_job_members`, `_job_survivors` and the constants.

**Reachability.** `agent_session` binds the moved objects under their old
names, `from kitlib.winjob import win32 as _win32, JobAccounting as
_JobAccounting, job_active_processes as _job_active_processes`, so every name
`tests/test_session_stdin.py` reaches still resolves:

- `agent_session._win32()` (line 560);
- `monkeypatch.setattr(agent_session, "_job_active_processes", ...)` (line
  513). This one keeps biting because `_job_survivors` stays in
  `agent_session` and resolves the module global at call time.

The probe ran this exact construction: 29 passed, with the file unchanged.

**The kit-side records:**

- **The bootstrap manifest.** `kitlib/bootstrap_manifest.py` `MAPPING` gains
  the `scripts/kitlib/winjob.py` row with its purpose comment. A shipped
  `agent_session` imports it, and LLR-181 states that every kitlib module is
  a `MAPPING` row, so a scaffold receives the package whole.
  `tests/test_bootstrap.py`'s file lists follow if they enumerate kitlib
  (session-protocol §3).
- **LLR-026's traced cells.** The `module` cell appends
  `project-trajectory/scripts/kitlib/winjob.py`. The `code_symbol` cell
  replaces `_win32` with `win32` and `_job_active_processes` with
  `job_active_processes`. These are traced cells, not approved ones (§A5.1;
  see the divergence above). Status, `detail` and `rationale` are unchanged.
- **One new IF row**, `[interface.IF-<next free>]`, status Drafted:
  - owner `scripts/kitlib/winjob`;
  - requestors `["scripts/agent_session"]`;
  - channel `call`;
  - data `win32() -> (kernel32, ntdll) with the job prototypes declared;
    job_active_processes(job) -> int`;
  - component CMP-008;
  - a rationale that names IF-297 as the nearest existing row;
  - a note that the root `conftest.py` (after P2) and
    `scripts/check_smoke_budget.py` (after P3), both outside the arch map,
    also call it.

  It is authored as a spine-cell edit per recipes §5, byte-exact TOML.
- **The RESYNC entry.** One `RESYNC_PACK.md` §3/§4 entry, `### The Windows
  job helpers move into kitlib/winjob.py [since <lane base>]`: a
  behaviour-preserving move with no adopter action, where the new file
  arrives with the kit-owned overwrite. `scripts/check_resync.py` needs the
  entry in this commit, anchored at the commit's trunk base. P10 re-anchors
  it at the landing's parent (D10).
- **Generated views.** `components.derived.toml`, `docs/interface-reference.md`
  and the arch map follow the recipes' landing regeneration list. A lane
  commit carries them only where its own `check_docs.py --stale` step names
  them.

**Tests:**

- `tests/test_session_stdin.py` must pass unchanged (D10). It is TC-026's
  method, and it runs.
- New `tests/test_kitlib_winjob.py` (in-process, smoke):
  - `test_the_job_helpers_import_without_loading_kernel32`: importing
    `kitlib.winjob` with `ctypes.WinDLL` stubbed to raise succeeds, and
    `JobAccounting` has the eight fields in order. Before: ModuleNotFoundError.
  - `test_agent_session_reaches_the_shared_helpers`: `agent_session._win32
    is winjob.win32`, and the same for `_JobAccounting` and
    `_job_active_processes`. Before: ModuleNotFoundError.
- `tests/test_mapping_purpose.py`, `tests/test_kit_path_invariant.py` and
  `tests/test_bootstrap.py` run on the new `MAPPING` row.
- `check_trajectory.py --strict` and `trace.py --strict` are clean. The
  connectivity WARN is gone once the IF row names the module.

### P2: the conftest imports the shared module, then gains its private job

**First, the import (F1; D-007 Q3 (a)).** This half is behaviour-preserving,
and the existing `tests/test_cpu_cap.py` pins prove it before the private
mode is added.

- **`kitlib/winjob.py`'s `win32()`** gains the four kernel32 prototypes only
  the conftest declares today: `SetInformationJobObject`, `IsProcessInJob`,
  `GetCurrentProcess` and `SetPriorityClass`, with the conftest's exact
  `restype`/`argtypes`. The change is additive. The two prototypes both
  files declare today (`CreateJobObjectW` and `AssignProcessToJobObject`)
  are already identical, and `win32()` already loads kernel32 with
  `use_last_error=True`, as the conftest does. `agent_session`'s calls are
  unchanged. The IF row's data cell names the four.
- **The root conftest** drops its own `ctypes.WinDLL("kernel32", ...)` and
  its prototype block. `_bound_windows` takes `k32, _ = winjob.win32()`. A
  small `_winjob()` reaches the module: it appends
  `project-trajectory/scripts` to `sys.path` when that entry is absent, then
  runs `from kitlib import winjob`. The reach is lazy, inside
  `_bound_windows`, so POSIX and a cap of `off` never import it. Appending
  instead of prepending means the path cannot shadow a stdlib module before
  `tests/conftest.py`'s `_put_scripts_on_path` moves `scripts/` to the front,
  as it already does. Only one `kitlib` exists on the path, so the append is
  enough, and the conftest and `agent_session` share one module object
  (`sys.modules["kitlib.winjob"]`) and one cached prototype set. `kitlib`'s
  `__init__` imports nothing, and `winjob` imports only `ctypes` and
  `functools`, so the root conftest pulls in no other kit script.
- **What stays in the conftest** is what only the cap does: the `RATE`
  structure, `ENABLE`/`HARD_CAP`/`CPU_RATE_INFO_CLASS`/`BELOW_NORMAL`,
  `capped()`, the named-then-private choice and its warning. The cap's rate,
  `HARD_CAP` and `BelowNormal` are unchanged. Moving the cap itself into the
  kit module is not owed: no other caller sets a CPU rate, and the ruling asks
  for the import, not for the conftest's whole logic in the kit.

**Then, the private-job input (deliverable 2).** `_bound_windows` reads one
new declared input, `PYTEST_CPU_CAP_JOB`:

- **absent or blank:** today's behaviour (the named `ai-template-pytest`
  job, with the private fallback).
- **`private`:** the run skips the named job. It creates and caps an unnamed
  job, the fallback's existing construction (`CreateJobObjectW(None, None)`
  plus `capped`), and emits no fallback warning, since the private job was
  asked for.
- **any other value:** a stderr line naming the value, then today's
  behaviour. The conftest is never fatal (its docstring), and the step only
  ever sets `private`, which P4 pins.

The cap's rate, `HARD_CAP` and `BelowNormal` priority are unchanged in both
modes. Under `private`, an xdist worker, or a per-test `pytest` child run
from the root, creates its own unnamed job nested in its parent's. That is
the fallback's topology, already pinned by
`test_a_run_that_is_already_jobbed_gets_its_own_ceiling`, and the ancestor
cap still bounds it. POSIX is unchanged (`os.nice(5)`).

**Tests**, in `tests/test_cpu_cap.py` (it already holds the conftest's
topology pins; slow or smoke as that module already sits):

- `test_a_private_run_joins_no_named_job` (Windows): a child applies
  `_bound_windows(25)` with `PYTEST_CPU_CAP_JOB=private` and a test-unique
  `JOB_NAME`. The test's own `CreateJobObjectW(None, <name>)` then reports a
  new object (`GetLastError() != 183`). The child self-reports
  `IsProcessInJob(me, NULL)` true and its below-normal priority class.
  Before: the input is ignored, so the named job exists and the 183 check
  fails.
- `test_the_job_mode_reads_its_one_value` (all platforms, in-process): the
  mode reader maps absent/blank to named and `private` to private, and maps
  any other value to named with a stderr line naming it. Before: the reader
  does not exist (AttributeError).
- `test_the_root_conftest_takes_its_prototypes_from_the_shared_module`
  (Windows, F1): a subprocess child loads the root `conftest.py` by path,
  imports `kitlib.winjob` and replaces `winjob.win32` with a recorder. The
  recorder returns a fake kernel32 whose functions log their calls and
  return truthy handles. The child sets a test-unique `JOB_NAME`, calls
  `_bound_windows(25)` and prints the log as JSON. The test asserts that the
  recorder was called, and that the log holds, in order,
  `CreateJobObjectW(None, <name>)`, a `SetInformationJobObject` with class 15
  and rate 2500 under `ENABLE|HARD_CAP`, `AssignProcessToJobObject`, and
  `SetPriorityClass(<me>, 0x4000)`. It also asserts that
  `conftest._winjob()` is `sys.modules["kitlib.winjob"]`, so the conftest
  reaches the one module `agent_session` imports (P1's
  `test_agent_session_reaches_the_shared_helpers` pins that side). Before: the conftest builds its own `WinDLL`, so the
  recorder is never called and the log is empty. (It runs in a child because
  before the change the real job is joined, and a child keeps that off the
  test process.)
- `test_this_live_process_runs_under_the_hard_cap_it_asked_for` and
  `test_a_run_that_is_already_jobbed_gets_its_own_ceiling` run unchanged.
  They are the proof that the import preserved the cap, the priority and the
  fallback topology.

### P3: the shared module's reading (B, Windows half)

`kitlib/winjob.py` gains the following. `GetCurrentProcess`, which the join
needs, already arrived in P2.

- **`create_joined_job()`**: an unnamed job, with the calling process
  assigned to it. That nests in the venv launcher's job, as the spec's probe
  measured for an empty job. It raises `OSError` (WinError) on either
  failure.
- **`job_cpu_seconds(job)`**: `(TotalUserTime + TotalKernelTime) / 1e7` from
  the same basic-accounting query.

`job_active_processes` and `job_cpu_seconds` share one private
`_accounting(job)` query, so the struct is read in one place. The IF row's
data cell gains both names in this commit.

**Tests:** `tests/test_kitlib_winjob.py` gains:

- `test_a_joined_job_counts_an_exited_grandchild` (Windows, a subprocess
  driver): the driver calls `create_joined_job()`, burns, starts and waits on
  a child that starts and waits on a grandchild that burns, then prints
  `job_cpu_seconds`. The result is at least the sum of the burns.
- `test_the_cpu_reader_sums_user_and_kernel_time` (all platforms): the query
  is stood in to fill fixed `TotalUserTime`/`TotalKernelTime` values, and
  the reader returns their sum in seconds.

Both fail before (AttributeError: no such function). The first lives in
P5's slow module.

### P4: the step (B)

`scripts/check_smoke_budget.py` is rewritten around small functions, each its
own seam for the in-process tests. Each item below is in exit-precedence
order (deliverable 3).

1. **Arguments.** `--mode warn|enforce` only. `--elapsed` is removed, so
   argparse refuses it as unrecognised and exits 2.
2. **`declared_limits(cp)`.** It returns `cpu-seconds`, `wall-seconds` and
   `max-tests` as positive numbers (`max-tests` an int), validated in both
   modes. It raises a `Refusal` naming `docs/stack.ini` and the key for each
   of these cases:
   - an absent or unreadable file (`_profile()` reads None);
   - an absent section;
   - an absent key;
   - a blank, non-numeric, non-finite or non-positive value.

   `main` turns a `Refusal` into exit 2 before any tier run. `seconds` is no
   longer read anywhere.
3. **`select_meter(platform=sys.platform)`.**
   - `win32` gives the job meter. Its `start()` calls
     `winjob.create_joined_job()` and records `job_cpu_seconds`, and its
     `stop()` returns the delta.
   - Any other platform where `importlib.import_module("resource")` succeeds
     gives the rusage meter: the change in `getrusage(RUSAGE_CHILDREN)`
     `ru_utime + ru_stime` across the run.
   - Anything else is a `Refusal` (exit 2): "no CPU meter on <platform>".

   An `OSError` from `start()` is a `Refusal` too, raised before the spawn.
   There is no wall-only path.
4. **The tier run.** `smoke_argv(cp)` is unchanged (the `[product] test`
   plus `[tiers] smoke` line). It runs once through `subprocess.run` with
   `env = os.environ` plus `PYTEST_CPU_CAP_JOB=private`, and the wall time
   is taken with `time.perf_counter` around it. The meter starts just before
   the spawn and stops just after the wait. Nothing else starts between the
   two, which is the rusage reading's premise. An `OSError` from `stop()` is
   a failed reading: recorded, not raised.
5. **The count** (enforce only; P7 adds it after the reading, outside it).
6. **The report.**
   - The verdict line:
     `smoke budget: CPU 512.3 s vs 900 s cpu-seconds; wall 41.2 s vs 600 s
     wall-seconds; meter windows-job (or getrusage); 8 logical CPUs ->
     within|OVER`.
   - A failed reading prints `smoke budget: CPU reading FAILED (<cause>);
     wall ...` instead.
   - Each limit over adds a `WARN:` (warn) or `FAIL (enforce):` line naming
     the limit and its key, with the GitHub annotation as today.
   - A red tier keeps its `note: smoke tier exited N` line.
7. **The exits**, in order: a `Refusal` gives 2; a red tier gives its own
   code, in both modes; a green tier with a failed reading (or, after P7, a
   failed count) gives 2; enforce with any limit over gives 1; warn gives 0;
   otherwise 0.

The docstring is replaced: the step's callers, modes, the two meters, their
stated bounds (POSIX counts only reaped descendants, a stated under-count),
and the private-job input. The 2026-08-21 wall re-argument moves out, since
P6's header carries the measurements.

`tests/test_stack_profile.py`'s `check_smoke_budget._profile` site follows
the reader. Its call becomes `declared_limits(_profile())`, its texts carry
the three keys, and its expected outcomes per class are unchanged. The
"valid", "bom", "upper" and "stray"-ruled outcomes become the limits tuple;
the others still raise. The loader's behaviour (WI-915) is what that site
pins, and it does not change.

**Tests:** `tests/test_check_smoke_budget.py` is rewritten in-process (smoke
tier). Every case drives `main(argv)` with three stand-ins:

- a tier: `smoke_argv` patched to an interpreter command that exits N, or
  `run_tier` patched to a recorder;
- a meter: `select_meter` patched to return a fixed reading, or to raise;
- limits: a tmp `stack.ini` with `STACK_INI` patched, where real parsing is
  the point.

The four `--elapsed` subprocess cases become the first four below (D8).
"Before" means today's step: its names (`select_meter`, `declared_limits`)
do not exist, so `monkeypatch.setattr` raises AttributeError, unless the
case says otherwise.

| Case | What it pins | Fails before |
|---|---|---|
| `test_within_both_limits_exits_zero_in_both_modes` | D5 | AttributeError |
| `test_over_a_limit_fails_enforce_naming_it` (cpu-seconds, wall-seconds) | 1, with `FAIL (enforce):` naming the limit and key (D5) | AttributeError |
| `test_over_a_limit_warns_and_passes_in_warn_mode` | 0, with `WARN:` naming it (D5) | AttributeError |
| `test_a_red_tier_exits_with_its_own_code_and_the_verdict_line` (both modes) | D5 | AttributeError; the old line is "wall-clock budget" |
| `test_a_red_tier_with_a_failed_reading_names_both` | the tier's code, with the reading-failed line and the note (D5) | AttributeError |
| `test_a_green_tier_with_a_failed_reading_exits_two` | D5 | AttributeError |
| `test_a_broken_key_refuses_before_the_tier_starts` (cpu-seconds, wall-seconds, max-tests × absent, blank, `abc`, `0`, `-5` × warn, enforce; plus an absent section and an absent file) | 2, naming the file and key; the tier recorder was never called (D6) | today a broken `cpu-seconds` or `max-tests` is never read, so the tier starts |
| `test_a_platform_without_resource_refuses_before_the_tier_starts` | `select_meter("plan9")` with `sys.modules["resource"] = None`: 2, naming the platform, tier never started (D6) | AttributeError |
| `test_a_job_that_cannot_be_made_refuses_before_the_tier_starts` | `select_meter("win32")` with `winjob.create_joined_job` patched to raise OSError, so it runs on every platform: 2, naming the error, tier never started (D6) | AttributeError |
| `test_the_verdict_line_names_cpu_wall_meter_and_cpu_count` | the reading and `cpu-seconds` value, the wall and `wall-seconds` value, the meter name, and `os.cpu_count()` logical CPUs (D7) | the old line names only wall and the 60 s budget |
| `test_elapsed_is_refused_as_an_unknown_argument` | `main(["--elapsed", "5"])` raises SystemExit(2), with stderr "unrecognized arguments: --elapsed" (D8) | it returns 0 |
| `test_the_tier_runs_under_the_private_cap_job` | the recorder sees `PYTEST_CPU_CAP_JOB=private` in the tier's env and one tier call (D4's construction) | no env is passed |

The new in-process cases join the smoke tier. If they take it past
`max-tests`, P6 re-stamps the ceiling from the measured count, with its
`fig:` line and log reason, in this commit.

### P5: the platform readings (B, tests)

A new `tests/test_smoke_budget_meter.py`, added to `tests/conftest.py`
`SLOW_MODULES` (subprocess and CPU burns; every script family keeps its
in-process pin in P4). On Windows the step joins its process to a job for
good, so these cases run the step in a **subprocess driver**: a short script
in `tmp_path` that loads `scripts/check_smoke_budget.py` by path, sets
`smoke_argv` to the stand-in tier and calls `main(["--mode", "warn"])`. The
test parses `CPU <x> s` from the verdict line. Burns are CPU burns (loop
until `time.process_time()` reaches the target), not sleeps.

- **`test_a_windows_reading_counts_the_exited_grandchild`** (skipped off
  Windows, D2). The stand-in tier burns 0.5 s, then starts and waits on a
  grandchild that burns 0.5 s. Asserts reading ≥ 1.0 s. Before: the step
  prints no CPU reading, so the parse fails.
- **`test_a_posix_reading_counts_a_waited_grandchild`** (skipped on Windows,
  D3). The same construction, read through `getrusage`. It runs in CI's
  Linux and macOS `test` jobs. The builder also runs it once on WSL Ubuntu
  and records the result in the fragment. Before: no CPU reading.
- **`test_an_outside_process_cannot_raise_a_reading`** (Windows, D4).
  - **The tier.** The stand-in tier loads the root `conftest.py` by path,
    with a minimal `pytest` stub in `sys.modules` (just `hookimpl` returning
    an identity decorator) so its startup CPU stays small. It sets
    `conftest.JOB_NAME` to a test-unique name, then calls
    `conftest._bound_windows(50)` directly, so the cap applies even where
    CI sets `PYTEST_CPU_CAP=off`. Its env is the one the step gave it. It
    then writes a ready file, waits for a go file, burns 0.3 s and exits.
  - **The outsider.** Once the tier is ready, the test starts it as its own
    child, outside the driver's job. It runs `CreateJobObjectW(None,
    <name>)`, records whether the object already existed (`GetLastError() ==
    183`) and whether `AssignProcessToJobObject(self)` succeeded, burns
    1.0 s, and prints both as JSON. Then the test writes the go file.
  - **The assertions.** (a) The outsider found no existing job by that name.
    That bites on every box, jobbed or not, because under the old named mode
    the tier's conftest created it inside the step's job. (b) The reading is
    below 0.3 s plus a **stated margin of 0.5 s**, so a contaminated reading
    (≥ 1.3 s) fails. The builder measures the stand-in's no-outsider reading
    five times. If the highest exceeds 0.3 + 0.35 s, the stand-in's imports
    shrink before the margin is accepted. The margin is never widened, and
    the five readings go in the fragment.
  - **Before:** no CPU reading, and P2's private mode does not exist, so (a)
    fails on the named job.

### P6: the stamped values (B, values)

The readings are taken on the B working tree with the step in warn mode. The
keys are set locally to provisional values for the run only, never committed.
The committed values are the measured ones:

- three or more readings in this workstation's quietest windows;
- three or more under the builder's own parallel jobs (two concurrent
  `pytest -q -n auto -m smoke` runs beside the measured one);
- one on WSL Ubuntu.

**The stamps:**

- **`cpu-seconds`** = the highest loaded reading plus 25 %, rounded up to the
  next 10 s. That stated count goes in the header comment.
- **`wall-seconds`** clears the ordinary loaded readings on record (58.7 to
  287 s, D-007 Q1 (a)) and every wall reading this lane takes. 600 s is
  proposed: it clears 287 s about twice over and stays far below the 1832 s
  window. It goes in only if no lane reading comes near it.
- **`seconds = 60`** and its trailing re-stamp prose are deleted, so no
  reader keeps 60.
- **`max-tests`** keeps its value unless P4's or P7's in-process cases cross
  it, in which case it is re-stamped from the count with its own `fig:` line.

**The hold** (spec B4). If the loaded readings spread too wide for one value
(highest over lowest above 1.5 across the six workstation readings), or the
WSL reading exceeds the budget, the lane holds before the stamp, for the
owner.

**The record.**

- Each value gets a `# fig: cmd="python scripts/check_smoke_budget.py --mode
  warn" rev=<sha>` line.
- The `[smoke-budget]` header is rewritten to state the split: `cpu-seconds`
  budget, `wall-seconds` cap, and `max-tests` ceiling, all judged by the
  audit and only reported by the bars.
- `check_figures.py` passes.
- The lane fragment (session-protocol §4) records every reading: CPU, wall,
  CPU count, meter, the window (quiet/loaded/WSL), the spread, and the
  margin arithmetic (D9).

### P7: the audit's smoke part (D)

- **`[run] audit`** is `python scripts/check_smoke_budget.py --mode enforce`.
  Its `audit.desc` says it is the audit's smoke part (review-churn item 12),
  run by hand and at phase close, with a breach filed as a re-tier row.
  `arch` and `hats` are item 12's rows and are not built here. `run.cmd
  audit` and `run_menu.py audit` reach it with no launcher change.
- **The count's home** is the step: `count_smoke_tier(run=subprocess.run)`
  in `scripts/check_smoke_budget.py`. With it moves `_run_pytest_collect`,
  which keeps the `-X utf8` M-01 lesson. It runs `python -X utf8 -m pytest
  --co -q -m smoke` from the repository root and counts the stdout lines
  carrying `::`. It raises `CountFailed` on a nonzero exit or a zero count.
- **In the step.** In enforce mode `main` calls it after `meter.stop()`, so
  the count is outside the reading, red tier or green. It prints `smoke tier
  count: N tests vs M max-tests -> within|OVER`. An over count is a limit
  over (exit 1 when green). A failed count is 2 after a green tier, and
  named beside a red tier's own code. Warn mode never calls it.
- **The ratchet.** `tests/test_smoke_budget.py`'s `_collected_smoke_count`
  and `_run_pytest_collect` are replaced by the step's function, loaded by
  path. The ratchet asserts `count <= max-tests` through it, so the two
  cannot count differently. Its message stops quoting `_budget("seconds")`
  (now absent). `test_nested_collection_survives_a_non_utf8_console_byte`
  calls the moved `_run_pytest_collect`.

**Tests:** in-process, smoke tier, in `tests/test_check_smoke_budget.py`
(the stand-in counter is `count_smoke_tier` patched):

| Case | What it pins | Fails before |
|---|---|---|
| `test_a_count_at_max_tests_passes_and_one_past_fails` (enforce) | 0 at the ceiling; 1 one past it, naming `max-tests` (D14) | AttributeError: no `count_smoke_tier` |
| `test_a_failed_or_empty_count_exits_two` (counter raising `CountFailed` for a nonzero collect and for zero ids) | 2, naming the failed count (D14) | AttributeError |
| `test_a_red_tier_over_max_tests_keeps_its_code_and_names_the_count` | D14 | AttributeError |
| `test_warn_mode_never_starts_the_counter` | the recorder is uncalled (D14) | AttributeError |
| `test_the_count_runs_after_the_reading_stops` | the event order is meter start, tier, meter stop, count (deliverable 3, "outside its reading") | AttributeError |
| `test_the_count_reads_node_ids_from_a_collect_only_run` | a `run` stand-in returning canned `--co -q` output gives the `::`-line count; returncode 1 or no ids raises `CountFailed` | AttributeError |
| `test_the_ratchet_and_the_step_count_through_one_function` | `tests/test_smoke_budget.py`'s count function is the step's `count_smoke_tier` (identity) (D14) | the ratchet has its own `_collected_smoke_count` |
| `test_the_audit_runs_the_step_in_enforce_mode` | `[run] audit`'s value, split on `&&`, holds one step, `python scripts/check_smoke_budget.py --mode enforce` (D13) | KeyError: no `audit` key |
| `test_the_audit_fails_over_each_limit_naming_its_key` (cpu-seconds, wall-seconds, max-tests) | `main` over the parsed `[run] audit` argv with stand-ins over one limit: 1, naming the limit and key (D13) | KeyError |

The audit is also run once from `run.cmd audit` on the B+D tree, and its
output goes in the fragment. P10 runs it again on the landing tip.

### P8: every bar and caller in warn mode (C)

- **`[run] smoke`'s last step** becomes `python scripts/check_smoke_budget.py
  --mode warn`. Its `.desc` says the tier runs once and its CPU and wall are
  reported, while the audit judges them. `[bars] review` stays `python
  project-trajectory/scripts/run_menu.py smoke`, and it takes warn mode
  through that line (spec S1 C).
- **`[step:smoke]`** `command` becomes `{py} scripts/check_smoke_budget.py
  --mode warn` (D-001).
- **The CI job.** `.github/workflows/test.yml`'s `smoke-budget` job step runs
  `python scripts/check_smoke_budget.py --mode warn`, and the step's name
  says warn (D-001).
- **The template.** The shipped `project-trajectory/stack.ini.template`
  carries only a commented `[step:smoke]` placeholder and no budget step,
  and no shipped workflow calls the step (grep), so no template copy
  changes.
- **The step-list test.** In `tests/test_smoke_budget.py`,
  `test_the_declared_commit_bar_runs_the_strict_lints_before_its_budget`
  changes only the mode token of its last expected step, which is D11's
  change. D8's "passes on the unchanged `[run] smoke` line" holds in the
  sense that `--elapsed`'s retirement needs no change to the line, since no
  step ever called it. The re-scope overrides D8 where they differ (spec,
  "Owner re-scope"). The test still asserts the budget step is last and the
  only tier run. Before the change it fails on the `--mode warn` token.

**Tests** (in-process, smoke):

| Case | What it pins | Fails before |
|---|---|---|
| `test_neither_bar_fails_on_seconds` (`[run] smoke`; `[bars] review`, resolved through `run_menu.py smoke` to `[run] smoke`) | the bar's budget-step argv is parsed from `docs/stack.ini`, and `main(argv)` with a green stand-in tier and a stand-in meter over both limits returns 0 and prints WARN lines naming `cpu-seconds` and `wall-seconds` (D11) | the parsed argv is `--mode enforce`, which returns 1 |
| `test_a_red_tier_still_fails_each_bar` | the same argv with a stand-in tier exiting 3 returns 3 (D11) | AttributeError on the stand-in meter |
| `test_every_other_caller_runs_warn_mode` (`[step:smoke]` command; the CI `smoke-budget` job's `run:` line, found by text under `smoke-budget:`) | each carries `scripts/check_smoke_budget.py --mode warn` and no `--mode enforce` (D12) | both read enforce |

### P9: the doc homes (C, deliverable 4)

Each home says that the bars run the tier once and report its CPU-seconds and
wall, failing only on a red tier, and that `run.cmd audit` judges the three
limits. Each home retires the paired-reading procedure. The homes:

- **CLAUDE.md**, the "Self-test before claiming done" bullet. Seconds are
  reported by the bar and judged by the audit. The "60 s wall ... a breach
  FAILS the bar" clause and the WI-652 re-measure sentence are replaced, not
  appended to. The file has 341 bytes free (8,159 of 8,500), so the rewrite
  stays net-neutral or shorter. `byte-budget-guard`'s table row records the
  delta, and all three copies of that skill stay byte-identical.
- **session-protocol §3.** The "results AND seconds" paragraph and the
  `--mode enforce` wording.
- **coordinator-cycle SKILL §3.** "the landing's smoke budget reading is
  taken quiet" goes.
- **coordinator-cycle recipes §6.** The `[bars] review` "refuses on a
  breach" bullet, the budget-step bullet and the parent-timing bullets.
- **coordinator-cycle recipes §4.** The "time the smoke tier beside trunk's
  tip" rebase bullet is pared to its test-module half, since a paired
  timing is no longer owed.
- **coordinator-cycle recipes §7.** "A smoke budget breach under load" is
  retired with D-005, D-011 and D-004's and D-012's budget clauses. The
  below-normal-priority rule stays.
- **`docs/registry-machinery-reference.md` §9.2.** The `[smoke-budget]`
  paragraph names the three keys.
- **`docs/stack.ini`.** The `[smoke-budget]` header (P6) and the `[run]
  smoke` `.desc` (P8).
- **`test.yml`.** The `smoke-budget` job comment and the workflow-level
  `PYTEST_CPU_CAP` comment, which no longer cites an enforced wall-clock
  number.
- **The step's and the root conftest's docstrings.** The conftest's "CI sets
  it off (... a wall-clock smoke-budget job)" and the new
  `PYTEST_CPU_CAP_JOB` dial.

The skill copies (`project-trajectory/skills/`, `.claude/skills/`,
`.agents/skills/`) stay byte-identical (`tests/test_skills_sync.py`). Both
skills are `scope: this-repo`, so none of this ships and no RESYNC entry is
owed for it.

**Checks:** a grep over the deliverable-4 files for "paired", "parent
reading", "same window" and "beside its parent" finds nothing left of the
procedure (D9), and the result goes in the fragment. `check_docs.py --root .
--stale` is green.

### P10: the landing (coordinator)

The landing keeps P1 as its own commit ahead of the squashed B, D and C
commits (D10). The RESYNC entry is re-anchored from the lane base to the
landing's parent (recipes §3).

On the landing tip:

- `run.cmd smoke` is green;
- `run.cmd audit` is run once on a quiet box, and its verdict and count lines
  are recorded in the fragment;
- `check_trajectory.py --strict` and `trace.py --strict` are clean (D15);
- the recipes' generated views are regenerated (components, interface and
  CLI references).

WI-957's D-004 hold is released by this landing (spec "Order"). Its attest
then refuses only a red bar, and that is recorded for the coordinator, not
built here.

## Open points for the coordinator (not built)

1. **The spine divergence above.** P1 updates LLR-026's traced cells and
   adds one Drafted IF row, against the spec's "no LLR or IF row". The probe
   shows the `--strict` ERROR without the first edit.
2. **The CI readings** (Linux `smoke-budget` job, macOS `test` job) wait for
   the owner's push. They are recorded as a decision after landing, and a
   breach there is a finding, not a re-stamp (spec B4, D-007 Q2 (a)).
