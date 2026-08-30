## 2026-08-30 — WI-508 rework: the three REVIEW-A findings addressed

The slice-6 approval/close (commits `580df781`, `f179a0b4`) drew a
**CHANGES-REQUESTED** verdict (`docs/reviews/wi508-architectural-remap/003-REVIEW-A-f179a0b.md`,
three MAJOR findings). This session addresses all three; none needs a decision
above the loop-held rung the flips sat at, so each was fixable in place rather
than escalated.

### Finding 1 & 2 — TC-199/TC-200 over-claimed SR-163 coverage

The findings: `TC-199` and `TC-200`, flipped to `Approved` in slice 6, verify
both their LLR **and** the parent `SR-163`. As **LLR** evidence they are sound —
`LLR-203`/`LLR-204` name delivered, tested mechanisms and state their own
undischarged halves on-row, and the seven cited node ids pass. But as **SR-163**
evidence they are partial: `SR-163` asks that every shipped file JOIN to a
requirement id across the whole shipped universe, and both LLRs record on their
face that the join does not exist and the walk covers only declared destinations
(`LLR-203`) / runs the inverse direction over the source roots only (`LLR-204`).
An `Approved` TC on `SR-163` therefore reads as "the full mapping obligation is
verified" when it is not — the false-green the kit exists to prevent.

The reviewer offered two remediations: keep the partial evidence `Drafted`, or
add and approve a TC that drives the complete join and universe. The second is
explicitly **not** WI-508's job — this program's mandate is to *file* divergences
as consolidation WIs, not resolve them, and the gaps are already filed
(`WI-519`/`WI-520`/`WI-521`). So the correct rework is the first: revert the two
TCs to `Drafted`.

- `docs/test/test-cases.toml`: `TC-199`, `TC-200` `Approved` → `Drafted`.
- `docs/archive/last_approved/docs/test/test-cases.toml`: the same two, kept
  byte-symmetric with live so no drift/immutability guard fires (`Status` is
  excluded from `baseline_snapshot.is_drifted`'s comparison and a `Drafted` row
  differing from its snapshot copy is work-in-progress, not drift).

`LLR-203`/`LLR-204` stay `Approved` — the reviewer flagged only the TCs and cited
the LLRs' honest content as authoritative; a blessed design row may carry `Drafted`
test evidence while final verification is still owed. `SR-163` stays `Approved`
and keeps its TC rows in `Verifies`, so it is not orphaned (`coherence.py` counts
a `Drafted` TC toward the child-completeness rule); its verification now honestly
reads *owed*, matching the filed-as-WIs reality.

### Finding 3 — the dead OI-64/OI-65 link

The slice-6 fragment cited `../log.d/2026-08-28-owner-rulings-oi64-oi65.md`, a
file that was never created (the same phantom path is `OI-64`'s `ruling_ref`, a
pre-existing state outside this WI's scope). `doc-navigability` (`check_docs.py`,
which link-checks `docs/log.d/`) failed on the one broken link. Replaced the dead
markdown link with a plain-text pointer to the ruling's real durable home — the
`OI-64` row in `docs/requirements/open-items.toml`, executed as `IF-144` via
`WI-523`–`WI-526`. No markdown link remains to break, and the stated fact (ruled
(b), executed 2026-08-28) is unchanged and true.

### Verification

`check_docs.py` re-run: broken-link count 0. Smoke bar and the full suite run
recorded in the commit.
