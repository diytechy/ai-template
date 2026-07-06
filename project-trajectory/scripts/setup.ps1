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

    # Privacy-check advisory (docs/privacy-check — process-options.md "Commit
    # identity & privacy"). Identity is USER-owned: setup no longer pins or
    # sets an author identity. But when the privacy gate is on, the author email
    # must be in the exempt allowlist (no private/contactable address) or commits
    # are blocked — so warn early if this clone's identity would fail. Advisory
    # only; the hooks are the enforcement. Reuses check_privacy.py --author.
    if (Test-Path "docs/privacy-check") {
        $privacy = (Get-Content "docs/privacy-check" |
            Where-Object { $_.Trim() -and -not $_.Trim().StartsWith("#") } |
            Select-Object -First 1)
        if ($privacy) { $privacy = $privacy.Trim() }
        if ($privacy -eq "true") {
            & $python scripts/check_privacy.py --author 2>$null | Out-Null
            if ($LASTEXITCODE -ne 0) {
                $email = ""
                try { $email = (git config user.email 2>$null) } catch {}
                Write-Warning ("docs/privacy-check is on, but this clone's git author email '" +
                    "$(if ($email) { $email } else { 'unset' })' is not in the exempt allowlist " +
                    "(scripts/check_privacy.py EXEMPT_EMAILS), so commits will be blocked. Set a " +
                    "no-reply identity: git config user.email <you>@users.noreply.github.com (repo-local).")
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
