# Resolved design notes — parallel WI execution

**Status: decision history, non-normative.** The canonical implementation plan
is [`parallel-wi-dispatch.md`](parallel-wi-dispatch.md). This note preserves the
questions that changed that plan without restating its contract.

## Questions resolved

- **Can scheduling be derived?** Yes. The ready frontier comes from queued WIs,
  hard predecessors, gate policy, and dispatcher reservations. Readiness is not
  stored or copied into prose.
- **Does the DAG prevent interdependent WIs from running together?** Yes for
  hard edges, transitively. Soft edges are advisory and cannot carry a safety
  dependency.
- **Is `status.md` required?** Not as a scheduling/resume authority. The root
  integrator may generate it after integration as a human reference; workers do
  not maintain lane-local status files.
- **Is `docs/next-wi` useful?** No. It is removed. Deliberate priority belongs in
  WI metadata, and normal selection is derived.
- **Are predefined parallel tracks required?** No. Workstream/Campaign remain
  categories; the dispatcher allocates temporary lanes and change trains.
- **Should possible path overlap suppress parallel work?** Not generally. The
  initial policy is optimistic, limited to two off-spine workers, with hard
  serialization for dependencies, protected root/spine state, and explicit
  exclusive resources. The integrator reconciles overlap and reruns the
  composed bar.
- **Can a dependent sequence stay on one branch?** Yes. A single safe successor
  may extend the train until a fork, join, gate/spine/review boundary, blocker,
  or safety cap.
- **Can ignored runtime state survive a crash?** `out/dispatch/` survives an
  ordinary reboot but is only a cache/journal. Reservation commits, train refs,
  worktrees, exact-head reviews, and integration trailers let startup rebuild
  ownership even when the entire directory is missing.
- **Should `agent-resume` parallelize automatically?** Yes. New scaffolds default
  to two workers; `--jobs 1` is the explicit serial mode.
- **Do migrated repos flip to parallel too?** Yes — deliberately, as an exercise
  of the framework, not just fresh scaffolds; `--jobs 1` is the per-run
  conservative escape.
- **Do we still need `docs/run-phase`?** No. The coordinator PLAN/BUILD phase
  becomes per-lane runtime state; the file is deleted and model routing keys off
  a lane's current activity.
- **What happens to the delivery `Phase` (v2/v3)?** Derived from closed gate
  anchors; the integrator prefers the largest phase bump among composed trains;
  the `Phase` column survives only for a forward-deferred SR (intent, not a
  derivable fact). Campaign is only a WI attribute, never a scheduling unit, so
  campaign-tagged WIs parallelize wherever off-spine — no isolation machinery.
- **When does an integration edit force re-review?** Only a *material* edit — a
  hunk the integrator authors that is not byte-identical to one side of the merge.
  Clean applies and verbatim one-side resolutions do not; generated artifacts are
  exempt. The rule is mechanical so it cannot drift between sessions.
- **Are `Exclusive` keys / hard edges runtime rules?** No — they are *planning-time
  declarations* set at WI draft. A runtime collision is under-allocation evidence:
  the run records it and reconciles, never pausing; a human corrects future WI
  drafts (and can declare a key on a not-yet-run WI sharing the resource). Never
  inferred or enforced by the dispatcher.
- **The DAG is checked before commit — what more builds confidence?** The
  validator confirms declared edges are well-formed but cannot detect a
  *forgotten* edge. Confidence = a one-time audit promoting real `~` soft edges to
  hard, plus collision telemetry over time.
- **How are stale `llm/` branches handled?** An advisory rolling check (like the
  push/privacy checks) reports train/integrate branches older than ~2 days,
  splitting merged from unintegrated, and never deletes — human-driven for now.
- **How is a launch sequenced?** Drain every open `llm/*` branch to an integrated
  baseline (surface + exit if one cannot merge), discard the stale traincar
  schedule, clear G1 then G2 spine work serially at whole-project scope (exit for
  ratification under attended/human authority; self-ratify under autonomous), then
  plan and dispatch parallel build-out.
- **How does a traincar execute?** One Build pass (plan/optimize as needed, one
  commit per WI) → one Review over the traincar's combined diff. Safe because
  clustering only groups review-compatible WIs (off-spine, bounded, non-critique,
  no boundary crossing); strong/spine/critique work runs as its own single-WI
  traincar.
- **How are WIs packed into traincars and dispatched?** The open design piece —
  resource-constrained DAG scheduling with clustering. Design path: (1) add an
  `EstTokens` estimate to WIs, calibrated from session telemetry; (2) design the
  batch-vs-parallel clustering heuristic; (3) define traincar-DAG ingestion (a
  traincar whose deps are all integrated feeds a free worker thread as one opens
  up). Research anchors: list scheduling (Graham 1966 — greedy is within 2× of
  optimal, so no optimal scheduler is needed), HEFT upward-rank (Topcuoglu et al.
  2002), DAG clustering / DSC (Sarkar 1989; Yang & Gerasoulis 1994), LPT
  bin-packing; applied analogs `make -j`/Ninja, Bazel/Nx/Turborepo, merge queues
  (GitHub/Bors/Zuul speculative pipelines), Airflow pools + Temporal durable
  execution.

## Evidence that changed the earlier proposal

A read-only replay of committed WI registries found a dependency-ready frontier
of 12 WIs on 2026-07-12 (`aca0b0a0`). The repo therefore has demonstrated DAG
width; manual `next-wi` selection and broad collision assumptions were the
larger constraints. Shared Workstream, Campaign, or SpecRef values are not used
as automatic mutexes in the canonical plan.

