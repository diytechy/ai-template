@echo off
setlocal
REM Agent-resume launcher (Windows) - double-click to boot the right agent
REM session at the right tier, or the unattended coordinator loop, from the
REM repo root (project-trajectory/PROCESS_OPTIONS.md "Unattended operation
REM (walk-away runs)"). This is the kit's own launcher applied to the kit
REM repo itself: the booted session inherits the committed context -
REM CLAUDE.md, AGENTS.md, docs/status.md, the docs/work/ registry,
REM docs/log.md, docs/process.toml (the live working surfaces;
REM IMPROVEMENT_PLAN.md is archived history, not a working surface). Read it
REM first; it only exports the slots below and runs the coordinator engine.
REM
REM CONSENT: the unattended loop runs the agent CLI headless; the permission-
REM bypass flag in AGENT_CMD means sessions edit without prompts. You consent
REM by keeping the slot filled, declaring docs/process.toml, and running this.

REM --- EDIT FOR YOUR PROJECT ---------------------------------------------------
REM The agent command template; {model} and {prompt} are substituted per
REM session. NO {prompt} = the prompt is piped to the CLI's STDIN (WI-216) -
REM immune to OS command-line caps and Windows batch-shell re-parsing. A .cmd/.bat
REM shim with {prompt} is refused even with shell=False; use stdin or a native
REM executable.
REM Keep agent-resume.sh's slots in sync - it is the POSIX twin;
REM agent-resume.command delegates to it.
REM stream-json + --verbose (WI-125): the CLI emits an event line per turn, so
REM the coordinator console shows live progress instead of 30 silent minutes;
REM the final result event carries the same telemetry the json format did.
set "AGENT_CMD=claude -p --model {model} --output-format stream-json --verbose --dangerously-skip-permissions"
REM Default model tier + per-phase fallback map (used when managed routing is
REM off). WI-274: the VALUES now live ONCE in docs/stack.ini [agent-loop] (model
REM / model-map) - agent_loop reads them there, so a dial change edits one file,
REM not this value in three launchers. These slots stay the env-override tier
REM (precedence: CLI flag ^> this env slot ^> docs/stack.ini ^> built-in
REM default); left empty so the declared home wins. Owner dial 2026-07-22 (Opus
REM at both strong and medium) lives in stack.ini now.
set "AGENT_MODEL="
set "AGENT_MODEL_MAP="
REM Per-phase ROUTING tier for the docs/agents.csv router (strong|medium|quick).
REM Empty = the engine's built-in defaults (PLAN / DESIGN-CHECK / CRITIQUE
REM strong, BUILD / REVIEW-A / REVIEW-B medium; a worker still pins BUILD up
REM to its WI row's BuildTier). EMPTY per the owner directive 2026-07-19:
REM builds are Anthropic-led per tier again - Fable takes strong-row BUILDs,
REM Opus takes medium - retiring the WI-160 Sol pin (2026-07-14b; that
REM directive stands in history if this one is reverted). Keep agent-resume.sh
REM in sync. tier-up-never-down unchanged.
set "AGENT_TIER_MAP="
REM Optional within-tier preference per phase. Unknown, disabled, wrong-tier,
REM or cooling ids fall through to docs/agents-enabled order; this never changes
REM the resolved tier. Empty since 2026-07-19: docs/agents-enabled order already
REM leads each tier with the ANTHROPIC row. Keep agent-resume.sh in sync.
set "AGENT_PREFER_MAP="
REM Optional per-phase COMMAND template map (cross-provider routing; pairs
REM with the the process.toml reviewer dial reviewer dial), e.g.:
REM   set "AGENT_CMD_MAP=REVIEW-B=gemini -p {prompt} --model {model}"
REM Empty here: under managed routing each enabled row's own CmdTemplate drives
REM its launch (docs/agents.csv spans THREE families - ANTHROPIC/claude,
REM OPENAI/codex, OPENCODE/opencode-go - all listed in docs/agents-enabled),
REM so this per-phase override map has nothing to add; AGENT_CMD stays the
REM legacy-path fallback. (Header corrected 2026-07-21 - it wrongly claimed
REM single-provider since WI-160.)
set "AGENT_CMD_MAP="
REM Optional hands-on template for --interactive (defaults to AGENT_CMD):
set "AGENT_CMD_INTERACTIVE=claude --model {model} {prompt}"
REM (The AGENT_JOBS worker-ceiling slot retired with the parallel dispatcher
REM at concurrency-restructure Phase 5: claiming and merging run through
REM integrate.py, and this launcher boots explicit session roles only --
REM agent_loop.py --wi / --interactive / --dual-plan.)
REM (The meta-repo resume prompt slot is retired with the serial driver,
REM WI-210: worker sessions build their explicit assignments - the repo
REM rules live in CLAUDE.md and the session-protocol skill, which every
REM session already reads.)
REM Per-session wall-clock bound (seconds) so one hung CLI cannot wedge a
REM lane forever - the walk-away guarantee (repo-review 2026-07-21 M-18).
REM Blank the slot to disable (engine default 0 = no timeout). Keep
REM agent-resume.sh in sync.
if not defined AGENT_SESSION_TIMEOUT set "AGENT_SESSION_TIMEOUT=7200"
REM ----------------------------------------------------------------------------

cd /d "%~dp0"
if not defined AGENT_CMD (
  echo agent-resume.cmd: no agent command wired yet.
  echo Edit AGENT_CMD in this file - see the EDIT FOR YOUR PROJECT block - and
  echo in agent-resume.sh. Filling it ^(and declaring docs/process.toml^) is your
  echo consent to unattended agent sessions; see
  echo project-trajectory/PROCESS_OPTIONS.md "Unattended operation".
  pause
  exit /b 1
)
REM Pick the interpreter that can actually RUN the engine, in preference order:
REM this repo's OWN .venv first (the pinned 3.11+ toolchain scripts\dev-setup.cmd
REM builds), then `python` on PATH, then `py -3`. Every candidate is probed by
REM RUNNING it - twice, because "found" and "usable" are two different questions
REM (repo-review 2026-08-19 H-01, which caught this launcher booting an ambient
REM 3.8 while a 3.11.9 .venv sat unused, dying at `import tomllib`):
REM   1. `-c "pass"` - does it run at all? On a bare Windows box `where python`
REM      matches the Microsoft-Store app-execution alias, a stub that opens the
REM      Store instead of running (repo-review 2026-07-21 M-16).
REM   2. sys.version_info - the engine and every kit script import tomllib, so
REM      anything below 3.11 is a broken boot, not a find.
REM `call` is load-bearing: without it cmd hands control to a .cmd/.bat shim
REM python (pyenv-win ships exactly that) and never returns to this file.
set "PY="
set "PYWHY="
if exist ".venv\Scripts\python.exe" call :pickpy ".venv\Scripts\python.exe"
if exist ".venv\bin\python" call :pickpy ".venv\bin\python"
call :pickpy "python"
call :pickpy "py -3"
if not defined PY (
  echo agent-resume.cmd: no Python 3.11+ interpreter found.
  echo Rejected:%PYWHY%
  echo Build the project environment ^(scripts\dev-setup.cmd^) or install
  echo Python 3.11+ and re-run.
  pause
  exit /b 1
)
if defined AGENT_SESSION_TIMEOUT (
  set "TIMEOUT_ARGS=--session-timeout %AGENT_SESSION_TIMEOUT%"
) else (
  set "TIMEOUT_ARGS="
)
REM --root . : in this repo the engine lives under project-trajectory\scripts\,
REM so its script-relative default would resolve to the kit dir, not the repo.
REM Explicit flags come first so anything you pass on the command line wins.
call %PY% project-trajectory\scripts\agent_loop.py --root . %TIMEOUT_ARGS% %*
set "EXITCODE=%ERRORLEVEL%"
echo.
echo Exited with code %EXITCODE%.
pause
exit /b %EXITCODE%

REM --- interpreter probe (called above; unreachable by fall-through) -----------
:pickpy
REM Probe ONE candidate (%~1, which may carry a flag like `py -3`) and record why
REM it lost; the first candidate that answers Python 3.11+ wins and later ones
REM are skipped. The rejection list is what the diagnostic above prints.
if defined PY goto :eof
call %~1 -c "pass" >nul 2>nul
if errorlevel 1 (
  set "PYWHY=%PYWHY% [%~1: not runnable here]"
  goto :eof
)
call %~1 -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)" >nul 2>nul
if errorlevel 1 (
  set "PYWHY=%PYWHY% [%~1: older than Python 3.11]"
  goto :eof
)
set "PY=%~1"
goto :eof
