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
REM Pass --jobs 1 for a serial dispatcher run; an absent slot retains legacy.
set "AGENT_JOBS=2"
REM Meta-repo resume prompt: the engine's default prompt assumes a scaffolded
REM downstream repo (docs/process.md etc.); this one names THIS repo's actual
REM surfaces. Empty = fall back to the engine default. Keep agent-resume.sh's
REM copy in sync.
set "AGENT_PROMPT=You are the driver session for the ai-template META-repo - the kit source, self-applied. Read CLAUDE.md, then docs/status.md Current State. The process masters are project-trajectory/PROCESS.md and PROCESS_OPTIONS.md 'Unattended operation'; no scaffolded docs/process.md exists here. Work only scope recorded in docs/requirements/work-items.csv and docs/status.md's Next action - a WI row - per the session-protocol skill; new scope needs a WI entry first. When filing or triaging a WI, assign BuildTier deliberately: quick for mechanical/off-spine work, medium by default, strong only for design-shaping or spine-touching work; never silently downgrade a declared route mid-loop. Clear the lowest gate level first: do not queue phase development ahead of its open [phase]-[g1|g2] work or Draft SRs unless the owner deliberately orders it. Gates before every commit (the commit bar): python -m pytest -q -n auto -m smoke and python project-trajectory/scripts/check_docs.py --root . --stale - paste the real output; never report a green you didn't produce. Run the FULL suite (python -m pytest -q -n auto, no -m) before claiming a slice/phase done or at close (session-protocol skill 'End green'). Honor docs/push-policy - human: never push, even if asked. Before stopping: commit progress; update docs/status.md resume point + open items, the WI row's Deliverable in docs/requirements/work-items.csv, and docs/log.md; write docs/run-state - RUNNING while work remains, DONE only at the declared end state, BLOCKED when everything remaining is blocked, NEEDS-HUMAN when the next step needs a human act, stating the ask as a 'Needs <human>' Open item in status.md first."
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
