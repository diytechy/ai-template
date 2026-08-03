## 2026-08-02 — WI-414: TC-056's amended cell is clean; its Method is not

**Summary.** The first fully machine-minted adjudication (WI-388's intake fired
it at the wi-389 merge) reached its judgment: the amended cell moved no scope,
and adjudicating it surfaced a real defect elsewhere in the same row, which is
drafted as a follow-up rather than waved through.

**The adjudicated cell — scope did not move.** `TC-056 Verifies` went
`SR-055;LLR-056` → `SR-055;LLR-056;IF-093;IF-094`. Both added ids are the
derived-vocabulary seams WI-389 declared, and the interfaces registry says so in
their own rows: IF-093 is "seam driven by TC-056's WI-389 station sync pins",
IF-094 names `test_station_barrier_and_admission_arms_pin_to_the_dispatcher`
explicitly. Those are the tests already in this row's `Evidence`. The amendment
made the citation accurate; it did not widen what the case covers. No flip was
owed — the row is already `Verified`.

**What the adjudication found instead.** `TC-056`'s `Method` and `Expected`
still describe the render WI-389 **deleted**: two intersecting hoops, the shared
`LLM_Agent` hub, loop A / loop B, and the "6 + 5 = 11" edge count of the WI-250
picture — while `Evidence` cites the station-cycle tests WI-389 shipped.
Verified by grep, not by eye: the only surviving mention of that render in
`traj_panels.py` is a comment recording that it was replaced.

So a `Verified` case carries a method nobody can run and an Expected describing
artefacts the render no longer emits. **The reason this rot was invisible is the
uncomfortable part:** the row's Evidence tests all pass, and they test the *new*
render, so every mechanical check stayed green while the prose describing what
is being proved quietly stopped being true. Rewriting those cells is outside
this row's scope (it adjudicates the amended cell), so it is drafted in
`## Dispositions` and the intake mints it at this row's merge — drafts-not-mints,
ruling R1.

**Verification.** The draft parses with intake's own parser rather than by
inspection: `_disposition_drafts` returns 1 draft, `refusal=None`, with the
derived `context` and `kind` filled in.

**A sharp edge worth recording for the next adjudication row.** A minted spec
carries an advisory `## Context` block, and `parse_spec_deliverable` clips the
body at `## Context` *before* it looks for `## Deliverable`. So a Deliverable
written after the Context block is clipped away entirely and R-A reports it
empty, with a message ("status=done but the Deliverable is empty") that points
at the symptom rather than the ordering. The section order a closed minted row
needs is **`## Deliverable` → `## Context` → `## Dispositions`**; the draft
parser partitions on `## Dispositions` independently, so it is unaffected.
