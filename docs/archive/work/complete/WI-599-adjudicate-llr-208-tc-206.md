+++
id = "WI-599"
title = "adjudicate: LLR-208, TC-206 - approved/routed cell(s) amended on merged trunk 503d0e7..7c5c6d8 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
+++

## Deliverable

Adjudication verdict recorded on the lane; this row is closed MECHANICALLY at its DONE (OI-70/OI-73). Its `## Dispositions` successors mint at this row's own merge (drafts-not-mints), the mint replaces the superseded row's inbound hard edges, and any human-owed answer becomes a `pending` open item the successor depends on. The verdict artifact is under `docs/reviews/`.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-208 `Detail`: 'One file per review scope under docs/reviews/rollup/<train>.md, compiled from the round files that scope carries: ordin…' -> 'One file per review scope under docs/reviews/rollup/<train>.md, compiled from the round files that scope carries: ordin…'
- TC-206 `Method`: 'The rollup as DERIVED state, driven on a scaffold carrying one review scope. Regeneration writes docs/reviews/rollup/<t…' -> 'The rollup as DERIVED state, driven on a scaffold carrying one review scope. Regeneration writes docs/reviews/rollup/<t…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
