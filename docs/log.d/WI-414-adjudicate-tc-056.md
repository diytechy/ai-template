## 2026-08-02 — WI-414: scope moved, and WI-390 already owns it

**Summary.** The first fully machine-minted adjudication (WI-388's intake fired
it at the wi-389 merge) reached its judgment: **scope moved**. Nothing is minted
and no Status is flipped, because the amendment this row adjudicates is one
visible edge of a re-scope the queued spine row WI-390 already owns.

**The first judgment was wrong, and that is the useful part of this entry.** It
read the `Verifies` amendment (`SR-055;LLR-056` → `+IF-093;IF-094`) against the
state *inside* the WI-389 branch — where the station tests already existed and
the commit merely registered the two seams — and concluded the citation had been
made accurate rather than widened. Independent REVIEW-A rejected it: this row
adjudicates the merged range `7894457..5211f07`, not one intra-branch commit.
Across the whole range TC-056's `Evidence` was *replaced* (hoop tests out,
station-cycle tests in) and only then did `Verifies` gain two interface
contracts. **An argument that depends on intra-branch commit order is not an
argument about the range under adjudication** — that is the reasoning error, and
it is the kind a green harness cannot catch.

**What the range actually did.** The case now verifies a different render while
its ratified definitions still describe the old one: `SR-055` still requires
"two circular working loops" and one shared `LLM_Agent` hub and is still
`Verified`; `LLR-056` still describes those loops; TC-056's own
`Method`/`Expected` still specify two hoops and the 6+5=11 edge count; and the
shipped render emits one station cycle. So the stale prose is not a defect that
happens to share a row with the amendment — it is evidence the merge moved the
case's behavioral scope without moving its ratified definition.

**Routed, not filed.** §A5.2 sends a real scope change to a `spine` row, and
that row exists. WI-389's own Deliverable says so in as many words: "DEVIATION,
recorded for WI-390: the RATIFIED prose of
SR-050/SR-055/LLR-051/LLR-056/TC-051/TC-056 still describes the
resume-loop/hoops picture — amending it is the program close's spine scope, not
this ordinary row's."

**The drafted disposition was removed.** The first attempt filed a
`## Dispositions` row for TC-056's Method/Expected at `ordinary`/`quick`. Review
made three concrete objections and all three hold: editing ratified cells owes a
re-attest and §A5.2 routes that to `spine`; intake dedupes only by exact title,
so the row would have been *minted alongside* WI-390's scope rather than
colliding with it; and it named only TC-056 when SR-055 and LLR-056 are equally
false. No cancellation and no open item are warranted either — the work and the
authority are already settled.

**No Status flip.** Flipping TC-056 would assert the case is verified against
definitions that presently contradict the code. The Modified/re-attest flow
belongs to WI-390's amendment, with the owner present — the single sitting that
row exists to cost exactly once.

**A sharp edge worth recording for the next adjudication row.** A minted spec
carries an advisory `## Context` block, and `parse_spec_deliverable` clips the
body at `## Context` *before* looking for `## Deliverable`. A Deliverable
written after Context is clipped away entirely and R-A reports it empty, with a
message naming the symptom rather than the ordering. Required order:
**`## Deliverable` → `## Context`**. REVIEW-A independently confirmed this is
the format's real contract, not a workaround.
