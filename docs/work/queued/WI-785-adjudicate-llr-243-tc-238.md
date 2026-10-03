+++
id = "WI-785"
title = "adjudicate: LLR-243, TC-238 - approved/routed cell(s) amended on merged trunk be6500f..1fda46e (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-243", "TC-238"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-243 `Detail`: 'release_gate_findings(das, srs, risks) fails each assumption cited by at least one requirement whose standing reads fal…' -> 'release_gate_findings(das, srs, risks) fails each assumption that at least one requirement cites and whose standing rea…'
- TC-238 `Method`: 'The assumption-evidence step driven on a scaffold with the setting on, in a module registered as slow, and its rule cal…' -> 'The assumption-evidence step driven on a scaffold with the setting on, in a module registered as slow, and its rule cal…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
