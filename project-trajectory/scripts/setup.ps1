# One-shot dev setup for Windows (PowerShell). Makes a fresh clone runnable.
# Idempotent. Edit the dependency list for your project; the reference installs
# the tools the Python check harness uses. Linux/macOS: use scripts/setup.sh.
$ErrorActionPreference = "Stop"
# Push/Pop so running the script doesn't leave the caller's shell cd'd here.
Push-Location (Join-Path $PSScriptRoot "..")
try {
    # Find a Python launcher.
    $py = $null
    foreach ($cand in @("py", "python", "python3")) {
        if (Get-Command $cand -ErrorAction SilentlyContinue) { $py = $cand; break }
    }
    if (-not $py) { Write-Error "Python 3 not found on PATH."; exit 1 }
    Write-Host "Using $(& $py --version)"

    # Create a local virtualenv so installs don't touch the system Python.
    if (-not (Test-Path ".venv")) {
        Write-Host "Creating .venv ..."
        & $py -m venv .venv
    }
    $python = Join-Path ".venv" "Scripts\python.exe"

    & $python -m pip install --upgrade pip
    # --- Edit below for your stack --------------------------------------------
    # This INSTALLS the tools; what the harness RUNS (format/lint/test commands,
    # tiers, coverage) is declared once in docs/stack.ini — edit there, not in
    # check.py. Install whatever those commands name.
    & $python -m pip install ruff pytest pytest-cov
    if (Test-Path "pyproject.toml") { & $python -m pip install -e . }
    elseif (Test-Path "requirements.txt") { & $python -m pip install -r requirements.txt }
    # ---------------------------------------------------------------------------

    # Enable the agent-neutral pre-commit hook (the process floor) if this is a
    # git repo. Opt-in + reversible: undo with `git config --unset core.hooksPath`.
    if (Test-Path ".githooks/pre-commit") {
        try {
            git rev-parse --is-inside-work-tree 2>$null | Out-Null
            if ($LASTEXITCODE -eq 0) {
                git config core.hooksPath .githooks
                Write-Host "Enabled pre-commit hook (core.hooksPath=.githooks; undo: git config --unset core.hooksPath)."
            }
        }
        catch {
            # Not a git repo yet (or git missing) — the hook is opt-in; skip quietly.
        }
    }

    # Apply the repo's commit-identity policy (docs/commit-identity —
    # process-options.md "Commit identity & anonymity"): when it names an email
    # pattern and this clone's effective identity doesn't match, ask for
    # name/email and set them REPO-LOCALLY — never --global. Consent-first:
    # prompts only when interactive; otherwise warns (the pre-commit hook is
    # the enforcement — it blocks a mismatched commit either way).
    if (Test-Path "docs/commit-identity") {
        $policy = (Get-Content "docs/commit-identity" |
            Where-Object { $_.Trim() -and -not $_.Trim().StartsWith("#") } |
            Select-Object -First 1)
        if ($policy) { $policy = $policy.Trim() }
        if ($policy -and $policy -ne "inherit") {
            $email = ""
            try { $email = (git config user.email 2>$null) } catch {}
            if (-not ($email -like $policy)) {
                if (-not [System.Console]::IsInputRedirected) {
                    Write-Host "This repo's commit-identity policy is '$policy'; this clone's identity is '$(if ($email) { $email } else { "unset" })'."
                    $ciName = Read-Host "Author name for this repo"
                    $ciEmail = Read-Host "Author email (must match $policy; GitHub anonymous form: <user>@users.noreply.github.com)"
                    git config user.name "$ciName"
                    git config user.email "$ciEmail"
                    Write-Host "Set repo-local identity for this clone (global config untouched)."
                }
                else {
                    Write-Warning ("commit-identity policy '$policy' unsatisfied (email '$(if ($email) { $email } else { "unset" })'); " +
                        "rerun scripts/setup interactively or set a repo-local git config user.name/user.email - " +
                        "the pre-commit hook blocks mismatched commits.")
                }
            }
        }
    }

    Write-Host ""
    Write-Host "Setup complete. Run the harness with: .\scripts\check.ps1 --gate G3"
    Write-Host "(check.ps1 uses the venv python directly; no activation needed.)"
}
finally {
    Pop-Location
}
