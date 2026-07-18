#!/bin/sh
# Product launcher (POSIX) — run this project with no commands to remember.
# It presents the capabilities declared in docs/stack.ini's [run] section
# (process.md §7, "the evaluator's rungs"): no args = a numbered menu, and
# `run.sh <name>` launches one directly. Read it first; it only delegates to
# scripts/run_menu.py, so the launch commands live once, in docs/stack.ini.
# macOS: run.command is the double-clickable Finder wrapper around this file.
#
# Not applicable (a pure library)? Delete the run.* launchers and describe
# usage in README.md instead.

cd "$(dirname "$0")" || exit 1
PY="$(command -v python3 || command -v python)" || {
  echo "run.sh: python3 not found." >&2
  exit 1
}
exec "$PY" scripts/run_menu.py "$@"
