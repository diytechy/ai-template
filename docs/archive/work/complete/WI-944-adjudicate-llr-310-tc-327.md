+++
id = "WI-944"
title = "adjudicate: LLR-310, TC-327 - approved/routed cell(s) amended on merged trunk 1b4d9d7..e45ed5a (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-310", "TC-327"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second
sitting is held (the re-mint trap, S11 plan section 4.2; owner-agreed
close, 2026-10-03). WI-929's in-lane checkpoint sitting
`docs/reviews/wi-929/003-ADJUDICATE-1a07afc.md` blessed LLR-310 and TC-327
as MEANING+BLESS, and the lane's act turn took act seq 128, which
re-attested both. At the landing e45ed5a75 the low-level and test
registries are byte-equal to their approved snapshots under
docs/archive/last_approved/.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-310 `Detail`: 'A combined class accepts only amendment:<id>, first-approval:<id> and done-when:<id> Adjudicates tokens; it composes ea…' -> 'A combined class accepts only amendment:<id>, first-approval:<id> and done-when:<id> Adjudicates tokens; it composes ea…'
- LLR-310 `Rationale`: 'A shared checkpoint reduces adjudication launches only if no constituent judgement loses its scope or grammar. One pars…' -> 'A shared checkpoint reduces adjudication launches only if no constituent judgement loses its scope or grammar. One pars…'
- TC-327 `Expected`: 'The done-when brief displays the claim-bound checklist, changes, digest and bounded Context or refuses a missing prereq…' -> 'The done-when brief displays the claim-bound checklist, changes, digest and bounded Context or refuses a missing prereq…'
- TC-327 `Method`: 'Run test_the_done_when_brief_binds_the_digest_the_holds_compute, test_the_done_when_brief_refuses_an_unchanged_done_whe…' -> 'Run test_the_done_when_brief_binds_the_digest_the_holds_compute, test_the_done_when_brief_refuses_an_unchanged_done_whe…'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
