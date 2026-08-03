+++
id = "WI-414"
title = "adjudicate: TC-056 - ratified/routed cell(s) amended on merged trunk 7894457..5211f07 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
buildtier = "medium"
safety_class = "adjudication"
+++

## Deliverable

Adjudicated 2026-08-02. **SCOPE MOVED.** No new row is filed and no Status is
flipped: the amendment this row adjudicates is one visible edge of a re-scope
that WI-390 already owns.

THE FIRST JUDGMENT WAS WRONG, AND THE ERROR IS WORTH RECORDING. It read the
`Verifies` amendment (`SR-055;LLR-056` -> `+IF-093;IF-094`) against the state
*inside* the WI-389 branch, where the station tests already existed and the
commit merely registered the two seams — and concluded the citation had been
made accurate rather than widened. REVIEW-A rejected that: this row adjudicates
the merged range `7894457..5211f07`, not one intra-branch commit. Across the
whole range TC-056's `Evidence` was *replaced* — hoop tests out, station-cycle
tests in — and only then did `Verifies` gain two new interface contracts. An
argument that depends on intra-branch commit order is not an argument about the
range under adjudication.

WHAT THE RANGE ACTUALLY DID. The case now verifies a different render, while the
ratified definitions it hangs from still describe the old one:

- `SR-055` still requires "two circular working loops" and one shared
  `LLM_Agent` hub — still `Verified`.
- `LLR-056` still describes those loops.
- `TC-056`'s own `Method`/`Expected` still specify two intersecting hoops and
  the 6+5=11 edge count.
- The shipped render emits ONE station cycle; the only surviving mention of the
  hoops in `traj_panels.py` is the comment recording their replacement.

So the stale `Method`/`Expected` are not, as first judged, an unrelated defect
that happened to sit in the same row. They are direct evidence that the merge
moved the test case's behavioral scope without moving its ratified definition.
The judgment rests on the ENDPOINT COMPARISON, not on the order of edits
inside the branch. `Verifies` is a TRACED cell, not a ratified one, so
registering IF-093/IF-094 can be perfectly accurate seam bookkeeping in its own
right; what moved scope is that across the range the case's subject was swapped
while its ratified definitions were not. The amendment is the visible edge of
that, not the whole of it.

WHERE IT IS ROUTED, AND WHY NOTHING IS MINTED HERE. §A5.2 routes a real scope
change to a `spine` row, and that row already exists and already owns this.
WI-389's own Deliverable records it in as many words: "DEVIATION, recorded for
WI-390: the RATIFIED prose of SR-050/SR-055/LLR-051/LLR-056/TC-051/TC-056 still
describes the resume-loop/hoops picture — amending it is the program close's
spine scope, not this ordinary row's." WI-390 is queued, spine class, and its
title claims THE SPINE AMENDMENT plus "any further amendments the seven builds
surface".

The first attempt drafted a `## Dispositions` row for TC-056's Method/Expected.
That section is REMOVED, for three reasons the review made concrete: it declared
`ordinary`/`quick` for work that edits ratified cells and owes a re-attest,
which §A5.2 routes to `spine`; intake dedupes only by exact title, so it would
have minted a redundant row alongside WI-390's existing scope rather than
colliding with it; and it was too narrow anyway, naming only TC-056 when SR-055
and LLR-056 are equally false.

NO STATUS FLIP IS AVAILABLE HERE, which is a different statement from
declining one. TC-056 is already `Verified`, so there is no Modified -> Verified
flip to make; the flip arm belongs to the no-scope-moved path. On the
scope-moved path the Status movement that IS owed — Modified plus re-attest on
the ratified cells — opens with WI-390's amendment, at the owner sitting that
row exists to cost exactly once.

row takes the other arm: WI-390's spec now carries a `### Re-scope (WI-414,
2026-08-02)` subsection under its `## Context` block, naming three affected
surfaces — SR-055, LLR-056 and TC-056's Method/Expected — with this row and the
adjudicated range as origin, and retaining WI-389's broader ratified-prose route
(which also names SR-050/LLR-051/TC-051). Constructing the exact amendment stays
WI-390's.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Ratified and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- TC-056 `Verifies`: 'SR-055;LLR-056' -> 'SR-055;LLR-056;IF-093;IF-094'

Outcomes (§A5.2): flip rows back to Verified where no scope moved
(per docs/gate-policy — recommend-only under attended, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
