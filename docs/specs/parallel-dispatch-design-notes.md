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

## Evidence that changed the earlier proposal

A read-only replay of committed WI registries found a dependency-ready frontier
of 12 WIs on 2026-07-12 (`aca0b0a0`). The repo therefore has demonstrated DAG
width; manual `next-wi` selection and broad collision assumptions were the
larger constraints. Shared Workstream, Campaign, or SpecRef values are not used
as automatic mutexes in the canonical plan.

