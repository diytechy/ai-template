+++
id = "WI-728"
title = "adjudicate: LLR-286 - approved/routed cell(s) amended on merged trunk 5124c93..d05b4b0 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-286"]
+++

## Deliverable

`VERDICT: MEANING rows=1`, from spine-acts batch G. The verdict is
[001-ADJUDICATE-f1733da.md](../../../reviews/wi-728-adjudicate-llr-286-approved/001-ADJUDICATE-f1733da.md).

LLR-286's amendment is blessed: "live" means live in any carrier form,
which matches SR-226, and TC-299's new case drives it. It is not anchored
yet, because the LLR registry's snapshot is refused while WI-726's returned
LLR-223 drifts. Its re-attestation is owed, and it is carried in WI-724's
Dispositions draft.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-286 `Detail`: 'retire(root, row_id, reason, successor, date) judges the whole retirement before writing anything: the id is SN, SR, LL…' -> 'retire(root, row_id, reason, successor, date) judges the whole retirement before writing anything: the id is SN, SR, LL…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
