# WI-976 checkpoint sitting at 066e66c

## amendment

This re-sits the whole set after sitting 011 (`011-ADJUDICATE-a46aad8.md`). That sitting blessed SR-161, LLR-183 and TC-211, ruled SR-165 CLARITY, recommended SN-036 to the owner, and did not bless TC-178. Since 011's commit (28eb00696), two registry changes have landed:
- TC-178's Method COVERAGE clause is restated to the code, and its Evidence now cites `test_a_spine_that_uses_the_cell_nowhere_gets_NO_advisories`.
- TC-211's Inputs now name this sitting's brief and verdict instead of 011's.

This sitting's brief, `012-ADJUDICATE-066e66c.brief.md`, is committed beside this verdict. Checks I ran: `tests/test_trace_hats.py` passes (29 run), and `trace.py --strict` exits 0. No other row text has moved, so my 011 reasoning stands for the unchanged rows, restated briefly here.

Five rows changed MEANING and one only CLARITY. I would bless the four MEANING rows on released rungs. SN-036 sits on a held rung and goes to the owner. No CLARITY row shares its registry, so nothing else is held behind it.

- [MEANING] SN-036 Acceptance -> before: a machine-readable per-decomposition record of perspectives, applicability and results, with a check reporting a missing one -> after: each decomposition round is reviewed against every applicable declared perspective, and the review record names each perspective and its outcome; an independent review judges adequacy -> not the same: a record and a reporting check become a reviewed round with named outcomes. The rung is held, so this stops here. I recommend it to the owner, as at sitting 011: it is the owner's 2026-09-06 ruling verbatim, an observable condition that names no instrument, recoverable from need and acceptance alone.
- [MEANING+BLESS] SR-161 Requirement, AcceptanceCriteria, Rationale, Coincident, Title, Verification -> before: every decomposition leaves a machine-readable perspective record, and a missing applicable perspective is reportable (Test) -> after: when a round is reviewed, its brief presents every applicable perspective's question and its review record names each outcome (Inspection) -> not the same: a record and a check become a brief and a review record, under another verification method. Unchanged since 011 blessed it. Its Rationale's dated citation remains a warn-only advisory, which the spec asks for.
- [MEANING+BLESS] LLR-183 Detail -> before: Hat-Refs as the record's machine-readable half, with the no-finding half owed to a sidecar row -> after: Hat-Refs as row-level provenance, with per-decomposition coverage discharged by the review path -> not the same: the debt toward a sidecar is now discharged elsewhere. Unchanged since 011 blessed it.
- [MEANING+BLESS] TC-178 Expected, Method -> before: Expected "satisfies the acceptance folded into LLR-183", and Method COVERAGE "a tree whose rows carry no Hat-Refs at all exits zero under --strict and reports exactly one coverage advisory" -> after: Expected claims LLR-183's provenance, resolution, severity and effective-set mechanics, handing SR-161 to TC-211. Method COVERAGE now reads "a tree whose rows carry no Hat-Refs at all reports no finding and no advisory; once at least one row carries the cell, assert exactly one coverage advisory and no finding" -> not the same: the claim narrows, and the coverage expectation changes for an unused layer. Ready to bless. Sitting 011's finding is answered:
  - the clause now matches the code's gate-on-use rule;
  - both halves are held by cited cases, `test_a_spine_that_uses_the_cell_nowhere_gets_NO_advisories` (no advisory) and `test_coverage_is_one_advisory_and_never_a_finding` (one coverage advisory, no finding);
  - the unsupported "exits zero under --strict" claim is gone;
  - the Evidence also lists the design-tier, absent-roster-file and unattributed-hat cases, which hold the arms the map found unexercised.
- [CLARITY] SR-165 Rationale -> before: the reproducibility reason compares its form to "the SR-161 form applied to the partition" -> after: the same reason without that comparison -> the same: SR-165's requirement and acceptance are unchanged, and the dropped analogy named a form SR-161 no longer has. Unchanged since 011.
- [MEANING+BLESS] TC-211 Expected, Inputs, Method -> before: inspect the chain and a paraphrasing child, with the sidecar as an input -> after: inspect one actual completed decomposition review record, its chain and a paraphrasing child, with the record naming every applicable outcome and each child's purpose and stopping reason; Inputs name SR-161, the roster, and this sitting's brief and verdict -> not the same: the inspected object and the verified set change. Ready to bless. Its Inputs now resolve to this re-sit, whose brief is committed and whose verdict is this file. It is the Done-when's TC-211 clause, and this whole-set sitting is the sample it names.

VERDICT: MEANING rows=6

## first-approval

LLR-360 and TC-399 are byte-identical to the text sitting 011 approved, and their chain has moved only as the amendment section records. TC-178's change touches LLR-183's verification, not LLR-360's. I approve both again, on 011's reasons.

- [APPROVE] LLR-360 -> the obligation:
  - a decomposition round's brief carries every applicable perspective question and asks for one outcome each, in lines that leave verdict parsing unchanged;
  - a round is a judged SR awaiting first approval or an amended approved need, and any other set gets no question;
  - parents are each amended need and each need a judged SR names, each widened by the authoring work item's tags and evaluated alone;
  - the slot is filled only where the template declares it, and a combined sitting carries the questions once;
  - outside a round the roster is not read; an absent roster gives its no-perspective line, and an unreadable roster refuses only a declared slot, naming the roster.

  -> what its chain shows: it decomposes SR-161's brief obligation, and TC-399 holds each arm. The merge-mint route's conformance to "the authoring work item's tags" stays owed to sitting 004's successor -> why it is ready: a refactor-proof contract with no `shall` or symbol in its text, unchanged since 011.
- [APPROVE] TC-399 -> the obligation: each state of the hat block, as its Method enumerates them -> what its chain shows: every arm has a named, existing, passing case -> why it is ready: an observable Expected over existing cases, unchanged since 011.

- HAT SECURITY -> no finding -> the round touches no secret, credential or irreversible act: it retires a warn-first tool and adds text to a brief no code gates on.
- HAT FIRST-RUN-ADOPTER -> no finding -> the upgrade's breakage (the removed `record` command, inert `.perspectives.toml` files) is stated in the required RESYNC entry, a template override without the slot composes unchanged, and TC-178 now states that a fresh spine with no Hat-Refs hears no advisory.
- HAT MAINTAINER -> LLR-183 (Hat-Refs MAINTAINER) -> its detail says why coverage left the cell, so a later reader can tell the narrowed role is deliberate.
- HAT TEST-ENGINEER -> SR-161 and LLR-183 (Hat-Refs TEST-ENGINEER) -> SR-161's Inspection is honest, with TC-399 testing the brief. TC-178's evidence now examines the coverage behaviour it claims, which answers sitting 011's finding under this hat.
- HAT UX-DESIGNER -> no finding -> the brief's perspectives part states the reader's one decision, an outcome per hat, once after the sections.
- HAT UX-ENGINEER -> no finding -> no rendered surface changes.
- HAT ACCESSIBILITY -> no finding -> textual outcomes only, with no visual-only or pointer-only interaction.
- HAT PERFORMANCE -> no finding -> the roster is read only inside a decomposition round, and never outside one.
- HAT CONSISTENCY -> no finding against these rows -> SN-036, SR-161, LLR-183, LLR-360 and TC-178 now agree with each other and with the code. The two composing routes' tag sources remain owed to sitting 004's successor.
- HAT INTEGRITY-RECOVERABILITY -> no finding -> nothing durable is updated in place by the new path.
- HAT PRODUCT-FITNESS -> no finding -> the outcome is the one the owner ruled on 2026-09-06 and re-affirmed on 2026-10-13: review against perspectives, not a coverage record or a gate.

OUTCOME: APPROVE rows=2

SITTING: JUDGED kinds=amendment;first-approval
