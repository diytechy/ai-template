#!/bin/sh
# Agent-resume launcher (macOS) — the double-clickable Finder wrapper. The
# POSIX command template lives once, in agent-resume.sh (edit AGENT_CMD there);
# this file only hops to its own directory so double-click works from anywhere.
# WI-274: the dispatcher dials (jobs/model/model-map) now live once in
# docs/stack.ini [agent-loop] (IF-068), so this wrapper no longer declares its
# own AGENT_JOBS slot — one home for the dials, not a third copy.
cd "$(dirname "$0")" || exit 1
exec ./agent-resume.sh "$@"
