#!/bin/sh
# Agent-resume launcher (macOS) — the double-clickable Finder wrapper. The
# POSIX command template lives once, in agent-resume.sh (edit AGENT_CMD
# there); this file only hops to its own directory so double-click works
# from anywhere.
cd "$(dirname "$0")" || exit 1
exec ./agent-resume.sh "$@"
