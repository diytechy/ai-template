## 2026-11-19 — WI-1011: dev-setup reports the GitHub CLI and offers it consent-first, as an optional tool

Deferred open items: none.

Built on the maintenance branch `maint/wi-1011`, outside the lane workflow, at
the operator's direction, with the commit hooks on.

- **Critique:** the three round-1 findings adopted: `planmode = "single"` with
  the architectural delta stated (none; `-ForRun`/`--for-run` untouched), the
  closed default spelled out in the Done-when, and the workstation run
  replaced by a stubbed-PATH test (kept as a manual note, and confirmed).
- **Report:** every dev-setup, this repository's and the shipped template's,
  `.sh` and `.ps1`, prints one `GitHub CLI gh (optional: ...)` line: `[ok]`, or
  `[missing]` with the platform's install command (winget on Windows and Git
  Bash; brew on macOS; the distribution's package or GitHub's apt repository
  on Linux) and `gh auth login`. The template's missing count leaves it out.
- **Offer:** the install operations only (`-Install`/`--install` here; the
  template's baseline and full tiers), through a package manager already on
  the machine, run only on a yes. Here the answer is read as the agent-CLI
  offers read it; the template asks at an interactive terminal only. No
  package manager prints the manual command; a failed install warns; no arm
  changes an exit status. The bare run reports the line and never offers it.
- **Rows:** LLR-372, TC-433, TC-434, all Drafted, under SR-032.
- **Tests:** 11 tests (31 cases) in `tests/test_run_devsetup.py`, each on a
  PATH of stand-ins only, so a host's `gh` never shows through and nothing is
  installed. On Windows 28 pass and the 3 pseudo-terminal cases skip; under
  WSL Ubuntu the 18 POSIX cases pass.
- **RESYNC:** one entry; nothing forced, since dev-setup is the adopter's
  after scaffold.
