# WI-963 dispute adjudication: F1 (the gate over aa86c9b)

Range: `1ca1caf7567263c7b74117cb5424197e8ccf73bb..aa86c9bb9790d1736ae61007f49dbf7ab4374aa5`.
Ruled against PROCESS.md §6 "Review threat model", the WI-963 Done-when, and the code at this range.

## F1: a later act's whole-registry copy settles a routed traced change nobody judged

**Reproduced.** I followed the finding's sequence in a scratch test outside the repo. It used `tests/test_intake_settled.py`'s own helpers and the real producer, `baseline_snapshot.copy_live`, committed into a real git repo:
1. Seed SR-001 and SR-002 as Approved.
2. Amend SR-001's Requirement.
3. Act A re-attests SR-001.
4. Re-point SR-001's `SN-Refs` from SN-001 to SN-002, and amend SR-002's Requirement.
5. Act B re-attests SR-002 alone.

Over `before..after`, `staged_spine_amendments` returns two records: SR-001 (approved Requirement, routed traced SN-Refs) and SR-002 (Requirement). Act B's copy of the SR registry now carries SR-001's `sn_refs = ["SN-002"]`. `copy_live` refreshed the whole registry, and a traced cell is not drift, so nothing refused. `intake_after_merge` returns no refusal and mints nothing. Before the filter, the same range mints a row for each of them.

**Why the filter lets it through.** `settled_amendments` (acceptance_record.py, the `_row_settled` call) asks two things: did a range-added ledger entry re-attest the row, and do the row's approved and routed traced cells at `after` equal its copy at `after`. Act A answers the first. Act B's unrelated refresh answers the second, by copying the very re-point the second test exists to catch. The equality proves the copy is current, not that any act judged the row's routed cells. The code meets LLR-342's text as written; the text's condition is what falls short.

**This is a convergence-class gap on a supported route, not a contrived one.** The Done-when says "a row re-attested in the range and then amended again after its act still yields its amendment row". A routed traced cell is an amendment in this mint's own terms: trigger (a) is the approved/routed-cell diff, and the lane's own guard, `test_a_routed_traced_cell_moved_after_the_act_still_mints`, pins exactly that a re-point after the act must still mint.

Nothing in the reproduction is a hand act. A lane holding more than one checkpoint is the in-lane route (WI-956 held two sittings). The reconcile between sittings edits rows. Any later act on that registry copies it whole, a closing first-approval flip of another row included. The kit's own route also guarantees that act B leaves SR-001 out: the amendment brief selects rows by approved-cell drift against the copy (`adjudicate_brief`'s amendment assembler excludes traced cells by design). So at the second checkpoint SR-001's approved text equals its copy, it is not shown, and the act re-attests only what was shown.

Before the filter, the trunk mint at least filed a visible row for SR-001's re-point. After it, the change lands with no record at all, which is a silent suppression of a routed change: fail-open in this mint's terms. None of the threat model's exclusions applies: no hand-edited carrier, no alias, no timing window.

**The ruling is FIX, not ESCALATE or SUCCESSOR.** A Done-when gap is never SUCCESSOR. Nor is it a high-risk call for the owner: the defect is local to the filter's own condition, and the fix tightens it, so the failure direction moves back toward minting.

The smallest fix: compare the row at `after` with its snapshot copy as written by the act that re-attested it, meaning the commit that added the latest range ledger entry naming the row, not with the copy at `after`. Then a later act's refresh of the registry cannot vouch for cells it never judged. Treating a later copy write by a non-re-attesting act as unsettled is an equivalent route.

LLR-342's "at that revision" and TC-373 must be amended to match, with a regression of two acts on one registry and a routed traced edit between them, as the finding asks. The amended rows are then re-sat.

RULING: F1 FIX the filter judges settlement by the row's copy at `after`, so a later act re-attesting another row in the same registry silently absorbs a routed traced change made after the row's own act; reproduced through the real producer (SR-001's SN-Refs re-point and SR-002's amendment both mint nothing), it breaks the Done-when "re-attested ... then amended again after its act still yields its amendment row" on a supported multi-checkpoint route. Compare against the copy written by the re-attesting act's own commit, amend LLR-342 and TC-373, and add the two-acts regression.
