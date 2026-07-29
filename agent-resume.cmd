@echo off
setlocal
REM Agent-resume launcher (Windows) - double-click to boot the right agent
REM session at the right tier, or the unattended coordinator loop, from the
REM repo root (project-trajectory/PROCESS_OPTIONS.md "Unattended operation
REM (walk-away runs)"). This is the kit's own launcher applied to the kit
REM repo itself: the booted session inherits the committed context -
REM CLAUDE.md, AGENTS.md, docs/status.md, the docs/work/ registry,
REM docs/log.md, docs/gate-policy (the live working surfaces;
REM IMPROVEMENT_PLAN.md is archived history, not a working surface). Read it
REM first; it only exports the slots below and runs the coordinator engine.
REM
REM CONSENT: the unattended loop runs the agent CLI headless; the permission-
REM bypass flag in AGENT_CMD means sessions edit without prompts. You consent
REM by keeping the slot filled, declaring docs/gate-policy, and running this.

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
REM with the docs/review-policy reviewer dial), e.g.:
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
  echo in agent-resume.sh. Filling it ^(and declaring docs/gate-policy^) is your
  echo consent to unattended agent sessions; see
  echo project-trajectory/PROCESS_OPTIONS.md "Unattended operation".
  pause
  exit /b 1
)
REM Probe by RUNNING the candidate, not just finding it: on a bare Windows
REM box `where python` matches the Microsoft-Store app-execution alias, a
REM stub that opens the Store instead of running (the hooks' pattern,
REM applied here - repo-review 2026-07-21 M-16).
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
REM --root . : in this repo the engine lives under project-trajectory\scripts\,
REM so its script-relative default would resolve to the kit dir, not the repo.
REM Explicit flags come first so anything you pass on the command line wins.
%PY% project-trajectory\scripts\agent_loop.py --root . %TIMEOUT_ARGS% %*
set "EXITCODE=%ERRORLEVEL%"
echo.
echo Exited with code %EXITCODE%.
pause
exit /b %EXITCODE%
