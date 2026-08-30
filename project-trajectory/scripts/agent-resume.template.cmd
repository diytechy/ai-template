@echo off
setlocal
REM Agent-resume launcher (Windows) - double-click to boot the right agent
REM session at the right tier, or the unattended coordinator loop, from the
REM repo root (process-options.md "Unattended operation (walk-away runs)").
REM The booted session inherits the whole committed context - AGENTS.md,
REM docs/status.md, docs/stage + docs/process.toml - so resuming work
REM never requires recalling an incantation. Read it first; it only exports
REM the slots below and runs scripts/agent_loop.py.
REM
REM CONSENT: the unattended loop runs the agent CLI headless; a permission-
REM bypass flag in AGENT_CMD means sessions edit without prompts. You consent
REM by filling the slot, declaring docs/process.toml, and running this.
REM No agent-driven work in this repo? Delete the agent-resume.* launchers.

REM --- EDIT FOR YOUR PROJECT ---------------------------------------------------
REM The agent command template; {model} and {prompt} are substituted per
REM session. NO {prompt} = the prompt is piped to the CLI's STDIN - immune to
REM the OS command-line caps (Windows: 8191 chars under cmd.exe .CMD shims,
REM ~32767 via CreateProcess). A Windows .cmd/.bat shim with {prompt} is refused
REM because cmd.exe can reparse prompt metacharacters even with shell=False; use
REM stdin or a native executable. Example:
REM   set "AGENT_CMD=claude -p --model {model} --output-format json --dangerously-skip-permissions"
REM Keep agent-resume.sh's slots in sync - it is the POSIX twin;
REM agent-resume.command delegates to it.
set "AGENT_CMD="
REM Default model tier + optional per-phase map keyed on the in-process phase.
REM The plan/build cadence (process-options.md "Unattended operation") wires
REM strong-model-plans / cheaper-model-executes here, e.g.:
REM   set "AGENT_MODEL_MAP=PLAN=<strong-model>,BUILD=<cheap-model>"
set "AGENT_MODEL="
set "AGENT_MODEL_MAP="
REM Optional per-phase preference WITHIN the resolved routing tier, e.g.:
REM   set "AGENT_PREFER_MAP=BUILD=OPENAI-SOL"
REM Unknown/cooling ids fall through to docs/agents-enabled order.
set "AGENT_PREFER_MAP="
REM Optional per-phase COMMAND template map (cross-provider routing; pairs
REM with the the process.toml reviewer dial reviewer dial - cross-provider dual review
REM is the recommended review-policy 2 config), e.g.:
REM   set "AGENT_CMD_MAP=REVIEW-B=gemini -p {prompt} --model {model}"
set "AGENT_CMD_MAP="
REM Optional hands-on template for --interactive (defaults to AGENT_CMD):
set "AGENT_CMD_INTERACTIVE="
REM Parallel work runs through the integration seam (process-options.md
REM "Parallel work - the integration seam"): claim with `integrate.py claim`,
REM build worker sessions on the claimed branches (this launcher: --wi in the
REM branch's worktree), merge through `integrate.py integrate`. (The
REM AGENT_JOBS dispatcher ceiling retired with the parallel dispatcher at
REM concurrency-restructure Phase 5.)
REM Single-home option (IF-068): to avoid editing model/model-map in each of
REM the three launchers, declare them once in docs\stack.ini [agent-loop] and
REM keep AGENT_MODEL / AGENT_MODEL_MAP blank - agent_loop resolves CLI flag ^>
REM AGENT_* env ^> that file ^> default.
REM Per-session wall-clock bound (seconds) so one hung CLI cannot wedge a
REM lane forever - the walk-away guarantee. Blank the slot to disable
REM (engine default 0 = no timeout). Keep agent-resume.sh in sync.
if not defined AGENT_SESSION_TIMEOUT set "AGENT_SESSION_TIMEOUT=7200"
REM Per-session IDLE bound (seconds): a child that stops emitting output is
REM killed this long after its last line, instead of being discovered at the
REM wall deadline above (C3, the stall-guard plan). Blank the slot to fall
REM through to the engine default (900); 0 disables the idle kill entirely.
REM Keep agent-resume.sh in sync.
if not defined AGENT_SESSION_IDLE_TIMEOUT set "AGENT_SESSION_IDLE_TIMEOUT=900"
REM ----------------------------------------------------------------------------

cd /d "%~dp0"
if not defined AGENT_CMD (
  echo agent-resume.cmd: no agent command wired yet.
  echo Edit AGENT_CMD in this file - see the EDIT FOR YOUR PROJECT block - and
  echo in agent-resume.sh. Filling it ^(and declaring docs/process.toml^) is your
  echo consent to unattended agent sessions; see docs/process-options.md
  echo "Unattended operation".
  pause
  exit /b 1
)
REM Pick the interpreter that can actually RUN the engine, in preference order:
REM this repo's OWN .venv first (the pinned 3.11+ toolchain scripts\setup.ps1
REM builds), then `python` on PATH, then `py -3`. Every candidate is probed by
REM RUNNING it - twice, because "found" and "usable" are two different questions:
REM   1. `-c "pass"` - does it run at all? On a bare Windows box `where python`
REM      matches the Microsoft-Store app-execution alias, a stub that opens the
REM      Store instead of running (the hooks' pattern).
REM   2. sys.version_info - the engine and every kit script import tomllib, so
REM      anything below the kit's 3.11 floor is a broken boot, not a find. An
REM      adopter targeting an older runtime lowers this WITH scripts/setup.*.
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
  echo Build the project environment ^(scripts\setup.ps1^) or install
  echo Python 3.11+ and re-run.
  pause
  exit /b 1
)
if defined AGENT_SESSION_TIMEOUT (
  set "TIMEOUT_ARGS=--session-timeout %AGENT_SESSION_TIMEOUT%"
) else (
  set "TIMEOUT_ARGS="
)
if defined AGENT_SESSION_IDLE_TIMEOUT (
  set "TIMEOUT_ARGS=%TIMEOUT_ARGS% --session-idle-timeout %AGENT_SESSION_IDLE_TIMEOUT%"
)
call %PY% scripts\agent_loop.py %TIMEOUT_ARGS% %*
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
