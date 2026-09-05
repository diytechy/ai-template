# Claude Fable adversarial review — findings and dispositions

**Date:** 2026-09-05. **Scope:** review and amend this proposal; no implementation, requirement approval, stage change, commit, or publication.

**Reviewer verdict:** **Adopt-with-corrections.** Read [Fable's unmodified review](FABLE-REVIEW.md). Its finding severities describe the input draft; they are not a second verdict over the revised documents.

The requested model ran through the installed Claude CLI, using `--model claude-fable-5 --effort high` and `CLAUDE_CODE_EFFORT_LEVEL=high`. Session initialization and result usage identify Fable. Only Read/Grep/Glob tools were enabled, with safe mode and no model fallback. No Claude-specific callable tool was available in this session's tool catalog. CLI telemetry also records a small auxiliary Haiku call; the architectural review was produced by Fable, not substituted with Haiku.

Session ID: `e1bc8ef3-ea7b-4959-a9dc-2545478898d2`. Duration reported by CLI: 438,243 ms. Total reported cost: USD 4.003825, including the auxiliary call. [Metadata](FABLE-REVIEW-METADATA.json) records input/output hashes and route details. These are CLI-reported figures, not independently measured billing or reasoning-effort telemetry.

## Dispositions

| ID | Decision | Correction and rationale |
|---|---|---|
| F-01 | **Accept — blocker in implementation order** | Added P1A before new-runner enablement: narrow, reviewed, version-scoped amendments for changed runtime contracts. P8 requires these to land; P9 handles only remaining bulk consolidation. Verified SR-148 expressly requires the old admission partition and LLR-149 the multi-WI batch. Qualification: mechanical trace checks do not prove every semantic clause; the core defect is enabling behavior against incompatible approved contracts, whether or not every test detects it. |
| F-02 | **Accept failure scenario; qualify remedy** | Preserve `keep_nondependent` behavior. Under a stopping hold, drain before preparing the candidate and prevent coordinator promotions during its review. With continuation enabled, retain the pending candidate and reserve the final turn when the owner takes up the decision. Distinguish unchanged artifact-content attestation from exact-tree approval. Rejected the suggestion that an unchanged delta alone should carry tree approval to a new tree: that would weaken the assurance contract. The dial value alone does not establish that human holds are frequent. |
| F-03 | **Accept with conservative scoping** | Intake records affected queued IDs, based on normative scope, requirement/artifact references, dependency closure, and shared/exclusive resources against a specific snapshot. Scheduler consumes that decision. Missing/ambiguous evidence means a global hold. Structured references are useful inputs, not proof of semantic independence; a nonempty list must not create false certainty. |
| F-04 | **Accept** | Claim policy is execution provenance. Current trunk policy governs review/promotion authority, holds, evidence, and publication. Recheck at phase boundaries and promotion; test a mid-flight tightening. |
| F-05 | **Accept** | P5 now requires predeclared numeric experiment budgets and workloads, multi-round rework/arbitration, intake latency, human holds, and configured lane counts. Count all serial phases per completion. Historical whole-WI wall time is not treated as measured exclusive-turn duration. No performance result or threshold satisfaction is claimed yet. |
| F-06 | **Accept missing decision material** | P0 must census historical train sizes, including the named four-row case, and compare one coherent acceptance decision with separate deliverables. Default: consolidate only shared acceptance; otherwise sequence one-WI exclusive assignments and count extra checks/reviews. The census is future P0 work, not a measurement performed during this document revision. |
| F-07 | **Accept citation defect; correct the replacement** | Verified SR-169 is the architecture state view. Replaced it with SR-156 for the serial lane lifecycle, alongside SR-144 and LLR-182 for partial close. SR-170/SR-173 are identified separately for shared regeneration; they are not substitute partial-close contracts. |
| F-08 | **Accept context and cost; qualify inference** | Explain the deliberate nonsemantic-churn rationale for the current four-field digest. Separate transaction revision checks from semantic decision reuse. Hash normative scope inputs, not telemetry/Deliverable/routing-only changes; measure repeated adjudication. Reject the assumption that broader invalidation necessarily makes reuse rare without measuring actual workloads. |
| F-09 | **Accept clarification** | Capability sets use the existing bootstrap mapping/profile; inventory/requirement/check views are generated from existing sources. No second authored manifest/schema. The word “manifest” did not inherently require a new framework, but the ambiguity invited one. |
| F-10 | **Accept** | P0/P5 explicitly compare added receipt schemas, parsers, candidate refs, recovery/export and turn rules against deleted history interpretation. Passing correctness and latency is insufficient if complexity has merely moved. |
| F-11 | **Accept narrowing** | Preserve the settled SN-006 enforcement-fault and SN-029 authority-fault clauses. P1 seeks a ruling only for an unresolved concrete independence-under-hold failure, not a broad reopening of failure policy. |
| F-12 | **Accept** | State that a coordinator reservation does not exclude human commits. Recheck trunk/policy before and after each expensive phase and again at promotion, aborting stale work early. This reduces wasted work; it supplements rather than replaces final correctness checks. |

Also applied Fable's unnumbered schema warning: the shared review envelope carries provenance, findings, and disposition; criteria remain typed subject-specific payloads instead of a universal collection of optional fields.

## What remains proposed

- P1A artifact amendments, train census, scope decisions, and experiment budgets still require implementation-phase work and appropriate authority.
- P5 still must establish whether the same-tree receipt design is simpler and operationally acceptable. This review does not turn that experiment into a proven design.
- One-WI cardinality, changed ordering, partial-close changes, and capability scope remain explicit proposals for owner review.
- Fable has not issued a new verdict over the amended documents. The primary agent checked the revisions against the findings and repository evidence; no claim of a second independent approval is made.

## Location and validation

At review time, `docs/ai-template-redesign-2026-09-05-codex/` was absent and Git showed its files deleted. The adjacent copy existed and was byte-identical to the tracked input at repository revision `0d6f3398`. The user was asked which destination to use. With no destination response at the time of applying corrections, the existing adjacent copy was updated; the repository deletions were preserved.

Validation covers local Markdown file targets, internal anchors, balanced fences, input-to-output diff inspection, and a check that repository status was not changed by this task. No implementation tests were run for this proposal-only revision. The original review snapshot and full CLI output remain in the temporary review workspace; the raw final findings and reproducibility metadata are retained here.
