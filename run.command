#!/bin/sh
# Actions-menu launcher (macOS) for THIS repo — the double-clickable Finder
# wrapper. The actions live once, in docs/stack.ini's [run] section (read by
# run.sh via project-trajectory/scripts/run_menu.py); this file only hops to its own directory so double-click
# works from anywhere, then delegates to run.sh, which runs dev-setup's check
# for a bare run (once: this wrapper runs none of its own).
cd "$(dirname "$0")" || exit 1
exec ./run.sh "$@"
