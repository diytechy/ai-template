+++
id = "WI-867"
title = "adjudicate: TC-254 - approved/routed cell(s) amended on merged trunk c5e8220..68b9b26 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/test/test-cases.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["TC-254"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- TC-254 `Expected`: 'Satisfies the acceptance folded into LLR-210 (parent SR-220): the mint, the close and its three outcomes, driven throug…' -> 'Satisfies SR-220 through LLR-210 and LLR-312: the mint and close preflight every affected specification before writing,…'
- TC-254 `Method`: 'Driven on real git repositories and lanes, in a module registered as slow: a queue with an overlapping cluster mints ex…' -> 'Driven on real git repositories and lanes, in a module registered as slow: a queue with an overlapping cluster mints ex…'
- TC-254 `Verifies`: 'SR-220;LLR-210' -> 'SR-220;LLR-210;LLR-312'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
