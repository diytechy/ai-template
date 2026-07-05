#!/bin/sh
# Agent-resume launcher (POSIX) — boot the right agent session at the right
# tier, or the unattended coordinator loop, from the repo root
# (project-trajectory/PROCESS_OPTIONS.md "Unattended operation (walk-away
# runs)"). This is the kit's own launcher applied to the kit repo itself: the
# booted session inherits the committed context — CLAUDE.md, AGENTS.md,
# IMPROVEMENT_PLAN.md, docs/status.md, docs/gate-policy + run-state. Read it
# first; it only exports the slots below and runs the coordinator engine.
# macOS: agent-resume.command is the double-clickable Finder wrapper.
#
# CONSENT: the unattended loop runs the agent CLI headless; the permission-
# bypass flag in AGENT_CMD means sessions edit without prompts. You consent
# by keeping the slot filled, declaring docs/gate-policy, and running this.

# --- EDIT FOR YOUR PROJECT ----------------------------------------------------
# The agent command template; {model} and {prompt} are substituted per
# session (no {prompt} = the resume prompt is appended).
# Keep agent-resume.cmd's slots in sync — it is the Windows twin.
AGENT_CMD="claude -p {prompt} --model {model} --output-format json --dangerously-skip-permissions"
# Default model tier + optional per-phase map read against docs/run-phase.
# Kit work is gate-bearing template design — default to the strong tier.
AGENT_MODEL="opus"
AGENT_MODEL_MAP=""
# Optional hands-on template for --interactive (defaults to AGENT_CMD):
AGENT_CMD_INTERACTIVE="claude --model {model} {prompt}"
# ------------------------------------------------------------------------------

cd "$(dirname "$0")" || exit 1
if [ -z "$AGENT_CMD" ]; then
  echo "agent-resume.sh: no agent command wired yet." >&2
  echo "Edit AGENT_CMD in this file and in agent-resume.cmd. Filling it (and" >&2
  echo "declaring docs/gate-policy) is your consent to unattended agent" >&2
  echo "sessions; see project-trajectory/PROCESS_OPTIONS.md 'Unattended operation'." >&2
  exit 1
fi
export AGENT_CMD AGENT_MODEL AGENT_MODEL_MAP AGENT_CMD_INTERACTIVE
PY="$(command -v python3 || command -v python)" || {
  echo "agent-resume.sh: python3 not found." >&2; exit 1;
}
# --root . : in this repo the engine lives under project-trajectory/scripts/,
# so its script-relative default would resolve to the kit dir, not the repo.
exec "$PY" project-trajectory/scripts/agent_loop.py --root . "$@"
