+++
id = "WI-783"
title = "adjudicate: TC-309 - spine row(s) authored Drafted on merged trunk e95c85f..5afc927 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["TC-309", "TC-310"]
+++

## Deliverable

Act seq 25 (combined with WI-782): TC-309 and TC-310 are approved. The independent Claude Opus 5.5 adjudicator ruled `OUTCOME: APPROVE rows=2`. Probes showed WI-780's earlier returns closed: putting the case above the chain, dropping `Expected` from the refusal cells, a CRLF-to-LF rewrite of the registry, and listing an automated case each fail the tests. Codex Luna (high) cross-review: SOUND at 1b2bbfa4. Verdict: `docs/reviews/wi-783-adjudicate-tc-309-spine-row/001-ADJUDICATE-d040ad7.md`.

## Context

Carried in by the coordinator 2026-10-03: TC-310, returned by WI-780 for its tests only; WI-781 changed its tests and not its text, so no mint routes it. Sit this row with WI-782 in one combined act: WI-782's drifted approved TC rows block any first-approval copy of the test-case registry until they are re-attested.

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- TC-309 amended in `docs/test/test-cases.toml` (Expected, Method)

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.
