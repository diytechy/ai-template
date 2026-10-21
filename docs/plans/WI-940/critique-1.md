Reviewed: 51e0885c45548f56a36d0071644dc852da093d13

### CRITIC — WI-940 implementation plan — Round 1 — 2026-10-21

Reviewer/session: this fresh, non-author Codex critic session, invoked for the assigned pc-940 round-1 record. No provider session id was supplied.

Artifact: `docs/plans/WI-940/plan.md`, read with `git show` at the reviewed commit. The full WI spec and its specref were read at that revision. No implementer session notes, status/log records, or adjacent plan critiques were used.

Rubric: `docs/rubrics/plan-decomposition.md`, as held at the reviewed commit; its last modifying revision is `247dc36c46a6536f3586cc241b231151b5692a93`. Intent sources: `docs/requirements/stakeholder-needs.toml` SN-007 and SN-008; `docs/work/active/wi-940/WI-940-cpu-time-smoke-budget.md` (including all Done-when clauses); `docs/decisions/coordinator-2026-10-17.toml` D-004/D-005/D-007; the quoted re-scope in `coordinator-2026-10-20.toml` D-014 and caller extension in `coordinator-2026-10-21.toml` D-001.

Rubric derivation check: adequate for this plan review. DevStg-Tests and B2 require actual coverage of the declared bar, honest CPU accounting, refusal behavior and audit split; DevStg-Reqs, DevStg-Impl, G4 and B1/B3/B4 judge whether those obligations form solvable, distinct, buildable steps. This independently connects the rubric to SN-007's tested changes and SN-008's trustworthy verdicts; no additional numbered anchor is needed.

Transfer caveat: the protocol's debate/selection evidence comes from QA, math and code with objective verifiers. It has not been benchmarked on plan artifacts, and two-planner reconciliation for plan quality remains an open research gap. This rubric is an extrapolation, not a proven instrument.

Anchors judged: DevStg-Reqs, DevStg-Tests, DevStg-Impl, G4, B1, B2, B3, B4. The supplied report covers D1–D15 mechanically. The repeated citations generally describe real seams: shared implementation versus end-to-end tests, meter behavior versus caller commands, measured values versus documentation, and initial move versus landing. The plan supplies concrete outputs and checks, and orders the audit before the bars stop enforcing seconds. Its DELTA: within answer correctly identifies the new state, domain values, accounting/count inputs and module boundary; P1–P8 carry them. The finding below concerns a written intent obligation that the coverage arithmetic does not establish.

- [MAJOR] DevStg-Tests -> P2's paragraph beginning “D-007 Q3 (a) says” and open point 2 explicitly leave the root conftest's prototypes in place and do not make it import the shared module. The specref's owner ruling D-007 Q3 (a) expressly requires the session kill, root conftest and budget step all to import the shared job module. Deliverable 6's narrower description of which code moves does not revoke that caller requirement. Calling the import unnecessary for isolation and flagging it for the coordinator leaves an owner-directed part of the boundary change unimplemented, requiring a design/review round before the plan can be built as authorized. -> Amend P2 to consume the shared module for the conftest's overlapping job operations while preserving its cap and priority behavior, with a check that it uses that shared implementation; alternatively obtain and cite a ruling that removes this caller obligation before treating the plan as complete. -> @planner

VERDICT: CHANGES-REQUESTED findings=1

