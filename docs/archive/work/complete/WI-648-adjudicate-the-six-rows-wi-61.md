+++
id = "WI-648"
title = "adjudicate: LLR-140, LLR-143, LLR-151, TC-132, TC-144, TC-145 - approved cells amended by WI-612's bookkeeping helper; judge whether scope moved"
workstream = "process"
specref = ""
sr_refs = ["SR-156"]
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
priority = 2
+++

## Deliverable

Ruled by an independent adjudicator session from the kit's amendment brief,
against the record written at cbb6649f:

    VERDICT: MEANING rows=6

All six amended rows (LLR-140, LLR-143, LLR-151 `detail`; TC-132, TC-144,
TC-145 `method`) change what a builder or a test must do, and all six were
judged blessable: true of the code at c429dd0c, exercised by the tests their
cases name (the adjudicator ran them), and within SR-156 (SR-026 for LLR-143).
The verdict is `docs/reviews/wi-648-adjudicate-the-six-rows-wi-61/001-ADJUDICATE-c429dd0.md`
(0c2228b1).

Re-anchored in its own commit with `intake.py snapshot --reattests
LLR-140,LLR-143,LLR-151,TC-132,TC-144,TC-145`, the first act under WI-635's
row-level refusal. It copied the design-row and test-case records only, and
stamped the six ids.

Not acted on, recorded in the verdict: LLR-140 still lists a
"non-ordinary safety_class" rung that WI-381 deleted and omits two it added
(unamended text, byte-identical in the record; it needs its own authoring
amendment); no test case's Evidence cites `tests/test_bookkeeping.py`; LLR-154
still says the mint commits "the declared generated set".

## Context

WI-612 replaced the claim's clean-trunk refusal and the dispatcher's
dirty-trunk stop with one shared bookkeeping helper that refuses by name a
dirty path the step must write, and ignores the owner's scratchpad. Six
approved rows stated the old behaviour, and the build amended their attesting
cells in the same change (status left `Approved`, nothing re-anchored):

- LLR-140 `detail`, LLR-143 `detail`, LLR-151 `detail` (plus traced `module`
  and `code_symbol`)
- TC-132 `method`, TC-144 `method`, TC-145 `method` (plus traced `verifies`)

Each row now differs from its copy in `docs/archive/last_approved/`. The
design-row and test-case tiers are released to the adjudicator
(`human_approval_through = "DevStg-Needs"`), so a MEANING verdict is
re-attested by the adjudicator, re-anchoring only these rows.

## Done-when

- Each amended row is ruled MEANING or CLARITY, with the verdict recorded
  where the amendment brief puts it.
- A MEANING row whose new text is blessable is re-anchored in its own commit,
  naming exactly these rows; one that is not gets its corrective work drafted
  in `## Dispositions`.
