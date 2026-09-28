+++
id = "WI-690"
title = "adjudicate: LLR-203, LLR-233 - approved/routed cell(s) amended on merged trunk 0ded5c7..da7ad24 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-203", "LLR-233"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-203 `Detail`: "MAPPING is the declaration SR-163's own reasoning designates as the coverage universe: one row per shipped source, the …" -> "MAPPING is the declaration SR-163's own reasoning designates as the coverage universe: one row per shipped source, the …"
- LLR-203 `Rationale`: 'Naming the INVENTORY, and only the inventory, is what keeps this row falsifiable. The declaration, its exclusion carrie…' -> 'Naming the INVENTORY, and only the inventory, is what keeps this row falsifiable. The declaration, its exclusion carrie…'
- LLR-233 `Detail`: 'is_observation_tc(tc) reads the Automated cell alone: a case whose Automated reads No is an observation test case, the …' -> 'is_observation_tc(tc) reads the Automated cell alone: a case whose Automated reads No is an observation test case, the …'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
