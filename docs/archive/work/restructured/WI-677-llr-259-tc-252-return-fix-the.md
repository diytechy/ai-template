+++
id = "WI-677"
title = "Make LLR-259 and TC-252 state only what their tests drive, then re-file their first approval"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "spine"
priority = 3
bar = "DevStg-Tests"
needs = ["WI-674"]
+++

## Deliverable

Restructured into WI-582.

## Context

Minted by hand at WI-674's integration from its `## Dispositions` draft (the first-approval adjudication of LLR-259 and TC-252 returned both rows).

VERDICT THIS CONTINUES:
`docs/reviews/wi-674-adjudicate-llr-259-tc-252/001-ADJUDICATE-efa9e3c.md`,
governing line `OUTCOME: RETURN rows=2` over `LLR-259` and `TC-252`. Every
finding was driven on the tree at that commit: `tests/test_trace_briefs.py`
is green (`31 passed`), every LLR-259 clause is true of `trace.py`, the parent
`SR-139` is right (SR-049 is the stage-derivation row and is NOT the parent),
and `IF-224` is cited by TC-252 rather than allowlisted. The rows return
TOGETHER: the design and test halves of one seam, each fix a clause or two.

IN SCOPE — two cells and two assertions, then a first-approval adjudication.

1. `TC-252.method`, last sentence: "The freshness check passes on each written
   brief." The suite writes four briefs and runs `_check` on two
   (`tests/test_trace_briefs.py:1072`, `:1181`). The no-dial arm
   (`test_the_shipped_default_dial_holds_every_chain_and_collapses_none`) and
   the every-tier-released arm
   (`test_a_dial_releasing_every_rung_leaves_the_owner_a_stated_empty_ask`)
   write a brief and never read it back. Preferred remedy: add
   `assert _check(tmp_path).returncode == 0` to both arms, so the sentence
   becomes true and the two renderings that differ most from the split brief
   (no block; a block over an empty owner's section) pass through the
   freshness gate too. Narrowing the sentence to the two briefs it is true of
   is the weaker, acceptable alternative.
2. `LLR-259.detail`, clause "with the chains' ids in its summary". No assertion
   distinguishes the summary's ids from the chain headings below it: the one
   summary check (`test_trace_briefs.py:1047`) tests only the label before
   `</summary>`. Add an assertion in the released-chain test that the text
   before `</summary>` names `SR-002` (and, in the every-tier-released test,
   all three ids), so the clause has a detector. The clause itself stands.
3. `LLR-259.detail`: add the one decision the code makes and TC-252 already
   asserts — when every owing chain is released, the owner's section states
   that no chain on a held rung owes an act (`trace.py:4432-4437`), so the
   brief never reads as nothing owed above a collapsed block. One clause,
   beside "the held ones in the owner's section as before"; wording is the
   builder's, the obligation is that a literal implementer emits the line.

Both rows stay `Drafted` through this lane (an authoring lane never
approves; the merge refuses a lane that flips). Their re-adjudication is
intake's first-approval mint at this successor's merge — or, if the
integrator merges by hand as at WI-577, a hand-filed adjudication naming
both rows.

OUT OF SCOPE: `SPINE_APPROVAL_RUNGS` and any rung table; the adjudication-side
filter (`intake._released_drafted_rows`, `adjudicate_brief.first_approval_values`);
`gen_open_items` (`open-items.html` still renders the unsplit population —
WI-577 noted it, this lane does not take it); `IF-224` (off-spine, its own
approval route); the call-count of `human_approves_spine` in `released_tiers`
(once per tier, untested, benign failure direction — recorded as an
observation, not a finding).

## Done-when

- TC-252's method states only what its tests drive (the freshness check runs on every written brief, or the sentence is narrowed), and a test asserts the summary names the released chains' ids.
- LLR-259's detail states the stated-empty owner's section the code renders when every owing chain is released.
- A first-approval adjudication of LLR-259 and TC-252 is filed, and the commit bar passes.
