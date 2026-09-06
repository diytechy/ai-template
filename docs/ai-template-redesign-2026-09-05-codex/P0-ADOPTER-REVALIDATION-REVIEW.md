# P0a adopter-revalidation review record

**Fixture basis:** the populated Node adopter in
`tests/test_old_kit_resync.py::test_node_adopter_upgrade_preserves_populated_owner_content`,
validated against committed implementation `77612fb217b1b0d18b420d7460b394e7398d7d0f`.
The documented current-kit re-sync steps and measurements are recorded in
[P0 adopter evidence](P0-ADOPTER-EVIDENCE.md).

All eight upgrade/catalog tests passed on that clean committed tree
(`8 passed in 9.51s`); this source stamp identifies code and fixture state,
not an adopter approval or a passing manual Inspection.

The fixture is a controlled, fictional adopter named **Signal Triage**. Its
real fixture records are: a vision for trustworthy browser-signal incident
timelines; `SN-701` on event source and confidence; `SR-701` on retaining those
fields; a custom `DATA-PROVENANCE` hat activated by `telemetry`; a draft
source-confidence WI; and a Node application/test. The add-only upgrade test
proves byte preservation and Git-history retention. The separate overwrite
route demonstrates the documented operator restore/merge followed by carrier
conversion and current-harness checks; preservation is not a property of
`--force`. Neither route judges adequacy. This record supplies review examples;
none of its proposed hats, needs, SRs, or approvals are written to the fixture
or to a live adopter.

## Review boundary

The current target-kit change is tooling and carrier migration. It does not
alter Signal Triage's stated incident-timeline purpose, browser-signal boundary,
or owner decisions. A reviewer may therefore record **no relevant semantic
impact** for that target upgrade, citing the preserved README, custom hat,
`SN-701`/`SR-701`, draft WI and history. That is a scoped conclusion, not a
claim that a preserved charter has been revalidated or that a future product
change needs no review.

The fixture also demonstrates why copying this repository's [O1–O6 purpose anchors](../../README.md#project-vision) is
wrong: its relevant outcome is dispatchers distinguishing source/confidence in
an incident timeline, which is neither a request to adopt this kit's objectives
nor evidence that any kit hat is relevant. The adopter retains its own vision
and selected `DATA-PROVENANCE` question.

## Changed-purpose example — proposed, not adopted

Assume the fictional adopter later expands from browser signals to field-device
automated incident recommendations. A device can now submit a derived event as
though it were observed, and the decision can trigger an operator escalation.
The review begins from that changed purpose and boundary; it does not infer a
change merely because the kit upgraded.

| Review question | Scoped proposal | Why this is the right tier | Required ordinary follow-through |
| --- | --- | --- | --- |
| Does the existing hat still earn its place? | Keep `DATA-PROVENANCE`; its question directly catches an inferred event presented as authoritative. Test it on a `telemetry`-tagged need and inspect the actual brief. | It remains a relevant failure question for the existing vision. | Record the applicability example and counterexample in the adopter's review record. An unreachable predicate is a review failure, even if the TOML parses. |
| Is another lens needed? | Propose a `RECOMMENDATION-SAFETY` hat only if no retained hat asks whether automated escalation can cause unsafe operator action. | A distinct failure question belongs in the roster before it can guide a derivation. | Define a predicate, question and failure class; compare it with every retained hat. This is a proposal, not a seeded-kit addition or a live charter edit. |
| Is a stakeholder outcome missing? | If dispatchers need a right to recognize and stop a consequential recommendation before action, propose a new SN with that outcome and observable acceptance intent. | That is a distinct stakeholder result, absent from `SN-701`'s source/confidence outcome. A rationale or a new hat cannot create it. | Use normal intake and the adopter's authority. Preserve `SN-701` and prior approvals while the proposal is reviewed. |
| Does a sound need need a new constraint? | If `SN-701` already remains the complete outcome, propose an SR requiring displayed provenance and confidence to distinguish observed from derived recommendations. Attribute the deriving `DATA-PROVENANCE` or approved new hat. | This is a perspective-derived capability/constraint under an existing sound need, not a second need. | Compare the candidate SR with `SR-701`; identify affected LLRs, TCs, interfaces, evidence, and `WI-701`. A reviewed SR amendment gets its normal evidence/approval path. |
| Is there only an implementation gap? | If `SR-701` already fully requires the distinction but `src/timeline.js` or its Node test omits confidence, repair the implementation and evidence. | The obligation already exists; re-minting an SN or SR would duplicate it. | Keep the existing IDs and scope the code/test work to the real gap. |

The review must also reject a tempting but invalid shortcut: copying the kit's
O1–O6 wording, its full hat roster, or a kit SR into Signal Triage would replace
the product's purpose with meta-repository content. The only valid reuse is the
method for asking and recording the above questions.

## Combined/removed-hat check

If the fictional adopter proposes merging `DATA-PROVENANCE` into a broader
data-quality lens, first list every inbound Hat-Ref and the derived
SN/SR/LLR/TC/work relation. Keep the provenance obligation under an explicit
remaining basis or amend it through normal review. The hat's removal alone
neither retires `SN-701`/`SR-701` nor makes an existing approval disappear.
The fixture has no populated inbound Hat-Ref ledger, so this is a required
operator review step, not a machine result asserted by the preservation test.

## Evidence and decision status

The fixture supplies structural evidence for a non-Python populated adopter:
add-only preservation, operator restore/merge followed by conversion on the
overwrite route, current harness checks, and Git-reachable history. This review
record supplies the scoped no-change conclusion. The fixture does
not supply an adopter's independent judgment of relevance, a live new-SN/SR
approval, or cross-platform evidence.

Before treating the changed-purpose proposals as an adoption decision, an
independent review must assess the hat question, whether the outcome is
really absent from `SN-701`, and whether the proposed SR adds a constraint
rather than paraphrase. Its result belongs in the adopter's ordinary scoped
review record. Rejection leaves the preserved fixture records authoritative;
acceptance follows that adopter's existing authoring, approval and trace path.
This sitting uses the requested Opus route to review the worked examples;
adopters do not inherit a vendor requirement. Authoring can proceed within
already-authorized scope; this review is not a new permission gate.
