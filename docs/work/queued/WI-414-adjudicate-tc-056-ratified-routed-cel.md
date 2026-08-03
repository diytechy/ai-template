+++
id = "WI-414"
title = "adjudicate: TC-056 - ratified/routed cell(s) amended on merged trunk 7894457..5211f07 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/test/test-cases.csv"
buildtier = "medium"
safety_class = "adjudication"
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Ratified and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- TC-056 `Verifies`: 'SR-055;LLR-056' -> 'SR-055;LLR-056;IF-093;IF-094'

Outcomes (§A5.2): flip rows back to Verified where no scope moved
(per docs/gate-policy — recommend-only under attended, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
