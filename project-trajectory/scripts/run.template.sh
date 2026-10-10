#!/bin/sh
# Product launcher (POSIX) — run this project with no commands to remember.
# It presents the capabilities declared in docs/stack.ini's [run] section
# (process.md §7, "the evaluator's rungs"): no args = a numbered menu, and
# `run.sh <name>` launches one directly. Read it first; it only delegates to
# scripts/run_menu.py, so the launch commands live once, in docs/stack.ini.
# macOS: run.command is the double-clickable Finder wrapper around this file.
#
# A bare run (no arguments: the double-click) first runs dev-setup's check for
# run, `scripts/dev-setup.sh --for-run --python <interpreter>`, from the
# repository root: the workstation report, then, at an interactive terminal
# only, each missing piece offered consent-first. A runtime still missing
# afterwards ends the run with the step to take instead of the menu.
# `run.sh <name>` and `run.sh --list`, the agent surface, never run it and
# never prompt. run.command delegates here, so the check runs once.
#
# One interpreter: it is resolved once below, the check is handed exactly that
# interpreter, and the menu runs on it, so the menu runs on the interpreter
# whose 3.11 floor the check confirmed. Each candidate is probed by RUNNING it,
# and the probe prints the interpreter's own path only when it satisfies the
# floor (run_menu.py imports tomllib); nothing is chosen by mere existence.
# After .venv, the list is scripts/dev-setup.sh's own runtime search, so a check that
# finds a runtime means this resolves one too.
# With none resolved, a bare run's check reports the runtime missing and the
# direct and list forms exit 1 with the step.
#
# Not applicable (a pure library)? Delete the run.* launchers and describe
# usage in README.md instead.

cd "$(dirname "$0")" || exit 1
PY=""
for cand in .venv/bin/python .venv/Scripts/python.exe python3 python; do
  PY=$("$cand" -c 'import sys; sys.version_info >= (3, 11) and print(sys.executable)' 2>/dev/null) || PY=""
  [ -n "$PY" ] && break
done
if [ "$#" -eq 0 ]; then
  sh scripts/dev-setup.sh --for-run ${PY:+--python "$PY"} || {
    echo "run.sh: the runtime is still missing; take the step above, then run again." >&2
    exit 1
  }
elif [ -z "$PY" ]; then
  echo "run.sh: no Python 3.11+ interpreter found (checked .venv/bin/python, .venv/Scripts/python.exe, python3 and python); install Python 3.11+ or put an installed one first on PATH, then run again." >&2
  exit 1
fi
exec "$PY" scripts/run_menu.py "$@"
