#!/usr/bin/env bash
# One-shot dev setup for Linux/macOS. Makes a fresh clone runnable. Idempotent.
# Edit the dependency list for your project; the reference installs the tools the
# Python check harness uses. Windows: use scripts/setup.ps1.
set -euo pipefail
cd "$(dirname "$0")/.."

# Find a supported Python interpreter. Probe by running it, not just finding it: on
# Windows (Git Bash), `python3` can resolve to the Microsoft Store alias, which
# exists on PATH but doesn't run.
python_311() {
  "$1" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' \
    >/dev/null 2>&1
}
PY=""
for cand in python3 python; do
  if command -v "$cand" >/dev/null 2>&1 && python_311 "$cand"; then
    PY="$cand"; break
  fi
done
[ -n "$PY" ] || { echo "ERROR: Python 3.11+ not found on PATH." >&2; exit 1; }
echo "Using $($PY --version)"

# Create/activate a local virtualenv so installs don't touch the system Python.
if [ ! -d .venv ]; then
  echo "Creating .venv ..."
  "$PY" -m venv .venv
elif [ ! -x .venv/bin/python ] || ! python_311 .venv/bin/python; then
  echo "ERROR: Existing ./.venv does not use Python 3.11+; move or remove it, then rerun setup." >&2
  exit 1
fi
# shellcheck disable=SC1091
. .venv/bin/activate

python -m pip install --upgrade pip
# --- Edit below for your stack -------------------------------------------------
# This INSTALLS the tools; what the harness RUNS (format/lint/test commands,
# tiers, coverage) is declared once in docs/stack.ini — edit there, not in
# check.py. Install whatever those commands name.
pip install ruff pytest pytest-cov
if [ -f pyproject.toml ]; then pip install -e .
elif [ -f requirements.txt ]; then pip install -r requirements.txt
fi
# ------------------------------------------------------------------------------

# Enable the agent-neutral pre-commit hook (the process floor) if this is a git
# repo. Opt-in + reversible: undo with `git config --unset core.hooksPath`.
if [ -f .githooks/pre-commit ] && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git config core.hooksPath .githooks
  echo "Enabled pre-commit hook (core.hooksPath=.githooks; undo: git config --unset core.hooksPath)."
fi

# Privacy-check advisory (docs/privacy-check — process-options.md "Commit
# identity & privacy"). Identity is USER-owned: setup no longer pins or sets an
# author identity. But when the privacy gate is on, the author email must be in
# the exempt allowlist (no private/contactable address) or commits are blocked —
# so warn early if this clone's identity would fail. Advisory only; the hooks are
# the enforcement. Reuses check_privacy.py --author to single-source the list.
if [ -f docs/privacy-check ] && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  privacy=$(grep -v '^[[:space:]]*#' docs/privacy-check | grep -v '^[[:space:]]*$' | head -n 1 | tr -d '[:space:]' || true)
  if [ "$privacy" = "true" ] && ! "$PY" scripts/check_privacy.py --author >/dev/null 2>&1; then
    email=$(git config user.email 2>/dev/null || true)
    echo "WARNING: docs/privacy-check is on, but this clone's git author email" >&2
    echo "  '${email:-unset}' is not in the exempt allowlist (scripts/check_privacy.py" >&2
    echo "  EXEMPT_EMAILS), so commits will be blocked. Set a no-reply identity:" >&2
    echo "    git config user.email <you>@users.noreply.github.com   (repo-local)" >&2
  fi
fi

echo
echo "Setup complete. Run the harness with: ./scripts/check.sh --stage DevStg-Impl"
echo "(check.sh uses the venv python directly; activating is optional.)"
