# Rubric — Plan decomposition (WI-190)

**Adjudicates:** the dual-plan cross-critique and arbiter rounds
(process-options master, "Dual-plan decomposition") — whether a proposed WI
decomposition is worth building, judged as **artifacts against the goal brief
and the coverage report**, never as a conversation.
**Used by:** the plan-critic and arbiter hats
(`project-trajectory/prompts/dual-plan-*.template.md`). `plan_coverage.py`
already computes clause coverage and resolves refs; this rubric judges what
code cannot — are the WIs solvable, is the coverage honest, is the
decomposition non-redundant?

Every verdict **cites anchor ids**. The critic's verdict line is
`VERDICT: APPROVE|CHANGES-REQUESTED findings=N`; the arbiter's is
`VERDICT: SELECT <plan> ports=N`, each port a cited delta
("port B-3 — closes C4, anchored G2").

**Transfer caveat (state wherever this rubric is applied):** the
debate/selection evidence behind this protocol comes from QA, math, and code
with objective verifiers — nothing benchmarks it on *plan artifacts*, and
two-planner reconciliation evaluated for plan quality is an open research gap.
This rubric is the best-supported extrapolation, not a proven instrument
([co-planning knowledge pack](../knowledge/co-planning.md), retrieved
2026-07-16).

## Anchors

**G1 — Solvable unit.** Each proposed WI is completable by one build session at
its tier: a first-time implementer could name the deliverable and a checkable
done-condition from the row alone. *Bad:* "improve the dispatch layer" (no
deliverable); a row whose scope needs three sessions and two design rulings.

**G2 — Complete coverage.** Every goal clause is covered by some WI **or its
exclusion is declared** in the plan's notes as a non-goal with a reason —
never silence. The coverage report computes the gap; the critic judges whether
a declared exclusion is honest.

**G3 — Non-redundant decomposition.** No two WIs cover the same clause without
a declared split reason; scope boundaries are crisp enough that two
implementers would not collide. Multi-covered clauses in the coverage report
are the tripwire; the judgment is whether the overlap is a real seam or a
duplicated scope.

**G4 — Coherent DAG.** Every predecessor edge reflects a real artifact-level
dependency (an edge the planner could defend by naming what the successor
consumes), and no real dependency is missing. `plan_coverage.py` catches
unknown ids and cycles; the phantom edge and the missing edge are judgment
calls.

**B1 — Seam duplication** *(imports
[spec-interface-hygiene](spec-interface-hygiene.md) B1).* A row's `Proposed:`
seam near-duplicates an existing `IF-###` instead of consuming or amending it,
or its rationale does not truly name the nearest existing seam. Judge as a
first-time reader of `interfaces.toml`, not as the plan's author.

**B2 — Coverage laundering.** A row cites clauses its title and deliverable do
not actually deliver — citation as decoration to win the coverage diff. The
pre-pass counts citations; only a reader catches a hollow one.

**B3 — Padding.** A WI that exists to look thorough: its deliverable restates
another row's done-condition, or a split adds coordination cost without an
independently testable deliverable. **More WIs is not better** — a 4-row plan
does not beat a 3-row plan for count or prose volume.

**B4 — Phantom or missing dependency.** A predecessor edge with no
artifact-level dependency behind it (sequencing habit), or an absent edge
where one WI plainly consumes another's deliverable — either way the DAG lies
about buildable order.
