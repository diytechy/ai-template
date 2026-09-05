## 2026-09-04 — A finished lane may still owe a round, and a pause stops only the claim

Two coordinator defects measured on the same day, both of them a lane that
could not be reached by the machinery that was supposed to reach it. They land
together because they are the same shape at two ends of `dispatch.run`'s tick:
the run decided a lane was beyond a worker's help — once because it was
finished, once because a pause was present — and in both cases a worker was
exactly what it needed.

Deferred open items: none — both defects are fixed at the reader that
held the wrong rule, each with a regression test driven against the pre-fix
code, and neither fix left an arm for a successor. The round-cap question
the first raises is already an owner ruling of 2026-09-03 (no cap yet), not
a remainder of this work.

### 1. A finished lane that owes a round is resumed before it is integrated

Measured on WI-590. The lane was DONE — every spec out of `active/`,
mechanically closed — and then its TREE moved: a supervisor rework of the
spec's `## Dispositions`, which is the adjudicator's own proper answer to a
CHANGES-REQUESTED round and the only rework that can move a record-only lane's
identity at all. On the next launch the coordinator handed the FINISHED branch
straight to the merge slot, which refused "no logged review round on
wi-590-… names its current tree", and the run exited. No worker ever resumed
to draw the owed round, so the supervisor drew rounds 011–014 by hand and
compiled a legacy rollup to get the lane merged.

`dispatch._parked_branches` now admits a finished branch that still owes a
round, and the existing parked-resume path carries it from there: `dispatch:
cycle N - resuming parked branch …`, whose worker's own resume arm
(`agent_loop.resume_owed_round`) schedules exactly the owed phases before any
build session. Only a finished branch that owes nothing goes to the slot.

`_round_owed` is COMPOSED from the two readers that already own the question
rather than being a third copy of the rule. `integrate._verdict_gate` is the
authority on whether the slot would refuse at all — it holds the reviewer dial,
the no-merged-outcome arm, the adjudication waiver and the legacy-rollup
migration window, so a coordinator that resumed past any of those would spend a
worker session against a satisfied slot and would break the hand-compiled
rollup recovery an operator is using this week. `kitlib.verdict.phases_owed` at
the governing identity is the NARROWING: it answers which declared phases were
never DRAWN at this tree. A refusal with nothing owed is one of the gate's
other three answers — a dissent, a reroll-until-green, or a contradicted
attestation — and none of them is fixed by drawing another round, so each still
stops the run for a human exactly as before.

The loop is guarded by progress rather than by a cap, which is the same bargain
every other resume takes: a resumed finished lane whose round returns
CHANGES-REQUESTED reworks as any lane would (the rework moves the tree, so the
next round is owed at a NEW identity), one that returns APPROVE owes nothing
and integrates on the next cycle, and a lane that draws nothing at all is
bounded by the iteration budget and the trunk-unmoved stall guard.
Tests: `test_a_finished_branch_that_owes_a_round_is_resumed_not_integrated`
(driven against the pre-fix line: it claims the frontier row instead and stalls),
`test_a_finished_branch_that_owes_nothing_goes_straight_to_the_slot`,
`test_the_worker_preflight_accepts_the_resumed_finished_lane` — the far end,
where the 2026-09-04 `stale_terminal_assignment` fix already lets a lane's own
closed rows through, driven here on the shape the coordinator now hands it so
the resume cannot be arranged upstream and refused downstream.

### 2. A fresh launch under `docs/work/pause` resumes the lanes in flight

Measured the same day: a fresh `agent_loop.py --root .` under a tracked pause
exited `EXIT_PAUSED` (8) at once, with an active claim whose lane was parked
mid-work. The pause's own contract says the opposite — §5.6 of
`docs/concurrency-restructure.md`, and the pause file's header: "pause = stop
CLAIMING. Everything in flight finishes, integrates and archives… the pause
never strands finished work on a branch." The operating recipe that grew around
the defect (delete the pause, launch, re-create it in the next commit) is a
person hand-simulating the drain the dispatcher owes.

The pause arm moved out of the tick top and into `dispatch._admit`, where the
one act a pause forbids lives. Under a pause the run now resumes every
parked lane and integrates every finished branch exactly as an unpaused run
does, and claims nothing new; `_paused_exit` ends the run with the banner and
exit 8 once the station is idle and nothing is left in flight. The
integrator's own refusal is still the one thing that can end a pause with work
on a branch — §5.6 says so, and that is the gate working rather than the pause
failing.

One deliberate ordering change: a pause with a DIRTY trunk and nothing in
flight now reports the dirty-trunk refusal (exit 2) rather than the pause
banner, because the drain the pause now performs needs a clean trunk like every
other merge does.
Tests: `test_drive_pause_appearing_mid_run_stops_the_next_claim` (rewritten —
it now asserts the in-flight lane finished AND merged while the next frontier
row stayed queued, which is the property the old test could not see),
`test_a_fresh_launch_under_a_pause_resumes_the_lane_in_flight`,
`test_a_pause_with_nothing_in_flight_exits_paused_at_once`.

### Ratchets

`dispatch.run` re-stamps DOWNWARD on the cognitive-complexity baseline (25 ->
21, SLOC 52 -> 43): the tick's pause banner-and-return block became one read
handed to `_admit`. `_admit` itself went to 17 with the pause arm and was
decomposed OUTWARD rather than bumped — `_admit_frontier` now holds the claim
half (frontier read, §A8 policy answer, enactment) and `_admit` holds the
station half (free lanes, parked branches, the pause), which is the split the
two questions were already making. No module-size row moved.
