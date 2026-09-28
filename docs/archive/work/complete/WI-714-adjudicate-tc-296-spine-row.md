+++
id = "WI-714"
title = "adjudicate: TC-296 - spine row(s) authored Drafted on merged trunk b1dd35e..78fd8fc await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["TC-296"]
+++

## Deliverable

Ruled in spine-acts batch E by an independent Fable adjudicator from the kit's own brief, routed pointer cells included; cross-reviewed SOUND by Codex Sol. The verdict (`docs/reviews/wi-714-adjudicate-tc-296-spine-row/001-ADJUDICATE-8cd77ea6.md`) ends:

    OUTCOME: APPROVE rows=1

The one act (ledger seq 7) approved LLR-286, TC-299 and TC-296. SR-226, LLR-287 and TC-300 returned on form findings the gate raises only on Approved rows, which the adjudicator found by driving the flipped tree; the follow-up is WI-712's one Dispositions draft, minted at this merge.

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- TC-296 amended in `docs/test/test-cases.toml` (Method)

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.
