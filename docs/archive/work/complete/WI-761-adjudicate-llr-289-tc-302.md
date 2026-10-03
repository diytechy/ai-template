+++
id = "WI-761"
title = "adjudicate: LLR-289, TC-302 - approved/routed cell(s) amended on merged trunk 75acecb..4873bef (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-289", "TC-302"]
+++

## Deliverable

Act seq 18: an independent Claude Opus 5.5 adjudicator ruled LLR-289 detail and
TC-302 method/evidence (WI-759's example-reference amendment) MEANING and
re-attested both; true of `open_item_wi_ref_findings` and
`test_example_wi_refs_are_inert`. Sonnet 5.5 cross-review: SOUND at b790bd90.
Verdict: `docs/reviews/wi-761-adjudicate-llr-289-tc-302/001-ADJUDICATE-ca6d79a.md`.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-289 `Detail`: "Report each real open item's wi_refs entry that names no work item, checking pending and ruled history against live and…" -> "Report each real open item's wi_refs entry that names no work item, checking pending and ruled history against live and…"
- TC-302 `Method`: 'For pending and ruled open-item rows whose wi_refs names an absent work item, assert one finding naming the item and th…' -> 'For pending and ruled open-item rows whose wi_refs names an absent work item, assert one finding naming the item and th…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
