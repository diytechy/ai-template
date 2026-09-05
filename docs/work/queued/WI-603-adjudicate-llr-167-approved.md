+++
id = "WI-603"
title = "adjudicate: LLR-167 - approved/routed cell(s) amended on merged trunk 3b004c4..f395907 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-167 `Detail`: "The row's DECLARED `Brief` cell selects the template (`intake` writes it at every adjudication mint); `compose` fills i…" -> "The row's DECLARED `Brief` cell selects the template (`intake` writes it at every adjudication mint); `compose` fills i…"

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
