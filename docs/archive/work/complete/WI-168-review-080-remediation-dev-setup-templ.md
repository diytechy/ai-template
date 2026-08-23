+++
id = "WI-168"
title = "Review 080 remediation - dev-setup.template.cmd consented install is a silent no-op (swap -Install for -Baseline; flip the shape-test token; fix the bootstrap MAPPING docstring)"
workstream = "scripts"
sr_refs = ["SR-032"]
needs = ["WI-166"]
buildtier = "medium"
order = 167
+++

## Deliverable

Swapped -Install -> -Baseline across dev-setup.template.cmd (install invocation line 31, later-hint line 33, the two comments, and the [y/N] prompt wording); rewrote test_scaffold_ships_devsetup_cmd to cross-check every switch the shim hands the ps1 against the scaffolded ps1's param() block instead of pinning a literal; appended cmd to the bootstrap MAPPING docstring inventory.
