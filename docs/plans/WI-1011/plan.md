# WI-1011 plan: dev-setup reports the GitHub CLI and offers it, as an optional tool

Planned on branch `maint/wi-1011` at `7358b47b7` (the critique dispositions),
cut from `refactor_again` at `b696b6c36`. A maintenance-branch build: no plan
critique or pass record.

## The construction

One optional tool entry, `gh`, added to the report and the install offer of the
four dev-setup scripts. The launchers (`dev-setup.cmd`, `dev-setup.command`,
both families) hand their arguments to these scripts and do not change.

| | This repository (`scripts/dev-setup.*`) | Shipped template (`project-trajectory/scripts/dev-setup.template.*`) |
|---|---|---|
| Report | one `Report`/`report` line beside the agent CLIs' | one line after the roles, passed `optional` so the missing count leaves it out |
| Offered by | `-Install` / `--install`, after the agent CLIs' offers | `-Baseline`/`--baseline` and `-Full`/`--full`; never the run tier |
| Consent pattern | `Offer-Cli`/`offer_cli`'s: a `[y/N]` read on every run, where an empty line or closed input reads as no | `MaybeInstall`/`maybe_install`'s: interactive terminal only, else "non-interactive; skipping install" |
| Bare run (`-ForRun`) | reports the line, offers nothing | the same |

### The platform table

The install goes through a package manager already on the machine. Nothing is
fetched or piped into a shell (`test_no_setup_script_pipes_a_remote_script_into_a_shell`
holds that).

| Platform (`uname`, or the `.ps1`) | Offered through, in order | Install command | Report hint (the manual route) |
|---|---|---|---|
| Windows (`.ps1`; `MINGW*`/`MSYS*`/`CYGWIN*` under Git Bash) | winget | `winget install --id GitHub.cli` | that command, or the installer from https://cli.github.com |
| macOS (`Darwin`) | Homebrew | `brew install gh` | that command, or the macOS package from https://cli.github.com |
| Linux (anything else) | apt-get, dnf, Homebrew | `sudo apt-get install gh`, `sudo dnf install gh`, `brew install gh` | the distribution's gh package, or GitHub's apt repository (https://github.com/cli/cli/blob/trunk/docs/install_linux.md) |

Every hint ends with the sign-in step, `gh auth login`.

### The answer table (each install operation)

| Input | Result |
|---|---|
| `gh` already on PATH | no offer; the report reads `[ok]` |
| no package manager from the table | no prompt; `[skip]` with the manual command |
| an answer beginning `y`/`Y` | the install command runs once |
| `n`, any other answer (` y`, with its leading blank, included), an empty line, closed input | nothing runs; the skip line names the manual command |
| the install command fails | `[warn]` with the manual command |
| any of the above | the operation's exit status is unchanged |

The template asks only at an interactive terminal, so piped input there is
never an answer.

## Files

- `scripts/dev-setup.ps1`, `scripts/dev-setup.sh`: the report line, `Offer-Gh`
  / `offer_gh`, the `-Install` call, the usage comment and the check footer.
- `project-trajectory/scripts/dev-setup.template.ps1`,
  `project-trajectory/scripts/dev-setup.template.sh`: `Report`/`report` gain
  the optional argument; the report line; `OfferGh` / `offer_gh`, called from
  the install tiers only; the usage comment (and the `.sh` help range).
- `tests/test_run_devsetup.py`: the tests below; it already holds the stubbed
  PATH, pseudo-terminal and real-console helpers they reuse.
- `docs/requirements/low-level-requirements.toml` (LLR-372),
  `docs/test/test-cases.toml` (TC-433 report, TC-434 offer), all Drafted.
- `project-trajectory/RESYNC_PACK.md`: the entry. dev-setup is copied once at
  scaffold and not re-synced, so nothing is forced.

Encoding traps kept: the `.ps1` files keep their UTF-8 BOM and CRLF; no `.cmd`
changes.

## The arms the tests pin

Every run uses a PATH that holds only stand-ins: `uname` printing the platform,
this interpreter as `python3`/`python` where the operation needs one, the shell
tools the script runs (each forwarding to the real one), `gh` when present, and
recording package-manager stand-ins (and a `sudo` that runs its arguments). A
`gh` installed on the host cannot show through. Nothing is really installed.

TC-433, the report:

1. This repository's `dev-setup.sh --check` under Darwin, Linux and Git Bash:
   missing names the platform's command and `gh auth login`, marked optional;
   present reads `[ok]`; exit 0.
2. The shipped template's `dev-setup.template.sh --check` (copied into a
   scratch tree) under Darwin, Linux and Git Bash: the same, and the missing
   count is the same with and without `gh`.
3. This repository's `dev-setup.ps1 -Check` and the template's
   `dev-setup.template.ps1 -Check` on Windows: present and missing, winget's
   command and `gh auth login`; the template's count is unchanged.

TC-434, the offer:

4. This repository's `dev-setup.sh --install`, per platform and package
   manager (brew on Darwin, apt-get and dnf on Linux, winget under Git Bash):
   `y` runs the stand-in with the install arguments; `n`, an empty line,
   closed input and ` y` (a leading blank) run nothing; exit 0 each time.
5. The same with no package manager (the `[skip]` line, no prompt), with a
   failing one (`[warn]`) and with `gh` present (no offer), exit 0.
6. This repository's `dev-setup.ps1 -Install` on Windows: `y`, `n`, an empty
   line, closed input, ` y`, no winget, failing winget, `gh` present.
7. The template's install tier, `dev-setup.template.sh --baseline` and
   `dev-setup.template.ps1 -Baseline`, with piped (and, for `.sh`, closed)
   input: nothing is offered or run ("non-interactive"), exit 0. At a
   pseudo-terminal (POSIX, `.sh`): `y` installs, `n` and ` y` do not. At a
   real console (Windows, `.ps1`): `y` installs, `n` does not.
8. The bare run's readiness operation (`--for-run` / `-ForRun`), both
   families, at a pseudo-terminal (POSIX, `.sh`) or a real console (Windows,
   `.ps1`), answering yes throughout, with `gh` missing and a package manager
   present: the `gh` line is reported, no `gh` offer is made.
