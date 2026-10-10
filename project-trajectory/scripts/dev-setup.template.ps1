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
# Usage:  powershell -ExecutionPolicy Bypass -File dev-setup.ps1 [-Check|-Baseline|-Full|-ForRun [-Python <interpreter>]] [-Profile <role>]
#   -Check     (default) detect + report what's present; install nothing.
#   -ForRun    what a bare `run` calls first: the -Check report, then, with an
#              interactive console only, each missing piece offered
#              consent-first (nothing offered without one, piped input
#              included). -Python is the interpreter the launcher resolved
#              and will run its menu on (omitted when it resolved none); the
#              runtime reported is that interpreter only, never one found
#              here. Exits 0 when it satisfies the 3.11 floor, 1 with the
#              step to take when not.
#   -Baseline  ensure runtime + git + an offline Mermaid renderer, plus the
#              selected role(s)' tools. Asks before each install.
#   -Full      baseline + an IDE and editor extensions. Opt-in; skipped headless.
#   -Profile   install only that role's tools (plus the shared baseline) — the
#              opt-down for a contributor who wants just their slice. DEFAULT
#              (no -Profile): every declared role. Roles: see $Roles below.
#
# Linux/macOS contributors: use scripts/dev-setup.sh.
# Contracts: IF-292, IF-293 — the interface seams this script declares (process.md §8;
# rows of record in docs/requirements/interfaces.toml).
#
# Contract IF-292: a bare run invokes this script as -ForRun from the repository
#     root once before its menu, handing it as -Python the interpreter it
#     resolved for the menu (omitted when it resolved none).
# Contract IF-293: exit 0 says that handed interpreter satisfies the runtime
#     floor; nonzero leaves the menu unopened after setup guidance.
param(
    [switch]$Check,
    [switch]$Baseline,
    [switch]$Full,
    [switch]$ForRun,
    [string]$Python = "",   # -ForRun only: the interpreter the launcher resolved
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

$tier = if ($Full) { "full" } elseif ($Baseline) { "baseline" } elseif ($ForRun) { "run" } else { "check" }

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
# Interactive only with a real console whose input is not redirected, and
# outside CI, so -Full never blocks an automated run on a prompt and a consent
# prompt never consumes input piped to the run menu.
function Interactive {
    [Environment]::UserInteractive -and -not $env:CI -and -not [Console]::IsInputRedirected
}
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
# $PyCandidates: the interpreters searched, in order. Keep run.cmd's list the
# same (after its .venv entry), so a check that finds a runtime means run
# resolves one too.
$PyCandidates = @("py", "python", "python3")
$PyChecked = ".venv\Scripts\python.exe, " + ($PyCandidates -join ", ")
# $pybin: the interpreter the kit's own readers below run on; $runtime is
# whether there is one. For a bare run (-ForRun) it is the interpreter the
# launcher handed in, if that satisfies the floor: the one the menu runs on,
# so no search here can vouch for a different one. Otherwise, the first
# floor-satisfying candidate.
function FindPython {
    if ($tier -eq "run") {
        if ($Python -and (HavePython $Python)) { return $Python }
        return $null
    }
    foreach ($cand in $PyCandidates) { if (HavePython $cand) { return $cand } }
    return $null
}
$pybin = FindPython
$runtime = [bool]$pybin
Report "runtime (python)" $runtime "install a Python 3.11+ runtime - e.g. winget install Python.Python.3.13, uv python install 3.13, or the python.org Windows installer"
# Git is queried only once it is known present: under ErrorActionPreference
# Stop, calling an absent native command throws, which would end the report
# before its runtime result (round 024 F2). Without git the floor reads
# missing, and nothing below offers or wires it.
$haveGit = Have "git"
Report "git" $haveGit "install git (needed to make reviewable changes)"
Report "offline Markdown+Mermaid renderer" (RendererPresent) `
    "VS Code + a Mermaid preview extension, or: npm i -g @mermaid-js/mermaid-cli"
$hooksPath = if ($haveGit) { git config --get core.hooksPath 2>$null } else { "" }
$floorHint = if ($haveGit) { "run -Baseline (or: git config core.hooksPath .githooks)" } else { "needs git: install git first" }
Report "pre-commit floor (core.hooksPath)" ($hooksPath -eq ".githooks") $floorHint

foreach ($r in $selected) {
    Report "role: $r" (RolePresent $r) "fill `$Roles['$r'] Cmds/Install in the EDIT block for this role's tools"
}
if ($tier -eq "full") {
    Report "IDE (VS Code 'code')" (Have "code") "install an editor; run again with -Full to add extensions"
}

# The retained adjudicator's sign-in (WI-834): with [adjudicator] retention on,
# a retained Claude launch runs under its own dedicated home and authenticates
# with the long-lived token in the file AGENT_CLAUDE_TOKEN_FILE names (WI-846),
# refused before launch without one. Read through the kit's own readers (the
# retention dial and the sign-in probe, coordinator_adjudicate.py signin
# -retained) when a Python runtime exists, else unknown; reported only while
# retention is on. dev-setup never reads, stores or prints the token.
function KitReading($argList) {
    if (-not $pybin) { return "" }
    # `-X utf8` first: the `py` launcher then runs the interpreter the probe
    # validated, never one a script's shebang names.
    try { $out = & $pybin -X utf8 @argList 2>$null } catch { return "" }
    if ($LASTEXITCODE -ne 0) { return "" }
    return (($out | Out-String).Trim())
}
$signin = "unknown"
if ($pybin) {
    $line = KitReading @("scripts/coordinator_adjudicate.py", "signin", "--retained", "--root", ".")
    if ($line -match '^signin \[ANTHROPIC\]: (\S+)$') { $signin = $Matches[1] }
}
switch ($signin) {
    "off" { }
    "signed-in" { Write-Host "  [ok]      retained adjudicator sign-in (AGENT_CLAUDE_TOKEN_FILE)" }
    "missing" {
        Write-Host "  [missing] retained adjudicator sign-in - run 'claude setup-token' once (offered by -Baseline and a bare run), keep the token in a file outside the repository, and set AGENT_CLAUDE_TOKEN_FILE to that file"
        $script:missing++
    }
    default { Write-Host "  [unknown] retained adjudicator sign-in - could not be read (it needs a Python 3.11+ runtime to read the retention dial and the token)" }
}

# The coordinator's Claude Code hooks (WI-834): shipped inert in
# .claude/settings.json.example and switched on only with consent, merged into
# the machine-local .claude/settings.local.json beside any hooks already there,
# each bound to the interpreter that runs the opt-in (never the committed
# .claude/settings.json: the bound path is this machine's).
$hooksExample = ".claude/settings.json.example"
$hooks = "none"
if ($pybin -and (Test-Path $hooksExample)) {
    $hooks = KitReading @("scripts/coordinator_guard.py", "--root", ".", "hooks", "--example", $hooksExample)
    if (-not $hooks) { $hooks = "none" }
}
if ($hooks -eq "on") { Write-Host "  [ok]      coordinator Claude Code hooks (.claude/settings.local.json)" }
elseif ($hooks -eq "off") { Write-Host "  [note]    coordinator Claude Code hooks are off - opt-in, offered by -Baseline and a bare run" }

Write-Host ""
if (Test-Path ".venv") { Write-Host "Product toolchain: .venv present (run scripts/setup.ps1 to refresh)." }
else { Write-Host "Product toolchain: run scripts/setup.ps1 to create .venv + install test tools." }

# --- -Check stops here: pure report, always green ----------------------------
if ($tier -eq "check") {
    Write-Host ""
    Write-Host "$script:missing component(s) missing. Install them with: dev-setup.ps1 -Baseline"
    exit 0
}

# The one-time long-lived token step (WI-846's, shown only while retention is
# on and the token is missing), consented. `claude setup-token` prints the
# token once; the person keeps it in a file outside the repository and points
# AGENT_CLAUDE_TOKEN_FILE at that file. Nothing here reads the token.
function OfferSignin {
    if (-not (($signin -eq "missing") -and (Have "claude") -and (Interactive))) { return }
    Write-Host ""
    Write-Host "The retained adjudicator runs Claude under its own dedicated home, which signs"
    Write-Host "in with a long-lived token. The one-time 'claude setup-token' step mints that"
    Write-Host "token; you keep it in a file outside this repository, at the location you set"
    Write-Host "AGENT_CLAUDE_TOKEN_FILE to. Your normal 'claude' login and every other"
    Write-Host "repository are left alone, and declining changes no configuration or credential."
    $ans = Read-Host "Run 'claude setup-token' now? [y/N]"
    if ($ans -match '^[Yy]') {
        & claude setup-token
        Write-Host "  Keep the printed token in a file outside this repository, then set"
        Write-Host "  AGENT_CLAUDE_TOKEN_FILE to that file's path (e.g. setx AGENT_CLAUDE_TOKEN_FILE <path>)."
    } else { Write-Host "  - skipped the token step; nothing was changed" }
}

# Switching the coordinator's hooks on, consented (WI-834).
function OfferHooks {
    if (-not (($hooks -eq "off") -and (Interactive))) { return }
    $ans = Read-Host "Switch on the coordinator's Claude Code hooks (merged into the machine-local .claude/settings.local.json, keeping any hooks already there)? [y/N]"
    if ($ans -match '^[Yy]') {
        $null = KitReading @("scripts/coordinator_guard.py", "--root", ".", "hooks", "--example", $hooksExample, "--enable")
        Write-Host "  Switched on the coordinator hooks in .claude/settings.local.json."
    } else { Write-Host "  - skipped the coordinator hooks; nothing was changed" }
}

# --- -Baseline / -Full / -ForRun: consent-first offers -------------------------
Write-Host ""
if (($tier -eq "run") -and -not (Interactive)) {
    Write-Host "No interactive console: nothing is offered (run dev-setup at a console to install)."
} else {
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
    OfferSignin
    OfferHooks
}

# --- -ForRun ends here, with its result: the runtime the menu needs -----------
# Nothing more is wired unasked (the floor below is offered, not set), and the
# setup.ps1 chain stays with -Baseline.
if ($tier -eq "run") {
    $hooksPathNow = if ($haveGit) { git config --get core.hooksPath 2>$null } else { "" }
    if ($haveGit -and ($hooksPathNow -ne ".githooks") -and (Test-Path ".githooks/pre-commit") -and (Interactive)) {
        $ans = Read-Host "Enable the pre-commit floor (git config core.hooksPath .githooks)? [y/N]"
        if ($ans -match '^[Yy]') { git config core.hooksPath .githooks }
        else { Write-Host "  - skipped the pre-commit floor" }
    }
    if ($runtime) { exit 0 }
    Write-Host ""
    Write-Host "The runtime is still missing - the step to take: install a Python 3.11+ runtime (e.g. winget install Python.Python.3.13, uv python install 3.13, or the python.org Windows installer) or put an installed one first on PATH, then run again. run checked: $PyChecked"
    exit 1
}

# Wire the agent-neutral pre-commit process floor (core.hooksPath) — universal,
# zero-dependency, reversible (process.md §7).
# setup.ps1 wires it too (idempotent); doing it here protects a dev-setup-only
# onboarding. Skipped cleanly outside a git repo or before the hook is scaffolded.
if ($haveGit -and (Test-Path ".githooks/pre-commit")) {
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
