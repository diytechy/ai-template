+++
id = "WI-601"
title = "adjudicate: LLR-061 - approved/routed cell(s) amended on merged trunk 67e6a50..dc36375 (§A5.2); judge whether scope moved and record the decision"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-061"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-061 `Detail`: 'Replaces internal --track assumptions with explicit --wi/--train/worktree assignment; assembles the worker prompt from …' -> 'Replaces internal --track assumptions with explicit --wi/--train/worktree assignment; assembles the worker prompt from …'

Outcomes (§A5.2): record the exact LLR-061 decision in this spec's
`## Approval` section, or RETURN with findings and draft the real scope-change,
re-scope or cancellation continuation in `## Dispositions`. The primary
publisher applies any accepted Status/snapshot effects and closes or mints the
recorded dispositions atomically after independent review.
