# WI-967 checkpoint sitting at 822b798

## first-approval

This sitting re-judges sitting 003 (`003-ADJUDICATE-feda13c.md`), which returned LLR-361 and TC-400.

**Only the two returned cells moved.** Between feda13c and this tip, the only registry change is LLR-361's Detail and TC-400's Method (one line each), and no code or test changed. A word-diff shows each change is the one sitting 003 asked for:
- **LLR-361:** one sentence was added, stating the commit-bound refusal.
- **TC-400:** "intake.py snapshot" is replaced by "the snapshot command", and the four act shapes and the commit-bound cases are named.

`trace.py --strict` exits 0. TC-400's cited tests were run at 003 (41 passed), and nothing under them has changed since.

- [APPROVE] LLR-361 -> the snapshot writer records `copied`, the non-empty sorted distinct canonical paths of the registry files the act wrote. A legacy entry reads as copy set unknown, never empty and never inferred. An entry a commit adds relative to each parent, without `copied` or with `copied` naming a file outside the snapshot's registry files, is refused. A whole ledger refuses an entry that omits `copied` after one that carries it. A malformed parent or a hand-edited ledger is outside the bound, and a copied file is no evidence its rows were judged -> SR-178 needs to know which copy records each row's acceptance, and this row records the act-level half of that, beside LLR-273's per-registry provenance, without overlap. The code implements every arm: the writer, `acts_problems`' shape and order rules, and `added_acts_problems` on the integrity floor. TC-400 verifies each arm -> ready:
  - Both refusals are now stated as refusals, so a builder can no longer satisfy the row with the writer alone.
  - `copied` is a field of the act ledger, a shipped boundary artifact the LLR tier may name.
  - The row names no code carrier.
  - Its scope bound matches the spec's, and PROCESS.md §6.
- [APPROVE] TC-400 -> drive the four act shapes through the snapshot command: an approval or re-attestation act, a traced re-anchor naming no row, a mixed approval/re-attestation act across two registries, and a re-seed. Exercise the whole-file and commit-bound rules, passing and refused: an added entry without `copied`, an added entry with a foreign path, legacy entries a commit does not add never refused, and an entry the other parent holds not counted as added in a merge. Expected: each entry names its copied files, a legacy entry parses with its copy set unknown, both commit-bound refusals hold, and the order refusal holds -> the evidence's 16 tests exist. The whole-file order rule is driven as a case of `test_a_malformed_act_ledger_is_refused_whole` ("an entry omits copied after one that carries it"), and the merge case by `test_a_merge_counts_no_entry_its_other_parent_holds_as_added` -> ready. The Method is closed over LLR-361's arms, "relative to each parent" included, and names no code file. It reads the same as TC-269's "the snapshot command".

**Parent-first.** SR-178 is Approved, and LLR-361 and its TC-400 are approved together.

**What the act needs.** The rung is released, so the later act turn flips LLR-361 and TC-400 from `Drafted` to `Approved` and takes the low-level-requirements and test-cases copies. Nothing is held for the owner.

OUTCOME: APPROVE rows=2

SITTING: JUDGED kinds=first-approval
