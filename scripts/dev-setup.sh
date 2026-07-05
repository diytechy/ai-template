#!/usr/bin/env sh
# dev-setup for THIS repo (the ai-template meta-repo) — the concrete dogfood of
# the onboarding ladder's dev-setup rung (project-trajectory/PROCESS.md §7).
#
# The kit ships project-trajectory/scripts/dev-setup.template.{sh,ps1} with EMPTY
# install slots for downstream repos to fill. This is that template *filled in*
# for the meta-repo's own stack, so the kit provisions itself: Python 3.8+, ruff
# (format), pytest (the self-test suite), and an offline Mermaid renderer for the
# generated diagrams. Consent-first: the default only reports; --install acts.
#
# Usage:  sh scripts/dev-setup.sh [--check | --install]
#   --check    (default) report what's present; install nothing.
#   --install  create ./.venv and install ruff + pytest into it (asks first).
#
# Windows contributors: use scripts/dev-setup.ps1.
set -eu
cd "$(dirname "$0")/.."  # scripts/ -> the repo root (like the scaffolded layout)

MODE="check"
case "${1:-}" in
  --install) MODE="install" ;;
  --check|"") MODE="check" ;;
  -h|--help) sed -n '2,16p' "$0"; exit 0 ;;
  *) echo "Unknown option: $1" >&2; exit 2 ;;
esac

have() { command -v "$1" >/dev/null 2>&1; }
report() { # <label> <present:0/1> <hint>
  if [ "$2" -eq 1 ]; then echo "  [ok]      $1"; else echo "  [missing] $1  — $3"; fi
}

if have python3; then PY=python3; elif have python; then PY=python; else PY=""; fi
echo "dev-setup (ai-template meta-repo). Run tests with: python -m pytest -q"
echo
report "runtime (python3)" "$([ -n "$PY" ] && echo 1 || echo 0)" "install Python 3.8+"
report "git"               "$(have git && echo 1 || echo 0)" "install git"
report "ruff (format/lint)" "$([ -n "$PY" ] && "$PY" -c 'import importlib.util,sys; sys.exit(0 if importlib.util.find_spec("ruff") else 1)' 2>/dev/null && echo 1 || echo 0)" "pip install ruff (or run --install)"
report "pytest (self-tests)" "$([ -n "$PY" ] && "$PY" -c 'import importlib.util,sys; sys.exit(0 if importlib.util.find_spec("pytest") else 1)' 2>/dev/null && echo 1 || echo 0)" "pip install pytest (or run --install)"
report "offline Mermaid renderer" "$( { have code || have mmdc || have npx; } && echo 1 || echo 0)" "VS Code + a Mermaid preview extension, or: npm i -g @mermaid-js/mermaid-cli"

if [ "$MODE" = "check" ]; then
  echo
  echo "To install ruff + pytest into ./.venv: sh scripts/dev-setup.sh --install"
  exit 0
fi

# --- --install: consent-first venv + dev tools -------------------------------
[ -n "$PY" ] || { echo "Python 3 not found on PATH; install it first." >&2; exit 1; }
echo
printf 'Create ./.venv and install ruff + pytest into it? [y/N] '
read -r ans
case "$ans" in
  [Yy]*) ;;
  *) echo "Cancelled."; exit 0 ;;
esac
[ -d .venv ] || "$PY" -m venv .venv
# shellcheck disable=SC1091
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install ruff pytest
echo
echo "Done. Run the self-tests with: python -m pytest -q"
