# WI-834 rework round 4: coverage plan

Answers `docs/reviews/wi-834/012-REVIEW-A-3b1d473.md` (F1: the one line
under its findings, the `[MAJOR] run.cmd:52` line; plan_coverage reads the
same one).

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| R1 | F1: each run launcher resolves one floor-satisfying interpreter by running it, hands that interpreter to the readiness operation, which checks only it, and runs the menu on exactly it; the direct and list forms use the same resolution and end with the step when none passes | F1; D28; D31; D32; D33; D39; D41; D44; D67; SR-046; SR-032; TC-342; TC-343 | IF-292; IF-293 | |
| R2 | The round's regression bar: the launcher and readiness pins, the scaffold readiness tests and the dogfood sync re-run, with the pins R1 changes; the item's blackout, retention and relaunch SRs re-run unchanged in the smoke bar | SR-227; SR-229; SR-230; TC-344; TC-345 | intra-module (no seam changes in this row) | R1 |

## R1 (F1)

- **Confirmed** on the real code path. Probe
  `C:/Projects/ai-template.wt/review-tmp/2026-10-09-wi834r4/f1-probe.py`
  (the real, installed `C:\Python38` prepended to a child PATH, `CI=true`, no
  fake executable), run against the lane at a6813ad4:

  ```text
  scripts\dev-setup.ps1 -ForRun -> exit 0
        [ok]      runtime (python)
  run.cmd (bare, "q" piped)     -> exit 1
        [ok]      runtime (python)
        import tomllib
    ModuleNotFoundError: No module named 'tomllib'
  run.cmd --list                -> exit 1
    ModuleNotFoundError: No module named 'tomllib'
  ```

  The readiness step's floor probe found a 3.11 through its own candidates,
  then `run.cmd`'s `:python` took `python` (3.8) because `python -c ""` merely
  ran. The direct form fails the same way: it has no floor check at all. On
  this box `py -3` also selects `C:\Python38\python.exe`.
- **Class:** the interpreter that runs the menu is not the interpreter whose
  3.11 floor the readiness step established: a launcher chooses an
  interpreter by existence or runnability (after, or instead of, a floor
  check), or the readiness step chooses its own.
- **Sites examined** (everything that launches `run_menu.py` or decides the
  runtime a bare run is ready on):
  - (a) IN THE CLASS: `run.cmd` and `project-trajectory/scripts/run.template.cmd`,
    `:python` (`python -c ""` else `py -3`, else falls through to `py -3`):
    a runnability-only choice used by both the bare path (after
    `dev-setup.ps1 -ForRun`) and the direct path (`run.cmd <name>`,
    `run.cmd --list`, no floor check at all).
  - (b) IN THE CLASS: `run.sh` and `project-trajectory/scripts/run.template.sh`,
    `PY="$(command -v python3 || command -v python)"`: an existence-only choice
    on the bare path (after `dev-setup.sh --for-run`) and the direct path.
  - (c) IN THE CLASS (the readiness side): `project-trajectory/scripts/dev-setup.template.ps1`
    `FindPython` (`py`, `python`, `python3`, each floor-probed) and its re-call
    at the run tier's result (`if (FindPython) { exit 0 }`);
    `project-trajectory/scripts/dev-setup.template.sh` `detect_runtime`
    (`python3`, `python`) and its re-call at the run tier's result;
    `scripts/dev-setup.ps1` (`.venv\Scripts\python.exe`, then `py`, `python`,
    `python3`, `py -3.13`, `py -3.12`, `py -3.11`) and
    `scripts/dev-setup.sh` `discover_py` (`.venv/bin/python`, `python3`,
    `python`, `python3.13..3.11`, re-run after the runtime offer). Each
    chooses its own interpreter, so its `exit 0` speaks for an interpreter the
    launcher never runs. Removing the launcher's choice alone does not end the
    class while the readiness step keeps a second one.
  - `run.command` and `project-trajectory/scripts/run.template.command`:
    `exec ./run.sh "$@"`, no choice of their own; the class ends there by
    delegation (pinned by the run.command case of the bare-run test).
  - `scripts/dev-setup.cmd`, `scripts/dev-setup.command` and their templates:
    pass arguments to dev-setup or run `--check`/`--baseline`/`--install`;
    they never launch the menu and never run the readiness operation. Not in
    the class.
  - Observed, outside this row's surface, not changed: `agent-resume.{cmd,sh}`
    and their templates (`:pickpy` / `pick_py`, already floor-probed by
    running, WI-475), `project-trajectory/scripts/check.sh` `pick_py`, the
    git hooks, and `coordinator-relaunch.*`. None launches `run_menu.py`.
    R1 shares no code with them (no owner outside the spec's surface is
    introduced).
  - (d) IN THE CLASS (found by the coordinator after the first R1 build): the
    run launchers' candidate lists were narrower than their dev-setup's own
    runtime search, which `--check`, `--baseline`/`-Install` and `--full` still
    use: `scripts/dev-setup.ps1` searches `py`, `python`, `python3`,
    `py -3.13`, `py -3.12`, `py -3.11` (WI-274c) and `scripts/dev-setup.sh`
    `python3`, `python`, `python3.13`, `python3.12`, `python3.11`;
    `dev-setup.template.ps1` `py`, `python`, `python3`;
    `dev-setup.template.sh` `python3`, `python`. With `C:\Python38` first on
    PATH and 3.11/3.12 reachable only through `py -3.1x`, the standalone check
    reported `[ok] runtime` while `run.cmd` (`.venv`, `python`, `py -3`)
    refused. Two sides again answered "is the runtime ready" from different
    interpreter sets.
- **Searches:**
  - `git grep -l "run_menu" -- ':!docs' ':!*.md' ':!*.html' ':!tests'` ->
    `run.{cmd,sh,command}`, `project-trajectory/scripts/run.template.{cmd,sh,command}`,
    `run_menu.py` itself, `bootstrap.py` and `kitlib/bootstrap_manifest.py`
    (scaffold copies only) and `stack.ini.template` (prose): the six launchers
    are the only processes that start the menu;
  - `git grep -n -E "command -v python3|py -3|python -c \"\"|FindPython|detect_runtime|discover_py|pick_?py" -- ':!docs' ':!*.md' ':!*.html' ':!tests'`
    -> the run launchers' two choices (a, b), the four dev-setup choices (c),
    and the agent-resume / check.sh probes (observed, out of scope);
  - `git grep -n -E "candidates|foreach \(\$cand|for cand in" -- scripts/dev-setup.ps1 scripts/dev-setup.sh project-trajectory/scripts/dev-setup.template.ps1 project-trajectory/scripts/dev-setup.template.sh`
    -> each dev-setup's runtime search (site d: `dev-setup.ps1:103-106`,
    `dev-setup.sh:153`, `dev-setup.template.ps1:144`,
    `dev-setup.template.sh:184`), plus the two ambient-interpreter debris
    probes (`dev-setup.ps1:211`, `dev-setup.sh:254`), which only warn about
    what a bare `python -m pytest` resolves and decide no runtime;
  - `git grep -n "ForRun\|for-run" -- ':!docs/archive'` -> the two root and two
    template readiness operations, the run launchers that call them, and
    `tests/test_run_devsetup.py`.
- **Owning boundary:** the launcher's one resolution. Each `run.*` launcher
  probes its candidates by RUNNING them (its `.venv` interpreter, then
  exactly its dev-setup's own runtime search, in the same order: root
  `run.cmd` = `scripts/dev-setup.ps1`, root `run.sh` = `scripts/dev-setup.sh`,
  `run.template.cmd` = `dev-setup.template.ps1`, `run.template.sh` =
  `dev-setup.template.sh`; each dev-setup's list now lives in one variable,
  `$PyCandidates` / `PY_CANDIDATES`, with no candidate added) with one probe that
  prints `sys.executable` only when `sys.version_info >= (3, 11)`; the first
  answer is the interpreter, as a concrete executable path (so a `py`
  launcher's shebang handling, D-008, cannot swap it afterwards). The bare
  path hands it to the readiness operation (`-ForRun -Python <path>` /
  `--for-run --python <path>`, omitted when none passed), whose run tier
  checks the floor of exactly that interpreter, runs the kit's readers on it,
  and keeps no candidate search of its own; its exit 0 then speaks for the
  interpreter the menu runs on. The direct and list forms use the same
  resolution and, when none passes, exit 1 with the step, without running the
  readiness operation, prompting or pausing. The launcher's existence-only
  choice and its `py -3` fall-through are deleted, not kept as a fallback.
  With none resolved, a bare run's readiness reports the runtime missing and
  offers what it offers; the run then ends with the step, which names what
  was checked and says to install Python 3.11+ or put an installed one first
  on PATH, then run again, because an interpreter installed during the run is not one the
  launcher resolved. Recorded as D-017.
- **Owner header and docstring:** the dev-setup templates' `IF-292` / `IF-293`
  contract bodies gain the handed interpreter; the run launchers' headers
  state the resolution. The row texts are the spine author's
  (`013-SPINE-CHANGES-r4.md`).
- **Pins (red first):**
  - `tests/test_run_devsetup.py`: a bare run (`run.sh`, `run.command`,
    `run.cmd`) hands the readiness operation the interpreter the menu then
    runs on (a menu stub prints `sys.executable`; the stub dev-setup records
    its arguments), and that interpreter passes the floor. Deterministic on
    every host: the host's own interpreter is the one resolved. Red on the
    lane: the launcher hands nothing.
  - the direct and list forms with only sub-floor candidates first on PATH
    exit 1 naming the 3.11 floor and never start the menu, using the WI-475
    version-spoofed fakes (`tests/test_launcher_interpreter.py`: the real
    interpreter with only `sys.version_info` spoofed, executing the
    launcher's own probe string), which the review threat model does not
    discount because nothing is faked but the version the probe asks for.
    Red on the lane: the menu runs under the fake.
  - the shipped readiness operation (`dev-setup.template.sh --for-run`,
    `dev-setup.template.ps1 -ForRun` on Windows) without a handed
    interpreter reports the runtime missing and exits 1 while a 3.11+ is on
    PATH, and with the host's interpreter handed exits 0. Red on the lane:
    it finds its own and exits 0.
  - site (d): `test_each_run_launcher_searches_what_its_dev_setup_searches`
    reads the launcher's list (`for %%C in (...)` / `for cand in ...`, after
    its `.venv` entries) and the dev-setup's (`$PyCandidates` /
    `PY_CANDIDATES`) from the files of each of the four pairs and asserts
    they are the same, in the same order, so the lists cannot drift. Red on
    the lane after the variable extraction and before widening the launchers
    (three pairs differ; `run.template.sh` already matched).

## R2 (regression bar)

- **Class:** none new; the other readiness and launcher readings must not
  move.
- **Sites:** `tests/test_run_devsetup.py` (TC-342, TC-343, TC-344, TC-345), the smoke tier (the SR-227, SR-229 and SR-230 pins, untouched by R1),
  `tests/test_launcher_interpreter.py` (the agent-resume and check probes,
  unchanged), `tests/test_onboard_devsetup.py` (run.cmd stays ASCII),
  `tests/test_bootstrap.py` (the launchers still delegate to `run_menu.py`),
  `tests/test_dogfood_sync.py`, `tests/test_seam_resolution.py` (the
  dev-setup `Contracts:` headers).
- **Search:** `git grep -ln "run\.template\|run\.cmd\|dev-setup" tests/`.
- **Owning boundary:** unchanged; re-run, no edit beyond the R1 pins.

## Exclusions

Excludes: TC-266; TC-267; TC-268; TC-303; TC-315; TC-316; TC-317; TC-318; TC-321; TC-322; TC-323; TC-324; TC-329; TC-330; TC-339; TC-340; TC-341 — the blackout, retention, guard and relaunch paths are untouched by this round (F1 is the run/readiness relationship only); they run in their tiers unchanged.
Excludes: D1; D2; D3; D4; D5; D6; D7; D8; D9; D10; D11; D12; D13; D14; D15; D16; D17; D18; D19; D20; D21; D22; D23; D24; D25; D26; D27; D29; D30; D34; D35; D36; D37; D38; D40; D42; D43; D45; D46; D47; D48; D49; D50; D51; D52; D53; D54; D55; D56; D57; D58; D59; D60; D61; D62; D63; D64; D65; D66; D68 — built in the lane's earlier rounds (785a004d, 9bc1eb2a, 8cb21762 and the adjudicated rounds through 3b1d4733) and not reopened by this round's REVIEW-A; this round reopens only F1 (the readiness result D28, the bare run D31/D39/D44, the direct and list forms D32/D41, the run-to-dev-setup seam D33, and the RESYNC line D67).
Excludes: F1 — spine text (LLR-047's and LLR-320's detail, IF-292's and IF-293's data, TC-342's and TC-343's method/expected/evidence): the spine author reconciles it at the lane's checkpoint (coordinator-cycle skill §3) from `docs/reviews/wi-834/013-SPINE-CHANGES-r4.md`; this builder does not touch the registries' text.
