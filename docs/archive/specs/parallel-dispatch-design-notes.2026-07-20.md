# Resolved design notes — parallel WI execution

> **ARCHIVED 2026-07-20 — WI-251 spec-lifecycle sweep.** Spec-of-record for **no registry citer (working notes for the effort it accompanies)** (all `done`; deliverables in `docs/requirements/work-items.csv`, session records in `docs/log.md`). Absorb-verified before archiving: every durable decision has a live spine/architecture/process home (dispositions in the log, 2026-07-20 entry).

**Status: decision history, non-normative.** A short log of the questions that
shaped the canonical plan, [`parallel-wi-dispatch.md`](parallel-wi-dispatch.2026-07-20.md),
each pointing at the section that decides it. It does **not** restate the
contract; where a line here and the plan ever disagree, the plan wins.

## Questions resolved

| Question | Resolution | Plan |
|---|---|---|
| Can scheduling be derived? | Yes — the frontier is queued WIs whose hard predecessors are integrated, never stored in prose. | §1, §3.2 |
| Does the DAG stop interdependent WIs running together? | Yes, transitively, on hard edges; soft edges are advisory only. | §3.2 |
| Is `status.md` a scheduling authority? | No — integrator-generated reference only; workers never read or write lane status. | §10 |
| `docs/next-wi`? | Retired; deliberate ordering lives in a `Priority` column. | §1, §10 |
| Do tracks or groupings schedule work? | No — both are WI attributes only, so "parallel groupings" needs no isolation machinery. | §1.3, §10 |
| Optimistic or conservative overlap? | Optimistic off-spine, bounded to two workers; spine / `Exclusive` / dependency work serializes. | §5 |
| `docs/run-phase`? | Coordinator file retired; a lane routes from its activity + a `{phase}-{gate}` branch name (crash-recoverable). | §10 |
| Delivery `Phase` (v2/v3)? | Left unchanged — feeds `derive_gate`, shifts only at gates; the "largest bump at merge" idea was dropped. | §10 |
| `Exclusive` keys / hard edges? | Declared at draft **and enforced**; the dispatcher never invents them, and an undeclared collision is recorded (not enforced), reconciled without pausing. | §1.11, §5.2 |
| When does integration re-review? | Any genuine conflict resolution (incl. `ours`/`theirs` verbatim); clean applies + regenerated artifacts exempt; the re-review is focused. | §5.2 |
| Traincar execution? | One Build → one Review; successors depend on an *accepted-on-train* (not approved) ancestor; no WI is `done` until the train integrates. | §7 |
| Series vs independent batching? | Both are just traincar packing — a dependency chain or a batch of small independent WIs on one branch; failure isolation is the cost. | §7 |
| Migrated repos → parallel? | Yes, but only after the soft-edge audit passes; until then `--jobs 1`, then a recorded promotion. | §4, §14 |
| Stale `llm/` branches? | Advisory age check (merged vs unintegrated), never auto-deletes. | §9 |
| Launch sequence? | Reconcile owned trains → clear G1/G2 spine serially → dispatch build-out; a stuck train never halts disjoint work. | §4 |
| Clustering / `EstTokens`? | In scope from the start (not deferred); research + honest caveats in the `parallel-scheduling` knowledge pack. | §7 |
| DAG completeness before parallel? | The validator proves well-formedness, not a *forgotten* edge; a one-time soft-edge audit is the confidence step. | §14 |
| Crash recovery of runtime state? | `out/dispatch/` is a rebuildable cache; ownership reconstructs from git refs + trailers even if it is deleted. | §11 |

## Evidence

A read-only replay found a **12-WI** dependency-ready frontier on 2026-07-12
(`aca0b0a0`) — the repo has real DAG width, so manual selection and broad
collision assumptions were the true constraints, not a lack of parallelism.

A subsequent independent (Codex) review pass caught internal contradictions
introduced by fast fold-ins — Exclusive/enforcement wording, the material-edit
bright line, the train-review terminology, and the gate-policy vocabulary — all
reconciled into the plan; the redesign is filed as **WI-176** (WI-162 was the
documentation-only exploration it supersedes).
