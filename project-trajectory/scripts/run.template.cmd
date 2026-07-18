@echo off
setlocal
REM Product launcher (Windows) — double-click to run this project.
REM It presents the capabilities declared in docs/stack.ini's [run] section
REM (process.md section 7, "the evaluator's rungs") so starting the product
REM never requires recalling a command: no args = a numbered menu, and
REM `run.cmd <name>` launches one directly. Read it first; it only delegates
REM to scripts\run_menu.py, so the launch commands live once, in docs/stack.ini.
REM
REM Not applicable (a pure library)? Delete the run.* launchers and describe
REM usage in README.md instead.

cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 ( set "PY=py -3" ) else ( set "PY=python" )
%PY% scripts\run_menu.py %*
set "EXITCODE=%ERRORLEVEL%"
echo.
echo Exited with code %EXITCODE%.
pause
exit /b %EXITCODE%
