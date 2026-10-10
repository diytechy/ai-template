# WI-834 rework round 5: coverage plan

Answers `docs/reviews/wi-834/016-REVIEW-A-e6717f0.md` (F1, F2: the two
`[MAJOR]` lines at its end, in the order written; plan_coverage reads the
same two). Lane rebased onto ed2533cb; step A confirmed both findings at
tip a47198e4, and this step B plan is for tip 8dc0d6a8. F1 was ruled FIX by
dispute sitting 017 (`017-ADJUDICATE-1003705.md`, decision D-020); F2's
remedy is the owner's ruling D-019.

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| R1 | F1 (ruled FIX, sitting 017, D-020): a PowerShell assignment's right-hand command is read as the command it is; a quoted or variable right-hand side stays data | F1; D7; D10; D25; SR-229; TC-339 | IF-274; IF-275 | |
| R2 | F2 (owner ruling D-019): the opt-in binds the guard hooks to the interpreter it runs on, in the machine-local settings file; the relaunch launchers resolve a floor interpreter with the run launchers' probe and candidates; the guard's injected command names the hook's own interpreter | F2; D10; D14; D43; D51; SR-230; SR-227; TC-340; TC-345; TC-342 | IF-280 | |
| R3 | The round's regression bar: the hook-reading, opt-in, relaunch and launcher pins re-run, with R1's and R2's pins added | TC-317; TC-318; TC-343 | intra-module (no seam changes in this row) | R1; R2 |

## R1 (F1): ruled FIX

- **Confirmed** on the real hook. Probe
  `C:/Projects/ai-template.wt/review-tmp/2026-10-09-wi834r5/f1-probe.py`
  runs `coordinator_guard.py --root <scratch> hook` as a subprocess with
  `context_guard_pct = 0` and an armed `blackout` window covering now (UTC):

  ```text
  window 20:42-22:42 now Fri 21:42 UTC; context_guard_pct = 0
  PowerShell  'claude -p x'               exit=0 -> deny
  PowerShell  '$response = claude -p x'   exit=0 -> no decision (close-down context only, no deny)
  PowerShell  "$response = 'claude -p x'" exit=0 -> ALLOW (no output)
  Bash        'r=$(claude -p x)'          exit=0 -> deny
  ```

  In-process, `shell_line.segments(c, "powershell")` and
  `coordinator_guard.command_words(c, "powershell")`:

  ```text
  '$response = claude -p x'   [['$response', '=', 'claude', '-p', 'x']]  ['$response']
  "$response = 'claude -p x'" [['$response', '=', 'claude -p x']]        ['$response']
  '$a, $b = claude -p x'      [['$a,', '$b', '=', 'claude', '-p', 'x']]  ['$a,']
  '[string]$r = claude -p x'  [['[string]$r', '=', 'claude', '-p', 'x']] ['[string]$r']
  '$r += claude -p x'         [['$r', '+=', 'claude', '-p', 'x']]        ['$r']
  '$r = (claude -p x)'        [['$r', '='], ['claude', '-p', 'x']]       ['$r', 'claude']
  '$r = & claude -p x'        [['$r', '='], ['claude', '-p', 'x']]       ['$r', 'claude']
  ```

  `_segment_command` (coordinator_guard.py:965) skips only POSIX
  `NAME=value` words (`_ASSIGNMENT`, :873), so the PowerShell target
  `$response` is taken as the command word. The reader also drops quoting, so
  `$r = 'claude -p x'` and `$r = claude -p x` cannot be told apart from the
  words alone.
- **Class:** the hook's shell reading (rounds 001 F1, 004 and now 016). As
  its third review round it went to dispute sitting 017, which ruled R16F1
  FIX: ordinary output capture inside the declared "any command word"
  coverage, fixed at the one shell-reading boundary with quoted right-hand
  values kept as data (D-020).
- **Sites:** `kitlib/shell_line.py` `segments` (the one reading; PowerShell
  words lose whether they were quoted) and `coordinator_guard.py`
  `_segment_command` (assignment skipping is POSIX-only).
- **Search:** `rg -n "_ASSIGNMENT|def _segment_command|def command_words|def segments" project-trajectory/scripts/coordinator_guard.py project-trajectory/scripts/kitlib/shell_line.py`.
- **Owning boundary (as ruled):** `shell_line.segments` keeps, on each word,
  where its first quoted piece starts (`Word.quoted_at`), so a quoted
  right-hand value stays data;
  `_segment_command`, for the PowerShell dialect, skips a leading assignment
  (`$name`, `[type]$name`, `$env:NAME`, a comma list of these; operators `=`
  `+=` `-=` `*=` `/=` `%=` `??=`) and takes the next unquoted, non-`$` word as
  the command (also with the operator written against the target,
  `$r=claude`). A variable or quoted right-hand side is an expression: no
  command. Pins (red first): the ruling's table in TC-339's QUOTED_DENIED
  (`$response = claude -p x`, `[string]$r = ...`, `$a, $b = ...`,
  `$r += ...`, `$env:X = ...`, plus `$r ??= ...` and `$r=claude ...`) and
  QUOTED_ALLOWED (`$r = 'claude -p x'`, `$r = "claude -p x"`,
  `$r='claude -p x'`, `$r = $other`).

## R2 (F2)

- **Confirmed** on the real path. Probe
  `C:/Projects/ai-template.wt/review-tmp/2026-10-09-wi834r5/f2-probe.py`:
  a real scaffold (`bootstrap.py --dest <d> --agents claude`), its
  `process.toml` armed with a window covering now, and the real opt-in
  (`coordinator_guard.py hooks --example .claude/settings.json.example
  --enable`, run on the 3.11 interpreter dev-setup hands over). The installed
  PreToolUse command is then run through bash with a JSON `Agent` call on
  stdin:

  ```text
  hooks --enable -> 0 on
  installed hook commands: ['python "${CLAUDE_PROJECT_DIR}/scripts/coordinator_guard.py" hook']
  3.11 first (this PATH)   exit=0 decision=deny
  C:\Python38 first        exit=1 decision=none (allowed) stderr=["ModuleNotFoundError: No module named 'tomllib'"]
  ```

  This repo's own committed `.claude/settings.json` fails the same way: its
  eight commands are all `python "${CLAUDE_PROJECT_DIR}/project-trajectory/scripts/coordinator_guard.py" hook`,
  and with `C:\Python38` first that command exits 1 with
  `ModuleNotFoundError: No module named 'tomllib'`. A failing PreToolUse hook
  does not block, so the window's denial fails open.
- **Class (the 012 F1 class):** the interpreter that runs kit Python is
  chosen by existence (`python` / `python3` on PATH, whichever comes first)
  instead of being the floor-resolved one. Round 4's brief scoped sites to
  those that launch the menu (the coordinator's error, as the coordinator
  noted). This plan lists every launch of a kit script by an interpreter word
  inside the lane's surface.
- **Sites, each with the search that found it:**
  - Search A: `git diff --name-only ed2533cb...HEAD -- . ':!docs/iteration' ':!docs/reviews' ':!docs/log.md' ':!docs/log.d' ':!PROJECT_STATE.html' ':!docs/open-items.html' ':!docs/stage'`
    (the lane's 63 files, saved as `review-tmp/2026-10-09-wi834r5/lane-files.txt`),
    then grep each non-test file for
    `(^|[^A-Za-z_.])(python3?|py)( -3(\.[0-9]+)?)?( -X utf8)? +[^ ]*\.py\b`.
  - Search B: `grep -n -E "\[\"python3?\"|'python3?'|\"python3? |sys\.executable"`
    over the lane's changed Python modules.
  - (a) IN THE CLASS, the shipped hook config:
    `project-trajectory/agent-hooks/claude.settings.json` :8 :19 :39 :50 :61
    :80 :91 :102, eight `python "${CLAUDE_PROJECT_DIR}/scripts/coordinator_guard.py" hook`
    commands added by this lane (search A). Also in the class but present at
    base and never merged by the opt-in (which takes only the guard's
    groups): :31 `python scripts/subagent_gate.py` and :72
    `python scripts/gen_arch_map.py --check && python scripts/trace.py --strict-integrity`.
    These are observed only.
  - (b) IN THE CLASS, the opt-in that installs them:
    `coordinator_guard.py` `enable_hooks` (:1424, `hooks --enable`) copies the
    example's command strings verbatim into `.claude/settings.json` (search
    B's caller, and the probe). It runs on dev-setup's floor-resolved
    interpreter (`KitReading` / `$PYBIN`), so it knows the right interpreter
    (`sys.executable`) and drops it.
  - (c) IN THE CLASS, this repo's `.claude/settings.json`: eight bare `python`
    guard hooks, committed by WI-822 (8868537c). The file is not in the
    lane's diff, but the lane's blackout behaviour runs through it.
  - (d) IN THE CLASS, the relaunch launchers (this repo's own, not shipped,
    D-001; changed by this lane):
    - `scripts/coordinator-relaunch.cmd:15` `python "...coordinator_guard.py" --root "%~1" window-check`
      (this lane's line) and `:17` `python "...coordinator_guard.py" exec-claude`
      (WI-822's);
    - `scripts/coordinator-relaunch.sh:22` `python3 ".../coordinator_guard.py" --root "$1" window-check`
      (this lane's).
    
    With a sub-floor first `python`, `window-check` crashes and `|| exit` ends
    the relaunch even outside the window: it fails closed, but every relaunch
    breaks. Their spawner `coordinator_guard.launch_command` (:1302) runs on a
    floor interpreter.
  - (e) IN THE CLASS, this repo's actions-menu lines: `docs/stack.ini` `[run]`
    (:1253-1259, added by this lane, D44): `smoke`, `trajectory`, `docs`,
    `dashboard` all start with bare `python`. The menu now runs on the
    resolved interpreter, but each shell line re-resolves `python` by PATH, so
    `run trajectory` with `C:\Python38` first dies on tomllib. The shipped
    `stack.ini.template` `[run]` declares no lines (nothing shipped is in the
    class).
  - (f) IN THE CLASS (instruction text, not a launch): `coordinator_guard.py:175`
    `GUARD = "python project-trajectory/scripts/coordinator_guard.py"`, the
    command the close-down and drain instructions tell the session to run
    (`request-relaunch`, `release`). The session types it, so its `python` is
    PATH's. The hook that builds the text runs on a floor interpreter.
  - Not in the class (floor-resolved already): dev-setup's readers
    (`$pybin` / `$PYBIN`, the handed interpreter in run mode), the run
    launchers (round 4), and the Python modules' own subprocesses
    (`agent_common` :414 :527 :1893 use the resolved interpreter or
    `sys.executable`).
  - Observed, outside the lane's diff and the spec's surface, not changed:
    the shipped git pre-commit hook `project-trajectory/hooks/pre-commit:129-139`
    probes `.venv` then `python3` / `python` by runnability only (`-c ""`, no
    3.11 floor); `agent-resume.*` and `check.sh` already floor-probe (WI-475);
    the skills' prose `python ...` lines (`session-protocol/SKILL.md:193`)
    are instructions, not launches.
- **Owning boundary (owner ruling D-019).** The interpreter is known,
  floor-checked, at each site's spawner, and the binding is made there:
  - (a)/(b) `enable_hooks`, run by dev-setup's consented step on the
    floor-resolved interpreter, writes the guard's hook groups into the
    machine-local `.claude/settings.local.json`, never the committed
    `.claude/settings.json`. Each command names `sys.executable` (the
    interpreter the opt-in runs on), quoted for a path with spaces, in place
    of the example's leading `python`. It merges with hooks already there, a
    re-run is idempotent, and a denial changes nothing. The shipped example
    stays inert and portable. `hooks_state` reads the same file. The
    scaffold's `.gitignore` (`gitignore.template`, which does not cover it
    today) gains `.claude/settings.local.json`. D-019 supersedes D-001's
    target file.
  - (d) `coordinator-relaunch.cmd` / `.sh` resolve their interpreter with the
    run launchers' floor probe (`sys.executable` printed only at 3.11+) over
    the same candidates as root `run.cmd` / `run.sh`. The parity test
    (TC-342) gains the two pairs: relaunch.cmd with `scripts/dev-setup.ps1`,
    relaunch.sh with `scripts/dev-setup.sh`. With none found they exit 1
    naming what was checked; no bare `python` / `python3` is left.
  - (f) `GUARD` names the interpreter the hook itself runs on
    (`sys.executable`, quoted).
  - Out of this row's scope, under the owner's ruling, filed as D-019's
    follow-up row (the kit-wide interpreter leftovers, cited by subject until
    it has an id): (c) this repo's committed `.claude/settings.json` hooks,
    (e) the `docs/stack.ini` `[run]` lines' bare `python`, and the shipped git
    pre-commit hook's interpreter choice. Not changed here. If a test needs
    (c) to change, the build stops and reports.
- **Pins (red first):**
  - (a)/(b) real interpreters only: a scaffold's installed PreToolUse hook,
    written by the real opt-in into `.claude/settings.local.json`, run
    through bash with the real `C:\Python38` first on PATH, still denies
    inside an armed window (skipped where no sub-floor interpreter is
    installed). The portable pin on every host: the command written into
    `settings.local.json` names `sys.executable`; `.claude/settings.json` is
    not created; a re-run is idempotent; the scaffold's `.gitignore` ignores
    the file. TC-345.
  - (d) the parity test over the relaunch pairs; the Windows relaunch e2e
    runs its guard step on the resolved interpreter. TC-342, TC-340.
  - (f) the injected command text names `sys.executable`. TC-340.
- D10 is covered twice on purpose: R1 is the hook's reading of a launch, R2
  (d) the relaunch launchers' `window-check`.

## R3 (regression bar)

- **Sites:** `tests/test_blackout_window.py` (TC-339 QUOTED_DENIED /
  QUOTED_ALLOWED, TC-340), `tests/test_run_devsetup.py` (TC-342, TC-343,
  TC-345 hooks), `tests/test_coordinator_guard.py` and
  `tests/test_coordinator_guard_e2e.py` (TC-317, TC-318 relaunch), and the
  smoke tier.
- **Search:** `git grep -ln "launch_command\|enable_hooks\|command_words\|QUOTED_DENIED" tests/`.
- **Owning boundary:** unchanged; re-run.

## Exclusions

Excludes: TC-266; TC-267; TC-268; TC-303; TC-315; TC-316; TC-321; TC-322; TC-323; TC-324; TC-329; TC-330; TC-341 — the retention, keep-warm, sign-in and adjudication paths are untouched by this round (F1 is the hook's shell reading, F2 the interpreter that runs kit Python); they run in their tiers unchanged.
Excludes: D44 — this repository's actions-menu `[run]` lines' bare `python` (F2 site e) is out of round 5's scope by the owner's ruling D-019 and goes to its follow-up row (the kit-wide interpreter leftovers: the `[run]` lines, this repository's committed `.claude/settings.json` hooks and the shipped git pre-commit hook), cited by subject until that row has an id.
Excludes: D1; D2; D3; D4; D5; D6; D8; D9; D11; D12; D13; D15; D16; D17; D18; D19; D20; D21; D22; D23; D24; D26; D27; D28; D29; D30; D31; D32; D33; D34; D35; D36; D37; D38; D39; D40; D41; D42; D45; D46; D47; D48; D49; D50; D52; D53; D54; D55; D56; D57; D58; D59; D60; D61; D62; D63; D64; D65; D66; D67; D68 — built in the lane's earlier rounds (through round 4's checkpoint and sitting 015, rebased onto ed2533cb) and not reopened by round 016; this round reopens only the hooks' reading (D7/D10/D25, F1), the hook opt-in and its test (D43/D51, F2), and the relaunch launch path (D10/D14, F2 site d).
