@echo off
setlocal
REM Product launcher (Windows) - double-click to run this project.
REM It presents the capabilities declared in docs/stack.ini's [run] section
REM (process.md section 7, "the evaluator's rungs") so starting the product
REM never requires recalling a command: no args = a numbered menu, and
REM `run.cmd <name>` launches one directly. Read it first; it only delegates
REM to scripts\run_menu.py, so the launch commands live once, in docs/stack.ini.
REM
REM Not applicable (a pure library)? Delete the run.* launchers and describe
REM usage in README.md instead.

cd /d "%~dp0"
REM Probe each candidate by RUNNING it, not just finding it: `where python`
REM succeeds on the Microsoft Store app-execution alias, which sits on PATH
REM but exits nonzero when Python is not actually installed (the same probe
REM the shipped git hooks use). Prefer a working `python`, else a working
REM `py -3`; if neither probe passes, fall through to `py -3` so the run
REM fails with the same visible not-found error (+ pause) as before.
set "PY=py -3"
python -c "" >nul 2>nul
if not errorlevel 1 (
  set "PY=python"
) else (
  py -3 -c "" >nul 2>nul
  if errorlevel 1 echo Python 3 was not found - checked python and py -3. Install Python 3.11+ first.
)
%PY% scripts\run_menu.py %*
set "EXITCODE=%ERRORLEVEL%"
echo.
echo Exited with code %EXITCODE%.
pause
exit /b %EXITCODE%
