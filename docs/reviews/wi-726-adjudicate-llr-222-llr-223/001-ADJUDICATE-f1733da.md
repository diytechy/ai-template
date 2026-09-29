# ADJUDICATE — WI-726 — amendment at f1733da

Independent adjudication, spine-acts batch G, of the twelve approved rows
whose approved cells WI-723 amended when it built OI-97 (a), the joint-delivery
class. The question the brief asks: did each amendment change the row's
MEANING or only its CLARITY? The brief was read in full. The routed pointer
cells were also read from the registries and ruled, the new `delivered_with`
first among them. The owner's ruling of OI-97 (the `decision` cell in
`docs/requirements/open-items.toml`, and
`docs/log.d/2026-09-28-owner-ruling-oi97.md`) sets three checks for every
joint row, applied on each line below:

1. **Alignment.** Read every sibling and the assumptions each sibling cites
   directly. They must line up around a shared need, and no sibling's
   assumptions are imported.
2. **Tier.** A joint row still states a behaviour at a boundary. A row whose
   output crosses none and only feeds a sibling belongs at LLR.
3. **Re-opening.** A changed `delivered_with` re-opens attestation. That is
   why these rows are here.

Before the amendment, each of the seven SRs made no claim about how its need
is delivered, and SR-193 reported it as unclassified (the honest "not known").
After it, each row asserts, in a cell the kit now treats as approved content
(`acceptance_record.SPINE_APPROVED_CELLS`), that its need is delivered
together with named siblings. The classifier's verdict on the row changes too.
That is a change in what the row claims, so each is MEANING, and this session
re-attests the ones it would bless.

- [MEANING] SR-015 Delivered-With -> no claim; unclassified -> joint with SR-157 on SN-002 -> a new approved claim about the row's delivery argument. Alignment: SR-015 states the PB registry's Refs invariant, and SR-157 is the harness verdict that polices it. Both rows' Rationales already name this "deliberate pair". SR-157 cites no assumption, so nothing could be imported. Tier: SR-015's observable, a PB row with unresolvable Refs being a finding, is read by the owner at B-09, so it holds as an SR. BLESSED; re-attested.
- [MEANING] SR-033 Delivered-With -> no claim; unclassified -> joint with SR-006 and SR-049 on SN-004 -> a new approved claim. Alignment: the release-checklist generator, the gate harness (SR-006) and the derived stage (SR-049) together are how a gate is passed and read. Both siblings are coincident and cite no assumption, so nothing is imported. Tier: the checklist is a view read at B-09. The link is weaker than the others. SR-006's coincident waiver claims it alone delivers SN-004's acceptance, and SR-033's own Rationale calls the checklist this project's answer to the PERFORMANCE charter. So the claim holds in the sense the cell defines ("together with this row, deliver its needs"), not in the sense that SR-033 is a necessary link. It is true, not the strongest statement: noted, not a finding. BLESSED; re-attested.
- [MEANING] SR-111 Delivered-With -> no claim; unclassified -> joint with SR-011 and SR-036 on SN-001 -> a new approved claim. Alignment: the kit-version stamp is the base the documented re-sync (SR-036) diffs from, and the no-clobber re-run (SR-011) is the other half of the re-sync clause. SR-111's Rationale argues exactly that contribution. SR-036's DA-014 (the adopter upgrades through the documented route) is SR-036's premise, reached by SR-111 only through SR-036, and it is correctly not copied. Tier: the stamp is written into the adopter's repository at B-05 and read by a maintainer, so it holds. BLESSED; re-attested.
- [MEANING] SR-174 Delivered-With -> no claim; unclassified -> joint with SR-148 and SR-170 on SN-025 -> a new approved claim. Alignment: the identity allocated once serves the deterministic frontier (SR-148) and is minted by the serial actor (SR-170). SR-170's Rationale names SR-174 as identity allocation's home, and SR-174's argues its contribution to SN-025. DA-006 (SR-148's) and DA-013 (SR-170's) stay with their citers. Tier: the identity lands in governed writes at B-01 and is read in trailers and archived documents, so it is not consumed only by a sibling. BLESSED; re-attested.
- [MEANING] SR-177 Delivered-With -> no claim; unclassified -> joint with SR-156 and SR-170 on SN-027 -> a new approved claim. Alignment: SN-027's own `why` assigns the observability of its fan-out claim to the lane-utilisation report. SR-156 is the bounded fan-out it measures, and SR-170 the serialized shared surfaces. DA-006 and DA-013 stay with SR-156 and SR-170. Tier: the report is read at B-09. BLESSED; re-attested. Outside the amended cell, and not this act's to judge (the brief: the cells below and nothing else): SR-177's Rationale still reads "NOT DECOMPOSED … the row lands Drafted-undecomposed" at `Status = Approved`, with LLR-196 under it, and cites a plans document by section. That is a receipt, folded as an optional item into WI-724's draft.
- [MEANING] SR-223 Delivered-With -> no claim; unclassified -> joint with SR-154 and SR-175 on SN-026 -> a new approved claim. Alignment: the per-model guardrails payload is part of what a session on a routed model is told. SR-154 carries SN-026's roster and consent that choose the model, and SR-175 the declared inclusion rule for what is dispatched. SR-154's DA-007 (a cross-family reviewer finds what the author missed) is no premise of SR-223's and is correctly not imported. OI-97 named this labelled derived row among the nine, and joint delivery does not undo its DERIVED label. Tier: the payload crosses to the runner at B-10, so it is not consumed only by a sibling. BLESSED; re-attested.
- [MEANING] SR-225 Delivered-With -> no claim; unclassified -> joint with SR-139 and SR-140 on SN-029 -> a new approved claim. Alignment: SN-029's delegated run is held by the approval ordinal (SR-139), recorded per approval (SR-140), and recorded per delegated call (SR-225). DA-003 (a Status change on a human-held rung means a human judged) is about approvals, not about the calls SR-225 records, so leaving it uncited is right. Tier: the close refusal is read at B-09. BLESSED; re-attested.
- [MEANING] SR-193 Requirement, AcceptanceCriteria -> report each SR that neither cites its assumptions nor records a coincident waiver; bridged, coincident, unclassified and both; citations traced, the waiver approved -> the same plus a third route: siblings sharing a need make a row joint; an undeclared sibling fails; a disjoint sibling is reported; joint rows may cite their own assumptions and inherit none; joint plus a waiver is reported; Delivered-With re-opens attestation -> a new class, a new failure, new advisories and a new re-opening rule. `SN-Refs` SN-043 and `Boundary-Refs` B-09 HOLD. The text is closed: the joint condition ("one or more declared requirements that share at least one of its needs") and the unclassified fallback ("none of the three") together settle every case. It implements the owner's ruling, including no inheritance. BLESSED; re-attested. The code does not meet it (below, under LLR-223), which is the implementation's defect and not the text's. Noted, not a finding on this cell: the Rationale does not yet argue the third class or why Delivered-With re-opens attestation while DA-Refs does not. It is folded as an optional item.
- [MEANING] LLR-222 Detail -> the tier gains `da_refs` and `coincident`; the template carries both -> the tier carries `delivered_with` too (a list, in REF_COLS), and Delivered-With is in `SPINE_APPROVED_CELLS`; the template carries all three -> a new key and a new approved-cell membership. Every claim was checked true at HEAD: `migrate_carrier.py` 149/314, `spine_carrier.py` 345, `kitlib/spine.py` 803, `acceptance_record.py` 352, and template line 29. The traced `Module`/`CodeSymbol` re-points (acceptance_record.py, SPINE_APPROVED_CELLS) resolve. `SR-Refs` SR-193 HOLDS. BLESSED, but NOT ANCHORED this sitting (see the act below). Outside the amended cell: the Title still names only "assumption citations and coincident waiver". Folded as optional.
- [MEANING] LLR-223 Detail -> bridged, coincident, unclassified and both, from DA-Refs and Coincident -> joint from Delivered-With, taking precedence over DA-Refs and importing no sibling assumptions, with new advisories and failures -> a new class and new rules. NOT BLESSED. Its joint condition, "A non-empty Delivered-With whose entries are declared requirements sharing a need", reads as EVERY entry sharing a need. SR-193 makes a row joint when ONE OR MORE siblings share a need. So parent and child disagree on a row naming one sharing and one disjoint sibling. The code implements neither. `assumption_rules._classify` returns `joint` for any non-empty, all-declared sibling list (`elif siblings: cls = "joint"`, line 476). Run at HEAD, a row whose only sibling shares no need classifies `joint` and gets no "unclassified" report, where SR-193 says it is unclassified. The design row the code must match has to state the condition exactly. RETURNED through WI-724's draft.
- [MEANING] TC-220 Expected, Method -> the bridged, coincident, unclassified and both cases, an undeclared citation, need references unchanged -> the same plus joint, joint with its own citations, joint with a waiver, a disjoint sibling reported, an undeclared sibling failing, direct coupling only -> new cases and a new claim ("joint … classified as stated"). NOT BLESSED. No case asserts the class of a row whose siblings share no need. `test_a_joint_requirement_and_sibling_with_no_shared_need_are_reported` checks only the advisory, so SR-193's share condition for the joint class goes unverified, and it is exactly where the implementation departs. A row claims what its evidence asserts. RETURNED through WI-724's draft.
- [MEANING] TC-222 Expected, Method -> the listed approved cells re-open their row's attestation -> Delivered-With is among them -> an added case. `Verifies` HOLDS (SR-193 among the eight, and LLR-225). `tests/test_cell_classes.py` adds `(SR-003, "Delivered-With", "approved")`. BLESSED, but NOT ANCHORED this sitting (see below).

## The act

Re-attested in this sitting's one act commit: SR-015, SR-033, SR-111,
SR-174, SR-177, SR-193, SR-223 and SR-225 (`--reattests`; no `Status`
moves). The SR registry is authorised on its own, with no drifted row left
unnamed.

Not anchored: LLR-222 and TC-222. Both are blessed, but their registries
cannot be copied while LLR-223 and TC-220, which are returned, hold drifted
approved text. The snapshot names exactly those two rows when the act
includes those registries (checked read-only with
`baseline_snapshot.refresh_refusal`). A returned row cannot be re-attested,
and naming it would bless text this verdict refuses. So LLR-222's and
TC-222's re-attestation, like WI-728's LLR-286, is owed to the first act
that can copy `low-level-requirements.toml` and `test-cases.toml`. That act
comes after the draft in WI-724's `## Dispositions` resolves LLR-223 and
TC-220.

Tests I ran at f1733da (not claimed): `tests/test_assumption_rules.py` and
`tests/test_cell_classes.py`, among the 351 passed recorded in WI-724's
verdict. At HEAD, a two-row probe of `classify_srs`, where SR-001 names
disjoint SR-002, returned `joint` for SR-001 with no unclassified advisory.

VERDICT: MEANING rows=12
