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
# Usage:  powershell -ExecutionPolicy Bypass -File scripts\dev-setup.ps1 [-Check | -Install | -ForRun [-Python <interpreter>]]
#   -Check    (default) report what's present; install nothing.
#   -ForRun   what a bare root `run` calls first (WI-834): the -Check report,
#             then, at an interactive console only (input not redirected), a
#             missing runtime (through uv or winget, when present), the agent
#             CLIs and the retained adjudicator's token step, each offered
#             consent-first. -Python is the interpreter run.cmd
#             resolved and will run its menu on (omitted when it resolved
#             none); the report describes that interpreter only. Exits 0 when
#             it satisfies the 3.11 floor, 1 with the step to take when not.
#   -Install  create .\.venv (ruff + pytest + pytest-cov + pytest-xdist, asks first) AND wire
#             the pre-commit process floor (core.hooksPath=.githooks; local +
#             reversible). Then OFFERS the agent CLIs (claude, codex) — each
#             its own [y/N] (WI-112): most users want the agentic workflow, but
#             both are deferrable for someone driving sessions with their own
#             tools or an IDE extension. With no 3.11+ runtime it first offers
#             one (uv or winget, when present) and searches again, as
#             dev-setup.sh --install does (WI-880); last it offers the
#             coordinator hooks' machine-local opt-in.
#
# Linux/macOS contributors: use scripts/dev-setup.sh.
param([switch]$Check, [switch]$Install, [switch]$ForRun, [string]$Python = "")
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
    function HavePython([string]$exe, [string[]]$exeArgs = @()) {
        if (-not (Get-Command $exe -ErrorAction SilentlyContinue)) { return $false }
        try {
            & $exe @exeArgs -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)" `
                2>$null | Out-Null
        } catch { return $false }
        return ($LASTEXITCODE -eq 0)
    }
    # The dotted version an interpreter reports (e.g. "3.8.10"), or "" when it
    # cannot run — used to NAME a stale .venv (WI-274b) and the recreate
    # interpreter. A broken venv (base CPython uninstalled) yields "".
    function PyVersion([string]$exe, [string[]]$exeArgs = @()) {
        if (-not (Get-Command $exe -ErrorAction SilentlyContinue)) { return "" }
        try {
            $v = & $exe @exeArgs -c "import sys; sys.stdout.write('.'.join(map(str, sys.version_info[:3])))" 2>$null
        } catch { return "" }
        if ($LASTEXITCODE -eq 0) { return ("$v").Trim() }
        return ""
    }
    # A consent prompt needs a console whose input is not redirected, so a
    # prompt never consumes input meant for the run menu.
    function Interactive {
        [Environment]::UserInteractive -and -not $env:CI -and -not [Console]::IsInputRedirected
    }
    function Report($label, $present, $hint) {
        if ($present) { Write-Host "  [ok]      $label" }
        else { Write-Host "  [missing] $label  — $hint" }
    }

    # Prefer the project venv -Install creates, so the report reflects what the
    # harness will actually import; fall back to the ambient interpreter. $py +
    # $pyArgs together are the invocation, so a version-pinned `py -3.12` keeps
    # its selector arg apart for correct splatting (& $py @pyArgs ...).
    $py = $null
    $pyArgs = @()
    $venvPython = ".venv\Scripts\python.exe"
    # WI-274a (002-REVIEW-A): detect the .venv DIRECTORY independently of its
    # interpreter. A broken/incomplete .venv — base CPython uninstalled, or an
    # empty leftover dir — has no runnable Scripts\python.exe, so keying "a venv
    # exists" off the interpreter alone let such a venv slip PAST the
    # consented-recreate branch; -Install then accepted the ordinary create
    # prompt, skipped `venv` (the dir was already there), and died invoking the
    # nonexistent interpreter (line ~228). $venvDirExists routes broken AND
    # sub-floor venvs through the same recreate offer (parity with dev-setup.sh's
    # `[ -d .venv ]` gate).
    $venvDirExists = Test-Path ".venv" -PathType Container
    $venvSupported = (Test-Path $venvPython) -and (HavePython $venvPython)
    # The interpreters searched for a runtime after the venv, in order. WI-274c:
    # after the bare candidates, try version-pinned `py -3.13/-3.12/-3.11`. A
    # stale sub-3.11 .venv active on PATH (VS Code auto-activation) otherwise
    # shadows every bare `python`/`py`, hiding an installed 3.11+ from the
    # recreate offer below (the 2026-07-23 repro). Each is still floor-checked
    # by HavePython. run.cmd probes this same list (WI-834; pinned by
    # tests/test_run_devsetup.py), so a check that finds a runtime means run
    # resolves one too.
    $PyCandidates = @(@("py"), @("python"), @("python3"), @("py", "-3.13"), @("py", "-3.12"), @("py", "-3.11"))
    $PyChecked = ".venv\Scripts\python.exe, " + (($PyCandidates | ForEach-Object { $_ -join " " }) -join ", ")
    # The runtime search: the supported venv, else the first candidate that
    # passes the floor. A function so -Install can search again after a
    # consented runtime install, as dev-setup.sh's discover_py does (WI-880).
    function Find-Runtime {
        $script:py = $null
        $script:pyArgs = @()
        if ($venvSupported) { $script:py = $venvPython; return }
        foreach ($cand in $PyCandidates) {
            if (HavePython @cand) {
                $script:py = $cand[0]
                $script:pyArgs = @($cand | Select-Object -Skip 1)
                return
            }
        }
    }
    if ($ForRun) {
        # A bare run's check (WI-834): only the interpreter run.cmd handed in,
        # the one its menu runs on, so no search here can vouch for another.
        if ($Python -and (HavePython $Python)) { $py = $Python }
    }
    else { Find-Runtime }
    function HasModule($mod) {
        if (-not $py) { return $false }
        & $py @pyArgs -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('$mod') else 1)" 2>$null
        return ($LASTEXITCODE -eq 0)
    }

    Write-Host "dev-setup (ai-template meta-repo). Run tests with: python -m pytest -q"
    Write-Host ""
    Report "runtime (python)" ([bool]$py) "install Python 3.11+ - e.g. winget install Python.Python.3.13, uv python install 3.13, or the python.org Windows installer"
    # WI-274b: name a stale/broken .venv explicitly. The report above prefers the
    # venv when it is supported, else silently describes the ambient interpreter —
    # so without this a contributor sees only "[missing] runtime" and never learns
    # the .venv that shadows their PATH is the sub-floor (or broken) culprit.
    if ($venvDirExists -and -not $venvSupported) {
        $staleVer = PyVersion $venvPython
        if ($staleVer) {
            Write-Host ("  [stale]   .venv is Python {0} — below the 3.11 floor; rerun -Install to recreate it" -f $staleVer)
        } else {
            Write-Host "  [stale]   .venv is unusable (no working 3.11+ interpreter) — rerun -Install to recreate it"
        }
    }
    # Git is queried only once it is known present: under ErrorActionPreference
    # Stop, calling an absent native command throws, which would end the report
    # before its runtime result (round 024 F2). Without git the floor reads
    # missing, and nothing below offers or wires it.
    $haveGit = Have "git"
    Report "git" $haveGit "install git"
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
    $hooksPath = if ($haveGit) { git config --get core.hooksPath 2>$null } else { "" }
    $floorHint = if ($haveGit) { "run -Install, or: git config core.hooksPath .githooks" } else { "needs git: install git first" }
    Report "pre-commit floor (core.hooksPath)" ($hooksPath -eq ".githooks") $floorHint
    # The retained adjudicator's sign-in (WI-834): with [adjudicator] retention
    # on, a retained Claude launch runs under its dedicated home on the
    # long-lived token in the file AGENT_CLAUDE_TOKEN_FILE names (WI-846),
    # refused before launch without one. Read through the kit's own readers
    # (the retention dial and the sign-in probe) when a runtime exists, else
    # unknown; reported only while retention is on. The token is never read here.
    $signin = "unknown"
    if ($py) {
        try {
            # `-X utf8` first: the `py` launcher then runs the interpreter the
            # probe validated, never one the script's shebang names.
            $line = & $py @pyArgs -X utf8 project-trajectory/scripts/coordinator_adjudicate.py signin --retained --root . 2>$null
        } catch { $line = "" }
        if ((($line | Out-String).Trim()) -match '^signin \[ANTHROPIC\]: (\S+)$') { $signin = $Matches[1] }
    }
    switch ($signin) {
        "off" { }
        "signed-in" { Write-Host "  [ok]      retained adjudicator sign-in (AGENT_CLAUDE_TOKEN_FILE)" }
        "missing" { Write-Host "  [missing] retained adjudicator sign-in  — run -Install (or a bare run) for the one-time 'claude setup-token' step, keep the token in a file outside the repository, and set AGENT_CLAUDE_TOKEN_FILE to that file" }
        default { Write-Host "  [unknown] retained adjudicator sign-in  — could not be read (it needs a Python 3.11+ runtime to read the retention dial and the token)" }
    }
    # The coordinator's Claude Code hooks (WI-880, owner ruling 2026-10-10):
    # this repository commits none. The guard's machine-local opt-in merges the
    # hook groups of the inert .claude/settings.json.example into
    # .claude/settings.local.json, each bound to the interpreter that runs it;
    # a machine that has not opted in runs no guard hooks. Read through the
    # guard's own report when a runtime exists.
    $hooksExample = ".claude/settings.json.example"
    $hooks = "none"
    if ($py -and (Test-Path $hooksExample)) {
        try {
            $hooks = ((& $py @pyArgs -X utf8 project-trajectory/scripts/coordinator_guard.py --root . hooks --example $hooksExample 2>$null) | Out-String).Trim()
        } catch { $hooks = "none" }
    }
    switch ($hooks) {
        "on" { Write-Host "  [ok]      coordinator Claude Code hooks (.claude/settings.local.json)" }
        "off" { Write-Host "  [note]    coordinator Claude Code hooks are off - the machine-local opt-in, offered by -Install and a bare run" }
    }
    # Switching them on, consented: the opt-in runs on this script's runtime,
    # the floor-resolved interpreter its hooks are then bound to.
    function Offer-Hooks {
        if ($hooks -ne "off") { return }
        $a = Read-Host "Switch on the coordinator's Claude Code hooks (merged into the machine-local .claude/settings.local.json, keeping any hooks already there)? [y/N]"
        if ($a -match '^[Yy]') {
            & $py @pyArgs -X utf8 project-trajectory/scripts/coordinator_guard.py --root . hooks --example $hooksExample --enable | Out-Null
            if ($LASTEXITCODE -eq 0) { Write-Host "  Switched on the coordinator hooks in .claude/settings.local.json." }
            else { Write-Host "  [warn] the opt-in could not write .claude/settings.local.json; the hooks stay off." }
        } else {
            Write-Host "  Skipped the coordinator hooks; nothing was changed."
        }
    }

    # The one-time long-lived token step (WI-846's), consented; shown only while
    # retention is on and the token is missing. Nothing here reads the token.
    function Offer-Signin {
        if (-not (($signin -eq "missing") -and (Have "claude"))) { return }
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
        } else {
            Write-Host "  Skipped the token step; nothing was changed. A retained adjudication is refused until it is done."
        }
    }

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

    # The agent-CLI offer (WI-112) — individually consented, never implicit.
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

    # The runtime offer (round 032 F1): dev-setup.sh's offer_python on Windows.
    # One consented install of a 3.11+ runtime, only through a provisioner the
    # developer already has (uv, else winget: the two the runtime hint names),
    # never one this script fetches. With neither, nothing is offered and the
    # step text follows. A runtime installed here counts from the next run.
    function Offer-Python {
        if (Have "uv") { $tool = "uv"; $toolArgs = @("python", "install", "3.13") }
        elseif (Have "winget") { $tool = "winget"; $toolArgs = @("install", "--id", "Python.Python.3.13", "-e") }
        else { return }
        $shown = "$tool " + ($toolArgs -join " ")
        $a = Read-Host "No Python 3.11+ found, but $tool is installed. Run '$shown' now? [y/N]"
        if ($a -match '^[Yy]') {
            & $tool @toolArgs
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  [ok] $tool finished - the new runtime counts from the next run."
            } else {
                Write-Host "  [warn] $tool could not install it - install Python 3.11+ your own way."
            }
        } else {
            Write-Host "  Skipped - install Python 3.11+ your own way, then run again."
        }
    }

    # --- -ForRun: the check above, then offers at a console only -------------
    if ($ForRun) {
        Write-Host ""
        if (Interactive) {
            if (-not $py) { Offer-Python }  # installed now, it counts from the next run
            Offer-Cli "claude" "@anthropic-ai/claude-code" "run claude once to sign in (or: claude setup-token)"
            Offer-Cli "codex" "@openai/codex" "sign in with: codex login"
            Offer-Signin
            Offer-Hooks
        } else {
            Write-Host "No interactive console: nothing is offered (run scripts\dev-setup.ps1 -Install at a console)."
        }
        if ($py) { exit 0 }
        Write-Host ""
        Write-Host "The runtime is still missing - the step to take: install Python 3.11+ (e.g. winget install Python.Python.3.13, uv python install 3.13, or the python.org Windows installer) or put an installed one first on PATH, then run again. run checked: $PyChecked"
        exit 1
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
        # dev-setup.sh --install's offer (WI-880): the runtime, through a
        # provisioner already on this machine, then the search again.
        Offer-Python
        Find-Runtime
    }
    if (-not $py) {
        Write-Host ""
        Write-Host "Python 3.11+ not found on PATH; install a supported interpreter first."
        Write-Host "  install Python 3.11+ - e.g. winget install Python.Python.3.13, uv python install 3.13, or the python.org Windows installer"
        Write-Host "  (a newly installed interpreter may need a new console, or its directory on PATH)"
        exit 1
    }
    # WI-274a: a sub-3.11 OR broken .venv gets a CONSENTED recreate at the floor,
    # not the old fail-closed "move or remove" dead end. $py/$pyArgs already hold
    # the discovered 3.11+ interpreter (venv unsupported -> the discovery
    # else-branch ran). Decline keeps today's fail-closed exit; a non-interactive
    # Read-Host returns empty -> declines gracefully, so unattended -Install stays
    # safe. Gated on $venvDirExists (not the interpreter), so an empty/broken
    # .venv dir is offered the recreate instead of crashing the create step below.
    $recreated = $false
    if ($venvDirExists -and -not $venvSupported) {
        $staleVer = PyVersion $venvPython
        $discVer = PyVersion $py $pyArgs
        $discShown = ($py + $(if ($pyArgs) { " " + ($pyArgs -join " ") } else { "" })).Trim()
        if ($staleVer) {
            $prompt = "Existing .\.venv is Python {0} — below the 3.11 floor. Recreate it with {1} (Python {2})? [y/N]" -f $staleVer, $discShown, $discVer
        } else {
            $prompt = "Existing .\.venv is unusable (no working interpreter). Recreate it with {0} (Python {1})? [y/N]" -f $discShown, $discVer
        }
        $ans = Read-Host $prompt
        if ($ans -match '^[Yy]') {
            Remove-Item -Recurse -Force ".venv"
            Write-Host "Removed the stale .\.venv."
            $recreated = $true
        } else {
            Write-Error "Existing .\.venv is below the 3.11 floor or has no working interpreter; recreate declined — move or remove that environment, then rerun -Install."
            exit 1
        }
    }

    # Wire the agent-neutral pre-commit floor (setup.ps1 wires it downstream; this
    # meta-repo folds it into dev-setup — IMPROVEMENT_PLAN WI-1.42). Independent of
    # the venv install, so it happens even if that's declined. Reversible
    # (git config --unset core.hooksPath); idempotent.
    if ($haveGit) { $null = git rev-parse --is-inside-work-tree 2>$null }
    if ($haveGit -and (Test-Path ".githooks/pre-commit") -and ($LASTEXITCODE -eq 0)) {
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
        if ($recreated) {
            # Consent was already given at the recreate prompt above — go
            # straight to the fresh create+install, no second [y/N].
            $ans = "y"
        } else {
            Write-Host ""
            $ans = Read-Host "Create .\.venv and install ruff + pytest + pytest-cov + pytest-xdist into it? [y/N]"
        }
        if ($ans -match '^[Yy]') {
            if (-not (Test-Path ".venv")) { & $py @pyArgs -m venv .venv }
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
    # an IDE extension (Offer-Cli, above).
    Write-Host ""
    Write-Host "Agent CLIs (docs/agents.csv routes unattended sessions through these):"
    Offer-Cli "claude" "@anthropic-ai/claude-code" "run claude once to sign in (or: claude setup-token)"
    Offer-Cli "codex" "@openai/codex" "sign in with: codex login"
    Offer-Signin
    Offer-Hooks
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
