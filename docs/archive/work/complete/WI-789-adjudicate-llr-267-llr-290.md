+++
id = "WI-789"
title = "adjudicate: LLR-267, LLR-290 - approved/routed cell(s) amended on merged trunk e78204b..439a2bb (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-267", "LLR-290"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second sitting is held (the re-mint trap, S11 plan §4.2; owner-agreed close, 2026-10-03). LLR-267 and LLR-290 were ruled MEANING, blessed and re-attested at act 28, by verdict `docs/reviews/wi-787-codex-occupancy-default-home/001-ADJUDICATE-AMENDMENT-da2037a.md`. Both rows are byte-identical to their `docs/archive/last_approved/` anchors at this row's mint (2abce2fb).

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
