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
# session. NO {prompt} = the prompt is piped to the CLI's STDIN (WI-216) —
# immune to the OS command-line caps (a brief-sized prompt-in-argv dies at the
# Windows 8191/32767-char limits); keep {prompt} only for a CLI with no stdin
# prompt path.
# Keep agent-resume.cmd's slots in sync — it is the Windows twin.
# stream-json + --verbose (WI-125): the CLI emits an event line per turn, so
# the coordinator console shows live progress instead of 30 silent minutes;
# the final result event carries the same telemetry the json format did.
AGENT_CMD="claude -p --model {model} --output-format stream-json --verbose --dangerously-skip-permissions"
# Default model tier + per-phase map keyed on the in-process phase (the default
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
# BUILD / REVIEW-A / REVIEW-B medium). BUILD=strong per the owner directive
# 2026-07-14b (WI-160): builds prefer Codex Sol — strong tier + OPENAI-SOL first
# in docs/agents-enabled — superseding FOR NOW the WI-121 medium relax (which
# had undone the original strong pin after 78% wall time in strong BUILDs;
# that history stands if this directive is reverted). Keep agent-resume.cmd in
# sync. tier-up-never-down unchanged.
AGENT_TIER_MAP="BUILD=strong"
# Optional within-tier preference per phase. Unknown, disabled, wrong-tier, or
# cooling ids fall through to docs/agents-enabled order; this never changes the
# resolved tier. Keep agent-resume.cmd in sync.
AGENT_PREFER_MAP="BUILD=OPENAI-SOL"
# Optional per-phase COMMAND template map (cross-provider routing; pairs
# with the docs/review-policy reviewer dial), e.g.:
#   AGENT_CMD_MAP="REVIEW-B=gemini -p {prompt} --model {model}"
# Empty here: single-provider (every docs/agents.csv row is Family=ANTHROPIC), so
# every phase uses AGENT_CMD; add a row + entry when a cross-provider CLI exists.
AGENT_CMD_MAP=""
# Optional hands-on template for --interactive (defaults to AGENT_CMD):
AGENT_CMD_INTERACTIVE="claude --model {model} {prompt}"
# This repo has completed the dispatcher migration audits in docs/parallel-ready,
# so normal launches use the two-worker dispatcher. Pass --jobs 1 for a serial
# dispatcher run; an absent slot also boots the dispatcher (WI-210 — the
# legacy serial driver is retired), defaulting to 2 held at 1 until audited.
AGENT_JOBS="2"
# (The meta-repo resume prompt slot is retired with the serial driver,
# WI-210: a plain launch is the dispatcher, and worker sessions build
# their explicit assignments — the repo rules live in CLAUDE.md and the
# session-protocol skill, which every session already reads.)
# ------------------------------------------------------------------------------

cd "$(dirname "$0")" || exit 1
if [ -z "$AGENT_CMD" ]; then
  echo "agent-resume.sh: no agent command wired yet." >&2
  echo "Edit AGENT_CMD in this file and in agent-resume.cmd. Filling it (and" >&2
  echo "declaring docs/gate-policy) is your consent to unattended agent" >&2
  echo "sessions; see project-trajectory/PROCESS_OPTIONS.md 'Unattended operation'." >&2
  exit 1
fi
export AGENT_CMD AGENT_MODEL AGENT_MODEL_MAP AGENT_TIER_MAP AGENT_PREFER_MAP AGENT_CMD_MAP AGENT_CMD_INTERACTIVE AGENT_JOBS
PY="$(command -v python3 || command -v python)" || {
  echo "agent-resume.sh: python3 not found." >&2; exit 1;
}
# --root . : in this repo the engine lives under project-trajectory/scripts/,
# so its script-relative default would resolve to the kit dir, not the repo.
# Explicit flags come first so anything you pass on the command line wins.
exec "$PY" project-trajectory/scripts/agent_loop.py --root . "$@"
