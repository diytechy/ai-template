+++
id = "WI-899"
title = "adjudicate: TC-055 - approved/routed cell(s) amended on merged trunk fe30b0a..d40e9af (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/test/test-cases.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["TC-055"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- TC-055 `Method`: 'A fresh, family-heterogeneous CRITIQUE session (LLR-048/LLR-082 loop) adjudicates the generated PROJECT_STATE.html agai…' -> 'A fresh, family-heterogeneous CRITIQUE session (LLR-048/LLR-082 loop) adjudicates the generated PROJECT_STATE.html agai…'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
