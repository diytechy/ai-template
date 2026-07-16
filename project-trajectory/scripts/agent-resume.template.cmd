@echo off
setlocal
REM Agent-resume launcher (Windows) — double-click to boot the right agent
REM session at the right tier, or the unattended coordinator loop, from the
REM repo root (process-options.md "Unattended operation (walk-away runs)").
REM The booted session inherits the whole committed context — AGENTS.md,
REM docs/status.md, docs/gate + gate-policy + run-state — so resuming work
REM never requires recalling an incantation. Read it first; it only exports
REM the slots below and runs scripts/agent_loop.py.
REM
REM CONSENT: the unattended loop runs the agent CLI headless; a permission-
REM bypass flag in AGENT_CMD means sessions edit without prompts. You consent
REM by filling the slot, declaring docs/gate-policy, and running this.
REM No agent-driven work in this repo? Delete the agent-resume.* launchers.

REM --- EDIT FOR YOUR PROJECT ---------------------------------------------------
REM The agent command template; {model} and {prompt} are substituted per
REM session (no {prompt} = the resume prompt is appended). Example:
REM   set "AGENT_CMD=claude -p {prompt} --model {model} --output-format json --dangerously-skip-permissions"
REM Keep agent-resume.sh's slots in sync — it is the POSIX twin;
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
REM with the docs/review-policy reviewer dial — cross-provider dual review
REM is the recommended review-policy 2 config), e.g.:
REM   set "AGENT_CMD_MAP=REVIEW-B=gemini -p {prompt} --model {model}"
set "AGENT_CMD_MAP="
REM Optional hands-on template for --interactive (defaults to AGENT_CMD):
set "AGENT_CMD_INTERACTIVE="
REM ----------------------------------------------------------------------------

cd /d "%~dp0"
if not defined AGENT_CMD (
  echo agent-resume.cmd: no agent command wired yet.
  echo Edit AGENT_CMD in this file — see the EDIT FOR YOUR PROJECT block — and
  echo in agent-resume.sh. Filling it ^(and declaring docs/gate-policy^) is your
  echo consent to unattended agent sessions; see docs/process-options.md
  echo "Unattended operation".
  pause
  exit /b 1
)
where python >nul 2>nul
if errorlevel 1 ( set "PY=py -3" ) else ( set "PY=python" )
%PY% scripts\agent_loop.py %*
set "EXITCODE=%ERRORLEVEL%"
echo.
echo Exited with code %EXITCODE%.
pause
exit /b %EXITCODE%
