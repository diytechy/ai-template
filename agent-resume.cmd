@echo off
setlocal
REM Agent-resume launcher (Windows) — double-click to boot the right agent
REM session at the right tier, or the unattended coordinator loop, from the
REM repo root (project-trajectory/PROCESS_OPTIONS.md "Unattended operation
REM (walk-away runs)"). This is the kit's own launcher applied to the kit
REM repo itself: the booted session inherits the committed context —
REM CLAUDE.md, AGENTS.md, IMPROVEMENT_PLAN.md, docs/status.md,
REM docs/gate-policy + run-state. Read it first; it only exports the slots
REM below and runs the coordinator engine.
REM
REM CONSENT: the unattended loop runs the agent CLI headless; the permission-
REM bypass flag in AGENT_CMD means sessions edit without prompts. You consent
REM by keeping the slot filled, declaring docs/gate-policy, and running this.

REM --- EDIT FOR YOUR PROJECT ---------------------------------------------------
REM The agent command template; {model} and {prompt} are substituted per
REM session (no {prompt} = the resume prompt is appended).
REM Keep agent-resume.sh's slots in sync — it is the POSIX twin;
REM agent-resume.command delegates to it.
set "AGENT_CMD=claude -p {prompt} --model {model} --output-format json --dangerously-skip-permissions"
REM Default model tier + optional per-phase map read against docs/run-phase.
REM Kit work is gate-bearing template design — default to the strong tier.
set "AGENT_MODEL=opus"
set "AGENT_MODEL_MAP="
REM Optional hands-on template for --interactive (defaults to AGENT_CMD):
set "AGENT_CMD_INTERACTIVE=claude --model {model} {prompt}"
REM Meta-repo resume prompt: the engine's default prompt assumes a scaffolded
REM downstream repo (docs/process.md etc.); this one names THIS repo's actual
REM surfaces. Empty = fall back to the engine default. Keep agent-resume.sh's
REM copy in sync.
set "AGENT_PROMPT=You are the driver session for the ai-template META-repo - the kit source, self-applied. Read CLAUDE.md, then docs/status.md Current State. The process masters are project-trajectory/PROCESS.md and PROCESS_OPTIONS.md 'Unattended operation'; no scaffolded docs/process.md exists here. Work only scope recorded in IMPROVEMENT_PLAN.md - a thread or a WI-1.x entry - per the session-protocol skill; new scope needs a WI entry first. Gates before every commit: python -m pytest -q and python project-trajectory/scripts/check_docs.py --root . - paste the real output; never report a green you didn't produce. Honor docs/push-policy - human: never push, even if asked. Before stopping: commit progress; update docs/status.md resume point + open items and the plan's WI log; write docs/run-state - RUNNING while work remains, DONE only at the declared end state, BLOCKED when everything remaining is blocked, NEEDS-HUMAN when the next step needs a human act, stating the ask as a 'Needs <human>' Open item in status.md first."
REM ----------------------------------------------------------------------------

cd /d "%~dp0"
if not defined AGENT_CMD (
  echo agent-resume.cmd: no agent command wired yet.
  echo Edit AGENT_CMD in this file — see the EDIT FOR YOUR PROJECT block — and
  echo in agent-resume.sh. Filling it ^(and declaring docs/gate-policy^) is your
  echo consent to unattended agent sessions; see
  echo project-trajectory/PROCESS_OPTIONS.md "Unattended operation".
  pause
  exit /b 1
)
where python >nul 2>nul
if errorlevel 1 ( set "PY=py -3" ) else ( set "PY=python" )
REM --root . : in this repo the engine lives under project-trajectory\scripts\,
REM so its script-relative default would resolve to the kit dir, not the repo.
REM Explicit flags come first so anything you pass on the command line wins.
if defined AGENT_PROMPT (
  %PY% project-trajectory\scripts\agent_loop.py --root . --prompt "%AGENT_PROMPT%" %*
) else (
  %PY% project-trajectory\scripts\agent_loop.py --root . %*
)
set "EXITCODE=%ERRORLEVEL%"
echo.
echo Exited with code %EXITCODE%.
pause
exit /b %EXITCODE%
