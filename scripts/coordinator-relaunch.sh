#!/bin/sh
# Coordinator relaunch, POSIX (WI-822): started detached by the coordinator
# guard at the lease holder's true session end. Opens a terminal in the
# declared repo root and starts `claude` there with the handoff's session
# prompt; the successor token in PT_COORDINATOR_TAKE lets the new session take
# the coordinator lease at its SessionStart.
#
#   coordinator-relaunch.sh REPO_ROOT PROMPT_FILE TOKEN          open a terminal
#   coordinator-relaunch.sh --inner REPO_ROOT PROMPT_FILE TOKEN  run claude here
#
# Windows uses coordinator-relaunch.cmd. Paths must not contain a single quote.
# It starts a model outside the session service, so it asks the guard's
# window-check first and starts nothing inside the blackout window (WI-834).
# The guard's step runs on one interpreter, resolved as run.sh resolves its
# own: each candidate is RUN, and only a Python 3.11+ answers, with its own
# path; after .venv the list is scripts/dev-setup.sh's runtime search. No bare
# `python3` a sub-floor install may answer (round 016 F2, D-019).
set -eu
if [ "${1:-}" = "--inner" ]; then
  shift
  cd "$1"
  PT_COORDINATOR_TAKE="$3"
  export PT_COORDINATOR_TAKE
  exec claude "$(cat "$2")"
fi
resolve_python() {
  cd "$1" || return 1
  for cand in .venv/bin/python .venv/Scripts/python.exe python3 python python3.13 python3.12 python3.11; do
    found=$("$cand" -c 'import sys; sys.version_info >= (3, 11) and print(sys.executable)' 2>/dev/null) || found=""
    if [ -n "$found" ]; then printf '%s\n' "$found"; return 0; fi
  done
  return 1
}
PY=$(resolve_python "$1") || {
  echo "coordinator-relaunch.sh: no Python 3.11+ interpreter found (checked .venv/bin/python, .venv/Scripts/python.exe, python3, python, python3.13, python3.12 and python3.11); install Python 3.11+ or put an installed one first on PATH." >&2
  exit 1
}
"$PY" "$1/project-trajectory/scripts/coordinator_guard.py" --root "$1" window-check || exit 1
inner="sh '$0' --inner '$1' '$2' '$3'"
case "$(uname -s)" in
  Darwin) exec osascript -e "tell application \"Terminal\" to do script \"$inner\"" ;;
  *) exec x-terminal-emulator -e sh -c "$inner" ;;
esac
