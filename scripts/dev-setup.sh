#!/usr/bin/env sh
# dev-setup for THIS repo (the ai-template meta-repo) — the concrete dogfood of
# the onboarding ladder's dev-setup rung (project-trajectory/PROCESS.md §7).
#
# The kit ships project-trajectory/scripts/dev-setup.template.{sh,ps1} with EMPTY
# install slots for downstream repos to fill. This is that template *filled in*
# for the meta-repo's own stack, so the kit provisions itself: Python 3.11+, ruff
# (format), pytest + pytest-cov (the self-test suite and the harness's coverage
# step), pytest-xdist (`-n auto` parallel execution — the declared test command,
# WI-075), an offline Mermaid renderer for the generated diagrams, and the two
# agent CLIs the unattended layer routes through — claude + codex
# (docs/agents.csv pair rows; preflight-enforced at agent-resume boot, WI-109;
# codex replaced opencode at the WI-160 provider-CLI swap, 2026-07-14b).
# Consent-first: the default only reports; --install acts.
#
# Usage:  sh scripts/dev-setup.sh [--check | --install | --for-run [--python <interpreter>]]
#   --check    (default) report what's present; install nothing.
#   --for-run  what a bare root `run` calls first (WI-834): the --check
#              report, then, at an interactive terminal only, the runtime,
#              the agent CLIs and the retained adjudicator's token step, each
#              offered consent-first. --python is the interpreter run.sh
#              resolved and will run its menu on (omitted when it resolved
#              none); the report describes that interpreter only. Exits 0
#              when it satisfies the 3.11 floor, 1 with the step to take when
#              not (a runtime installed here counts from the next run).
#   --install  create ./.venv (ruff + pytest + pytest-cov + pytest-xdist, asks first) AND wire
#              the pre-commit process floor (core.hooksPath=.githooks; local +
#              reversible). Then OFFERS the agent CLIs (claude, codex) — each
#              its own [y/N] (WI-112): most users want the agentic workflow, but
#              both are deferrable for someone driving sessions with their own
#              tools or an IDE extension. Last it offers the coordinator
#              hooks' machine-local opt-in (WI-880).
#
# Windows contributors: use scripts/dev-setup.ps1.
set -eu
cd "$(dirname "$0")/.."  # scripts/ -> the repo root (like the scaffolded layout)

MODE="check"
RUN_PYTHON="" # --for-run only: the interpreter run.sh resolved
case "${1:-}" in
  --install) MODE="install" ;;
  --for-run)
    MODE="run"
    case "${2:-}" in
      --python) RUN_PYTHON="${3:-}" ;;
      "") ;;
      *) echo "Unknown option: $2" >&2; exit 2 ;;
    esac
    ;;
  --check|"") MODE="check" ;;
  -h|--help) sed -n '2,24p' "$0"; exit 0 ;;
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
python_311() {
  real "$1" &&
    "$1" -c 'import sys; raise SystemExit(sys.version_info < (3, 11))' \
      >/dev/null 2>&1
}
# A consent prompt needs a terminal: never one on piped or closed input, so a
# prompt never consumes input meant for the run menu.
interactive() { [ -t 0 ] && [ -z "${CI:-}" ]; }
report() { # <label> <present:0/1> <hint>
  if [ "$2" -eq 1 ]; then echo "  [ok]      $1"; else echo "  [missing] $1  — $3"; fi
}
offer_cli() { # <cmd> <npm package> <post-install sign-in hint>  (--install helper, WI-112)
  # One consented offer per agent CLI — never implicit. `read` guarded so a
  # non-interactive run (stdin closed) declines gracefully instead of dying.
  have "$1" && return 0
  if ! have npm; then
    echo "  [skip] $1 — npm not found; install Node.js first, or install $1 your own way."
    return 0
  fi
  printf 'Install the %s CLI now (npm install -g %s)? [y/N] ' "$1" "$2"
  read -r ans || ans=""
  case "$ans" in
    [Yy]*)
      if npm install -g "$2" && have "$1"; then
        echo "  [ok] $1 installed — $3"
      else
        echo "  [warn] $1 is still not on PATH — check the npm global bin dir is on PATH, then: $3"
      fi
      ;;
    *) echo "  Skipped $1 — fine if you use your own tools or an IDE extension." ;;
  esac
}
offer_python() { # (WI-302) one consented offer of a 3.11+ RUNTIME — and only
  # through a provisioner the developer ALREADY installed. Returns 1 when none
  # is present, so the caller falls through to the printed hint.
  #
  # The `offer_cli` pattern above, held to a stricter line on purpose. That one
  # requires npm to exist and never bootstraps it; the same rule matters more
  # here, because a language runtime is not a leaf tool — a wrong one shadows the
  # system interpreter and breaks things well outside this repo. And this script
  # SHIPS (dev-setup.template.sh): curl|sh-ing a third-party installer from a
  # setup script would push a supply-chain surface onto every adopting repo that
  # never chose it. Borrow trust the developer already extended; never manufacture
  # it on their behalf.
  if have uv; then pname="uv"; pcmd="uv python install 3.13"
  elif have pyenv; then pname="pyenv"; pcmd="pyenv install -s 3.13"
  elif have brew; then pname="Homebrew"; pcmd="brew install python@3.13"
  else return 1
  fi
  printf 'No Python 3.11+ found, but %s is installed. Run `%s` now? [y/N] ' \
    "$pname" "$pcmd"
  read -r ans || ans=""
  case "$ans" in
    [Yy]*)
      # Unquoted on purpose: $pcmd is a multi-word command to be word-split.
      if $pcmd; then
        echo "  [ok] $pname finished — re-checking for a floor-satisfying interpreter."
      else
        echo "  [warn] $pname could not install it — install Python 3.11+ your own way." >&2
      fi
      ;;
    *) echo "  Skipped — install Python 3.11+ your own way, then rerun --install." ;;
  esac
  return 0
}

# Prefer the project venv --install creates, so the report reflects what the
# harness will actually import; fall back to the ambient interpreter.
# WI-274c: after the bare candidates, try version-pinned python3.13/3.12/3.11.
# A stale sub-3.11 .venv active on PATH otherwise shadows every bare python3,
# hiding an installed 3.11+ from the recreate offer (the 2026-07-23 repro).
# Each candidate is still floor-checked by python_311.
# The interpreters searched for a runtime after the venv, in order; run.sh
# probes this same list (WI-834; pinned by tests/test_run_devsetup.py), so a
# check that finds a runtime means run resolves one too.
PY_CANDIDATES="python3 python python3.13 python3.12 python3.11"
discover_py() { # sets PY to a floor-satisfying interpreter, or "" (WI-302: a
  # function so --install can RE-run discovery after a consented provisioner
  # install, instead of telling the user to start over.) A bare run's check
  # (WI-834) takes only the interpreter run.sh handed in, the one its menu
  # runs on, so no search here can vouch for another.
  if [ "$MODE" = "run" ]; then
    PY=""
    [ -n "$RUN_PYTHON" ] && python_311 "$RUN_PYTHON" && PY="$RUN_PYTHON"
    [ -n "$PY" ]
    return
  fi
  if [ -x .venv/bin/python ] && python_311 .venv/bin/python; then
    PY=.venv/bin/python
    return 0
  fi
  PY=""
  for cand in $PY_CANDIDATES; do
    if python_311 "$cand"; then PY="$cand"; return 0; fi
  done
  return 1
}
discover_py || true
# WI-302: a remedy must be able to SATISFY the floor it is quoted against. The
# old hint sent macOS users to `xcode-select --install` / dev-setup.command, but
# the Command Line Tools ship Python 3.9 on current macOS — BELOW this very
# line's floor — so following it landed back here unchanged, with no exit from
# the loop. CLT is still what makes /usr/bin/{python3,git} real (see `real()`);
# it simply is not a source of 3.11+. Name provisioners that actually are.
case "$(uname 2>/dev/null || echo unknown)" in
  Darwin)
    PY_HINT="install Python 3.11+ — e.g. 'uv python install 3.13', 'brew install python@3.13', or the python.org macOS installer. NOT xcode-select / Command Line Tools: those ship Python 3.9, below this floor."
    ;;
  *)
    PY_HINT="install Python 3.11+ — e.g. 'uv python install 3.13', your distro's python3.13 package, or the python.org installer"
    ;;
esac
echo "dev-setup (ai-template meta-repo). Run tests with: python -m pytest -q"
echo
report "runtime (python3)" "$([ -n "$PY" ] && echo 1 || echo 0)" "$PY_HINT"
# WI-274b: name a stale .venv explicitly. The report above prefers ./.venv when
# supported, else silently describes the ambient interpreter it fell back to —
# so without this a contributor sees only "[missing] runtime" and never learns
# the .venv shadowing their PATH is the sub-floor culprit.
if [ -d .venv ] && { [ ! -x .venv/bin/python ] || ! python_311 .venv/bin/python; }; then
  vv=$(.venv/bin/python -c 'import sys;sys.stdout.write(".".join(map(str,sys.version_info[:3])))' 2>/dev/null || true)
  if [ -n "$vv" ]; then
    echo "  [stale]   .venv is Python $vv — below the 3.11 floor; rerun --install to recreate it"
  else
    echo "  [stale]   .venv is unusable (no working 3.11+ interpreter) — rerun --install to recreate it"
  fi
fi
report "git"               "$(real git && echo 1 || echo 0)" "install git (macOS: xcode-select --install)"
report "ruff (format/lint)" "$([ -n "$PY" ] && "$PY" -c 'import importlib.util,sys; sys.exit(0 if importlib.util.find_spec("ruff") else 1)' 2>/dev/null && echo 1 || echo 0)" "pip install ruff (or run --install)"
report "pytest (self-tests)" "$([ -n "$PY" ] && "$PY" -c 'import importlib.util,sys; sys.exit(0 if importlib.util.find_spec("pytest") else 1)' 2>/dev/null && echo 1 || echo 0)" "pip install pytest (or run --install)"
report "pytest-cov (harness coverage step)" "$([ -n "$PY" ] && "$PY" -c 'import importlib.util,sys; sys.exit(0 if importlib.util.find_spec("pytest_cov") else 1)' 2>/dev/null && echo 1 || echo 0)" "pip install pytest-cov (or run --install)"
report "pytest-xdist (parallel -n auto)" "$([ -n "$PY" ] && "$PY" -c 'import importlib.util,sys; sys.exit(0 if importlib.util.find_spec("xdist") else 1)' 2>/dev/null && echo 1 || echo 0)" "pip install pytest-xdist (or run --install)"
# The agent CLIs docs/agents.csv routes through (WI-109) — required for the
# unattended layer (agent_loop preflight refuses to boot without an enabled
# row's CLI); everything above still works without them.
report "claude CLI (agent sessions: agent-resume.*)" "$(have claude && echo 1 || echo 0)" "npm install -g @anthropic-ai/claude-code; then run claude once to sign in"
report "codex CLI (the OPENAI-* rows in docs/agents.csv)" "$(have codex && echo 1 || echo 0)" "npm install -g @openai/codex; then: codex login"
report "offline Mermaid renderer" "$( { have code || have mmdc || have npx; } && echo 1 || echo 0)" "VS Code + a Mermaid preview extension, or: npm i -g @mermaid-js/mermaid-cli"
# Optional, dev-only (WI-189): the dashboard render-critique loop. NOT installed
# by --install and NOT shipped downstream (the kit's install-nothing posture
# governs project-trajectory/scripts, never this meta tool). See
# scripts/dashboard-shots/README.md + the render-dashboard-critique skill.
report "dashboard shots (optional, meta-only)" "$( [ -d scripts/dashboard-shots/node_modules/playwright ] && echo 1 || echo 0)" "cd scripts/dashboard-shots && npm ci && npx playwright install chromium (pinned; dev-only)"
report "pre-commit floor (core.hooksPath)" "$([ "$(git config --get core.hooksPath 2>/dev/null)" = ".githooks" ] && echo 1 || echo 0)" "run --install, or: git config core.hooksPath .githooks"
# The retained adjudicator's sign-in (WI-834): with [adjudicator] retention on, a
# retained Claude launch runs under its dedicated home on the long-lived token
# in the file AGENT_CLAUDE_TOKEN_FILE names (WI-846), refused before launch
# without one. Read through the kit's own readers (the retention dial and the
# sign-in probe) when a runtime exists, else unknown; reported only while
# retention is on. The token is never read here.
SIGNIN="unknown"
if [ -n "$PY" ]; then
  SIGNIN=$("$PY" project-trajectory/scripts/coordinator_adjudicate.py signin --retained --root . 2>/dev/null |
    sed -n 's/^signin \[ANTHROPIC\]: //p')
  [ -n "$SIGNIN" ] || SIGNIN="unknown"
fi
case "$SIGNIN" in
  off) ;;
  signed-in) echo "  [ok]      retained adjudicator sign-in (AGENT_CLAUDE_TOKEN_FILE)" ;;
  missing) echo "  [missing] retained adjudicator sign-in  — run --install (or a bare run) for the one-time 'claude setup-token' step, keep the token in a file outside the repository, and set AGENT_CLAUDE_TOKEN_FILE to that file" ;;
  *) echo "  [unknown] retained adjudicator sign-in  — could not be read (it needs a Python 3.11+ runtime to read the retention dial and the token)" ;;
esac
# The coordinator's Claude Code hooks (WI-880, owner ruling 2026-10-10): this
# repository commits none. The guard's machine-local opt-in merges the hook
# groups of the inert .claude/settings.json.example into
# .claude/settings.local.json, each bound to the interpreter that runs it; a
# machine that has not opted in runs no guard hooks. Read through the guard's
# own report when a runtime exists.
HOOKS_EXAMPLE=.claude/settings.json.example
HOOKS="none"
if [ -n "$PY" ] && [ -f "$HOOKS_EXAMPLE" ]; then
  HOOKS=$("$PY" project-trajectory/scripts/coordinator_guard.py --root . hooks --example "$HOOKS_EXAMPLE" 2>/dev/null) || HOOKS="none"
fi
case "$HOOKS" in
  on) echo "  [ok]      coordinator Claude Code hooks (.claude/settings.local.json)" ;;
  off) echo "  [note]    coordinator Claude Code hooks are off — the machine-local opt-in, offered by --install and a bare run" ;;
esac
# Switching them on, consented: the opt-in runs on this script's runtime, the
# floor-resolved interpreter its hooks are then bound to.
offer_hooks() {
  [ "$HOOKS" = "off" ] || return 0
  printf "Switch on the coordinator's Claude Code hooks (merged into the machine-local .claude/settings.local.json, keeping any hooks already there)? [y/N] "
  read -r ans || ans=""
  case "$ans" in
    [Yy]*)
      if "$PY" project-trajectory/scripts/coordinator_guard.py --root . hooks --example "$HOOKS_EXAMPLE" --enable >/dev/null; then
        echo "  Switched on the coordinator hooks in .claude/settings.local.json."
      else
        echo "  [warn] the opt-in could not write .claude/settings.local.json; the hooks stay off."
      fi
      ;;
    *) echo "  Skipped the coordinator hooks; nothing was changed." ;;
  esac
}

# The one-time long-lived token step (WI-846's), consented; shown only while
# retention is on and the token is missing. Nothing here reads the token.
offer_signin() {
  { [ "$SIGNIN" = "missing" ] && have claude; } || return 0
  echo
  echo "The retained adjudicator runs Claude under its own dedicated home, which signs"
  echo "in with a long-lived token. The one-time 'claude setup-token' step mints that"
  echo "token; you keep it in a file outside this repository, at the location you set"
  echo "AGENT_CLAUDE_TOKEN_FILE to. Your normal 'claude' login and every other"
  echo "repository are left alone, and declining changes no configuration or credential."
  printf "Run 'claude setup-token' now? [y/N] "
  read -r ans || ans=""
  case "$ans" in
    [Yy]*)
      claude setup-token || echo "  [warn] claude setup-token did not finish; rerun it when ready."
      echo "  Keep the printed token in a file outside this repository, then set"
      echo "  AGENT_CLAUDE_TOKEN_FILE to that file's path (e.g. in your shell profile)."
      ;;
    *) echo "  Skipped the token step; nothing was changed. A retained adjudication is refused until it is done." ;;
  esac
}

# Ambient-interpreter debris warning (WI-175 / WI-105). The report above describes
# ./.venv (PY prefers it), but a bare `python -m pytest` resolves via PATH — which
# may be a DIFFERENT interpreter carrying a pre-5.0 pytest-cov. That racing version
# loses subprocess data from the parallel combine and strands thousands of
# .coverage.* files at the repo root. Warn (never fail) when the PATH python is not
# the venv and carries the racing version; point at ./.venv. The `[0-4].*` glob
# matches only majors 0–4 (5.0.0 / 10.x never match), and an empty covver (no
# pytest-cov on PATH) matches nothing — no coverage run, no debris to warn about.
AMBIENT=""
for cand in python3 python; do
  if real "$cand"; then AMBIENT=$(command -v "$cand"); break; fi
done
if [ -n "$AMBIENT" ] && [ -x .venv/bin/python ] \
   && [ "$AMBIENT" != "$(command -v .venv/bin/python 2>/dev/null)" ]; then
  covver=$("$AMBIENT" -c 'import pytest_cov,sys; sys.stdout.write(pytest_cov.__version__)' 2>/dev/null || true)
  case "$covver" in
    [0-4].*)
      echo
      echo "  [warn] PATH python ($AMBIENT) carries pytest-cov $covver — this pre-5.0"
      echo "         version races the parallel coverage combine and strands .coverage.*"
      echo "         debris at the repo root (WI-105). Run the suite through ./.venv"
      echo "         (.venv/bin/python -m pytest), or activate it, so the pinned tools run."
      ;;
  esac
fi

# --- --for-run: the check above, then offers at a terminal only -------------
if [ "$MODE" = "run" ]; then
  echo
  if interactive; then
    [ -n "$PY" ] || offer_python || true  # installed now, it counts from the next run
    offer_cli claude "@anthropic-ai/claude-code" "run claude once to sign in (or: claude setup-token)"
    offer_cli codex "@openai/codex" "sign in with: codex login"
    offer_signin
    offer_hooks
  else
    echo "No interactive terminal: nothing is offered (run sh scripts/dev-setup.sh --install at a terminal)."
  fi
  [ -n "$PY" ] && exit 0
  echo
  echo "The runtime is still missing — the step to take: $PY_HINT, or put an installed one first on PATH, then run again. run checked: .venv/bin/python, .venv/Scripts/python.exe, $PY_CANDIDATES"
  exit 1
fi

if [ "$MODE" = "check" ]; then
  echo
  if ! have claude || ! have codex; then
    echo "note: agent CLI(s) missing above — agent-resume.* cannot boot the unattended"
    echo "loop while docs/agents-enabled lists their rows (preflight refuses, naming"
    echo "each gap + hint). --install offers each CLI, individually consented;"
    echo "skipping is fine with your own tools / an IDE extension."
    echo
  fi
  echo "To install the Python dev tools into ./.venv (and be offered the agent CLIs): sh scripts/dev-setup.sh --install"
  exit 0
fi

# --- --install: consent-first venv + dev tools -------------------------------
if [ -z "$PY" ]; then
  # WI-302: before the fail-closed exit, offer the runtime through a provisioner
  # already on this machine, then RE-discover — so a developer who has uv/pyenv/
  # brew is one consented [y/N] from a working environment instead of a dead end.
  offer_python || true
  discover_py || true
fi
[ -n "$PY" ] || {
  echo "Python 3.11+ not found on PATH; install a supported interpreter first." >&2
  echo "  $PY_HINT" >&2
  echo "  (a managed interpreter may need a new shell, or its bin dir on PATH)" >&2
  exit 1
}
# WI-274a: a sub-3.11 (or broken) ./.venv gets a CONSENTED recreate at the
# floor, not the old fail-closed "move or remove" dead end. $PY is the discovered
# 3.11+ interpreter (guaranteed non-empty by the check above). Decline keeps
# today's fail-closed exit; a non-interactive `read` returns empty -> declines
# gracefully (the offer_cli pattern), so an unattended --install stays safe.
RECREATE=0
if [ -d .venv ] && { [ ! -x .venv/bin/python ] || ! python_311 .venv/bin/python; }; then
  vv=$(.venv/bin/python -c 'import sys;sys.stdout.write(".".join(map(str,sys.version_info[:3])))' 2>/dev/null || true)
  dv=$("$PY" -c 'import sys;sys.stdout.write(".".join(map(str,sys.version_info[:3])))' 2>/dev/null || echo "3.11+")
  if [ -n "$vv" ]; then
    printf 'Existing ./.venv is Python %s — below the 3.11 floor. Recreate it with %s (Python %s)? [y/N] ' "$vv" "$PY" "$dv"
  else
    printf 'Existing ./.venv is unusable (no working interpreter). Recreate it with %s (Python %s)? [y/N] ' "$PY" "$dv"
  fi
  read -r ans || ans=""
  case "$ans" in
    [Yy]*)
      rm -rf .venv
      echo "Removed the stale ./.venv."
      RECREATE=1
      ;;
    *)
      echo "Existing ./.venv is below the 3.11 floor or has no working interpreter; recreate declined — move or remove that environment, then rerun --install." >&2
      exit 1
      ;;
  esac
fi

# Wire the agent-neutral pre-commit floor (the process-floor rung setup.sh wires
# downstream; this meta-repo folds it into dev-setup — IMPROVEMENT_PLAN WI-1.42).
# Independent of the venv install below, so it happens even if that's declined.
# Local + reversible (git config --unset core.hooksPath); idempotent.
if [ -f .githooks/pre-commit ] && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git config core.hooksPath .githooks
  echo "Enabled pre-commit floor (core.hooksPath=.githooks; undo: git config --unset core.hooksPath)."
fi
# Delta-aware venv section (WI-111): --install must never initiate an
# unnecessary install. When ./.venv already imports all four dev tools, skip
# this whole section — no prompt AND no unconditional `pip install --upgrade
# pip`. (The floor wiring above still ran: local git config, idempotent, not
# an install.) The agent-CLI offers below still run either way (WI-112).
if [ -x .venv/bin/python ] && .venv/bin/python -c 'import importlib.util,sys; sys.exit(0 if sys.version_info >= (3,11) and all(importlib.util.find_spec(m) for m in ("ruff","pytest","pytest_cov","xdist")) else 1)' 2>/dev/null; then
  echo "All dev tools already present in ./.venv — nothing to install."
else
  if [ "$RECREATE" = "1" ]; then
    # Consent was already given at the recreate prompt above — go straight to
    # the fresh create+install, no second [y/N].
    ans="y"
  else
    echo
    printf 'Create ./.venv and install ruff + pytest + pytest-cov + pytest-xdist into it? [y/N] '
    read -r ans || ans=""
  fi
  case "$ans" in
    [Yy]*)
      [ -d .venv ] || "$PY" -m venv .venv
      # shellcheck disable=SC1091
      . .venv/bin/activate
      python -m pip install --upgrade pip
      # Pinned toolchain (requirements-dev.txt, WI-104) — same versions CI runs.
      python -m pip install -r requirements-dev.txt
      echo "Python dev tools installed. Run the self-tests with: python -m pytest -q"
      ;;
    *) echo "Skipped the Python dev-tools install." ;;
  esac
fi

# Agent CLIs (WI-112) — individually consented, never implicit: most users
# want the agentic workflow (agent-resume.*) easily accessible, but each CLI
# is deferrable for someone driving sessions with their own tools or an IDE
# extension.
echo
echo "Agent CLIs (docs/agents.csv routes unattended sessions through these):"
offer_cli claude "@anthropic-ai/claude-code" "run claude once to sign in (or: claude setup-token)"
offer_cli codex "@openai/codex" "sign in with: codex login"
offer_signin
offer_hooks
if ! have claude || ! have codex; then
  echo
  echo "NOTE: docs/agents-enabled currently routes sessions through BOTH claude and"
  echo "codex — with either CLI missing, agent-resume.* cannot boot the walk-away"
  echo "loop (its preflight refuses, naming each gap and its install/sign-in hint)."
  echo "Skipping is fine if you drive sessions with your own tools or an IDE"
  echo "extension; then trim docs/agents-enabled to the rows whose CLIs you keep."
fi
