# WI-963 checkpoint sitting at e3d9617

## amendment

Two approved LLRs moved against their copies (anchor 889498874). Each gains one sentence tying it to the new settled-amendment filter, LLR-364.

What I checked:
- **The code.** `acceptance_record.settled_amendments` and its helpers (`_settled_row`, `_no_later_writer`, `_routed_unmoved`, `_snapshot_copy_rows`) implement the filter both sentences point at.
- **The tests.** `pytest tests/test_intake_settled.py`: 24 passed.
- **The lint.** `trace.py --strict` exits 0.

Both rows are MEANING, and I would bless both.

- [MEANING+BLESS] LLR-153 Detail -> before: trigger (a) mints one adjudication row from every approved or routed cell change on the merged commit -> after: the same, except that trigger (a) "excludes only records the merged range already settled under LLR-364" -> not the same: a class of amendment records no longer mints. Ready to bless:
  - The exclusion is closed: "only" what LLR-364 settles.
  - It cites the row that owns the condition rather than restating it.
  - It names no new carrier.
- [MEANING+BLESS] LLR-158 Detail -> before: the shared two-tree walk feeds the amend-without-flip warn and the intake amendment mint alike, over the approval-act tiers -> after: the same, plus the mint additionally drops records the merged range already settled under LLR-364, while the pre-commit warn reads the unfiltered walk because it runs before any act -> not the same: the two consumers of the walk now differ in what they see. Ready to bless:
  - The new obligation that is this row's own is that the warn stays unfiltered, and it is stated with its reason.
  - The mint half points at LLR-364 rather than restating its condition.
  - Note, not a finding: the mint's exclusion is now mentioned in LLR-153, here and in LLR-364. Only LLR-364 states the condition, so this is a pointer, not a second home.

VERDICT: MEANING rows=2

## first-approval

Two new rows await a first approval under SR-178: LLR-364 and its TC-403. They are judged afresh at this tip, as the brief asks. Their earlier forms, LLR-342 and TC-373, were judged at sitting 003 and bind nothing here.

**Upward, the parent holds.** SR-178 reports an artifact "whose text has moved away from the copy recording its acceptance". A row re-attested inside the merged range, whose whole approved and routed cell set equals its copy, has not moved away from its copy. Minting an amendment record for it reports a drift that does not exist. The filter is therefore SR-178's own definition, applied at the mint. LLR-153 decides when the mint runs. LLR-158 decides what a change is. LLR-364 decides which changes a range has already settled. These are three decisions with no overlap, and splitting LLR-364 further (one row per arm of its condition) would restate one settlement rule over different inputs.

- [APPROVE] LLR-364 -> the trunk mint drops an amendment record only when three things hold:
  - an act-ledger entry added within the range re-attests the row;
  - the row's whole approved and routed traced cell set at the range's end equals its snapshot copy there;
  - either no later range-added entry wrote the row's registry, a legacy entry with no copy record counting as one that may have, or the row's routed traced cells are unchanged across the range.

  An unlisted ledger supplies no acts, and a missing copy or a row absent from its copy mints. A listed carrier that cannot be read or parsed refuses the mint by name, never reading as absent. The same result serves both mint routes, and the refusal names its recovery. Hand-edited carriers, aliases and sub-second windows lie outside the bound -> the code implements each clause:
  - `_settled_row` takes the latest re-attestation, the whole-row equality, then `_no_later_writer` or `_routed_unmoved`;
  - `_no_later_writer` treats an entry without `copied` as a possible writer;
  - `_snapshot_copy_rows` makes a listed but unreadable copy a failure, never an absence.

  The rationale's claim that a later writer can absorb only routed traced drift rests on the snapshot's refusal to copy unattested approved drift (LLR-245), which is an approved row. TC-403 drives every arm on both range shapes -> ready:
  - It fails toward minting wherever settlement is unproven (unknown copy sets, moved routed cells, missing copies).
  - It names only boundary artifacts: the act ledger and the snapshot copy.
  - Its scope bound matches PROCESS.md §6.
- [RETURN] TC-403 -> drives the settled, still-mints, absent-ledger, unconsulted-filter, unreadable- and malformed-carrier, restored-cell, routed and unrouted traced, later-writer (both arms, legacy included, over squashed and unsquashed ranges) and replayed-landing cases; Expected: LLR-364's contract on both routes and IF-091's outcome -> its 19 evidence nodes exist and the suite passes. The arms are closed over LLR-364 -> not ready, for one defect: the Method's first sentence enumerates every test function by name ("Run test_a_row_reattested_in_range_..., test_a_row_amended_again_..., ..."). Those are code symbols, which row text may not name. It is also a second home for the Evidence cell's list, the copy that goes stale silently when a test is renamed. The Method's second sentence ("Assert settled records are omitted on both mint routes; ...") already states every arm in capability voice. The fix is to delete the enumeration, keeping the "(over an unsquashed and a squashed range)" and "(both ranges)" qualifiers as statements of the arms they qualify.

**Parent-first.** LLR-364's parent SR-178 is Approved. LLR-364 is approved here, and its TC-403 returns alone and re-sits.

**What the act needs.**
- The rung is released, so the later act turn re-attests LLR-153 and LLR-158 and flips LLR-364.
- TC-403 stays Drafted.
- Nothing is held for the owner.

### Dispositions (draft, for WI-963's own spec: a return answered in the lane before TC-403 re-sits)

This is a Done-when item of this row (its spine set carries its target meaning), so it is answered in this lane, not by a minted successor:

- **TC-403 Method:** remove the test-function enumeration, which the Evidence cell already holds. State the range-shape coverage (an unsquashed and a squashed range for the two later-writer arms) inside the capability-voice assertion sentence. Name no test function or other code symbol.

OUTCOME: RETURN rows=2

SITTING: JUDGED kinds=amendment;first-approval
