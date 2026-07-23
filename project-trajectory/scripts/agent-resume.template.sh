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
# session. NO {prompt} = the prompt is piped to the CLI's STDIN — immune to
# the OS command-line caps (Windows: 8191 chars under cmd.exe .CMD shims,
# ~32767 via CreateProcess). A Windows .cmd/.bat shim with {prompt} is refused
# because cmd.exe can reparse prompt metacharacters even with shell=False; use
# stdin or a native executable. Example:
#   AGENT_CMD="claude -p --model {model} --output-format json --dangerously-skip-permissions"
# Keep agent-resume.cmd's slots in sync — it is the Windows twin.
AGENT_CMD=""
# Default model tier + optional per-phase map keyed on the in-process phase.
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
# Parallel dispatch (process-options.md "Worker assignment"): a FRESH scaffold
# ships parallel-by-default at two workers. The dispatcher still HOLDS at one
# worker until this repo's soft-edge + SafetyClass audits pass (a fresh
# scaffold passes by construction); a repo migrating in from the legacy loop
# sets AGENT_JOBS=1 here until it signs off (the downstream-resync skill).
# An inherited AGENT_JOBS wins over this default; an absent/empty value still
# boots the dispatcher at its own default (the legacy serial resume driver is
# retired).
# Single-home option (IF-068): to avoid editing jobs/model/model-map in each of
# the three launchers, declare them once in docs/stack.ini [agent-loop]. Keep
# AGENT_MODEL / AGENT_MODEL_MAP blank; for jobs, replace the next line with
# `unset AGENT_JOBS` AND remove AGENT_JOBS from the export line below. That exact
# POSIX edit leaves no launcher env override, so agent_loop resolves CLI flag >
# AGENT_* env > that file > default. Opt-in: a fresh scaffold keeps its dials in
# the launcher by default.
AGENT_JOBS="${AGENT_JOBS:-2}"
# Per-session wall-clock bound (seconds) so one hung CLI cannot wedge a lane
# forever — the walk-away guarantee. Blank to disable (engine default 0 = no
# timeout). Keep agent-resume.cmd in sync.
AGENT_SESSION_TIMEOUT="${AGENT_SESSION_TIMEOUT:-7200}"
# ------------------------------------------------------------------------------

cd "$(dirname "$0")" || exit 1
if [ -z "$AGENT_CMD" ]; then
  echo "agent-resume.sh: no agent command wired yet." >&2
  echo "Edit AGENT_CMD in this file and in agent-resume.cmd. Filling it (and" >&2
  echo "declaring docs/gate-policy) is your consent to unattended agent" >&2
  echo "sessions; see docs/process-options.md 'Unattended operation'." >&2
  exit 1
fi
export AGENT_CMD AGENT_MODEL AGENT_MODEL_MAP AGENT_PREFER_MAP AGENT_CMD_MAP AGENT_CMD_INTERACTIVE AGENT_JOBS
PY="$(command -v python3 || command -v python)" || {
  echo "agent-resume.sh: python3 not found." >&2; exit 1;
}
if [ -n "$AGENT_SESSION_TIMEOUT" ]; then
  set -- --session-timeout "$AGENT_SESSION_TIMEOUT" "$@"
fi
exec "$PY" scripts/agent_loop.py "$@"
