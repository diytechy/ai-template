# WI-978 dispute sitting at 7f27643

DISPUTE: findings=F1

## F1: a reserved number the lane itself retired can be issued again inside its own reservation

**Observed at this range.**
- **What the judgement takes.** The landing judgement (`id_carrier.landing_lines`, called by `landing_refusal` for the merge slot and the hand-squash step alike) has the signature `(added, carrier_records, wi_ids, landing_records, parent_records, carrier_present, claim_problem)`. It is given no retirement record and reads none.
- **What it authorizes.** An added id passes when any carrier record naming the work item covers its number (`_outside_lines`). Nothing else in `id_carrier.py` mentions retirement.
- **Called directly**, with the lane's own reservation `SR 6-6 (WI-401)`:
  - an added `SR-006` returns `[]`, a pass, whether or not `docs/log.d/retired/SR-006.md` exists;
  - an added `SR-003` is refused, but only because it lies outside the range.
- **What the test covers.** That out-of-range case is the only retired-number case the landing tests drive (`tests/test_id_landing.py` `REFUSED["retired-number"]`, SR-003 against `OWN`), as the finding says.
- **No other guard catches it.** The retirement machinery checks unreadable records, spent ids without a record, and records edited or removed after landing (`retire.retirement_findings`). It does not check a live id that also has a retirement record. `retire._judge` refuses retiring an id twice, not authoring it again.

So the supported sequence lands both a retirement record and a live row for the same identity:
1. reserve SR=1 (SR-006);
2. author SR-006;
3. retire it with `retire.py`, which writes `docs/log.d/retired/SR-006.md`;
4. author a different SR-006.

**In scope, and plausible.** §6 asks whether a supported workflow or the kit's own routes reach it, and here every step is one. The reserve verb, `retire.py` (the one writer of retirements) and the spine author all take part. The author is the most likely to make the step that matters: this lane's own spine-author prompt tells it to draft new ids "from the reserved ranges its brief names". This lane's own PROCESS.md §4 text tells it to lean toward minting a new id when a row is replaced. A replacement drafted from the brief's range will naturally reuse the freed number when the range holds just one. No hand edit, forged state or timing window is needed.

**It is convergence-class, so it cannot be SUCCESSOR.**
- **Against the approved SR.** It breaks SR-174's approved text: "an identity freed by a deletion is never re-issued"; acceptance: "an identity freed by deleting its record is not re-issued to new work".
- **Against the spec's own table.** It breaks the spec's landing table, whose refused row reads "an added id outside every record naming that work item (no record, another work item's record, or a retired number re-used)".
- **Against the Done-when.** It is a gap in the Done-when, "Every row of the landing table is driven, on both callers". The retired-number arm is driven only where the range check refuses it anyway.

Before this lane the mark alone kept a freed number from being reissued, since authors drew numbers above it. This lane makes range membership the authority, so the landing check is where non-reissue now has to be enforced.

**What the fix must do.** The finding's remedy is the right size:
- the landing judgement, on both callers, refuses an added id that the landing tree or its parent records as retired, inside a reservation as well as outside it, naming the id and the record;
- the existing refusal matrix is kept;
- a real reserve, author, retire, re-author regression is driven through the merge slot and the hand squash, and fails on the current code;
- LLR-363, TC-402 and the IF-101 contract are amended through their own authority to state it, with SR-174 left as approved, since it already states the rule.

RULING: F1 FIX the landing judgement authorizes any added id inside the work item's reservation and reads no retirement record, so a lane that reserves SR-006, authors it, retires it with retire.py and authors a different SR-006 lands a retired identity re-issued, against SR-174's approved non-reissue clause and the spec's landing-table row "a retired number re-used"; refuse an added id the landing or its parent records as retired on both callers, with a real reserve/retire/re-author regression and the LLR-363/TC-402/IF-101 amendments
