# WI-930 adjudication 003: amendment of LLR-313 and TC-333

I judged the two amended rows at `6cbacac8d`. Since the anchor (`810289417`), LLR-313's `detail` and TC-333's Expected and Method lines are the only movement in the LLR and TC registries. The LLR and TC rungs are released (`human_approval_through = "DevStg-Boundary"`).

**What I checked:**
- **The refusal is gone from the code.** `review_brief.py` no longer reads `ROLLUP_DIR` or compares the round directory with it; only descriptive comments about the rollup remain.
- **The kept refusal is still there.** A branch the round reader cannot read back as one review scope is still refused.
- **Tests:** every test TC-333 names exists and is in its Evidence. Its test list is unchanged; only the rollup-named branch loops were removed from two tests, and their `feature/wi-900` refusals stay.

## amendment

- [MEANING] LLR-313 Detail -> `file_review` writes an accepted verdict as the round record only when the round reader reads its lane path back as that lane's scope AND the record's directory is not the rollup generator's own -> only when the round reader reads its lane path back as that lane's scope -> a refusal case removed. A branch named for the rollup's directory (in any letter case) was refused before and is now filed, so an implementation correct under the new text (no rollup comparison) fails the old one. **Blessed.**
  - **The owner ruled the guard contrived** (D-011, under PROCESS.md §6's plausibility extension): no kit route makes a branch named `rollup`, since the claim mints `wi-NNN` and the coordinator files from the lane's worktree.
  - **The parent is satisfied by what remains.** SR-235's promise, a recorded verdict or a refusal, is fully met by the remaining scope-read construction, and SR-235 names no directory.
  - **The plausible branch-name refusal stays.**
  - **The cell adds no name and keeps every other clause verbatim.**
- [MEANING] TC-333 Expected and Method -> verify that a lane whose scope is the rollup generator's own directory is refused without a requested file or review record, and attempt filing on such a branch -> both clauses removed; the unreadable-scope refusal and every other assertion kept -> a verification obligation removed. **Blessed.** It matches LLR-313's change exactly, drops no other clause, and its named tests all still exist. The removed assertion was a test of the residue the owner ruled out, not of supported behaviour.

VERDICT: MEANING rows=2

**Aftermath:** this session re-attests both rows on the released rung, in their own act commit:

`python project-trajectory/scripts/intake.py snapshot --reattests LLR-313,TC-333`

SITTING: JUDGED kinds=amendment
