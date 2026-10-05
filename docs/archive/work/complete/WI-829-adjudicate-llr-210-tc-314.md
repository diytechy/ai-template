+++
id = "WI-829"
title = "adjudicate: LLR-210, TC-314 - approved/routed cell(s) amended on merged trunk b27ef5d..e81c43d (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-210", "TC-314"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second sitting is held (the re-mint trap, S11 plan §4.2; owner-agreed close, 2026-10-03). The in-lane adjudicator ruled LLR-210 and TC-314 MEANING and blessed them (verdict `docs/reviews/wi-821-dupe-burn-down/002-ADJUDICATE-e50e311.md`, after its 001 return was applied byte-exact), re-attested at act seq 35 in the WI-821 lane. The low-level, system and test-case registries are byte-identical to their anchors under `docs/archive/last_approved/` at the landing.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-210 `Detail`: "The queue-overlap pre-filter's judgement half, as a producer of one adjudication row rather than a warn. `clusters` sel…" -> "The queue-overlap pre-filter's judgement half, as a producer of one adjudication row rather than a warn. `clusters` sel…"
- TC-314 `Method`: 'Drive open-item and work-item registries in temporary repositories. An uncited pending item is an error with no work ro…' -> 'Drive open-item and work-item registries in temporary repositories. An uncited pending item is an error with no work ro…'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
