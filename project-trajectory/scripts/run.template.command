#!/bin/sh
# Product launcher (macOS) — the double-clickable Finder wrapper. The launch
# capabilities live once, in docs/stack.ini's [run] section (read by run.sh via
# scripts/run_menu.py); this file only hops to its own directory so double-click
# works from anywhere, then delegates to run.sh.
cd "$(dirname "$0")" || exit 1
exec ./run.sh "$@"
