#!/usr/bin/env bash
# Thin launcher for the check harness on Linux/macOS. Prefers the project venv,
# then any Python 3 on PATH. All arguments pass straight through to check.py,
# e.g.:  ./scripts/check.sh --gate DevBar-Release --tier smoke
set -euo pipefail
cd "$(dirname "$0")/.."

# Probe both venv layouts (hooks/pre-commit pattern): bin/ is POSIX, Scripts/
# is what a Windows-created venv has — Git Bash users would otherwise silently
# skip their venv and run the ambient PATH python.
PY=""
for venvpy in .venv/bin/python .venv/Scripts/python.exe; do
  if [ -x "$venvpy" ]; then PY="$venvpy"; break; fi
done
if [ -z "$PY" ]; then
  for cand in python3 python; do
    if command -v "$cand" >/dev/null 2>&1; then PY="$cand"; break; fi
  done
  [ -n "$PY" ] || { echo "ERROR: Python 3 not found. Run ./scripts/setup.sh first." >&2; exit 1; }
fi

exec "$PY" scripts/check.py "$@"
