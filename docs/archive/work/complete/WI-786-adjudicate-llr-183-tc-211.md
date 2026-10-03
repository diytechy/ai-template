+++
id = "WI-786"
title = "adjudicate: LLR-183, TC-211 - approved/routed cell(s) amended on merged trunk 9233772..a979130 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-183", "TC-211"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second sitting is held (the re-mint trap, S11 plan §4.2; owner-agreed close, 2026-10-03).

- LLR-183's `detail` was ruled CLARITY and re-attested at act 26, by verdict `docs/reviews/wi-688-re-judge-tc-211-no-result-rec/003-ADJUDICATE-AMENDMENT-6d76936.md`.
- TC-211's `inputs` was ruled MEANING, blessed and re-attested at act 27, by verdict `004-ADJUDICATE-AMENDMENT-16b163b.md`.

Both rows are byte-identical to their `docs/archive/last_approved/` anchors at this row's mint (2ef5a2a1).

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
