@echo off
rem Coordinator relaunch, Windows (WI-822): started detached, in a new console,
rem by the coordinator guard at the lease holder's true session end. Starts
rem `claude` in the declared repo root with the handoff's session prompt; the
rem successor token in PT_COORDINATOR_TAKE lets the new session take the
rem coordinator lease at its SessionStart. The POSIX sibling is
rem coordinator-relaunch.sh.
rem
rem   coordinator-relaunch.cmd REPO_ROOT PROMPT_FILE TOKEN
setlocal
cd /d "%~1" || exit /b 1
set "PT_COORDINATOR_TAKE=%~3"
python "%~1\project-trajectory\scripts\coordinator_guard.py" exec-claude --prompt-file "%~2"
