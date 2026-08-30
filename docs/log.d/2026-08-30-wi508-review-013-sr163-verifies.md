## 2026-08-30 — WI-508 review round 013: the SR-163 `verifies` finding TAKEN — the honest orphan beats a Drafted row that trace reads as coverage

Deferred open items: none — an orphan the ladder already counts as assigned
debt, not a ruling.

Round 013 (`docs/reviews/wi508-architectural-remap/010-REVIEW-A-c225c34.md`,
gpt-5.6-terra, on the refreshed tip `c225c34d`) returned one MAJOR, the same
finding rounds 003 and 011 raised: `TC-199`/`TC-200` formally verify `SR-163`
while both TC methods and both LLRs leave the file-to-requirement join and the
shipped-file universe unimplemented, and `trace.py` therefore reports `SR-163`
as covered.

**Round 011's disposition of this point is REVERSED here, and the reason is
the reviewer's, not a new reading.** Round 011's record refuted the fix on its
cost — dropping the targets raises `orphans` 2 → 3 with `SR SR-163 has no
test (TC)` — which is a cost, not a refutation of the claim. The claim is
that a `Drafted` TC citing an SR still makes the coverage matrix read the SR
as tested; three independent rounds said so and the instrument agrees
(`trace.py` counts the row's `verifies` regardless of `Status`). An orphan
finding on `SR-163` is the TRUE state of its verification — "owed and
unscheduled", exactly what the archived Deliverable already says in prose —
where a Drafted TC on the SR was a claim waiting to become false the day
someone approved it.

Applied:

- `docs/test/test-cases.toml`: `TC-199` `verifies = ["LLR-203"]`, `TC-200`
  `verifies = ["LLR-204"]` (was `["SR-163", "LLR-203"]` / `["SR-163",
  "LLR-204"]`). Both rows stay `Drafted`; the LLR links stand.
- `docs/archive/work/complete/WI-508-architectural-remap-program.md`: the
  Deliverable sentence that described the direct `SR-163` links as
  "non-evidence while Drafted" now records their removal and the resulting
  orphan.
- `trace.py --strict-integrity`: `orphans=3 integrity=0` — the new orphan is
  `SR-163` (no TC), beside `SR-181`'s two standing findings.
  <!-- fig: cmd="python project-trajectory/scripts/trace.py --strict-integrity" rev=this-commit -->

`SR-163`'s verification is now visibly the ladder's debt: the acceptance row
needs a TC that drives the complete join over the whole shipped universe, and
no queued row owns it (the 2026-08-25 alignment filed consolidation rows, not
that TC). That row is the owner's to file or delegate — carried in the
supervisor's decisions file.

**Deviations from spec:** none — a review-round rework inside the close.

**Byte deltas on budgeted files:** none touched.

**pytest totals:** smoke tier **1378 passed, 6 skipped in 24.89 s**; budget **24.3 s vs 60 s -> within**; `check_trajectory --strict`: clean; `trace.py --strict-integrity`: `orphans=3 integrity=0`.
