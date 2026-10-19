## 2026-10-18 — WI-925: the declared trunk, and a spec move's relink inside another claim's Done-when

### Relink reproduction (D8)

The fixture ran first, on the lane's code before any fix (trunk base
2268a9a8c), in `tests/test_done_when_blessing.py`: trunk `main` holds two
claimed rows, X (`active/wi-x/`) and Y (`active/wi-y/`), and Y's Done-when
links X's spec. X's lane closes X through `spec_move.move_spec`, which
rewrites the link inside Y's claim copy.

- **Reproduced.** Landing X's lane by the squash recipe stages Y's copy as
  modified on trunk, and the trunk arm holds the landing naming Y: the
  rewritten link target reads as a changed item plus an added one
  (`test_a_squash_landing_that_relinks_another_claims_done_when_link_is_held`).
  So deliverable 3 stands.
- The same landing with a real rewording of Y's item beside the relink is
  held naming Y
  (`test_a_squash_landing_with_a_real_edit_beside_the_relink_is_held`).

The reach beyond the same delta (call C2), on one history of Y's lane, cut
before X lands so its tip still carries Y's original link
(`test_a_relink_reaching_an_existing_lanes_claim_copy_across_the_landing`):

- (ii) before Y refreshes: the merge slot (trunk's copy after X's landing,
  relinked, against Y's lane tip, original) **holds**; the build hold at the
  lane's fork point (both original) does not.
- (i) after Y merges trunk in: the build hold at the merge base (X's
  landing; both relinked) does not hold; at Y's claim commit (original
  against relinked) it **holds**; the merge slot (both relinked) does not.
- (iii) when Y closes by the ritual and lands: the mint compares trunk's copy
  before Y's landing (relinked) with the closed copy and **mints** the
  goalposts row; a direct `blessing_owed` read of Y's claim-commit copy
  against the closed copy owes a blessing too.

By C2 (a) each of these holds is stated residue, released by an owner
ruling; the fix is not widened for them. The lane was cut before the landing,
so the probes cover the pair the spec names.

One reading beyond the ruled scope: at (iii) the closed copy's link is not
the relinked one. The ritual's other half, which re-relativises the moved
file's own outbound links, rewrote it again for the closed folder. So a row
whose own Done-when carries a relative link reads as changed at its own close
whether or not any other spec moved.

### The relink exemption (stage 2)

The staged reader now treats a claim copy's lone modification whose staged
bytes are exactly the inbound relink of a spec move the same delta carries
as no change, through one shared reading (`spec_move.exact_relink`), which
the claim recognizer and the plan gate call too. The first reproduction test
flipped to
`test_a_squash_landing_that_relinks_another_claims_done_when_link_is_not_held`;
the real-edit test stays held, and the C2 probes keep their recorded
outcomes unchanged.
