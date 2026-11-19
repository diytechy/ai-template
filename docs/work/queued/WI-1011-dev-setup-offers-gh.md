+++
id = "WI-1011"
title = "dev-setup reports the GitHub CLI and offers to install it, as an optional tool"
workstream = "scripts"
sr_refs = ["SR-032"]
specref = "docs/plans/2026-11-11-test-tiers/HANDOFF.md#126-progress-log"
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand on 2026-11-19 at the operator's direction: the GitHub CLI
should be "an optional package that comes with the setup.cmd", which in this
repository is `scripts/dev-setup.cmd`. Without `gh`, a
session cannot read the CI state of a pushed branch (HANDOFF §6, B6: the
Actions history could not be checked). It was installed on this workstation
by hand the same day (`winget install --id GitHub.cli`, 2.105.0); `gh auth
login` is still the operator's.

dev-setup already reports and offers the agent CLIs, consent-first:
`-Check` reports, and `-Install` offers each one (`scripts/dev-setup.ps1`,
`dev-setup.sh`, and their launchers `dev-setup.cmd` and `dev-setup.command`).
The shipped templates under `project-trajectory/scripts/dev-setup.template.*`
carry the same structure, and `tests/test_dogfood_sync.py` holds the two
equal in structure.

## Done-when

- [ ] `-Check` reports `gh` as present or missing, marked optional, with the
      install command for the platform (`winget install --id GitHub.cli` on
      Windows; `brew install gh` on macOS; the distribution's package or
      GitHub's apt repository on Linux) and the sign-in step, `gh auth login`.
- [ ] `-Install` (`--install` on POSIX) offers to install it and installs it
      only on consent. A missing `gh` never fails setup.
- [ ] The shipped dev-setup templates make the same offer, so an adopter's
      setup has it too; a RESYNC entry covers the shipped change.
- [ ] The touched dev-setup tests pass, and a run on this workstation reports
      `gh` as present.
