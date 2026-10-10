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

## Done-when

- Each site below runs kit Python on a floor-resolved interpreter, resolved
  once at its own boundary, with no second existence-only choice:
  - this repository's committed `.claude/settings.json` guard hooks (bare
    `python`; the coordinator's own guard runs through them; the owner
    decides whether they move to the machine-local opt-in);
  - the `docs/stack.ini` `[run]` lines (bare `python`; `run trajectory` dies
    under an older interpreter first on PATH);
  - the shipped git pre-commit hook (`project-trajectory/hooks/pre-commit`),
    which picks an interpreter by runnability, not the floor;
  - this repository's `scripts/dev-setup.ps1 -Install`, which stops where
    `dev-setup.sh --install` offers the runtime.
- Tests, red first, on real interpreters (no fake runner), with the
  existing candidate-parity pin extended to any new launcher.
- RESYNC_PACK entry for the shipped sites, migration flagged.
