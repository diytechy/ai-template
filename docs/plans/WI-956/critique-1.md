Reviewed: d838f1f850a2400d8f136446ac45278ac42121a8

### INDEPENDENT CRITIC — WI-956 single-plan critique — Round 1 — 2026-10-20

Reviewer/session: fresh non-author Codex critic session invoked for this review. Invocation record: `2026-10-20c-leg05/plan-956`, assigned round 1 verdict carrier. No provider session id was supplied. This session did not produce the plan. No implementer session notes, status, log, or adjacent plan critiques were consulted; the scope-critique dispositions embedded in the required full WI spec were not used as evidence.

Artifact: `docs/plans/WI-956/plan.md`, read using `git show` at the Reviewed commit. This is a direct text review, not a description proxy. Coverage input: the invocation's seven-clause coverage report.

Rubric: `docs/rubrics/plan-decomposition.md` at d838f1f850a2400d8f136446ac45278ac42121a8, matching the supplied rubric. Intent sources: the full `docs/work/active/wi-956/WI-956-tree-bound-bar-attestation.md`; its specref, `docs/plans/2026-10-11-review-churn/README.md#13-review-only-a-green-tip-review-test-cases-in-stages`, especially precondition 2; SN-004 and SN-008 in `docs/requirements/stakeholder-needs.toml`; SR-156 in `docs/requirements/system-requirements.toml`, all at the Reviewed revision. Existing seams were checked against `docs/requirements/interfaces.toml` at that revision.

Rubric adequacy: independently adequate for this plan judgment. SN-004's enforced mechanical bar, SN-008's honest passing record, and SR-156's fail-closed composed-tree landing yield obligations for the common grammar, verified tree/parent/bar, producer, and preservation of the landing-only peel. DevStg-Tests and B2 require substantive coverage of those obligations, rather than accepting clause citations alone; DevStg-Reqs requires executable steps, and G4/B4 require buildable order. No additional failure-mode anchor is needed for the finding below.

Anchors judged: DevStg-Reqs, DevStg-Tests, DevStg-Impl, G4, B1, B2, B3, B4. The seven clauses have substantive planned deliverables; the excluded TC arms are outside the changed attestation seam. Repeated D1/D3/D4/D7 citations describe registry, verifier, producer, CLI, and landing responsibilities rather than duplicate implementations. The existing IF rows are amended in place. `DELTA: within` is supported: the plan carries the new bar domain, review-command input and CLI boundary within its named modules and interfaces. These strengths do not resolve the ordering defect below.

Transfer caveat: the debate/selection evidence comes from QA, math, and code with objective verifiers; plan-artifact quality and two-planner reconciliation remain unbenchmarked. This rubric is a best-supported extrapolation, not a proven instrument.

- [MAJOR] G4/B4 -> P3's tests include `test_the_refresh_and_attest_commit_through_one_producer`, which explicitly drives both refresh and attest. P3 has only P2 as predecessor; the callable and CLI for attest are first delivered by P5, which itself depends on P3 and P4. Consequently P3 cannot complete its stated test deliverable in the declared build order: its test consumes an artifact two steps later. Adding the missing edge would create a cycle and force a build round to reorganize the plan. -> Move the cross-route producer test and its evidence ownership to P5, where both callers exist; keep P3's independently runnable checks on refresh and the producer, and update the row/detail split consistently. -> @planner

VERDICT: CHANGES-REQUESTED findings=1
