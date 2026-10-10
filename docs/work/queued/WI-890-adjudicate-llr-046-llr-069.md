+++
id = "WI-890"
title = "adjudicate: LLR-046, LLR-069, LLR-313, TC-069, TC-083, TC-333 - approved/routed cell(s) amended on merged trunk caafdb0..c31a23c (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-046", "LLR-069", "LLR-313", "TC-069", "TC-083", "TC-333"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-046 `Detail`: 'Computes advisory substance components and decay history; treats tripwires as gates and never rewards length. Severity …' -> 'Computes advisory substance components and decay history; treats tripwires as gates and never rewards length. Severity …'
- LLR-069 `Detail`: 'Uses one plan-table grammar for dual goal and single item runs. Resolves clause, SR, TC and interface references; valid…' -> 'Uses one plan-table grammar for dual goal and single item runs. Resolves clause, SR, TC and interface references; valid…'
- LLR-313 `Detail`: 'Round accepts only a full-lane review with no prior findings or a narrow review that names the prior findings file, and…' -> 'Round accepts only a full-lane review with no prior findings or a narrow review that names the prior findings file, and…'
- TC-069 `Expected`: 'A review verdict yields ordered F# clauses; a covered or reasoned-excluded finding passes; an uncovered finding, bad re…' -> 'A review verdict yields ordered F# clauses for its declared-severity findings only; a bracketed non-severity bullet yie…'
- TC-083 `Expected`: 'Scores and decay match fixtures; all tripwires fire as gates; length is never positive; persistence is stable; each mal…' -> 'Scores and decay match fixtures; all tripwires fire as gates; length is never positive; persistence is stable; each mal…'
- TC-083 `Method`: 'Run substance components, corroboration, tripwires, decay, verdict parsing, and CLI cases, including malformed or ambig…' -> 'Run substance components, corroboration, tripwires, decay, verdict parsing, and CLI cases, including malformed or ambig…'
- TC-333 `Expected`: 'A complete attended review or critique brief has no unfilled slot and carries the shipped review clauses, lane facts or…' -> 'A complete attended review or critique brief has no unfilled slot and carries the shipped review clauses, lane facts or…'
- TC-333 `Method`: 'Run test_a_rendered_review_brief_carries_the_kit_clauses_and_the_lane_facts, test_a_narrow_round_names_the_findings_it_…' -> 'Run test_a_rendered_review_brief_carries_the_kit_clauses_and_the_lane_facts, test_a_narrow_round_names_the_findings_it_…'
- TC-333 `Verifies`: 'SR-146;SR-235;LLR-313;IF-288;IF-289' -> 'SR-146;SR-235;LLR-313;IF-046;IF-047;IF-288;IF-289'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
