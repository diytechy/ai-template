+++
id = "WI-414"
title = "adjudicate: TC-056 - ratified/routed cell(s) amended on merged trunk 7894457..5211f07 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
buildtier = "medium"
safety_class = "adjudication"
+++

## Deliverable

Adjudicated 2026-08-02. The judgment, and the follow-up it surfaced:

**The adjudicated cell: SCOPE DID NOT MOVE.** `TC-056 Verifies` went
`SR-055;LLR-056` -> `SR-055;LLR-056;IF-093;IF-094`. Both added ids are the
derived-vocabulary seams WI-389 declared, and the interfaces registry says so in
their own rows rather than leaving it to be inferred: IF-093 is "seam driven by
TC-056's WI-389 station sync pins", IF-094 is "seam driven by TC-056's WI-389
station sync pin (`test_station_barrier_and_admission_arms_pin_to_the_dispatcher`:
the rendered exclusive-kind list must equal the schedule-derived one)". Those are
the very tests already sitting in this row's own `Evidence` cell. The amendment
therefore recorded what the case already verified — it made the citation
accurate, it did not widen what the case covers. No flip is owed either: the row
is already `Verified`.

**But the adjudication surfaced a real defect in the same row, and it gets its
own follow-up rather than a silent pass.** `TC-056`'s `Method` and `Expected`
still describe the render WI-389 DELETED — "two intersecting hoops", the shared
`LLM_Agent` hub, "loop A"/"loop B", and a stage-and-arrow count ("6 for the
5-stage intake loop + 5 for the 4-stage decision loop = 11") that belongs to the
WI-250 picture. Meanwhile its `Evidence` cites the station-cycle tests WI-389
shipped. Verified by grep rather than by eye: the only surviving mention of that
render in `traj_panels.py` is line 454's comment recording that it was
*replaced*.

That leaves a `Verified` test case whose stated method cannot be run against the
code, and whose Expected describes artefacts the render no longer emits — a
proof text that has quietly stopped being true. It is out of this row's scope to
rewrite (this row adjudicates the amended cell), so it is drafted below.

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

## Dispositions

```toml
title = "TC-056's Method and Expected still describe the DELETED WI-250 two-hoop render (LLM_Agent hub, loop A/loop B, the 6+5=11 edge count) while its Evidence cites the WI-389 station-cycle tests - rewrite both cells onto the station cycle actually rendered (_station_svg/_station_panel: the directed ring, the three terminal outcomes, the serial merge-slot waist, the spine-barrier gate glyph, the intake mint arm), so the case's stated method is one somebody can run. Surfaced by WI-414's adjudication of the Verifies amendment; the Verifies cell itself was judged scope-not-moved. Verify by regenerating and re-reading, not by eye - the render's own tests are the Evidence and they already pass, which is exactly why this rot was invisible."
workstream = "process"
buildtier = "quick"
safety_class = "ordinary"
specref = "docs/test/test-cases.csv"
```
