# kit-python.sh — the ONE interpreter probe the kit's git hooks share (WI-880).
#
# Sourced, never run: pre-commit, commit-msg and pre-push each do
#   . "$(dirname "$0")/kit-python.sh"
#   kit_python <hook> <commit|push> || exit 1
# and every step they run uses "$PY". Bootstrap ships it beside them in
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
  printf '  %s,\n' "${KIT_DEV_SETUP_INSTALL:-run dev-setup's install, which offers the runtime: sh scripts/dev-setup.sh --baseline (Windows: scripts\\dev-setup.cmd -Baseline)}" >&2
  echo "  or put an installed Python 3.11+ first on PATH; then try again." >&2
  return 1
}
