# kit-python.sh — the ONE interpreter probe the kit's git hooks share (WI-880).
#
# Sourced, never run: pre-commit, commit-msg and pre-push each do
#   . "$(dirname "$0")/kit-python.sh"
#   kit_python <hook> <commit|push> || exit 1
#   kit_policy <hook> <commit|push> || exit 1
# and every step they run uses "$PY" and "$SCRIPTS_DIR" (kit_policy, below,
# also reads the declared policy once for them). Bootstrap ships it beside them in
# .githooks/, so a hook and its probe travel together; a hook whose probe is
# missing fails at the `.` and refuses, it never guesses.
#
# Each candidate is probed by RUNNING it (on Windows `python3` often resolves to
# the Microsoft Store app-execution alias, which exists on PATH but runs
# nothing), and the probe prints the interpreter's own path only when it
# satisfies the kit's 3.11 floor (the kit scripts import tomllib). The project
# venv comes first, so tool-backed steps like format actually RUN; after it the
# list is the shipped dev-setup.sh's own runtime search, so a dev-setup that
# reports a runtime means the hooks resolve one too (the kit pins the two
# equal). With none, the hook REFUSES, naming dev-setup's install: its checks
# never run on an older interpreter (they would die mid-floor) and are never
# skipped (WI-880 Trust ruling; this also covers a declared privacy policy and
# a loop commit's provenance trailer). A layout whose dev-setup installs
# differently (the kit's own repository) names its step in
# KIT_DEV_SETUP_INSTALL, as it names its scripts dir in KIT_SCRIPTS_DIR.
#
# Needs REPO_ROOT set by the sourcing hook. Sets PY; returns 1 after printing
# the refusal when no candidate passes.
kit_python() {
  PY=""
  for cand in .venv/bin/python .venv/Scripts/python.exe python3 python; do
    PY=$(cd "$REPO_ROOT" && "$cand" -c 'import sys; sys.version_info >= (3, 11) and print(sys.executable)' 2>/dev/null) || PY=""
    [ -n "$PY" ] && return 0
  done
  echo "$1: no Python 3.11+ interpreter found (checked .venv/bin/python," >&2
  echo "  .venv/Scripts/python.exe, python3 and python), so its checks cannot" >&2
  echo "  run: refusing to skip them, and refusing the $2. The fix:" >&2
  # The default is its own assignment, never a ${VAR:-word} word: macOS's
  # /bin/sh (bash 3.2) reads the apostrophe inside a quoted expansion word as
  # an opening quote and the whole file fails to parse (WI-909).
  kit_install_default="run dev-setup's install, which offers the runtime: sh scripts/dev-setup.sh --baseline (Windows: scripts\\dev-setup.cmd -Baseline)"
  printf '  %s,\n' "${KIT_DEV_SETUP_INSTALL:-$kit_install_default}" >&2
  echo "  or put an installed Python 3.11+ first on PATH; then try again." >&2
  return 1
}

# kit_policy <hook> <commit|push>: called right after kit_python, as
#   kit_policy <hook> <commit|push> || exit 1
# It resolves the kit scripts dir once for all three hooks, then asks the
# kit's privacy checker for the ONE policy answer (`check_privacy.py
# --hook-policy`, one parse of the declared policy), so no hook reads the
# policy file as text. Sets SCRIPTS_DIR, KIT_PRIVACY (on|off) and KIT_REVIEW
# (require|warn-unwired when the privacy gate is on); returns 1 after printing
# the refusal on anything else.
#
# The scripts dir: KIT_SCRIPTS_DIR (set by a delegating wrapper; absolute, or
# relative to the repo root) is taken as given, and one that names no
# directory refuses with NO fallback; unset, scripts/ then Scripts/ (NTFS is
# case-preserving, Linux CI is not). A hook that cannot find the kit scripts
# checks nothing, so it refuses rather than skip its floor (WI-926).
#
# The answer is taken on an exact token only: a failed read, an empty answer
# or a near-token (a stray carriage return included) refuses. Every failure
# path returns 1 explicitly, because `set -e` is suspended inside a function
# called from an `||` list.
# Implements: SR-031, LLR-021
kit_policy() {
  SCRIPTS_DIR=""
  KIT_PRIVACY=""
  KIT_REVIEW=""
  if [ -n "${KIT_SCRIPTS_DIR:-}" ]; then
    case "$KIT_SCRIPTS_DIR" in
      /*) SCRIPTS_DIR="$KIT_SCRIPTS_DIR" ;;
      *)  SCRIPTS_DIR="$REPO_ROOT/$KIT_SCRIPTS_DIR" ;;
    esac
  else
    for sd in scripts Scripts; do
      if [ -d "$REPO_ROOT/$sd" ]; then
        SCRIPTS_DIR="$REPO_ROOT/$sd"; break
      fi
    done
  fi
  if [ -z "$SCRIPTS_DIR" ] || [ ! -d "$SCRIPTS_DIR" ]; then
    echo "$1: cannot find the kit scripts dir (KIT_SCRIPTS_DIR or scripts/)" >&2
    echo "  under $REPO_ROOT, so the $2 floor cannot run. REFUSING the $2." >&2
    echo "  Fix one of: set KIT_SCRIPTS_DIR in the delegating wrapper; re-run" >&2
    echo "  bootstrap; or turn the hooks off: git config --unset core.hooksPath" >&2
    return 1
  fi
  if ! KIT_POLICY=$("$PY" "$SCRIPTS_DIR/check_privacy.py" --root "$REPO_ROOT" --hook-policy); then
    echo "$1: the policy read failed: $SCRIPTS_DIR/check_privacy.py --hook-policy" >&2
    echo "  exited nonzero, so the declared policy is unknown. REFUSING the $2." >&2
    return 1
  fi
  case "$KIT_POLICY" in
    "privacy=off")
      KIT_PRIVACY=off ;;
    "privacy=on review=require")
      KIT_PRIVACY=on; KIT_REVIEW=require ;;
    "privacy=on review=warn-unwired")
      KIT_PRIVACY=on; KIT_REVIEW=warn-unwired ;;
    "refuse=mixed")
      echo "$1: docs/process.toml AND the legacy docs/privacy-check both declare" >&2
      echo "  the privacy policy. REFUSING — a mixed config is where two readers" >&2
      echo "  disagree about the same gate. From your kept kit checkout, run:" >&2
      echo "    python project-trajectory/scripts/bootstrap.py --migrate-config --dest ." >&2
      return 1 ;;
    "refuse=unreadable")
      echo "$1: docs/process.toml cannot be read or parsed (the reader's message" >&2
      echo "  is above), so the declared policy is unknown. REFUSING the $2." >&2
      echo "  Fix the file; the fixing commit passes, since this reads the working tree." >&2
      return 1 ;;
    *)
      printf '%s: the policy read (%s --hook-policy) answered "%s",\n' "$1" "$SCRIPTS_DIR/check_privacy.py" "$KIT_POLICY" >&2
      echo "  which is outside its answers, so the declared policy is unknown." >&2
      echo "  REFUSING the $2." >&2
      return 1 ;;
  esac
  return 0
}
