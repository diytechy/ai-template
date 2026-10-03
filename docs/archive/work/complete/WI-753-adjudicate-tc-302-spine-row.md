+++
id = "WI-753"
title = "adjudicate: TC-302 - spine row(s) authored Drafted on merged trunk 5636237..85016f9 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["TC-302"]
+++

## Deliverable

TC-302's first approval (act seq 16): an independent Claude Opus 5.5 adjudicator
ruled APPROVE (WI-752 closed both findings of WI-751's return; a mutation probe
hiding archived rows failed the archive test, as it should). The C: drive filled
before its commit, so the coordinator executed its recorded steps: the verdict
commit, TC-302's status flip, and `intake.py snapshot --approves
"docs/test/test-cases.toml=WI-753"`. A first attempt chained a failed flip into an
empty act (seq 16, `approved = []`), caught before review and reset on the lane.
Sonnet 5.5 cross-review: SOUND at 952611cb.

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- TC-302 amended in `docs/test/test-cases.toml` (Evidence, Method)

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.
