# WI-926 — implementation plan (revision 2)

Item: `docs/work/active/wi-926/WI-926-hooks-on-at-launch.md` (specref
`docs/specs/WI-926.md`). Item SRs: SR-019 (`docs/requirements/system-requirements.toml`),
SR-113 (same file). TCs verifying them (`docs/test/test-cases.toml`): TC-019 and
TC-021 (SR-019), TC-032 (SR-113). Interfaces read in
`docs/requirements/interfaces.toml`, the component in
`docs/requirements/components.toml` (CMP-007 the hooks, CMP-008 the routes), the
flows in `docs/runtime-flows.md` (Flow 1, Flow 3, Flow 4).

## What changed from revision 1, and why

The critique's three findings were checked against the code before any change.
All three are confirmed.

- **F1, confirmed.** This repository's `AGENTS.md` is a pointer stub. It says
  "the content lives in `CLAUDE.md`, not here". `tests/test_dogfood_sync.py`
  has no pin that ties a guide line in `AGENTS.md` to `AGENTS.template.md`.
  The spec's deliverable 4 says "this repository's own guide", and that is
  `CLAUDE.md`. P11 (was P10) now targets `CLAUDE.md` beside the template and
  leaves the stub alone. The budgets were also read
  (`.claude/skills/byte-budget-guard/SKILL.md`):
  - `AGENTS.template.md` is 9,996 bytes against a hard cap of 10,000, so the
    line must be paid for inside that file;
  - `CLAUDE.md` is 7,991 bytes against 8,500.
- **F2, confirmed.** Revision 1's P4 found its migration set from the reds of
  P5–P7, while P5–P7 named P4 as a predecessor. That is a cycle. The helper and
  its adoption are now two rows:
  - P4 creates the helper. P5–P7 consume it in their own new tests.
  - P8 migrates the existing fixtures after P5–P7 and verifies the whole set.

  P5–P8 land as one commit slice, so trunk never carries the red middle.
- **F3, confirmed.** `overnight_legs.log` opens `LOGDIR / "loop.log"` for
  append. With the check placed above `LOGDIR.mkdir`, a first launch would raise
  `FileNotFoundError` instead of refusing. P7 now prints the refusal to stderr
  before any log directory is created, then returns 2. Its test runs with
  `LOGDIR` absent.

## The architectural delta

Every route's start now depends on a new input: the checkout's git hooks
configuration, which no route read before. The check lives in one new module,
and every route crosses into it. That is a new boundary, drawn as one new
interface row. Two existing interfaces also gain a value in their refusal
domain:

- IF-246's `act` gains a second refused outcome beside `BlackoutRefused`;
- IF-186's `commit` gains a refusal.

No new persistent state. All of it is in scope and carried by the rows below
(P3, P5, P6, P10). No refactor is owed. A single shared entry for all routes was
weighed and rejected at filing (D-015 call 1). The revision moves no part of
this: F1–F3 change a docs target, a row order and a stderr path.

DELTA: within

## Facts read from the code that shape the plan

1. **The git call, confirmed.** It is one call:
   `git -C <root> rev-parse --path-format=absolute --git-path hooks --git-common-dir --show-toplevel`.
   It prints three absolute lines: the hooks directory, the common git dir and
   this worktree's top. `--path-format` is already used by `session_keep.py`.
   Tried on git 2.49 in a scratch repository:
   - unset → `<top>/.git/hooks`;
   - `.githooks` (relative) → `<this worktree's top>/.githooks`, also from a
     linked worktree;
   - an absolute path → that path;
   - empty → the top itself.

   Every one of these that is not `.githooks` at the top of this worktree or of
   the main worktree reads "not on". The main worktree's top is the parent of
   the common git dir. Paths are compared after `resolve()` and
   `os.path.normcase`, so case and separators on Windows cannot fail the check.
2. **`session_service.act`'s refusal cannot be a `BlackoutRefused`.**
   `through_blackout` catches `BlackoutRefused` and waits it out, so a hooks
   refusal shaped that way would wait forever. It gets its own exception class,
   `HooksOffRefused`, which is not a subclass of `BlackoutRefused`.
   - `act` raises it before anything is built or accounted.
   - A retained call's keep is released first, as the blackout refusal does.
   - `call`'s record is not written, because `_record_call` writes nothing
     before `invocation-id` is set.
   - `coordinator_adjudicate.py` catches `BlackoutRefused` at its two `_call`
     sites and maps it to `EXIT_PREFLIGHT`. It catches the new class beside it
     the same way.
3. **The claim's ladder.** LLR-140 (D13) asks for the hooks-on refusal first.
   The claim reaches `bookkeeping.commit` only after the guard refusal, the
   dispatch lock and the tracked-pause rung. So `integrate.claim` also calls the
   check first, before `coordinator_guard.claim_refusal` and `_dispatch_lock`,
   so that a hookless claim takes no lock. This is a nested call, like the
   dispatcher's inside the loop. It is not a seventh census entry: D5's list
   stays the six plus `overnight_legs.py`. A claim test pins it as the first
   call.
4. **The successor's take does not reach `take`.** The spec's Context says it
   does, but the code says otherwise: `on_session_start` installs the successor
   through `_install` directly. The check is not added there, for two reasons:
   - the hook path must always exit 0 (IF-281);
   - the successor runs in the checkout whose `take` was already checked, so
     hooks turned off between the two are the stated hand-act residue
     (`## Trust`).

   The plan records this discrepancy for the critic rather than widening scope.
5. **Deleting the hooks' special cases leaves dead sh functions.** Three
   functions are called only by the skip branches that deliverable 3 deletes:
   `privacy_declared_true` in `pre-commit` and in `commit-msg`, and
   `loop_marked` in `commit-msg`. They are deleted with those branches.

   That has a ripple. TC-150's evidence (`tests/test_process_config.py`)
   sources `privacy_declared_true` out of `hooks/pre-commit` and pins it
   byte-equal to commit-msg's copy. That is SR-137's reader-agreement table,
   which is not in D16's list. The one live sh privacy reader left is
   `pre-push`'s inline read.
   - P2 lifts that read, unchanged, into a `privacy_declared_true` function in
     `pre-push` and repoints the table there.
   - The byte-for-byte test then compares `process_declares` and
     `mixed_config_refusal` only.
   - TC-150's method ("sources the SHIPPED hook's own sh functions") stays
     true, so no row text changes.
6. **The fixture helper must survive the fixtures' own shapes.** The helper is
   `conftest.hooks_on(root)`. It writes stub `pre-commit` and `commit-msg`
   (`#!/bin/sh` + `exit 0`, LF, mode 0755 on POSIX) into `<root>/.githooks/`.
   It sets `core.hooksPath` to that directory's absolute path, so linked lane
   worktrees read "on" without carrying the stubs.
   - Where `.githooks/` is untracked, it is added to `.git/info/exclude`, so the
     stubs never make a dirty trunk.
   - Where a bootstrapped scaffold already tracks real hooks there, the files
     are marked `--skip-worktree`, so the real floor never runs on fixture
     commits.

   The helper is the only way a fixture turns hooks on. Nothing in it is an
   environment variable or a flag the check reads (D6).
7. **`overnight_legs.main`'s order (F3).** Today `main` does three things in
   this order: `LOGDIR.mkdir`, then the kit-scripts `sys.path.insert`, then the
   import of `coordinator_guard`. `log()` appends to `LOGDIR / "loop.log"`.
   `LOGDIR` is `WTROOT / "overnight-logs"`, a module global, so a test can
   point it at a `tmp_path` child that does not exist.

## Plan

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | The three shipped hooks refuse when the kit scripts directory cannot be found | D4; SR-019; TC-019; TC-021 | IF-134; IF-135; Proposed: commit-msg's exit code (git admits the commit on 0), nearest IF-134, the pre-commit hook's identical exit-code contract with git | |
| P2 | The privacy reader's agreement pin follows the one live sh reader | D4; SR-019 | IF-135 | P1 |
| P3 | The check, in one new module | D1; D6 | Proposed: `kitlib/commit_hooks` `hooks_refusal(root)` returning None or the refusal text, requestors agent_loop, session_service, bookkeeping, integrate, coordinator_guard; nearest IF-194 (`kitlib/provenance`, one vocabulary module below the same family of writers) | |
| P4 | The fixture helper, created and self-tested (no adoption yet) | D2; F2 | no interface (test support only) | P3 |
| P5 | The loop and the session service call the check first | D2; D14 | IF-246; IF-015 | P3; P4 |
| P6 | The trunk writers call the check first: bookkeeping commit, claim, refresh and merge slot | D2; D13; D14 | IF-186; IF-080; IF-271 | P3; P4 |
| P7 | The lease's take and this repo's headless legs call the check first; the legs refuse on stderr before any log directory exists | D2; D3; D15; F3 | IF-280; IF-281 | P3; P4 |
| P8 | Every existing route-driving fixture adopts the helper, found and verified after the routes change | D2; F2 | no interface (test support only) | P4; P5; P6; P7 |
| P9 | The census, with its mutation test, and the no-override read of the entries | D5; D6 | no interface (a test reading function bodies) | P5; P6; P7 |
| P10 | Spine rows, interface rows and runtime flows, judged at the lane's checkpoint sitting | D8; D9; D10; D11; D12; D13; D14; D15; D16; SR-019; SR-113; TC-019; TC-021; TC-032 | IF-186; IF-246; IF-134; IF-135; IF-271; Proposed: the new check's row (P3's) | P1; P2; P3; P5; P6; P7 |
| P11 | The shipped guide template and this repo's own guide (`CLAUDE.md`) carry the hooks-on line | D7; F1 | no interface (docs only) | P5 |
| P12 | RESYNC_PACK entry and ADOPTING's withdrawn skip option | D17 | no interface (docs only) | P1; P5; P6; P7 |
| P13 | The bar on the landing tip | D18; SR-019; SR-113; TC-019; TC-021; TC-032 | no interface (runs the bar) | P1; P2; P3; P4; P5; P6; P7; P8; P9; P10; P11; P12 |

## Steps

### P1 — the hooks stop skipping (D4)

Files: `project-trajectory/hooks/pre-commit`, `hooks/commit-msg`,
`hooks/pre-push`.

When the scripts lookup comes back empty, or names a directory that does not
exist, each hook prints one refusal and exits 1. The refusal names the cause:
the kit scripts directory cannot be found under `KIT_SCRIPTS_DIR` or
`scripts/`. It also names the three fixes:

- set `KIT_SCRIPTS_DIR` in the delegating wrapper;
- re-run bootstrap;
- `git config --unset core.hooksPath` to turn the hooks off.

Per hook:

- **pre-commit:** the `privacy_declared_true` branch and the `exit 0` skip
  become that one refusal.
- **commit-msg:** the privacy-declared and `loop_marked` branches and the skip
  become that one refusal.
- **pre-push:** both scripts-lookup sites refuse:
  - the privacy-off secrets-floor site, which is `exit 0` today;
  - the privacy-on site, which already refuses and now gets the shared text.

The functions only those branches called are deleted (fact 5). The header
comments that describe a skip are rewritten in the same step. The mixed-config
refusal and the interpreter probe (WI-880) stay where they are and keep their
order. Both run before the lookup.

Tests are all `sh`-driven and env-gated `posix-shell`/`git`. They live in the
existing SLOW_MODULES `tests/test_pre_commit_hook.py` and
`tests/test_pre_push_hook.py`.

| Test | What it asserts | Why it fails before the change |
|---|---|---|
| `test_hook_honors_kit_scripts_dir_override` (bad half inverted; good half kept) | `KIT_SCRIPTS_DIR=nope-not-here` with no `scripts/`: a non-zero exit and the three fixes in stderr | Today it asserts exit 0 |
| New `test_each_hook_refuses_when_the_kit_scripts_cannot_be_found` | pre-commit and commit-msg, each with a bogus `KIT_SCRIPTS_DIR` and with `scripts/` moved away: a non-zero exit, the cause and the fixes | Today both exit 0 |
| New `test_privacy_and_loop_commits_get_the_same_scripts_refusal` | Privacy declared (pre-commit and commit-msg) and `KIT_LOOP_SESSION` set (commit-msg): the shared refusal text | Today's special-case texts differ |
| `test_pre_push_honors_kit_scripts_dir` (`slipped` half inverted) | A non-zero exit and the shared refusal | Today it asserts exit 0 |

### P2 — the agreement pin follows the live reader (fact 5)

`hooks/pre-push`'s inline privacy read becomes a `privacy_declared_true`
function, byte-for-byte the logic it holds today. Its one call site sets
`privacy`.

In `tests/test_process_config.py`:

- `sh_privacy_declared_true` extracts the function from `pre-push`;
- `test_both_hooks_carry_the_same_reader_byte_for_byte` drops
  `privacy_declared_true` from the pre-commit/commit-msg pair, since it no
  longer exists in either.

The adversarial table runs unchanged against the moved reader. There is no red
before, since this move preserves behaviour. P1 alone would leave the table's
extraction failing, and this step keeps it green. TC-150 is run, not amended.

### P3 — the check (D1, D6)

The new pure module is `project-trajectory/scripts/kitlib/commit_hooks.py`. Its
one public function is `hooks_refusal(root)`, which returns None or the refusal
text. It makes one git call (fact 1) through `kitlib.git.git_out`. A failing call
(None, git missing, not a work tree) reads "not on".

"On" holds only when all of these do:

- the resolved hooks directory equals `<this top>/.githooks` or
  `<main top>/.githooks`;
- `pre-commit` and `commit-msg` are files there;
- on POSIX, both are executable (`os.access(..., X_OK)`).

Every refusal names the cause it found and the fix.

- **Causes:**
  - unset (reads `.git/hooks`);
  - another directory (named);
  - a missing hook (named);
  - a hook not executable (named);
  - git unanswered.
- **Fixes:** `sh scripts/setup.sh` (Windows `scripts\setup.ps1`), or
  `git config core.hooksPath .githooks`.

The module reads no environment variable and takes no parameter besides `root`.
It does not read the hooks' contents.

Tests: new `tests/test_commit_hooks.py` (in-process, smoke tier, real git in
`tmp_path`).

- **Not on.** Each case asserts that the refusal names its cause and the setup
  command:
  - `core.hooksPath` unset;
  - `.git/hooks`;
  - another directory;
  - empty;
  - `pre-commit` missing;
  - `commit-msg` missing;
  - a hook with mode 0644 (POSIX only, skipped on Windows);
  - a `root` that is not a work tree;
  - git made unrunnable by monkeypatching `kitlib.git.git_out` to return None.
- **On:**
  - relative `.githooks`;
  - absolute `.githooks`;
  - from a linked worktree (`git worktree add`), both with a tracked relative
    `.githooks` and with an absolute path to the main worktree's.
- **D6:** `test_the_check_reads_no_override` parses the module's AST. It asserts
  that no `os.environ`, `getenv` or `environ` name appears, and that
  `hooks_refusal`'s signature is exactly `(root)`: no defaults, no `*args` and
  no `**kwargs`.

There is no red before, since the function is new (D1 says so). The route items
carry it.

### P4 — the fixture helper, created (D2, F2)

`tests/conftest.py` gains `hooks_on(root)` (fact 6). This row only creates it
and proves it. It adopts it nowhere.

New tests in `tests/test_commit_hooks.py`:

- `test_hooks_on_makes_a_fixture_read_on`: on a fresh `git init`,
  `hooks_refusal` is None after `hooks_on`, and also from a linked worktree of
  it. Red before: the helper does not exist.
- `test_hooks_on_leaves_the_tree_clean`: after `hooks_on` and one commit,
  `git status --porcelain` is empty. This is checked both untracked and with a
  tracked `.githooks/` (the skip-worktree path).

P5–P7's new tests call the helper for their "with the hooks on, it runs as
today" cases. That is all they need from it, so P4 is complete before them.

### P5 — the loop and the session service (D2, D14 IF-246)

- **`agent_loop.main`:** the check runs right after `_resolve_root`, before
  `mark_loop_process`, the fingerprint check and `_coordinator_lock`. That makes
  it the first call after argument parsing and root resolution, and
  `mark_loop_process` moves below it. A refusal prints the refusal and returns
  `EXIT_PREFLIGHT`. Lane workers (`--worktree --wi`) enter here too.
- **`session_service.act`:** the check runs first, before `launch_refusal`. A
  refusal releases a retained call's keep and raises the new
  `HooksOffRefused(text)` (fact 2). `coordinator_adjudicate.py`'s two `_call`
  sites catch it beside `BlackoutRefused` and return `EXIT_PREFLIGHT`.

Tests go in the new `tests/test_hooks_on_routes.py` (in-process where possible,
smoke tier). Each refusal case builds a repo without calling `hooks_on` and
asserts that the refusal names the setup command. Each "runs as today" case
calls `hooks_on` (P4) and asserts today's outcome.

| Test | What it asserts | Why it fails before the change |
|---|---|---|
| `test_the_loop_refuses_a_hookless_checkout` | Runs `agent_loop.py --root <repo>` as a subprocess, with a stub agent CLI that writes a marker if run. Exit 2; no `out/agent-loop.lock`; no branch cut; HEAD and the marker unchanged | Today it gets past preflight and takes the lock |
| `test_act_refuses_a_hookless_checkout` | A `Call` whose template is a marker script: `HooksOffRefused`, no marker, no record under the invocation records dir, and the keep released | Today `act` launches |
| `test_through_blackout_does_not_wait_out_a_hooks_refusal` | The exception propagates and `sleep` is never called | The class does not exist |

### P6 — the trunk writers (D2, D13 LLR-140, D14 IF-186)

- **`bookkeeping.commit`:** the check is first. A refusal returns
  `(None, "<label> cannot start: <refusal>")`, the shape of its existing
  no-HEAD refusal.
- **`integrate.claim`:** the check is first (fact 3), before the guard refusal
  and `_dispatch_lock`. A refusal returns its existing refusal string shape.
- **`integrate.refresh`:** the check is first, before `_lane_bar_directives`. A
  refusal returns `(None, "refresh REFUSED for <branch> - <refusal>")`.
- **`integrate.integrate`:** the check is first, before the dirty check and
  `_slot`. A refusal returns `fail(<refusal>)`.

Tests go in `tests/test_hooks_on_routes.py`. Each refusal case fails before the
change, because today the route runs.

- `test_bookkeeping_commit_refuses_a_hookless_checkout`: `(None, refusal)`, HEAD
  unchanged, and the `write` callback never called.
- `test_claim_refuses_a_hookless_checkout_first`: with a queued spec present, it
  asserts all of these:
  - the refusal;
  - no `wi-…` branch exists;
  - the spec has not moved;
  - HEAD is unchanged;
  - the dispatch lock file was never created.

  A second case pins the order: a hookless checkout that would also fail the
  guard's refusal gets the hooks refusal.
- `test_refresh_refuses_a_hookless_checkout`: a claimed lane is built with
  `hooks_on`, then `core.hooksPath` is unset. It asserts the refusal and that
  the lane tip is unchanged.
- `test_merge_slot_refuses_a_hookless_checkout`: with a finished branch
  present, a non-zero `fail`, `out/integrate.lock` never taken, and trunk
  unchanged.

### P7 — the lease's take and the headless legs (D2, D3, D15 LLR-300, F3)

- **`coordinator_guard.take`:** the check is first. A refusal returns the
  refusal string, and the CLI's existing path maps it to exit 1 (IF-281).
  Fact 4 records why `on_session_start`'s successor install is left alone.
- **`scripts/coordinator/overnight_legs.py` `main`** (fact 7). The new order is:
  1. argument parsing and `repo` resolution, as today;
  2. the kit-scripts `sys.path.insert`;
  3. the check against `repo`;
  4. `LOGDIR.mkdir`, only once the check has passed;
  5. the `coordinator_guard` import and the leg loop, as today.

  On a refusal it prints `stop: <refusal>` to **stderr**, without `log()`,
  creates no log directory, and returns 2 (its stop code). A refusal never
  touches `LOGDIR`, so a first launch with no log directory refuses cleanly
  instead of raising `FileNotFoundError`.

Tests go in `tests/test_hooks_on_routes.py`.

- `test_take_refuses_a_hookless_checkout_and_records_no_holder`: the refusal,
  an empty lease (`_load`) and no `take` event. Red before: today the take
  installs the holder.
- `test_overnight_legs_refuses_a_hookless_checkout_before_any_log_dir`
  (in-process). The script is imported by path, and its `LOGDIR` is
  monkeypatched to `tmp_path / "overnight-logs"`, which does not exist. The
  fixture repo holds a handoff with a session prompt and has no `hooks_on`.
  `main(["--repo", <repo>, "--dry-run"])`:
  - returns 2;
  - writes the refusal, naming the setup command, to stderr (`capsys`);
  - leaves `tmp_path / "overnight-logs"` absent.

  Red before: today the dry run creates the directory and returns 0.
- `test_overnight_legs_runs_as_today_with_hooks_on`: the same fixture with
  `hooks_on`. The dry run returns 0 as today, and the log directory now exists.
  This pins that the move left the passing path intact.

### P8 — every existing route-driving fixture adopts the helper (D2, F2)

This runs after P5–P7, so the routes now refuse in a hookless checkout.

- **Discovery.** Run the full unfiltered suite. Its new reds are exactly the
  existing fixtures that drive a route without hooks on. The spec estimates
  about 45 modules. The expected homes are:
  - `tests/integrate_fixtures.py::git_repo`;
  - the per-module repo builders in the loop, dispatch, lane, handback, intake,
    sweep/census/consolidate/rejudge, bookkeeping, session-service,
    coordinator-adjudicate and coordinator-guard suites.

  The suite's reds, not that list, decide the set.
- **Migration.** Each fixture gains one `hooks_on(root)` call before its first
  commit. None is fixed by weakening the check, by skipping a test or by an
  environment variable.
- **Verification.** Re-run the full suite. It must be green apart from failures
  already red on the lane's base, which are compared and listed.
- **Slice boundary.** P5–P8 form one commit slice, and the commit bar runs at
  P8's end. The red middle between P5 and P8 never reaches a commit.
- **Cost.** The stubs run on every fixture commit, which costs a `sh` spawn per
  hook. P13 measures the smoke tier against its 60 s budget with this in place.
  On a breach, cases move to SLOW_MODULES per the CLAUDE.md rule; the budget is
  never moved.

Red before: none of its own. This row keeps P5–P7's "runs as today" half green
across the existing suite.

### P9 — the census (D5, D6)

The new `tests/test_hooks_on_census.py` reads function bodies by AST, as
`tests/test_commit_floor_census.py` reads the floor. It runs in process, smoke
tier. `ROUTES` is the reviewed declaration of seven `(file, function,
preamble)` entries:

- the six from the spec's Context;
- `scripts/coordinator/overnight_legs.py::main`.

`preamble` is the closed set of calls allowed before the check:

| Entry | Calls allowed before the check |
|---|---|
| `agent_loop.main` | `_utf8_console`, `parse_args`, `_resolve_root` |
| `overnight_legs.main` | the argparse calls, `Path(...).resolve()` and `sys.path.insert`; `LOGDIR.mkdir` is not in it (F3) |
| every other entry | none, or the `Path(root)` coercion |

The census asserts that the first call outside the preamble is
`commit_hooks.hooks_refusal`, passed exactly the entry's root and nothing else.
That is the D6 half at the call sites.

Mutation test: `test_the_census_fails_when_an_entry_stops_calling_first`. For
each entry, it rewrites that function's source in memory twice: once with the
check moved below the next statement, once with it deleted. Each time, the
census's own judging function must report that entry. That shows the census is
not vacuous.

### P10 — spine, interfaces, flows (D8–D16)

Authored in-lane and judged at the lane's checkpoint sitting:

- **New SR (D9):** derived, under SN-005, in capability voice. Where the commit
  floor is not active in a checkout, the delivered agent routes refuse to start
  there and name the setup step.
- **New LLR and TC (D10):**
  - the LLR has module `kitlib/commit_hooks.py` plus the seven call sites,
    component CMP-008;
  - the TC's evidence is `tests/test_commit_hooks.py`,
    `tests/test_hooks_on_routes.py` and `tests/test_hooks_on_census.py`.
- **SR-019 acceptance (D11):** the scripts-lookup refusal sentence, the
  interpreter rule's sibling.
- **LLR-019 / LLR-020 detail (D12).**
- **LLR-140 (D13):** the hooks-on refusal first in the claim's ladder.
- **IF-186 data (D14):** the refusal list gains the hooks-on refusal.
- **IF-246 data (D14):** `act/call -> Outcome or BlackoutRefused or
  HooksOffRefused`.
- **LLR-300 detail (D15):** take's refusal.
- **New interface row (P3's Proposed):** owner `scripts/kitlib/commit_hooks`,
  with the five requestors, channel `call`, Drafted.
- **Commit-msg's seam (P1's Proposed):** there is no row today. Whether it gets
  one is left to the sitting. The plan does not mint one silently.
- **Unchanged, verified, not edited (D16):** SR-113, LLR-122, TC-019, TC-021
  (their evidence modules still carry the pins P1 adds or inverts), IF-134,
  IF-271, SR-229, LLR-151, LLR-269.
- **`docs/runtime-flows.md`:**
  - Flow 1's preflight line gains the hooks-on check before the lock;
  - Flow 3 gains the scripts-lookup refusal arm;
  - Flow 4's claim note gains the hooks-on rung.

The regenerated outputs (components, cli-reference, interface-reference, the
arch map) are refreshed at the landing, per the coordinator-cycle recipe.

### P11 — the guide line (D7, F1)

The two homes are the shipped guide `project-trajectory/AGENTS.template.md` and
this repository's own guide, **`CLAUDE.md`**. This repository's `AGENTS.md` is a
pointer stub ("the content lives in `CLAUDE.md`, not here"), and it stays
unchanged.

- **`AGENTS.template.md`** gets one line beside its setup/commit guidance: hooks
  are on before any work (`sh scripts/setup.sh`, or `scripts\setup.ps1` on
  Windows), and a commit never bypasses them. The file is at 9,996 of a 10,000
  hard cap, so the line is paid for inside the file by tightening adjacent
  wording, never by moving the cap. The byte-budget-guard skill's
  measured-size row is updated.
- **`CLAUDE.md`** gets the same rule as one sentence in the principles bullet
  that already names the commit bar. It is phrased for this repository: hooks
  on via `core.hooksPath .githooks`, and the agent routes refuse otherwise.
  CLAUDE.md is at 7,991 of 8,500.

There is no automated sync between the two lines, so revision 1's claim that
`tests/test_dogfood_sync.py` keeps them in step is withdrawn. Instead, the
builder quotes both inserted lines in the lane log, side by side, so the review
can inspect that they say the same rule. Before and after byte counts for both
files, from the byte-budget-guard skill, are reported there too. The check is
done when:

- both lines are present;
- `AGENTS.md` is byte-identical to its base;
- `AGENTS.template.md` is at or under 10,000 bytes;
- `CLAUDE.md` is at or under 8,500 bytes.

### P12 — resync (D17)

The `RESYNC_PACK.md` entry lists the shipped files:

- the three hooks;
- `kitlib/commit_hooks.py`;
- the edited `agent_loop`, `session_service`, `bookkeeping`, `integrate` and
  `coordinator_guard`;
- `AGENTS.template.md`.

It names two forced changes:

- agent routes run with `core.hooksPath` unset, or pointed at a hook manager or
  at `.git/hooks`, now refuse;
- a checkout whose hooks cannot find the kit scripts now refuses commits
  instead of skipping.

The fix it names: point `core.hooksPath` at the kit's hooks and call your own
chain from them. `ADOPTING.md`'s "or skip the wiring" option (around line 85) is
withdrawn for any repo that runs the kit's agent routes.

### P13 — the bar (D18)

- **Each slice:** the commit bar is `run.cmd smoke`. The P5–P8 slice is
  measured at P8's end, because the stubs add a `sh` spawn per fixture commit,
  and the 60 s budget is held.
- **The lane's gate:** the full unfiltered suite (`python -m pytest -q -n auto`)
  runs on the landing tip. It runs TC-019, TC-021 and TC-032, plus TC-020 and
  TC-150, whose evidence P1 and P2 touch.
- **Before the landing commit:** `check_trajectory --strict` runs.

The real output is pasted.

## Not covered here, stated

- Fact 4: the successor install via `on_session_start` is not checked. Its
  residue matches `## Trust`'s "hooks turned off by hand after a route's check
  passed".
- Fact 3: the claim's own first call is pinned by a claim test, not by the
  census. D5's list stays as the spec names it.
