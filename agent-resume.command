#!/bin/sh
# Agent-resume launcher (macOS) — the double-clickable Finder wrapper. The
# POSIX command template lives once, in agent-resume.sh (edit AGENT_CMD
# there); this file only declares the audited dispatcher default and hops to
# its own directory so double-click works from anywhere. Pass --jobs 1 for a
# serial dispatcher run. agent-resume.sh honors this inherited value (it
# defaulted over it before — repo-review 2026-07-21 L-22), so editing the
# slot here works.
AGENT_JOBS="2"
export AGENT_JOBS
cd "$(dirname "$0")" || exit 1
exec ./agent-resume.sh "$@"
