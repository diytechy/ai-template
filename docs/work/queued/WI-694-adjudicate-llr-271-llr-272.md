+++
id = "WI-694"
title = "adjudicate: LLR-271, LLR-272, LLR-273, LLR-277, LLR-278, TC-269, TC-270, TC-271, TC-272, TC-278 - spine row(s) authored Drafted on merged trunk e520b6e..fe96ec6 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-271", "LLR-272", "LLR-273", "LLR-277", "LLR-278", "TC-269", "TC-270", "TC-271", "TC-272", "TC-278"]
+++

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- LLR-271 authored in `docs/requirements/low-level-requirements.toml`
- LLR-272 authored in `docs/requirements/low-level-requirements.toml`
- LLR-273 authored in `docs/requirements/low-level-requirements.toml`
- LLR-277 authored in `docs/requirements/low-level-requirements.toml`
- LLR-278 authored in `docs/requirements/low-level-requirements.toml`
- TC-269 authored in `docs/test/test-cases.toml`
- TC-270 authored in `docs/test/test-cases.toml`
- TC-271 authored in `docs/test/test-cases.toml`
- TC-272 authored in `docs/test/test-cases.toml`
- TC-278 authored in `docs/test/test-cases.toml`

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.
