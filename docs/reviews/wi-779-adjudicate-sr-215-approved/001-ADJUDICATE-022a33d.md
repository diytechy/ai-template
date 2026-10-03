# WI-779 adjudication: SR-215 Rationale (amendment)

Independent adjudicator: Claude Opus 5.5. I directed none of WI-775, WI-776 or WI-778.
The anchor is `docs/archive/last_approved` (SR copy f7d5a12a), which still holds the text last blessed: the "at most the configured number of closed work items" form.
`trace.reattest_model` at 022a33d5 shows SR-215's `Rationale` as the only approved cell drifted from its copy in the SR, LLR and TC registries. TC-309 and TC-310 are Drafted and are WI-780's.
The arbitration ruling B sentence was checked against the code, not taken on authority. I read `observation_cadence.Cadence.eligible`, `rejudge._judge`, `rejudge._expired`, `assumption_rules`'s expiry refusal, and SR-215's Requirement and AcceptanceCriteria.

- [MEANING] SR-215 Rationale -> the closed-work floor alone is the owner's cost limit, and it lets an accepted judgement outlive changes to what it judged for at most the configured number of closed work items: an upper bound on staleness a reader could build or test against -> the floor and the declared trigger are both cost limits; no change or checkpoint makes an accepted judgement due again within the floor of its latest record; a declared trigger replaces input changes with the change or checkpoint it names; so a judgement can stand on unjudged changes until a qualifying change or checkpoint meets the floor, or until its result expires -> not the same. The old cell bounded staleness from above. The new one withdraws that bound and states a lower bound (the floor) plus a substitution (the trigger in place of input changes). A builder honouring the old bound would make a triggered case due on an input change after N closed items, and the new text says it must not. The cell is a rationale, not the acceptance, but the method fails toward meaning.

## Re-attestation

The dial releases the SR tier, so the re-attestation is mine. I would bless the whole cell as written:

- **"no change or checkpoint makes an accepted judgement due again within the configured number of closed work items of its latest record"**: true.
  - `eligible` returns False whenever `count < floor`, before reading any trigger.
  - `count` is the number of distinct terminal archived WI ids added since the commit that added the latest record.
  - The floor is `max(policy, case MinWorkItems)`, matching the acceptance's "a case may raise that number but not lower it". A zero policy floor makes the clause vacuous, not false.
  - Expiry is neither a change nor a checkpoint, and the sentence keeps it as a separate end.
- **"a declared trigger replaces input changes with the change or checkpoint it names"**: true for all four trigger kinds.
  - In `rejudge._judge`, a row with a `Trigger` is due as WHY_TRIGGER when eligible, and otherwise not due. The input digest is never read for it.
  - `files:` and `component:` name a change.
  - `release` and `stage-gate` name a checkpoint (`observation_cadence.py:141`, `checkpoint == trigger and since != self.revision`), with no change required. This is the case ruling B found the earlier text got wrong, and this sentence now covers it.
- **"so a judgement can stand on changes it never judged until a qualifying change or checkpoint meets the floor or its result expires"**: true.
  - With no trigger, the qualifying change is an input-digest change, under the same floor (acceptance: "subject to the same floor").
  - With neither a trigger nor inputs, nothing qualifies, and only expiry ends the standing. That matches the acceptance's "only absence and expiry make it due".
- **"First judgement and expiry keep missing or old evidence from standing indefinitely"**: true.
  - `_judge` returns WHY_NEVER and WHY_EXPIRED before the cadence is consulted.
  - `_expired` treats a record with no parseable expiry as expired.
  - The observation writer refuses to record a result for a case without a usable MaxAge.
  - So every standing record has a finite life.
- **The first two sentences** (cost and variance of judgements; written criteria fixed before the first judgement) are unchanged blessed text and still true. The rubric warning in the acceptance is their consequence.
- **"cost limits the owner directed"**: WI-747, which introduced both the floor and the triggers, was filed at the owner's direction ("judgement is not occurring from an LLM too frequently"), so naming the trigger as owner-directed is supported.
- The cell names no script, command, file or function (ruling R2), carries no citation frame, and does not depend on the assumption evidence ladder (WI-771's).

As a standing claim the cell is complete. It explains every due path the Requirement and AcceptanceCriteria state (absence, expiry, trigger past the floor, input change past the floor) and the warning on missing criteria. The open-item guard and revision-bound reads need no justification beyond the cost argument already given.

SR-215 is named in the combined act's `--reattests`.

VERDICT: MEANING rows=1
