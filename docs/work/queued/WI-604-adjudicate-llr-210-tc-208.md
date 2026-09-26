+++
id = "WI-604"
title = "adjudicate: LLR-210, TC-208 - spine row(s) authored Drafted on merged trunk 3b004c4..f395907 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-210", "TC-208"]
+++

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- LLR-210 authored in `docs/requirements/low-level-requirements.toml`
- TC-208 authored in `docs/test/test-cases.toml`

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.

## Done-when

- A verdict is committed under `docs/reviews/` at the path the brief names
  (`NNN-ADJUDICATE-<sha>.md` in this lane's folder), with one `APPROVE` or
  `RETURN` line for each of LLR-210 and TC-208 and exactly one
  `OUTCOME: APPROVE|RETURN rows=2` line, in a commit carrying this row's `WI:`
  trailer.
- Each approved row's `Status` moves from `Drafted` to `Approved` with no other
  registry cell changed, and `intake.py snapshot --approves` names only the
  registries holding an approved row, in one reviewed commit after the verdict
  commit.
- Each returned row keeps every cell byte-exact, and this spec's
  `## Dispositions` section drafts its follow-up.
