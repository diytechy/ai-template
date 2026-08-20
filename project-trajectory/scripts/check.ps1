# Thin launcher for the check harness on Windows (PowerShell). Prefers the
# project venv, then any Python 3.11+ on PATH. All arguments pass to check.py,
# e.g.:  .\scripts\check.ps1 --gate DevStg-Impl --tier smoke
$ErrorActionPreference = "Stop"
# Push/Pop so running the script doesn't leave the caller's shell cd'd here.
Push-Location (Join-Path $PSScriptRoot "..")
try {
    # Every candidate is probed by RUNNING it, and the .venv is preferred but NOT
    # exempt: check.py imports tomllib, so a below-floor interpreter — or a stale
    # venv built on one — is a broken run rather than a find, and "exists" says
    # nothing about that (WI-475 / repo-review 2026-08-19 H-01; the same policy
    # agent-resume.* and check.sh apply). A probe's non-zero exit is DATA here,
    # so the native-command preference is relaxed for the loop — PowerShell 7.4+
    # turns a non-zero native exit into a terminating error under "Stop".
    $python = $null
    $why = @()
    $eapWas = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    foreach ($cand in @((Join-Path ".venv" "Scripts\python.exe"),
                        (Join-Path ".venv" "bin\python"),
                        "py", "python", "python3")) {
        if ($cand -like ".venv*") {
            if (-not (Test-Path $cand)) { continue }
        } elseif (-not (Get-Command $cand -ErrorAction SilentlyContinue)) {
            $why += "[${cand}: not found]"; continue
        }
        # `-c "pass"`, not `-c ""`: PowerShell DROPS an empty string when it
        # builds a native command line, so the empty form reaches python as a
        # bare `-c` with nothing to run — every candidate then reads as broken.
        # Found by running this file, which is the whole lesson of H-01.
        & $cand -c "pass" *> $null
        if ($LASTEXITCODE -ne 0) { $why += "[${cand}: not runnable here]"; continue }
        & $cand -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)" *> $null
        if ($LASTEXITCODE -ne 0) { $why += "[${cand}: older than Python 3.11]"; continue }
        $python = $cand; break
    }
    $ErrorActionPreference = $eapWas
    if (-not $python) {
        Write-Error ("No Python 3.11+ interpreter found. Rejected: " +
            ($why -join " ") + ". Run .\scripts\setup.ps1 first.")
        exit 1
    }

    & $python scripts/check.py @args
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
