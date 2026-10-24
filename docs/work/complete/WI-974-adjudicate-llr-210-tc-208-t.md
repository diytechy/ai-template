+++
id = "WI-974"
title = "adjudicate: LLR-210, TC-208, TC-254 - approved/routed cell(s) amended on merged trunk 3b9f2b4..b65b304 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-210", "TC-208", "TC-254"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second
sitting is held (the re-mint trap, S11 plan section 4.2; owner-agreed
close, 2026-10-03). WI-856's in-lane sitting
`docs/reviews/wi-856/003-ADJUDICATE-793f65c.md` blessed all three rows as
MEANING+BLESS, and the lane's act turn took act seq 158. At the landing
b65b30462 the stakeholder, system, low-level and test registries are
byte-equal to their approved snapshots under docs/archive/last_approved/.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-210 `Detail`: "The queue-overlap pre-filter's judgement half, as a producer of one adjudication row rather than a warn. `clusters` sel…" -> "The queue-overlap pre-filter's judgement half, as a producer of one adjudication row rather than a warn. `clusters` sel…"
- TC-208 `Method`: 'Driven in process, in a fast module, on hand-built rows and a directory tree with no git. THE SELECTION, its candidate …' -> 'Driven in process, in a fast module, on hand-built rows and a directory tree with no git. THE SELECTION, its candidate …'
- TC-254 `Method`: 'Driven on real git repositories and lanes, in a module registered as slow: a queue with an overlapping cluster mints ex…' -> 'Driven on real git repositories and lanes, in a module registered as slow: a queue with an overlapping cluster mints ex…'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested, bound to the text the verdict judged, and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
