+++
id = "WI-728"
title = "adjudicate: LLR-286 - approved/routed cell(s) amended on merged trunk 5124c93..d05b4b0 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-286"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-286 `Detail`: 'retire(root, row_id, reason, successor, date) judges the whole retirement before writing anything: the id is SN, SR, LL…' -> 'retire(root, row_id, reason, successor, date) judges the whole retirement before writing anything: the id is SN, SR, LL…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
