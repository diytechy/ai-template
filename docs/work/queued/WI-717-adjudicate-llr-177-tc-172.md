+++
id = "WI-717"
title = "adjudicate: LLR-177, TC-172 - approved/routed cell(s) amended on merged trunk 4697024..b90e84b (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-177", "TC-172"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-177 `Detail`: 'write_session_log passes every transcript through redact_secrets before the tracked per-session log (docs/iteration/NNN…' -> "write_session_log passes every transcript, and every header value (a verbatim raw-usage line can carry a runner's resul…"
- TC-172 `Method`: 'Plant credential-shaped values (an API key, a Bearer token, an AWS key id) in a transcript and write the session log: e…' -> 'Plant credential-shaped values (an API key, a Bearer token, an AWS key id) in a transcript and write the session log: e…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
