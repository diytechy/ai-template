+++
id = "WI-1035"
title = "Review rounds and reviewers are declared in one [review] section that the coordinator cycle and the loop both read"
workstream = "process"
sr_refs = ["SR-040", "SR-234", "SR-154"]
needs = ["WI-1031"]
specref = "docs/plans/2026-10-11-review-churn/README.md#4-review-settings-a-cap-an-exit-and-a-convergence-round"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed on trunk on 2026-11-21 so the review-churn plan's phase 3 is not lost
(queue-drill hand-off §3.3 N2). This is item 4's settings, which phase 3
places beside item 10's steps.

Ruled (rulings table, item 4): `iteration_reviewers = 0`,
`iteration_rounds_max = 0`, `full_reviewers = 2`, `full_rounds_max = 3`,
`on_limit = "adjudicate"` and `block_on = ["BLOCKER", "MAJOR"]`. The last
allowed round runs in the convergence stance, and severity is tied to
reachability. Revision 37's three reviewers apply to that program only, and
two stays the norm.

Already landed, so not in scope: the text pieces. WI-911 put severity tied
to reachability and the convergence stance into
`prompts/reviewer.template.md`. `review_brief.py` renders
`--stance convergence`. The coordinator-cycle skill already runs counted
rounds 1 and 2 plainly and the third in convergence. The dispute template
already rules at the cap.

Missing, and this row's scope: the settings. The kit has one review dial,
`[policies] review_rounds` (0, 1 or 2; it is 1 in this repo and in the
template). Despite its name it counts reviewers, and only the managed loop
reads it (`agent_loop.py`, `agent_policy.py`, `kitlib/verdict.py`). The
coordinator cycle hard-codes its shape in skill text.

Settled here:

- **A new `[review]` table** holds the six ruled keys, declared in WI-1031's
  schema. The last round's convergence stance is fixed behaviour, not a key
  (the ruling states it as behaviour). `reviewer_families` is item 7's and
  is not added here.
- **`[reviewer]` stays as it is:** WI-887's session-retention dials, a
  different concern. The template header names the split. The draft row
  WI-802 uses "[review]" for a session family; whichever lands second
  reconciles the name.
- **`review_rounds` migrates into `full_reviewers`,** keeping its value,
  since a re-sync never overwrites a value (item 10's ruling). The template
  ships the ruled 2. This repo keeps its 1 until the operator changes it by
  a reviewed commit.
- **Both routes read the section:** the managed loop in place of
  `review_rounds`, and the coordinator cycle through `review_brief.py`,
  which renders the round count and the convergence stance from it.

## Done-when

- [ ] `[review]` is in `process.toml`, its template and the schema, with the
      ruled defaults. `review_rounds` is gone, and a file still holding it
      is refused, naming the new key.
- [ ] The managed loop and `review_brief.py` read the section, and a test
      for each changes a key and sees the behaviour follow.
- [ ] The coordinator-cycle skill points at the section instead of stating
      round counts. The dogfooded copies stay byte-equal.
- [ ] `RESYNC_PACK.md` carries this row's entry.
