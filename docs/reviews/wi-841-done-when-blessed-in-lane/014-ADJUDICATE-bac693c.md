# WI-841 amendment adjudication at bac693c

Question: did each amendment change the requirement's MEANING, or only its CLARITY?
Judged on the before/after cells only, against the anchors copied at 927a09eb (LLR) and e9e5f846 (TC).

- [MEANING] LLR-262 Detail -> adjudication_bookkeeping receives the loop call's success from session_bookkeeping -> run_iteration records the loop call's success from call_succeeded in the plan, and adjudication_bookkeeping reads it from there -> the actor and the source of "success" changed. Success is now call_succeeded's derivation (LLR-310: exit 0, no timeout, no reported error result) rather than session_bookkeeping's. A loop correct under the old text that took success from session_bookkeeping, where a CLI-reported error could still read as success, fails the new text
- [MEANING] TC-326 Expected, Method -> an accepted, bound, valid verdict releases (anchor e9e5f846) -> it releases only if its call also succeeded; `test_the_loop_records_a_failed_calls_verdict_failed[1-False]` and `[0-True]` are added -> a new acceptance case, carried by both cells (the same move adjudication 013 judged; the TC anchor has not moved since)
- [MEANING] TC-278 Expected, Method -> on a held rung only an accepted CLARITY verdict permits a re-attestation (anchor e9e5f846) -> every added act naming a verdict, held or released, must name an accepted one; on a RELEASED rung an act naming an unaccepted verdict is refused, naming the verdict, and its whole act is refused, a first approval included -> new refusal cases on released rungs, carried by both cells
- [MEANING] LLR-306 Detail -> a pre-launch refusal removes the empty reservation and binding; accepted requires validation and an exit-0, in-deadline call; a non-zero exit or timeout is the failed-call outcome -> a pre-launch refusal removes ONLY the reservation and binding THIS call created; a successful call also requires NO REPORTED ERROR RESULT, and a reported error result is a failed-call outcome returned without reading the verdict -> a new failure condition and a narrowed cleanup. An entry point correct under the old text records accepted for an exit-0 call whose result reports an error, and may remove a binding another call owns. The new text forbids both
- [MEANING] LLR-310 Detail -> record_outcome records accepted only when the call succeeded and validation passes -> accepted only when call_succeeded has derived exit 0, no timeout and no reported error result, and validation passes; call_succeeded is derived once and shared by both routes, and a failed call is recorded failed without its verdict being read -> the success definition gained the reported-error condition and a single shared derivation, and a failed call's verdict must not be read

All five rows are MEANING, and the LLR and TC tiers' rung is RELEASED, so the blessing is the adjudicator's to give. I would bless each new text:

- The code matches. `session_service.call_succeeded` returns `code == 0 and not timed_out and not is_error`. `agent_loop` sets `plan["call_ok"]` from it, and `coordinator_adjudicate` uses the same function.
- The cited tests drive the new cases: `test_a_call_reporting_an_error_is_failed_on_both_routes`, `test_a_refused_reservation_leaves_a_binding_it_does_not_own` and `test_a_failed_call_is_recorded_failed_without_reading_its_verdict` in `tests/test_done_when_blessing.py`.
- TC-278 answers adjudication 013's return. Its released-rung cases now stand in their own sentence ("On a RELEASED rung, ..."), separate from the held-rung clause, matching the two released-rung tests it cites.

The re-attestation is taken in its own act. It includes TC-326, which 013 left unanchored behind TC-278.

VERDICT: MEANING rows=5
