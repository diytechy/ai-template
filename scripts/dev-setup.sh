#!/usr/bin/env sh
# dev-setup for THIS repo (the ai-template meta-repo) — the concrete dogfood of
# the onboarding ladder's dev-setup rung (project-trajectory/PROCESS.md §7).
#
# The kit ships project-trajectory/scripts/dev-setup.template.{sh,ps1} with EMPTY
# install slots for downstream repos to fill. This is that template *filled in*
# for the meta-repo's own stack, so the kit provisions itself: Python 3.8+, ruff
# (format), pytest + pytest-cov (the self-test suite and the harness's coverage
# step), pytest-xdist (`-n auto` parallel execution — the declared test command,
# WI-075), an offline Mermaid renderer for the generated diagrams, and the two
# agent CLIs the unattended layer routes through — claude + opencode
# (docs/agents.csv pair rows; preflight-enforced at agent-resume boot, WI-109).
# Consent-first: the default only reports; --install acts.
#
# Usage:  sh scripts/dev-setup.sh [--check | --install]
#   --check    (default) report what's present; install nothing.
#   --install  create ./.venv (ruff + pytest + pytest-cov + pytest-xdist, asks first) AND wire
#              the pre-commit process floor (core.hooksPath=.githooks; local +
#              reversible).
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
# have() alone lies on a fresh Mac: /usr/bin/python3 and /usr/bin/git are
# Command Line Tools placeholders that satisfy `command -v` but only pop
# Apple's installer when run. real() trusts /usr/bin/<tool> on Darwin only
# once the toolchain is actually present (xcode-select -p).
real() {
  have "$1" || return 1
  [ "$(uname)" = "Darwin" ] || return 0
  [ "$(command -v "$1")" = "/usr/bin/$1" ] || return 0
  xcode-select -p >/dev/null 2>&1
}
report() { # <label> <present:0/1> <hint>
  if [ "$2" -eq 1 ]; then echo "  [ok]      $1"; else echo "  [missing] $1  — $3"; fi
}

# Prefer the project venv --install creates, so the report reflects what the
# harness will actually import; fall back to the ambient interpreter.
if [ -x .venv/bin/python ]; then PY=.venv/bin/python
elif real python3; then PY=python3; elif real python; then PY=python; else PY=""; fi
echo "dev-setup (ai-template meta-repo). Run tests with: python -m pytest -q"
echo
report "runtime (python3)" "$([ -n "$PY" ] && echo 1 || echo 0)" "install Python 3.8+ (fresh macOS: double-click scripts/dev-setup.command, or xcode-select --install)"
report "git"               "$(real git && echo 1 || echo 0)" "install git (macOS: xcode-select --install)"
report "ruff (format/lint)" "$([ -n "$PY" ] && "$PY" -c 'import importlib.util,sys; sys.exit(0 if importlib.util.find_spec("ruff") else 1)' 2>/dev/null && echo 1 || echo 0)" "pip install ruff (or run --install)"
report "pytest (self-tests)" "$([ -n "$PY" ] && "$PY" -c 'import importlib.util,sys; sys.exit(0 if importlib.util.find_spec("pytest") else 1)' 2>/dev/null && echo 1 || echo 0)" "pip install pytest (or run --install)"
report "pytest-cov (harness coverage step)" "$([ -n "$PY" ] && "$PY" -c 'import importlib.util,sys; sys.exit(0 if importlib.util.find_spec("pytest_cov") else 1)' 2>/dev/null && echo 1 || echo 0)" "pip install pytest-cov (or run --install)"
report "pytest-xdist (parallel -n auto)" "$([ -n "$PY" ] && "$PY" -c 'import importlib.util,sys; sys.exit(0 if importlib.util.find_spec("xdist") else 1)' 2>/dev/null && echo 1 || echo 0)" "pip install pytest-xdist (or run --install)"
# The agent CLIs docs/agents.csv routes through (WI-109) — required for the
# unattended layer (agent_loop preflight refuses to boot without an enabled
# row's CLI); everything above still works without them.
report "claude CLI (agent sessions: agent-resume.*)" "$(have claude && echo 1 || echo 0)" "npm install -g @anthropic-ai/claude-code; then run claude once to sign in"
report "opencode CLI (the OPENAI-* rows in docs/agents.csv)" "$(have opencode && echo 1 || echo 0)" "npm install -g opencode-ai (or see opencode.ai); then: opencode auth login"
report "offline Mermaid renderer" "$( { have code || have mmdc || have npx; } && echo 1 || echo 0)" "VS Code + a Mermaid preview extension, or: npm i -g @mermaid-js/mermaid-cli"
report "pre-commit floor (core.hooksPath)" "$([ "$(git config --get core.hooksPath 2>/dev/null)" = ".githooks" ] && echo 1 || echo 0)" "run --install, or: git config core.hooksPath .githooks"

if [ "$MODE" = "check" ]; then
  echo
  echo "To install ruff + pytest + pytest-cov + pytest-xdist into ./.venv: sh scripts/dev-setup.sh --install"
  exit 0
fi

# --- --install: consent-first venv + dev tools -------------------------------
[ -n "$PY" ] || { echo "Python 3 not found on PATH; install it first." >&2; exit 1; }

# Wire the agent-neutral pre-commit floor (the process-floor rung setup.sh wires
# downstream; this meta-repo folds it into dev-setup — IMPROVEMENT_PLAN WI-1.42).
# Independent of the venv install below, so it happens even if that's declined.
# Local + reversible (git config --unset core.hooksPath); idempotent.
if [ -f .githooks/pre-commit ] && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git config core.hooksPath .githooks
  echo "Enabled pre-commit floor (core.hooksPath=.githooks; undo: git config --unset core.hooksPath)."
fi
echo
printf 'Create ./.venv and install ruff + pytest + pytest-cov + pytest-xdist into it? [y/N] '
read -r ans
case "$ans" in
  [Yy]*) ;;
  *) echo "Cancelled."; exit 0 ;;
esac
[ -d .venv ] || "$PY" -m venv .venv
# shellcheck disable=SC1091
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install ruff pytest pytest-cov pytest-xdist
echo
echo "Done. Run the self-tests with: python -m pytest -q"
