+++
id = "WI-1011"
title = "dev-setup reports the GitHub CLI and offers to install it, as an optional tool"
workstream = "scripts"
sr_refs = ["SR-032"]
specref = ""
buildtier = "quick"
safety_class = "ordinary"
planmode = "single"
priority = 3
+++

## Deliverable

dev-setup reports the GitHub CLI, `gh`, as an optional tool and offers it
consent-first, in this repository's `scripts/dev-setup.{sh,ps1}` and the
shipped `project-trajectory/scripts/dev-setup.template.{sh,ps1}`; the
`.cmd`/`.command` launchers hand their arguments on and are unchanged. Built
on the maintenance branch `maint/wi-1011`. By commit:

- `376edbd80`: the tests' stand-in builder takes an exit status and a list of
  present commands instead of two boolean flags (the readability report's
  flag-axis reading back to 0).
- `9ef7e138c`: `README.md` names the optional GitHub CLI among what
  dev-setup offers.
- `cfcc68d15`: the report line (marked optional, the platform's install
  command and `gh auth login`; the template's count leaves it out through a
  new optional argument to `report`/`Report`), the offer (`offer_gh`,
  `Offer-Gh`, `OfferGh`) from the install operations only, through winget,
  Homebrew, apt-get or dnf already on the machine, and the RESYNC entry
  (nothing forced).
- `71c7d9893`: LLR-372, TC-433 and TC-434 (Drafted) and 11 tests (31 cases)
  in `tests/test_run_devsetup.py`, every one on a PATH of stand-ins only; red
  at that commit.
- `415952047`: the plan, `docs/plans/WI-1011/plan.md`.
- `7358b47b7`: the critique dispositions and `planmode = "single"`.

Left undone: nothing in the Done-when. The three pseudo-terminal cases run
on POSIX only and skip on Windows; they were run under WSL Ubuntu (Python
3.12, dash as `sh`) and passed, as did this row's other POSIX cases. The
manual confirmation was made: `scripts\dev-setup.ps1 -Check` with
`C:\Program Files\GitHub CLI` on PATH reads `[ok]` for `gh` 2.105.0. Out of
scope, not done: the `gh` row in
`docs/dependencies.md` still reads "Forge-mode backend only"; dev-setup now
offers `gh` without depending on it, so the row may want a note. The
specref (`docs/plans/2026-11-11-test-tiers/HANDOFF.md`, §12.6) is cleared at
close, as a terminal row's is.

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
`dev-setup.sh`, and their launchers `dev-setup.cmd` and `dev-setup.command`,
which hand every argument to those two and need no change).
The shipped templates under `project-trajectory/scripts/dev-setup.template.*`
report and offer under their own tiers: their `-Baseline`/`--baseline` (and
`-Full`/`--full`) install where this repository's `-Install` does, and offer
only at an interactive terminal. `tests/test_dogfood_sync.py` deliberately does
not pin dev-setup (its module docstring says why), so this row's tests hold the
two families to the same report and offer.

**Architectural delta (scope critique S5).** None at the component or seam
level. `gh` adds one optional tool entry to the existing dev-setup report and
install offer in CMP-009, inside the four dev-setup scripts. The bare run's
readiness operation (`-ForRun`/`--for-run`, IF-292 and IF-293) is untouched:
its report shows the `gh` line, but it never offers `gh`, and `gh` never
changes its exit status.

## Done-when

- [x] Each dev-setup's standalone check (`-Check`; `--check` on POSIX), this
      repository's and the shipped template's, reports `gh` as present or
      missing, marked optional, with the install command for the platform
      (`winget install --id GitHub.cli` on Windows; `brew install gh` on macOS;
      the distribution's package or GitHub's apt repository on Linux) and the
      sign-in step, `gh auth login`. A missing `gh` is not counted among the
      template's missing components, and the check still exits 0.
- [x] `-Install` (`--install` on POSIX) offers to install it through the
      platform's package manager when one is on the machine (winget on
      Windows; Homebrew on macOS; apt-get, dnf or Homebrew on Linux), and
      installs it only on consent: an answer beginning `y` or `Y` installs;
      any other answer, an empty line, or closed input (end of file) skips the
      install and runs nothing. With no such package manager it prints the
      manual command and offers nothing; a failed install prints a warning
      and the manual command. A missing `gh` never fails setup: the
      operation's exit status is the one it has without the `gh` step.
- [x] The shipped dev-setup templates make the same report and offer, from
      their install tiers (`-Baseline`/`--baseline` and `-Full`/`--full`) and
      at an interactive terminal only, as their other installs are; a RESYNC
      entry covers the shipped change.
- [x] Tests on a stubbed PATH, with stand-ins for `gh` and each package
      manager and with nothing really installed, verify both families' present
      and missing reports, each platform's install command, and the consent,
      decline, closed-input, no-package-manager and failed-install arms; the
      touched dev-setup tests pass.

A manual confirmation, not a Done-when item: on this workstation `gh` is
installed at `C:\Program Files\GitHub CLI\`, and `scripts\dev-setup.ps1
-Check` from a console whose PATH carries that directory reports it present.

## Critique dispositions

Round 1 (Gemini Argon, 2026-11-19, `docs/reviews/2026-11-19-scope-critiques/WI-1011.md`):
CHANGES-REQUESTED, three findings.

- **S4 (MAJOR), `planmode` missing and the S5 delta unstated: adopted as
  `planmode = "single"`.** The platform and consent table (which package
  manager each platform offers through, what each answer does, where the offer
  sits in each family's tiers) is a design choice across four scripts, so a
  short plan records it before code (`docs/plans/WI-1011/plan.md`). The S5
  answer is the "Architectural delta" paragraph in Context: no new component
  or seam, and `-ForRun`/`--for-run` untouched.
- **S3 (MINOR), the closed default: adopted.** The second Done-when item now
  states that only an answer beginning `y`/`Y` installs, that any other answer,
  an empty line or closed input skips, that an absent package manager prints
  the manual command and offers nothing, that a failed install warns with the
  manual command, and that the exit status never depends on `gh`. The third
  item states the template's interactive-only offer.
- **B4 (MINOR), the workstation-dependent check: adopted.** The fourth
  Done-when item is now a test on a stubbed PATH covering present and missing
  for both families, with no ambient `gh` able to show through. The workstation
  run is kept as a manual confirmation below the list, not as a Done-when.
