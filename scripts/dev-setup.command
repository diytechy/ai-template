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

# 1b. Runtime rung (WI-303): the Command Line Tools installed above ship Python
# 3.9 on current macOS — BELOW the kit's 3.11 floor — and macOS ships no
# first-party 3.11+. So on a fresh Mac the double-click path could reach step 2,
# report "[missing] runtime", and stop: every remedy required leaving the flow.
# This rung closes that, and is deliberately the ONLY place in the kit that
# fetches a runtime.
#
# Why this does not contradict the WI-302 ruling ("never bootstrap a provisioner,
# never pipe a download into a shell"). That ruling's substance is: do not execute
# UNVERIFIABLE code from the network. Here nothing is executed until the artifact
# has proved itself twice — a pinned SHA256, and an Apple-notarized Developer-ID
# signature from the Python Software Foundation's team id. That is verifiable
# provenance, not manufactured trust, and it is the opposite of `curl | sh` (which
# is unverifiable by construction: a server can serve different bytes to a pipe).
# Scope is held tight on purpose: macOS only, this launcher only. dev-setup.sh
# stays detect-only on every platform, and the SHIPPED
# dev-setup.template.command stays detect-only too — adopters do not inherit a
# network fetch until this is proven here (owner ruling 2026-07-25).
#
# MAINTENANCE: the pin below must be re-stamped when the kit moves Python.
# Re-stamp with: curl -fsSL <url> -o p.pkg && shasum -a 256 p.pkg &&
#                pkgutil --check-signature p.pkg
PY_VER="3.13.14"
PY_PKG_URL="https://www.python.org/ftp/python/${PY_VER}/python-${PY_VER}-macos11.pkg"
PY_PKG_SHA256="8e58affb218c155a1dfdc27b291f817129669f8760e7a297adb2e4439ba5d2e8"
PY_TEAM_ID="BMM5U3QVKW"  # Developer ID Installer: Python Software Foundation

# The floor probe, mirroring dev-setup.sh's python_311() (canonical definition
# lives there). The CLT-placeholder caveat it also guards is already settled here:
# step 1 above returned unless `xcode-select -p` succeeded.
have_py311() {
  for c in python3 python python3.13 python3.12 python3.11; do
    command -v "$c" >/dev/null 2>&1 || continue
    if "$c" -c 'import sys; raise SystemExit(sys.version_info < (3, 11))' \
      >/dev/null 2>&1; then return 0; fi
  done
  return 1
}

if [ "$(uname)" = "Darwin" ] && ! have_py311; then
  say "No Python 3.11+ found. macOS ships 3.9 (the Command Line Tools), which is"
  say "below the floor this project needs, so one more download is required."
  say
  say "  Install : Python ${PY_VER}"
  say "  From    : ${PY_PKG_URL}"
  say "  Verified: pinned SHA-256, plus an Apple-notarized Developer ID"
  say "            signature from the Python Software Foundation"
  say "  Note    : macOS will ask for your admin password (system install)."
  say
  printf 'Download and install it now? [y/N] '
  read -r okpy
  case "$okpy" in
    [Yy]*)
      tmp=$(mktemp -d) || { say "Could not create a temp dir."; exit 1; }
      # Clean up the installer whatever happens — success, failure, or Ctrl-C.
      trap 'rm -rf "$tmp"' EXIT HUP INT TERM
      pkg="$tmp/python-${PY_VER}.pkg"
      say "Downloading (about 70 MB)..."
      if ! curl -fsSL --proto '=https' --tlsv1.2 "$PY_PKG_URL" -o "$pkg"; then
        say "Download failed. Check your connection, or install Python ${PY_VER}"
        say "manually from https://www.python.org/downloads/macos/"
        exit 1
      fi
      # FAIL CLOSED, and BEFORE anything is executed. Integrity first, then
      # authenticity: the hash pins the exact artifact this kit was tested
      # against; the signature proves who built it and that Apple notarized it.
      say "Verifying checksum..."
      if ! printf '%s  %s\n' "$PY_PKG_SHA256" "$pkg" | shasum -a 256 -c - >/dev/null 2>&1; then
        say "CHECKSUM MISMATCH - refusing to install. The download did not match"
        say "the pinned hash. Nothing was run. Report this: it means the artifact"
        say "changed, or the download was tampered with."
        exit 1
      fi
      say "Verifying Apple signature..."
      sig=$(pkgutil --check-signature "$pkg" 2>&1) || sig=""
      case "$sig" in
        *"$PY_TEAM_ID"*) ;;
        *) say "SIGNATURE CHECK FAILED - not signed by the expected Python"
           say "Software Foundation team id. Refusing to install; nothing was run."
           exit 1 ;;
      esac
      case "$sig" in
        *"trusted by the Apple notary service"*) ;;
        *) say "NOT NOTARIZED by Apple - refusing to install; nothing was run."
           exit 1 ;;
      esac
      say "Verified. Installing (admin password required)..."
      if ! sudo installer -pkg "$pkg" -target /; then
        say "The installer did not complete. Nothing else has changed."
        exit 1
      fi
      rm -rf "$tmp"
      trap - EXIT HUP INT TERM
      if have_py311; then
        say "Python ${PY_VER} installed."
      else
        say "Installed, but no 3.11+ is on PATH in THIS shell yet. Close this"
        say "window and double-click this file again to continue."
        exit 0
      fi
      say
      ;;
    *)
      say "Skipped. dev-setup will report the runtime as missing and name the"
      say "alternatives (uv / Homebrew / python.org)."
      say
      ;;
  esac
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
