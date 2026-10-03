+++
id = "WI-769"
title = "adjudicate: LLR-295, LLR-296, TC-308, TC-309, TC-310 - spine row(s) authored Drafted on merged trunk 30ee386..4ba5890 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-295", "LLR-296", "TC-308", "TC-309", "TC-310"]
+++

## Deliverable

Spine-acts batch O (act seq 22): LLR-295 and TC-308 approved; LLR-296, TC-309
and TC-310 returned. LLR-296 lists every assumption-naming test case where SR-033
says observation cases; TC-309 leaves LLR-295's two refusals untested; TC-310
follows LLR-296. Their follow-up is the combined draft in WI-773's Dispositions.

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- LLR-295 authored in `docs/requirements/low-level-requirements.toml`
- LLR-296 authored in `docs/requirements/low-level-requirements.toml`
- TC-308 authored in `docs/test/test-cases.toml`
- TC-309 authored in `docs/test/test-cases.toml`
- TC-310 authored in `docs/test/test-cases.toml`

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.

## Follow-up for the returned rows

Verdict: `docs/reviews/wi-769-adjudicate-llr-295-llr-296/001-ADJUDICATE-2256e4e.md`.
LLR-295 and TC-308 are approved. LLR-296, TC-309 and TC-310 return. Their
follow-up is not drafted here. It is ONE lane with WI-773's returned TC-306,
drafted with exact replacement cells and prohibitions in the `## Dispositions` section of
`docs/work/queued/WI-773-adjudicate-llr-293-llr-294.md`: all four are Drafted
rows that one first-approval sitting judges together. This section carries no
draft, so this row's merge mints nothing of its own; it is not a `## Dispositions`
section because one with no draft block refuses the mint.
