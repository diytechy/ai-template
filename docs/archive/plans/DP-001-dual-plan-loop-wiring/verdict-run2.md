> **ARCHIVE** — design history as of 2026-08-13; not current guidance.

```
PER-ANCHOR:
- [G1] B: B's P1 is a pure, standalone-unit-tested state machine and P2/P3/P4/P5 each name a fixture-based done-condition in the row itself; A's P3/P4 split is sound but leans on the Notes to state its checkable conditions rather than the rows.
- [G2] even: coverage report shows both cover C1–C7 (7/7) with no declared exclusions.
- [G3] even: A carries zero multi-cover; B's only overlap is C7 (P1 owns the round-budget cap, P6 owns per-session limit/telemetry inheritance) with a declared, real seam — not duplicated scope.
- [G4] B: A's P1→P2→P3→P4→P5→P6 chain over-sequences build order (P3 coverage-adapter depends on P2 session-runner, P4 on P3) though those are buildable against fixtures; B roots P1/P2/P3/P5 edge-free and defends P4→P1 and the P6 fan-in as real consumption.
- [B1] even: both cite the nearest IF with direction/provider rationale (A-P3 vs IF-046, A-P5 vs IF-055; B-P1 vs IF-053, B-P4 vs IF-057/IF-041, B-P5 vs IF-054/IF-023); neither near-duplicates a live seam.
- [B2] even: no decorative citations — A maps rows 1:1 to clauses; B's C5-in-P1 and the C7 split are substantive and declared.
- [B3] even: both are 6 rows with distinct deliverables; B explicitly refused a 7th WI when closing the P3 critique ("the fix is a contract completion, not new scope").
- [B4] B: A's P3→P2, P4→P3 and the redundant P6→P4 (already implied via P5→P4) read as sequencing habit; B's P4→P1 (emits P1's typed constants) and P6 integration fan-in are artifact-level, with the edge-free P2/P3/P5 defended.
VERDICT: SELECT B ports=0
RESIDUAL GAPS: none
```
