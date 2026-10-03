# WI-768 adjudication: SR-033 (amended by WI-667, merged on trunk 30ee386..4ba5890)

Independent adjudicator: Claude Opus 5.5. I directed none of WI-667.
The anchor is `docs/archive/last_approved` (SR copy d46c5278).
The governing ruling is WI-667's "Owner ruling 2026-10-02", items 1–9, item 8 in particular: the release checklist's assumptions section.
I checked the row against `gen_release_checklist.assumption_checklist_lines` and `tests/test_release_assumptions.py`.

- [MEANING] SR-033 Requirement/AcceptanceCriteria/Rationale -> emit the release-gate checklist, including a perf-budget section listing each warn-tier PB with its id and allocation -> also emit a separate assumptions section: one item, once, per active Approved assumption and per assumption with no falsifier, each with an ASSUMPTION DA-id marker, its falsifier or a missing-falsifier notice, and the ids of the observation cases naming it; falsified or Drafted assumptions with a falsifier are omitted; an absent registry gives no section and no error; the generator changes no standing -> a correct old generator (budgets only) fails the new acceptance. The Requirement and AcceptanceCriteria cells carry the move; the Rationale states the SN-043 derivation.

Routed pointer, read and ruled, not counted in rows=N: SR-033 SN-Refs gained SN-043. That is sound. The new Rationale sentence states the derivation: a premise is shown false only by someone looking for its falsifier, so the release gate puts each active approved premise, and any with no falsifier, before the person signing. SN-043's own need-text amendment is the owner's to re-attest and is not judged here.

## Re-attestation

The dial releases the SR tier, so the re-attestation is mine. I would bless SR-033 as written.

- It states ruling item 8's inclusion set, marker and absent-tolerance exactly, and item 6's limit: checking asserts only "not falsified", and a person sets standing.
- Ruling R2 holds. The cell names a capability (the release-checklist generator) and an output token (the ASSUMPTION marker), not a script or file.
- Nothing in its text depends on the evidence ladder WI-771 removes.
- "Differentiable" is the owner's own word in item 8. In context it means distinguishable from a requirement check, and the acceptance makes that observable (its own section and marker).

It is named in the combined act's `--reattests`.

A finding for the decomposition below it, ruled in WI-769 rather than here: SR-033 lists "the observation case ids naming it". LLR-296 and `assumption_checklist_lines` list every test case naming the assumption in `Assumption-Refs`, automated or not, and TC-310's test fixture pins an automated case as the listed method. The SR's narrower reading is the one the ruling supports: falsification comes from an observation or a review (items 2, 5 and 6), and the method a person follows is an observation case's. So the child returns to match its parent, and the parent stands.

VERDICT: MEANING rows=1
