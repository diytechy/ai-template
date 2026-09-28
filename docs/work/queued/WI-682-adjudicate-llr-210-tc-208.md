+++
id = "WI-682"
title = "adjudicate: LLR-210, TC-208 - approved/routed cell(s) amended on merged trunk 464dc7a..77fb093 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-210", "TC-208"]
+++

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
