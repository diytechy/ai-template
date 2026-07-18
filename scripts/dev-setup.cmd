@echo off
setlocal
REM dev-setup launcher (Windows) - the double-clickable Explorer wrapper for
REM scripts\dev-setup.ps1 (the logic lives once, there; edit it, not this).
REM The WI-051 dev-setup.command pattern, Windows twin (WI-160 follow-up):
REM double-clicking a .ps1 opens an editor instead of running it, so this shim
REM is the double-click rung - it runs the consent-first -Check report, then
REM offers the -Install step exactly like the macOS .command offers --install.
REM ASCII-only on purpose: cmd.exe decodes batch text by console codepage, so
REM any non-ASCII here would mojibake (the .ps1 itself carries a UTF-8 BOM for
REM the same reason - Windows PowerShell 5.1 reads a BOM-less .ps1 as ANSI and
REM an em-dash's trailing byte parses as a curly quote, wrecking the strings).
REM
REM Linux/macOS contributors: use dev-setup.sh / dev-setup.command.
cd /d "%~dp0"

REM Terminal use: any argument is forwarded straight to the .ps1 (parity with
REM dev-setup.command's "$@" hand-off) and the interactive prompt/pause is
REM skipped, e.g.:  scripts\dev-setup.cmd -Install
if not "%~1"=="" (
  powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0dev-setup.ps1" %*
  exit /b %ERRORLEVEL%
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0dev-setup.ps1" -Check
if errorlevel 1 (
  echo.
  echo dev-setup check failed - see the report above.
  pause
  exit /b 1
)

echo.
set /p GO="Run the install step now (.\.venv + dev tools + pre-commit hook, each consented)? [y/N] "
if /i "%GO%"=="y" (
  powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0dev-setup.ps1" -Install
) else (
  echo Done. Install later with: powershell -ExecutionPolicy Bypass -File scripts\dev-setup.ps1 -Install
)
echo.
pause
