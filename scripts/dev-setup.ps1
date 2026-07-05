# dev-setup for THIS repo (the ai-template meta-repo) — the concrete dogfood of
# the onboarding ladder's dev-setup rung (project-trajectory/PROCESS.md §7).
#
# The kit ships project-trajectory/scripts/dev-setup.template.{sh,ps1} with EMPTY
# install slots for downstream repos to fill. This is that template *filled in*
# for the meta-repo's own stack, so the kit provisions itself: Python 3.8+, ruff
# (format), pytest (the self-test suite), and an offline Mermaid renderer for the
# generated diagrams. Consent-first: the default only reports; -Install acts.
#
# Usage:  powershell -ExecutionPolicy Bypass -File scripts\dev-setup.ps1 [-Check | -Install]
#   -Check    (default) report what's present; install nothing.
#   -Install  create .\.venv and install ruff + pytest into it (asks first).
#
# Linux/macOS contributors: use scripts/dev-setup.sh.
param([switch]$Check, [switch]$Install)
$ErrorActionPreference = "Stop"
# scripts/ -> the repo root (like the scaffolded layout), so .venv lands there.
Push-Location (Split-Path $PSScriptRoot -Parent)
try {
    function Have($cmd) { [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }
    function Report($label, $present, $hint) {
        if ($present) { Write-Host "  [ok]      $label" }
        else { Write-Host "  [missing] $label  — $hint" }
    }

    $py = $null
    foreach ($cand in @("py", "python", "python3")) { if (Have $cand) { $py = $cand; break } }
    function HasModule($mod) {
        if (-not $py) { return $false }
        & $py -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('$mod') else 1)" 2>$null
        return ($LASTEXITCODE -eq 0)
    }

    Write-Host "dev-setup (ai-template meta-repo). Run tests with: python -m pytest -q"
    Write-Host ""
    Report "runtime (python)" ([bool]$py) "install Python 3.8+"
    Report "git" (Have "git") "install git"
    Report "ruff (format/lint)" (HasModule "ruff") "pip install ruff (or run -Install)"
    Report "pytest (self-tests)" (HasModule "pytest") "pip install pytest (or run -Install)"
    Report "offline Mermaid renderer" ((Have "code") -or (Have "mmdc") -or (Have "npx")) `
        "VS Code + a Mermaid preview extension, or: npm i -g @mermaid-js/mermaid-cli"

    if (-not $Install) {
        Write-Host ""
        Write-Host "To install ruff + pytest into .\.venv: scripts\dev-setup.ps1 -Install"
        return
    }

    # --- -Install: consent-first venv + dev tools ----------------------------
    if (-not $py) { Write-Error "Python 3 not found on PATH; install it first."; exit 1 }
    Write-Host ""
    $ans = Read-Host "Create .\.venv and install ruff + pytest into it? [y/N]"
    if ($ans -notmatch '^[Yy]') { Write-Host "Cancelled."; return }
    if (-not (Test-Path ".venv")) { & $py -m venv .venv }
    $python = Join-Path ".venv" "Scripts\python.exe"
    & $python -m pip install --upgrade pip
    & $python -m pip install ruff pytest
    Write-Host ""
    Write-Host "Done. Run the self-tests with: python -m pytest -q"
}
finally {
    Pop-Location
}
