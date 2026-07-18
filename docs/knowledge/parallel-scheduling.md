# Traincar scheduling — DAG scheduling and clustering research

This pack preserves the prior art behind **traincar packing** (the
parallel-dispatch plan, `docs/specs/parallel-wi-dispatch.md` §7). The normative
rule stays in the plan; this note records the sources, the analogs, and — most
importantly — why their guarantees do **not** transfer to this system.

## The problem

Packing dependency-ready work items into "traincars" (one branch/lane carrying an
ordered run of WIs) and dispatching them across a bounded worker pool is
**resource-constrained DAG scheduling with task clustering**: list scheduling +
DAG clustering + bin packing.

## Findings retained

**No approximation bound is claimed for this system.** The classical results below
assume identical machines, known non-preemptive durations, and a fixed partial
order — none of which hold for heterogeneous LLM workers with retries, review
gates, integration conflicts, and uncertain cost estimates. They are design
*inspiration*, not guarantees.

- **List scheduling** — Graham, "Bounds for Certain Multiprocessing Anomalies,"
  *Bell System Technical Journal* 45 (1966). Greedy dispatch of ready tasks to
  free workers in priority order is within `(2 − 1/m)` of optimal makespan for `m`
  identical machines. Takeaway: a simple greedy dispatcher is a sound default — no
  optimal scheduler is needed (the shape of the plan's §4 loop).
- **HEFT** — Topcuoglu, Hariri & Wu, "Performance-Effective and Low-Complexity
  Task Scheduling for Heterogeneous Computing," *IEEE TPDS* 13(3):260–274 (2002).
  Prioritize by *upward rank* — a **cost-weighted** critical path — then assign to
  the earliest-finishing worker. Takeaway: the plan's unweighted "remaining
  hard-path length" is criticality-*inspired*, not HEFT's weighted rank; a weighted
  version (using `EstTokens` / measured API-seconds) is the HEFT-shaped upgrade.
- **DAG clustering / coalescing** — Sarkar, *Partitioning and Scheduling Parallel
  Programs for Execution on Multiprocessors*, MIT Press (1989) (edge-zeroing); and
  DSC — Yang & Gerasoulis, "DSC: Scheduling Parallel Tasks on an Unbounded Number
  of Processors," *IEEE TPDS* (1994). The batch-vs-parallel trade-off is
  computation-vs-communication. Takeaway (the plan's normative rule): the
  "communication cost" here is per-traincar integration + review overhead, so
  batch WIs when the overhead saved exceeds the parallelism and failure-isolation
  given up — and never so as to create a traincar cycle (respect WI precedence).
- **LPT / bin packing** — Graham, "Bounds on Multiprocessing Timing Anomalies,"
  *SIAM J. Applied Mathematics* (1969). Longest-processing-time-first is a `4/3`
  approximation for makespan — and it needs a per-job size estimate, which is why
  `EstTokens` exists. The bound is classical-model only; treat estimates as
  advisory.

## Applied analogs (crib, don't reinvent)

- `make -j` / Ninja — job-limited parallel dispatch from a dependency graph.
- Bazel / Nx / Turborepo — build-target DAG + affected-set + result caching.
- Merge queues — GitHub merge queue, Bors, and Zuul's speculative dependent
  pipelines — the integration-ordering half (the plan's §13 speculative rung).
- Airflow **pools** + `priority_weight`, and Temporal **durable execution** — the
  resource-cap and crash-recovery semantics (the plan's §11).

## Application here

- Calibrate `EstTokens` from telemetry already logged (`tokens`, `cost-usd`,
  `turns`, `api-secs`); prefer **wall / API seconds** over raw tokens as the cost —
  tokens miss review and integration latency.
- Keep the scheduler robust to a wrong estimate; do not build one you must trust.
- Measure before tuning: only real integration/review-overhead evidence justifies
  more aggressive clustering.

## Failed or bounded approaches

- Importing a classical approximation bound as if it held for LLM workers with
  review/rework/conflict loops — it does not; treat the theory as inspiration.
- Sizing traincars by raw token estimate alone — it misses review and integration
  latency, the very overhead clustering trades against.
