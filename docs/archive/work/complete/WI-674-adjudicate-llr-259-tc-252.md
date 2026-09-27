+++
id = "WI-674"
title = "adjudicate: LLR-259, TC-252 - spine rows authored Drafted by WI-577 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-259", "TC-252"]
+++

## Deliverable

**OUTCOME: RETURN rows=2.** An independent Fable adjudicator, which authored
neither row, read LLR-259's and TC-252's whole chain. Its verdict is
`docs/reviews/wi-674-adjudicate-llr-259-tc-252/001-ADJUDICATE-efa9e3c.md`.

- SR-139 is the right parent (SR-049 is the stage-derivation row).
- Every LLR-259 clause is true of `trace.py`.
- IF-224 is cited, not allowlisted.
- `tests/test_trace_briefs.py` is green (31 passed).

Both rows return together, as the two halves of one seam:

- TC-252's method claims a freshness check on every written brief, but two
  of the four briefs are never read back.
- LLR-259's "ids in its summary" clause has no assertion.
- LLR-259 omits the stated-empty owner's section that the code renders and
  TC-252 asserts.

No row was approved and no snapshot was taken. The follow-up is minted from
this spec's Dispositions as **WI-677**, which re-files the first approval
when done.

## Context

Filed by hand at WI-577's integration (the integrator merges by hand, so
intake's first-approval mint arm did not run). WI-577 carried out OI-82's
ruling on the owner's approval brief and, because no spine row stated that
rendering, authored these two rows Drafted (arbitration ruling 10 of
`docs/reviews/2026-09-26-wave3/ARBITRATION.md`), so that IF-224 is cited by a
test case rather than allowlisted:

- LLR-259 authored in `docs/requirements/low-level-requirements.toml`, under
  SR-139 (the builder named SR-049 as the alternative parent; judge it)
- TC-252 authored in `docs/test/test-cases.toml`, verifying SR-139, LLR-259
  and IF-224

Outcomes: read each row's WHOLE CHAIN — the parent SR, the sibling LLRs, the
test cases — and either APPROVE (move the rows' `Status` to `Approved` and
take the anchoring snapshot, `python project-trajectory/scripts/intake.py
snapshot --approves "<REGISTRY>=<this row>"`, in ONE reviewed commit on this
lane) or RETURN with findings, drafting the follow-up in a `## Dispositions`
section of THIS spec. The design and test tiers are released to the
adjudicator (`human_approval_through` holds only DevStg-Needs, or
DevStg-Boundary once the C1 sitting lands).

## Done-when

- A verdict is committed under `docs/reviews/` at the path the brief names,
  with one `APPROVE` or `RETURN` line for each of LLR-259 and TC-252 and
  exactly one `OUTCOME: APPROVE|RETURN rows=2` line, in a commit carrying this
  row's `WI:` trailer.
- Each approved row's `Status` moves from `Drafted` to `Approved` with no other
  registry cell changed, and `intake.py snapshot --approves` names only the
  registries holding an approved row, in one reviewed commit after the verdict
  commit.
- Each returned row keeps every cell byte-exact, and this spec's
  `## Dispositions` section drafts its follow-up.

## Dispositions

```toml
title = "LLR-259/TC-252 return: one TC Method sentence claims a freshness check two arms never run, one LLR clause has no assertion, and one rendered decision the test enforces is missing from the design row"
workstream = "process"
safety_class = "spine"
buildtier = "medium"
priority = 3
specref = "docs/requirements/low-level-requirements.toml"
bar = "DevStg-Tests"
```

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
