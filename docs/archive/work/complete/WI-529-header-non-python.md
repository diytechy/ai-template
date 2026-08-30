+++
id = "WI-529"
title = "The contract header in non-Python files and hooks, and an owner-exact reverse check (OI-67 slice 2)"
workstream = "architecture"
sr_refs = ["SR-159"]
needs = ["WI-528"]
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Every owner can declare. Record:
[../../../log.d/2026-08-29-wi529-header-non-python.md](../../../log.md#2026-08-29--wi-529-the-contract-header-reaches-every-owner-oi-67-slice-2).

`gen_arch_map.header_lines` / `file_contracts` read a non-Python file's leading
comment header — `#` lines (shebang skipped) or a Markdown file's first HTML
comment — through the ONE marker and body grammar a module docstring gets
(`_contract_bodies` and `_grammar_findings_over` extracted so both carriers
share it); `owner_files` names the registry's file owners (a directory through
its README); the reference lists them beside the modules. The two git hooks
declare and state `IF-134` / `IF-135`. `check_trajectory._owner_exact_findings`
names the owner — module or file — that fails to declare its row, every
inventory module judged; the marker-grammar honesty arm covers file headers.
Tests for the header carriers, the reference, `owner_files`, a lossy header
marker, and a seam declared on the wrong module.
