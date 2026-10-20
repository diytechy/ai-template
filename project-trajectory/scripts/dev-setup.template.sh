#!/usr/bin/env sh
# dev-setup (Linux/macOS) — provision the *developer workstation* rung of the
# onboarding ladder (process.md §7):
#
#     Stage 0  ->  dev-setup  ->  setup  ->  check
#                  (this)         deps       gates
#
# This readies what a *human* needs to view, render, edit, and run this repo —
# a runtime, git, and an OFFLINE Markdown+Mermaid renderer — which is distinct
# from `setup.sh` (that installs the *product* toolchain: venv, ruff, pytest).
# Separating them is the point: "no required tools" was always a claim about the
# stdlib *process* checks, never about what a person needs at a workstation.
#
# Consent-first and readable by design: the DEFAULT tier only detects and
# reports; it installs nothing. Nothing here pipes a remote script to a shell.
#
# Usage:  sh dev-setup.sh [--check|--baseline|--full|--for-run [--python <interpreter>]] [--profile <role>]
#   --check     (default) detect + report what's present; install nothing.
#   --for-run   what a bare `run` calls first: the --check report, then, with
#               an interactive terminal only, each missing piece offered
#               consent-first (nothing offered without one). --python is the
#               interpreter the launcher resolved and will run its menu on
#               (omitted when it resolved none); the runtime reported is that
#               interpreter only, never one found here. Exits 0 when it
#               satisfies the 3.11 floor, 1 with the step to take when not.
#   --baseline  ensure runtime + git + an offline Mermaid renderer, plus the
#               selected role(s)' tools. Asks before each install.
#   --full      baseline + an IDE and editor extensions. Opt-in, and skipped when
#               headless / non-interactive (no TTY or $CI set).
#   --profile <role>  install only that role's tools (plus the shared baseline) —
#               the opt-down for a contributor who wants just their slice.
#               DEFAULT (no --profile): every declared role. Roles: see ROLES below.
#
# Windows contributors: use scripts/dev-setup.ps1.
# Contracts: IF-292, IF-293 — the interface seams this script declares (process.md §8;
# rows of record in docs/requirements/interfaces.toml).
#
# Contract IF-292: a bare run invokes this script as --for-run from the repository
#     root once before its menu, handing it as --python the interpreter it
#     resolved for the menu (omitted when it resolved none).
# Contract IF-293: exit 0 says that handed interpreter satisfies the runtime
#     floor; nonzero leaves the menu unopened after setup guidance.
set -eu

# =================== EDIT FOR YOUR STACK / ROLES ===========================
# The shared BASELINE (runtime, git, offline renderer) is provisioned for every
# profile — fill its install slots. Then declare one ROLE per contributor kind
# (code, asset design, CAD, marketing, …); each adds its own tools on top. The
# DEFAULT installs every role; `--profile <role>` narrows to one. Role names
# must be [a-z0-9_]. Leave any *_INSTALL empty to skip its install (detection
# still reports). Debian/Ubuntu shown for reference — swap apt-get for
# brew/dnf/pacman as needed.
#
#   RUNTIME_INSTALL="sudo apt-get install -y python3"
#   RENDERER_INSTALL="npm install -g @mermaid-js/mermaid-cli"   # or install VS Code + a Mermaid preview extension
#   IDE_INSTALL="sudo snap install code --classic"
RUNTIME_INSTALL=""
RENDERER_INSTALL=""
IDE_INSTALL=""

# Declared roles (space-separated). For each <role>, set:
#   <role>_CMDS     detection commands; if ANY is on PATH the role reads present
#   <role>_INSTALL  the install command (empty = nothing to install here)
ROLES="code design"

# code — a code contributor. The linter/test toolchain is setup.sh's job, so
# this usually stays empty (baseline runtime + git is what they need here).
code_CMDS=""
code_INSTALL=""

# design — a non-code asset designer (art/UI). Example: an SVG editor.
design_CMDS="inkscape"
design_INSTALL=""   # e.g. "sudo apt-get install -y inkscape"
# ===========================================================================

TIER="check"
PROFILE=""   # empty = all declared roles
RUN_PYTHON="" # --for-run only: the interpreter the launcher resolved
while [ $# -gt 0 ]; do
  case "$1" in
    --check)     TIER="check" ;;
    --baseline)  TIER="baseline" ;;
    --full)      TIER="full" ;;
    --for-run)   TIER="run" ;;
    --python)    shift; RUN_PYTHON="${1:-}" ;;
    --python=*)  RUN_PYTHON="${1#*=}" ;;
    --profile)   shift; PROFILE="${1:-}" ;;
    --profile=*) PROFILE="${1#*=}" ;;
    -h|--help)   sed -n '2,33p' "$0"; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

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
say()  { printf '%s\n' "$*"; }
# Indirect lookup of a per-role variable (<role>_CMDS / <role>_INSTALL); the
# `:-` default keeps `set -u` happy when a slot is left unset.
role_val() { eval "printf '%s' \"\${$1_$2:-}\""; }

# Resolve which roles this run acts on: the one named by --profile, or all.
if [ -n "$PROFILE" ]; then
  ok=0
  for r in $ROLES; do [ "$r" = "$PROFILE" ] && ok=1; done
  if [ "$ok" -eq 0 ]; then
    echo "Unknown --profile '$PROFILE'. Declared roles: $ROLES" >&2
    exit 2
  fi
  SELECTED="$PROFILE"
else
  SELECTED="$ROLES"
fi

# Interactive only when there is a TTY and we are not in CI — so --full never
# blocks an automated run waiting on a prompt.
interactive() { [ -t 0 ] && [ -z "${CI:-}" ]; }

missing=0
report() { # <label> <present:0/1> <hint>
  if [ "$2" -eq 1 ]; then
    say "  [ok]      $1"
  else
    say "  [missing] $1  — $3"
    missing=$((missing + 1))
  fi
}

# Consent-first install: show the command, ask (default no), run it. A blank
# command is treated as "not configured for this stack" and skipped.
maybe_install() { # <label> <install-cmd>
  if [ -z "$2" ]; then
    say "  - $1: no install command configured (see EDIT FOR YOUR STACK); skipping."
    return 0
  fi
  if ! interactive; then
    say "  - $1: non-interactive; skipping install ($2)"
    return 0
  fi
  printf '  Install %s via "%s"? [y/N] ' "$1" "$2"
  read -r ans
  case "$ans" in [Yy]*) sh -c "$2" ;; *) say "  - skipped $1" ;; esac
}

renderer_present() { have code || have mmdc || have npx; }
# A role reads present when any of its detection commands is on PATH, or when it
# declares none (e.g. `code`, whose toolchain is setup.sh's job).
role_present() { # <role>
  cmds=$(role_val "$1" CMDS)
  [ -z "$cmds" ] && return 0
  for c in $cmds; do have "$c" && return 0; done
  return 1
}

say "dev-setup — profile=${PROFILE:-all} tier=$TIER"
say "Developer workstation (process.md §7). Product deps are scripts/setup.sh."
say

# --- Detect + report (every tier does this first) ----------------------------
# PY_CANDIDATES: the interpreters searched, in order. Keep run.sh's list and
# the git pre-commit hook's the same (after their .venv entries), so a check
# that finds a runtime means run and the hook resolve one too.
PY_CANDIDATES="python3 python"
# PYBIN: the interpreter the kit's own readers below run on; RUNTIME=1 when
# there is one. For a bare run (--for-run) it is the interpreter the launcher
# handed in, if that satisfies the floor: the one the menu runs on, so no
# search here can vouch for a different one. Otherwise, the first
# floor-satisfying candidate.
detect_runtime() {
  PYBIN=""
  if [ "$TIER" = "run" ]; then
    if [ -n "$RUN_PYTHON" ] && python_311 "$RUN_PYTHON"; then PYBIN="$RUN_PYTHON"; fi
  else
    for cand in $PY_CANDIDATES; do
      if python_311 "$cand"; then PYBIN="$cand"; break; fi
    done
  fi
  if [ -n "$PYBIN" ]; then RUNTIME=1; else RUNTIME=0; fi
}
detect_runtime
# A remedy must be able to SATISFY the floor it is quoted against. This line used
# to send macOS users to `xcode-select --install`, but the Command Line Tools ship
# Python 3.9 — below this floor — so following it landed back here unchanged, with
# no way out of the loop. CLT is still what makes /usr/bin/{python3,git} real (see
# `real()` above); it is simply not a source of 3.11+.
case "$(uname 2>/dev/null || echo unknown)" in
  Darwin) PY_HINT="install a Python 3.11+ runtime — e.g. 'uv python install 3.13', 'brew install python@3.13', or the python.org macOS installer. NOT xcode-select / Command Line Tools: those ship Python 3.9, below this floor." ;;
  *)      PY_HINT="install a Python 3.11+ runtime — e.g. 'uv python install 3.13', your distro's python3.13 package, or the python.org installer" ;;
esac
report "runtime (python3)"          "$RUNTIME"                        "$PY_HINT"
report "git"                        "$(real git && echo 1 || echo 0)" "install git — needed to make reviewable changes (macOS: xcode-select --install)"
report "offline Markdown+Mermaid renderer" \
       "$(renderer_present && echo 1 || echo 0)" \
       "VS Code + a Mermaid preview extension, or: npm i -g @mermaid-js/mermaid-cli"
report "pre-commit floor (core.hooksPath)" \
       "$([ "$(git config --get core.hooksPath 2>/dev/null)" = ".githooks" ] && echo 1 || echo 0)" \
       "run --baseline (or: git config core.hooksPath .githooks)"

for r in $SELECTED; do
  report "role: $r" "$(role_present "$r" && echo 1 || echo 0)" \
    "fill ${r}_CMDS/${r}_INSTALL in the EDIT block for this role's tools"
done

if [ "$TIER" = "full" ]; then
  report "IDE (VS Code 'code')" "$(have code && echo 1 || echo 0)" "install an editor; run again with --full to add extensions"
fi

# The retained adjudicator's sign-in (WI-834, WI-798): with [adjudicator]
# retention on, the adjudicator's entry runs under its declared account: a token
# account authenticates with the long-lived token in the file its
# token_file_variable names (WI-846), a login account with its own home. Read
# through the kit's own readers (the retention dial and the sign-in probe,
# coordinator_adjudicate.py signin --retained, which prints the account, its
# kind and its reading) when a Python runtime exists, else unknown; reported
# only while retention is on. dev-setup never reads, stores or prints the token.
SIGNIN="unknown"
SIGNIN_ACCOUNT="" SIGNIN_KIND="" SIGNIN_VAR="" SIGNIN_HINT="" SIGNIN_UNVERIFIED="" SIGNIN_WHY=""
if [ -n "$PYBIN" ]; then
  SIGNIN_OUT=$("$PYBIN" scripts/coordinator_adjudicate.py signin --retained --root . 2>/dev/null) || SIGNIN_OUT=""
  SIGNIN_ACCOUNT=$(printf '%s\n' "$SIGNIN_OUT" | sed -n 's/^signin \[\([^]]*\)\] [a-z]*: [a-z-]*.*$/\1/p' | head -n 1)
  SIGNIN_KIND=$(printf '%s\n' "$SIGNIN_OUT" | sed -n 's/^signin \[[^]]*\] \([a-z]*\): [a-z-]*.*$/\1/p' | head -n 1)
  SIGNIN=$(printf '%s\n' "$SIGNIN_OUT" | sed -n 's/^signin \[[^]]*\] [a-z]*: \([a-z-]*\).*$/\1/p' | head -n 1)
  SIGNIN_VAR=$(printf '%s\n' "$SIGNIN_OUT" | sed -n 's/^signin \[[^]]*\]: token_file_variable //p' | head -n 1)
  SIGNIN_HINT=$(printf '%s\n' "$SIGNIN_OUT" | sed -n 's/^signin \[[^]]*\]: provision it yourself: //p' | head -n 1)
  SIGNIN_WHY=$(printf '%s\n' "$SIGNIN_OUT" | sed -n 's/^signin \[[^]]*\] unresolved: [a-z-]* (\(.*\))$/\1/p' | head -n 1)
  case "$SIGNIN_OUT" in *"(unverified)"*) SIGNIN_UNVERIFIED=1 ;; esac
  [ -n "$SIGNIN" ] || SIGNIN="unknown"
fi
case "$SIGNIN_KIND:$SIGNIN" in
  *:off) ;;
  ambient:*) say "  [ok]      retained adjudicator sign-in (its entry runs on your own login; no account declared)" ;;
  token:signed-in) say "  [ok]      retained adjudicator sign-in (account $SIGNIN_ACCOUNT, its token file)" ;;
  login:signed-in)
    if [ -n "$SIGNIN_UNVERIFIED" ]; then
      say "  [ok]      retained adjudicator sign-in (account $SIGNIN_ACCOUNT, its own home) — UNVERIFIED: its login-isolation check has not passed"
    else
      say "  [ok]      retained adjudicator sign-in (account $SIGNIN_ACCOUNT, its own home)"
    fi
    ;;
  token:missing)
    say "  [missing] retained adjudicator sign-in (account $SIGNIN_ACCOUNT) — run 'claude setup-token' once (offered by --baseline and a bare run), keep the token in a file outside the repository, and set ${SIGNIN_VAR:-the variable its token_file_variable names} to that file"
    missing=$((missing + 1))
    ;;
  login:missing)
    say "  [missing] retained adjudicator sign-in (account $SIGNIN_ACCOUNT) — sign it in yourself under its own home: $SIGNIN_HINT (nothing here runs it)"
    missing=$((missing + 1))
    ;;
  unresolved:*)
    say "  [missing] retained adjudicator sign-in — its entry does not resolve (${SIGNIN_WHY:-no reason given}): declare the adjudicator's account in docs/agents.toml and add its qualified entry to docs/agents-enabled, as RESYNC_PACK's accounts entry says, or run coordinator_adjudicate.py with --route <your entry>"
    missing=$((missing + 1))
    ;;
  *) say "  [unknown] retained adjudicator sign-in — could not be read (it needs a Python 3.11+ runtime to read the retention dial and the adjudicator's account)" ;;
esac

# The coordinator's Claude Code hooks: shipped inert in
# .claude/settings.json.example and written only with consent into the
# machine-local .claude/settings.local.json, each bound to the interpreter that
# runs the install (never the committed .claude/settings.json: the bound path
# is this machine's). The guard's reader prints none, absent, on or occupied;
# a reader that fails or prints nothing is reported missing, never none.
HOOKS="none"
if [ -n "$PYBIN" ] && [ -f .claude/settings.json.example ]; then
  HOOKS_STATUS=0
  HOOKS=$("$PYBIN" scripts/coordinator_guard.py --root . hooks --example .claude/settings.json.example 2>&1) || HOOKS_STATUS=$?
  case "$HOOKS_STATUS:$HOOKS" in
    0:on | 0:absent | 0:none) ;;
    *)
      HOOKS_ERR=${HOOKS:-the hooks reader printed nothing}
      HOOKS="failed"
      ;;
  esac
fi
case "$HOOKS" in
  on) say "  [ok]      coordinator Claude Code hooks (.claude/settings.local.json)" ;;
  absent) say "  [note]    coordinator Claude Code hooks are not installed — opt-in, offered by --baseline and a bare run" ;;
  failed)
    say "  [missing] coordinator Claude Code hooks: $HOOKS_ERR"
    missing=$((missing + 1))
    ;;
esac

say
if [ -d .venv ]; then
  say "Product toolchain: .venv present (run scripts/setup.sh to refresh)."
else
  say "Product toolchain: run scripts/setup.sh to create .venv + install test tools."
fi

# --- --check stops here: pure report, always green ---------------------------
if [ "$TIER" = "check" ]; then
  say
  say "$missing component(s) missing. Install them with: sh $0 --baseline"
  exit 0
fi

# The one-time long-lived token step (WI-846's, shown only while retention is on
# and a TOKEN account's token is missing; a login account is named its
# provisioning command above and offered nothing), consented. `claude
# setup-token` prints the token once; the person keeps it in a file outside the
# repository and points the account's token_file_variable at that file.
# Nothing here reads the token.
offer_signin() {
  { [ "$SIGNIN_KIND" = "token" ] && [ "$SIGNIN" = "missing" ] && have claude && interactive; } || return 0
  say
  say "The retained adjudicator runs Claude on its token account $SIGNIN_ACCOUNT, which signs"
  say "in with a long-lived token. The one-time 'claude setup-token' step mints that"
  say "token; you keep it in a file outside this repository, at the location you set"
  say "${SIGNIN_VAR:-its token_file_variable} to. Your normal 'claude' login and every other"
  say "repository are left alone, and declining changes no configuration or credential."
  printf "Run 'claude setup-token' now? [y/N] "
  read -r ans || ans=""
  case "$ans" in
    [Yy]*)
      claude setup-token || say "  [warn] claude setup-token did not finish; rerun it when ready."
      say "  Keep the printed token in a file outside this repository, then set"
      say "  ${SIGNIN_VAR:-its token_file_variable} to that file's path (e.g. in your shell profile)."
      ;;
    *) say "  - skipped the token step; nothing was changed" ;;
  esac
}

# Installing the coordinator's hooks, consented: the guard asks the question
# at this terminal and writes them only after a yes (stdout and stdin stay the
# terminal's; its stderr is kept to name a refusal).
offer_hooks() {
  { [ "$HOOKS" = "absent" ] && interactive; } || return 0
  exec 3>&1
  HOOKS_ERR=$("$PYBIN" scripts/coordinator_guard.py --root . hooks --example .claude/settings.json.example --offer 2>&1 1>&3 3>&-) || {
    exec 3>&-
    say "  [missing] coordinator Claude Code hooks: ${HOOKS_ERR:-the install failed and printed nothing}"
    return 0
  }
  exec 3>&-
  HOOKS=$("$PYBIN" scripts/coordinator_guard.py --root . hooks --example .claude/settings.json.example 2>/dev/null) || HOOKS="failed"
  [ "$HOOKS" = "on" ] && say "  Switched on the coordinator hooks in .claude/settings.local.json."
  return 0
}

# --- --baseline / --full / --for-run: consent-first offers ----------------------
say
if [ "$TIER" = "run" ] && ! interactive; then
  say "No interactive terminal: nothing is offered (run dev-setup at a terminal to install)."
else
  say "Installing the $TIER workstation (asks before each step)…"
  [ "$RUNTIME" -eq 1 ] || maybe_install "runtime" "$RUNTIME_INSTALL"
  renderer_present     || maybe_install "offline Mermaid renderer" "$RENDERER_INSTALL"
  for r in $SELECTED; do
    role_present "$r" || maybe_install "role: $r" "$(role_val "$r" INSTALL)"
  done
  if [ "$TIER" = "full" ]; then
    if interactive; then
      maybe_install "IDE" "$IDE_INSTALL"
    else
      say "  - IDE: headless/non-interactive; skipped (opt-in, --full only)."
    fi
  fi
  offer_signin
  offer_hooks
fi

# --- --for-run ends here, with its result: the runtime the menu needs --------
# Nothing more is wired unasked (the floor below is offered, not set), and the
# setup.sh chain stays with --baseline.
if [ "$TIER" = "run" ]; then
  if [ "$(git config --get core.hooksPath 2>/dev/null)" != ".githooks" ] &&
    [ -f .githooks/pre-commit ] && interactive; then
    printf 'Enable the pre-commit floor (git config core.hooksPath .githooks)? [y/N] '
    read -r ans || ans=""
    case "$ans" in [Yy]*) git config core.hooksPath .githooks ;; *) say "  - skipped the pre-commit floor" ;; esac
  fi
  [ "$RUNTIME" -eq 1 ] && exit 0
  say
  say "The runtime is still missing — the step to take: $PY_HINT, or put an installed one first on PATH, then run again. run checked: .venv/bin/python, .venv/Scripts/python.exe, $PY_CANDIDATES"
  exit 1
fi

# Wire the agent-neutral pre-commit process floor (core.hooksPath) — universal,
# zero-dependency, reversible, so every committer gets it from the rung they
# actually run. setup.sh wires it too (idempotent); doing it here means a
# contributor who onboards via dev-setup is protected without waiting to run setup
# (process.md §7). Skipped cleanly outside a git repo
# or before the hook is scaffolded.
if [ -f .githooks/pre-commit ] && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git config core.hooksPath .githooks
  say "Enabled the pre-commit process floor (core.hooksPath=.githooks; undo: git config --unset core.hooksPath)."
fi

# A code contributor needs the product toolchain too (setup.sh: venv + linters +
# tests). Offer to chain into it so onboarding is one command; a non-code role
# (e.g. an asset designer) is not asked (WI-1.42).
case " $SELECTED " in
  *" code "*)
    if interactive; then
      printf 'Run scripts/setup.sh now for the product toolchain (venv + test tools)? [y/N] '
      read -r ans
      case "$ans" in [Yy]*) sh scripts/setup.sh ;; *) say "  - skipped setup.sh (run it when ready)" ;; esac
    fi
    ;;
esac

say
say "Done. Workstation ready; the pre-commit floor is wired."
say "If you skipped it above, run scripts/setup.sh for the product toolchain, then"
say "./scripts/check.sh --stage DevStg-Impl to run the gates."
