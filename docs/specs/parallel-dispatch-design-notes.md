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
- **Do migrated repos flip to parallel too?** Yes, but only **after the soft-edge
  audit passes** — until then `--jobs 1`, then a recorded, deliberate promotion;
  fresh scaffolds default to two.
- **Do we still need `docs/run-phase`?** No — the coordinator file is deleted. A
  build-out lane routes from its activity (build → review), and its train branch
  is named `{phase}-{gate}` so the phase is crash-recoverable without
  `out/dispatch/`. The richer routing phases (PLAN/DESIGN-CHECK/CRITIQUE/G1-G2)
  belong to the serial upfront gate pass, not a parallel lane.
- **What happens to the delivery `Phase` (v2/v3)?** **Left unchanged this
  campaign.** It feeds `derive_gate.py` and shifts only at gates (serial, upfront),
  so there is nothing to derive or reconcile at merge — the column, its meaning,
  and the gate model stay as they are. (The earlier "derive it / largest bump at
  merge" idea was dropped as out-of-scope and underdefined.)
- **When does an integration edit force re-review?** **Any genuine conflict
  resolution** — including choosing one side (`ours`/`theirs`) verbatim, because a
  conflict means a reviewed change was dropped and byte-identity proves only
  provenance, not that the merge satisfies both WIs. Clean conflict-free applies
  and regenerated artifacts do not; the renewed review is focused on the composed
  conflict.
- **Are `Exclusive` keys / hard edges runtime rules?** Yes — declared at WI draft
  and **enforced** by the scheduler (that is their purpose). What the dispatcher
  never does is *invent* one: an undeclared collision is under-allocation evidence,
  recorded and reconciled without pausing, and corrected in future WI drafts.
- **The DAG is checked before commit — what more builds confidence?** The
  validator confirms declared edges are well-formed but cannot detect a
  *forgotten* edge. Confidence = a one-time audit promoting real `~` soft edges to
  hard, plus collision telemetry over time.
- **How are stale `llm/` branches handled?** An advisory rolling check (like the
  push/privacy checks) reports train/integrate branches older than ~2 days,
  splitting merged from unintegrated, and never deletes — human-driven for now.
- **How is a launch sequenced?** **Reconcile** dispatcher-owned trains
  (`llm/train|integrate/*`) to a clean baseline — integrate recoverable, resume
  incomplete, quarantine only the stuck (never halting disjoint work) — discard the
  stale schedule, clear G1/G2 spine serially (exit for ratification under
  `attended`/`single-ratify`; self-close under `autonomous`), then dispatch
  build-out.
- **How does a traincar execute?** One Build pass (plan/optimize as needed, one
  commit per WI) → one Review over the combined diff. Successors depend on an
  **accepted-on-train** (locally green, not yet reviewed) ancestor, and **no WI is
  `done` until the whole train integrates**. Clustering only groups
  review-compatible WIs; strong/spine/critique work runs as its own single-WI
  traincar.
- **How are WIs packed into traincars and dispatched?** Resource-constrained DAG
  scheduling with clustering, **in scope from the start** (not deferred). Design
  path: `EstTokens` estimate → clustering heuristic → traincar-DAG ingestion. The
  research anchors and their honest caveats (heuristics, **not** guarantees for
  this setting — no approximation bound is claimed) live in the plan §7.

## Evidence that changed the earlier proposal

A read-only replay of committed WI registries found a dependency-ready frontier
of 12 WIs on 2026-07-12 (`aca0b0a0`). The repo therefore has demonstrated DAG
width; manual `next-wi` selection and broad collision assumptions were the
larger constraints. Shared Workstream, Campaign, or SpecRef values are not used
as automatic mutexes in the canonical plan.

