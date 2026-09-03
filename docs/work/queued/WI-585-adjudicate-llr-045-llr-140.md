+++
id = "WI-585"
title = "adjudicate: LLR-045, LLR-140, TC-082 - approved/routed cell(s) amended on merged trunk 273564c..b5735bb (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
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

- LLR-045 `Detail`: 'Schedules review-policy sessions in managed mode, constructs redacted prompt-map briefs, parses verdicts, logs selectio…' -> 'Schedules review-policy sessions in managed mode, constructs redacted prompt-map briefs, parses verdicts, logs selectio…'
- LLR-140 `Detail`: 'claim: §2.3 steps 1+2 with the refusal ladder (tracked pause via agent_common.tracked_pause, dirty tree, existing branc…' -> 'claim: §2.3 steps 1+2 with the refusal ladder (tracked pause via agent_common.tracked_pause, dirty tree, existing branc…'
- TC-082 `Method`: 'Run review-policy 0/1/2, prompt-map, redaction, selection logging, verdict, and unmanaged cases.' -> "Run review-policy 0/1/2, prompt-map, redaction, selection logging, verdict, and unmanaged cases. The queue's phases are…"

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
