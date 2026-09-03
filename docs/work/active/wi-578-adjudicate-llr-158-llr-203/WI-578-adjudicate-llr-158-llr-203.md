+++
id = "WI-578"
title = "adjudicate: LLR-158, LLR-203, LLR-204 - approved/routed cell(s) amended on merged trunk 2f660cb..0ae37a1 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-158 `Detail`: 'An approval that records what it blessed by COPYING the registries needs no canonical text to hash, no separator that c…' -> 'An approval that records what it blessed by COPYING the registries needs no canonical text to hash, no separator that c…'
- LLR-203 `Detail`: "MAPPING is the declaration SR-163's own reasoning designates as the coverage universe: one row per shipped source, the …" -> "MAPPING is the declaration SR-163's own reasoning designates as the coverage universe: one row per shipped source, the …"
- LLR-203 `Rationale`: 'Naming the inventory that exists rather than a purpose-coverage checker that does not is what keeps this row falsifiabl…' -> 'Naming the INVENTORY, and only the inventory, is what keeps this row falsifiable. The declaration, its exclusion carrie…'
- LLR-203 `Title`: 'The shipped-file inventory and its declared exclusions, carrying no purpose reference' -> 'The shipped-file inventory, its declared exclusions, and its tolerant purpose reference'
- LLR-204 `Detail`: 'backlink_ids is the ONE definition of a purpose declaration in the source surface: an Implements token OPENING a line, …' -> 'backlink_ids is the ONE definition of a purpose declaration in the source surface: an Implements token OPENING a line, …'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
