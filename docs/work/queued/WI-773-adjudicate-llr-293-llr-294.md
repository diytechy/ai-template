+++
id = "WI-773"
title = "adjudicate: LLR-293, LLR-294, TC-306, TC-311 - spine row(s) authored Drafted on merged trunk 00467fc..1ffd8c5 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-293", "LLR-294", "TC-306", "TC-311", "TC-307", "TC-279"]
+++

## Context

Carried in by the coordinator 2026-10-03: TC-307 (returned by WI-767 for its parent's gap, given no text change by WI-770, so no mint routes it), and TC-279 (an assumption-only observation case WI-767's composer could not render; WI-667 added the arm).

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- LLR-293 amended in `docs/requirements/low-level-requirements.toml` (Detail)
- LLR-294 amended in `docs/requirements/low-level-requirements.toml` (Detail)
- TC-306 amended in `docs/test/test-cases.toml` (Expected)
- TC-311 authored in `docs/test/test-cases.toml`

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.
