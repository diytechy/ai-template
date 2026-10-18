# WI-929 adjudication 003: amendment of LLR-310 and TC-327

I judged the two amended rows at `1a07afc24`. Since the anchor (`5604f0fd9`), the LLR and TC registries moved only in these rows. The LLR and TC rungs are released (`human_approval_through = "DevStg-Boundary"`).

**The scope:** the work item's Context records the owner's ruling (D-011, on the contrived-guards audit) that WI-852's repeated-field refusal is discarded, because no supported route writes a machine line naming a field twice.

**What I checked, in process against the lane's code:**
- **The review line still refuses a repeat.** `review_line("VERDICT: APPROVE findings=7 findings=0")` returns no verdict and the reason "is not exactly `VERDICT: <APPROVE|CHANGES-REQUESTED> findings=<digits>`", while the canonical line reads `('APPROVE', 0)`. The exact-form match, not the removed check, carries that refusal, and `tests/test_review_brief.py` pins it with the repeated-count case.
- **Every test TC-327 cites still exists.**

## amendment

- [MEANING+BLESS] LLR-310 Detail and Rationale -> the one machine-line parser invalidates a bare, split, bad-label, field-missing or **declared-field-repeated** line; the review line is accepted only in its exact canonical form "with findings named once" -> the parser invalidates a bare, split, bad-label or field-missing line; the review line is accepted only in its exact canonical form; the Rationale adds that an adjudication machine line repeating a declared field reads its last copy, a form only a model writing the field twice produces and outside the bound of lines the kit's routes write -> on adjudication lines the obligation changed: `VERDICT: MEANING rows=2 rows=0` was refused and now reads `rows=0`. On the review line nothing moved, because "findings named once" was already implied by the exact form, which still refuses a repeat. **Blessed.**
  - **The owner ruled the guard contrived**, and the Rationale states the residue honestly.
  - **The residue carries no fail-open path that matters:** a repeated `digest=` still has to match the computed digest to cover, and the counts are checked against the lines they count.
  - **The rest of the cell is verbatim:** every other parser rule, the binding, the acceptance rules and the merge authorization, and the bless reader.
  - **No carrier is added.**
- [MEANING+BLESS] TC-327 Expected and Method -> verify that the combined verdict refuses "a line that repeats a declared field" -> that clause is removed; every other brief, binding and section assertion is kept, with the same named tests -> a verification obligation removed. **Blessed.** It matches LLR-310's removal exactly, keeps every other assertion, and cites only tests that exist. The review line's repeated-count refusal is still verified by TC-333's and TC-083's own tests, as the arms map shows.

VERDICT: MEANING rows=2

**For the later act turn:** both rows are marked `[MEANING+BLESS]` on a released rung, so the act turn re-attests LLR-310 and TC-327. No row is held, and no row is returned.

SITTING: JUDGED kinds=amendment
