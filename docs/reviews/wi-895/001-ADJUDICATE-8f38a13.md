# ADJUDICATE — WI-895 @ 8f38a13: lane checkpoint sitting

## amendment

Judged on the before/after cells against the 2026-10-10 anchors
(`docs/archive/last_approved`: LLR registry b6766302e, TC registry d40e9af00).
I read the chain to decide whether to bless. Up: SR-227 and SR-238; LLR-270's
`sr_refs` gains SR-238 in this change set, and TC-268's `verifies` gains it too.
Down: TC-268's Method and Evidence, and the tests the arms map names.

- [MEANING] LLR-270 Detail -> before: the KEEP-WARM paragraph fixes the ping's thread, serialisation, and when its log is recorded (clean versus dirty trunk, and at the run's end); it says nothing about a ping whose launch fails, so a build that swallowed every ping failure on the ping thread met it -> after: a ping whose launch raised `TreeNotEnded` hands it, with the finished call, to the dispatcher's thread, and the next tick or the run's end raises it. Over a clean trunk the call is recorded first, and a recording failure rides as the raised exception's context. Over a dirty trunk it is raised unrecorded, and the dirty-trunk hold does not defer it. Every other ping failure is recorded as an ERROR call and the run continues -> not the same: a case was added. A correct build of the old text, one that recorded `TreeNotEnded` as ERROR and carried on, fails the new text, which now makes the run stop. The ERROR-and-continue rule for other failures is also newly stated.
- [MEANING] TC-268 Method -> before: verify the due rules, the one-turn route gate, the held-lease skip, the blocking-launch threading and recording, the credential refusal, the dirty-trunk hold, the run-end recording, the shared dirty check and the registry-built warmer -> after: all of that, plus four assertions: a `TreeNotEnded` ping makes the next tick and the run's end raise, after recording over a clean trunk and unrecorded over a dirty one; a failed recording never replaces the exception; and an ordinary ping failure is still recorded as ERROR and swallowed -> not the same: the test case owes four checks it did not owe before. A run of the old method could pass with none of them.

Re-attestation judgement (the LLR and TC rungs are RELEASED, so blessing is mine): I would bless both rows.
- Up: the new clause answers SR-238's acceptance, which says the coordinator "stops with an error ... instead of continuing" when a session's processes cannot be ended. The keep-warm ping was the one caller still swallowing that stop, and LLR-270 now names SR-238 as a parent. The ERROR-and-continue rule keeps SR-227's "record each call like any other" for every other failure, so no SR-227 obligation regresses.
- A closed obligation: the actor (the dispatcher's thread), the trigger (`TreeNotEnded` from the ping's launch), both trunk states, the run's end, the context rule and the non-`TreeNotEnded` exemption are each stated and observable. No "should" stands in for a "must", and no threshold is left without units.
- Down: TC-268 binds each new arm to a test named in its Evidence. Those are `test_a_ping_whose_tree_cannot_be_ended_is_recorded_then_raised`, `test_over_a_dirty_trunk_the_unended_tree_is_raised_unrecorded`, `test_a_failed_recording_never_replaces_the_unended_tree` and `test_an_ordinary_ping_failure_is_still_recorded_and_swallowed`. I ran those four, together with the keep-warm threading and run-end tests, at this range: `10 passed, 67 deselected`. Nothing the new clause states goes unverified.
- One decision per row: the clause extends LLR-270's existing KEEP-WARM paragraph, which already owns the ping's thread hand-off and recording. Splitting it into a new LLR would separate one transfer route from its own recording rule.

VERDICT: MEANING rows=2

SITTING: JUDGED kinds=amendment
