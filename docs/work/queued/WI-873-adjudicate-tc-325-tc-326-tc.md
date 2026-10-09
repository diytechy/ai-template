+++
id = "WI-873"
title = "adjudicate: TC-325, TC-326, TC-327, TC-328 - approved/routed cell(s) amended on merged trunk 50570fa..82f2866 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/test/test-cases.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["TC-325", "TC-326", "TC-327", "TC-328"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- TC-325 `Tier`: 'Smoke' -> 'Full'
- TC-326 `Tier`: 'Smoke' -> 'Full'
- TC-327 `Tier`: 'Smoke' -> 'Full'
- TC-328 `Tier`: 'Smoke' -> 'Full'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
