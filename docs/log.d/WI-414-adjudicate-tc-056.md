## 2026-08-02 — WI-414: scope moved; WI-390 re-scoped to carry the amendment

**Summary.** The first fully machine-minted adjudication (WI-388's intake fired
it at the wi-389 merge) judged **scope moved**, and produced its §A5.2 output by
**re-scoping the queued spine row WI-390** rather than filing a second one.
Nothing was minted and no Status was flipped.

**The judgment rests on the endpoint comparison.** Across the adjudicated range
`7894457..5211f07`, TC-056's `Evidence` was replaced (hoop tests out,
station-cycle tests in) and `Verifies` gained `IF-093;IF-094`, while the ratified
definitions the case hangs from did not move: `SR-055` still requires "two
circular working loops" and one shared `LLM_Agent` hub and is still `Verified`,
`LLR-056` still describes those loops, and TC-056's own `Method`/`Expected` still
specify two hoops and the 6+5=11 edge count — against a shipped render that emits
one station cycle. `Verifies` is a **traced** cell, not a ratified one, so
registering the two seams can be accurate bookkeeping in its own right; what
moved scope is that the case's subject was swapped while its ratified definitions
were not. The order of edits inside the WI-389 branch does not carry the
judgment, and an earlier draft of this entry that leaned on it was wrong.

**The §A5.2 output, and where it landed.** The scope-moved path authorizes filing
a real spine WI and/or re-scoping the queued rows whose premises moved. Filing a
second spine row would duplicate WI-390, so this row took the other arm:
**WI-390's spec now carries a `### Re-scope (WI-414, 2026-08-02)` subsection
under its `## Context` block**, naming SR-055, LLR-056 and TC-056's
Method/Expected as the surfaces the merge falsified, citing WI-414 and the range
as origin, retaining WI-389's broader "ratified prose" route (which also names
SR-050/LLR-051/TC-051), and leaving the exact amendment and its Modified/re-attest
flow to WI-390's owner sitting. That content edit also re-affirmed WI-390 against
its amended SpecRef, which cleared the standing `check_trajectory` SpecRef-clock
warning.

**Placement, learned from the checker.** The spec body format admits only
`## Deliverable` / `## Handback` / `## Context`, and a queued row's Deliverable
must stay empty under R-A — so a bare `## Re-scope` heading is a malformation,
which `check_trajectory` said immediately. The note lives as a sub-heading under
`## Context`. The structured registry loaders clip that block, so it does not
reach the row's registry cells — but it is NOT unread by machine:
`check_trajectory` consumes the full spec including Context citations for its
knowledge-pack advisory, with a regression test pinning that a citation inside
`## Context` is seen. Its primary reader is still the human one the session
protocol requires — whoever opens the scoped WI spec before building it, which
for WI-390 is its owner sitting.

**No Status flip is available here**, which differs from declining one. TC-056 is
already `Verified`, so no Modified → Verified flip exists; that arm belongs to the
no-scope-moved path. The Status movement actually owed — Modified plus re-attest
on the ratified cells — opens with WI-390's amendment.

**A sharp edge for the next adjudication row.** `parse_spec_deliverable` clips
the body at `## Context` *before* looking for `## Deliverable`, so a Deliverable
written after the minted Context block is clipped away entirely and R-A reports
it empty, naming the symptom rather than the ordering. Required order:
`## Deliverable` → `## Context`.

**Review.** Three REVIEW-A rounds (cross-family, OpenAI `gpt-5.6-sol`). Round 1
rejected the original "scope did not move" judgment and its drafted
ordinary/quick disposition; round 2 accepted scope-moved but rejected
"route and produce nothing" as an unauthorized §A5.2 outcome; round 3 accepted
the re-scope as authorized, sufficient and correctly placed. Artifact:
[WI-414-REVIEW-A](../reviews/WI-414-REVIEW-A.md).
