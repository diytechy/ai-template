# WI-841 amendment adjudication at 263e22d

Question: did each amendment change the requirement's MEANING, or only its CLARITY?
Judged on the before/after cells only, against the anchors copied at bc47c087 (LLR and TC).

- [MEANING] LLR-262 Detail -> after the call, run_iteration records the call's success and adjudication_bookkeeping records accepted only when that success and validation both hold, otherwise failed, and commits its binding -> session_body binds the composed request beside the verdict BEFORE the loop calls; adjudication_bookkeeping records through record_outcome against those bound kinds and takes its returned why as the completion obligation; a failed call is recorded failed, keeps that obligation and does not read its verdict -> new obligations: a pre-call binding on the loop route, recording against the bound kinds, completion tied to the recorded decision, and a failed call's verdict left unread. A loop that recorded correctly under the old text without binding at composition, or that read a failed call's verdict, fails the new one
- [MEANING] TC-326 Method -> run 18 named tests -> also run test_a_failed_loop_call_keeps_its_obligation_and_reads_no_verdict and test_the_loop_route_accepts_a_combined_sitting_on_its_bound_kinds -> two new acceptance cases, so a run that met the old Method does not meet the new one
- [MEANING] TC-327 Expected, Method -> the ENTRY POINT binds the requested kinds beside a combined verdict -> the entry point AND THE LOOP bind them, with test_the_loop_route_accepts_a_combined_sitting_on_its_bound_kinds added to the Method -> the binding obligation now covers a second actor, the loop route, and the Method adds a new case
- [MEANING] LLR-278 Detail -> every added act needs an accepted verdict of each KIND it takes among the branch's bindings; held re-attestation is checked by verdict_rulings -> every row the act flips needs an APPROVE ruling in an accepted first-approval part, and every row it re-attests needs a MEANING or CLARITY ruling in an accepted amendment part; a named verdict must also judge every row its act re-attests -> coverage moves from per kind to per row. An accepted verdict over OTHER rows satisfied the old text and is refused by the new one, and the named-verdict row check is new
- [MEANING] TC-278 Expected, Method -> each merging act carries an accepted verdict of each kind it takes -> each merging act's bindings rule every flipped row APPROVE and every re-attested row MEANING or CLARITY; a named verdict judges each row it re-attests; a new case: a first-approval part that RETURNs its only row approves nothing, while its combined act may still re-attest -> the same move from per-kind to per-row coverage, plus a new case
- [MEANING] LLR-306 Detail -> it creates the requested-kinds binding exclusively -> its exclusive binding goes through the shared bind_pending request binder -> the new text names a shared mechanism. An entry point that bound exclusively with its own writer met the old text and fails the new one
- [MEANING] LLR-310 Detail -> the binding records pending at reservation (the coordinator route); record_outcome records the outcome; every added act needs an accepted verdict of each kind it takes -> both routes bind pending before the call (the entry point at reservation, the loop at composition); record_outcome returns `(outcome, why)` and the loop takes that why as its completion obligation; the loop records against the kinds read back from its bound request; the accepted-verdict reader also returns per-part row rulings; coverage is per row (APPROVE for flips, MEANING/CLARITY for re-attestations), an accepted verdict over other rows authorizes nothing, and a named verdict must judge each row it re-attests -> a new actor (the loop) binds, a new return contract, and per-row authority in place of per-kind authority

Every row is MEANING. The LLR and TC tiers' rung is RELEASED, so the blessing is the adjudicator's to give. I would bless every new text:

- The cells state one rule two ways. Both routes bind the request before the call and record the outcome through one recorder, and the loop's completion is that same decision. An act's authority comes from accepted rulings on its OWN rows.
- The code matches:
  - `adjudicate_brief.bind_pending` is called by `coordinator_adjudicate` (exclusive, at reservation) and by `agent_loop.session_body` (at composition).
  - `record_outcome` returns `(outcome, why)`, reads back the bound kinds when given none, and does not read the verdict when the call failed.
  - `agent_loop.adjudication_bookkeeping` takes that why as `adjudication_owed`.
  - `kitlib.sitting` (`_AUTHORIZING`, `judged_rows`, `_ACT_KINDS`) refuses each row no accepted ruling judges, and refuses a named verdict that does not judge the rows its act re-attests.
- Every test the TC-326 and TC-327 Methods name exists in `tests/`. The RETURN-only first-approval case is exercised in `tests/test_snapshot_readers.py`.

The re-attestation is taken in its own act.

VERDICT: MEANING rows=7
