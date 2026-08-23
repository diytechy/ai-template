+++
id = "WI-264"
title = "Wire next_primary (owner ruling 2026-07-21, repo-review-2026-07-21 M-34 policy half): the win-stay/lose-shift escalation output becomes real - the draw/escalation path consumes next_primary so the documented policy executes, building on the already-applied arithmetic fixes (float margin default + float() env parse). Tests must use pipeline-reachable margins (bounded by 1.0), not fabricated margin:3; cover both stay (winner above threshold) and shift (below threshold) paths and the interaction with the WI-263 cross-train weighted draw (policy override vs weighted baseline precedence must be explicit in the spec). LIVENESS (fail-open, per the 2026-07-21 author-identity lesson): this wires dormant code into the LIVE routing path - a None/invalid/disabled-provider next_primary MUST fall back to the ordinary weighted draw, never wedge or fail a session; add a test that a bogus next_primary degrades to a valid draw rather than halting"
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
order = 261
+++

## Deliverable

Wire next_primary (agent_route.py + agent_loop.py): the win-stay/lose-shift escalation output is now consumed in the live review draw via winstay_preferred_ids() composed into select()'s preferred_ids — on a WIN the winner is pinned ahead of the weighted baseline (pin>weights, overrides WI-263), on a LOSS/None it resolves to () and the weighted draw is untouched (lose-shift); two-layer fail-open (invalid/disabled/off-tier/non-string next_primary degrades to the weighted draw, never wedges the session). Gated to review draws. Pipeline-reachable margins, e2e + managed-subprocess tests, bite-proven. Adversarial REVIEW-A APPROVE f=0.
