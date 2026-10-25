+++
id = "WI-975"
title = "adjudicate: LLR-069, LLR-310, LLR-314, LLR-315, TC-069, TC-327, TC-334 - approved/routed cell(s) amended on merged trunk a7c89a5..e592e5e (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-069", "LLR-310", "LLR-314", "LLR-315", "TC-069", "TC-327", "TC-334"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-069 `Detail`: 'Uses one plan-table grammar for dual goal and single item runs. Resolves clause, SR, TC and interface references; valid…' -> 'Uses one plan-table grammar for dual goal and single item runs. Resolves clause, SR, TC and interface references; valid…'
- LLR-310 `Detail`: 'A combined class accepts only amendment:<id>, first-approval:<id> and done-when:<id> Adjudicates tokens; it composes ea…' -> 'A combined class accepts only amendment:<id>, first-approval:<id> and done-when:<id> Adjudicates tokens; it composes ea…'
- LLR-314 `Detail`: 'kitlib.dispute accepts one TOML findings file with only a non-empty `range` and a non-empty `[[finding]]` list. Each fi…' -> 'kitlib.dispute accepts one TOML findings file with only a non-empty `range` and a non-empty `[[finding]]` list. Each fi…'
- LLR-315 `Detail`: 'dispute_values accepts exactly one findings-file reference from an adjudication row, reads it through kitlib.dispute, a…' -> 'dispute_values accepts exactly one findings-file reference from an adjudication row, reads it through kitlib.dispute, a…'
- TC-069 `Expected`: 'A review verdict yields ordered F# clauses for its declared-severity findings only; a bracketed non-severity bullet yie…' -> 'A review verdict yields ordered F# clauses for its declared-severity findings only; a bracketed non-severity bullet yie…'
- TC-069 `Method`: 'Run dual and single plan coverage, reference, graph, exclusion, review-verdict finding, dispute-ruling, SR/TC-diff, abs…' -> 'Run dual and single plan coverage, reference, graph, exclusion, review-verdict finding, dispute-ruling, SR/TC-diff, abs…'
- TC-069 `Tier`: 'Smoke' -> 'Full'
- TC-327 `Expected`: 'The done-when brief displays the claim-bound checklist, changes, digest and bounded Context or refuses a missing prereq…' -> 'The done-when brief displays the claim-bound checklist, changes, digest and bounded Context or refuses a missing prereq…'
- TC-327 `Method`: 'Run test_the_done_when_brief_binds_the_digest_the_holds_compute, test_the_done_when_brief_refuses_an_unchanged_done_whe…' -> 'Run test_the_done_when_brief_binds_the_digest_the_holds_compute, test_the_done_when_brief_refuses_an_unchanged_done_whe…'
- TC-334 `Expected`: 'A dispute brief contains every requested finding and position verbatim with independently derived range facts and a rev…' -> 'A dispute brief contains every requested finding and position verbatim with independently derived range facts and a rev…'
- TC-334 `Method`: 'Run the dispute tests that compose a brief carrying every finding, held position, range fact and review-scope link; ref…' -> 'Run the dispute tests that compose a brief carrying every finding, held position, range fact and review-scope link; ref…'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested, bound to the text the verdict judged, and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
