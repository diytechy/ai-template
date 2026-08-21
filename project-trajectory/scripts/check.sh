#!/usr/bin/env bash
# Thin launcher for the check harness on Linux/macOS. Prefers the project venv,
# then any Python 3.11+ on PATH. All arguments pass straight through to check.py,
# e.g.:  ./scripts/check.sh --stage DevStg-Impl --tier smoke
set -euo pipefail
cd "$(dirname "$0")/.."

# Probe both venv layouts (hooks/pre-commit pattern): bin/ is POSIX, Scripts/
# is what a Windows-created venv has — Git Bash users would otherwise silently
# skip their venv and run the ambient PATH python. Every candidate is probed by
# RUNNING it, twice, and the .venv is preferred but NOT exempt: check.py imports
# tomllib, so a below-floor interpreter — or a stale venv built on one — is a
# broken run rather than a find, and "exists on PATH" says nothing about that
# (WI-475 / repo-review 2026-08-19 H-01; the same policy agent-resume.* applies).
PY=""
PYWHY=""
pick_py() {
  if [ -n "$PY" ]; then return 0; fi
  if ! "$1" -c "pass" >/dev/null 2>&1; then
    PYWHY="$PYWHY [$1: not runnable here]"
    return 0
  fi
  if ! "$1" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' \
    >/dev/null 2>&1; then
    PYWHY="$PYWHY [$1: older than Python 3.11]"
    return 0
  fi
  PY="$1"
}
if [ -x ".venv/bin/python" ]; then pick_py ".venv/bin/python"; fi
if [ -x ".venv/Scripts/python.exe" ]; then pick_py ".venv/Scripts/python.exe"; fi
pick_py python3
pick_py python
if [ -z "$PY" ]; then
  echo "ERROR: no Python 3.11+ interpreter found. Rejected:$PYWHY" >&2
  echo "Run ./scripts/setup.sh first." >&2
  exit 1
fi

exec "$PY" scripts/check.py "$@"
