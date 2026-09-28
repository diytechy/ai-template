+++
id = "WI-704"
title = "adjudicate: LLR-285, TC-296 - spine row(s) authored Drafted on merged trunk 1d84d77..500be4c await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-285", "TC-296"]
+++

## Deliverable

Ruled in spine-acts batch D by an independent Fable adjudicator from the kit's own brief, cross-reviewed by Codex Sol over three rounds (wave-5 rulings 49, 51, 52). The verdict (`docs/reviews/wi-704-adjudicate-llr-285-tc-296/001-ADJUDICATE-126cf5f2.md`) ends:

    OUTCOME: RETURN rows=2

The one act (ledger seq 6) copied the SR, LLR and TC registries: 13 rows approved (SR-220 on its batch-C approval, confirmed unchanged), 76 re-attested. Those include the 66 WI-695 waivers and SR-178 carried from batch C, and the 81 routed pointer changes ruled explicitly, four of them completed first.

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- LLR-285 authored in `docs/requirements/low-level-requirements.toml`
- TC-296 authored in `docs/test/test-cases.toml`

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.

## Dispositions

The adjudication is recorded at
`docs/reviews/wi-704-adjudicate-llr-285-tc-296/001-ADJUDICATE-126cf5f2.md`,
governing line `OUTCOME: RETURN rows=2`: LLR-285 is APPROVED (flipped and
anchored by batch D's act); TC-296 is RETURNED on one sentence of its `Method`
cell and stays `Drafted`, every cell byte-exact. One draft, one cell.

```toml
title = "TC-296 Method: state the standing reason the sweep excludes the committed dashboard, not its status"
workstream = "process"
safety_class = "spine"
buildtier = "quick"
priority = 3
specref = "docs/test/test-cases.toml"
sr_refs = ["SR-054"]
bar = "DevStg-Tests"
```

IN SCOPE — one cell, amended in place with status left `Drafted`, then the
first-approval adjudication the merge's sweep mints.

1. `TC-296.method`: the parenthetical "(the committed dashboard is an older
   renderer's markup, so it is left out)" states the row's own status at
   authoring time, and it is false at HEAD (`gen_trajectory.py --check`
   reports the dashboard up to date) while the test still excludes the
   shipped document. Keep the exclusion; state why it stands: the case
   asserts the CURRENT emitter, which only a document rendered now can
   evidence, whereas the committed artifact evidences whichever renderer
   last wrote it and its freshness is SR-070's contract. A reader with no
   history must not be able to reconstruct a correction from the cell.

OUT OF SCOPE: the test itself (it already sweeps the fresh fixtures only),
LLR-285 (approved), and whether the shipped artifact should ALSO be swept —
that would be a new claim, not a re-wording.
