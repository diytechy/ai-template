Reviewed: 9c472a1dbc6538b9e9b5e2da9357ab6c75457675

## 2026-10-23 — WI-851 independent plan critique, round 2

Fresh non-author session: the independently invoked Codex critic for coordinator leg 16, plancrit2. This session did not produce the plan. No provider session id was supplied. This is the final, convergence critique; the verdict is recorded only at the invocation's assigned scratch path, without a commit or checkout changes.

Artifact: `docs/plans/WI-851/plan.md` at the Reviewed commit, read directly with `git show`. Inputs: the full claim spec `docs/work/active/wi-851/WI-851-held-rung-state-guard.md`, its specref `docs/plans/2026-10-07-wi841-retro/PROPOSAL.md` (especially sections 7.1, 7.1b and 8.4), and the supplied coverage report. Prior critique files, review files, implementation session notes, status/log files and the lane decisions record were not read. Historical dispositions embedded in the required artifacts were not used as evidence of correctness.

Rubric: `docs/rubrics/plan-decomposition.md` at the Reviewed commit; its last-changing revision there is `247dc36c46a6536f3586cc241b231151b5692a93`. Intent sources: `docs/requirements/stakeholder-needs.toml` SN-029 and `docs/requirements/system-requirements.toml` SR-208 and SR-178, all at the Reviewed commit, scoped by the claim spec and specref. The relevant existing IF-196, IF-287, IF-296, IF-129 and IF-220 contracts were inspected independently.

Rubric derivation check: adequate for this plan review. SN-029 reserves held tiers for human judgment and requires evidence-backed delegated review; SR-208 supplies the held-status control, while SR-178 supplies the approved/traced comparison and amendment-without-status-movement intent. DevStg-Tests and B2 require substantive coverage of the scoped state predicate, identity binding, refusal paths and both landing routes, rather than accepting permissive TC citations. DevStg-Reqs, DevStg-Impl, G4 and B1/B3/B4 test whether those obligations form buildable, distinct steps with honest interfaces and dependencies. No missing numbered anchor is needed for the supplied intent. Transfer caveat: the protocol's supporting evidence comes from objectively verified QA, math and code; its application to plan quality is an extrapolation, not a proven instrument.

Anchors judged:

- DevStg-Reqs: pass. The rows name deliverables and checkable outcomes. P8 is substantial but deliberately combines the new authority rule with its retirements; the earlier rows supply its tests, readers and identity producer.
- DevStg-Tests: pass. The 51 reported clauses have substantive delivery paths. The plan includes the eight-registry claim predicate, five-condition exception, per-parent walk, committed trunk dial, malformed-input behavior, act-before-launch refusal, narrowed writers, migration guidance and regression cases. The deferred-spec read is an explicit verification step, with drift routed to the coordinator.
- DevStg-Impl: pass. Repeated citations distinguish extraction from changed behavior, tests from implementation, identity producer from consumers, and initial authoring from the combined sitting. D43 separates entry authoring from landing-time anchoring.
- G4: minor failure described below. The implementation's substantive dependencies are present, but two edges are sequencing rather than artifact dependencies.
- B1: pass. The plan amends and relocates existing seams rather than proposing competing IF rows; IF-129 owns the comparison/digest basis and IF-287 the binding reader.
- B2: pass. Coverage citations are supported by named behavior, tests or an explicit verification deliverable; no hollow Done-when coverage found.
- B3: pass. The moves, tests, identity pipeline, atomic rule replacement, migration entry and checkpoint have distinct reviewable deliverables. No duplicated implementation step found.
- B4: minor failure described below.

DELTA: within is supported. P2/P3 carry the reader and module boundaries, including scaffold delivery; P5/P6 carry the identity state and grammar through production and outcome rewrites; P7 carries the new act input/refusal; P8 carries the landing input, rider and narrowed marker arm. P10 carries adoption consequences. No reachable fail-open, data-loss or Done-when gap was established.

- [MINOR] G4/B4 -> Plan table, P3 predecessor P2 and P11 predecessor P9: the held-status extraction in P3 does not consume the claimed-branch reader moved by P2 (that reader is consumed by P8), and P11's regression/fixture audit does not consume an artifact from P9's read-only deferred-spec report. These are ordering preferences represented as artifact dependencies, contrary to the DAG anchors. -> Give P3 predecessor P1; remove P9 from P11's predecessors, retaining P10 (which transitively depends on P8). Keep the preferred execution order in table order or a sequencing note. -> @planner

VERDICT: CHANGES-REQUESTED findings=1
