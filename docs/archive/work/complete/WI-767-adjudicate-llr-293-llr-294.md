+++
id = "WI-767"
title = "adjudicate: LLR-293, LLR-294, TC-279, TC-306, TC-307 - spine row(s) authored Drafted on merged trunk 122816d..1f1dc64 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-293", "LLR-294", "TC-279", "TC-306", "TC-307"]
+++

## Deliverable

Spine-acts batch N, first-approval half: an independent Claude Opus 5.5
adjudicator returned LLR-293, LLR-294, TC-306 and TC-307 (`OUTCOME: RETURN rows=4`,
`docs/reviews/wi-767-adjudicate-llr-293-llr-294/001-ADJUDICATE-30ee386.md`).
TC-279 was not rendered by the composer (the gap WI-667 closed) and stays
Drafted, unruled. The follow-up is the single successor drafted in WI-766's
Dispositions; see "Follow-up for the returned rows" below.

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- LLR-293 authored in `docs/requirements/low-level-requirements.toml`
- LLR-294 authored in `docs/requirements/low-level-requirements.toml`
- TC-279 amended in `docs/test/test-cases.toml` (Inputs, MinWorkItems, Rubric, Trigger)
- TC-306 authored in `docs/test/test-cases.toml`
- TC-307 authored in `docs/test/test-cases.toml`

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.

## Follow-up for the returned rows

Verdict: `docs/reviews/wi-767-adjudicate-llr-293-llr-294/001-ADJUDICATE-30ee386.md`,
RETURN on all four rows. Their follow-up is not drafted here. LLR-293, LLR-294,
TC-306 and TC-307 are reworked by the single combined successor drafted in
WI-766's Dispositions section
(`docs/work/queued/WI-766-adjudicate-llr-254-sr-215-t.md`, minted at that row's
merge), together with SR-215, LLR-254, LLR-255, TC-247, TC-248, a new
check_trajectory case for LLR-294 and the gate-advance stage-gate step. One
lane carries them because two would couple through the snapshot: a registry
copy is refused while any approved row in it has drifted. TC-279 was not shown
and stays Drafted for an adjudication after WI-667 lands.
