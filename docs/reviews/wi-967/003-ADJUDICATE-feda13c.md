# WI-967 checkpoint sitting at feda13c

## first-approval

Two rows await a first approval: LLR-361 and its TC-400, both new, both under SR-178. The other rows in the chain are approved and are evidence only.

What I checked:
- **The code.** In `baseline_snapshot.py`:
  - the writer records `copied`;
  - the whole-file rule (`acts_problems`) checks `copied`'s shape and refuses an entry that omits it after one that carries it;
  - the commit-bound rule (`added_acts_problems`, through `added_acts_findings` on the integrity floor that `record_findings` feeds) judges only entries whose `seq` no parent holds;
  - that rule refuses an added entry without `copied`, or one naming a file outside the snapshot's registry files;
  - a legacy entry parses with no `copied` key, never an empty one.
- **The tests.** `pytest tests/test_baseline_snapshot.py`, over TC-400's cited cases: 41 passed.
- **The lint.** `trace.py --strict` exits 0 (drafts=2).

**Upward, the parent holds.** SR-178 asks that text moved away from "the copy recording its acceptance" be reported. Which copy records a row's acceptance depends on which registries each act copied. The row records exactly that, for WI-963's settlement to read (OI-115, ruled (a)). Sibling LLR-273 already decomposes the same SR into per-registry copy provenance, and LLR-361 adds the act-level half without overlapping it.

**But both rows go back, each for a small, specific defect.**

- [RETURN] LLR-361 -> the snapshot writer records `copied`, the non-empty sorted distinct canonical paths it wrote; a legacy entry reads as copy set unknown, never inferred; an entry a commit adds "carries `copied` naming only snapshot registry files"; a whole ledger refuses an entry omitting `copied` after one that carries it; a malformed parent and a hand-edited ledger are outside the bound -> the code implements every arm, the commit-bound rule as an integrity finding naming the entry and the recovery -> not ready: the commit-bound rule is stated as an invariant with no response to its breach. A builder following this text could ship the writer, which keeps the invariant for every entry it writes, and no validator at all, and still satisfy the row. The Done-when demands the validator: "The ledger's validators refuse an entry a commit adds ... that omits the record or names a registry outside the snapshot's own registry files". The lane's own D-003 calls this row "the copied record and its two refusals", but only one refusal is stated. The whole-file sentence says "refuses"; the commit-bound sentence says only "carries". Fix: state the refusal, e.g. "an entry a commit adds relative to each parent without `copied`, or with `copied` naming any file outside the snapshot's registry files, is refused as an integrity finding". Everything else in the row is ready.
- [RETURN] TC-400 -> drive the act shapes through the snapshot command, then the whole-file and commit-bound rules, passing and refused; Expected: each entry names its copied files, a legacy entry parses with its copy set unknown, an added entry without `copied` or with a foreign path is refused, and an omission after a carrying entry is refused -> the evidence's 16 tests exist and pass, and the Expected matches LLR-361's arms -> not ready, for two reasons:
  - **A code file is named.** The Method says "through intake.py snapshot". Every other TC in the registry that drives this route says "the snapshot command" (TC-269: "the scaffold's own snapshot command"). The naming rule bars a code file in row text, and an amendment adds none.
  - **The Method doesn't say what it drives.** "the four act shapes" and "the whole-file rules and the commit-bound rules" are undefined inside the row. A reader cannot tell what is driven without opening the spec. Name the four shapes the Done-when lists (an approval or re-attestation act, a traced re-anchor naming no row, a mixed `--approves`/ids act, a re-seed). Name the commit-bound arm's merge case too: an entry either parent holds is not added. That arm carries LLR-361's "relative to each parent" and is driven by `test_a_merge_counts_no_entry_its_other_parent_holds_as_added`.

**Parent-first.** Both rows return together, so nothing is approved over a returned parent.

### Returns answered in the lane (re-sat at 004-ADJUDICATE-822b798.md)

These are Done-when items of this row (D3 and D4), so they are answered in this lane, not by a minted successor:

- **LLR-361 Detail:** state the commit-bound refusal. An entry a commit adds without `copied`, or with `copied` naming a file outside the snapshot's registry files, is refused (an integrity finding), beside the whole-ledger order refusal.
- **TC-400 Method:**
  - replace "intake.py snapshot" with "the snapshot command";
  - name the four act shapes;
  - name the commit-bound rule's cases: an added entry without `copied`, an added entry with a foreign path, legacy entries a commit does not add never refused, and an entry the other parent holds not counted as added during a merge.

OUTCOME: RETURN rows=2

SITTING: JUDGED kinds=first-approval
