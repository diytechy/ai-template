+++
id = "WI-786"
title = "adjudicate: LLR-183, TC-211 - approved/routed cell(s) amended on merged trunk 9233772..a979130 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-183", "TC-211"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-183 `Detail`: 'The machine-readable half of the perspective record, sited on the row rather than beside it. spine_carrier declares hat…' -> 'The machine-readable half of the perspective record, sited on the row rather than beside it. spine_carrier declares hat…'
- TC-211 `Inputs`: 'docs/test/inspection-procedures.md;SR-186' -> 'docs/test/inspection-procedures.md;SR-186;docs/ai-template-redesign-2026-09-05-codex/DECOMPOSITION-AMENDMENTS.md;docs/a…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
