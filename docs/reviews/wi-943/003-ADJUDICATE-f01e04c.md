# WI-943 adjudication 003: amendment of LLR-278, TC-278, LLR-338 and LLR-310

I judged the four amended rows at `f01e04ce4`. Since the anchor (`5790639d4`), the LLR and TC registries moved only in these rows and in TC-368's traced evidence cell. The LLR and TC rungs are released (`human_approval_through = "DevStg-Boundary"`).

**What I checked:**
- **The shared reader exists.** `kitlib/sitting.judged_rows` (lines 612-632) admits an APPROVE row, a CLARITY row, and an amendment MEANING row only when `blessed_rows` marks it (a row tagged two ways reads unblessed).
- **Both consumers read it.** The merge's backing checks (`sitting.py` lines 642 and 721) and the act assembler (`adjudicate_act.py:211`) call it, so the "one reader" sentences in LLR-310 and LLR-338 describe the code.
- **Tests.** Every test TC-278 cites exists, including the eight new plain-MEANING and MEANING+BLESS cases: released refusal naming the row and the mark, released blessed merge, a named verdict ruling plain MEANING refused and one blessing merging, a combined act refused whole and a blessed one merging, plus the held-rung pair. Every test TC-368 cites exists.

## amendment

- [MEANING+BLESS] LLR-278 Detail -> every acted re-attestation needs a MEANING **or** CLARITY ruling in an accepted amendment part, and a named verdict must judge each row it re-attests -> it needs a CLARITY ruling, or a MEANING ruling **carrying the bless mark**, and a named verdict must authorize each re-attested row the same way -> the merge's authority tightened. On a released rung, a re-attestation backed only by a plain MEANING ruling merged before and is refused now. **Blessed.**
  - **It makes the merge enforce the protocol the act turn already follows:** a plain `[MEANING]` row is one the judge would not bless, so it must not be re-anchored.
  - **It closes the hole** where a re-attestation of such a row could still merge.
  - **The tightening fails closed.**
  - **Acts already on trunk are not re-read,** so no landed history is refused retroactively.
  - **The held-rung CLARITY rule and every other clause are verbatim.**
- [MEANING+BLESS] TC-278 Expected and Method -> verify re-attested rows MEANING- or CLARITY-ruled by accepted bindings, and a named verdict judging each one -> verify CLARITY or blessed-MEANING authorization, with a named verdict authorizing the same way; on a released rung, a plain-MEANING or two-way-tagged re-attestation is refused naming the row, through the backing check and a named verdict alike, a combined act carrying one is refused whole, and the same act under MEANING+BLESS merges -> new verification obligations. **Blessed.** It is closed over LLR-278's tightening, with a named, existing test for each case.
- [MEANING+BLESS] LLR-338 Detail -> each row's act is read from the one held-rung act policy, and the bless mark is the added condition for a released-rung MEANING row -> which rows a verdict authorizes, a MEANING row only with its bless mark, is read from the one reader the merge's backing check also reads, and each authorized row's act from the held-rung policy -> a new design constraint: the act assembler must share its authorization reader with the merge. An implementation that derived authorization separately would satisfy the old text and fail the new one. **Blessed.**
  - It removes the chance that the act turn derives an act the merge would refuse, or the reverse.
  - The code calls `judged_rows`, as the row says.
  - The act outcomes themselves are unchanged.
- [MEANING+BLESS] LLR-310 Detail -> every re-attested row needs a MEANING or CLARITY ruling in an accepted amendment part, and a named verdict must judge each row -> it needs a CLARITY ruling, or a MEANING ruling carrying the bless mark, and a named verdict must authorize the same way; one reader of the rows an accepted verdict authorizes serves both the merge and the act assembler -> the same tightening at the reader's home, plus the single-reader constraint. **Blessed.** It is the reader row the other three decompose from. It matches `judged_rows`, and TC-368's tests verify it.

VERDICT: MEANING rows=4

**For the later act turn:** all four rows are marked `[MEANING+BLESS]` on a released rung, so the act turn re-attests LLR-278, TC-278, LLR-338 and LLR-310. No row is held, and no row is returned.

**On the coordinator's note:** the two act-side tests TC-368 gained (`test_judged_rows_admits_an_amendment_MEANING_row_only_with_its_bless_mark` and `test_the_bless_mark_has_one_reader_shared_by_the_merge_and_the_act`) belong under TC-368, not TC-278. They exercise the shared reader (LLR-310) and its sharing with the act assembler (LLR-338), both of which TC-368 verifies. TC-278 verifies the merge's refusals (LLR-278), and its own new tests cover those. No move is needed.

SITTING: JUDGED kinds=amendment
