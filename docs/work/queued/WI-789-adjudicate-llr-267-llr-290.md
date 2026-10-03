+++
id = "WI-789"
title = "adjudicate: LLR-267, LLR-290 - approved/routed cell(s) amended on merged trunk e78204b..439a2bb (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-267", "LLR-290"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-267 `Detail`: "context(stream, env, session_id) returns (session_id, used, window, pct) for the session's final model request, each fi…" -> "context(stream, env, session_id) returns (session_id, used, window, pct) for the session's final model request, each fi…"
- LLR-290 `Detail`: 'The codex adapter reads compacted entries and per-request input counts from the exact thread rollout under the launch C…' -> 'The codex adapter reads compacted entries and per-request input counts from the exact thread rollout under the launch C…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
