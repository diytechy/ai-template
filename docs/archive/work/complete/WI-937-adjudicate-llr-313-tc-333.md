+++
id = "WI-937"
title = "adjudicate: LLR-313, TC-333 - approved/routed cell(s) amended on merged trunk 1a182d1..87ceeaf (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-313", "TC-333"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second
sitting is held (the re-mint trap, S11 plan section 4.2; owner-agreed
close, 2026-10-03). WI-930's in-lane checkpoint sitting
`docs/reviews/wi-930/003-ADJUDICATE-6cbacac.md` blessed LLR-313 and TC-333
as MEANING, and act seq 123 re-attested them. At the landing 87ceeafea the
system, low-level and test registries are byte-equal to their approved
snapshots under docs/archive/last_approved/.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-313 `Detail`: 'Round accepts only a full-lane review with no prior findings or a narrow review that names the prior findings file, and…' -> 'Round accepts only a full-lane review with no prior findings or a narrow review that names the prior findings file, and…'
- TC-333 `Expected`: 'A complete attended review or critique brief has no unfilled slot and carries the shipped review clauses, lane facts or…' -> 'A complete attended review or critique brief has no unfilled slot and carries the shipped review clauses, lane facts or…'
- TC-333 `Method`: 'Run test_a_rendered_review_brief_carries_the_kit_clauses_and_the_lane_facts, test_a_narrow_round_names_the_findings_it_…' -> 'Run test_a_rendered_review_brief_carries_the_kit_clauses_and_the_lane_facts, test_a_narrow_round_names_the_findings_it_…'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
