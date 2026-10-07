# WI-841 amendment adjudication at 82d78a2

Question: did each amendment change the requirement's MEANING, or only its CLARITY?
Judged on the before/after cells only, against the anchors copied at 5aba34ee (LLR and TC).

- [MEANING] LLR-309 Detail -> build_hold is asked BEFORE a build or rework session; review sessions and adjudication rows are not held -> build_hold is asked AFTER routed_session selects a build or rework session; review sessions, critiques and adjudication rows are not held; worker_endstate asks no hold -> the hold point moves from before the session to after routing selects it. A critique is now an explicit exemption, and worker_endstate is forbidden from holding. An implementation correct under the old text could check the hold before routing, or in worker_endstate, and the new text refuses both
- [MEANING] TC-325 Expected, Method -> exemptions: the editing commit, adjudication rows, review sessions and test runs; 14 named tests -> critique sessions are added to the exemptions; dispatch applies its hold after routing selects a build or rework session, driven through routed_session; two new tests (test_a_build_after_a_dirty_completed_lane_is_held_at_dispatch, test_a_resumed_blocked_lanes_first_build_is_held_at_dispatch) -> a new exempt actor, a new timing condition and two new acceptance cases, so a run that met the old Method does not meet the new one

Both rows are MEANING. The LLR and TC tiers' rung is RELEASED, so the blessing is the adjudicator's to give. I would bless both new texts:

- The cells state one rule. The Done-when hold sits at the one point a session is dispatched, after routing has decided that the session builds.
- The code matches. `agent_loop.routed_session` routes first, then calls `build_hold` only when the plan is neither a review, a critique nor an adjudication brief. `build_hold` asks `kitlib.done_when.lane_hold`, and `worker_endstate` holds nothing.
- Every test the TC-325 Method names, including both new ones, exists in `tests/test_done_when_blessing.py`.

The re-attestation is taken in its own act.

VERDICT: MEANING rows=2
