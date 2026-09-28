+++
id = "WI-682"
title = "adjudicate: LLR-210, TC-208 - approved/routed cell(s) amended on merged trunk 464dc7a..77fb093 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-210", "TC-208"]
+++

## Deliverable

Ruled in spine-acts batch C by an independent Fable adjudicator from the kit's own brief, cross-reviewed by Codex Sol over four rounds (wave-5 rulings 37, 38, 44, 45). The verdict (`docs/reviews/wi-682-adjudicate-llr-210-tc-208/001-ADJUDICATE-1d84d77c.md`) ends:

    VERDICT: MEANING rows=2

The act (ledger seq 5) was narrowed to the LLR and TC registries (ruling 38): 31 rows approved, 9 amendment rows re-attested. The SR registry was not copied, so SR-220, SR-223 and SR-224 stay Drafted, and the SR-tier amendments (WI-695's cells, SR-178) stay drifted and visible for a later act. Batch C's returns are one follow-up, drafted in WI-695's `## Dispositions` and minted at this merge.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-210 `Detail`: "The queue-overlap pre-filter's judgement half, as a producer of one adjudication row rather than a warn. `clusters` sel…" -> "The queue-overlap pre-filter's judgement half, as a producer of one adjudication row rather than a warn. `clusters` sel…"
- TC-208 `Method`: 'Driven in process, in a fast module, on hand-built rows and a directory tree with no git. THE SELECTION, its candidate …' -> 'Driven in process, in a fast module, on hand-built rows and a directory tree with no git. THE SELECTION, its candidate …'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
