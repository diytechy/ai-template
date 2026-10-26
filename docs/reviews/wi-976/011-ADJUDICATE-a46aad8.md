# WI-976 checkpoint sitting at a46aad8

## amendment

Six approved rows moved against their copies. Together they carry the 2026-09-06 SN-036 / SR-161 ruling: the perspective-record sidecar and its checker retire, and each decomposition round is reviewed against its applicable hats, with the sitting's verdict naming each outcome. I read the rows against WI-976's Done-when, the lane's ruling fragment, the code at this tip and the arms map. Three of the map's gaps were closed at `a76b2a78a`, and its other findings I re-checked myself.

Checks I ran:
- `trace.py --strict` exits 0.
- The hat, round and roster cases in `tests/test_trace_hats.py`, `tests/test_plan_briefs.py` and `tests/test_adjudicate_brief.py` pass (70 run).
- The brief TC-211 names, `011-ADJUDICATE-a46aad8.brief.md`, is committed beside this verdict.

Five rows changed MEANING and one only CLARITY. Of the five MEANING rows, I would bless three on their released rungs. SN-036 sits on a held rung and goes to the owner. TC-178 I would not bless, for a defect in its own Method that predates this lane.

**Consequence for the act:**
- The system-requirements registry (SR-161, SR-165) and the design registry (LLR-183, plus LLR-360 below) can be acted on now.
- The test-case registry holds TC-178 drifted and unblessed. Any act copying that registry, including TC-211's re-attestation and TC-399's flip, waits until TC-178 re-sits.
- SN-036's act is the owner's, as the Done-when states. No CLARITY row shares its registry, so nothing else is held behind it.

- [MEANING] SN-036 Acceptance -> before: each decomposition has a machine-readable record of the declared perspectives, their applicability and their requirements or no-finding, and a check reports an applicable perspective missing from it -> after: each decomposition round is reviewed against every applicable declared perspective, and the review record names each perspective and its outcome; an independent review judges adequacy -> not the same: the obligation moves from a machine-readable record and a reporting check to a reviewed round whose record names outcomes, and the check is gone. The rung is held, so this stops here, and I recommend it to the owner:
  - it is the owner's 2026-09-06 ruling (re-affirmed 2026-10-13), carried verbatim from `contract_split`;
  - it states an observable condition (every applicable perspective has a named outcome in the review record) and names no instrument;
  - a blind reader recovers the obligation from need and acceptance alone;
  - the partition (coverage and provenance here, adequacy to independent review) is kept.
- [MEANING+BLESS] SR-161 Requirement, AcceptanceCriteria, Rationale, Coincident, Title, Verification -> before: the planning content leaves, with every decomposition, a machine-readable perspective record, such that a missing applicable perspective is a reportable finding (Verification: Test) -> after: when a decomposition round is reviewed, the planning content provides every applicable perspective's question in the brief and requires the sitting's review record to name each outcome (Verification: Inspection) -> not the same: a record and a reporting check become a brief and a review record, and the verification method changes. Ready to bless:
  - a `When` fronts a discrete event, and one `shall` governs one decision;
  - no cell names a file;
  - its acceptance is the fit criterion: perspectives resolve from the declared roster, the brief presents each question, the record names every outcome, and the adequacy review reads it;
  - Inspection is honest for an outcome a reader judges, and TC-399 tests the brief side.

  Two notes, not findings. The Rationale's dates ("2026-09-06, re-affirmed 2026-10-13") draw `trace.py`'s warn-only citation-frame advisory. The spec asks for exactly that naming of the authority ruling, so I leave it. And no TC states the acceptance's last clause ("the independent adequacy review reads that record") in so many words; TC-211's inspection is that reading.
- [MEANING+BLESS] LLR-183 Detail -> before: Hat-Refs as the machine-readable half of the perspective record, with "NOT DISCHARGED: ... the no-finding half is a per-decomposition artifact, built under LLR-297" -> after: Hat-Refs as the row-level provenance part of perspective review, with per-decomposition coverage "discharged by the existing review path" (roster applicability, the brief's questions, the record's outcomes), and applicability or no-finding outcomes never stored in the cell -> not the same: a debt the row carried toward a sidecar is now discharged elsewhere, and the cell's role narrows. Ready to bless. The Hat-Refs mechanics are byte-identical to the blessed text. The new sentence points at the path SR-161 and LLR-360 now state, rather than restating them as obligations, and it adds no name. The arms not exercised by tests (the carrier's optional typed key, the TRACED classification) are pre-existing approved arms this amendment does not touch.
- [MEANING] TC-178 Expected -> before: "Satisfies the acceptance folded into LLR-183 (parent SR-161)" -> after: "Satisfies LLR-183's Hat-Refs provenance, name-resolution, severity and effective-set mechanics; SR-161's perspective-review acceptance is inspected by TC-211" -> not the same: the claim narrows from SR-161's acceptance to LLR-183's mechanics, handing SR-161 to TC-211. NOT blessed. The narrowing is sound, but re-attesting it would bless the row's Method, and one Method clause is false at this tip:
  - The Method says: "COVERAGE NEVER GATES: assert a tree whose rows carry no Hat-Refs at all exits zero under --strict and reports exactly one coverage advisory."
  - The code reports no advisory for that tree. `test_a_spine_that_uses_the_cell_nowhere_gets_NO_advisories` pins `advisories == []` on it, deliberately, because the first-run adopter's spine carries no Hat-Refs.
  - The evidence case `test_coverage_is_one_advisory_and_never_a_finding` drives a tree with one filled cell, and it is a unit call, not a `--strict` run.

  So the Expected's "severity" claim rests on a Method that misstates the severity rule. The fix is one clause.
- [CLARITY] SR-165 Rationale -> before: the reproducibility reason ends "— the SR-161 form applied to the partition instead of the perspective set" -> after: the same reason without that analogy -> the same: SR-165's requirement, acceptance and every other cell are unchanged. The removed words compared its form to SR-161's old record-and-recompute form, which no longer exists, so a reader acting on either text does the same thing.
- [MEANING+BLESS] TC-211 Expected, Inputs, Method -> before: inspect the chain and an extra paraphrasing child for children with no independent purpose, with the sidecar among the inputs -> after: inspect one actual completed decomposition review record, its complete chain and an extra paraphrasing child. The record must name every applicable perspective's outcome, and each child must have a purpose and a stopping reason. Inputs name SR-161, the hats roster, and this sitting's brief and verdict, and no sidecar -> not the same: the inspected object and the verified set change. Ready to bless. It is the Done-when's TC-211 clause, its inputs resolve (the brief is committed and this verdict is its record), and it inspects SR-161's acceptance where TC-178 now hands it.

VERDICT: MEANING rows=6

## first-approval

Two lane-added rows await a first approval: LLR-360 and TC-399, under SR-161 as blessed above. The arms map's three gaps on these rows (the parse invariance, the no-read outside a round, and the slot-scoped refusal) are closed in LLR-360's text at this tip. Every TC-399 evidence node exists and passes.

- [APPROVE] LLR-360 -> the obligation:
  - a decomposition round's sitting brief carries every applicable perspective question and asks for one outcome per perspective, in lines that are neither row-ruling nor machine lines, so parsing is unchanged;
  - a round is a judged SR awaiting first approval, or an amended approved need, and any other judged set carries no question;
  - parents are each amended need and each need a judged SR names, amended SRs included, each widened by the authoring work item's tags and evaluated alone;
  - the slot is filled only where the template declares it, and a template without it composes unchanged;
  - a combined sitting carries the questions once;
  - outside a round the roster is not read; an absent roster gives its no-perspective line, and an unreadable roster refuses a round's composition only when the slot is declared, naming the roster.

  -> what its chain shows: it decomposes SR-161's brief obligation with the Done-when's closed input space, and TC-399's twenty cases hold each arm. "The authoring work item's declared tags" now states the rule sitting 004 asked for. The merge-mint route does not yet meet it: it widens by the minted row's tags. That conformance is owed by sitting 004's successor and was re-confirmed at sitting 010. The row states the intended contract, and the successor brings that route to it -> why it is ready: a contract in observable inputs, outcomes and refusals, with no `shall` and no symbol in its text, naming only the two shipped templates as boundary artifacts in its Module.
- [APPROVE] TC-399 -> the obligation: each state of the hat block (non-round, round, parents, per-need widening, slot declared or not, combined once, absent and unreadable roster, non-ruling outcome lines) -> what its chain shows: its Method enumerates every LLR-360 arm, and each arm has a named, existing, passing case -> why it is ready: an observable Expected over existing cases, with Unit at Full honest. Two notes, not findings:
  - Expected's closing "remain as stated" defers to LLR-360's sentences rather than restating them; the Method names them one by one.
  - The instruction's "every hat, once each" wording is asserted only as the presence of the non-ruling form.

- HAT SECURITY -> no finding -> the round touches no secret, credential or irreversible act: it retires a warn-first tool and adds text to a brief whose outcome lines no code reads.
- HAT FIRST-RUN-ADOPTER -> no finding -> the upgrade's breakage, an adopter script calling the removed `record` command, and its inert `.perspectives.toml` files are stated in the RESYNC entry the Done-when requires, and an overridden template without the slot composes unchanged.
- HAT MAINTAINER -> LLR-183 (Hat-Refs MAINTAINER) -> its amended detail says why coverage left the cell (stored outcomes would duplicate review facts and go stale), so a later reader can tell the cell's narrowed role is deliberate.
- HAT TEST-ENGINEER -> SR-161 and LLR-183 (Hat-Refs TEST-ENGINEER) -> SR-161's verification moves honestly to Inspection, with TC-399 testing the brief side. TC-178's false COVERAGE clause, ruled above, is this hat's finding: evidence passing without examining the claimed behaviour.
- HAT UX-DESIGNER -> no finding -> the brief's perspectives part puts the reader's one decision (an outcome per hat) after the sections and states it once.
- HAT UX-ENGINEER -> no finding -> no rendered surface changes, and the brief is plain text the composer emits.
- HAT ACCESSIBILITY -> no finding -> textual outcomes only, with no visual-only or pointer-only interaction.
- HAT PERFORMANCE -> no finding -> the block adds a bounded roster read only inside a decomposition round, and none outside it.
- HAT CONSISTENCY -> no finding against these rows -> SN-036, SR-161, LLR-183 and LLR-360 now say one thing. The one disagreement found is between the two composing routes' tag sources, owed to sitting 004's successor.
- HAT INTEGRITY-RECOVERABILITY -> no finding -> nothing durable is written in place by the new path. The retirement deletes files in reviewed commits.
- HAT PRODUCT-FITNESS -> no finding -> the outcome is the one the owner ruled on 2026-09-06 and re-affirmed on 2026-10-13: review against perspectives, not a coverage record or a gate.

OUTCOME: APPROVE rows=2

## Returns answered in the lane

```toml
title = "WI-976 spine rework: TC-178's COVERAGE clause made true to the gated coverage advisory; re-sit TC-178"
workstream = "process"
sr_refs = ["SR-161"]
needs = ["WI-976"]
safety_class = "ordinary"
buildtier = "quick"
```

This is one cell of spine text, plus one existing case cited. No code change is called for.
1. **TC-178 Method:** restate COVERAGE to match the code. A tree whose rows carry no Hat-Refs at all reports no finding and no advisory. Once at least one row carries the cell, the tree reports exactly one coverage advisory and still never gates. Cite `tests/test_trace_hats.py::test_a_spine_that_uses_the_cell_nowhere_gets_NO_advisories` beside the existing coverage case in Evidence. If the "exits zero under --strict" claim is kept, the Method should name the real-run case that drives it, or drop the claim.

Then re-sit TC-178 for the amendment, ahead of any act that copies the test-case registry. The other rows here keep their rulings, because none of this touches their text.

SITTING: JUDGED kinds=amendment;first-approval
