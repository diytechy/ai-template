#!/bin/sh
# dev-setup launcher (macOS) — the double-clickable Finder wrapper for
# scripts/dev-setup.sh (the POSIX command lives once, there; edit it, not this).
#
# Beyond hopping to the repo root (so double-click works from anywhere), this
# wrapper owns the one macOS-only rung the shared script can't do for itself:
# on a fresh Mac, /usr/bin/python3 and /usr/bin/git are Command Line Tools
# *placeholders* that satisfy `command -v` but only pop Apple's installer when
# actually run — so the first double-click offers that one-time install, then
# hands off to dev-setup.sh once the real toolchain is present.
#
# Linux contributors: use scripts/dev-setup.sh.  Windows: scripts/dev-setup.ps1.
set -eu
cd "$(dirname "$0")/.."  # scripts/ -> the repo root (where dev-setup.sh runs)

say() { printf '%s\n' "$*"; }

# 1. Fresh-Mac rung: ensure the Xcode Command Line Tools (real python3 + git).
if [ "$(uname)" = "Darwin" ] && ! xcode-select -p >/dev/null 2>&1; then
  say "The Xcode Command Line Tools are not installed yet. On a fresh Mac the"
  say "preinstalled 'python3' and 'git' are placeholders that only work after"
  say "this one-time Apple download."
  say
  printf 'Request the Command Line Tools install now (opens an Apple dialog)? [Y/n] '
  read -r ok
  case "$ok" in
    [Nn]*) say "Skipped. Install later with: xcode-select --install"; exit 0 ;;
  esac
  xcode-select --install || true
  say
  say "A system dialog should have appeared — click Install and let the"
  say "download finish (a few minutes). If no dialog appeared, the install may"
  say "already be running, or run 'xcode-select --install' in Terminal."
  say
  say "When it completes, double-click this file again to continue."
  exit 0
fi

# 2. Real toolchain present — hand off to the shared POSIX script.
if [ "$#" -gt 0 ]; then exec sh scripts/dev-setup.sh "$@"; fi
sh scripts/dev-setup.sh --check
say
printf 'Run the baseline install now (asks before each step)? [y/N] '
read -r go
case "$go" in
  [Yy]*) exec sh scripts/dev-setup.sh --baseline ;;
  *) say "Done. Install later with: sh scripts/dev-setup.sh --baseline" ;;
esac
