#!/bin/sh
# Agent-resume launcher (POSIX) — boot the right agent session at the right
# tier, or the unattended coordinator loop, from the repo root
# (process-options.md "Unattended operation (walk-away runs)"). The booted
# session inherits the whole committed context — AGENTS.md, docs/status.md,
# docs/gate + gate-policy + run-state — so resuming work never requires
# recalling an incantation. Read it first; it only exports the slots below
# and runs scripts/agent_loop.py.
# macOS: agent-resume.command is the double-clickable Finder wrapper.
#
# CONSENT: the unattended loop runs the agent CLI headless; a permission-
# bypass flag in AGENT_CMD means sessions edit without prompts. You consent
# by filling the slot, declaring docs/gate-policy, and running this.
# No agent-driven work in this repo? Delete the agent-resume.* launchers.

# --- EDIT FOR YOUR PROJECT ----------------------------------------------------
# The agent command template; {model} and {prompt} are substituted per
# session (no {prompt} = the resume prompt is appended). Example:
#   AGENT_CMD="claude -p {prompt} --model {model} --output-format json --dangerously-skip-permissions"
# Keep agent-resume.cmd's slots in sync — it is the Windows twin.
AGENT_CMD=""
# Default model tier + optional per-phase map read against docs/run-phase.
# The plan/build cadence (process-options.md "Unattended operation") wires
# strong-model-plans / cheaper-model-executes here, e.g.:
#   AGENT_MODEL_MAP="PLAN=<strong-model>,BUILD=<cheap-model>"
AGENT_MODEL=""
AGENT_MODEL_MAP=""
# Optional per-phase preference WITHIN the resolved routing tier, e.g.:
#   AGENT_PREFER_MAP="BUILD=OPENAI-SOL"
# Unknown/cooling ids fall through to docs/agents-enabled order.
AGENT_PREFER_MAP=""
# Optional per-phase COMMAND template map (cross-provider routing; pairs with
# the docs/review-policy reviewer dial — cross-provider dual review is the
# recommended review-policy 2 config), e.g.:
#   AGENT_CMD_MAP="REVIEW-B=gemini -p {prompt} --model {model}"
AGENT_CMD_MAP=""
# Optional hands-on template for --interactive (defaults to AGENT_CMD):
AGENT_CMD_INTERACTIVE=""
# ------------------------------------------------------------------------------

cd "$(dirname "$0")" || exit 1
if [ -z "$AGENT_CMD" ]; then
  echo "agent-resume.sh: no agent command wired yet." >&2
  echo "Edit AGENT_CMD in this file and in agent-resume.cmd. Filling it (and" >&2
  echo "declaring docs/gate-policy) is your consent to unattended agent" >&2
  echo "sessions; see docs/process-options.md 'Unattended operation'." >&2
  exit 1
fi
export AGENT_CMD AGENT_MODEL AGENT_MODEL_MAP AGENT_PREFER_MAP AGENT_CMD_MAP AGENT_CMD_INTERACTIVE
PY="$(command -v python3 || command -v python)" || {
  echo "agent-resume.sh: python3 not found." >&2; exit 1;
}
exec "$PY" scripts/agent_loop.py "$@"
