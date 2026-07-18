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
# Usage:  sh dev-setup.sh [--check|--baseline|--full] [--profile <role>]
#   --check     (default) detect + report what's present; install nothing.
#   --baseline  ensure runtime + git + an offline Mermaid renderer, plus the
#               selected role(s)' tools. Asks before each install.
#   --full      baseline + an IDE and editor extensions. Opt-in, and skipped when
#               headless / non-interactive (no TTY or $CI set).
#   --profile <role>  install only that role's tools (plus the shared baseline) —
#               the opt-down for a contributor who wants just their slice.
#               DEFAULT (no --profile): every declared role. Roles: see ROLES below.
#
# Windows contributors: use scripts/dev-setup.ps1.
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
while [ $# -gt 0 ]; do
  case "$1" in
    --check)     TIER="check" ;;
    --baseline)  TIER="baseline" ;;
    --full)      TIER="full" ;;
    --profile)   shift; PROFILE="${1:-}" ;;
    --profile=*) PROFILE="${1#*=}" ;;
    -h|--help)   sed -n '2,26p' "$0"; exit 0 ;;
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
if real python3 || real python; then RUNTIME=1; else RUNTIME=0; fi
report "runtime (python3)"          "$RUNTIME"                        "install a Python 3.8+ runtime (fresh macOS: double-click scripts/dev-setup.command, or xcode-select --install)"
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

# --- --baseline / --full: consent-first installs -----------------------------
say
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
say "./scripts/check.sh --gate G3 to run the gates."
