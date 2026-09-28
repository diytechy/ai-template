+++
id = "WI-717"
title = "adjudicate: LLR-177, TC-172 - approved/routed cell(s) amended on merged trunk 4697024..b90e84b (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-177", "TC-172"]
+++

## Deliverable

Ruled in spine-acts batch F by an independent Fable adjudicator from the kit's own brief, routed pointer cells included. Codex Sol cross-reviewed it in two rounds (wave-5 rulings 58 and 59): NOT YET SOUND on the first act, and SOUND on the re-taken act, after the correction returned LLR-270 (a receipt phrase) and ruled LLR-177's `SR-Refs`. The verdict (`docs/reviews/wi-717-adjudicate-llr-177-tc-172/001-ADJUDICATE-d7e1be0e.md`) ends:

    VERDICT: MEANING rows=2

The one act (ledger seq 8) approved SR-226, LLR-287, TC-300, TC-263, TC-265, TC-266 and TC-267, and re-attested LLR-177 and TC-172 on a MEANING verdict. SR-222, SR-227, LLR-266 to LLR-270, TC-262, TC-264 and TC-268 returned on fourteen cells, mostly receipts and history in standing cells. The follow-up is WI-718's one Dispositions draft, minted at this merge.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-177 `Detail`: 'write_session_log passes every transcript through redact_secrets before the tracked per-session log (docs/iteration/NNN…' -> "write_session_log passes every transcript, and every header value (a verbatim raw-usage line can carry a runner's resul…"
- TC-172 `Method`: 'Plant credential-shaped values (an API key, a Bearer token, an AWS key id) in a transcript and write the session log: e…' -> 'Plant credential-shaped values (an API key, a Bearer token, an AWS key id) in a transcript and write the session log: e…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
