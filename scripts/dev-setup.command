#!/bin/sh
# dev-setup launcher (macOS) — the double-clickable Finder wrapper for
# scripts/dev-setup.sh (the POSIX command lives once, there; edit it, not this).
#
# Beyond hopping to its own directory (so double-click works from anywhere),
# this wrapper owns the one macOS-only rung the shared script can't see: on a
# fresh Mac, /usr/bin/python3 and /usr/bin/git are Command Line Tools
# *placeholders* that satisfy `command -v` but only pop Apple's installer when
# actually run — so dev-setup.sh would report them [ok] while nothing works.
# The real-toolchain probe is `xcode-select -p`; when it fails, offer the
# one-time Apple install first, then hand off.
#
# Linux contributors: use dev-setup.sh.  Windows: use dev-setup.ps1.
set -eu
cd "$(dirname "$0")" || exit 1

say() { printf '%s\n' "$*"; }

# 1. Fresh-Mac rung: ensure the Xcode Command Line Tools (real python3 + git).
if [ "$(uname)" = "Darwin" ] && ! xcode-select -p >/dev/null 2>&1; then
  say "The Xcode Command Line Tools are not installed yet. On a fresh Mac the"
  say "preinstalled 'python3' and 'git' are placeholders that only work after"
  say "this one-time Apple download (see the README's 'Which python?' note)."
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
if [ "$#" -gt 0 ]; then exec sh ./dev-setup.sh "$@"; fi
sh ./dev-setup.sh --check
say
printf 'Run the install step now (./.venv + ruff + pytest + pre-commit hook)? [y/N] '
read -r go
case "$go" in
  [Yy]*) exec sh ./dev-setup.sh --install ;;
  *) say "Done. Install later with: sh scripts/dev-setup.sh --install" ;;
esac
