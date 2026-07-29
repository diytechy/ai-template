#!/bin/sh
# Agent-resume launcher (POSIX) — boot the right agent session at the right
# tier, or the unattended coordinator loop, from the repo root
# (project-trajectory/PROCESS_OPTIONS.md "Unattended operation (walk-away
# runs)"). This is the kit's own launcher applied to the kit repo itself: the
# booted session inherits the committed context — CLAUDE.md, AGENTS.md,
# docs/status.md, docs/requirements/work-items.csv, docs/log.md, and
# docs/gate-policy (the live working surfaces; IMPROVEMENT_PLAN.md is archived
# history, not a working surface). Read it first; it only exports the slots
# below and runs the coordinator engine.
# macOS: agent-resume.command is the double-clickable Finder wrapper.
#
# CONSENT: the unattended loop runs the agent CLI headless; the permission-
# bypass flag in AGENT_CMD means sessions edit without prompts. You consent
# by keeping the slot filled, declaring docs/gate-policy, and running this.

# --- EDIT FOR YOUR PROJECT ----------------------------------------------------
# The agent command template; {model} and {prompt} are substituted per
# session. NO {prompt} = the prompt is piped to the CLI's STDIN (WI-216) —
# immune to OS command-line caps and Windows batch-shell re-parsing. A .cmd/.bat
# shim with {prompt} is refused even with shell=False; use stdin or a native
# executable.
# Keep agent-resume.cmd's slots in sync — it is the Windows twin.
# stream-json + --verbose (WI-125): the CLI emits an event line per turn, so
# the coordinator console shows live progress instead of 30 silent minutes;
# the final result event carries the same telemetry the json format did.
AGENT_CMD="claude -p --model {model} --output-format stream-json --verbose --dangerously-skip-permissions"
# Default model tier + per-phase fallback map (used when managed routing is off).
# WI-274: the VALUES now live ONCE in docs/stack.ini [agent-loop] (model /
# model-map) — agent_loop reads them there, so a dial change edits one file, not
# this value in three launchers. These slots stay as the env-override tier
# (precedence: CLI flag > this env slot > docs/stack.ini > built-in default);
# leaving them empty lets the declared home win. Owner dial 2026-07-22 (Opus at
# both strong and medium) lives in stack.ini now.
AGENT_MODEL=""
AGENT_MODEL_MAP=""
# Per-phase ROUTING tier for the docs/agents.csv router (strong|medium|quick).
# Empty = the engine's built-in defaults (PLAN / DESIGN-CHECK / CRITIQUE strong,
# BUILD / REVIEW-A / REVIEW-B medium; a worker still pins BUILD up to its WI
# row's BuildTier). EMPTY per the owner directive 2026-07-19: builds are
# Anthropic-led per tier again — Fable takes strong-row BUILDs, Opus takes
# medium — retiring the WI-160 Sol pin (2026-07-14b, which had superseded the
# WI-121 medium relax; both stand in history if this is reverted). Keep
# agent-resume.cmd in sync. tier-up-never-down unchanged.
AGENT_TIER_MAP=""
# Optional within-tier preference per phase. Unknown, disabled, wrong-tier, or
# cooling ids fall through to docs/agents-enabled order; this never changes the
# resolved tier. Empty since 2026-07-19: docs/agents-enabled order already leads
# each tier with the ANTHROPIC row. Keep agent-resume.cmd in sync.
AGENT_PREFER_MAP=""
# Optional per-phase COMMAND template map (cross-provider routing; pairs
# with the docs/review-policy reviewer dial), e.g.:
#   AGENT_CMD_MAP="REVIEW-B=gemini -p {prompt} --model {model}"
# Empty here: under managed routing each enabled row's own CmdTemplate drives
# its launch (docs/agents.csv spans THREE families — ANTHROPIC/claude,
# OPENAI/codex, OPENCODE/opencode-go — all listed in docs/agents-enabled), so
# this per-phase override map has nothing to add; AGENT_CMD stays the
# legacy-path fallback. (Header corrected 2026-07-21 — it wrongly claimed
# single-provider since WI-160.)
AGENT_CMD_MAP=""
# Optional hands-on template for --interactive (defaults to AGENT_CMD):
AGENT_CMD_INTERACTIVE="claude --model {model} {prompt}"
# (The AGENT_JOBS worker-ceiling slot retired with the parallel dispatcher
# at concurrency-restructure Phase 5: claiming and merging run through
# integrate.py, and this launcher boots explicit session roles only —
# agent_loop.py --wi / --interactive / --dual-plan.)
# (The meta-repo resume prompt slot is retired with the serial driver,
# WI-210: worker sessions build their explicit assignments — the repo rules
# live in CLAUDE.md and the session-protocol skill, which every session
# already reads.)
# Per-session wall-clock bound (seconds) so one hung CLI cannot wedge a lane
# forever — the walk-away guarantee (repo-review 2026-07-21 M-18). Blank to
# disable (engine default 0 = no timeout). Keep agent-resume.cmd in sync.
AGENT_SESSION_TIMEOUT="${AGENT_SESSION_TIMEOUT:-7200}"
# ------------------------------------------------------------------------------

cd "$(dirname "$0")" || exit 1
if [ -z "$AGENT_CMD" ]; then
  echo "agent-resume.sh: no agent command wired yet." >&2
  echo "Edit AGENT_CMD in this file and in agent-resume.cmd. Filling it (and" >&2
  echo "declaring docs/gate-policy) is your consent to unattended agent" >&2
  echo "sessions; see project-trajectory/PROCESS_OPTIONS.md 'Unattended operation'." >&2
  exit 1
fi
export AGENT_CMD AGENT_MODEL AGENT_MODEL_MAP AGENT_TIER_MAP AGENT_PREFER_MAP AGENT_CMD_MAP AGENT_CMD_INTERACTIVE
PY="$(command -v python3 || command -v python)" || {
  echo "agent-resume.sh: python3 not found." >&2; exit 1;
}
# --root . : in this repo the engine lives under project-trajectory/scripts/,
# so its script-relative default would resolve to the kit dir, not the repo.
# Explicit flags come first so anything you pass on the command line wins.
if [ -n "$AGENT_SESSION_TIMEOUT" ]; then
  set -- --session-timeout "$AGENT_SESSION_TIMEOUT" "$@"
fi
exec "$PY" project-trajectory/scripts/agent_loop.py --root . "$@"
