+++
id = "WI-691"
title = "adjudicate: LLR-205, LLR-206, LLR-262, LLR-274, LLR-275, LLR-276, TC-201, TC-203, TC-204, TC-273, TC-274, TC-275, TC-276 - spine row(s) authored Drafted on merged trunk 0ded5c7..da7ad24 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-205", "LLR-206", "LLR-262", "LLR-274", "LLR-275", "LLR-276", "TC-201", "TC-203", "TC-204", "TC-273", "TC-274", "TC-275", "TC-276"]
+++

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- LLR-205 amended in `docs/requirements/low-level-requirements.toml` (Detail, Rationale)
- LLR-206 amended in `docs/requirements/low-level-requirements.toml` (Rationale)
- LLR-262 amended in `docs/requirements/low-level-requirements.toml` (Detail)
- LLR-274 authored in `docs/requirements/low-level-requirements.toml`
- LLR-275 authored in `docs/requirements/low-level-requirements.toml`
- LLR-276 authored in `docs/requirements/low-level-requirements.toml`
- TC-201 amended in `docs/test/test-cases.toml` (Method)
- TC-203 amended in `docs/test/test-cases.toml` (Method)
- TC-204 amended in `docs/test/test-cases.toml` (Evidence, Method, Verifies)
- TC-273 authored in `docs/test/test-cases.toml`
- TC-274 authored in `docs/test/test-cases.toml`
- TC-275 authored in `docs/test/test-cases.toml`
- TC-276 authored in `docs/test/test-cases.toml`

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.
