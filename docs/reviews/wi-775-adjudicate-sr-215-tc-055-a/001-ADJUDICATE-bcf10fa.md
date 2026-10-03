# WI-775 adjudication: SR-215 Rationale and TC-055 Expected (amendment)

Independent adjudicator: Claude Opus 5.5. I directed none of WI-772, WI-773 or WI-774.
The anchor is `docs/archive/last_approved` (SR and TC copies f7d5a12a).
`trace.reattest_model` at bcf10fa7 shows exactly these two approved cells drifted from their copies, and no other approved row in the SR, LLR or TC registries.
I read batch O's verdicts (WI-772 with its 2026-10-03 addendum, WI-773, WI-769) as prior findings; they bind nothing here.

- [MEANING] TC-055 Expected -> the standing limit says the recorded verdict is re-judged at a merge or release checkpoint when no result is on record, when a declared input changes, or when the record passes its max_age -> the standing limit says it is re-judged when no result is on record or the record passes its max_age, and otherwise only when its declared trigger fires after its closed-work floor -> not the same. A reader acting on the old text would re-judge on any change to a declared input; the new text forbids that unless the trigger fires and the floor is met. The "merge or release checkpoint" qualifier is also gone, so the old text's checkpoint scope no longer bounds the absence and expiry cases. The trigger set and the timing both moved.
- [MEANING] SR-215 Rationale -> the closed-work floor alone is the owner's cost limit, and it lets an accepted judgement outlive changes to what it judged for at most the configured number of closed work items -> the floor and the declared trigger are both cost limits; no change makes a judgement due again within the floor, a trigger narrows which changes can make it due at all, and so a judgement can stand on unjudged changes until a qualifying change meets the floor or the result expires -> not the same. The old cell stated an upper bound on staleness (N closed work items) that a reader could build or test against; the new cell withdraws that bound and adds a second limiting instrument. The cell is a rationale, not the acceptance, but the justification it gives now licenses behaviour the old one ruled out, and the method fails toward meaning.

## Re-attestation

The dial releases the SR and TC tiers, so the re-attestation is mine. I would bless both rows as written.

- TC-055: the new sentence agrees with SR-215's AcceptanceCriteria and with the case's own cells (`trigger = component:CMP-009`, `min_work_items = 10`, `max_age = 90`). It states the cadence through those cells rather than restating their values, so it cannot drift from them. The rest of the Expected is byte-identical to the blessed text.
- SR-215: the new Rationale is true of the AcceptanceCriteria and names no script, command, file or function (ruling R2). It corrects the false bound WI-772's addendum recorded.

A note that does not withhold the blessing: for a `release` or `stage-gate` trigger, the occasion that makes a case due is the checkpoint, not a change. "until a qualifying change meets the floor or its result expires" omits that earlier exit. It is still true as an upper bound (expiry always ends the standing), and it overclaims nothing. Worth tightening at the next amendment that touches the row; not a reason on its own.

Both rows are named in the combined act's `--reattests`.

VERDICT: MEANING rows=2
