# WI-978 dispute sitting at d3a3531

DISPUTE: findings=F1

## F1: retiring an id live at the lane's base, then authoring it again, escapes the retirement refusal

**Disclosure.** I ruled dispute sitting 008, whose FIX worded the retirement refusal as applying to "an added id the landing tree or its parent records as retired". The lane built exactly that, and this finding is the shape that wording left out. I also blessed SR-174's widened text and approved LLR-363 and TC-402 at sitting 013. The gap is partly in what I asked for, and this ruling closes it rather than defending it.

**Observed at this range.** In `id_carrier.landing_lines`:
- **The order of the checks.** The judgement collects the added ids, `(s, n)` live in the tip and not in the lane's merge base (`_added_ids`). It returns `[]` when there are none (line 486), and only then runs `_retired_lines` over the added set. With SR-003 live at the base and live again at the tip, the judgement is handed no added id and passes. That holds even with `docs/log.d/retired/SR-003.md` in the landing tree, and the same id treated as added is refused naming its record (called directly, both shown).
- **No other guard.** `retire.retirement_findings` checks unreadable records, census problems, spent ids without a record and records edited after landing. Nothing reports a live row whose id holds a retirement record.

So this sequence lands, on both routes, a retirement record and a live row with a different obligation under the same identity:
1. `retire.py SR-003`, which writes the record and deletes the row;
2. a new, different SR-003 authored in the same lane.

The reviewer reports the merge slot landing it and the squash step exiting 0, which matches the code path above.

**In scope.** §6 counts "the content agents write into the repository (the gates exist to check it)". The steps are the kit's own: `retire.py` is the one writer of retirements, and the row is authored by the spine author. The confusion is a natural one for a model author told to replace a row: it retires the row, then writes "the replacement" under the same id. It needs no forged state, no hand edit of a kit-written record, and no timing window. It is less likely than sitting 008's in-range case, since the brief's reserved ranges do not point at the number. But it is the same misuse, and the retirement record that would refuse it is already on disk at the boundary that judges the landing.

**Convergence-class: a fail-open against the approved SR.**
- SR-174, as this lane widened it and sitting 013 blessed it, promises "an identity freed by a deletion is never re-issued", and its acceptance says "an identity freed by deleting its record is not re-issued to new work".
- Before this lane, that promise covered work items only. The lane extended it to every registry identity, so the lane owes its enforcement on the routes it built.
- A fail-open of an approved requirement's promise on a supported route cannot be SUCCESSOR. Its fix is cheap beside the defect, so it is not `not-worth-cost`.

**What the fix must do.**
- **The refusal.** At the one landing boundary both routes share, judge the identities live in the landing tree against the retirement records, independently of the net-added set. Refuse a live id that a retirement record names, naming the id and the record, at least where the landing adds the record or changes the row. The narrower form keeps a legacy pair, already on trunk before the lane, from blocking unrelated landings.
- **The kept refusals.** The existing added-id refusals and sitting 008's in-range case stand.
- **The regression.** Drive a base-live retire, re-author regression through the merge slot and the hand squash, failing on the current code.
- **The spine.** Amend LLR-363's retirement sentence (today "An added identity that a retirement record ... names is refused") and TC-402's matching arms through their own authority. SR-174 is unchanged, since it already states the rule.

RULING: F1 FIX the landing judgement applies the retirement refusal only to net-added ids and returns before consulting retirement records when none is added, so a lane that retires an id live at its base with retire.py and authors a different row under that id lands a retired identity re-issued on both routes, against SR-174's approved non-reissue clause; judge live identities against retirement records the landing adds or whose row it changes, on both callers, with a base-live regression and the LLR-363/TC-402 amendments
