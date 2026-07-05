#!/usr/bin/env bash
# One-shot dev setup for Linux/macOS. Makes a fresh clone runnable. Idempotent.
# Edit the dependency list for your project; the reference installs the tools the
# Python check harness uses. Windows: use scripts/setup.ps1.
set -euo pipefail
cd "$(dirname "$0")/.."

# Find a Python 3 interpreter. Probe by running it, not just finding it: on
# Windows (Git Bash), `python3` can resolve to the Microsoft Store alias, which
# exists on PATH but doesn't run.
PY=""
for cand in python3 python; do
  if command -v "$cand" >/dev/null 2>&1 && "$cand" -c "" >/dev/null 2>&1; then
    PY="$cand"; break
  fi
done
[ -n "$PY" ] || { echo "ERROR: Python 3 not found on PATH." >&2; exit 1; }
echo "Using $($PY --version)"

# Create/activate a local virtualenv so installs don't touch the system Python.
if [ ! -d .venv ]; then
  echo "Creating .venv ..."
  "$PY" -m venv .venv
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

# Apply the repo's commit-identity policy (docs/commit-identity —
# process-options.md "Commit identity & anonymity"): when it names an email
# pattern and this clone's effective identity doesn't match, ask for name/email
# and set them REPO-LOCALLY — never --global. Consent-first: prompts only on a
# TTY; a non-interactive run warns and moves on (the pre-commit hook is the
# enforcement — it blocks a mismatched commit either way).
if [ -f docs/commit-identity ] && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  policy=$(grep -v '^[[:space:]]*#' docs/commit-identity | grep -v '^[[:space:]]*$' | head -n 1 | tr -d '[:space:]' || true)
  if [ -n "$policy" ] && [ "$policy" != "inherit" ]; then
    email=$(git config user.email 2>/dev/null || true)
    case "$email" in
      $policy) : ;; # already satisfied
      *)
        if [ -t 0 ]; then
          echo "This repo's commit-identity policy is '$policy'; this clone's identity is '${email:-unset}'."
          printf "Author name for this repo: "; read -r ci_name
          printf "Author email (must match %s; GitHub anonymous form: <user>@users.noreply.github.com): " "$policy"; read -r ci_email
          git config user.name "$ci_name"
          git config user.email "$ci_email"
          echo "Set repo-local identity for this clone (global config untouched)."
        else
          echo "WARNING: commit-identity policy '$policy' unsatisfied (email '${email:-unset}');" >&2
          echo "  rerun scripts/setup interactively or set a repo-local git config user.name/user.email —" >&2
          echo "  the pre-commit hook blocks mismatched commits." >&2
        fi
        ;;
    esac
  fi
fi

echo
echo "Setup complete. Run the harness with: ./scripts/check.sh --gate G3"
echo "(check.sh uses the venv python directly; activating is optional.)"
