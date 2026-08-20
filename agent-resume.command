#!/bin/sh
# Agent-resume launcher (macOS) — the double-clickable Finder wrapper. The
# POSIX command template lives once, in agent-resume.sh (edit AGENT_CMD there);
# this file only hops to its own directory so double-click works from anywhere.
# WI-274: the session dials (model/model-map) live once in docs/stack.ini
# [agent-loop] (IF-068), so this wrapper declares no slots of its own — one
# home for the dials, not a third copy.
# INTERPRETER SELECTION (prefer ./.venv, require >= 3.11 — WI-475) is likewise
# NOT repeated here, and this is the launcher set's one exception: a wrapper
# whose whole body is `exec ./agent-resume.sh` has nothing to select FOR — the
# `exec` runs the selection in the twin before the engine ever starts, so the
# venv preference holds here by inheritance rather than by a second copy that
# could drift. It is inheritance and not a gap because it is EXECUTED:
# tests/test_launcher_interpreter.py runs this wrapper against a fake ambient
# python and asserts the venv still wins.
cd "$(dirname "$0")" || exit 1
exec ./agent-resume.sh "$@"
