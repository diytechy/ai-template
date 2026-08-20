#!/bin/sh
# Agent-resume launcher (POSIX) — boot the right agent session at the right
# tier, or the unattended coordinator loop, from the repo root
# (process-options.md "Unattended operation (walk-away runs)"). The booted
# session inherits the whole committed context — AGENTS.md, docs/status.md,
# docs/gate + docs/process.toml — so resuming work never requires
# recalling an incantation. Read it first; it only exports the slots below
# and runs scripts/agent_loop.py.
# macOS: agent-resume.command is the double-clickable Finder wrapper.
#
# CONSENT: the unattended loop runs the agent CLI headless; a permission-
# bypass flag in AGENT_CMD means sessions edit without prompts. You consent
# by filling the slot, declaring docs/process.toml, and running this.
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
# the the process.toml reviewer dial reviewer dial — cross-provider dual review is the
# recommended review-policy 2 config), e.g.:
#   AGENT_CMD_MAP="REVIEW-B=gemini -p {prompt} --model {model}"
AGENT_CMD_MAP=""
# Optional hands-on template for --interactive (defaults to AGENT_CMD):
AGENT_CMD_INTERACTIVE=""
# Parallel work runs through the integration seam (process-options.md
# "Parallel work — the integration seam"): claim with `integrate.py claim`,
# build worker sessions on the claimed branches (this launcher: --wi in the
# branch's worktree), merge through `integrate.py integrate`. (The AGENT_JOBS
# dispatcher ceiling retired with the parallel dispatcher at
# concurrency-restructure Phase 5.)
# Single-home option (IF-068): to avoid editing model/model-map in each of
# the three launchers, declare them once in docs/stack.ini [agent-loop] and
# keep AGENT_MODEL / AGENT_MODEL_MAP blank — agent_loop resolves CLI flag >
# AGENT_* env > that file > default.
# Per-session wall-clock bound (seconds) so one hung CLI cannot wedge a lane
# forever — the walk-away guarantee. Blank to disable (engine default 0 = no
# timeout). Keep agent-resume.cmd in sync.
AGENT_SESSION_TIMEOUT="${AGENT_SESSION_TIMEOUT:-7200}"
# ------------------------------------------------------------------------------

cd "$(dirname "$0")" || exit 1
if [ -z "$AGENT_CMD" ]; then
  echo "agent-resume.sh: no agent command wired yet." >&2
  echo "Edit AGENT_CMD in this file and in agent-resume.cmd. Filling it (and" >&2
  echo "declaring docs/process.toml) is your consent to unattended agent" >&2
  echo "sessions; see docs/process-options.md 'Unattended operation'." >&2
  exit 1
fi
export AGENT_CMD AGENT_MODEL AGENT_MODEL_MAP AGENT_PREFER_MAP AGENT_CMD_MAP AGENT_CMD_INTERACTIVE
# Pick the interpreter that can actually RUN the engine, in preference order:
# this repo's OWN .venv first (the pinned >=3.11 toolchain scripts/setup.sh
# builds), then python3, then python. Every candidate is probed by RUNNING it —
# twice, because "found" and "usable" are two different questions:
#   1. `-c "pass"` — does it run at all? A Windows `python3` on PATH is often
#      the Microsoft-Store alias stub, which exists and runs nothing.
#   2. sys.version_info — the engine and every kit script import tomllib, so
#      anything below the kit's 3.11 floor is a broken boot, not a find. An
#      adopter targeting an older runtime lowers this WITH scripts/setup.*.
# Both .venv layouts are probed: bin/ is POSIX, Scripts/ is what a
# Windows-created venv has, so a Git Bash user finds their own venv too (the
# check.sh / pre-commit pattern).
PY=""
PYWHY=""
pick_py() {
  if [ -n "$PY" ]; then return 0; fi
  if ! "$1" -c "pass" >/dev/null 2>&1; then
    PYWHY="$PYWHY [$1: not runnable here]"
    return 0
  fi
  if ! "$1" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' \
    >/dev/null 2>&1; then
    PYWHY="$PYWHY [$1: older than Python 3.11]"
    return 0
  fi
  PY="$1"
}
if [ -x ".venv/bin/python" ]; then pick_py ".venv/bin/python"; fi
if [ -x ".venv/Scripts/python.exe" ]; then pick_py ".venv/Scripts/python.exe"; fi
pick_py python3
pick_py python
if [ -z "$PY" ]; then
  echo "agent-resume.sh: no Python 3.11+ interpreter found." >&2
  echo "Rejected:$PYWHY" >&2
  echo "Build the project environment (scripts/setup.sh) or install Python" >&2
  echo "3.11+ and re-run." >&2
  exit 1
fi
if [ -n "$AGENT_SESSION_TIMEOUT" ]; then
  set -- --session-timeout "$AGENT_SESSION_TIMEOUT" "$@"
fi
exec "$PY" scripts/agent_loop.py "$@"
