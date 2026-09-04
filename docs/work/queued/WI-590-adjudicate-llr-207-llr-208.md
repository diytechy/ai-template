+++
id = "WI-590"
title = "adjudicate: LLR-207, LLR-208, TC-205, TC-206 - spine row(s) authored Drafted on merged trunk e507b76..c5c4a8b await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-207", "LLR-208", "TC-205", "TC-206"]
+++

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- LLR-207 amended in `docs/requirements/low-level-requirements.toml` (Detail)
- LLR-208 amended in `docs/requirements/low-level-requirements.toml` (Detail)
- TC-205 amended in `docs/test/test-cases.toml` (Evidence, Method)
- TC-206 amended in `docs/test/test-cases.toml` (Evidence, Method)

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.
