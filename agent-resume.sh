#!/bin/sh
# Agent-resume launcher (POSIX) — boot the right agent session at the right
# tier, or the unattended coordinator loop, from the repo root
# (project-trajectory/PROCESS_OPTIONS.md "Unattended operation (walk-away
# runs)"). This is the kit's own launcher applied to the kit repo itself: the
# booted session inherits the committed context — CLAUDE.md, AGENTS.md,
# docs/status.md, docs/requirements/work-items.csv, docs/log.md, docs/gate-policy
# + run-state (the live working surfaces; IMPROVEMENT_PLAN.md is archived
# history, not a working surface). Read it first; it only exports the slots
# below and runs the coordinator engine.
# macOS: agent-resume.command is the double-clickable Finder wrapper.
#
# CONSENT: the unattended loop runs the agent CLI headless; the permission-
# bypass flag in AGENT_CMD means sessions edit without prompts. You consent
# by keeping the slot filled, declaring docs/gate-policy, and running this.

# --- EDIT FOR YOUR PROJECT ----------------------------------------------------
# The agent command template; {model} and {prompt} are substituted per
# session (no {prompt} = the resume prompt is appended).
# Keep agent-resume.cmd's slots in sync — it is the Windows twin.
# stream-json + --verbose (WI-125): the CLI emits an event line per turn, so
# the coordinator console shows live progress instead of 30 silent minutes;
# the final result event carries the same telemetry the json format did.
AGENT_CMD="claude -p {prompt} --model {model} --output-format stream-json --verbose --dangerously-skip-permissions"
# Default model tier + per-phase map read against docs/run-phase (the default
# model stays strong — an unknown phase routes UP, never down). With managed
# routing ON (docs/agents-enabled present) the docs/agents.csv registry +
# AGENT_TIER_MAP below drive selection; these env maps are the declared FALLBACK
# (an absent enable-list = this legacy path). Values kept coherent with the
# owner dial 2026-07-12 evening (WI-121): strong (fable) plans, medium (opus)
# builds + reviews.
AGENT_MODEL="claude-fable-5"
AGENT_MODEL_MAP="PLAN=claude-fable-5,BUILD=opus,REVIEW-A=opus,REVIEW-B=opus,DESIGN-CHECK=claude-fable-5,CRITIQUE=claude-fable-5"
# Per-phase ROUTING tier for the docs/agents.csv router (strong|medium|quick).
# Empty = the engine's built-in defaults (PLAN / DESIGN-CHECK / CRITIQUE strong,
# BUILD / REVIEW-A / REVIEW-B medium). BUILD's initial strong pin was relaxed to
# the medium default at the owner's 2026-07-12-evening dial turn (WI-121 — the
# first live run spent 78% of its wall time in strong-tier BUILD sessions);
# tier-up-never-down still re-raises a contested build to strong.
AGENT_TIER_MAP=""
# Optional per-phase COMMAND template map (cross-provider routing; pairs
# with the docs/review-policy reviewer dial), e.g.:
#   AGENT_CMD_MAP="REVIEW-B=gemini -p {prompt} --model {model}"
# Empty here: single-provider (every docs/agents.csv row is Family=ANTHROPIC), so
# every phase uses AGENT_CMD; add a row + entry when a cross-provider CLI exists.
AGENT_CMD_MAP=""
# Optional hands-on template for --interactive (defaults to AGENT_CMD):
AGENT_CMD_INTERACTIVE="claude --model {model} {prompt}"
# Meta-repo resume prompt: the engine's default prompt assumes a scaffolded
# downstream repo (docs/process.md etc.); this one names THIS repo's actual
# surfaces. Empty = fall back to the engine default.
AGENT_PROMPT="You are the driver session for the ai-template META-repo - the kit source, self-applied. Read CLAUDE.md, then docs/status.md Current State. The process masters are project-trajectory/PROCESS.md and PROCESS_OPTIONS.md 'Unattended operation'; no scaffolded docs/process.md exists here. Work only scope recorded in docs/requirements/work-items.csv and docs/status.md's Next action - a WI row - per the session-protocol skill; new scope needs a WI entry first. Gates before every commit (the commit bar): python -m pytest -q -n auto -m smoke and python project-trajectory/scripts/check_docs.py --root . --stale - paste the real output; never report a green you didn't produce. Run the FULL suite (python -m pytest -q -n auto, no -m) before claiming a slice/campaign done or at close (session-protocol skill 'End green'). Honor docs/push-policy - human: never push, even if asked. Before stopping: commit progress; update docs/status.md resume point + open items, docs/next-wi (the next WI id - or a ';'-joined batch of independent off-spine WIs to execute in order as ONE session with ONE review round, WI-133 - for the coordinator's BuildTier pin), the WI row's Deliverable in docs/requirements/work-items.csv, and docs/log.md; write docs/run-state - RUNNING while work remains, DONE only at the declared end state, BLOCKED when everything remaining is blocked, NEEDS-HUMAN when the next step needs a human act, stating the ask as a 'Needs <human>' Open item in status.md first."
# ------------------------------------------------------------------------------

cd "$(dirname "$0")" || exit 1
if [ -z "$AGENT_CMD" ]; then
  echo "agent-resume.sh: no agent command wired yet." >&2
  echo "Edit AGENT_CMD in this file and in agent-resume.cmd. Filling it (and" >&2
  echo "declaring docs/gate-policy) is your consent to unattended agent" >&2
  echo "sessions; see project-trajectory/PROCESS_OPTIONS.md 'Unattended operation'." >&2
  exit 1
fi
export AGENT_CMD AGENT_MODEL AGENT_MODEL_MAP AGENT_TIER_MAP AGENT_CMD_MAP AGENT_CMD_INTERACTIVE
PY="$(command -v python3 || command -v python)" || {
  echo "agent-resume.sh: python3 not found." >&2; exit 1;
}
# --root . : in this repo the engine lives under project-trajectory/scripts/,
# so its script-relative default would resolve to the kit dir, not the repo.
# Explicit flags come first so anything you pass on the command line wins.
if [ -n "$AGENT_PROMPT" ]; then
  exec "$PY" project-trajectory/scripts/agent_loop.py --root . --prompt "$AGENT_PROMPT" "$@"
fi
exec "$PY" project-trajectory/scripts/agent_loop.py --root . "$@"
