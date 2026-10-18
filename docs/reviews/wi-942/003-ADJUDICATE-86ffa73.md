# WI-942 adjudication 003: amendment of LLR-278 and TC-278

I judged the two amended rows at `86ffa7397`. Since the anchor (`e45ed5a75`), the LLR and TC registries moved only in these rows. The LLR and TC rungs are released (`human_approval_through = "DevStg-Boundary"`).

**What I checked:** the six tests the arms map names all exist in `tests/test_snapshot_readers.py`. TC-278's Evidence cites the four that carry its new clauses: the acted-set placement, the lone retirement, the held-rung refusal, and the retirement beside another act. TC-278's tier is `Full`.

## amendment

- [MEANING+BLESS] LLR-278 Detail -> a snapshot is WIDENED only when the complete acted set holds no approved or re-attested row in that registry identity, a row's registry being read from where it lives at the head -> the same rule, but a row the act ledger names is placed in the registry its id's tier names, whether or not the row remains in the live registry at the head, so a retirement (a re-attestation of a row the lane deleted) authorizes its own registry's copy -> the authorization changed. A lane whose only act in a registry retires a row had its copy refused as WIDENED before, and now merges, so an implementation correct under the old text fails the new one. **Blessed.**
  - **It closes a real dead end:** the act derivation already blessed in WI-912 (LLR-338) owes a retirement while the recorded copy still holds the row, and takes it once the copy no longer does. Without this change the merge slot refuses the very copy that act must write.
  - **It is not a fail-open:** every other bound still applies to the retirement. It must lie inside the amendment scope, be ruled by an accepted amendment verdict among the branch bindings, and is refused by row on a held rung. Placement by id tier is closed and observable.
  - **The rest of the cell is verbatim**, and no new carrier is named.
- [MEANING+BLESS] TC-278 Expected and Method -> verify scope, held-rung, ruling-binding and combined-act merges and refusals -> it adds that a retired row's re-attestation authorizes its own registry's copy whether or not another act moved that registry, and that on a released rung an act whose only re-attestation retires an Approved row the lane deleted, ruled by an accepted amendment verdict inside the scope, merges with that copy as its only copy, while the same retirement on a held rung is refused by row -> new verification obligations. **Blessed.** It is closed over LLR-278's insertion: the lone case, the beside-another-act case and the held-rung refusal each have a named, existing test, and the arms map adds the scope and verdict bounds. Every earlier assertion is kept verbatim.

VERDICT: MEANING rows=2

**For the later act turn:** both rows are marked `[MEANING+BLESS]` on a released rung, so the act turn re-attests LLR-278 and TC-278. No row is held, and no row is returned.

SITTING: JUDGED kinds=amendment
