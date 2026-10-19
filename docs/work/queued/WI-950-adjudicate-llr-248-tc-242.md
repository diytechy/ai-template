+++
id = "WI-950"
title = "adjudicate: LLR-248, TC-242 - approved/routed cell(s) amended on merged trunk cab3b2a..16e4374 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-248", "TC-242"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-248 `Detail`: 'The claim, refresh, merge, bookkeeping, handback-close and telemetry writers append format_loop_trailer to their messag…' -> 'The claim, refresh, merge, bookkeeping, handback-close and telemetry writers append format_loop_trailer to their messag…'
- TC-242 `Expected`: "Satisfies SR-209's acceptance: every loop-started process carries the marker; a loop commit without a valid trailer is …" -> "Satisfies SR-209's acceptance: every loop-started process carries the marker; a loop commit without a valid trailer is …"
- TC-242 `Method`: 'The trailer helpers unit-tested: format and parse round-trip, a session the grammar refuses cannot be formatted, the tr…' -> 'The trailer helpers unit-tested: format and parse round-trip, a session the grammar refuses cannot be formatted, the tr…'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
