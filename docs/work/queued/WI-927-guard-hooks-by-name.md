+++
id = "WI-927"
title = "The coordinator's Claude Code guard hooks are checked by name, installed with consent when none are there, and refused when other hooks hold their events, with no re-enable path"
workstream = "process"
sr_refs = ["SR-032", "SR-229"]
specref = "docs/specs/WI-927.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = []
+++

## Context

This row is split from WI-926 at its scope critique (S1; coordinator-2026-10-15
D-019). It carries the owner's ruling in D-011 on WI-834's hook re-enabling:
the command-level ownership in `kitlib/guard_hooks.py` is contrived. The
owner's rule replaces it: the required hooks are checked by name; when none
are there they are installed on first run; when other hooks occupy the slot
the route complains and exits; and there is no re-enable path. D-019 adds
two rulings. The first run is both the coordinator lease's take and
dev-setup's readiness check. The install keeps asking for consent before it
writes the hooks.

**What WI-834 built, and why** (read before proposing the removal; the
sources are in `docs/decisions/wi-834.toml` and `docs/reviews/wi-834/`):

- D-001: the kit ships the guard's hook groups inert
  (`agent-hooks/claude.settings.json`, scaffolded as
  `.claude/settings.json.example`). dev-setup's consented switch merges
  only the guard's groups.
- D-019, the owner's ruling, kept: the switch binds each guard command to
  the floor-resolved interpreter. It writes machine-local
  `.claude/settings.local.json`, never the committed settings. An older
  Python first on PATH had crashed the hook, and the call went ahead.
- Round 018 F2: re-enabling dropped a user's command that shared a group
  with the guard's. Plan r6 made one merge function own only the guard's
  commands. `hooks_state` reads "on" when that merge would change nothing.
- Round 020 (a sibling observation) and D-023: a user's
  `ruff check .../coordinator_guard.py` was dropped too, because ownership
  matched file-name mentions. So ownership became the example's exact command
  shapes. It moved to the new pure module `kitlib/guard_hooks.py` when
  `coordinator_guard.py` passed the module ratchet.
- LLR-322's rationale: the hooks change a contributor's interactive
  environment, so an explicit opt-in preserves their configuration and
  leaves a declined setup reversible.

The audit (`docs/plans/2026-10-11-review-churn/audit-contrived-guards-2026-10-15.md`,
the wi-834 018 F2 row) reclassified 018 F2 as contrived. It needs the user's
own command inside the kit's hook group, and re-enabling is not a normal act.
What stays plausible, and is kept: D-019's binding, the machine-local target,
the consent before the write, and "nothing to do" when the example registers
no guard hook (an adopter without Claude).

**The slot.** It is the machine-local settings' `hooks` entry for each event
the example's guard groups use: eight today (SessionStart, UserPromptSubmit,
PreToolUse, PostToolUse, PostToolUseFailure, Stop, PreCompact and
SessionEnd). Other events in that file, and every other key (Claude Code
writes its own permission allow-list there), are not the slot and are never
touched.

**Who can be asked.** dev-setup asks only at an interactive terminal (its
`interactive` test: stdin is a terminal and `CI` is unset). The lease take is
a CLI that the coordinator runs from its agent's shell tool, where stdin is
not a terminal. A headless leg runs it the same way. So in practice the take
cannot ask. Deliverable 3 states what it does instead.

## Deliverables

1. **One reading of the guard hooks' state** (shipped:
   `kitlib/guard_hooks.py`, shrunk). Over the example and the machine-local
   settings, it returns one of four answers:
   - `none`: the example registers no guard group;
   - `absent`: no guard event in the settings holds any hook;
   - `on`: every guard event holds exactly the guard's own command, checked
     by name: the guard script's file name followed by the `hook`
     subcommand, whatever the interpreter word;
   - `occupied`: anything else, naming each event and command that is not
     the guard's, and each guard event that is missing.

   A settings file that does not parse, or whose `hooks` or event values
   are not the expected JSON shapes, is `occupied` with the parse problem
   named. Deny by default: only `none`, `on`, or a consented install from
   `absent` that then reads `on` let a route go on.
2. **The consented install** (shipped: `coordinator_guard.py`, and
   dev-setup's offer in `dev-setup.template.sh` and `dev-setup.template.ps1`,
   with this repository's copies, kept). On `absent`, at an interactive
   terminal, the route asks before it writes. The question is today's offer,
   with "merging" reworded as "writing", because nothing else is ever in the
   slot.
   - **Yes:** it writes the example's guard groups into the machine-local
     settings, bound to the running interpreter (`bind`, D-019 of wi-834,
     unchanged). It keeps every other key and every non-guard event.
   - **No:** it writes nothing.

   The answer is held in one place, the settings file itself. A yes leaves
   the installed groups, which read `on` from then on. A no leaves the slot
   `absent`, so nothing is recorded, and the next first run asks again, as a
   declined offer does today. No new answer store is added.
3. **The lease take** (shipped: `coordinator_guard.take`). It reads the
   state before it records a holder.
   - `none` or `on`: it goes on.
   - `occupied`: it refuses, writing nothing (deliverable 4).
   - `absent` at an interactive terminal: it asks, as in deliverable 2.
     After a yes it reads the settings file again, and goes on only when
     that re-read reads `on`. The re-read is the construction, not a check
     of the write's success: a failed or partial write reads otherwise
     (`## Trust`). It refuses after a no.
   - `absent` without a terminal (the coordinator's shell tool, a headless
     leg): it cannot ask. It refuses the take, records no holder and writes
     nothing. The refusal names how to consent: run dev-setup at a terminal
     (the bare `run`, or `dev-setup --baseline` / `-Baseline`) and answer
     yes, then take again. That headless ruling is the one call left for the
     owner (Q1).
   - The plan checks whether Claude Code applies hooks written mid-session.
     If it reads them only at session start, an install made at an
     interactive take guards the next session, and the take's message says
     so.
4. **Complain and exit** (shipped, both routes). On `occupied`, the route
   writes nothing and exits non-zero. It names the settings file, the events
   and commands in the way, and the fix: move those hooks to another
   settings file, or remove them, then run again. dev-setup's readiness
   report prints the same text, and its other steps go on, as today's
   report lines do.
5. **No re-enable path** (shipped). These are deleted:
   - `hooks --enable` and `enable_hooks`;
   - `merged`, `_without_guard`, `_owns`, `command_shapes`, and
     `_split_interpreter`'s ownership use.

   dev-setup's consent offer is kept and calls the consented install
   (deliverable 2) instead of `--enable`. `hooks` without `--enable` stays as
   the read-only report, printing the four states.
6. **WI-897's instruction.** WI-897's Done-when tells an adopter to re-run
   `hooks --enable` to pick up a changed matcher. The state is checked by
   command name (deliverable 1), so a matcher-only change to the example
   still reads `on`, and nothing reinstalls the groups. An adopter who
   wants the new matcher removes the installed guard groups and runs the
   consented install again: the next first run reads `absent`, asks, and
   installs the new ones. The coordinator amends WI-897's queued row on
   trunk before its claim. This row only records the change in its RESYNC
   entry.
7. **`RESYNC_PACK.md`**, one entry. It covers:
   - the deleted `--enable`;
   - the consented install at both first runs;
   - the take's refusal while the hooks are absent and no terminal can
     answer;
   - the `occupied` refusal and how an adopter with hooks of their own
     moves them;
   - that a matcher-only change to the guard groups still reads `on`, and
     that an adopter who wants the new matcher removes the installed guard
     groups and runs the consented install again (deliverable 6).

## Trust

The state reading (deliverable 1) gets authority over a hold. Its answer
lets the lease take go on, or refuses it. With a consent answer it also
decides an act: the install writes a settings file. This is a trust boundary
in the sense of `project-trajectory/PROCESS.md` §3, "When a guard is owed".
The inputs are files on disk, written by people and by another program, and
a person's answer at a terminal.

- **Inputs and their producers.**
  - **`.claude/settings.local.json`** (machine-local, git-ignored). It is
    written by this row's install, by Claude Code itself (its permission
    allow-list, and hooks a user adds through its `/hooks` menu) and by
    hand. Failed-write shapes:
    - absent;
    - unreadable (an OS error on read);
    - not JSON;
    - JSON that is not an object;
    - `hooks` not an object;
    - an event value that is not a list;
    - a group without a `hooks` list;
    - a command that is not a string.
  - **`.claude/settings.json.example`**, written by bootstrap from the kit's
    `agent-hooks/claude.settings.json`. Failed-write shapes: absent (read as
    `none`; nothing is installed, as today); not parseable, or unreadable
    (an OS error on read): `occupied`, named.
  - **The consent answer.** It is read from an interactive terminal only,
    and only `y` or `Y` at the start is a yes. Anything else is a no:
    another reply, an empty line, end of input, or no terminal at all. The
    answer is never stored; the settings file it produces is the record.
- **Consumers, by path:**
  - `coordinator_guard.take`;
  - dev-setup's readiness check and its offer in `dev-setup.template.sh`
    and `dev-setup.template.ps1`, and this repository's `scripts/dev-setup.sh`
    and `scripts/dev-setup.ps1`;
  - `coordinator_guard.py hooks` (the report).
- **Rulings.**
  - An absent settings file, or one with no hooks on any guard event, is
    `absent`. It is installed only after a yes.
  - An unparseable or malformed file is `occupied`, and nothing is written.
    An unreadable settings file or example (an OS error on read) is ruled
    the same way: `occupied`, the file and error named, nothing written.
  - A take goes on only at `none`, at `on`, or after a yes whose install
    then reads `on`. Every other case refuses, records no holder, and names
    how to consent or what to move.
- **A failed install.** After a yes, the route reads the settings file
  again (deliverable 3). A write that fails makes that re-read read
  something other than `on`. Each consumer:
  - `coordinator_guard.take` refuses, records no holder, and names the file
    and the error;
  - dev-setup's readiness check reports it on a `[missing]` line naming the
    file, the error and the fix (move or repair the file, then run again),
    counted with the other missing components, and its other steps go on,
    as today's report lines do. It takes the state only from the hooks
    reader's printed word when the reader exits 0; a non-zero exit or empty
    output is reported on the same `[missing]` line with the reader's
    error, and is never read as `none`;
  - `coordinator_guard.py hooks` (the report) prints the state it reads.
- **Residue, stated once** (PROCESS.md §6): a user command whose last words
  are the guard's file name and `hook` reads as the guard's. A guard command
  bound to an interpreter that was later deleted reads `on` and fails when
  run. Claude Code then treats the hook as a non-blocking error. The fix is
  to remove the group and run again.

## Done-when

- With an example that has guard groups:
  - **Absent, yes:** at an interactive dev-setup, a settings file that is
    absent, empty, or holds only permissions gets every guard group after a
    yes. Each group is bound to the running interpreter, and every other key
    is kept. This passes before the change as well, through today's merge;
    it is a pin.
  - **Absent, no:** a no, an empty line or end of input writes nothing. The
    next run asks again. This is a pin too: today's
    `test_a_denial_changes_no_configuration_or_credential` keeps both halves.
  - **On:** a file already holding the guard's groups by name is left byte
    for byte unchanged, and nothing is asked. This is a pin.
  - **Occupied:** each of these refuses at both routes, writes nothing, and
    names the events and commands:
    - a guard event holding a user command beside the guard's (WI-834's
      mixed PreToolUse group);
    - a second group on a guard event;
    - a guard event missing while others are present;
    - an unparseable file.

    The first fails before the change: today it merges.
    `tests/test_blackout_window.py::test_the_hook_opt_in_merges_and_keeps_existing_hooks`
    is inverted into this case.
- The lease take:
  - with no terminal and the hooks `absent`, it refuses, records no holder,
    writes nothing, and names dev-setup's consent step. Fails before the
    change: today the take never reads the hooks;
  - at `on` or `none`, it takes as today;
  - at `occupied`, it refuses;
  - at an interactive terminal (driven with a pseudo-terminal where the
    platform allows; the plan says how on Windows), it asks, and installs
    and takes after a yes. It refuses after a no;
  - a consented install whose write fails refuses the take, records no
    holder, and names the file.
- dev-setup, given a hooks reader that exits non-zero or prints nothing,
  reports a `[missing]` line naming the error and never reads it as `none`,
  in both templates. Fails before the change: each maps that case to
  `none`.
- An example with no guard groups changes nothing, and both routes go on
  (`test_the_hook_opt_in_with_no_guard_hooks_changes_nothing`, kept with its
  `--enable` call removed).
- `coordinator_guard.py hooks --enable` is gone: the parser refuses
  `--enable`. dev-setup's offer calls the consented install. Fails before the
  change. `tests/test_run_devsetup.py::test_the_hooks_command_reports_and_switches_on`
  becomes a read-only report test, and the offer's own install is driven
  through dev-setup.
- Kept unchanged:
  - `test_an_installed_hook_denies_with_an_older_python_first`, run on the
    consented install;
  - `test_a_scaffold_keeps_the_machine_local_settings_out_of_git`;
  - `tests/test_coordinator_guard.py::test_the_guard_hooks_are_this_repos_opt_in_not_its_tracked_settings`;
  - `test_this_repos_readiness_report_names_the_hooks_opt_in`, which
    becomes the four-state report and still names where the offer is made.
- `kitlib/guard_hooks.py` holds no merge or ownership code. The module-size
  ratchet's entry for it shrinks.
- Spine rows, judged at the lane's checkpoint sitting:
  - **LLR-322**: amended. Its title and detail state the four-state reading,
    the consented install at both first runs, the take's refusal without a
    terminal, the occupied refusal and no re-enable path. Its rationale
    keeps the consent ("an explicit opt-in ... leaves a declined setup
    reversible") and drops "preserves existing configuration", since the
    slot is never shared now. Its `code_symbol` cell drops the deleted
    symbols, keeps `offer_hooks/OfferHooks`, and gains the take's reading;
  - **TC-345**: method, expected and evidence amended to the cases above;
  - **IF-280** (Drafted): its data cell drops `[--enable]`;
  - **LLR-300**: detail amended for the take's new refusal; its
    `code_symbol` cell (`hooks_state/enable_hooks`) follows the code. The
    WI-834 grammar-removal row and WI-926 edit the same row, and whichever
    lands second rebases;
  - **SR-229**: acceptance checked at the sitting. It lists the take's
    admission cases, and gains the hooks refusal only if the sitting reads
    the list as exhaustive;
  - unchanged: SR-032.
- `RESYNC_PACK.md` carries the entry. The bar is green on the landing tip.

## Scope answers

- **S1:** one deliverable set. The reading, the consented install, the take's
  rule, the refusal and the deletion are one rule, and none stands alone.
  Split from WI-926, which shares no input with it (D-019).
- **S2:** yes; see `## Trust`. The state reading holds the lease take, and
  with consent it decides the install.
- **S3:** a closed space. Each guard event is either empty, exactly the
  guard's command by name, or something else. The consent answer is a yes
  or anything else. Only `none`, `on`, or a yes from `absent` whose install
  then reads `on` let a route go on; the rest refuse by default. The promise reaches settings that Claude
  Code, the kit and a user's ordinary edits produce. A user command that
  imitates the guard's name lies outside it (residue).
- **S4:** `single`. It has a Trust section, and it touches two script
  families (the coordinator guard and the dev-setup templates).
- **S5, the architectural delta:** a domain value is added (`absent` and
  `occupied` replace `off`). The take's start depends on a new input, the
  hooks' state. The merge is deleted. All of it is inside scope.
- **S6, dependencies:** `needs = []`. Soft edges, with the row that lands
  second rebasing:
  - WI-897 should follow this row (deliverable 6);
  - the WI-834 grammar-removal row and WI-926 share LLR-300;
  - the wi-798 lane edits the dev-setup templates;
  - WI-926 also edits `coordinator_guard.take`.

  No third-party dependency.
- **B1:** none; the Context's history commits to no work.
- **B3:** the reading is of the current settings at the moment of use. No
  past decision is recomputed; a declined answer is never stored or
  re-derived.
- **B4:** the consent is a person's answer at a terminal, not an owner act
  inside the Done-when. Every Done-when item is driven by a test that
  answers for them, and no item waits on a real answer.

## Calls ruled at filing

- **The split** (D-019): this row is split from WI-926 under S1.
- **The rule** (D-011): the hooks are checked by name, installed on first
  run when none are there, refused when other hooks occupy the slot, with no
  re-enable path.
- **Which route is the first run** (D-019): both the coordinator lease's take
  and dev-setup's readiness check.
- **Consent** (D-019, overruling the coordinator's recommendation to drop
  it): the install asks before it writes, and dev-setup's consent offer is
  kept.
- **The take without a terminal, with the hooks absent** (D-021, as
  recommended): it refuses, records no holder, writes nothing, and names
  dev-setup's consent step; at a terminal it asks. No answer is stored.

## Critique dispositions

Round 1 (Codex Sol, medium, 2026-10-16; CHANGES-REQUESTED, two findings):

- **S2, MAJOR: adopted.** A consented install whose write failed or was
  partial was not ruled, and the take could go on on consent alone.
  Deliverable 3 now reads "After a yes it reads the settings file again,
  and goes on only when that re-read reads `on`. The re-read is the
  construction, not a check of the write's success", and the Trust rulings
  read "A take goes on only at `none`, at `on`, or after a yes whose
  install then reads `on`". The Trust failure contract adds "An unreadable
  settings file or example (an OS error on read) is ruled the same way:
  `occupied`, the file and error named, nothing written" and "A write that
  fails makes that re-read read something other than `on`", with each
  consumer ruled: the
  take "refuses, records no holder, and names the file and the error";
  dev-setup's readiness check "reports it on a `[missing]` line naming the
  file, the error and the fix", and "a non-zero exit or empty output is
  reported on the same `[missing]` line with the reader's error, and is
  never read as `none`" (today both templates map a reader failure to
  `none`); the report "prints the state it reads". The Done-when adds "a
  consented install whose write fails refuses the take, records no holder,
  and names the file" and the dev-setup reader-failure case. No residue is
  added for a partial write: the install already writes through the kit's
  atomic write, so the re-read sees the old file or the new one.
- **S3, MAJOR: adopted.** Deliverable 6 said a changed example no longer
  reaches `on`, while `on` is decided by command name. The name rule wins,
  as the title and D-011 say "checked by name". Deliverable 6 now reads "a
  matcher-only change to the example still reads `on`, and nothing
  reinstalls the groups. An adopter who wants the new matcher removes the
  installed guard groups and runs the consented install again", and the
  RESYNC entry's item reads "that a matcher-only change to the guard groups
  still reads `on`, and that an adopter who wants the new matcher removes
  the installed guard groups and runs the consented install again".
