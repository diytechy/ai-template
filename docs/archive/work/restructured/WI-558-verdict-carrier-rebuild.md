+++
id = "WI-558"
title = "The verdict carrier rebuilt: the gate computes over logged rounds, the tree-bound trailer, the generated rollup (OI-76)"
specref = ""
workstream = "process"
sr_refs = []
needs = []
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Restructured into WI-579.

## Context

`OI-76` RULED 2026-08-31 (record `docs/log.d/2026-08-31-owner-ruling-oi76.md`;
plan of record `docs/plans/2026-08-31-verdict-record-and-queue-blockers.md`
section 1): the hand-authored `docs/reviews/WI-<n>-REVIEW-A.md` is the fossil
of a retired convention — the gate was never re-pointed when the
concurrency-train rewrite moved reviewer output to per-train sha-bound round
files. Four of the seven 2026-08-31 unattended runs stopped on its absence;
every mechanized lane needs a supervisor to hand-compile it. This row is the
queue's unblocker: the plan's acceptance measurement (three consecutive rows
merged by one launch with zero supervisor commits) reads zero today.

## Done-when

1. `integrate._verdict_gate` computes its predicate over the branch train's
   round files, restricted to rounds a LOGGED reviewer session produced (the
   telemetry commit is the anchor) — an implementer-authored file in the
   review path is not a round (the plan's finding K closed).
2. The round's own commit carries the machine half as a trailer —
   `Review-Verdict: APPROVE|CHANGES-REQUESTED rounds=N tree=<sha>` — the
   existing `Bar-Green` pattern. GOVERNING = TREE IDENTITY as ruled: a
   verdict counts only if it names the branch's current non-record tree; no
   ordering rule; the gate's freshness comparison retires.
3. The per-WI rollup becomes a GENERATED artifact: a regenerator compiles it
   from the round files, `--check` keeps it fresh, it is declared in
   `docs/stack.ini [generated]`, and the gate never reads it. The supervisor
   prompt's hand-compile instruction retires in the same change.
4. Migration window per the plan's section 6: during the window the gate
   accepts EITHER the round-file evidence or a legacy hand-authored rollup,
   warning on the legacy path; `RESYNC_PACK.md` carries the entry. The
   trailer is additive and costs an adopter nothing until their loop writes
   one.
5. Tests drive the gate's new predicate, the trailer identity rule, the
   logged-session restriction, and the migration warn on a scaffold; the
   full suite stays green.
