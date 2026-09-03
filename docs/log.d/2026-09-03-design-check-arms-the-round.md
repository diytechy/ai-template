## 2026-09-03 — a committing DESIGN-CHECK arms the review round itself (owner ruling after the WI-579 lane)

Owner ruling, 2026-09-03 (this session): of the four findings the WI-579 lane
exposed, fix only the redundant rework cycle; the round cap, the review-path
tripwire and the blackout's placement stay as they are (rare; a supervisor
watches `agent-resume`; the blackout does not match the owner's intent but is
not touched yet). All four are recorded in the `docs/work/pause` reason at
`319f374a`.

**The change.** `agent_loop.build_bookkeeping`'s `DESIGN-CHECK` arm: a
committing design-check records itself as the committing build
(`on_committed_build` — its family is the one the reviewer must differ from)
and schedules the review and critique rounds exactly as the `BUILD` arm does;
a non-committing one still arms nothing; `next_phase` still resets to `BUILD`.
`NON_BUILD_PHASES` keeps `DESIGN-CHECK` (it is not a build for tier/routing).
Test: `tests/test_agent_loop_routing.py::test_a_committing_design_check_arms_the_review_round_itself`
drives both outcomes on a `RoutingState` with `train_evidence` stubbed.
PROCESS_OPTIONS's loop-held sentence and a `RESYNC_PACK.md` entry ship with it.
`agent_loop.py` size ratchet 2583 → 2587, reason in the baseline entry.

**The measurement it answers.** On the WI-579 lane (loop log of 2026-09-03):
13 DESIGN-CHECK sessions / 4.4 h did the rework; 13 BUILD sessions / 5.1 h
followed them only to re-verify and produce the commit that armed the round
(one of them NO-COMMIT, one re-running the full suite in-turn); 14 REVIEW-A
sessions / 1.2 h. Nine and a half builder hours per review hour.

**Left as found, for the record.** The WI-579 merge (`b5735bb8`) raised two
rows past the cognitive-complexity ratchet without a stamp:
`agent_common.commit_telemetry` 14 → 21 and `agent_loop.worker_endstate`
15 → 18 (measured at `319f374a` vs `c6b97493`). The sensor is armed from
DevStg-Impl, so the lane's bar did not red; `check_complexity --mode enforce`
on trunk now exits 1 on those two rows. Not this change's; it is the lane's
debt and is noted here rather than absorbed into a baseline stamp.
