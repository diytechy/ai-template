+++
id = "WI-742"
title = "adjudicate: TC-268 - spine row(s) authored Drafted on merged trunk 4cbb73c..3ecef62 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["TC-268"]
+++

## Deliverable

`OUTCOME: APPROVE rows=1`, from spine-acts batch K, act seq 13. The verdict
is
[001-ADJUDICATE-768b209.md](../../../reviews/wi-742-adjudicate-tc-268-spine-row/001-ADJUDICATE-768b209.md).

TC-268 is approved and anchored. Every Method clause maps to a named test,
and a flip showed no form finding.

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- TC-268 amended in `docs/test/test-cases.toml` (Method)

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.
