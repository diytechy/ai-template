+++
id = "WI-133"
title = "Dev-slice batching - next-wi batch: one session one review (strongest pin)"
workstream = "unattended"
needs = ["~WI-126"]
order = 132
+++

## Deliverable

WI-133 (2026-07-13, owner-directed at the session-economics sitting): dev-slice batching - docs/next-wi's value line may carry a ;-joined ORDERED batch of WI ids that one BUILD session executes in order (commit per WI), taking ONE review round (the loop already reviews a committing session's whole commit range - no dispatch change). agent_loop: _next_wi_ids() shared parse; build_tier_pin() batch-aware - single-id paths byte-identical (legacy strings pinned by the four WI-126 tests), a batch pins the STRONGEST member BuildTier (route up never down), unknown/invalid members named in the one loud line; new batch_advisories() - eligibility is ADVISORY never fatal (one dev-batch advisory line per violation: a spine-touching member with SR-Refs, a member hard-depending on another member; soft ~edges quiet); BUILD route branch prints them. Docs single-homed: PROCESS_OPTIONS 'Unattended operation' WI-126 bullet gains the batching block + one cross-ref sentence at 'Parallel for pre-dev, series for dev' (batching = the sanctioned relaxation for the cheap off-spine tail; deliberately does NOT touch docs/review-policy - that dial stays WI-123/OI-7); both meta launcher AGENT_PROMPTs + the session-protocol skill (source + .claude/.agents fan-outs byte-identical) name the batch form; docs/next-wi header documents it. Tests (test_agent_loop_review.py, 5 new): strongest-member pin routes, unknown-member-named-still-pins, clean-no-pin batch silent, both advisories fire + never block, soft-edge quiet. Dogfood: docs/next-wi = WI-098;WI-103 (the owner-ruled off-spine pair) is the first live batch. No spine change; no new SR (WI-126/WI-129 precedent).
