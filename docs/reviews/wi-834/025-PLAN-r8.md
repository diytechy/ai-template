# WI-834 rework round 8: coverage plan

Answers `docs/reviews/wi-834/024-REVIEW-A-5d0a27e.md` (F1, F2: its two
`[MAJOR]` lines, in order). Step A confirmed both at lane tip c1326f37; this
step B plan is for tip c224690b. Dispute sitting 025
(`025-ADJUDICATE-22cf09c.md`, decision D-024) ruled R24F1 FIX and drew the
coverage line: the hook covers the word the shell's own grammar makes the
command. Invocation operators (`&`, `.`) are inside; wrapper commands that
take a command as an argument are outside.

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| R1 | F1 (ruled FIX, sitting 025, D-024): PowerShell's dot invocation (`. claude -p x`, `$r = . claude -p x`) is read as invoking its following command | F1; D7; D10; D25; SR-229; TC-339 | IF-274; IF-275 | |
| R2 | F2: the readiness report never aborts on an unavailable workstation tool; it reports the tool missing and still returns the runtime result | F2; D28; D30; D31; D39; SR-227; SR-230; TC-342; TC-343 | IF-293 | |

## R1 (F1): ruled FIX

- **Confirmed** through the actual hook. Probe
  `C:/Projects/ai-template.wt/review-tmp/2026-10-09-wi834r8/f1-probe-r8.py`
  runs `coordinator_guard.py --root <scratch> hook` as a subprocess at
  `context_guard_pct = 0` inside a window covering now. The scratch registry
  names `claude`. "no decision" means close-down context only, no deny:

  ```text
  PowerShell  '& claude -p x'          -> deny
  PowerShell  '. claude -p x'          -> no decision (not denied)   review form
  PowerShell  '$r = . claude -p x'     -> ALLOW                      review form
  PowerShell  '$r = & claude -p x'     -> deny
  PowerShell  ". 'claude' -p x"        -> ALLOW                      extra probe
  ```

  `&` is an operator boundary in the PowerShell dialect, so the command after
  it starts a new simple command. `.` cannot be an operator (paths and
  numbers hold dots), so `_segment_command` takes the word `.` as the
  executable.
- **Unlisted sites of the same class (an invocation prefix read as the
  command word), probed, not widened:**

  ```text
  Bash        'command claude -p x'                         -> ALLOW
  Bash        'builtin claude -p x'                         -> ALLOW   (bash refuses it anyway: claude is no builtin)
  Bash        'exec claude -p x'                            -> ALLOW
  Bash        'nohup claude -p x'                           -> ALLOW
  Bash        'time claude -p x'                            -> deny    (a reserved word, `_RESERVED`)
  Bash        'echo x | xargs claude -p'                    -> ALLOW
  Bash        "sh -c 'claude -p x'"                         -> ALLOW
  PowerShell  "Start-Process claude -ArgumentList '-p x'"   -> ALLOW
  PowerShell  "Invoke-Expression 'claude -p x'"             -> ALLOW
  PowerShell  "iex 'claude -p x'"                           -> ALLOW
  PowerShell  'cmd /c claude -p x'                          -> ALLOW
  ```

  The spec's declared coverage names the `timeout` and `env` prefixes,
  `VAR=value` and the four chain operators, and says "script wrappers are not
  inspected". Sitting 025 ruled the line: the dot is grammar like `&` and
  is inside; the wrapper commands above stay outside and untouched (see
  Excludes).
- **Sites:** `coordinator_guard.py` `command_words` (the PowerShell branch
  through `_assigned`) and `_segment_command`. Search:
  `rg -n "_RESERVED|_OPTION_ARGS|def _segment_command|def command_words|def _assigned" project-trajectory/scripts/coordinator_guard.py`.
- **Owning boundary (as ruled):** the PowerShell branch of `command_words`,
  beside `_assigned`. A leading unquoted word `.` (PowerShell's dot
  invocation operator) is passed over, as `&` already is by the reader, so
  its following word is the command. A quoted `'.'` stays data. About 5
  lines, and about 4 TC-339 cases (`. claude -p x`, `$r = . claude -p x`,
  `. 'claude' -p x` denied; `. ./setup.ps1` allowed), pinned red first in
  TC-339's existing QUOTED_DENIED and QUOTED_ALLOWED.

## R2 (F2)

- **Confirmed** on the real path. Probe
  `C:/Projects/ai-template.wt/review-tmp/2026-10-09-wi834r8/f2-probe.py` uses
  a real static PATH:
  `C:\Users\Peter\AppData\Local\Programs\Python\Python311;C:\WINDOWS\System32;C:\WINDOWS\System32\WindowsPowerShell\v1.0;C:\WINDOWS`.
  Git is not on it (`shutil.which("git")` is None); a working Python 3.11 is.
  The probe runs on a fresh template scaffold (`bootstrap.py --dest`) and on
  this repository:

  ```text
  scaffold dev-setup.ps1 -ForRun -Python <py>      -> exit 1   [ok] runtime (python); [missing] git; git : The term 'git' is not recognized ... $hooksPath = (git config --get core.hooksPath 2>$null)
  scaffold run.cmd (bare)                          -> exit 1   ... run: the runtime is still missing; take the step above, then run again.
  root scripts/dev-setup.ps1 -ForRun -Python <py>  -> exit 1   same throw
  root run.cmd (bare)                              -> exit 1   same; no menu
  ```

  Probe `f2-probe-more.py`, with the same PATH, and for sh Git's `usr\bin`
  (sh, no git):

  ```text
  scaffold dev-setup.ps1 -Check            -> exit 1 (its contract is: read-only, always exit 0)
  root scripts/dev-setup.ps1 -Check        -> exit 1
  scaffold dev-setup.sh --for-run --python -> exit 0, [missing] git
  scaffold dev-setup.sh --check            -> exit 0, [missing] git
  root scripts/dev-setup.sh --for-run      -> exit 0, [missing] git
  root scripts/dev-setup.sh --check        -> exit 0, [missing] git
  ```
- **Class:** the readiness report aborts on an unavailable workstation tool
  instead of reporting it missing. Under `$ErrorActionPreference = "Stop"`,
  calling an absent native command throws `CommandNotFoundException`, and
  `2>$null` does not stop it, so the script dies before its runtime result.
- **Sites** (every native workstation-tool call in the dev-setups, from
  `grep -n -E "\b(git|npm|code|mmdc|npx|claude|codex|winget|uv)\b +[a-z-]"`
  over the four files):
  - (a) IN THE CLASS: `project-trajectory/scripts/dev-setup.template.ps1`:
    - :158 `$hooksPath = (git config --get core.hooksPath 2>$null)`, the
      report every tier runs (`-Check`, `-ForRun`, `-Baseline`, `-Full`);
    - :277 `$hooksPathNow = (git config ...)` and :280
      `git config core.hooksPath .githooks`, the `-ForRun` floor offer;
    - :294 `$null = git rev-parse --is-inside-work-tree 2>$null` and :296
      `git config core.hooksPath .githooks`, the `-Baseline` / `-Full` floor
      wiring.
  - (b) IN THE CLASS: `scripts/dev-setup.ps1` (this repo's):
    - :158 `$hooksPath = (git config ...)` (`-Check`, `-ForRun`, `-Install`);
    - :314 `$null = git rev-parse ...` and :316 `git config ...` (`-Install`).
  - Not in the class: `& claude setup-token` (template :238, root :194) and
    `& npm install -g` (root :237) are each called only after `Have`;
    `(Get-Command $cand).Source` (root, the ambient-debris warning) is behind
    `Have`; `py`/`python` are probed through `HavePython`'s `try`.
  - Not in the class, checked: `dev-setup.template.sh` and
    `scripts/dev-setup.sh` query git only inside `$(...)` with `2>/dev/null`
    or behind `if git rev-parse ...`, so a missing git yields the
    `[missing] git` line and the run continues (the probes above). Observed,
    out of class: the template's `maybe_install` reads with a bare
    `read -r ans` under `set -e`, so an EOF at a real terminal would end the
    run. That is no workstation query, and it is reachable only
    interactively.
  - The launchers (`run.cmd`, `run.template.cmd`) are correct as built: they
    report what dev-setup returned.
- **Search:** the grep above; `rg -n "ErrorActionPreference" project-trajectory/scripts/dev-setup.template.ps1 scripts/dev-setup.ps1`.
- **Owning boundary:** in each PowerShell dev-setup, a workstation tool is
  queried only once `Have` reports it present. One reading, `$haveGit`, is
  taken where the report states `git`. The `core.hooksPath` read, the floor
  offer and the floor wiring each run only with it; without it the floor
  line reads `[missing]` naming git as its cause, nothing is offered or
  wired, and the run reaches its runtime result (IF-293 / LLR-320). The
  standalone `-Check` returns to exit 0. No `try`/`catch` around the call:
  the call is simply not made.
- **Pins (red first):**
  - `tests/test_run_devsetup.py`, Windows: a bare `run.cmd` on a template
    scaffold, with a real static PATH that holds this interpreter's
    directory and the Windows system directories but no git, reaches the
    menu. Separately, `dev-setup.ps1 -ForRun -Python <this interpreter>`
    exits 0 reporting `[missing] git`, and `-Check` exits 0 (TC-342,
    TC-343). The PATH is built from real directories on any Windows host,
    with no fake executable.
  - The same for this repository's root `run.cmd` / `scripts/dev-setup.ps1`.
  - POSIX: `dev-setup.sh --for-run` without git already passes; it is pinned
    the same way so it cannot regress.

## Exclusions

Excludes: TC-266; TC-267; TC-268; TC-303; TC-315; TC-316; TC-317; TC-318; TC-321; TC-322; TC-323; TC-324; TC-329; TC-330; TC-340; TC-341; TC-344; TC-345 — the retention, relaunch, sign-in, adjudication and hook opt-in paths are untouched by round 8 (F1 is the hook's launch reading, F2 the readiness report's workstation queries); they run in their tiers unchanged.
Excludes: F1 — the wrapper forms (Start-Process, Invoke-Expression/iex, cmd /c, sh -c, exec, command, builtin, nohup, xargs, script files) take a command as an argument, so they are outside the declared any-command-word coverage by dispute 025's ruling (D-024); not changed.
Excludes: D1; D2; D3; D4; D5; D6; D8; D9; D11; D12; D13; D14; D15; D16; D17; D18; D19; D20; D21; D22; D23; D24; D26; D27; D29; D32; D33; D34; D35; D36; D37; D38; D40; D41; D42; D43; D44; D45; D46; D47; D48; D49; D50; D51; D52; D53; D54; D55; D56; D57; D58; D59; D60; D61; D62; D63; D64; D65; D66; D67; D68 — built in the lane's earlier rounds (through round 7 and sitting 023) and not reopened by round 024, which reopens only the hooks' launch reading (D7/D10/D25, F1) and the readiness operation's report and result (D28/D30/D31/D39, F2).
