+++
id = "WI-988"
title = "adjudicate: LLR-271, TC-269 - approved/routed cell(s) amended on merged trunk 3f4b989..3082599 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-271", "TC-269"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second
sitting is held (the re-mint trap, S11 plan section 4.2; owner-agreed
close, 2026-10-03). WI-987's in-lane combined sitting
`docs/reviews/wi-987/003-ADJUDICATE-d47f01b.md` blessed both rows
(MEANING+BLESS), and the lane's act turn took act seq 164. At the landing
308259971 the system, low-level and test registries are byte-equal to
their approved snapshots under docs/archive/last_approved/.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-271 `Detail`: "baseline_snapshot.NEED_TIERS names the needs file's need tier (SN-ID) and stakeholder tier (STK-ID), and SNAPSHOT_TIERS…" -> "baseline_snapshot.NEED_TIERS names the needs file's need tier (SN-ID) and stakeholder tier (STK-ID), and SNAPSHOT_TIERS…"
- TC-269 `Expected`: 'Satisfies LLR-271 (parent SR-178): a need or stakeholder whose approved text moved is reported and briefed with its dif…' -> 'Satisfies LLR-271 (parent SR-178): a need or stakeholder whose approved text moved is reported and briefed with its dif…'
- TC-269 `Method`: "Driven on scaffolds made by the kit's bootstrap. An approved need is recorded by a seed; with no text moved it owes not…" -> "Driven on scaffolds made by the kit's bootstrap. An approved need is recorded by a seed; with no text moved it owes not…"

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested, bound to the text the verdict judged, and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
