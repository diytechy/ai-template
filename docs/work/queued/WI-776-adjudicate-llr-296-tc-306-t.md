+++
id = "WI-776"
title = "adjudicate: LLR-296, TC-306, TC-309, TC-310 - spine row(s) authored Drafted on merged trunk f2bc66c..ba68016 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-296", "TC-306", "TC-309", "TC-310"]
+++

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- LLR-296 amended in `docs/requirements/low-level-requirements.toml` (Detail)
- TC-306 amended in `docs/test/test-cases.toml` (Expected, Method)
- TC-309 amended in `docs/test/test-cases.toml` (Evidence, Expected, Method)
- TC-310 amended in `docs/test/test-cases.toml` (Method, Verifies)

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.
