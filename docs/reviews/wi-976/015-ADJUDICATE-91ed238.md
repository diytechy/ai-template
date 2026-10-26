# WI-976 checkpoint sitting at 91ed238

## amendment

This re-sits the whole set after the act turn on sitting 012 refused. That verdict did not name the retired LLR-297 and TC-312, and the composer dropped them from the amendment scope (wi-976 D-016). The lane since:
- moved the amendment brief's arm into its own module, with no behaviour change;
- made the composer brief a scoped retired row as a removal, and refuse a scope token in neither home;
- reconciled the rows that change touches: LLR-167, TC-161 and LLR-273 (D-018);
- moved TC-211's sample to this sitting.

This sitting's brief, `015-ADJUDICATE-91ed238.brief.md`, is committed, and it shows LLR-297 and TC-312 as removals. The rows sittings 011 and 012 ruled have not moved, so their rulings stand here on the same reasons.

Checks I ran:
- The removal-briefing, hat, round and roster cases in `tests/test_adjudicate_brief.py`, `tests/test_trace_hats.py` and `tests/test_plan_briefs.py` pass (76 run).
- `trace.py --strict` exits 0.
- Both retirement records exist (`docs/log.d/retired/LLR-297.md`, `TC-312.md`).

Ten rows changed MEANING and one only CLARITY:
- I would bless eight MEANING rows on their released rungs.
- SN-036 is held and goes to the owner.
- LLR-273 I would not bless. Its amendment swaps one module name for another in row text, the same shape I returned for WI-851's LLR-249 (sitting 003 there).

**Consequence for the act:**
- The design registry holds LLR-273 drifted and unblessed. An act copying that registry (LLR-167, LLR-183 and LLR-297's removal re-attested, LLR-360's flip) waits until LLR-273 re-sits.
- The system-requirements registry (SR-161, SR-165) and the test-case registry (TC-161, TC-178, TC-211, TC-312's removal, TC-399's flip) carry no unblessed row and can be acted on now.
- SN-036's act is the owner's. No CLARITY row shares its registry.

- [MEANING] SN-036 Acceptance -> before: a machine-readable per-decomposition record and a check reporting a missing perspective -> after: each round reviewed against every applicable declared perspective, the review record naming each outcome, adequacy left to independent review -> not the same: a record and a check become a reviewed round. The rung is held. As at sittings 011 and 012, I recommend it to the owner: it is the owner's 2026-09-06 ruling verbatim, an observable condition that names no instrument.
- [MEANING+BLESS] LLR-297 (removed) -> before: the per-decomposition perspective record: derived applicability and production, an authored no-finding, MISSING, STALE and CONFLICT reported by a warn-first check -> after: removed from the live registry -> not the same: the obligation is withdrawn. Ready to bless as a removal. It is the ruling's own act ("Do NOT build `hats_no_finding`, a sidecar record, or a coverage check"), the Done-when's "LLR-297 and TC-312 are retired, each with its retirement record, at the sitting that rules those amendments", and its record exists. Its parent SR-161 no longer asks for the record, and LLR-183 no longer points its debt at it.
- [MEANING+BLESS] TC-312 (removed) -> before: the record command's derivation, refusal, check-class and CLI cases -> after: removed -> not the same: the verified set loses the record's arms. Ready to bless as a removal. It verified only the retired LLR-297, the command and its test module are gone with it, and its retirement record exists.
- [MEANING+BLESS] LLR-167 Detail -> before: the amendment brief renders the scoped rows whose approved cells drifted, and a scope none of whose rows still differs refuses -> after: the same, plus a scoped row the recorded copy holds approved and the live registry lacks is briefed as a removal. It appears in one block naming it removed, with its approved cells as before and the removal as after; its tier counts for questions, baseline and aftermath; and its identity is its recorded text's digest. A scope token in neither home refuses, naming it, and a present undrifted row still drops out -> not the same: a removal, which the old brief silently dropped, is now judged. Ready to bless:
  - it closes the gap that refused sitting 012's act;
  - each new clause is an observable output or refusal;
  - it adds no name;
  - the arms map's R1 to R6 cases hold it in chained and unchained tiers and in the combined class. Only the questions' tier for a removed row is not asserted separately, a test-depth note.
- [MEANING+BLESS] TC-161 Method -> before: the routed briefs' derivations, refusals and pins -> after: the same, plus the removal briefing in a chained and an unchained tier, for the single-kind and combined classes, the undrifted row still dropping, and the neither-home refusal -> not the same: new arms. Ready to bless. It matches LLR-167's new clause one for one, and its cases exist and pass.
- [MEANING] LLR-273 Detail -> before: "the first-approval brief's anchor (adjudicate_brief._copy_stamp_lines, shared with the amendment brief)" -> after: "(amendment_brief._copy_stamp_lines, shared with the amendment brief)" -> not the same: the contract now places the helper in another module, and an implementation true to the old text fails the new. NOT blessed. The amendment adds a module name (`amendment_brief`) to row text. §0 says an amendment adds no name the rule forbids, and this lane's own move shows why: a row pinned to a module went false at the first refactor. Drop the module qualifier and keep the approved symbol verbatim, as WI-851's LLR-249 did.
- [MEANING+BLESS] SR-161 Requirement, AcceptanceCriteria, Rationale, Coincident, Title, Verification -> before: every decomposition leaves a machine-readable perspective record (Test) -> after: a reviewed round's brief presents every applicable question and its record names each outcome (Inspection) -> not the same: a record and a check become a brief and a review record. Unchanged since sittings 011 and 012 blessed it.
- [MEANING+BLESS] LLR-183 Detail -> before: Hat-Refs as the record's machine-readable half, with the no-finding half owed to LLR-297 -> after: Hat-Refs as row-level provenance, with coverage discharged by the review path -> not the same: the debt toward a sidecar is now discharged elsewhere. Unchanged since 011 and 012.
- [MEANING+BLESS] TC-178 Expected, Method -> before: satisfies the folded acceptance, and COVERAGE claims one advisory on an unused layer -> after: LLR-183's mechanics, with COVERAGE true to the gated advisory -> not the same: the claim narrows and the coverage expectation changes. Unchanged since sitting 012 blessed it.
- [CLARITY] SR-165 Rationale -> before: the reproducibility reason ends by comparing its form to SR-161's old one -> after: the same reason without the comparison -> the same: the requirement and acceptance are unchanged. Unchanged since 011.
- [MEANING+BLESS] TC-211 Expected, Inputs, Method -> before: inspect the chain and a paraphrasing child, with the sidecar as an input -> after: inspect one actual completed decomposition review record, its chain and a paraphrasing child, with the record naming every applicable outcome; Inputs name SR-161, the roster, and this sitting's brief and verdict -> not the same: the inspected object and the verified set change. Ready to bless. Its Inputs resolve to this re-sit: the brief is committed and the verdict is this file.

VERDICT: MEANING rows=11

## first-approval

LLR-360 and TC-399 are byte-identical to the text sittings 011 and 012 approved. The rows that changed since 012 (LLR-167, TC-161, LLR-273) sit outside their chain. I approve both again, on those sittings' reasons.

- [APPROVE] LLR-360 -> the obligation: a decomposition round's brief carries every applicable perspective question and asks for one non-ruling outcome each. A round is a judged SR awaiting first approval or an amended approved need. Parents are each such need, widened by the authoring work item's tags and evaluated alone. The slot is filled only where declared, a combined sitting carries the questions once, the roster is not read outside a round, an absent roster gives the no-perspective line, and an unreadable roster refuses a declared slot, naming it -> what its chain shows: it decomposes SR-161's brief obligation, and TC-399 holds each arm. The merge-mint route's conformance stays owed to sitting 004's successor -> why it is ready: unchanged and refactor-proof, with no `shall` or symbol in its text.
- [APPROVE] TC-399 -> the obligation: each state of the hat block -> what its chain shows: every arm has an existing, passing case -> why it is ready: unchanged since its approval at 011 and 012.

- HAT SECURITY -> no finding -> the round withdraws a warn-first tool and adds brief text no code gates on. No secret, credential or irreversible act is touched, and the removals are reviewed deletions with retirement records.
- HAT FIRST-RUN-ADOPTER -> no finding -> the RESYNC entry states the removed command and inert sidecar files, a template override without the slot composes unchanged, and a fresh spine with no Hat-Refs hears no advisory.
- HAT MAINTAINER -> LLR-183 (Hat-Refs MAINTAINER) -> its detail says why coverage left the cell. LLR-273's unblessed module swap, ruled above, is this hat's concern too: row text pinned to a module the next reviser moves.
- HAT TEST-ENGINEER -> SR-161 and LLR-183 (Hat-Refs TEST-ENGINEER) -> SR-161's Inspection is honest, with TC-399 and TC-178 holding their arms, and TC-161 now drives the removal briefing that sitting 012's act lacked.
- HAT UX-DESIGNER -> no finding -> a removal is shown as one labelled block, the reader's decision first.
- HAT UX-ENGINEER -> no finding -> no rendered surface changes.
- HAT ACCESSIBILITY -> no finding -> textual outcomes only.
- HAT PERFORMANCE -> no finding -> the roster is read only inside a round, and the removal reading adds one recorded-copy lookup per scoped row.
- HAT CONSISTENCY -> no finding against these rows -> the retired rows leave with their parent's and sibling's references updated. The two composing routes' tag sources remain owed to sitting 004's successor.
- HAT INTEGRITY-RECOVERABILITY -> no finding -> the act's refusal on sitting 012 left nothing written, and the composer fix makes the retirement judgeable rather than forcing it through.
- HAT PRODUCT-FITNESS -> no finding -> the outcome is the one the owner ruled on 2026-09-06 and re-affirmed on 2026-10-13: review against perspectives, not a sidecar or a gate.

OUTCOME: APPROVE rows=2

## Returns answered in the lane

```toml
title = "WI-976 spine rework: LLR-273 without its new module qualifier; re-sit LLR-273"
workstream = "process"
sr_refs = ["SR-146", "SR-178"]
needs = ["WI-976"]
safety_class = "ordinary"
buildtier = "quick"
```

This is one cell of spine text, and no code change is called for.
1. **LLR-273 Detail:** write "the first-approval brief's anchor (_copy_stamp_lines, shared with the amendment brief)", keeping the approved symbol verbatim and dropping the module qualifier.

Then re-sit LLR-273 for the amendment, ahead of any act that copies the design registry. Every other row here keeps its ruling, because this touches no other text.

SITTING: JUDGED kinds=amendment;first-approval
