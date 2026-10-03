+++
id = "WI-764"
title = "adjudicate: LLR-292, TC-305 - spine row(s) authored Drafted on merged trunk 1d68869..5c74722 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-292", "TC-305"]
+++

## Deliverable

First approval of LLR-292 and TC-305 (act seq 21): an independent Claude Opus 5.5
adjudicator approved both (lane separation, test-bound for TC-055's T8, beside
LLR-120's box clearance with no clause held twice). Sonnet 5.5 cross-review: SOUND
at 89310142. Noted, not filed: the rubric's T8 still names the Knowledge graph,
which LLR-292 does not cover; this repo emits no Knowledge tab.

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- LLR-292 authored in `docs/requirements/low-level-requirements.toml`
- TC-305 authored in `docs/test/test-cases.toml`

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.
