+++
id = "WI-603"
title = "adjudicate: LLR-167 - approved/routed cell(s) amended on merged trunk 3b004c4..f395907 (§A5.2); judge whether scope moved and record the decision"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-167"]
+++

## Deliverable

Restructured into WI-610.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-167 `Detail`: "The row's DECLARED `Brief` cell selects the template (`intake` writes it at every adjudication mint); `compose` fills i…" -> "The row's DECLARED `Brief` cell selects the template (`intake` writes it at every adjudication mint); `compose` fills i…"

Outcomes (§A5.2): record the exact LLR-167 decision in this spec's
`## Approval` section, or RETURN with findings and draft the real scope-change,
re-scope or cancellation continuation in `## Dispositions`. The primary
publisher applies any accepted Status/snapshot effects and closes or mints the
recorded dispositions atomically after independent review.
