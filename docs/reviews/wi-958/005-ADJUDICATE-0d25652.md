# WI-958 checkpoint sitting at 0d25652

## first-approval

Eleven lane-added rows await a first approval: SR-242, LLR-343 and LLR-344, and TC-375 to TC-382. I read them as two chains. The first is SR-154, with its approved LLRs and TCs, and LLR-344 and TC-375 to TC-377 beside them. The second is SR-242, with LLR-343 and TC-378 to TC-382. I also read the lane's arms map, the hat roster, the interface notes, and the tests. All twenty-two evidence nodes exist.

The batch is mixed. The seven test cases whose text stands on its own are approved. Four rows go back, for one shared gap in the derivation record and for the cap close's fields.

**On the parent question the lane put:** SR-154 is an acceptable parent for LLR-344. SR-154 obliges the loop to obtain each review verdict the policy requires. A precondition on when the loop draws a reviewer is a design decision under that obligation, not a second boundary behaviour. The attended route's SR-241 does not fit the loop, as two review rounds found. The precondition is still content SR-154 does not demand, so it is legitimate only as a recorded derivation, and that record is what is missing below.

- [RETURN] SR-242 -> the obligation: when an unattended lane reaches its declared maximum of consecutive red review-bar rounds, the delivered dispatcher closes it partial and reports the cap outcome separately. Its acceptance: bounded by the maximum, closing partial rather than escalating through the declared approval level, the close naming the count, the maximum and the final review-bar result, and distinguishable from a stall, crash or ordinary completion -> what its chain shows: the text is sound. The `When` is fronted. It speaks in artifact classes and names no file. Its acceptance carries observable pass lines. Its lens, PERFORMANCE, fits: that hat's `listens_for` names an operating-cost risk left unassessed, and unbounded red rounds are exactly that. LLR-343 decomposes it -> why it is not ready: the row is labelled DERIVED, and two of the derivation's three records are missing.
  - (1) **No perspective record.** No `*.perspectives.toml` covers this lane's rows; the only lane record present is WI-957's. So §2(c3)'s check cannot run, and the hats that apply to a fail-closed cap (INTEGRITY-RECOVERABILITY, UNATTENDED-OPS) have no recorded answer. This is the gap WI-957's sitting 003 returned and its lane answered with `hats.py record`.
  - (2) **No feedback upward.** §2(c)(iii) asks that a derived row be fed back to the need it was derived from. SR-241 states its feedback ("Fed back to the needs: ..."), but this Rationale argues the lens and the rejected alternative and stops there.
- [RETURN] LLR-343 -> the obligation:
  - Read the declared maximum as a positive integer, 3 only when the setting is absent, refusing every other shape before a session or claim and naming the key and its line or the parse cause.
  - Count distinct recorded red build commits since the newest verified review attestation, resetting at it. An unreadable log counts as one red; an unlistable history has no count and reads as at the cap.
  - Exit 12 at the maximum, both at run start and after each red record.
  - Have the dispatcher treat exit 12 as its own decided partial close, with reason, split authority, suggested tier and undelivered review bar, leaving the red landing to quarantine.

  -> what its chain shows: every stated arm is fail-closed where history is unknown, and each has a named TC case (TC-378 to TC-382) -> why it is not ready: it does not decompose all of its parent's acceptance. SR-242 requires that the partial close name the count, the maximum and the final review-bar result. This row says only that the cap decision "reports the count", and lists the close's fields as reason, split authority, suggested tier and undelivered review bar. A reader cannot tell whether the maximum and the final result are carried, and a refactor that dropped them would keep the row true. State that the close's reason names the count, the maximum and the final review-bar result. Its parent is also returned, and this row re-sits with it.
- [RETURN] LLR-344 -> the obligation: draw a queued unattended review round only over a tip carrying a verified review attestation. Otherwise run the review bar once through its one producer and record the result: green draws the round; red drops it and rebuilds with the refusal. Never produce again a result already recorded for the governing build commit. Apply this to fresh, resumed, post-narrow and adjudication-triggered draws -> what its chain shows: the contract is clear, refactor-proof and fail-closed, names no code symbol and has no `shall`. TC-375 to TC-377 drive each draw route and both bar colours, and TC-379's once-only cases back the no-repeat arm -> why it is not ready: its Rationale calls it "A DERIVED obligation through the PERFORMANCE lens", but the row has no `Hat-Refs` cell. §2(c) is explicit that a prose label is not the record, because it resolves against nothing. Its parent SR-154 carries only UNATTENDED-OPS, so PERFORMANCE is exactly the own ref §3 says a design row earns when it bears a hat no parent carries. It also shares SR-242's missing perspective record. Its text otherwise stands, so the fix is one cell plus the record, with no change to the Detail.
- [APPROVE] TC-375 -> the obligation: a red review-bar build draws no review, writes one red record naming the build commit, and the next build receives the recorded failure tail -> what its chain shows: it verifies SR-154 and LLR-344's red arm, through three named, existing cases covering a long summary's cause and final diagnostic -> why it is ready: Expected is an observable condition, and the Method asserts exactly it. Its text does not depend on the Hat-Refs fix LLR-344 owes, and its `Verifies` stays under the parent this sitting accepts.
- [APPROVE] TC-376 -> the obligation: a green review-bar build attests exactly once before the queued review is drawn -> what its chain shows: it holds LLR-344's green arm, through one named case -> why it is ready: an observable once-then-draw condition, unaffected by LLR-344's pending cell.
- [APPROVE] TC-377 -> the obligation: an unattested resumed round runs the producer once, green drawing and red not, and post-narrow and adjudication-triggered rounds draw only over a verified attestation -> what its chain shows: it holds LLR-344's route-coverage arm (all four draw routes), with the resumed case parametrized over both colours -> why it is ready: each route the LLR names has a driven case, and Expected states the condition.
- [APPROVE] TC-378 -> the obligation: distinct red build records survive a resume and reset at a verified green, an unreadable log counts as one red, and an unlistable history answers no count, read as at the cap -> what its chain shows: it holds LLR-343's counting and fail-closed arms through five named cases, a resume to the cap included -> why it is ready: every clause is observable, and none depends on the close-field text LLR-343 still owes.
- [APPROVE] TC-379 -> the obligation: an unrecorded red is rechecked once and counted once, a build ending in a record-only commit counts once, one build recorded twice counts once, and the attest phase is inert to every phase reader -> what its chain shows: four named cases hold "distinct build commits define the count" -> why it is ready: an observable count definition, independent of the pending rework.
- [APPROVE] TC-380 -> the obligation: an unparseable process file or a non-table build section, and a bad maximum, refuse at both preflights, naming the cause and starting no session or claim -> what its chain shows: it holds LLR-343's refusal arm at the worker and the dispatcher -> why it is ready: an observable refusal with its pass line (no session, no claim).
- [RETURN] TC-381 -> the obligation it claims: at the cap the worker exits 12, also before any session for a lane resumed at the cap, and the dispatcher produces the typed partial close and its quarantine, while one fewer red does not close -> what its chain shows: its dispatcher case asserts the partial claim, "3 consecutive red rounds", the final bar output, the split authority and the quarantine. Its Expected says only "the typed partial close" -> why it is not ready: it is the TC for SR-242's two remaining acceptance arms, and its text claims neither.
  - It does not state what the close must name: the count, the maximum and the final review-bar result.
  - It does not state that the cap closes partial rather than escalating through the declared approval level.

  The evidence asserts most of the first, and nothing asserts the second. Add both to Expected and Method, matching LLR-343's restated close fields, and cite or add a case showing no approval-level hold or page at the cap.
- [APPROVE] TC-382 -> the obligation: an absent maximum reads 3, and zero, negative, boolean, text and floating values each refuse, naming their line and key -> what its chain shows: one named unit case over every shape LLR-343 names -> why it is ready: a closed input table with its outcome per value, and Smoke is honest for a pure reader.

OUTCOME: RETURN rows=11

## Returns answered in the lane

```toml
title = "WI-958 spine rework: the derivation records for SR-242 and LLR-344, the cap close's named fields in LLR-343 and TC-381; re-sit the four"
workstream = "process"
sr_refs = ["SR-242", "SR-154"]
needs = ["WI-958"]
safety_class = "ordinary"
buildtier = "medium"
```

This is spine text, plus one record file. Code changes only if no case yet shows that the cap neither holds nor pages through the approval level.

1. **The perspective record:** write the lane's perspective record beside its plan (`python project-trajectory/scripts/hats.py record docs/plans/WI-958/plan.perspectives.toml --row SR-242 --row LLR-343 --row LLR-344 --by <who>`), with a one-line `no_finding` for each applicable hat that produced nothing. It must pass `record <file> --check --strict`.
2. **SR-242:** add its feedback to the needs to the Rationale, as SR-241 does.
3. **LLR-344:** add `hat_refs = ["PERFORMANCE"]`. Its Detail is unchanged.
4. **LLR-343:** state that the partial close's reason names the count, the maximum and the final review-bar result.
5. **TC-381:** state the close's three named fields and the no-escalation arm in Expected and Method, and cite or add the case for the no-escalation arm.

Then re-sit SR-242, LLR-343, LLR-344 and TC-381 for first approval. The seven test cases this sitting approves keep their approval, because none of these changes touches their text or their `Verifies`.

SITTING: JUDGED kinds=first-approval
