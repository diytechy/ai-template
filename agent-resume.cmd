@echo off
setlocal
REM Agent-resume launcher (Windows) — double-click to boot the right agent
REM session at the right tier, or the unattended coordinator loop, from the
REM repo root (project-trajectory/PROCESS_OPTIONS.md "Unattended operation
REM (walk-away runs)"). This is the kit's own launcher applied to the kit
REM repo itself: the booted session inherits the committed context —
REM CLAUDE.md, AGENTS.md, docs/status.md, docs/requirements/work-items.csv,
REM docs/log.md, docs/gate-policy + run-state (the live working surfaces;
REM IMPROVEMENT_PLAN.md is archived history, not a working surface). Read it
REM first; it only exports the slots below and runs the coordinator engine.
REM
REM CONSENT: the unattended loop runs the agent CLI headless; the permission-
REM bypass flag in AGENT_CMD means sessions edit without prompts. You consent
REM by keeping the slot filled, declaring docs/gate-policy, and running this.

REM --- EDIT FOR YOUR PROJECT ---------------------------------------------------
REM The agent command template; {model} and {prompt} are substituted per
REM session (no {prompt} = the resume prompt is appended).
REM Keep agent-resume.sh's slots in sync — it is the POSIX twin;
REM agent-resume.command delegates to it.
REM stream-json + --verbose (WI-125): the CLI emits an event line per turn, so
REM the coordinator console shows live progress instead of 30 silent minutes;
REM the final result event carries the same telemetry the json format did.
set "AGENT_CMD=claude -p {prompt} --model {model} --output-format stream-json --verbose --dangerously-skip-permissions"
REM Default model tier + per-phase map keyed on the in-process phase (the default
REM model stays strong — an unknown phase routes UP, never down). With managed
REM routing ON (docs/agents-enabled present) the docs/agents.csv registry +
REM AGENT_TIER_MAP below drive selection; these env maps are the declared
REM FALLBACK (an absent enable-list = this legacy path). Values kept coherent
REM with the owner dial 2026-07-12 evening (WI-121): strong (fable) plans,
REM medium (opus) builds + reviews.
set "AGENT_MODEL=claude-fable-5"
set "AGENT_MODEL_MAP=PLAN=claude-fable-5,BUILD=opus,REVIEW-A=opus,REVIEW-B=opus,DESIGN-CHECK=claude-fable-5,CRITIQUE=claude-fable-5"
REM Per-phase ROUTING tier for the docs/agents.csv router (strong|medium|quick).
REM Empty = the engine's built-in defaults (PLAN / DESIGN-CHECK / CRITIQUE
REM strong, BUILD / REVIEW-A / REVIEW-B medium). BUILD=strong per the owner
REM directive 2026-07-14b (WI-160): builds prefer Codex Sol - strong tier +
REM OPENAI-SOL first in docs/agents-enabled - superseding FOR NOW the WI-121
REM medium relax (that history stands if this directive is reverted). Keep
REM agent-resume.sh in sync. tier-up-never-down unchanged.
set "AGENT_TIER_MAP=BUILD=strong"
REM Optional within-tier preference per phase. Unknown, disabled, wrong-tier,
REM or cooling ids fall through to docs/agents-enabled order; this never changes
REM the resolved tier. Keep agent-resume.sh in sync.
set "AGENT_PREFER_MAP=BUILD=OPENAI-SOL"
REM Optional per-phase COMMAND template map (cross-provider routing; pairs
REM with the docs/review-policy reviewer dial), e.g.:
REM   set "AGENT_CMD_MAP=REVIEW-B=gemini -p {prompt} --model {model}"
REM Empty here: single-provider (every docs/agents.csv row is Family=ANTHROPIC),
REM so every phase uses AGENT_CMD; add a row + entry when a cross-provider CLI exists.
set "AGENT_CMD_MAP="
REM Optional hands-on template for --interactive (defaults to AGENT_CMD):
set "AGENT_CMD_INTERACTIVE=claude --model {model} {prompt}"
REM This repo has completed the dispatcher migration audits in
REM docs/parallel-ready, so normal launches use the two-worker dispatcher.
REM Pass --jobs 1 for a serial dispatcher run; an absent slot also boots the
REM dispatcher (WI-210 - the legacy serial driver is retired).
set "AGENT_JOBS=2"
REM (The meta-repo resume prompt slot is retired with the serial driver,
REM WI-210: a plain launch is the dispatcher, and worker sessions build
REM their explicit assignments - the repo rules live in CLAUDE.md and the
REM session-protocol skill, which every session already reads.)
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
%PY% project-trajectory\scripts\agent_loop.py --root . %*
set "EXITCODE=%ERRORLEVEL%"
echo.
echo Exited with code %EXITCODE%.
pause
exit /b %EXITCODE%
