Reviewed: 678b0b21156f53578f5943e49b94ced6d428bf2a

## 2026-10-18 — WI-915 independent plan critique, round 1

Reviewer: fresh non-author Codex critic session, invoked for this coordinator review; this session did not produce the plan. No provider session id was supplied. Recording route: the invocation's assigned scratch verdict path only; no filing command, commit, or checkout changes.

Artifact inspected directly with git show: docs/plans/WI-915/plan.md at the reviewed commit. Read the WI-915 spec in full and its specref, docs/plans/2026-10-11-review-churn/README.md section 10, at that commit. Used the supplied coverage report (12 rows, D1-D14 covered). No implementer session notes, docs/status.md, docs/log.md, or sibling plan critiques were read.

Rubric: docs/rubrics/plan-decomposition.md at the reviewed commit, including the WI-913 single-plan extension. Intent sources: the WI specification and its Q1-Q7 rulings; the specref's shared-loader step; docs/requirements/system-requirements.toml SR-007 and SR-166; their parents SN-003 and SN-001/SN-007 in docs/requirements/stakeholder-needs.toml. Interface context: IF-022, IF-049 and IF-068. TC-007, TC-008, TC-176 and TC-331 were checked as evidence references, not substituted for the SN/SR intent.

Rubric derivation check: adequate for this scoped plan. DevStg-Tests and B2 require actual delivery of declaration-driven reading and refusal of malformed profiles (SR-007), and preservation of shipped-package completeness (SR-166), through the WI's obligations and existing checks. DevStg-Reqs, DevStg-Impl, G4 and B1/B3/B4 independently constrain implementability, duplication, interfaces and ordering. This judgment is not derived from a permissive TC. No additional numbered anchor is needed.

Anchors judged: DevStg-Reqs, DevStg-Tests, DevStg-Impl, G4, B1, B2, B3 and B4. D1-D14 have substantive planned deliverables/checks. The repeated D1-D5 citations have a declared split across disjoint reader families and aggregate verification; repeated D9/D10 checks bind different tips. No duplicate seam or padding was found. DELTA: none is supported: Q1/Q2 change treatment of existing file inputs within existing outcome domains, introduce no persisted state, and route existing readers into the declared shared kernel. The plan carries those behavior changes in its mapping and characterization cells. The defect below concerns its permitted commit sequence.

Transfer caveat: the protocol's supporting debate/selection evidence comes from QA, math and code with objective verifiers. It has not been benchmarked on plan artifacts; reconciliation for plan quality remains an open research gap. This rubric is an extrapolation, not a proven instrument.

- [MAJOR] G4/B4 -> docs/plans/WI-915/plan.md:145 permits P8 to follow the P2-P7 refactor commit, although P8 explicitly says the exact-size ratchet fails before re-stamping. The refactor changes four baselined modules, so that allowed sequence cannot pass its commit bar. Supporting inspection of tests/test_module_size_ratchet.py::test_module_sizes_exactly_match_the_committed_baseline confirms that shrinkage also fails and requires a re-stamp in the same commit. Following the plan's permitted sequence therefore costs a failed build/commit attempt before P8 can be reached as a later commit. -> Require P8's measurements, necessary baseline edits and reasons to be completed and included in the P2-P7 refactor commit before attempting its commit bar; retain P8's dependency on the completed edits, but remove the option of committing those edits first. P9 may remain optional in that commit. -> @planner

VERDICT: CHANGES-REQUESTED findings=1
