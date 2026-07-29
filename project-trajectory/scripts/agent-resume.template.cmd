@echo off
setlocal
REM Agent-resume launcher (Windows) - double-click to boot the right agent
REM session at the right tier, or the unattended coordinator loop, from the
REM repo root (process-options.md "Unattended operation (walk-away runs)").
REM The booted session inherits the whole committed context - AGENTS.md,
REM docs/status.md, docs/gate + gate-policy - so resuming work
REM never requires recalling an incantation. Read it first; it only exports
REM the slots below and runs scripts/agent_loop.py.
REM
REM CONSENT: the unattended loop runs the agent CLI headless; a permission-
REM bypass flag in AGENT_CMD means sessions edit without prompts. You consent
REM by filling the slot, declaring docs/gate-policy, and running this.
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
REM with the docs/review-policy reviewer dial - cross-provider dual review
REM is the recommended review-policy 2 config), e.g.:
REM   set "AGENT_CMD_MAP=REVIEW-B=gemini -p {prompt} --model {model}"
set "AGENT_CMD_MAP="
REM Optional hands-on template for --interactive (defaults to AGENT_CMD):
set "AGENT_CMD_INTERACTIVE="
REM Parallel dispatch (process-options.md "Worker assignment"): a FRESH scaffold
REM ships parallel-by-default at two workers. The dispatcher still HOLDS at one
REM worker until this repo's soft-edge + SafetyClass audits pass (a fresh
REM scaffold passes by construction); a repo migrating in from the legacy loop
REM sets AGENT_JOBS=1 here until it signs off (the downstream-resync skill).
REM An inherited AGENT_JOBS wins over this default; an absent/empty value
REM still boots the dispatcher at its own default (the legacy serial resume
REM driver is retired).
REM Single-home option (IF-068): to avoid editing jobs/model/model-map in each
REM of the three launchers, declare them once in docs\stack.ini [agent-loop].
REM Keep AGENT_MODEL / AGENT_MODEL_MAP blank; for jobs, replace the next line
REM with `set "AGENT_JOBS="` (CMD deletes the variable). This exact Windows edit
REM leaves no launcher env override, so agent_loop resolves CLI flag ^> AGENT_*
REM env ^> that file ^> default. Opt-in: a fresh scaffold keeps its dials here.
if not defined AGENT_JOBS set "AGENT_JOBS=2"
REM Per-session wall-clock bound (seconds) so one hung CLI cannot wedge a
REM lane forever - the walk-away guarantee. Blank the slot to disable
REM (engine default 0 = no timeout). Keep agent-resume.sh in sync.
if not defined AGENT_SESSION_TIMEOUT set "AGENT_SESSION_TIMEOUT=7200"
REM ----------------------------------------------------------------------------

cd /d "%~dp0"
if not defined AGENT_CMD (
  echo agent-resume.cmd: no agent command wired yet.
  echo Edit AGENT_CMD in this file - see the EDIT FOR YOUR PROJECT block - and
  echo in agent-resume.sh. Filling it ^(and declaring docs/gate-policy^) is your
  echo consent to unattended agent sessions; see docs/process-options.md
  echo "Unattended operation".
  pause
  exit /b 1
)
REM Probe by RUNNING the candidate, not just finding it: on a bare Windows
REM box `where python` matches the Microsoft-Store app-execution alias, a
REM stub that opens the Store instead of running (the hooks' pattern).
set "PY="
python -c "" >nul 2>nul
if not errorlevel 1 set "PY=python"
if not defined PY (
  py -3 -c "" >nul 2>nul
  if not errorlevel 1 set "PY=py -3"
)
if not defined PY (
  echo agent-resume.cmd: Python 3 not found on PATH ^(the Store alias stub
  echo does not count^). Install Python 3 and re-run.
  pause
  exit /b 1
)
if defined AGENT_SESSION_TIMEOUT (
  set "TIMEOUT_ARGS=--session-timeout %AGENT_SESSION_TIMEOUT%"
) else (
  set "TIMEOUT_ARGS="
)
%PY% scripts\agent_loop.py %TIMEOUT_ARGS% %*
set "EXITCODE=%ERRORLEVEL%"
echo.
echo Exited with code %EXITCODE%.
pause
exit /b %EXITCODE%
