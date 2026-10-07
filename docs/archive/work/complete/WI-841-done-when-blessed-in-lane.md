+++
id = "WI-841"
title = "An in-lane Done-when change is blessed in the lane before the lane builds on it or closes"
workstream = "process"
sr_refs = ["SR-156", "SR-227", "SR-232"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 9
+++

## Deliverable

A lane may edit its own Done-when, and an adjudicator blesses the change in the lane. The verdict, or an owner ruling in `docs/decisions` (`done_when = "sha256:<16 hex>"`), is bound to the exact text by a digest. Until it is blessed, one predicate (`kitlib.done_when`) holds the lane's next build dispatch (at the one dispatch point, `agent_loop.routed_session`), a hand close (the `done-when-blessed` hook step) and the merge slot; the editing commit and the tests are never held. An absent claim releases; an unreadable claim or current copy holds, naming why. Intake mints the goalposts row only for an uncovered close. New brief classes `done-when` and `combined` (one sitting per checkpoint, each section with its own grammar and acts), both retainable. Verdict acceptance is a recorded fact: the binding beside a verdict (`<verdict>.requested`) records the requested kinds and the outcome, written by one recorder that both routes call, and a verdict is accepted only when its call succeeded (`session_service.call_succeeded`) and it parses strictly, per physical line, in the one parser (`kitlib.sitting.parse`). Every consumer (the holds, the merge-time mint, the approval-act rung) reads through one accepted-verdict reader, and every act a merge adds must be authorized by an accepted verdict that judged its own rows. Snapshot copies are authorized by registry identity through the one carrier resolver (`spine_carrier`), covering TOML, CSV, markdown and a carrier conversion. Rows: SR-232 (derived) and LLR-307..LLR-310, TC-325..TC-328 approved; SR-156, LLR-167, LLR-262, LLR-277, LLR-278, LLR-305, LLR-306, TC-257, TC-278 re-attested (verdicts 001..019; every return answered in the lane). Codex 6.1 Sol: six narrow rounds, then eleven fresh full-lane gates, the last SOUND (`2874ff0a`). Decisions: `docs/decisions/wi-841.toml` (D-001..D-029).

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

## Adjudication follow-ups, answered in this lane

The first-approval adjudication (`docs/reviews/wi-841-done-when-blessed-in-lane/002-ADJUDICATE-be1e431.md`) approved LLR-309 and TC-326 and returned LLR-307, LLR-308, TC-325, TC-327 and TC-328 with two drafted follow-ups. Under the owner's ruling of 2026-10-06 (a return is answered in the lane, not minted), both are answered here:

- The unreadable claim no longer fails open: `kitlib.done_when.claim_copy` tells an absent claim (a row never claimed through the lane: released) from an unreadable one (held at the build dispatch, the hand close and the merge ladder, naming why; the merge-time mint refuses), D-015, with the tests TC-325 and TC-327 asked for (`63ed4a4e`). LLR-307 and TC-325 are restated (`31f245f5`).
- LLR-308 is split: it keeps the done-when brief class under SR-156, and the combined sitting moves to LLR-310 under SR-232, a derived requirement labelled with its lens and feed-back. TC-327 verifies the split rows and TC-328 states LLR-262's four arms (`31f245f5`). The re-sit judges them.

The amendment re-sit at 264d0e5 (`003-ADJUDICATE-264d0e5.md`) blessed LLR-278 and returned LLR-262's wording, drafted as one more block, answered the same way:

- LLR-262's merge-mint claim arms are restated as one readable obligation, wording only (`538bc9a3`). The next amendment sitting re-attests LLR-262 and LLR-278 together.

The amendment sitting at 9c22f9c (`004-ADJUDICATE-9c22f9c.md`) returned LLR-277's wording, and the first-approval sitting at 03c9ab4 (`005-ADJUDICATE-03c9ab4.md`) returned all seven Drafted rows, answered the same way:

- The current side no longer fails open: one reader serves both sides; an absent claim releases, and an unreadable claim, an unreadable current copy and a claimed row whose spec is gone each hold, naming why; a deleted Done-when section owes a blessing; the test-run exemption, a BLESSED cover and a draftless SUCCESSOR are tested (`1370abed`).
- LLR-277, LLR-307, LLR-308, LLR-310, SR-232, TC-325, TC-327 and TC-328 are restated as the verdicts ask (`236e2034`). The re-sits judge them.

The first-approval sitting at 88314d5 (`007-ADJUDICATE-88314d5.md`) approved LLR-307, LLR-308, LLR-310, SR-232, TC-325 and TC-327 and returned TC-328, with one coverage gap on LLR-307, answered the same way:

- TC-328's Method runs every test its Evidence cites; a test now drives LLR-307's retired-key clause and TC-326 cites it (`e80a0ddf`, `97c87102`).

The amendment sitting at 37217b4 (`013-ADJUDICATE-37217b4.md`) returned TC-278's Method wording, answered the same way:

- TC-278 states the released-tier refusals in their own sentence (`fa005df3`). The re-sit re-attests TC-278 and TC-326 together.
