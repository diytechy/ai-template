+++
id = "WI-749"
title = "adjudicate: LLR-116, TC-121 - approved/routed cell(s) amended on merged trunk 2a902b5..6a40d7b (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-116", "TC-121"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-116 `Detail`: 'The mechanized core of usability anchor T7 (docs/rubrics/dashboard-usability.md). Every emitted SVG (all three wrappers…' -> 'The mechanized core of usability anchor T7 (docs/rubrics/dashboard-usability.md). Every emitted SVG carries width:100% …'
- TC-121 `Expected`: 'Every emitted svg scales to fit its container; zero svgs keep the pre-fix fixed-width shape; the shrink floor is pinned…' -> 'Every emitted SVG scales to fit its container; zero SVGs keep the pre-fix fixed-width shape. Every emitted node type to…'
- TC-121 `Method`: 'Generate the dashboard and derive EVERY emitted <svg> from the document (not a hand list, so a fourth emitter cannot sk…' -> 'Generate the dashboard and derive EVERY emitted <svg> from the document (not a hand list, so a fourth emitter cannot sk…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
