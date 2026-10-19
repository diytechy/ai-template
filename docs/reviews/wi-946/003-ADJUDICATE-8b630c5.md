# WI-946 adjudication 003: amendment of LLR-248 and TC-242

I judged the two amended rows at `8b630c521` against the anchor in `docs/archive/last_approved`. The LLR and TC rungs are released (`human_approval_through = "DevStg-Boundary"`).

**What I checked:**
- **The diff:** I loaded both registries with `tomllib`. Since the anchor, only LLR-248 and TC-242 moved. Every changed cell keeps its anchored text as an exact prefix, and the addition is appended at the cell's end:
  - LLR-248 `detail`, plus `/loop_claimed` in the `code_symbol` trace cell;
  - TC-242 `expected` and `method`.
- **TC-242's other cells are unchanged:** `Evidence` (`tests/test_loop_provenance.py; tests/test_pre_commit_hook.py`), `Verifies` (SR-209, LLR-247, LLR-248, IF-194, IF-197) and `Tier` (`Full`, which `test_pre_commit_hook` in `SLOW_MODULES` still requires).
- **Tests:** the arms map's tests all exist in `tests/test_loop_provenance.py`, a file the Evidence cites. I ran them, and 11 passed: the trailer-rung and held-status-rung refusals, both unparseable-record cases, the six readable-log pins and the one-reader pin.

## amendment

- [MEANING+BLESS] LLR-248 Detail -> the merge slot reads a lane as the loop's when its claim or a loop-writer commit in its range carries the trailer, and judges a loop lane's commits within its window; the text says nothing about a claim record that cannot be read -> the same, plus: at the merge slot, a claim record that cannot be read is refused, naming the read, and nothing is merged; it is never read as a lane the loop did not claim -> a new refusal case. An implementation of the old text that read a failed or garbled claim log as "no loop claim" satisfied it, and fails the new text. **Blessed.**
  - **Upward:** SR-209 requires every commit of a loop lane to be judged, and the claim is one of the two marks that make a lane the loop's. In a claim-only lane, reading an unreadable claim as unclaimed turns the lane into a person's lane that is not judged, so the floor fails open. The new clause makes that read fail closed, which decomposes SR-209 instead of adding scope.
  - **Sideways:** the clause binds the claim read, which LLR-248 already owns as part of lane ownership. It applies wherever the slot reads the claim, including the held-status rung, which reaches the claim through the same window read. It does not restate the held-status rung's own decision.
  - **It is closed and observable:** the input is the claim record, the outcome is a refusal naming the read with nothing merged, and the single forbidden reading is named.
  - **No name is added:** the detail names no new carrier. `loop_claimed` enters only the `code_symbol` trace cell, which is a trace home, not row text.
- [MEANING+BLESS] TC-242 Expected and Method -> verify SR-209's acceptance and LLR-248's window, with no case for an unreadable claim record -> Expected adds the LLR sentence verbatim, and Method adds that at the merge ladder a loop lane whose claim record cannot be read is refused, naming the read, with nothing merged -> a new verification obligation, so the meaning changed. **Blessed.**
  - **It verifies exactly the obligation LLR-248 adds.** Each part has a named, passing test in the cited file:
    - the trailer rung's refusal, which names the failed read and leaves HEAD unmoved through `integrate_one`;
    - the held-status rung's refusal;
    - a record with no separator or no commit id, read as unreadable and never as unclaimed, at both rungs.
  - **It claims no more than its evidence and verified rows carry.** No other cell changed, and the tier stays correct.

VERDICT: MEANING rows=2

**For the later act turn:** both rows are marked `[MEANING+BLESS]` on a released rung, so the act turn re-attests LLR-248 and TC-242. No row is held, and no row is returned.

**One advisory, not blocking:** the Method says "a loop lane whose claim record cannot be read". When the claim cannot be read, the slot cannot yet know the lane is the loop's. The fixture and the Expected sentence ("never read as a lane the loop did not claim") make the intent clear: any lane whose claim read fails. A later edit could say "a lane" outright.

SITTING: JUDGED kinds=amendment
