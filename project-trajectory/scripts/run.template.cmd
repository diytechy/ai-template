@echo off
setlocal
REM Product launcher (Windows) - double-click to run this project.
REM It presents the capabilities declared in docs/stack.ini's [run] section
REM (process.md section 7, "the evaluator's rungs") so starting the product
REM never requires recalling a command: no args = a numbered menu, and
REM `run.cmd <name>` launches one directly. Read it first; it only delegates
REM to scripts\run_menu.py, so the launch commands live once, in docs/stack.ini.
REM
REM A bare run (no arguments: the double-click) first runs dev-setup's check
REM for run, `scripts\dev-setup.ps1 -ForRun -Python <interpreter>`, from the
REM repository root: the workstation report, then, at an interactive console
REM only, each missing piece offered consent-first. A runtime still missing
REM afterwards ends the run with the step to take instead of the menu.
REM `run.cmd <name>` and `run.cmd --list`, the agent surface, never run it,
REM never prompt and skip the closing pause.
REM
REM One interpreter: :python below resolves it once, the check is handed
REM exactly that interpreter, and the menu runs on it, so the menu runs on the
REM interpreter whose 3.11 floor the check confirmed. With none resolved, a
REM bare run's check reports the runtime missing and the direct and list
REM forms exit 1 with the step.
REM
REM Not applicable (a pure library)? Delete the run.* launchers and describe
REM usage in README.md instead.

cd /d "%~dp0"
call :python
if not "%~1"=="" goto direct
set "PYARG="
if defined PY set PYARG=-Python "%PY%"
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\dev-setup.ps1 -ForRun %PYARG%
if errorlevel 1 goto missing
"%PY%" scripts\run_menu.py
set "EXITCODE=%ERRORLEVEL%"
echo.
echo Exited with code %EXITCODE%.
pause
exit /b %EXITCODE%

:missing
echo.
echo run: the runtime is still missing; take the step above, then run again.
pause
exit /b 1

:direct
if not defined PY goto nopython
"%PY%" scripts\run_menu.py %*
exit /b %ERRORLEVEL%

:nopython
echo run: no Python 3.11+ interpreter found - checked .venv\Scripts\python.exe, py, python and python3.
echo Install Python 3.11+ or put an installed one first on PATH, then run again.
exit /b 1

:python
REM Resolve the ONE interpreter the check and the menu both run on. Each
REM candidate is probed by RUNNING it (`where python` also matches the
REM Microsoft Store app-execution alias, which runs nothing), and the probe
REM prints the interpreter's own path only when it satisfies the 3.11 floor
REM (run_menu.py imports tomllib). The first answer is a concrete executable,
REM so no launcher in between can pick another interpreter later. No answer
REM leaves PY undefined: nothing is chosen by mere existence. After .venv,
REM the list is scripts\dev-setup.ps1's own runtime search, so a check that finds a
REM runtime means this resolves one too.
set "PY="
for %%C in (".venv\Scripts\python.exe" "py" "python" "python3") do if not defined PY for /f "delims=" %%P in ('%%~C -c "import sys; sys.version_info >= (3, 11) and print(sys.executable)" 2^>nul') do set "PY=%%P"
exit /b 0
