## 2026-08-29 — the owner accepts decisions 4.1, 6.2, 6.7 and 6.8 of the OI-67 slices — recorded, nothing changes in code

Deferred open items: none — the four entries flagged for the owner's second
opinion in
[../decisions-for-review-2026-08-29-slices-4-6.md](../decisions-for-review-2026-08-29-slices-4-6.md)
are ruled by this entry; the decision surface for the program is empty.

All four statements were made in session, in two messages, and are recorded
verbatim here; each entry in the decisions file now carries a one-line
pointer to this record. The first message read the entries; the driver
corrected two readings (below) before the owner closed with *"Yes that's
fine"* over all four.

**4.1 — the harness's argv into each checker is NOT a row: ACCEPTED.** The
owner: *"I don't know the details here but I think it's fine, this is a bit
difficult on a meta-repo, but in general it's a balance between visability
and rot-risk."* Stands as decided: the exit-code rows are where the harness's
decision plugs in, and twenty `cli` rows restating the generated CLI
reference would be the rot.

**6.2 — declared-not-stated is the strict arm; an undeclared owner stays a
warn: ACCEPTED as built.** The owner's first reading — *"You mean the actual
contract prose can be omitted from the owner and it will generate a warning?
I think that's fine, but I'm making assumptions."* — was one notch off, and
the correction is on record: an owner that DECLARES the id and writes no body
is a `--strict` error; only the whole absence (no `Contracts:` marker for the
row at all) stays the reverse check's warn, visible as the gap between
registry rows and declared seams in the reference's summary line. The
migration reason holds; the option to promote the undeclared case (one branch,
one test, the unheaded fixture rows to fix) is recorded and not taken.

**6.7 — the definition gate rides the severity ladder: ACCEPTED.** The
owner asked whether this is *"really just another consequence of 6.2"*; it
is not — 6.2 is WHICH shapes the gate reports, 6.7 is WHEN its findings are
errors (`check.py` promotes `check_trajectory` to `--strict` at or above
`DevStg-Impl`, the ladder every promotion in that checker rides; below it the
gate warns in the hook and CI and errors on a direct `--strict` run). Kept
for plan decision 9 (header-first makes "declared, not stated" a sanctioned
transient for a work item in flight) and because the reference freshness
step already fails the floor on a deleted or malformed existing body.

**6.8 — a row with no in-tree endpoint is a strict finding: ACCEPTED.** The
owner: *"agreed if it's not findable the endpoint is just unknown at the
current time, but the information had to be available at some point to
satisfy that connection. Do we need a short hash to indicate what repo commit
relates to the date the interface was formed around? Even that seems risky,
perhaps a tag, but this one may never be perfect. Agreed though that it
should not result in a new document, failing that subfunction is okay so long
as it's handled properly upstream."* Two clarifications recorded with the
acceptance: the rule is about SHAPE, not findability — it fires only when the
owner AND every far-side entry are `external:` parties, a row with no code on
either end and so no home for its definition; and it is a reported finding
with a message, never a crash. The hash/tag idea is DECLINED on the
derived-not-authored rule: the body lives in the owner's header, so git
already records the commit each definition was formed at; the row's `version`
cell is the human signal of a contract change; a stamped hash would be a
second copy of git's record that rots on every edit. If "when did this
contract last move" is ever wanted, the reference generator derives it per
row — nothing is authored.

**Deviations from spec:** none — a record-only entry.

**Byte deltas on budgeted files:** none touched.

**pytest totals:** smoke tier under Git Bash **1378 passed, 6 skipped in 179.38 s** — the budget read **180.1 s vs 60 s → OVER** (90.1 s on the run before it) on a box other sessions held at 50–90 %: environmental, recorded, not waived, the quiet re-measure still owed; `check_docs --stale`: 0 broken; the open-items
view current.
