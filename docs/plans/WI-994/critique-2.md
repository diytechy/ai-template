Reviewed: 94074d45b2c4861692a35b36dd4a5ef6497388aa

### PLAN-CRITIC — WI-994 — Round 2 — 2026-11-04

Reviewer: Codex, independent critic in this fresh non-author session, invoked by the coordinator for the second and final plan critique. This session did not produce the plan. No provider session id was supplied.

Artifact: `docs/plans/WI-994/plan.md`, read directly with `git show` at the reviewed commit. This is a text artifact; no visual proxy was needed. The supplied coverage report is the coverage input. No earlier critique file, implementer session notes, `docs/status.md`, `docs/log.md`, `docs/reviews/`, or `docs/decisions/` was consulted. Revision commentary embedded in the required artifact is not independent evidence.

Rubric: `docs/rubrics/plan-decomposition.md` as held at the reviewed commit (last modifying commit `489678a52a5a610958ada5e0a908f22749348e3d`), including its WI-913 single-plan application and the invocation's stricter second-round severity rule. G5 also uses `docs/rubrics/architecture-decomposition.md`, principally A2, A3, A4, A6 and A8.

Intent sources: the full `docs/work/active/wi-994/WI-994-test-files-tag-their-tcs.md` at the reviewed commit; its `specref`, `docs/plans/2026-10-11-review-churn/README.md#13-review-only-a-green-tip-review-test-cases-in-stages`; SR-157 in `docs/requirements/system-requirements.toml`; and its SN-002, SN-012 and SN-025 parents in `docs/requirements/stakeholder-needs.toml`.

Rubric-to-intent check: the rubric independently covers the scoped intent. DevStg-Tests and B2 require actual delivery of the declared tag grammar, attributed refusals, strict versus advisory surface, vacuity, migration text and regressions, rather than accepting a permissive example test. DevStg-Reqs, DevStg-Impl, G4 and B4 test whether that delivery can be built in the promised order. G5 tests the changed input and finding domain. These checks support SR-157's mechanically verified findings and declared exit behavior, SN-002's traceable chain and SN-012's proportionality; they do not expand this row into SN-025's scheduler or the later scoped-test selector. No missing anchor was identified.

Transfer caveat: the protocol's debate/selection evidence comes from QA, math and code with objective verifiers. It has not been benchmarked on plan artifacts; reconciliation for plan quality remains an open research gap. This rubric is a supported extrapolation, not a proven instrument.

Anchor coverage and judgment:

- **DevStg-Reqs:** P1–P8 name concrete artifacts and checkable outcomes. The detailed test tables, reader contract, surface call site, migration entry and closeout checks make the rows executable within individual build sessions.
- **DevStg-Tests:** D1–D18 have substantive delivery or evidence steps. D19 is explicitly excluded from build steps because the coordinator supplies A+B review, and the commit sequence names the review handoff. That is an honest division of responsibility, not removal of the review obligation. The excluded existing TCs exercise unchanged rules; the source-side characterization and named trajectory suites cover the affected behavior.
- **DevStg-Impl:** the declared multi-coverage splits are real: P2 authors tests, P3/P4 deliver reader and surface behavior, P1/P7 author and reconcile the spine, and P5/P8 record migration boundaries in their required homes. They do not duplicate implementation ownership.
- **G4 and B4:** the DAG follows consumed artifacts from spine to tests to reader to surface, then documentation, reconciliation and closeout. C3 groups P3, P4 and P5 so the implementation, removed expected-failure marks, exact size stamps and required RESYNC entry land together. No missing or phantom dependency requiring a change was found.
- **G5 (A2/A3/A4/A6/A8):** `DELTA: within` holds. No persistent mode class is added; the four finding shapes and the test-files input are explicitly carried by P1's interface/requirement edits and P3/P4's contracts and implementation. Existing IF-131 and IF-263 carry the change, with an adjudication route for a distinct seam if required. Keeping the component whole fits this scope.
- **B1:** the plan amends the nearest existing seams rather than inventing a parallel parser interface. IF-199's existing token and declaration grammar remain the consumed source of truth.
- **B2:** the cited clauses have concrete deliverables, including refusal-shape tests, Drafted/absent/example TC handling, scaffold gating, code-side output characterization and the one-off differential. Coverage is not citation alone.
- **B3:** the eight rows have distinct deliverables or required closure evidence. Grouping the coupled implementation rows into C3 avoids unnecessary commit coordination while preserving their testable boundaries.

Findings: none. No new failure-mode anchor or TC-hardening proposal is needed.

VERDICT: APPROVE findings=0
