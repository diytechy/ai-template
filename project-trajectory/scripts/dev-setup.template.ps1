# dev-setup (Windows) — provision the *developer workstation* rung of the
# onboarding ladder (process.md §7):
#
#     Stage 0  ->  dev-setup  ->  setup  ->  check
#                  (this)         deps       gates
#
# This readies what a *human* needs to view, render, edit, and run this repo —
# a runtime, git, and an OFFLINE Markdown+Mermaid renderer — distinct from
# setup.ps1 (that installs the *product* toolchain: venv, ruff, pytest).
#
# Consent-first and readable: the DEFAULT tier only detects and reports; it
# installs nothing. Nothing here pipes a remote script into a shell.
#
# Usage:  powershell -ExecutionPolicy Bypass -File dev-setup.ps1 [-Check|-Baseline|-Full] [-Profile <role>]
#   -Check     (default) detect + report what's present; install nothing.
#   -Baseline  ensure runtime + git + an offline Mermaid renderer, plus the
#              selected role(s)' tools. Asks before each install.
#   -Full      baseline + an IDE and editor extensions. Opt-in; skipped headless.
#   -Profile   install only that role's tools (plus the shared baseline) — the
#              opt-down for a contributor who wants just their slice. DEFAULT
#              (no -Profile): every declared role. Roles: see $Roles below.
#
# Linux/macOS contributors: use scripts/dev-setup.sh.
param(
    [switch]$Check,
    [switch]$Baseline,
    [switch]$Full,
    [string]$Profile = ""   # "" = all declared roles
)
$ErrorActionPreference = "Stop"

# =================== EDIT FOR YOUR STACK / ROLES ===========================
# The shared BASELINE (runtime, git, offline renderer) is provisioned for every
# profile — fill its install slots. Then declare one ROLE per contributor kind
# (code, asset design, CAD, marketing, …); each adds its own tools on top. The
# DEFAULT installs every role; -Profile <role> narrows to one. Leave any
# Install empty to skip its install (detection still reports). winget shown for
# reference.
#
#   $RuntimeInstall = "winget install --id Python.Python.3.12 -e"
#   $RendererInstall = "npm install -g @mermaid-js/mermaid-cli"   # or install VS Code + a Mermaid preview extension
#   $IdeInstall = "winget install --id Microsoft.VisualStudioCode -e"
$RuntimeInstall = ""
$RendererInstall = ""
$IdeInstall = ""

# One entry per role. Cmds: detection commands (any present => role present).
# Install: the install command (empty = nothing to install here).
$Roles = [ordered]@{
    code   = @{ Cmds = @();           Install = "" }  # toolchain is setup.ps1's job
    design = @{ Cmds = @("inkscape"); Install = "" }  # e.g. "winget install --id Inkscape.Inkscape -e"
}
# ===========================================================================

$tier = if ($Full) { "full" } elseif ($Baseline) { "baseline" } else { "check" }

if ($Profile -and -not $Roles.Contains($Profile)) {
    # Write to stderr + exit 2 directly; Write-Error under -ErrorAction Stop
    # would terminate with exit 1 before this exit code is reached.
    [Console]::Error.WriteLine("Unknown -Profile '$Profile'. Declared roles: $($Roles.Keys -join ', ')")
    exit 2
}
$selected = if ($Profile) { @($Profile) } else { @($Roles.Keys) }

function Have($cmd) { [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }
# Python needs more than Have: on Windows, Get-Command resolves the Microsoft
# Store app-execution alias for `python`, which sits on PATH but exits nonzero
# when Python isn't actually installed — so probe by *running* the candidate
# (the shipped hooks/pre-commit pattern; try/catch keeps stderr noise from
# terminating under ErrorActionPreference=Stop on Windows PowerShell 5.1).
function HavePython($cand) {
    if (-not (Get-Command $cand -ErrorAction SilentlyContinue)) { return $false }
    try {
        & $cand -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)" `
            2>$null | Out-Null
    } catch { return $false }
    return ($LASTEXITCODE -eq 0)
}
# Interactive only with a real console and outside CI, so -Full never blocks
# an automated run on a prompt.
function Interactive { [Environment]::UserInteractive -and -not $env:CI }
function RendererPresent { (Have "code") -or (Have "mmdc") -or (Have "npx") }
# A role reads present when any detection command is on PATH, or when it
# declares none (e.g. code, whose toolchain is setup.ps1's job).
function RolePresent($role) {
    $cmds = $Roles[$role].Cmds
    if (-not $cmds -or $cmds.Count -eq 0) { return $true }
    foreach ($c in $cmds) { if (Have $c) { return $true } }
    return $false
}

$script:missing = 0
function Report($label, $present, $hint) {
    if ($present) { Write-Host "  [ok]      $label" }
    else { Write-Host "  [missing] $label  — $hint"; $script:missing++ }
}
function MaybeInstall($label, $cmd) {
    if (-not $cmd) {
        Write-Host "  - ${label}: no install command configured (see EDIT FOR YOUR STACK); skipping."
        return
    }
    if (-not (Interactive)) { Write-Host "  - ${label}: non-interactive; skipping install ($cmd)"; return }
    $ans = Read-Host "  Install $label via `"$cmd`"? [y/N]"
    if ($ans -match '^[Yy]') { Invoke-Expression $cmd } else { Write-Host "  - skipped $label" }
}

$profileLabel = if ($Profile) { $Profile } else { "all" }
Write-Host "dev-setup — profile=$profileLabel tier=$tier"
Write-Host "Developer workstation (process.md §7). Product deps are scripts/setup.ps1."
Write-Host ""

# --- Detect + report ---------------------------------------------------------
$runtime = (HavePython "py") -or (HavePython "python") -or (HavePython "python3")
Report "runtime (python)" $runtime "install a Python 3.11+ runtime - e.g. winget install Python.Python.3.13, uv python install 3.13, or the python.org Windows installer"
Report "git" (Have "git") "install git (needed to make reviewable changes)"
Report "offline Markdown+Mermaid renderer" (RendererPresent) `
    "VS Code + a Mermaid preview extension, or: npm i -g @mermaid-js/mermaid-cli"
$hooksPath = (git config --get core.hooksPath 2>$null)
Report "pre-commit floor (core.hooksPath)" ($hooksPath -eq ".githooks") `
    "run -Baseline (or: git config core.hooksPath .githooks)"

foreach ($r in $selected) {
    Report "role: $r" (RolePresent $r) "fill `$Roles['$r'] Cmds/Install in the EDIT block for this role's tools"
}
if ($tier -eq "full") {
    Report "IDE (VS Code 'code')" (Have "code") "install an editor; run again with -Full to add extensions"
}

# The retained adjudicator's long-lived token (WI-846). With [adjudicator]
# retention on, a retained Claude launch reads its token from the file the
# AGENT_CLAUDE_TOKEN_FILE environment variable names, and is refused before
# launch without one. Only a repo that turns retention on needs it, so it is a
# note, never counted missing. dev-setup never reads, stores or prints the token.
function TokenReady {
    $f = $env:AGENT_CLAUDE_TOKEN_FILE
    if (-not $f) { return $false }
    $item = Get-Item -LiteralPath $f -ErrorAction SilentlyContinue
    return ($null -ne $item) -and (-not $item.PSIsContainer) -and ($item.Length -gt 0)
}
if (TokenReady) { Write-Host "  [ok]      retained adjudicator token (AGENT_CLAUDE_TOKEN_FILE)" }
else {
    Write-Host "  [note]    retained adjudicator token not set - needed only with [adjudicator] retention on: run 'claude setup-token' once, keep the token in a file outside the repository, and set AGENT_CLAUDE_TOKEN_FILE to that file"
}

Write-Host ""
if (Test-Path ".venv") { Write-Host "Product toolchain: .venv present (run scripts/setup.ps1 to refresh)." }
else { Write-Host "Product toolchain: run scripts/setup.ps1 to create .venv + install test tools." }

# --- -Check stops here: pure report, always green ----------------------------
if ($tier -eq "check") {
    Write-Host ""
    Write-Host "$script:missing component(s) missing. Install them with: dev-setup.ps1 -Baseline"
    exit 0
}

# --- -Baseline / -Full: consent-first installs -------------------------------
Write-Host ""
Write-Host "Installing the $tier workstation (asks before each step)…"
if (-not $runtime) { MaybeInstall "runtime" $RuntimeInstall }
if (-not (RendererPresent)) { MaybeInstall "offline Mermaid renderer" $RendererInstall }
foreach ($r in $selected) {
    if (-not (RolePresent $r)) { MaybeInstall "role: $r" $Roles[$r].Install }
}
if ($tier -eq "full") {
    if (Interactive) { MaybeInstall "IDE" $IdeInstall }
    else { Write-Host "  - IDE: headless/non-interactive; skipped (opt-in, -Full only)." }
}

# The one-time long-lived token step (WI-846), consented. `claude setup-token`
# prints the token once; the person keeps it in a file outside the repository
# and points AGENT_CLAUDE_TOKEN_FILE at that file. Nothing here reads the token.
if (-not (TokenReady) -and (Have "claude") -and (Interactive)) {
    $ans = Read-Host "Run 'claude setup-token' now for the retained adjudicator's long-lived token (one-time)? [y/N]"
    if ($ans -match '^[Yy]') {
        & claude setup-token
        Write-Host "  Keep the printed token in a file outside this repository, then set"
        Write-Host "  AGENT_CLAUDE_TOKEN_FILE to that file's path (e.g. setx AGENT_CLAUDE_TOKEN_FILE <path>)."
    } else { Write-Host "  - skipped the token step (needed only with adjudicator retention on)" }
}

# Wire the agent-neutral pre-commit process floor (core.hooksPath) — universal,
# zero-dependency, reversible (process.md §7).
# setup.ps1 wires it too (idempotent); doing it here protects a dev-setup-only
# onboarding. Skipped cleanly outside a git repo or before the hook is scaffolded.
if (Test-Path ".githooks/pre-commit") {
    $null = git rev-parse --is-inside-work-tree 2>$null
    if ($LASTEXITCODE -eq 0) {
        git config core.hooksPath .githooks
        Write-Host "Enabled the pre-commit process floor (core.hooksPath=.githooks; undo: git config --unset core.hooksPath)."
    }
}

# A code contributor needs the product toolchain too (setup.ps1). Offer to chain
# into it so onboarding is one command; a non-code role is not asked (WI-1.42).
if (($selected -contains "code") -and (Interactive)) {
    $ans = Read-Host "Run scripts/setup.ps1 now for the product toolchain (venv + test tools)? [y/N]"
    if ($ans -match '^[Yy]') { & (Join-Path "scripts" "setup.ps1") }
}

Write-Host ""
Write-Host "Done. Workstation ready; the pre-commit floor is wired."
Write-Host "If you skipped it above, run scripts/setup.ps1 for the product toolchain, then"
Write-Host ".\scripts\check.ps1 --stage DevStg-Impl to run the gates."
