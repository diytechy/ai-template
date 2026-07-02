<#
.SYNOPSIS
    PowerShell reference port of the kit's gen_arch_map.py — regenerate the code
    map, dependency diagram, and high-level flow from the real source AST so none
    can drift. For a PowerShell-stack repo adopting the kit (see ADOPTING.md §3).

.DESCRIPTION
    The kit ships gen_arch_map.py, which parses *Python*. A PowerShell project
    needs the same guarantee over *its* source, and the contract is only the
    marker blocks this script fills — so a straight port satisfies check.ps1 /
    the pre-commit hook / CI identically. This is that port, generalized from a
    real adoption (the FileBackup pilot). It parses your modules with the
    PowerShell AST (System.Management.Automation.Language) and maintains three
    generated regions:

    GENERATED MODULE MAP (required in every -Doc): per module —
      - the module's one-line summary (its comment-based-help .SYNOPSIS),
      - internal coupling: which OTHER in-tree modules it calls into (so a
        layering invariant like "Common must never depend on Engine" is
        auditable, and a change's blast radius is visible),
      - each function, whether it is exported (Export-ModuleMember), and any
        `# Implements: SR-/LLR-` back-link comment in the function body.

    GENERATED DEPENDENCY DIAGRAM (optional per -Doc; presence opts in): the same
    coupling as a Mermaid `graph LR`, plus the entry scripts and which modules
    they call. Mermaid fences render natively on GitHub and in the VS Code
    Markdown preview — no diagram toolchain (process.md "Diagrams are text").

    GENERATED FLOW (optional per -Doc): the ordered internal calls the -Flow
    orchestrator makes, each with the callee's .SYNOPSIS — the "thin
    orchestrators" rule, generated. A short/vague list means the routine inlines
    logic instead of delegating.

    ── EDIT FOR YOUR REPO ─────────────────────────────────────────────────────
    Three inputs below are repo-shaped; adjust them and delete this banner:
      $ModuleGlob   where your modules live + their extension (default Modules/*.psm1)
      $EntryScripts top-level scripts to include in the diagram (default: none)
      -Flow default the orchestrator whose call sequence fills the FLOW block
    Everything else is the generic marker-block contract — leave it alone.

.PARAMETER Doc
    Target file(s) to update (each must contain the MODULE MAP marker pair;
    DIAGRAM/FLOW markers are optional per file). Default: docs/architecture.md
    and AGENTS.md.

.PARAMETER Flow
    Orchestrator function whose call sequence fills the GENERATED FLOW markers.
    Pass '' to skip the flow block.

.PARAMETER Check
    Do not write; exit 1 if any target's generated regions differ from disk
    (so check.ps1 / CI can fail on a stale doc). This is the freshness gate the
    kit's pre-commit hook runs — a string comparison, exactly like --check in
    gen_arch_map.py.

.NOTES
    Implements: (tooling — supports the traceability harness, not an SR/LLR.)
    Canonical passing command on a PowerShell repo is `scripts/check.ps1`
    (ADOPTING.md §3 "one definition of passing").
#>
[CmdletBinding()]
param(
    [string[]]$Doc,
    [string]$Flow = '',
    [switch]$Check
)

$ErrorActionPreference = 'Stop'
$repo = [System.IO.Path]::GetDirectoryName($PSScriptRoot)

# ── EDIT FOR YOUR REPO ──────────────────────────────────────────────────────
$ModuleGlob   = Join-Path $repo 'Modules'          # folder holding your modules
$ModuleFilter = '*.psm1'                            # module file extension
$EntryScripts = @()                                 # e.g. @('App.ps1','Restore.ps1')
# ────────────────────────────────────────────────────────────────────────────

$modules = @()
if (Test-Path -LiteralPath $ModuleGlob) {
    $modules = Get-ChildItem -LiteralPath $ModuleGlob -Filter $ModuleFilter | Sort-Object Name
}
$entryPaths = $EntryScripts |
    ForEach-Object { Join-Path $repo $_ } | Where-Object { Test-Path -LiteralPath $_ }

if (-not $Doc) {
    $Doc = @((Join-Path $repo 'docs/architecture.md'), (Join-Path $repo 'AGENTS.md'))
}

# An empty scan is legitimate pre-code, but it makes -Check pass *vacuously* —
# say so loudly rather than let the drift-proofing guarantee silently lapse
# (mirrors gen_arch_map.py's zero-source warning; see ADOPTING.md §3).
if (-not $modules) {
    Write-Warning "No modules found under $ModuleGlob ($ModuleFilter) — the map is empty and -Check passes vacuously. Point `$ModuleGlob at your source or remove the arch-map step (ADOPTING.md)."
}

function Get-ExportedNames {
    param([System.Management.Automation.Language.Ast]$Ast)
    $names = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
    $calls = $Ast.FindAll({ param($n)
        $n -is [System.Management.Automation.Language.CommandAst] -and
        $n.GetCommandName() -eq 'Export-ModuleMember' }, $true)
    foreach ($c in $calls) {
        $strings = $c.FindAll({ param($n)
            $n -is [System.Management.Automation.Language.StringConstantExpressionAst] }, $true)
        foreach ($s in $strings) {
            if ($s.Value -in 'Export-ModuleMember','Function','Alias','Cmdlet','Variable') { continue }
            [void]$names.Add($s.Value)
        }
    }
    return $names
}

function Get-ModuleCalls {
    # Distinct OTHER in-tree modules an AST calls into.
    param([System.Management.Automation.Language.Ast]$Ast, [hashtable]$FuncToModule, [string]$SelfShort)
    $deps = [System.Collections.Generic.SortedSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($c in $Ast.FindAll({ param($n)
        $n -is [System.Management.Automation.Language.CommandAst] }, $true)) {
        $name = $c.GetCommandName()
        if (-not $name) { continue }
        $owner = $FuncToModule[$name.ToLowerInvariant()]
        if ($owner -and $owner -ne $SelfShort) { [void]$deps.Add($owner) }
    }
    return $deps
}

function Get-FirstSynopsisLine {
    param($HelpContent)
    if ($HelpContent -and $HelpContent.Synopsis) {
        return ($HelpContent.Synopsis -split "`n" | Where-Object { $_.Trim() } | Select-Object -First 1).Trim()
    }
    return ''
}

# --- Pass 1: parse every module; index function name -> module/synopsis -------
$parsed = @{}
$funcToModule = @{}   # lower-case function name -> module short name
$funcSynopsis = @{}   # lower-case function name -> one-line .SYNOPSIS ('' if none)
foreach ($mod in $modules) {
    $tokens = $errs = $null
    $ast = [System.Management.Automation.Language.Parser]::ParseFile($mod.FullName, [ref]$tokens, [ref]$errs)
    $short = $mod.BaseName -replace '\.(psm1|ps1)$', ''
    $fns = $ast.FindAll({ param($n)
        $n -is [System.Management.Automation.Language.FunctionDefinitionAst] }, $false)
    foreach ($fn in $fns) {
        $key = $fn.Name.ToLowerInvariant()
        $funcToModule[$key] = $short
        if (-not $funcSynopsis.ContainsKey($key)) {
            $funcSynopsis[$key] = Get-FirstSynopsisLine -HelpContent $fn.GetHelpContent()
        }
    }
    $parsed[$mod.Name] = [pscustomobject]@{
        Ast      = $ast
        Short    = $short
        Synopsis = Get-FirstSynopsisLine -HelpContent $ast.GetHelpContent()
        Exported = Get-ExportedNames -Ast $ast
        Fns      = $fns
    }
}

# --- Pass 2: the MODULE MAP block ----------------------------------------------
$sb = [System.Text.StringBuilder]::new()
[void]$sb.AppendLine('<!-- BEGIN GENERATED MODULE MAP -->')
[void]$sb.AppendLine("_Generated by ``scripts/gen_arch_map.ps1`` from the modules' AST. Do not edit by hand;")
[void]$sb.AppendLine('run the generator. Summary = the module''s .SYNOPSIS; back-links come from `Implements:` comments._')
foreach ($mod in $modules) {
    $info = $parsed[$mod.Name]
    $deps = Get-ModuleCalls -Ast $info.Ast -FuncToModule $funcToModule -SelfShort $info.Short
    [void]$sb.AppendLine('')
    [void]$sb.AppendLine("### ``$($mod.Name)``")
    [void]$sb.AppendLine('')
    if ($info.Synopsis) { [void]$sb.AppendLine("_$($info.Synopsis)_") }
    if ($deps.Count) {
        $depList = ($deps | ForEach-Object { '`' + $_ + '`' }) -join ', '
        [void]$sb.AppendLine("Imports (internal): $depList")
    } else {
        [void]$sb.AppendLine('Imports (internal): _none_')
    }
    [void]$sb.AppendLine('')
    [void]$sb.AppendLine('| Function | Exported | Implements |')
    [void]$sb.AppendLine('|---|:---:|---|')
    foreach ($fn in $info.Fns | Sort-Object Name) {
        $impl = ''
        # Only the dedicated back-link comment line counts — help-block prose may
        # mention "Implements: ..." too (e.g. inside a .PARAMETER note).
        $m = [regex]::Match($fn.Extent.Text, '(?m)^\s*#\s*Implements:\s*([^\r\n#]+)')
        if ($m.Success) { $impl = $m.Groups[1].Value.Trim().TrimEnd('.') }
        $exp = if (($info.Exported.Count -eq 0) -or $info.Exported.Contains($fn.Name)) { 'yes' } else { 'no' }
        $imp = if ($impl) { $impl } else { '—' }
        [void]$sb.AppendLine("| ``$($fn.Name)`` | $exp | $imp |")
    }
}
[void]$sb.Append('<!-- END GENERATED MODULE MAP -->')
$mapBlock = $sb.ToString() -replace "`r`n", "`n"

# --- Pass 3: the DEPENDENCY DIAGRAM block (Mermaid) -----------------------------
function Get-MermaidNodeId { param([string]$Name) return 'n_' + ($Name -replace '\W', '_') }
function Get-MermaidLabel {
    param([string]$Name, [string]$Synopsis)
    $label = $Name
    if ($Synopsis) {
        $short = if ($Synopsis.Length -le 48) { $Synopsis } else { $Synopsis.Substring(0, 47) + '…' }
        $label = "$Name — $short"
    }
    return $label.Replace('"', "'")
}

$sb = [System.Text.StringBuilder]::new()
[void]$sb.AppendLine('<!-- BEGIN GENERATED DEPENDENCY DIAGRAM -->')
[void]$sb.AppendLine('_Generated by `scripts/gen_arch_map.ps1`: each arrow is a call into another')
[void]$sb.AppendLine('in-tree module. A layering-violation arrow is a defect you can see. Do not edit by hand._')
[void]$sb.AppendLine('')
[void]$sb.AppendLine('```mermaid')
[void]$sb.AppendLine('graph LR')
$edges = [System.Collections.Generic.SortedSet[string]]::new([System.StringComparer]::Ordinal)
foreach ($mod in $modules) {
    $info = $parsed[$mod.Name]
    $id = Get-MermaidNodeId $info.Short
    $label = Get-MermaidLabel $info.Short $info.Synopsis
    [void]$sb.AppendLine("    $id[`"$label`"]")
    foreach ($dep in (Get-ModuleCalls -Ast $info.Ast -FuncToModule $funcToModule -SelfShort $info.Short)) {
        [void]$edges.Add("    $id --> $(Get-MermaidNodeId $dep)")
    }
}
foreach ($script in $entryPaths) {
    $tokens = $errs = $null
    $ast = [System.Management.Automation.Language.Parser]::ParseFile($script, [ref]$tokens, [ref]$errs)
    $name = [System.IO.Path]::GetFileName($script)
    # Functions defined inside the script itself are not module calls.
    $localFns = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($fn in $ast.FindAll({ param($n)
        $n -is [System.Management.Automation.Language.FunctionDefinitionAst] }, $true)) { [void]$localFns.Add($fn.Name) }
    $deps = [System.Collections.Generic.SortedSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($c in $ast.FindAll({ param($n)
        $n -is [System.Management.Automation.Language.CommandAst] }, $true)) {
        $cn = $c.GetCommandName()
        if (-not $cn -or $localFns.Contains($cn)) { continue }
        $owner = $funcToModule[$cn.ToLowerInvariant()]
        if ($owner) { [void]$deps.Add($owner) }
    }
    $id = Get-MermaidNodeId $name
    $label = Get-MermaidLabel $name (Get-FirstSynopsisLine -HelpContent $ast.GetHelpContent())
    [void]$sb.AppendLine("    $id([`"$label`"])")
    foreach ($dep in $deps) { [void]$edges.Add("    $id --> $(Get-MermaidNodeId $dep)") }
}
foreach ($e in $edges) { [void]$sb.AppendLine($e) }
[void]$sb.AppendLine('```')
[void]$sb.Append('<!-- END GENERATED DEPENDENCY DIAGRAM -->')
$diagramBlock = $sb.ToString() -replace "`r`n", "`n"

# --- Pass 4: the FLOW block (ordered internal calls of the orchestrator) -------
$flowBlock = $null
if ($Flow) {
    $entryFn = $null
    foreach ($mod in $modules) {
        $hit = $parsed[$mod.Name].Fns | Where-Object { $_.Name -eq $Flow }
        if ($hit) { $entryFn = $hit | Select-Object -First 1; break }
    }
    if (-not $entryFn) { throw "Flow entry function not found in modules: $Flow" }

    $calls = $entryFn.FindAll({ param($n)
        $n -is [System.Management.Automation.Language.CommandAst] }, $true) |
        Sort-Object { $_.Extent.StartOffset }
    $sb = [System.Text.StringBuilder]::new()
    [void]$sb.AppendLine('<!-- BEGIN GENERATED FLOW -->')
    [void]$sb.AppendLine("_Generated by ``scripts/gen_arch_map.ps1 -Flow $Flow`` — the ordered internal calls")
    [void]$sb.AppendLine("in ``$Flow``. Keep orchestrators thin: a readable flow here means the routine")
    [void]$sb.AppendLine('delegates instead of computing. Loops/branches are not shown — see the')
    [void]$sb.AppendLine('hand-written overview for control flow. Do not edit by hand._')
    [void]$sb.AppendLine('')
    $entrySynopsis = $funcSynopsis[$Flow.ToLowerInvariant()]
    if ($entrySynopsis) {
        [void]$sb.AppendLine("**``$Flow``** — $entrySynopsis")
        [void]$sb.AppendLine('')
    }
    $i = 0
    foreach ($c in $calls) {
        $cn = $c.GetCommandName()
        if (-not $cn) { continue }
        $key = $cn.ToLowerInvariant()
        if (-not $funcToModule.ContainsKey($key) -or $cn -eq $Flow) { continue }
        $i++
        $s = $funcSynopsis[$key]
        $line = if ($s) { "$i. ``$cn`` — $s" } else { "$i. ``$cn``" }
        [void]$sb.AppendLine($line)
    }
    if ($i -eq 0) {
        [void]$sb.AppendLine("_(no internal calls found — is ``$Flow`` the orchestrator?)_")
    }
    [void]$sb.Append('<!-- END GENERATED FLOW -->')
    $flowBlock = $sb.ToString() -replace "`r`n", "`n"
}

# --- Splice the regions into every target doc -----------------------------------
function Set-DocRegion {
    # Replace the marker-delimited region; required markers must exist, optional
    # ones opt in by presence. A duplicated marker would make the splice
    # ambiguous (and silently eat the text between the copies) — refuse instead.
    param([string]$Text, [string]$Marker, [string]$Content, [string]$Target, [switch]$Required)
    $begin = "<!-- BEGIN $Marker -->"
    $end   = "<!-- END $Marker -->"
    $pattern = "(?s)$([regex]::Escape($begin)).*?$([regex]::Escape($end))"
    $count = [regex]::Matches($Text, $pattern).Count
    if ($count -eq 0) {
        if ($Required) { throw "$Marker markers not found in $Target" }
        return $Text
    }
    if ($count -gt 1 -or ([regex]::Matches($Text, [regex]::Escape($begin)).Count -gt 1)) {
        throw "$Target contains a duplicated $Marker marker; keep exactly one pair per file"
    }
    return [regex]::Replace($Text, $pattern, { param($m) $Content }.GetNewClosure())
}

$stale = $false
foreach ($target in $Doc) {
    if (-not (Test-Path -LiteralPath $target)) { throw "Target doc not found: $target" }
    $doc = (Get-Content -LiteralPath $target -Raw) -replace "`r`n", "`n"
    $updated = Set-DocRegion -Text $doc -Marker 'GENERATED MODULE MAP' -Content $mapBlock -Target $target -Required
    $updated = Set-DocRegion -Text $updated -Marker 'GENERATED DEPENDENCY DIAGRAM' -Content $diagramBlock -Target $target
    if ($flowBlock) {
        $updated = Set-DocRegion -Text $updated -Marker 'GENERATED FLOW' -Content $flowBlock -Target $target
    }

    if ($Check) {
        if ($updated -ne $doc) {
            Write-Error "Generated regions are stale in $target. Run: pwsh -File scripts/gen_arch_map.ps1"
            $stale = $true
        } else {
            Write-Host "[OK]  Generated regions current in $target"
        }
    } elseif ($updated -ne $doc) {
        Set-Content -LiteralPath $target -Value $updated -NoNewline -Encoding utf8
        Write-Host "Updated generated regions in $target"
    } else {
        Write-Host "[OK]  Generated regions already current in $target"
    }
}

if ($Check -and $stale) { exit 1 }
exit 0
