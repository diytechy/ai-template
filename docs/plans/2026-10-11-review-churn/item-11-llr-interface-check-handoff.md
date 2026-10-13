# Handoff: will item 11 (LLRs carried by interfaces) hold, or cause rework again?

> **Answered 2026-10-12 (plan revision 14):** see
> [`item-11-llr-fitness-report.md`](item-11-llr-fitness-report.md). Two claims below
> did not hold. The 55 reproduces (the 90 / 64 does not). Tests (2) and (3) wrongly
> take the end user as the observer: an LLR's observer is the consumer of its
> component-level seam. The text below is kept as written.

Written for: a fresh Opus session, working with the owner interactively. Read-only
analysis first; no spine edits, no commits unless the owner asks.

## Why this exists

The owner is about to decide item 11 of the review-churn plan
([README.md](README.md), "11. What points where"), a program that would rework the
spine's pointers (code → IF → LLR/SR, IF carries requirements, Every LLR carried by
an interface). They want evidence that it reduces future rework before committing
to it. The open worry is that moving LLRs under interfaces relocates the problem
without fixing it: an LLR that is vague, implementation-shaped, or tested at the
wrong level stays wrong under its new interface.

## The question to answer

Of the 302 LLRs, how many are fit to be carried by an interface as written, how
many need rewording first, and for how many is there no sensible interface? Then:
does the item 11 design (or a variant) lower rework, and what should the owner rule?

## What the prior session found (verify, don't trust)

Source: README item 11, "Every LLR then needs an interface" (about line 464) and the
clarification bullet "Will the interface carry the requirement, or only reach it?".

- The plan says 55 of 302 LLRs sit in modules that own no IF. A rough owner-path
  match by the prior session gave 90 LLRs in 64 modules, so the 55 is not
  reproduced; the method differs. Establish the real number and write the method down.
- OI-48 (ruled (d), 2026-08-21) declined "an IF per helper edge" because it makes the
  registry describe library usage, not architecture; edges into a declared kernel
  (`kitlib`) are not seams. Read OI-48 in `docs/requirements/open-items.toml` before
  recommending any `call`-channel seam.
- Worked sample, `project-trajectory/scripts/rendering/traj_render.py` (12 LLRs, no
  IF owned by that module):
  - **LLR-087** (SR-169): "seams terminate at the correct ports, and boundary
    aggregation adds no duplicates". "Correct" is undefined in the LLR. TC-089 /
    `tests/test_traj_views.py::test_when_view_seams_wire_to_block_ports` and
    `::test_boundary_aggregation_dedupes_cross_component_edges` hold the real meaning.
  - **LLR-100** (SR-054): names markup (`<nav class="crumbs">`, `data-root-crumb`).
    TC-103 asserts handler text `trail=trail.slice(0,i+1)`, while its `expected`
    states the user outcome. Evidence: `tests/test_traj_views.py::test_when_view_breadcrumb_restores_parent`.
  - **LLR-101** (SR-052): behavioural (no `role=img` svg over a focusable descendant),
    with an explicit SCOPE limit ("an emitter no rendered artifact exercises is
    unguarded"). TC-104 walks the shipped `PROJECT_STATE.html` and avoids pinning the
    implementation.
  - All three verify the generated dashboard HTML (the user's view) by parsing
    markup, never by executing a click or measuring focusability in a browser.
- Candidate remedy (a suggestion, not a ruling): attach such LLRs to one
  boundary-artifact IF (the dashboard HTML as delivered) rather than minting
  internal call seams. Check whether such an IF exists (`docs/requirements/interfaces.toml`,
  search `data`/`notes` for the dashboard or `PROJECT_STATE`) and whether item 11's
  "Non-code realizations" nuance (README ~line 472) already covers it.

## Method

1. Load `docs/requirements/low-level-requirements.toml` (`[design]`, keyed by LLR id;
   fields `sr_refs, title, module, code_symbol, detail, test_refs, component`),
   `docs/requirements/interfaces.toml` (`[interface]`; `owner, consumers, channel,
   data`) and `docs/test/test-cases.toml` (`[test]`; `verifies, level, method,
   expected, evidence`). Python `tomllib` works.
2. Classify every LLR on the three tests from the README clarification:
   (1) pass/fail wording defined in the LLR itself (flag "correct", "appropriate",
   "properly", "as expected"); (2) states the user-observable outcome, not the
   markup/handler/symbol that produces it; (3) its TCs exercise the interface the LLR
   would attach to, at the level the user sees it (read the evidence tests for a
   sample; do not classify TC level from the `level` cell alone).
3. Separately classify interface availability per LLR: carried by an existing IF /
   would attach to a boundary-artifact IF / only a kernel or internal edge (OI-48
   territory) / pure internal logic with no observable seam (candidate to reframe or
   retire). Sample at least 30 LLRs by hand across components; script the rest and
   say which is which.
4. Estimate rework: for each class, what the item 11 migration costs (reword LLR,
   re-point TC, mint IF, nothing) versus the cost of leaving the spine as is.
5. Report counts, the method, the sample you read by hand, and three or four
   concrete example rows per class.

## Constraints

- Treat everything here as claims to confirm or refute (owner directive, see
  memory `findings-are-claims-rearchitect-ok`).
- Requirements never reference code (2026-10-11 ruling): any reworded LLR you
  propose is in capability voice, no symbols or markup.
- `OWNER_SCRATCHPAD.md` is owner-only: do not read it.
- Do not edit the registries or start a migration. Write findings to a new file under
  this folder (for example `item-11-llr-fitness-report.md`) and stop for the owner.
- Surface design smells as separate findings; do not fix inline.

## Deliverable

A short report for the owner: the counts, the verdict on whether item 11 reduces
rework as designed, any variant you recommend (for example reword-first, then attach),
and the owner calls it leaves open. Lead with the answer.
