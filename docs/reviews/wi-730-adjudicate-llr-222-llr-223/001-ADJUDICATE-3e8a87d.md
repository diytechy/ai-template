# ADJUDICATE — WI-730 — amendment at 3e8a87d

Independent adjudication, spine-acts batch H, of the seven approved rows whose
approved cells moved after their last attestation. The brief's question is
whether each amendment changed the row's MEANING or only its CLARITY. The
brief was read in full. It measures against `docs/archive/last_approved` as
last written: the SR registry copied at 6f6613e2, the LLR and TC registries at
2d264589. For LLR-222, LLR-223, TC-220 and TC-222, the before-text is therefore
the text from before WI-723 built the joint-delivery class. For SR-177 and
SR-193 it is batch G's re-attested text, so their only change is WI-729's
rationale restatement. LLR-286 carries WI-721's Detail change. The routed
pointer cells were read from the registries and ruled:

- `SR-Refs`: SR-193 for LLR-222 and LLR-223; SR-226 for LLR-286.
- `Verifies`: SR-193, LLR-222 and LLR-223 for TC-220; the eight SRs and LLR-225 for TC-222.
- `SN-Refs`: SN-027 for SR-177; SN-043 for SR-193.
- `Delivered-With`: SR-156 and SR-170 for SR-177, which batch G re-attested and which is unchanged since.

OI-97's ruling (the `decision` cell in `docs/requirements/open-items.toml`)
sets the checks for the joint class: no inheritance of sibling assumptions,
alignment judged by the adjudicator, a joint row still states a behaviour at a
boundary, and a changed `delivered_with` re-opens attestation. Batch G's
verdicts (WI-726, WI-728) are context, not authority. What WI-729 changed was
read from its archived spec and from `git show 17c54c2f`.

- [MEANING] SR-177 Rationale -> the old text argues the row makes the throughput claim observable rather than budgeted, and records the build gap as descriptive: nothing yet aggregates the per-session wall seconds, API seconds and turns by lane or by run -> the new text says "The report must aggregate the existing per-session wall time, API time, turns and token telemetry by lane and by run" -> not the same. A description of the gap has become a `must`, and it widens the inputs (token telemetry) and the breakdown (by lane AND by run). The row's Requirement and AcceptanceCriteria ask for neither. They ask for a per-run statement of lanes configured, lanes actually occupied and work items integrated per wall-hour, derived from recorded telemetry. A report correct under the old text, which aggregates no tokens and gives no per-lane breakdown, fails the new rationale's `must`. NOT BLESSED. A reason cell that carries an obligation wider than the row's acceptance gives the obligation a second home, and the two homes disagree (spine-authoring §6: the reason cell states what breaks without the row and which alternative lost). Removing the receipt ("NOT DECOMPOSED … lands Drafted-undecomposed") and the plans-document citation was right and is kept. Restate the build gap as a reason, without the `must` or the added inputs. If token or per-lane aggregation is wanted, it belongs in the acceptance, through its own approval.
- [MEANING] TC-222 Expected, Method -> the listed approved cells each re-open their row's attestation, and the listed traced cells re-open none -> the same, with a requirement's Delivered-With among the approved cells -> an added case. `Verifies` HOLDS: SR-193 is among the eight, and LLR-225's `SPINE_APPROVED_CELLS` carries Delivered-With (`acceptance_record.py` 352). `tests/test_cell_classes.py` drives it: `(SR-003, "Delivered-With", "approved")` at line 42, and the column map at lines 64-67. This is what SR-193's acceptance and OI-97 direction (3) require. BLESSED; re-attested in this act.
- [CLARITY] SR-193 Rationale -> the reasons for the waiver, the need link staying on the requirement, and reporting over failing -> the same reasons, plus two argued points: a sibling requirement is neither a premise about the world (a DA) nor a sole-delivery claim (a waiver), and Delivered-With re-opens attestation while DA-Refs does not -> the obligation is identical. Both new points argue what the approved AcceptanceCriteria already require ("classified joint"; "changing assumption citations re-opens no attestation, while declaring or changing Delivered-With or the waiver re-opens the requirement's"). A reader acting correctly on the old text acts the same way on the new. The added prose carries no citation frame and states standing reasons. `SN-Refs` SN-043, `Boundary-Refs` B-09 and the unchanged `Coincident` waiver HOLD. The text is blessed. Its drifted cell is owed a place in the `--reattests` of the first act that can copy the SR registry, and that is NOT this act: SR-177's amendment, not blessed above, keeps the SR registry uncopyable.
- [MEANING] LLR-222 Detail, Title -> the requirement tier gains `da_refs` and `coincident`, and the template carries both -> the tier carries `delivered_with` too (a list, in `REF_COLS`), Delivered-With is in `SPINE_APPROVED_CELLS` while DA-Refs stays traced, the template's SR-000 carries all three keys, and the Title names the joint-delivery siblings -> a new key and a new approved-cell membership. The Title change is clarity inside a row that is meaning. Every claim was checked true at HEAD: `migrate_carrier.py` 149 and 314, `spine_carrier.py` 345, `kitlib/spine.py` 803, `acceptance_record.py` 352, template line 29. `SR-Refs` SR-193 HOLDS. BLESSED, but NOT ANCHORED this act: the LLR registry cannot be copied while LLR-223 (below) holds drifted text that is not blessed.
- [MEANING] LLR-223 Detail -> bridged, coincident, unclassified and "both", from DA-Refs and Coincident -> a row is joint when Delivered-With names one or more declared siblings sharing one of its needs, even beside DA-Refs, and imports no sibling assumptions; it is bridged or coincident otherwise; "DA-Refs with Coincident, or Delivered-With with Coincident, is an advisory naming the contradiction"; a disjoint sibling is an advisory; an undeclared assumption or requirement is a failure -> a new class and new rules. Batch G's finding is answered: the joint condition now reads "one or more", and `_classify` matches it. NOT BLESSED, on the contradiction sentence. It says any Delivered-With beside a Coincident waiver is reported as a contradiction. SR-193's acceptance scopes that report to "both joint delivery and a waiver", and so do TC-220 ("joint with a waiver is reported") and the code (`cls == "joint" and _cell(row, "Coincident")`). I probed it at HEAD. A row whose only sibling shares no need and which records a waiver classifies `coincident`, with only the disjoint-sibling advisory and no contradiction advisory. A row that is joint and carries both DA-Refs and a waiver gets the joint-waiver advisory and not the DA-waiver one. So the design row the code must match again states a condition the code, its parent and its test case do not. This is the same class of defect batch G returned on this row. Scope the sentence to the joint class (a joint row with a waiver, and a non-joint row with DA-Refs and a waiver). If the lane holds that any Delivered-With beside a waiver is contradictory, change the code, TC-220 and SR-193 together instead.
- [MEANING] TC-220 Expected, Method -> the bridged, coincident, unclassified and "both" cases, and an undeclared citation failing -> the same, plus: joint with one sharing sibling; a row whose only sibling is disjoint is not joint (unclassified and reported); a mixed sibling list is joint with the disjoint one reported; joint with its own citations inherits no sibling assumptions; joint with a waiver is reported; an undeclared sibling fails; direct coupling only; the template carries all three keys -> new cases and new claims. Batch G's finding is answered: the class is now asserted in both cases the text claims (`test_a_joint_requirement_and_sibling_with_no_shared_need_are_reported` asserts `unclassified`; `test_one_shared_sibling_makes_a_mixed_sibling_list_joint` asserts `joint`). Every other clause maps to a case in `tests/test_assumption_rules.py`, 198-395. `Verifies` SR-193, LLR-222 and LLR-223 HOLD. The Method agrees with SR-193 and the code on the contradiction scope ("joint with a waiver", "a citation with a waiver"). LLR-223's return above is on the design row's wording and leaves this case true. BLESSED; re-attested in this act.
- [MEANING] LLR-286 Detail -> `retire` refuses unless the id is a live row of its tier's TOML registry, so a legacy-carrier row reads as not live -> the id must be a live row in whichever carrier form the kit's registry reader resolves -> the obligation widened, and the old text allowed what the new one forbids (reporting a live legacy-carried row as a spent id with no record, and refusing a legacy-carried successor). Checked at HEAD: `retire.live_ids` reads the tiers through `spine_carrier`, and `test_legacy_registry_rows_are_live_and_only_a_spent_id_is_reported` (TC-299) drives the widened arm. `SR-Refs` SR-226 HOLDS. Its acceptance says a live id is not reported whatever carries it, and the amendment brings the design row into line with that. The text is unchanged since batch G blessed it. BLESSED, but NOT ANCHORED this act, for the same LLR-registry reason as LLR-222.

## The act

Re-attested in this batch's one act commit, with no `Status` moving: TC-220
and TC-222. The snapshot copies `test-cases.toml`, where WI-731's TC-262 flip
rides beside them. `baseline_snapshot.refresh_refusal`, run read-only on that
exact act, accepted it.

Not anchored, and owed to the first act that can copy their registry:

- SR-193: blessed as CLARITY. The SR registry is blocked by SR-177.
- LLR-222 and LLR-286: blessed as MEANING. The LLR registry is blocked by LLR-223. The read-only refusal for an act copying `low-level-requirements.toml` names exactly LLR-223 (`Detail`).

A row this verdict does not bless cannot be named in `--reattests`, so both
registries stay at their prior snapshot. SR-177 and LLR-223 are RETURNED. Their
follow-up is folded into the one consolidated draft in WI-731's
`## Dispositions`: one lane, and one adjudication at its merge. No registry
cell was edited by this sitting.

Checks I ran at 3e8a87d (results seen, not claimed):
- The six chain test modules gave **352 passed in 51.05s** (recorded in WI-731's verdict).
- A three-case probe of `classify_srs` and `sr_classification_advisories` gave these classes:
  - disjoint sibling plus waiver: `coincident`, with no contradiction advisory;
  - joint plus DA-Refs plus waiver: `joint`, with the joint-waiver advisory only;
  - disjoint sibling plus DA-Refs: `bridged`.

VERDICT: MEANING rows=7
