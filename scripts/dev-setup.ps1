# dev-setup for THIS repo (the ai-template meta-repo) — the concrete dogfood of
# the onboarding ladder's dev-setup rung (project-trajectory/PROCESS.md §7).
#
# The kit ships project-trajectory/scripts/dev-setup.template.{sh,ps1} with EMPTY
# install slots for downstream repos to fill. This is that template *filled in*
# for the meta-repo's own stack, so the kit provisions itself: Python 3.11+, ruff
# (format), pytest + pytest-cov (the self-test suite and the harness's coverage
# step), pytest-xdist (`-n auto` parallel execution — the declared test command,
# WI-075), an offline Mermaid renderer for the generated diagrams, and the two
# agent CLIs the unattended layer routes through — claude + codex
# (docs/agents.csv pair rows; preflight-enforced at agent-resume boot, WI-109;
# codex replaced opencode at the WI-160 provider-CLI swap, 2026-07-14b).
# Consent-first: the default only reports; -Install acts.
#
# Usage:  powershell -ExecutionPolicy Bypass -File scripts\dev-setup.ps1 [-Check | -Install]
#   -Check    (default) report what's present; install nothing.
#   -Install  create .\.venv (ruff + pytest + pytest-cov + pytest-xdist, asks first) AND wire
#             the pre-commit process floor (core.hooksPath=.githooks; local +
#             reversible). Then OFFERS the agent CLIs (claude, codex) — each
#             its own [y/N] (WI-112): most users want the agentic workflow, but
#             both are deferrable for someone driving sessions with their own
#             tools or an IDE extension.
#
# Linux/macOS contributors: use scripts/dev-setup.sh.
param([switch]$Check, [switch]$Install)
$ErrorActionPreference = "Stop"
# scripts/ -> the repo root (like the scaffolded layout), so .venv lands there.
Push-Location (Split-Path $PSScriptRoot -Parent)
try {
    function Have($cmd) { [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }
    # Python needs more than Have: on Windows, Get-Command resolves the
    # Microsoft Store app-execution alias for `python`, which sits on PATH but
    # exits nonzero when Python isn't actually installed — so probe by
    # *running* the candidate (the shipped hooks/pre-commit pattern; try/catch
    # keeps stderr noise from terminating under ErrorActionPreference=Stop on
    # Windows PowerShell 5.1). Mirrors dev-setup.template.ps1.
    function HavePython($cand) {
        if (-not (Get-Command $cand -ErrorAction SilentlyContinue)) { return $false }
        try {
            & $cand -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)" `
                2>$null | Out-Null
        } catch { return $false }
        return ($LASTEXITCODE -eq 0)
    }
    function Report($label, $present, $hint) {
        if ($present) { Write-Host "  [ok]      $label" }
        else { Write-Host "  [missing] $label  — $hint" }
    }

    # Prefer the project venv -Install creates, so the report reflects what the
    # harness will actually import; fall back to the ambient interpreter.
    $py = $null
    $venvPython = ".venv\Scripts\python.exe"
    $venvSupported = (Test-Path $venvPython) -and (HavePython $venvPython)
    if ($venvSupported) { $py = $venvPython }
    else { foreach ($cand in @("py", "python", "python3")) { if (HavePython $cand) { $py = $cand; break } } }
    function HasModule($mod) {
        if (-not $py) { return $false }
        & $py -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('$mod') else 1)" 2>$null
        return ($LASTEXITCODE -eq 0)
    }

    Write-Host "dev-setup (ai-template meta-repo). Run tests with: python -m pytest -q"
    Write-Host ""
    Report "runtime (python)" ([bool]$py) "install Python 3.11+"
    Report "git" (Have "git") "install git"
    Report "ruff (format/lint)" (HasModule "ruff") "pip install ruff (or run -Install)"
    Report "pytest (self-tests)" (HasModule "pytest") "pip install pytest (or run -Install)"
    Report "pytest-cov (harness coverage step)" (HasModule "pytest_cov") "pip install pytest-cov (or run -Install)"
    Report "pytest-xdist (parallel -n auto)" (HasModule "xdist") "pip install pytest-xdist (or run -Install)"
    # The agent CLIs docs/agents.csv routes through (WI-109) — required for the
    # unattended layer (agent_loop preflight refuses to boot without an enabled
    # row's CLI); everything above still works without them.
    Report "claude CLI (agent sessions: agent-resume.*)" (Have "claude") `
        "npm install -g @anthropic-ai/claude-code; then run claude once to sign in"
    Report "codex CLI (the OPENAI-* rows in docs/agents.csv)" (Have "codex") `
        "npm install -g @openai/codex; then: codex login"
    Report "offline Mermaid renderer" ((Have "code") -or (Have "mmdc") -or (Have "npx")) `
        "VS Code + a Mermaid preview extension, or: npm i -g @mermaid-js/mermaid-cli"
    # Optional, dev-only (WI-189): the dashboard render-critique loop. NOT
    # installed by -Install and NOT shipped downstream (the kit's
    # install-nothing posture governs project-trajectory/scripts, never this
    # meta tool). See scripts/dashboard-shots/README.md + the
    # render-dashboard-critique skill. (Same report line as dev-setup.sh.)
    Report "dashboard shots (optional, meta-only)" (Test-Path "scripts/dashboard-shots/node_modules/playwright") `
        "cd scripts/dashboard-shots && npm ci && npx playwright install chromium (pinned; dev-only)"
    $hooksPath = (git config --get core.hooksPath 2>$null)
    Report "pre-commit floor (core.hooksPath)" ($hooksPath -eq ".githooks") `
        "run -Install, or: git config core.hooksPath .githooks"

    # Ambient-interpreter debris warning (WI-175 / WI-105). $py above prefers the
    # venv; a bare `python -m pytest` resolves via PATH, which may be a DIFFERENT
    # interpreter carrying a pre-5.0 pytest-cov whose parallel-combine race strands
    # thousands of .coverage.* files at the repo root. Warn (never fail) when the
    # PATH python is not the venv and carries the racing version; point at .\.venv.
    # The ^[0-4]\. regex matches only majors 0-4 (5.0.0 / 10.x never match); an
    # empty $covver (no pytest-cov on PATH) fails the match — no coverage, no debris.
    # Probe `python`/`python3` (NOT the `py` launcher): the debris vector is a bare
    # `python -m pytest`, so resolve exactly what that invocation hits.
    $ambient = $null
    foreach ($cand in @("python", "python3")) {
        if (Have $cand) { $ambient = (Get-Command $cand).Source; break }
    }
    $venvPy = Join-Path ".venv" "Scripts\python.exe"
    if ($ambient -and (Test-Path $venvPy) -and
            ((Resolve-Path $ambient).Path -ne (Resolve-Path $venvPy).Path)) {
        $covver = & $ambient -c "import pytest_cov,sys; sys.stdout.write(pytest_cov.__version__)" 2>$null
        if (($LASTEXITCODE -eq 0) -and ($covver -match '^[0-4]\.')) {
            Write-Host ""
            Write-Host "  [warn] PATH python ($ambient) carries pytest-cov $covver - this pre-5.0"
            Write-Host "         version races the parallel coverage combine and strands .coverage.*"
            Write-Host "         debris at the repo root (WI-105). Run the suite through .\.venv"
            Write-Host "         (.venv\Scripts\python.exe -m pytest), or activate it, so the pinned tools run."
        }
    }

    if (-not $Install) {
        Write-Host ""
        if ((-not (Have "claude")) -or (-not (Have "codex"))) {
            Write-Host "note: agent CLI(s) missing above — agent-resume.* cannot boot the unattended"
            Write-Host "loop while docs/agents-enabled lists their rows (preflight refuses, naming"
            Write-Host "each gap + hint). -Install offers each CLI, individually consented;"
            Write-Host "skipping is fine with your own tools / an IDE extension."
            Write-Host ""
        }
        Write-Host "To install the Python dev tools into .\.venv (and be offered the agent CLIs): scripts\dev-setup.ps1 -Install"
        return
    }

    # --- -Install: consent-first venv + dev tools ----------------------------
    if (-not $py) {
        Write-Error "Python 3.11+ not found on PATH; install a supported interpreter first."
        exit 1
    }
    if ((Test-Path ".venv") -and -not $venvSupported) {
        Write-Error "Existing .\.venv uses Python below 3.11; move or remove that environment, then rerun -Install."
        exit 1
    }

    # Wire the agent-neutral pre-commit floor (setup.ps1 wires it downstream; this
    # meta-repo folds it into dev-setup — IMPROVEMENT_PLAN WI-1.42). Independent of
    # the venv install, so it happens even if that's declined. Reversible
    # (git config --unset core.hooksPath); idempotent.
    $null = git rev-parse --is-inside-work-tree 2>$null
    if ((Test-Path ".githooks/pre-commit") -and ($LASTEXITCODE -eq 0)) {
        git config core.hooksPath .githooks
        Write-Host "Enabled pre-commit floor (core.hooksPath=.githooks; undo: git config --unset core.hooksPath)."
    }
    # Delta-aware venv section (WI-111): -Install must never initiate an
    # unnecessary install. When .\.venv already imports all four dev tools,
    # skip this section — no prompt AND no unconditional pip self-upgrade.
    # ($py already prefers the venv interpreter when .venv exists, so HasModule
    # probes the right environment.) The agent-CLI offers below still run
    # either way (WI-112).
    if ($venvSupported -and (HasModule "ruff") -and (HasModule "pytest") `
            -and (HasModule "pytest_cov") -and (HasModule "xdist")) {
        Write-Host "All dev tools already present in .\.venv — nothing to install."
    } else {
        Write-Host ""
        $ans = Read-Host "Create .\.venv and install ruff + pytest + pytest-cov + pytest-xdist into it? [y/N]"
        if ($ans -match '^[Yy]') {
            if (-not (Test-Path ".venv")) { & $py -m venv .venv }
            $python = Join-Path ".venv" "Scripts\python.exe"
            & $python -m pip install --upgrade pip
            # Pinned toolchain (requirements-dev.txt, WI-104) — same versions CI runs.
            & $python -m pip install -r requirements-dev.txt
            Write-Host "Python dev tools installed. Run the self-tests with: python -m pytest -q"
        } else {
            Write-Host "Skipped the Python dev-tools install."
        }
    }

    # Agent CLIs (WI-112) — individually consented, never implicit: most users
    # want the agentic workflow (agent-resume.*) easily accessible, but each
    # CLI is deferrable for someone driving sessions with their own tools or
    # an IDE extension.
    function Offer-Cli($cmd, $pkg, $hint) {
        if (Have $cmd) { return }
        if (-not (Have "npm")) {
            Write-Host "  [skip] $cmd — npm not found; install Node.js first, or install $cmd your own way."
            return
        }
        $a = Read-Host "Install the $cmd CLI now (npm install -g $pkg)? [y/N]"
        if ($a -match '^[Yy]') {
            & npm install -g $pkg
            if (($LASTEXITCODE -eq 0) -and (Have $cmd)) {
                Write-Host "  [ok] $cmd installed — $hint"
            } else {
                Write-Host "  [warn] $cmd is still not on PATH — check the npm global bin dir, then: $hint"
            }
        } else {
            Write-Host "  Skipped $cmd — fine if you use your own tools or an IDE extension."
        }
    }
    Write-Host ""
    Write-Host "Agent CLIs (docs/agents.csv routes unattended sessions through these):"
    Offer-Cli "claude" "@anthropic-ai/claude-code" "run claude once to sign in (or: claude setup-token)"
    Offer-Cli "codex" "@openai/codex" "sign in with: codex login"
    if ((-not (Have "claude")) -or (-not (Have "codex"))) {
        Write-Host ""
        Write-Host "NOTE: docs/agents-enabled currently routes sessions through BOTH claude and"
        Write-Host "codex — with either CLI missing, agent-resume.* cannot boot the walk-away"
        Write-Host "loop (its preflight refuses, naming each gap and its install/sign-in hint)."
        Write-Host "Skipping is fine if you drive sessions with your own tools or an IDE"
        Write-Host "extension; then trim docs/agents-enabled to the rows whose CLIs you keep."
    }
}
finally {
    Pop-Location
}
