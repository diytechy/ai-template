@echo off
rem Coordinator relaunch, Windows (WI-822): started detached, in a new console,
rem by the coordinator guard at the lease holder's true session end. Starts
rem `claude` in the declared repo root with the handoff's session prompt; the
rem successor token in PT_COORDINATOR_TAKE lets the new session take the
rem coordinator lease at its SessionStart. The POSIX sibling is
rem coordinator-relaunch.sh.
rem
rem   coordinator-relaunch.cmd REPO_ROOT PROMPT_FILE TOKEN
rem
rem It starts a model outside the session service, so it asks the guard's
rem window-check first and starts nothing inside the blackout window (WI-834).
rem The guard's steps run on one interpreter, resolved as run.cmd resolves its
rem own: each candidate is RUN, and only a Python 3.11+ answers, with its own
rem path; after .venv the list is scripts\dev-setup.ps1's runtime search. No
rem bare `python` a sub-floor install may answer (round 016 F2, D-019).
setlocal
cd /d "%~1" || exit /b 1
set "PY="
for %%C in (".venv\Scripts\python.exe" "py" "python" "python3" "py -3.13" "py -3.12" "py -3.11") do if not defined PY for /f "delims=" %%P in ('%%~C -c "import sys; sys.version_info >= (3, 11) and print(sys.executable)" 2^>nul') do set "PY=%%P"
if not defined PY (
  echo coordinator-relaunch: no Python 3.11+ interpreter found - checked .venv\Scripts\python.exe, py, python, python3, py -3.13, py -3.12 and py -3.11.
  echo Install Python 3.11+ or put an installed one first on PATH.
  exit /b 1
)
"%PY%" "%~1\project-trajectory\scripts\coordinator_guard.py" --root "%~1" window-check || exit /b 1
set "PT_COORDINATOR_TAKE=%~3"
"%PY%" "%~1\project-trajectory\scripts\coordinator_guard.py" exec-claude --prompt-file "%~2"
