# WI-978 checkpoint sitting at e934cf2

## first-approval

This sitting re-judges the two rows that sitting 013 (`013-ADJUDICATE-d3cfb73.md`) returned: LLR-362 and TC-401.

**Only the two returned cells moved.** Between d3cfb73 and this tip, the only change is LLR-362's Detail and TC-401's Expected (one line each), and no code or test changed.

**The code agrees with the restated text:**
- `plan_reservation` starts each range one above the larger of the carrier's and trunk's committed mark;
- `reserve` raises every refusal before any write, and the carrier moves by compare-and-swap;
- `fold` yields each space's maximum mark and the unions of reservation and correction records.

**The checks.** TC-401's eight repository evidence nodes all exist, and its unit file passed at 013 (112 with the watermark suite), with nothing under it changed since. `trace.py --strict` exits 0.

- [APPROVE] LLR-362 -> The carrier is a shared ref, apart from any lane's branch, holding the watermark for the lane-minted spaces. A reservation moves it by compare-and-swap and appends one record per space (inclusive range and work item). Each range starts one above the larger of the carrier's and the integration branch's committed mark, so reservations in sequence or at once from any bases are disjoint. A refused argument or a lost swap writes nothing. The first reservation creates the carrier from the integration branch's committed watermark. Only a reservation writes a record, and only a fold copies one. A fold yields each space's maximum mark, the record unions, and a basis from the receiving tree's live ids. Committed records stay unchanged across every parent, every writer keeps them, and a mark rises only by allocation, ruled correction or a covering record -> it decomposes SR-174's lane half, and its acceptance clauses (disjoint ranges from any bases, the rise rule), beside LLR-363's admission. The sibling split is the one sitting 013 recorded: allocation here, admission there, the work-item half in LLR-153 and LLR-154. TC-401 and TC-158 verify every arm -> ready:
  - Each of sitting 013's six return points is answered, closed and observable.
  - It names only the watermark, a shipped artifact.
  - Note, not a finding, and partly mine: the fold sentence follows my 013 disposition's wording. It does not say that the carrier contributes only its records and the marks those records reserve (`carried`), not its own mark lines. An implementation that copied the carrier's raw marks would be refused by this same row's rise rule on the integrity floor, so the text does not admit the wrong behaviour silently. A later amendment could still state the carrier's contribution outright.
- [APPROVE] TC-401 -> carrier unit and repository cases. Every reserve refusal writes neither carrier nor working watermark. Sequential and stale-base reservations are disjoint, each range starting one above the applicable carrier or integration-branch mark. A lost swap writes nothing. The first reservation seeds the carrier from the integration branch's committed watermark. Clean and conflicted folds keep the maximum marks and every valid record exactly once -> its evidence drives each arm, including first-use seeding and the post-correction floor -> ready. It is closed over LLR-362's allocation arms, with LLR-362's record-history and rise rules held by TC-158. Note, not a finding: the Method's list omits the first-use case, which the Expected names and the evidence drives.

**Parent-first.** SR-174 is Approved, and its amendment was blessed at 013. LLR-362 and its TC-401 are approved together.

**What the act needs.** The rung is released, so the later act turn flips LLR-362 and TC-401 and takes the low-level-requirements and test-cases copies. Nothing is held for the owner.

OUTCOME: APPROVE rows=2

SITTING: JUDGED kinds=first-approval
