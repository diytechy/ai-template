+++
id = "WI-934"
title = "adjudicate: LLR-270, TC-267, TC-329 - approved/routed cell(s) amended on merged trunk b5b9273..8102894 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-270", "TC-267", "TC-329"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-270 `Detail`: 'CONFIG. keep_config reads [adjudicator] (context_reset_pct 0..100, retain_for, keepwarm_minutes, reset_on_same_artifact…' -> 'CONFIG. keep_config reads [adjudicator] (context_reset_pct 0..100, retain_for, keepwarm_minutes, reset_on_same_artifact…'
- TC-267 `Expected`: "Satisfies LLR-270 (parent SR-227) with the dial on: each runner's resume and occupancy are read from its own output und…" -> "Satisfies LLR-270 (parent SR-227) with the dial on: each runner's resume and occupancy are read from its own output und…"
- TC-267 `Method`: 'With the dial on, over the recorded fixtures (all three LIVE: claude 2026-09-28, codex and opencode 2026-09-30), assert…' -> 'With the dial on, over the recorded fixtures (all three LIVE: claude 2026-09-28, codex and opencode 2026-09-30), assert…'
- TC-267 `Verifies`: 'SR-227;LLR-270;IF-247;IF-248' -> 'SR-227;LLR-270;IF-247;IF-248;IF-273'
- TC-329 `Method`: 'With the dial on and no route record, release two first adjudications together. Assert exactly one takes a keep and min…' -> 'With the dial on and no route record, release two first adjudications together. Assert exactly one takes a keep and min…'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
