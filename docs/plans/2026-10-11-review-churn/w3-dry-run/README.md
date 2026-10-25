# Item 12's W3 dry run (2026-10-25, headless leg 21)

The review-churn plan's item 12, "First step: a dry run on W3, before building
anything": an independent model is given only a drafted
`architecture-decomposition` rubric and W3 Autonomy's current shape, and asked
for candidate decompositions. The queue's P6 starts here; its text row is filed
from this record.

- [rubric-draft.md](rubric-draft.md): the drafted rubric (anchors A1 to A8,
  failure patterns B1 to B4), by a fresh Claude Opus planner from item 12's
  "shared core", variant F, F-call 6's four descend tests and the value-domain
  research. Not shipped; the P6 text row ships the corrected version.
- [w3-shape.md](w3-shape.md): W3's shape as facts only (78 files by LLR module
  projection, the import graph, 65 internal and 121 boundary interface rows,
  Flow 4, 126 LLRs), by the same planner. The plan's "60 modules" figure did not
  reproduce: membership is the union of files the component's LLRs name, so 26
  files also sit in other components.
- [dry-run.md](dry-run.md): the dry run, by a fresh Codex Sol (another family)
  given only the two documents above.

## Result

The rubric works by item 12's test: the proposal is argued from the bundle's
evidence. It develops three candidates (keep W3 whole; extract provider
execution; extract the governing protocol vocabulary), compares them on the
decisions each hides, the import edges and interface rows each removes or
narrows, and each cut's cost, including the shared verdict service (IF-175)
several parts would depend on, and it rejects a split along Flow 4's stages
with reasons (shared verdict, acceptance and provenance access across the
stages). It prefers the provider-execution cut as the next to investigate and
says the bundle cannot yet establish an approvable decomposition.

## What the P6 text row takes from it

The dry run names five questions the draft failed to ask, each to be handled
by clarifying anchors A4, A6, A7 and A8 rather than adding failure patterns:

1. the ownership or allocation model for a file several components' rows name;
2. the invariants a cut must preserve (transaction scope, lock order, failure
   and retry ownership, durable effects);
3. the evidence adequate for an audit versus a fresh design, with explicit
   "not supplied" and "not assessable" outcomes;
4. the cost of enforceability and migration (access constraints, boundary
   tests, a migration plan where approved rows or tests would change);
5. what counts as one interface or one case (existing rows, new endpoint
   crossings, shared schema definitions and new semantic surfaces counted
   apart, with an explicit unknown remainder).

It also finds that A8's four descend tests stop requirement descent and give
no cost-based stop for component descent: the row distinguishes the two.
