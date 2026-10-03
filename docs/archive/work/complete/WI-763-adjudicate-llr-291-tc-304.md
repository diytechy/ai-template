+++
id = "WI-763"
title = "adjudicate: LLR-291, TC-304 - spine row(s) authored Drafted on merged trunk 8773677..c58af7a await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-291", "TC-304"]
+++

## Deliverable

Spine-acts batch M, act seq 20 (with WI-762): the same adjudicator approved LLR-291
and TC-304 (first approval). The reviewer noted SR-006 is a thin parent for the path
trigger (its text ties selection to the stage) and recommends a one-clause
amendment, surfaced to the owner; and two untested pattern cases (comma separation,
case-sensitivity). Sonnet 5.5 cross-review: SOUND at 8415796a.

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- LLR-291 authored in `docs/requirements/low-level-requirements.toml`
- TC-304 authored in `docs/test/test-cases.toml`

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.
