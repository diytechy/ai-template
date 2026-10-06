+++
id = "WI-841"
title = "An in-lane Done-when change is blessed in the lane, in one combined adjudication sitting, before the lane builds on it or closes"
workstream = "process"
sr_refs = ["SR-156", "SR-227"]
specref = "docs/log.d/2026-10-06-wave17-coordinator.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the wave-17 coordinator on 2026-10-06. The owner agreed the
design in conversation that day.

Nothing stops a lane from editing its own Done-when, and that is right: WI-835
had to change its scope in the lane, twice, by the owner's rulings. The blessing
comes only after the merge. Intake compares the closed spec's Done-when with
the claimed one and mints a goalposts adjudication row (`intake.py`, the
merged-outcomes arm; SR-156, LLR-262). WI-835's merge minted WI-837 that way,
which shows three weaknesses:

- The lane closes on unblessed scope, and the blessing needs its own claim,
  which the pause blocks, and its own session.
- The row is minted with no brief class, so neither the loop nor the
  coordinator's entry point can compose it, and the retained adjudicator cannot
  judge it.
- The lane spent five adjudication sittings (two amendment, three
  first-approval) on what one combined sitting per checkpoint could judge,
  including the SR-227 and SR-231 settlement judged in two passes.

Owner direction: an adjudicator, not a mechanical guard, blesses the change.
The block applies to what consumes the Done-when, not to the test suite: tests
are evidence and stay free to run. Merge-readiness stays with the cross-family
code review (REVIEW-A); it is not folded into the adjudicator, because reviews
stay independent of what they judge.

## Done-when

- A Done-when brief class asks whether each change between the claimed and the
  current Done-when only clarifies the scope or moves it (the amendment
  question, applied to the Done-when lines). It is composed by the shared brief
  step and is retainable under `[adjudicator] retain_for`.
- Its verdict is bound to the exact Done-when text it judged, as an act binds
  registry bytes. A moved scope the adjudicator would not bless is drafted as a
  successor, never a reversal.
- While the current Done-when differs from the claimed one and no verdict or
  owner ruling covers that exact text, the lane is held at two points: its next
  build dispatch, and its close and merge. The commit that edits the Done-when
  is not refused. An owner ruling citing the change (a `docs/decisions` entry,
  as D-007 was at WI-835) counts as that verdict.
- At merge, intake mints the goalposts row only when no in-lane verdict or
  ruling covers the closed Done-when text, so it stays as a safety net.
- One combined sitting per lane checkpoint: a single brief composes every
  pending in-lane judgement (drifted approved rows, Drafted rows and the
  Done-when change) into one verdict with one section per kind. Each section
  keeps its own grammar and acts, and text-then-act still applies. A returned
  item alone is re-sat.
- Tests cover: an edit with no verdict holds the dispatch and the close; a
  covering verdict or an owner ruling releases them; changing the text after a
  verdict holds them again; a combined sitting's sections are each parsed and
  acted on; at merge, a covered close mints nothing and an uncovered one mints
  the row.
- SR-156's rows (LLR-262 or a new LLR, TCs) state the in-lane blessing and pass
  adjudication on the one adjudication path. SR-227's retained classes include
  the new brief.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit. The change is inert for an
  adopter until a lane edits its Done-when.
