Reviewed: 109fb7d034045a70b57afd1954e8fcbbabd3c8a4

### PLAN-CRITIC — WI-982 — Round 1 — 2026-11-04

Reviewer/provenance: fresh non-author Codex session, independently invoked as the plan critic for coordinator leg33. This session did not produce the plan. No provider session id was supplied. The assigned critique carrier is this file; no commit is made, per the coordinator line.

Artifact: docs/plans/WI-982/plan.md, read directly with git show at the Reviewed commit. This is a text artifact; no image or render proxy was needed. The supplied coverage report was assessed against the plan, rather than treated as proof of substantive coverage. No implementer session notes, docs/status.md, docs/log.md, or neighboring critique files were read.

Rubric: docs/rubrics/plan-decomposition.md at the Reviewed commit (blob 89674a5a12463d7878348dde9d2849da4f711b63), including G5's referenced docs/rubrics/architecture-decomposition.md (blob b033f489ae64851e857d0006c6efe82027ad8ccd).

Intent sources: the full docs/work/active/wi-982/WI-982-minted-row-carries-authoring-tags.md and its specref docs/reviews/wi-976/004-ADJUDICATE-81e623b.md; SN-036 in docs/requirements/stakeholder-needs.toml; SR-161 in docs/requirements/system-requirements.toml; and LLR-360 in docs/requirements/low-level-requirements.toml, all at the Reviewed commit. TC-399 and the three excluded TCs were checked as trace context, not used to derive a permissive replacement rubric. Embedded disposition history in the required full spec is not evidence for this verdict.

Rubric adequacy: the anchors independently cover this scoped intent. DevStg-Tests and B2 require actual delivery of the provenance, branchless default, authoring-tag widening and paired-route equality promised by D1-D4; G5 examines the added domain and dependency; D5 supplies the landing checks. SN-036 and SR-161 require applicable perspectives to reach the brief and their outcomes to be reviewed. This WI repairs the applicability input, without changing the outcome-record mechanism. The record-inspection exclusion therefore does not remove an obligation this plan must implement. No missing numbered anchor is needed.

Anchor coverage and judgment:

- DevStg-Reqs: P1-P8 name bounded deliverables and checkable conditions. The detailed steps make the schema, reader, writer, tests, records, sitting and final checks actionable in a build session.
- DevStg-Tests / B2: D1-D5 are substantively covered. P2 tests both minted row kinds, explicit merged-sweep union, inherited authoring cells, empty-cell fallback, branchless variants and the paired shapes. The equality test also checks the lane-specific hat is present and the mint's process hat absent, preventing a vacuous equality. TC-178 and TC-198 concern unchanged Hat-Refs mechanics; TC-211 inspects the completed review record at release. Their exclusions are honest.
- DevStg-Impl / B3: repeated D1-D4 citations have explicit split reasons. Test construction, schema transport, reader behavior, mint behavior and adopter instructions are separate deliverables. P3-P6 remain one code commit, honoring the spec's coupled landing requirement. No row merely restates another row's done-condition.
- G4 / B4: the order carries the spine and test obligations into implementation, then the schema into the reader and the reader into provenance extraction by the writer. The records describe the settled behavior; the combined sitting follows the completed change, and final checks follow the sitting. The stated commit grouping prevents intermediate strict-XPASS failures from becoming standalone code commits. No missing dependency or consequential phantom edge was found.
- G5 (A2, A3, A4, A6, A8): DELTA: within is supported. No new stakeholder state is introduced. The non-empty/empty provenance domain and the hat output's new dependency are explicit. P1/P3 carry the IF-092 and schema edits; P4/P5 carry the dependency through the existing IF-023 carrier. The added intake-to-hats call stays within the declared component scope. The plan records why requirement and component descent stop here.
- B1: the plan amends IF-092 and consumes the existing IF-023/IF-078/IF-090 surfaces; it proposes no duplicate seam.

The pinned implementation supports the route premise: integrate passes outcomes and branch to intake_after_merge; _cmd_sweep supplies a claim identity only for --merged, whose shape requires --branch. The planned branch test therefore distinguishes named-author routes from branchless range and terminal scans. The reader replaces the minted row's classification tags rather than adding to them, preserving the ruling's intended hat set and routing SafetyClass.

Transfer caveat: this protocol's debate/selection evidence comes from QA, math and code with objective verifiers. It has not been benchmarked on plan artifacts; two-planner reconciliation evaluated for plan quality remains an open research gap. This rubric is a supported extrapolation, not a proven instrument.

VERDICT: APPROVE findings=0
