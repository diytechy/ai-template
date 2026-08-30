# Cross-platform scripting: Windows, macOS and Linux from one stdlib-preferred kit — DRAFT

> **DRAFT (agent-authored, WI-546, 2026-08-30).** Drafted by the unattended lane so the `hat.CROSS-PLATFORM` roster entry has a `knowledge` value to point at; the owner reviews and cuts at RETURN, per the `hats.toml` header's own rule. This distills THIS repo's accumulated perspective from its own decisions and surfaces — it is not retrieved external research, and its claims are the drafter's reading, not a settled finding.

This pack records what a reviewer wearing the CROSS-PLATFORM hat looks for HERE.
The charter question — "Which of Windows, macOS and Linux breaks this — path
separators, line endings, console encoding, shell quoting, case sensitivity?" —
is not abstract in this repo: SR-114's rationale states that *every one of those
differences has been a real failure here*, which is why testing one platform and
reading the others by inspection was rejected.

## What this hat looks for here

The obligation is two requirements, not a style preference. **SR-114** (kit
scripts run on Python 3.11+ across Linux, Windows and macOS) and **SR-034** (kit
scripts run on stdlib plus ledger-declared dependencies) — both tagged
`aspect = "portability"` in `docs/requirements/system-requirements.toml`, both
realizing SN-011 — are what CLAUDE.md's "stdlib-preferred and cross-platform"
principle discharges. The two interlock: a shipped check must run on a clean
interpreter with *nothing installed* so an adopter can run it on any of the three
OSes without a toolchain, which is also why the stdlib bar is strictest for
*shipped* checks (SR-034's acceptance singles out the shipped tier).

The evidence surface is the CI matrix in `.github/workflows/test.yml`: Linux,
Windows and macOS × Python 3.11 and 3.x, with the macOS+3.11 cell deliberately
excluded (the 3.11 floor is a language/stdlib guarantee already covered on Linux
+ Windows; macOS's job is OS-specific behavior — `fcntl.flock`, paths, git
worktrees — that does not vary by Python version). A rule "true only on the
author's platform" is caught by a red cell there, not by review prose — so the
hat's real job is the surfaces the matrix cannot see, or the changes that ship
*before* a green matrix exists.

The recurring hazards, each with a real carrier in this repo:

- **Line endings.** LF is load-bearing for `#!/bin/sh` shebangs: a CRLF
  `agent-resume.sh` breaks even under Git Bash. `gitattributes.template` pins
  `*.sh`/`*.command`/git-hooks to `eol=lf` and `*.cmd`/`*.bat`/`*.ps1` to
  `eol=crlf` (LF can misparse batch `goto` labels), and `bootstrap.py` writes
  those files byte-exact with `newline="\n"` so a Windows `core.autocrlf=true`
  clone cannot corrupt the scaffold before `.gitattributes` takes effect.
- **Console/text encoding.** Scripts pass `encoding="utf-8"` explicitly on I/O
  (~186 occurrences across the scripts) rather than trusting the platform default
  — on Windows that default is still often a legacy code page, so an implicit
  open is a latent mojibake bug. Generated docs also pin `newline="\n"` so output
  is byte-identical on every OS.
- **Path separators.** `pathlib`/`os.path` throughout; a hand-built `"a/b"` or a
  drive-letter assumption is the smell.
- **Shell quoting.** `run_menu.py` keeps *two* quoting paths behind `os.name`:
  `shlex.quote` on POSIX, a two-phase MSVCRT+cmd.exe caret quoter (`_win_quote`)
  on Windows, because cmd.exe re-parses `&`/`|`/`%VAR%` that POSIX never would.
  The launchers avoid the problem entirely by piping the agent prompt to STDIN
  (no `{prompt}` on the command line) — immune to OS arg-length caps and Windows
  batch re-parsing.
- **OS primitives with no portable stdlib call.** The coordinator lock branches
  `fcntl.flock` (POSIX) vs `msvcrt.locking` (Windows) in `agent_common._take_os_lock`
  — the macOS matrix cell exists largely to exercise this class.

## Application

- **A new script or launcher is a CROSS-PLATFORM review trigger** (the hat
  `applies_when` fires on `scripts`/`launcher`/`shell` tags). Ask the charter's
  five questions against a concrete carrier, not in the abstract.
- **Three launchers, one source of truth.** `agent-resume.sh` (POSIX) and
  `agent-resume.cmd` (Windows) are twins that must stay in sync; `agent-resume.command`
  (macOS Finder wrapper) `exec`s the `.sh` so it inherits, not copies, the logic.
  A change to one launcher's slots that skips its twin is the classic
  author's-platform defect.
- **"Found" is not "runnable."** Both launchers probe each interpreter by
  *running* it twice (`-c "pass"`, then a `version_info >= (3,11)` check) because
  a Windows `python3`/`python` on PATH is often the Microsoft-Store alias stub
  that runs nothing. Prefer this repo's own `.venv`, probing both `bin/` (POSIX)
  and `Scripts/` (Windows-created) layouts.
- **Don't fight a documented residual — record it.** `_win_quote` still lets
  cmd.exe expand `%VAR%`; the code documents that limit rather than adding fragile
  escaping. A bounded, stated gap beats a clever cross-platform hack that only the
  author understands.

## Open questions / bounded here

- The matrix is the evidence, but it runs *after* a change; nothing catches a
  platform assumption at authoring time except this hat. Treat a green Linux
  local run as necessary-not-sufficient.
- Case sensitivity (the charter names it) has no dedicated instrument here today;
  it lives on the reviewer's checklist, not in a check. Flag a filename that
  differs only by case, or an import/path that assumes a case-folding filesystem.
