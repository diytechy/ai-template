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
set -eu
if [ "${1:-}" = "--inner" ]; then
  shift
  cd "$1"
  PT_COORDINATOR_TAKE="$3"
  export PT_COORDINATOR_TAKE
  exec claude "$(cat "$2")"
fi
inner="sh '$0' --inner '$1' '$2' '$3'"
case "$(uname -s)" in
  Darwin) exec osascript -e "tell application \"Terminal\" to do script \"$inner\"" ;;
  *) exec x-terminal-emulator -e sh -c "$inner" ;;
esac
