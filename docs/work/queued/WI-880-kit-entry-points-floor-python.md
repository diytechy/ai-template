+++
id = "WI-880"
title = "Every kit entry point runs kit Python on a floor-resolved interpreter, not a bare python"
workstream = "process"
sr_refs = ["SR-046", "SR-032"]
specref = "project-trajectory/scripts/run.template.cmd"
buildtier = "medium"
safety_class = "ordinary"
priority = 4
+++

## Context

Filed by the coordinator on 2026-10-09 from WI-834's landing (fb1990aa),
under the owner's ruling recorded as D-019 in
`docs/decisions/wi-834.toml`: the hook opt-in binds the guard's hooks to the
floor-resolved interpreter in the machine-local settings, and "the kit-wide
leftovers of the class go to a follow-up row".

WI-834 made the `run.*` launchers, dev-setup's readiness check, the relaunch
launchers and the guard's hook opt-in run kit Python on one interpreter that
passes the 3.11 floor (rounds 4, 5 and 11; the candidate lists are pinned
equal to each dev-setup's runtime search). Kit Python is still started by a
bare `python` at the sites below, where an older interpreter first on PATH
(an ordinary workstation: on this box `C:\Python38` beside 3.11 and 3.12)
fails on `tomllib`.

**Owner ruling, 2026-10-10** (attended; decisions `coordinator-2026-10-10.toml`
D-004): the committed guard hooks move to the machine-local opt-in.
`.claude/settings.json` stops carrying them, and WI-834's opt-in writes them
into `.claude/settings.local.json`, bound to the floor-resolved interpreter.
A machine that has not opted in runs no guard hooks.

Landing order (scope critique, 2026-10-10; D-005): one row, one lane. The
four sites share one interpreter resolution and its candidate-parity pin.
Landing them separately would leave the class open at the sites still
waiting, and each would need its own RESYNC entry for one migration.

## Trust

The hook files decide whether a tool call or a commit proceeds
(`project-trajectory/PROCESS.md` §3, "When a guard is owed"):

- **The guard's hook groups in `.claude/settings.local.json`.** Producer:
  the guard's opt-in (`coordinator_guard.py hooks`, offered by dev-setup),
  which writes the file whole. A failed write exits non-zero, naming the
  file, and leaves the previous file. Consumer: the Claude Code harness,
  an external reader. The kit reads the file only in the opt-in's own
  re-run and report. Ruling: an absent file, or one without the guard's
  groups, means the machine has not opted in, and no guard runs. That is
  the owner's ruling above, and dev-setup's readiness report names it. A
  malformed file is refused by the opt-in, which never overwrites a file it
  cannot parse.
- **The shipped git pre-commit hook.** Producer: bootstrap and dev-setup's
  install. Consumer: git. Ruling: when no interpreter passes the 3.11
  floor, the hook fails the commit and names dev-setup's install as the
  fix. It never runs the checks on an older interpreter, and never skips
  them.

## Done-when

- Each site below runs kit Python on a floor-resolved interpreter, resolved
  once at its own boundary, with no second existence-only choice:
  - this repository's committed `.claude/settings.json` guard hooks (bare
    `python`; the coordinator's own guard runs through them): removed from
    the committed file, per the owner's ruling, and this repository's
    coordinator workstation opts in through the guard's machine-local
    opt-in in the same landing;
  - the `docs/stack.ini` `[run]` lines (bare `python`; `run trajectory` dies
    under an older interpreter first on PATH);
  - the shipped git pre-commit hook (`project-trajectory/hooks/pre-commit`),
    which picks an interpreter by runnability, not the floor;
  - this repository's `scripts/dev-setup.ps1 -Install`, which stops where
    `dev-setup.sh --install` offers the runtime.
- Tests, red first, on real interpreters (no fake runner), with the
  existing candidate-parity pin extended to any new launcher.
- RESYNC_PACK entry for the shipped sites, migration flagged.
