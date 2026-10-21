+++
id = "WI-940"
title = "No bar fails on the smoke tier's seconds; the run menu's audit judges the tier's own CPU-seconds, which other load does not move, under a looser wall-clock cap"
workstream = "process"
sr_refs = []
specref = "docs/decisions/coordinator-2026-10-17.toml"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = ["~WI-915", "~WI-916"]
+++

## Context

The bar's last step, `scripts/check_smoke_budget.py --mode enforce`, runs the
smoke tier once. It fails the bar when the tier's wall time exceeds
`docs/stack.ini` `[smoke-budget] seconds` (60). Wall time moves with the
rest of the box. The record shows 33 to 47 s quiet, and 58.7 to 287 s while
the owner's applications or the coordinator's parallel jobs ran. Once, at
below-normal priority, it reached 1832 s (coordinator-2026-10-16 D-012;
coordinator-2026-10-17 D-004, D-005). So each commit's reading is paired by
hand with its parent's, taken in the same window (recipes §7; D-005).

The owner ruled in session on 2026-10-17 (coordinator-2026-10-17 D-007,
recorded at filing): "the spirit of the smoke tests is just to prevent
egregiously heavy / long repetitive tests, but we never know what other
items will be running on the computer or what priority the smoke test has
been given." Offered a load-scaled wall budget or a CPU-time budget, the
owner chose the CPU-time budget. D-005's paired procedure stays until this
row lands.

**The anchor.** No spine row names the bar's budget. A grep of the
requirement and test-case registries for `check_smoke_budget`, `smoke`,
`budget`, `wall` and `CPU` finds three things only: the performance-budget
layer (SR-015, SR-167, the PB registry), SR-177's fan-out telemetry, and the
Smoke `tier` cells. `scripts/` is this repository's own tooling, outside the
traced product, and WI-281, WI-496, WI-652, WI-869 and WI-935 changed this
step without amending a spine row. As in WI-935, the anchor is SN-007
(approved): "The declared bar is green before a change lands." SN-008 rules
out a silent fallback. No LLR, TC or IF row is amended, since IF-022 does not
cover `[smoke-budget]`.

**Measured before drafting** (probes in the coordinator's scratch,
2026-10-17):
- **Windows** (this workstation, 3.11.9). An unnamed job's basic accounting
  counted a child and a grandchild after both had exited (1.28 s for 1.0 s
  of burns plus startups). It counted a child's own nested job (1.30 s), and
  CPU a process had used before it joined (0.47 to 0.50 s).
- **Contamination, Windows.** An outside process in no job joined a NAMED
  job nested in the accounting job. Its 2 × 1.0 s burn entered the reading,
  which rose from 0.58 s to 2.67 s. The root conftest's cap job is named
  (`ai-template-pytest`). A tier controller that creates it first nests it in
  the step's job, so an unjobbed run that joins it counts against the tier.
  A venv-launched interpreter, already in its launcher's job, was refused
  (error 5).
- **Linux** (WSL Ubuntu, 3.12.3). `getrusage(RUSAGE_CHILDREN)` and
  `os.times()`'s children fields counted a waited grandchild (0.66 s for
  0.6 s) and one in a new session. They did not count a grandchild orphaned
  before its 0.5 s burn (0.02 s).
- **The local Python 3.11.9 docs.** `RUSAGE_CHILDREN` is "child processes
  of the calling process which have been terminated and waited for", and
  `resource` is "Unix, not Emscripten, not WASI". On Windows, `os.times()`
  knows "only user and system". The docs are silent on grandchildren. That
  rule is getrusage(2)'s, checked on Linux only.

## Owner re-scope (2026-10-20)

The owner ruled in session on 2026-10-20 (coordinator-2026-10-20 D-014, on
wi-957 D-004): "This keeps coming up, I think we need to drop that budget
from the review bar and find a better way to keep an eye on a slower than
expected smoke bar. Maybe something that can be added into the auditing pass
from the run module." Asked whether the per-commit bar keeps failing on the
budget, the owner chose to drop it from both bars; asked what becomes of
this row, the owner folded it into the audit's smoke part. This overrules
the bar's "a breach FAILS the bar" (OI-52 ruling (a), 2026-08-23) for
seconds only. It overrides the deliverables below where they differ:

- **Neither bar fails on seconds.** `[run] smoke` (the per-commit bar) and
  `[bars] review` (the attestation's review bar) run the budget step in
  `--mode warn`: the tier runs once, a red tier still fails the bar with its
  own code, and the verdict line still prints the reading, so a slow tier
  stays visible on every commit. The paired-reading procedure (D-005,
  D-011) retires with the gate it served.
- **The audit judges.** A new `[run] audit` action, the first part of the
  review-churn plan's item 12 `run.cmd audit` (ruled in revision 35 as one
  manual action; its `arch` and `hats` parts are item 12's rows), carries a
  `smoke` part: the budget step in `--mode enforce` against the stamped
  `cpu-seconds` and `wall-seconds` (deliverables 1 to 3, unchanged), plus
  the tier's test count against `max-tests`. It is run by hand and at phase
  close, and a breach is filed as a re-tier row, never charged to whatever
  lane happened to run it.
- **Doc homes** (deliverable 4) state the new split: CLAUDE.md's
  "Self-test before claiming done" bullet says seconds are reported by the
  bar and judged by the audit, within its byte budget.
- **Order.** It lands before WI-957, which it releases from the D-004 hold
  (WI-957's attest then refuses only a red bar).
- The scope critique re-runs over this re-scope before the claim.

## Deliverables

1. **The CPU reading, per platform, from the stdlib only.**
   - **Windows** (`ctypes` over kernel32, through deliverable 6's shared
     module). Before the spawn, the step creates an unnamed job and joins it
     itself, nesting in the venv launcher's job.
     Every tier process is then born in the job. The reading is the job's
     `TotalUserTime + TotalKernelTime` after the tier exits, minus that sum
     just before the spawn. Exited processes, orphans and nested jobs count.
   - **Linux, macOS, and any platform where `resource` imports:** the change
     in `getrusage(RUSAGE_CHILDREN)` user plus system time across the run,
     with nothing else started meanwhile. This covers the tier, its xdist
     workers (execnet 2.1.2 waits on each at teardown), and every descendant
     its parent waited for.
   - **Anywhere else**, or when the job cannot be created or joined: exit 2
     (deliverable 3). There is no wall-only verdict and no fallback.
2. **No outside process adds CPU to a reading.** The step runs the tier so
   that its tree creates and joins no job another process can open by name.
   The plan settles the construction. The candidate: the root conftest gains
   one declared input that makes a run take its existing private (unnamed)
   capped job, and the step sets it. The cap's rate and its below-normal
   priority stay. POSIX needs no construction, because its reading counts
   only the tier's own reaped descendants.
3. **The declared values and the verdict.**
   - **Keys.** `[smoke-budget]` gains `cpu-seconds` (the budget) and
     `wall-seconds` (the looser cap). `seconds` retires, so no reader keeps
     60 as a budget. `max-tests` is unchanged in value, and the step now
     reads it too (the audit's count, below).
   - **The count (the audit's `max-tests` judgment).** In enforce mode,
     after the timed tier run and outside its reading, the step counts the
     smoke tier: the test node ids a collect-only `-m smoke` run from the
     repository root collects. That is the definition
     `tests/test_smoke_budget.py`'s membership ratchet applies today, and
     both read it through one counting function (the plan settles its home),
     so the audit and the ratchet cannot count differently. The ceiling is
     inclusive, as the ratchet's: at `max-tests` passes, one past it is over.
     A collect-only run that exits nonzero, or that yields no node id, is a
     failed count, never a pass. Warn mode, the bars' form, does not count:
     the bars keep judging membership through the ratchet, which runs inside
     the tier (the owner's re-scope overrules seconds only).
   - **Values.** Each is stamped from a measured baseline, never invented,
     with its `fig:` line and log reason. For CPU: three or more readings in
     this workstation's quietest windows, three or more under the builder's
     own parallel jobs, and one on WSL Ubuntu (recipes §7). The budget sits
     above the highest loaded reading by a stated count. The wall cap clears
     the ordinary loaded readings on record (D-007).
   - **Report.** One verdict line gives the CPU-seconds against the budget,
     the wall time against the cap, the meter, and the box's logical CPU
     count, which sets the worker count. In enforce mode a second line gives
     the tier's count against `max-tests`. A breach adds a WARN or FAIL line
     naming the limit and its key.
   - **Exits, in precedence order.** First, 2 in both modes, before any
     tier run, for a missing or broken value or meter. Then a red tier's own
     code in both modes (WI-935), naming a failed reading or count too, and
     any limit it measured over (a tier over `max-tests` is usually red
     already, through the ratchet). Then 2 for a green tier whose reading
     failed, or, in enforce mode, whose count failed. Then 1 in enforce mode
     for CPU, wall or count over; warn mode prints WARN and exits 0.
     Otherwise 0. Callers test only for nonzero, and the lines name the
     cause.
   - **`--elapsed` retires.** A bare wall time can give only a wall-only
     verdict. No script calls it, and the recipes' wrapper runs the whole
     bar.
4. **Doc homes.** CLAUDE.md's "Self-test before claiming done" bullet
   (byte-watched); the session-protocol skill's §3; the coordinator-cycle
   skill's §3 ("the landing's smoke budget reading is taken quiet"), its
   recipes §6 budget-step and parent-timing bullets, and its recipes §7 "A
   smoke budget breach under load", where the paired procedure retires
   (D-005, and D-004's and D-012's budget clauses) and the below-normal
   priority rule stays; `docs/registry-machinery-reference.md` §9.2;
   `docs/stack.ini`'s `[smoke-budget]` header and `[run] smoke` `.desc`; the
   `smoke-budget` job comment in `test.yml`; and the step's and the root
   `conftest.py`'s docstrings. Both skills are `scope: this-repo`, and their
   copies stay byte-identical.
5. **RESYNC.** One entry, for deliverable 6's move: a behaviour-preserving
   move with no adopter action, anchored at the landing's parent. The step
   owes none: every other file is this repository's own (WI-935's finding),
   and the shipped template lacks `[smoke-budget]`.
6. **The shared job module, landed first.** `agent_session.py`'s Windows job
   code (the prototypes, the accounting structure and its reader, today the
   private `_win32`, `_JobAccounting` and `_job_active_processes`) moves into
   one shared kit module. The move is its own behaviour-preserving commit
   ahead of the change (PROCESS.md §3). The names `tests/test_session_stdin.py`
   reaches on `agent_session` stay reachable, and the step reads its job
   through the module.

## Trust

`docs/stack.ini` `[smoke-budget]` already holds the value the bar's gate
compares against. This row replaces that one value (`seconds`) with two, so
the file keeps its authority, now over a new value domain. Written before
the claim, under [`PROCESS.md` §3, "When a guard is owed"](../../../project-trajectory/PROCESS.md#3-traceability--anti-duplication).

- **Producer:** a person or agent, editing by hand in a reviewed commit with
  its `fig:` line and log reason (`check_figures.py` checks presence, not
  truth). A failed write is a missing key or a blank, non-numeric or
  non-positive value.
- **Consumers** (grep for `"smoke-budget"` in `*.py`):
  `scripts/check_smoke_budget.py` (the verdict), `tests/test_smoke_budget.py`
  (the `max-tests` ceiling, and a message quoting the budget) and
  `tests/test_check_smoke_budget.py`. After WI-915, the step reads the file
  through the shared loader. After this row the step reads all three keys,
  `max-tests` included, for the audit's count (deliverable 3).
- **The count's path** (the audit's `max-tests` judgment): produced by the
  step's own collect-only `-m smoke` run, through the counting function the
  membership ratchet shares; consumed by the step alone, in the same run, and
  never persisted. It is not a declared value, so it has no producer outside
  that run.
- **Ruling:** the step exits 2, naming the file and the key, and starts no
  tier when the file is absent or unreadable, the section or a key is
  absent, or a value is blank, non-numeric or non-positive. There is no
  built-in default. It validates `cpu-seconds`, `wall-seconds` and
  `max-tests` in both modes, so one broken key refuses every caller alike. A
  failed count (the collect-only run exits nonzero or yields no node id)
  exits 2 naming it, after a green tier, and a red tier's own code wins over
  it (deliverable 3's precedence). The reading itself is no file: it comes from the OS, is
  judged in the same run and is never persisted. The authority binds to the
  working tree's `docs/stack.ini` when the step starts.

## Done-when

Each named test fails on the code before the change.
- **A Windows reading counts the tier's exited grandchild.** A stand-in tier
  burns, then waits on a grandchild that burns; the step's reading is at
  least the sum of the burns. Skipped off Windows.
- **A POSIX reading counts a waited grandchild.** The same, skipped on
  Windows. It runs on WSL and in CI's Linux and macOS test jobs.
- **An outside process cannot raise a reading** (Windows). A stand-in tier
  applies the root conftest's cap under the step's environment. An unjobbed
  outsider opens the conftest's job name and burns 1 s. The reading stays
  below the tier's own burns plus a stated margin.
- **In-process exits**, against a stand-in tier and meter: within both
  limits, 0; over, 1 in enforce or 0 with WARN in warn, naming the limit; a
  red tier, its own code in both modes with the verdict line; a red tier
  with a failed reading, its code naming both; a green tier with a failed
  reading, 2.
- **Refusals** exit 2, name their cause, and assert that the stand-in tier
  never started: an absent, blank, non-numeric or non-positive key
  (`max-tests` included, in both modes); a
  stand-in platform without `resource`; a job stand-in raising `OSError`.
- **The verdict line** names the CPU-seconds and the budget, the wall time
  and the cap, the meter, and the CPU count.
- **`--elapsed`** is refused as an unknown argument. Its cases become
  in-process cases. `tests/test_smoke_budget.py`'s step-list test passes on
  the unchanged `[run] smoke` line.
- **The record.** Both values are stamped from deliverable 3's readings
  with `fig:` lines, and the fragment records every reading and the spread.
  No text in deliverable 4 keeps the paired procedure. The skill copies are
  byte-identical, and CLAUDE.md is within its byte budget.
- **The move** (deliverable 6) lands first, as its own commit, with
  `tests/test_session_stdin.py` passing unchanged. The RESYNC entry is
  anchored at the landing's parent.
- **Neither bar fails on seconds** (the owner re-scope): `[run] smoke` and
  `[bars] review` run the step in warn mode; a test proves a stand-in tier
  over both limits exits 0 with its WARN line under each bar's command, and
  a red stand-in tier still exits nonzero.
- **No other enforce caller fails on seconds** (coordinator-2026-10-21
  D-001): `docs/stack.ini` `[step:smoke]` and the CI `smoke-budget` job run
  the step in warn mode; a test reads each command and finds the warn mode.
- **The audit's smoke part** runs from `run.cmd audit` (and `run_menu.py
  audit`), runs the step in enforce mode and reports the test count against
  `max-tests`; over any of its three limits (CPU, wall, `max-tests`) it
  exits 1 naming the limit and its key.
- **The audit's count**, in-process against a stand-in tier and counter, in
  enforce mode: a count at `max-tests` exits 0 and one past it exits 1,
  naming `max-tests`; a counter that fails or counts nothing exits 2 naming
  the failed count; a red tier over `max-tests` exits with the tier's own
  code, naming the count too. Warn mode never starts the counter. The
  membership ratchet in `tests/test_smoke_budget.py` and the step count
  through the same function.
- **On the landing tip**, the bar is green and `run.cmd audit` is run once
  quiet, its verdict line recorded in the fragment;
  `check_trajectory.py --strict` and `trace.py --strict` are clean.

## Scope answers

- **S1.** The final inventory, after the owner's re-scope, is four pieces:
  (A) deliverable 6, the job-code move; (B) the CPU meter, its isolation,
  the keys and their stamped values (deliverables 1 to 3); (C) the bars'
  switch to warn mode, which is one line, since `[bars] review` runs
  `run_menu.py smoke` and so takes `[run] smoke`'s step as written, with the
  paired procedure's retirement; (D) the `[run] audit` action's smoke part,
  with its count. The doc homes (deliverable 4) follow whichever of them
  they describe, and RESYNC (deliverable 5) follows A.
  - **Order.** A lands first, as its own behaviour-preserving commit
    (PROCESS.md §3). B, C and D follow in one landing, B's commit before
    C's and D's, all in this lane.
  - **Why B, C and D stay together.** Each is broken alone. C without D
    leaves the tier's seconds judged by nothing, the gap that retiring the
    paired procedure first would open. D without B is a wall-only verdict,
    which deliverable 1 refuses. B without C and D keeps both bars failing
    on seconds, against the re-scope. Within B, without deliverable 2
    another run can raise the reading, and without the step the keys are
    dead.
  - **The alternative, for the owner.** C could land alone, ahead of the
    lane, to release WI-957 sooner. Its cost is that seconds would be
    judged nowhere until D lands, only printed. The re-scope orders the row
    as a whole before WI-957, so this spec keeps one landing.
- **S2.** One file gains a value domain over the bar's gate (`## Trust`).
  The conftest's new input, an environment variable, only picks which job
  the cap uses, and gates nothing.
- **S3.** Closed, deny by default.
  - **Platforms:** `win32` reads the job; a platform where `resource` imports
    reads `RUSAGE_CHILDREN`; any other platform refuses (exit 2).
  - **Readings:** deliverable 3's exit table. Any other failure exits
    nonzero, naming its cause, never 0.
  - **Declared values:** `## Trust`.
  - **The bound, by platform:**
    - Windows counts every process born in the job, and nothing here
      requests breakaway.
    - POSIX counts what parents reaped. A process orphaned before it ends (a
      leaked daemon, git's detached auto-gc) is outside the reading. That is
      a stated under-count, which the build sizes on WSL against
      `/proc/stat`'s busy time.
  - Hand-edited state and sub-second races are outside (PROCESS.md §6).
- **S4.** `single`. The row promises behaviour over an input space, has a
  Trust section, and touches the step, the root conftest, `agent_session.py`
  and the new shared module.
- **Architectural delta,** within scope: a new verdict input (the OS's CPU
  accounting), a Windows boundary (the step's job), two keys, exit 2, a
  shared kit module holding moved code, and a conftest input under which the
  bar's tier stops sharing the named job's ceiling (a venv-launched run
  already cannot join it once another run holds it). No component or IF row
  changes. No refactor row is owed: the move is this row's first commit
  (D-007). The performance-budget layer
  (SR-167) was not used: it reports a missing measurement as a SKIP, the
  fallback this row refuses.
- **S6.** Two soft edges, both queued ahead; nothing third-party. `~WI-915`
  folds the step's `_profile` into the shared loader. `~WI-916` adds a
  `[run] smoke` step before this one and edits the same step-list test and
  `.desc`.
- **B1.** The probes are evidence, and each becomes a test.
- **B2.** No split. The move is a commit in this lane, not a minted row.
- **B3.** The step judges the run it measures. The paired procedure, which
  re-took a parent reading for each commit, retires.
- **B4.** No Done-when item needs an owner act. The CI Linux reading and the
  macOS run wait for the owner's push; they are recorded as a decision after
  landing, and a breach there is a finding for the owner, not a re-stamp. If
  the loaded CPU readings spread too wide for one value, the lane holds
  before the stamp, for the owner.
- **The two other enforce callers** (found at drafting, not raised by the
  critique; a delegated call, coordinator-2026-10-21 D-001, for the owner
  to confirm or overrule). Two more callers run the step in
  `--mode enforce` and the re-scope does not name them: `docs/stack.ini`
  `[step:smoke]` (the harness step, `from-stage = DevStg-Tests`, so it is
  in the stage bar a lane refresh runs) and `.github/workflows/test.yml`'s
  `smoke-budget` job. Both move to warn mode in this row, as the commit
  and review bars do: each is a bar in the sense of the owner's ruling,
  and the seconds are judged only by the run menu's audit. The
  template's copies of both (if shipped) follow the same rule.

## Calls ruled at filing

- **The design** (owner, 2026-10-17; coordinator-2026-10-17 D-007). Budget
  the tier's own CPU-seconds over the whole tree, xdist workers included,
  plus a looser wall-clock cap. D-005 stays until this lands.
- **Placement** (same ruling): after the current batch (WI-912, WI-929,
  WI-915 to WI-917, WI-925 to WI-927), at their `priority = 5`; the queue
  table orders the ties.
- **The wall cap** (coordinator-2026-10-17 D-007, Q1 (a)) clears the
  ordinary loaded readings on record (58.7 to 287 s), so only a window like
  the 1832 s one, or a tier that sleeps or hangs for minutes, breaches.
- **One CPU value** (D-007, Q2 (a)). The reading depends on the box (xdist
  workers are half the logical CPUs, and core speed and SMT vary), and one
  value from this workstation applies everywhere, CI included. The report
  names the CPU count; a breach elsewhere is a finding, not a re-stamp.
- **The shared job module** (D-007, Q3 (a)): deliverable 6, moved first in a
  behaviour-preserving commit, with its RESYNC entry (PROCESS.md §3, 0→A→B).

## Critique dispositions

Scope critique round 1 (Codex Sol, 2026-10-21), CHANGES-REQUESTED, two
findings.

- F1 (MAJOR, S2/S3, the re-scope's "The audit judges", Trust, Done-when
  "The audit's smoke part"): adopted. Deliverable 3 now reads "In enforce
  mode, after the timed tier run and outside its reading, the step counts
  the smoke tier: the test node ids a collect-only `-m smoke` run from the
  repository root collects", with "A collect-only run that exits nonzero, or
  that yields no node id, is a failed count, never a pass" and the exits
  "Then 1 in enforce mode for CPU, wall or count over". Trust adds "The
  count's path ... produced by the step's own collect-only `-m smoke` run
  ... consumed by the step alone, in the same run" and "It validates
  `cpu-seconds`, `wall-seconds` and `max-tests` in both modes". Done-when
  adds "The audit's count ... a count at `max-tests` exits 0 and one past it
  exits 1, naming `max-tests`; a counter that fails or counts nothing exits
  2 naming the failed count; a red tier over `max-tests` exits with the
  tier's own code". The owner's re-scope already rules that the audit judges
  the count and that a breach is filed as a re-tier row, so the contract
  needs no new owner call.
- F2 (MINOR, S1): adopted. S1 now reads "The final inventory, after the
  owner's re-scope, is four pieces", with "A lands first, as its own
  behaviour-preserving commit ... B, C and D follow in one landing" and "Why
  B, C and D stay together. Each is broken alone." The option of landing the
  bars' warn switch alone, to release WI-957 sooner, is recorded under "The
  alternative, for the owner"; the spec keeps one landing, as the re-scope
  orders the row as a whole before WI-957.
