+++
id = "WI-755"
title = "adjudicate: LLR-268, TC-264 - approved/routed cell(s) amended on merged trunk 183ff1c..ba0ea43 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-268", "TC-264"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-268 `Detail`: 'usage(stream) returns one dict with exactly the USAGE_KEYS columns for every runner: cli, semconv (OTEL_SEMCONV, open-t…' -> 'usage(stream) returns one dict with exactly the USAGE_KEYS columns for every runner: cli, semconv (OTEL_SEMCONV, open-t…'
- TC-264 `Method`: 'Over the recorded fixture of each runner (all three LIVE: claude 2026-09-28, codex and opencode 2026-09-30), assert eac…' -> 'Over the recorded fixture of each runner (all three LIVE: claude 2026-09-28, codex and opencode 2026-09-30), assert eac…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
