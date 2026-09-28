+++
id = "WI-690"
title = "adjudicate: LLR-203, LLR-233 - approved/routed cell(s) amended on merged trunk 0ded5c7..da7ad24 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-203", "LLR-233"]
+++

## Deliverable

Ruled in spine-acts batch C by an independent Fable adjudicator from the kit's own brief, cross-reviewed by Codex Sol over four rounds (wave-5 rulings 37, 38, 44, 45). The verdict (`docs/reviews/wi-690-adjudicate-llr-203-llr-233/001-ADJUDICATE-1d84d77c.md`) ends:

    VERDICT: MEANING rows=2

The act (ledger seq 5) was narrowed to the LLR and TC registries (ruling 38): 31 rows approved, 9 amendment rows re-attested. The SR registry was not copied, so SR-220, SR-223 and SR-224 stay Drafted, and the SR-tier amendments (WI-695's cells, SR-178) stay drifted and visible for a later act. Batch C's returns are one follow-up, drafted in WI-695's `## Dispositions` and minted at this merge.

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
