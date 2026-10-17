+++
id = "WI-938"
title = "adjudicate: LLR-300, TC-339 - approved/routed cell(s) amended on merged trunk a4691ac..01a5005 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-300", "TC-339"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-300 `Detail`: 'guard_config reads the declared coordinator threshold and window: a non-positive, out-of-range or malformed threshold i…' -> 'guard_config reads the declared coordinator threshold and window: a non-positive, out-of-range or malformed threshold i…'
- TC-339 `Expected`: 'Claims refuse on both routes and hooks deny only declared main-session launch forms. Quote-aware words, PowerShell assi…' -> 'Claims refuse on both routes and hooks deny only declared main-session launch forms. Quote-aware words, PowerShell assi…'
- TC-339 `Method`: 'Exercise claims and hooks during blackout with the context guard off. Exercise quote-aware shell reading, PowerShell as…' -> 'Exercise claims and hooks during blackout with the context guard off. Exercise quote-aware shell reading, PowerShell as…'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
