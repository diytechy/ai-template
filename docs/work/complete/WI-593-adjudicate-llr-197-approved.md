+++
id = "WI-593"
title = "adjudicate: LLR-197 - approved/routed cell(s) amended on merged trunk 104ecb3..d6e5240 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
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

- LLR-197 `Detail`: "What one registry row's cells MEAN, stated once below every reader: the three Status predicates of the closed {Drafted,…" -> "What one registry row's cells MEAN, stated once below every reader: the three Status predicates of the closed {Drafted,…"
- LLR-197 `Rationale`: 'trace.py ENFORCES the spine and spine_rules.py DERIVES its stage from the same rows, so every question either asked of …' -> 'trace.py ENFORCES the spine and spine_rules.py DERIVES its stage from the same rows, so every question either asked of …'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
