+++
id = "WI-760"
title = "adjudicate: LLR-290, TC-303 - spine row(s) authored Drafted on merged trunk a8dee5b..3a4afaf await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-290", "TC-303"]
+++

## Deliverable

First approval of LLR-290 and TC-303 (act seq 19): an independent Claude Opus 5.5
adjudicator approved both (WI-757 closed batch L's two findings; both true of
`_observe_compaction` and `CodexAdapter.compaction`). Sonnet 5.5 cross-review:
SOUND at 10fe2b5f. The lane's act (seq 18) collided with WI-761's, which landed
first, so the coordinator retook the snapshot on the merged tree: no refusal for
the same arguments, `last_approved/` reset to trunk, the exact command re-run.
Verdict: `docs/reviews/wi-760-adjudicate-llr-290-tc-303/001-ADJUDICATE-75acecb.md`.

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- LLR-290 amended in `docs/requirements/low-level-requirements.toml` (Detail)
- TC-303 amended in `docs/test/test-cases.toml` (Method)

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.
