+++
id = "WI-926"
title = "Every agent route refuses to start in a checkout whose commit hooks are not on, and a commit hook that cannot find the kit scripts refuses instead of skipping"
workstream = "process"
sr_refs = ["SR-019", "SR-113"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = []
+++

## Deliverable

Closed at its landing on 2026-10-19, after its gate and acts, in a headless
leg:

- Every agent route asks one check first, the commit-floor activation
  contract (`kitlib/commit_hooks.py`, IF-297), and refuses to start when the
  checkout's commit hooks are not on: the loop's launch, the session
  service's launch (a `HooksOffRefused` the blackout wait never waits out),
  the trunk bookkeeping commit, the claim, the refresh, the merge slot, the
  coordinator lease's take and the overnight launcher. "On" means git's
  hooks directory is this worktree's or the main worktree's `.githooks`
  with both commit hooks runnable; each other cause is refused naming the
  cause and its repair (activation, restoring a missing hook, or the mode
  bit), and nothing turns the check off. A census pins each route's first
  call.
- The three shipped hooks refuse, naming the repair, when they cannot find
  the kit scripts directory, where two exited 0 and skipped; the
  privacy-declared and loop-marked special cases became that one refusal.
- The agent guide and its template carry the hooks-on line; the shipped
  README's pre-push row and RESYNC_PACK.md's entry state the forced change.
- Spine: SR-240, LLR-340 and TC-370 approved (sittings 004 and 005, acts 137
  to 139); SR-019, SR-020, LLR-019, LLR-020, LLR-140 and LLR-300 amended and
  blessed; IF-297 added, IF-186 and IF-246 amended (Drafted).
- Reviews (docs/reviews/wi-926/): the single plan's critiques and the cap's
  sitting 001; counted round 1, 002-REVIEW-A-204938f and 003-REVIEW-B-204938f;
  the gate in convergence stance, 006-REVIEW-A-edb8b98 and
  007-REVIEW-B-edb8b98. Decisions: docs/decisions/wi-926.toml D-001 to D-014.

## Context

Filed as a placeholder on 2026-10-15 to hold the owner's direction
(`docs/specs/WI-926.md`). Its open calls were ruled in coordinator-2026-10-15
D-015 and D-019, and D-014 folded in one more item. This text replaces the sketch
before the scope critique.

The kit's commit hooks are opt-in per checkout. Only `setup.*` and
`dev-setup.*` set `core.hooksPath`, and no route reads it when it starts. In
a fresh clone, or where setup was skipped, every commit runs with no hook,
and nobody typed a bypass. That is the one plausible way a lane commit
escapes its hook (D-013). The owner's direction is to close it by
construction: the agent guide makes hooks part of starting work, and one
mechanical check at the start of every agent route refuses to start when the
hooks are not on.

A second gap sits inside the hook (D-014, item 5). `hooks/pre-commit` exits 0
when it cannot find the kit scripts directory, unless privacy is declared.
`hooks/commit-msg` and `hooks/pre-push` skip the same way. A checkout whose
hooks cannot find the kit scripts has hooks that check nothing, so it counts
as one whose hooks are not on.

**The routes, read from the code.** Six shipped entries start agent work or
commit for it. They share no single entry today:

1. `agent_loop.main`, the managed loop's launch, in every mode (drive,
   explicit roles, interactive, dual plan). Lane workers are
   `agent_loop.py --worktree --wi` subprocesses, so they start here too. The
   loop's own commits (telemetry, the handback close, and the claim, refresh
   and merge slot that `dispatch` calls in-process) all run inside this
   process.
2. `session_service`'s launch (`act`, beside the blackout's
   `launch_refusal`): every model session the kit starts, including the
   coordinator's `coordinator_adjudicate.py`.
3. `bookkeeping.commit`: every trunk bookkeeping commit. Its callers are the
   claim (`integrate.claim`) and the intake mints (`sweep`, `census`,
   `consolidate`, `rejudge`, and the mint inside the merge slot).
4. `integrate.refresh`: the station refresh's commit.
5. `integrate.integrate`: the merge slot.
6. `coordinator_guard.take`: the coordinator lease's take.

Two of these are partial shared entries already: the session service for
model launches, and `bookkeeping.commit` for trunk bookkeeping. Nothing covers
all six. So, per D-015 call 1, each entry calls the one check first, and a
census pins the list. This repository's own `scripts/coordinator/overnight_legs.py`
starts headless legs that commit, so it calls the check too and joins this
repository's census.

Not routes, and left alone: `integrate.py done-when-hold` (the hook's own
reader) and `audit`; `coordinator_guard.py` `status`, `window-check`, `hooks`
and `hook` (reads, or one hook call); `release`, `clear`, `handback` and
`request-relaunch` (lease records; a relaunched successor reaches `take`);
`retire.py` (it writes files and commits nothing); and setup, dev-setup,
bootstrap and `run` (the routes that turn hooks on; `run`'s menu starts
`agent-resume`, which is route 1).

This row is kept beside WI-922, narrowed (D-013, D-015 call 2). D-011's rule
for the agent CLI's guard hooks was folded into this row's sketch. It is
split off as WI-927 (D-019; `## Scope answers`, S1).

## Deliverables

1. **The check, in one home** (shipped: a new pure module, for example
   `project-trajectory/scripts/kitlib/commit_hooks.py`; the plan names it).
   One function answers whether this checkout's commit hooks are on, and
   returns either nothing or the refusal text.
   - It asks git once for the hooks directory (`git rev-parse --git-path hooks`
     honours `core.hooksPath`; the plan confirms the call) and resolves it to
     an absolute path.
   - "On" means all of these hold. The directory is the `.githooks`
     directory at the top of this worktree or of the main worktree. (This
     repository sets an absolute path to the primary's `.githooks`, and
     linked lane worktrees share it.) `pre-commit` and `commit-msg` are present
     there as files. On POSIX they are also executable, since git skips a
     hook that is not.
   - Everything else is "not on", deny by default: `core.hooksPath` unset,
     empty, or naming another directory (a hook manager's, or `.git/hooks`); a
     missing or non-executable hook; a git call that fails. The refusal names
     the cause and the fix: the setup command (`sh scripts/setup.sh`, on
     Windows `scripts\setup.ps1`), or `git config core.hooksPath .githooks`.
   - It does not read the hooks' contents. Whether the hook can find the kit
     scripts is the hook's own question (deliverable 3).
2. **Called first by every route** (shipped: the six entries in Context). Each
   calls the check before it reads or writes anything else, and a refusal
   exits through that entry's existing refusal path:
   - `agent_loop.main` before its lock, with the preflight exit code;
   - the session service's launch as a refused outcome beside the blackout's;
   - `bookkeeping.commit`, `integrate.refresh` and `integrate.integrate` as
     their named `(None, refusal)` or `fail(...)`;
   - `coordinator_guard.take` as its refusal string.

   Calls that nest (the dispatcher inside the loop) run the check again. It is
   one git call and a few file checks, so that is accepted rather than
   threading a flag.
3. **The hook stops skipping** (shipped: `hooks/pre-commit`, `hooks/commit-msg`,
   and `hooks/pre-push`, all three per D-019). When the kit scripts directory cannot be
   found, the hook refuses, exit 1, and names the cause and the three fixes:
   - set `KIT_SCRIPTS_DIR` in the delegating wrapper;
   - re-run bootstrap;
   - or `git config --unset core.hooksPath` to turn the hooks off.

   The two special cases that refuse today become this one refusal and are
   deleted: the privacy-declared branch (M-42) in each hook and commit-msg's
   loop-marked branch. A repository that is not yet set up has no
   `core.hooksPath`, so git runs no kit hook there and its commits are
   unchanged. Every agent route refuses there, through deliverable 1.
4. **The agent guide** (shipped: `AGENTS.template.md`; this repository's own
   guide). It states that hooks are on before any work (the setup step that
   turns them on) and that a commit never bypasses them. Both files are
   byte-watched, so the change stays a line or two and its delta is reported.
5. **The deliberate as-is writers stay.** `handback.close_partial`'s
   `--no-verify` close and the plumbing bookkeeping commits are judged by the
   landing walk, as today. The check guards the checkout they run in, not
   their commit.
6. **The census** (this repository's tests). It lists the six route entries
   and `overnight_legs.py`'s, and asserts that each one calls the check
   before any other kit call. It is read from the function bodies, as
   `tests/test_commit_floor_census.py` reads the floor. A new route added
   without the call fails it only if it is added to the list; the list is the
   reviewed declaration, as the floor census's is.
7. **Test fixtures** (this repository's tests). One conftest helper gives a
   fixture repository hooks that are on: stub `pre-commit` and `commit-msg`
   in its `.githooks`, and `core.hooksPath` set. No environment variable or
   flag turns the check off (the owner's no-fallback rule). Every fixture
   that drives a route uses the helper. About 45 test modules drive one of
   the six entries, so this is the row's largest cost.
8. **`RESYNC_PACK.md`**, one entry, listing the shipped files. It names the
   forced change: an adopter whose agent routes run with `core.hooksPath`
   unset, or pointed at a hook manager or at `.git/hooks`, now gets a refusal
   (D-019). The fix it names: point `core.hooksPath` at the kit's hooks and
   call one's own chain from them (WI-925's ruled Q7 convention).
   `ADOPTING.md`'s "skip the wiring" option is withdrawn for any repository
   that runs the kit's agent routes.

## Trust

Deliverables 1 and 2 give the check authority over a hold: its answer
refuses or admits the start of every agent route (a claim, a model launch, a
refresh, a merge, a lease take). Deliverable 3 gives the hook's scripts
lookup authority over every commit. This is a trust boundary in the sense of
`project-trajectory/PROCESS.md` §3, "When a guard is owed". The inputs are
files on disk and git's own answer.

- **Inputs and their producers.**
  - **`core.hooksPath`**, in the repository's git config. It is written by
    `setup.sh`, `setup.ps1` and dev-setup's baseline, or by hand. Failed-write
    shapes: unset; empty; a relative or absolute path to another directory; a
    path to a `.githooks` that does not exist.
  - **The hook files** in `.githooks`. They are written by bootstrap from the
    kit's MAPPING and tracked in git. Failed-write shapes: missing; present
    but not executable on POSIX (a checkout that lost the mode bit).
  - **Git's answer.** The check asks git for the hooks directory. Failed
    shapes: git missing from PATH, a directory that is not a work tree, or
    any non-zero exit.
  - **The scripts lookup** (deliverable 3): `KIT_SCRIPTS_DIR`, set by a
    delegating wrapper, else `scripts/` or `Scripts/` at the top of the
    worktree. Failed-write shapes: unset with neither directory present, or
    naming a directory that does not exist.
- **Consumers, by path:** the six entries in Context (`agent_loop.main`,
  `session_service` launch, `bookkeeping.commit`, `integrate.refresh`,
  `integrate.integrate`, `coordinator_guard.take`), this repository's
  `scripts/coordinator/overnight_legs.py`, and the three shipped hooks for
  the scripts lookup.
- **Rulings.** Absent, unreadable, failed or malformed input always reads
  "not on", and the route refuses before any work, naming the cause and the
  fix. A hook that cannot find the kit scripts refuses the commit, naming
  the cause and its fixes. No input can make the check pass by default, and
  there is no override.
- **Residue, stated once** (PROCESS.md §6; none of these is promised):
  - a human committing by hand outside any agent route (D-015 call 3). Git
    cannot install a hook at clone. A hookless hand commit is met where it
    reaches an agent route: the claim and the lease refuse in that checkout,
    and the landing walk judges each lane commit;
  - a typed `--no-verify`, or hooks turned off by hand after a route's check
    passed (both are hand acts the process forbids);
  - a hook file whose contents were replaced (the check reads presence, not
    contents);
  - per-worktree git config (`extensions.worktreeConfig`) giving one
    worktree its own hooks path, which no kit route sets.

## Done-when

- The check: a fixture checkout with `core.hooksPath` unset, set to
  `.git/hooks`, set to another directory, with `pre-commit` or `commit-msg`
  missing, and (POSIX) with a hook not executable, each reads "not on" with a
  refusal that names the cause and the setup command. The kit's `.githooks`
  as a relative path, as an absolute path, and from a linked worktree reads
  "on". A failing git call reads "not on". (New function: no red-before
  exists; the route items below carry it.)
- Each of the six route entries, started in a fixture checkout whose hooks
  are not on, refuses before any work. It takes no lock, cuts no branch,
  writes no commit and launches no session, and it names the setup command.
  Started with the hooks on, it runs as today. Each refusal case fails on the
  code before the change, where today the route runs.
- `coordinator_guard.take` in a hookless checkout refuses and records no
  holder. It fails before the change.
- Each of the three shipped hooks, run with no kit scripts directory
  findable (a bogus `KIT_SCRIPTS_DIR`, and no `scripts/`), exits non-zero and
  names the cause and the fixes. Privacy-declared and loop-marked commits get
  the same refusal. This fails before the change: the bad half of
  `tests/test_pre_commit_hook.py::test_hook_honors_kit_scripts_dir_override`
  asserts exit 0 today and is inverted. Its good half is kept.
- The census lists the six entries and `overnight_legs.py`. It fails when
  one of them stops calling the check first, shown by a mutation test.
- No environment variable, flag or parameter disables the check. A test
  reads the module for one.
- The agent guide and its template carry the hooks-on line, and the byte
  delta is reported.
- Spine rows, judged at the lane's checkpoint sitting:
  - **new SR** (derived, under SN-005), capability voice: where the commit
    floor is not active in a checkout, the delivered agent routes refuse to
    start there and name the setup step;
  - **new LLR and TC** for the check and the route refusals;
  - **SR-019**: acceptance amended. With no kit scripts directory, the
    commit hooks refuse the commit, name the fix and neither run nor skip
    the floor (the interpreter rule's sibling);
  - **LLR-019** and **LLR-020**: detail amended for the scripts refusal
    (pre-commit and commit-msg; pre-push);
  - **LLR-140**: amended, since the claim's refusal ladder gains the hooks-on
    refusal first;
  - **IF-186** (Drafted): the bookkeeping commit's refusal list gains the
    hooks-on refusal. **IF-246** (Drafted): the launch's refused outcome
    gains it;
  - **LLR-300**: detail amended for the take's refusal;
  - unchanged: SR-113, LLR-122, TC-019 and TC-021 (their evidence modules
    still carry the pins), IF-134, IF-271, SR-229, LLR-151, LLR-269.
- `RESYNC_PACK.md` carries the entry with the forced change named.
- The bar is green on the landing tip: the smoke tier within its budget, and
  the full suite at the lane's gate.

## Scope answers

- **S1:** split. The sketch carried two deliverables that share nothing:
  - the git hooks-on check (`core.hooksPath`, the `.githooks` files and the
    hook's scripts lookup);
  - the agent CLI's guard hooks (Claude Code hook groups in
    `.claude/settings.local.json`, D-011).

  They have different inputs, readers, files, spine rows (SR-019 and SR-113
  here; SR-032, SR-229, LLR-322 and TC-345 there) and tests, and either lands
  alone. This row keeps the git check, with D-014's item 5. The guard hooks
  are their own row, WI-927, filed on trunk before either
  claim (B2 holds). Neither needs the other. If WI-897 is to follow soon,
  WI-927 lands first, because WI-897 tells adopters to re-run the enable
  command that WI-927 deletes. Otherwise either order works, and the second
  rebases its `coordinator_guard.py` edit (here `take`; there the hooks
  section).

  Inside this row, deliverable 3 (the hook stops skipping) could also land
  alone. It stays here because D-014 folded it in as part of what "on"
  means. If the critique splits it out, it lands first: it is smaller, and
  it is complete on its own.
- **S2:** yes; see `## Trust`. The check's answer holds every agent route's
  start, and the hook's scripts lookup holds every commit.
- **S3:** two closed spaces:
  - The check's input is git's hooks directory and two named files. "On" is
    an enumerated condition, and everything else is "not on" by default.
  - The route set is the six entries plus this repository's one tool, an
    enumerated list the census pins.

  The promise reaches checkouts that supported routes produce: a fresh
  clone, a scaffold, a setup that ran or was skipped, a linked lane
  worktree. It does not reach hand-edited hook contents or per-worktree
  config (residue in `## Trust`).
- **S4:** `single`. The row has a Trust section, touches several script
  families (the loop, the integrator, bookkeeping, the session service, the
  coordinator guard, the shell hooks) and promises behaviour over an input
  space.
- **S5, the architectural delta:** every route's start now depends on a new
  input, the checkout's git hooks configuration, which no route read
  before. A new boundary is crossed in one place, the new module. No new
  state or domain value. The six call sites are inside scope, so no
  refactor row is owed. A single shared entry for all routes was weighed
  and rejected (D-015 call 1): building one means refactoring six entry
  shapes for a one-line call.
- **S6, dependencies:** `needs = []`. Soft edges, with the row that lands
  second rebasing:
  - WI-922 (active, narrowed) edits `hooks/pre-commit`'s comment block;
  - WI-917 edits `overnight_legs.py` and is ordered first by the queue;
  - the wi-798 lane edits `session_service.py` and dev-setup;
  - WI-927 edits `coordinator_guard.py`.

  No third-party dependency.
- **B1:** the Context commits to nothing the Done-when omits. The residue is
  stated, not built.
- **B3:** the check reads the current configuration at the moment it is
  used. That is the decision itself, not a past decision recomputed.
- **B4:** no Done-when item needs an owner act or credential.

## Calls ruled at filing

- **Which entry every route passes** (D-015 call 1): one shipped function
  holds the check. The planner read the code and found six routes and no
  shared entry, so each route's entry calls the check first and a census
  pins the list (D-019).
- **WI-922** (D-015 call 2): kept beside this row, narrowed (D-013).
- **A human committing by hand outside any agent route** (D-015 call 3): out
  of scope, stated residue (`## Trust`).
- **The split** (D-019): the agent CLI's guard hooks are WI-927.
- **Which hooks stop skipping** (D-019): all three, `pre-commit`, `commit-msg`
  and `pre-push`, refuse and name the fixes. A repository never set up (no
  `core.hooksPath`) commits as today.
- **A hook manager or `.git/hooks`** (D-019): fails the deny-by-default
  check, and every agent route refuses there. RESYNC names it as the forced
  change: point `core.hooksPath` at the kit's hooks and call one's own chain
  from them.
- **What the route check reads** (D-019): `core.hooksPath` and the hook files
  only. The scripts lookup is left to the hook's own refusal, and a route
  meets it at its first hooked commit.
