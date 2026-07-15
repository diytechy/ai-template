# Implementation plan — inherent parallel WI execution

**Status: DETAILED PLAN, pending ratification and implementation-WI filing.**
This plan supersedes the earlier proposed `--track`-lane design written under
WI-162. WI-162 delivered the design exploration; it did **not** deliver a
dispatcher. The implementation slices in §15 receive new WI ids only after this
contract is ratified.

The objective is simple: launching `agent-resume` should automatically execute
every dependency-ready work item that can safely make progress, without a human
curating `docs/next-wi` or predefining parallel tracks. Development and review
fan out; mutation of the integration branch remains serialized and gated.

---

## 1. Decisions fixed by this plan

1. **The WI DAG schedules work.** Readiness is derived from the tracked WI
   registry plus dispatcher reservations; it is never copied into prose.
2. **`agent-resume` is the dispatcher/integrator.** A normal launch uses bounded
   parallelism by default. `--jobs 1` is the explicit serial escape hatch.
3. **Neither tracks nor campaigns schedule work.** `Workstream` and `Campaign`
   are WI *attributes* for reporting/dashboards only — never a scheduling or
   isolation unit. "Parallel campaigns" therefore needs no special machinery: it
   is just parallel WIs that happen to carry different `Campaign` tags. Execution
   lanes and traincars are allocated dynamically.
4. **`docs/next-wi` is retired.** Explicit ordering, where needed, lives in WI
   metadata; otherwise a deterministic scheduler selects the frontier.
5. **Root `status.md` is reference-only.** Only the integrator regenerates it on
   the integration branch after a successful integration. Workers do not read
   or write lane-local status files.
6. **Parallelism is optimistic but bounded.** Ordinary off-spine WIs may run
   together even when their eventual file sets are not known. Hard dependencies,
   protected shared state, and explicit exclusivity still serialize work.
7. **Unary dependency sequences become change trains.** A lane may pull the
   single safe successor onto the same branch until a fork, join, boundary, or
   safety cap ends the train.
8. **Git is the durable recovery substrate.** `out/dispatch/` is a rebuildable
   runtime journal/cache, never the sole record of a reservation or unintegrated
   result.
9. **Integration is serialized and atomic.** A result becomes done only after it
   is composed with the latest integration HEAD, reviewed as required, passes
   the combined bar, and advances the integration ref in one compare-and-swap.
10. **Run-phase is retired; delivery phase is derived.** The coordinator
    `docs/run-phase` file is deleted — phase is per-lane runtime state (§3.3) and
    model routing keys off a lane's current activity. The delivery `Phase`
    (v2/v3 lifecycle) is derived from the workflow: the integrator prefers the
    largest phase bump among the trains it composes, and the registry retains a
    `Phase` tag only for a *forward-deferred* SR (authored now, built in a later
    phase), which cannot be derived. Because a campaign is only a WI attribute
    (§1.3), campaign-tagged WIs parallelize wherever they are off-spine; the only
    serialization is spine work itself (§5.1).
11. **`Exclusive` keys and hard edges are planning-time declarations, not runtime
    gates.** They are set when a WI is drafted, allocating its resources. A
    runtime collision is *evidence the WI setup under-allocated* — the dispatcher
    records it and reconciles normally (§5.2); it never pauses the run, and it
    never infers, adds, or enforces a key/edge itself. Corrections land upstream,
    in how future WIs are drafted.

## 2. Terms and ownership

| Term | Meaning | Owner |
| --- | --- | --- |
| **Workstream / Campaign** | Human grouping and dashboard categorization | WI registry |
| **Hard predecessor** | Correctness edge that blocks readiness | WI registry |
| **Soft predecessor** | Advisory ordering only; never a safety edge | WI registry |
| **Exclusive key** | Exceptional semantic resource that cannot be mutated concurrently | WI registry (declared at WI draft); collisions recorded for retrospective review, never enforced |
| **Frontier** | Queued WIs whose hard predecessors are integrated done | Scheduler, derived |
| **Reservation** | Dispatcher claim preventing another worker from owning the WI | Dispatcher journal + train branch |
| **Lane** | Temporary worker process and linked worktree | Dispatcher |
| **Change train** | One branch carrying an ordered dependency chain of one or more WIs | Lane, dispatcher-authorized |
| **Integration queue** | Reviewed trains waiting to compose into the development branch | Integrator |
| **Integration branch** | The project's main development/iteration branch for this run | Integrator only |

The public concept `track` is retired from automated scheduling. The current
`agent_loop.py --track` implementation is retained temporarily as compatibility
plumbing, then replaced internally by an explicit worker assignment. If a
downstream project wants long-lived human tracks, they remain an optional
dashboard/ownership view and do not influence readiness.

## 3. Sources of truth and state split

### 3.1 Tracked durable disposition

`docs/requirements/work-items.csv` remains the authoritative definition and
integrated disposition of every WI. The implementation extends its optional
schema with:

- `Priority` — integer, default `0`; a deliberate ordering override within the
  same gate class. Higher values run first.
- `Exclusive` — `;`-joined semantic mutex keys for the rare resource that must
  not be touched concurrently. Empty means optimistic execution, not unknown.
- `BlockRef` — required when `Status=blocked`; points to an `OI-N`, spec anchor,
  or named external condition explaining what must change.
- `EstTokens` — *(planned; design step 1)* a draft-time size estimate used by the
  traincar clustering heuristic (§7), calibrated from session-log telemetry and
  kept robust to error.

Tracked `Status` becomes:

- `queued` — authorized work, whether currently waiting, ready, or reserved;
- `deferred` — deliberately outside the active queue;
- `blocked` — cannot proceed for a non-predecessor reason named by `BlockRef`;
- `done` — integrated and verified at the required bar.

Legacy `active` rows remain readable during migration but are not written by
the new dispatcher. Runtime activity does not belong in a shared CSV: multiple
train branches would otherwise carry mutually stale copies of the same registry.

### 3.2 Derived dependency state

For a queued WI:

- `waiting` — at least one hard predecessor is not integrated `done`;
- `ready` — every hard predecessor is integrated `done`, or is an approved
  ancestor on the same dispatcher-authorized train;
- `reserved` — ready and claimed by exactly one live/recoverable train.

Readiness is never stored as a column. Because every immediate hard predecessor
must be satisfied, transitive dependencies are satisfied automatically. A soft
edge cannot prevent concurrent execution; any ordering needed for correctness
must be promoted to a hard edge.

### 3.3 Runtime execution state

The dispatcher maintains these reconstructable states under `out/dispatch/`:

`reserved -> building -> reviewing -> ready-to-integrate -> integrating -> integrated`

with side states `blocked`, `rework`, `waiting`, and `quarantined`. These are
operational facts, not project history. The authoritative `done` transition is
written to the root WI registry only by the integrator.

## 4. Scheduling and default concurrency

`agent-resume` launches the dispatcher by default. The public control is:

```text
agent-resume                 # bounded parallel scheduling; new default = 2
agent-resume --jobs 1        # explicit serial mode
agent-resume --jobs 4        # explicit higher ceiling
agent-resume --jobs auto     # adaptive up to the configured ceiling
```

The Windows/POSIX launchers expose the same value through `AGENT_JOBS`. CPU
count does not set it: model quotas, cost, agent availability, and integration
throughput are the real constraints. A new scaffold defaults to two workers.
During downstream migration a repo **flips to the same two-worker default** — a
deliberate exercise of the framework, not an opt-in — and an adopter that wants a
conservative first run pins `--jobs 1` for it. Running `agent-resume` remains the
permission-bypass consent act; a second parallel-consent file is unnecessary.

### The launch sequence — drain, gate, then build-out

A launch does not jump straight into parallel build-out; it establishes a clean
baseline and clears the gated spine first, in three stages:

1. **Drain to a clean baseline.** Bring every open `llm/*` branch to an
   integrated state before planning new work — an interrupted prior run may have
   left in-flight trains. The dispatcher completes each recoverable train through
   its remaining review/integration (§11); a train that cannot merge autonomously
   (blocked, needs-human, or an unreconciled dirty tree) is surfaced and the run
   exits for a human rather than looping. The prior traincar schedule is then
   **discarded** — new WIs may have been added, so it is stale; the schedule is
   derived fresh each launch, never resumed.
2. **Clear the gated spine, serially, whole-project.** Gate-affecting work is not
   fanned out — concurrent spine writes are the hazard §5.1 forbids. G1
   requirement work (draft/reopen SN/SR) runs as one coherent whole-project pass;
   if the gate needs human ratification the run **exits for ratification** (under
   `attended`/`human` gate authority; under `autonomous` the agent ratifies and
   continues). G2 decomposition (LLR/TC) then runs the same way, with the same
   ratification exit. Only a drafted, decomposed, ratified spine proceeds.
3. **Plan and dispatch build-out.** With the spine settled, the work-advisor
   scans the unblocked frontier and packs WIs into **traincars** (§7), then runs
   the steady-state loop below — dispatching any traincar whose dependencies are
   integrated to a free worker as one opens up.

For each scheduling event the dispatcher:

1. loads the integrated WI registry;
2. reconciles existing reservations and trains (§11);
3. computes the dependency-ready frontier;
4. applies the lowest-gate-first hard filter;
5. excludes blocked, deferred, reserved, protected-conflicting, and explicitly
   exclusive-conflicting WIs;
6. orders survivors by `(gate class, Priority descending, remaining hard-path
   length descending, WI id)`; and
7. reserves candidates until the worker ceiling or eligible frontier is
   exhausted.

It rescans after every reservation release, worker completion, block, review
verdict, or integration. It does not create static waves that wait for the
slowest member before filling a free lane.

`schedule.py` is a new stdlib-only library/CLI shared by validation, dashboard,
dispatcher, and tests:

```text
python scripts/schedule.py ready --explain
python scripts/schedule.py ready --format json
python scripts/schedule.py simulate --jobs 2
```

`check_trajectory.py` validates the registry and calls the library where useful;
it does not become the stateful scheduler.

## 5. Concurrency safety: optimistic ordinary work, explicit hard boundaries

The scheduler does **not** treat shared `Workstream`, `Campaign`, or `SpecRef` as
mutexes. Those are broad categories, and using them as locks would serialize
the same related work this feature exists to accelerate.

### 5.1 Always serialized

- hard predecessor/descendant relationships outside one authorized train;
- requirement-spine, gate-advance, attestation, and root registry mutation;
- root coordination files and generated artifacts owned by the integrator;
- two WIs sharing a non-empty `Exclusive` key;
- a WI explicitly marked blocked/deferred;
- any state the dispatcher cannot reconcile to a single owner.

Spine-affecting work may still use a worker branch, but only one such train is
active and it integrates before another spine train starts. Generated artifacts
are regenerated on the composed integration tree rather than text-merged from
workers.

### 5.2 Optimistically parallel

Independent, dependency-ready off-spine WIs normally run together even when
their precise path sets are not predeclared. Each train records its base commit.
At integration the dispatcher compares its changed paths with changes integrated
since that base:

- disjoint paths take the fast path;
- overlapping paths trigger integrator reconciliation;
- textual conflicts are resolved on the integration staging branch;
- an integrator-**authored** reconciliation is *material* and invalidates the old
  approval, requiring a fresh review of the composed change; taking one side of a
  conflict verbatim is **not** material;
- the combined commit bar always runs, even after a clean textual apply.

**Material edit — the bright line.** Re-review is required iff the composed tree
contains, in any non-generated product or doc file, a hunk that is **not**
byte-identical to one side of the merge. A clean 3-way apply, and a conflict
resolved by keeping one side verbatim, never re-review; any hunk the integrator
authors (interleaving two edits, reconciling two logic changes, hand-adjusting a
value) always does. Generated artifacts are exempt — they are regenerated, not
reviewed. The rule is mechanical so the boundary cannot drift between sessions.

Telemetry records overlap, conflict, re-review, and rollback rates. A repeated
collision is **under-allocation evidence** (§1.11): the run reconciles and
continues — it never pauses — and a human reviews the pattern in retrospect,
declaring an `Exclusive` key or hard edge on any *not-yet-run* WI that shares the
resource (it cannot un-collide work already done). The dispatcher never infers or
enforces a key itself, and the system does not demand speculative path metadata
before evidence shows a need.

## 6. Lane and branch lifecycle

For each accepted candidate the dispatcher:

1. chooses a unique train id, e.g. `WI-180-a31f`;
2. creates `llm/train/WI-180-a31f` from the current integration HEAD;
3. creates/reuses a linked worktree leased to that branch;
4. writes the runtime reservation atomically;
5. launches an internal worker with explicit `--wi`, `--train`, and worktree
   arguments; and
6. records the process identity as a lease hint, never as proof of life.

The unique train branch ref is the durable reservation: its name carries the WI
and train id, and before the first work commit its target is the exact base. The
first real WI commit carries `WI`, `Train`, and `Base` trailers; later recovery
can derive the same base with `git merge-base`. This avoids an empty metadata
commit and its unnecessary product-hook run while preserving recovery if the
machine dies before the worker's first commit.

The worker prompt is assembled from `AGENTS.md`, the WI row, its `SpecRef`, its
predecessor context, the current train diff, and any rework finding. It does not
resume from `status.md` and does not read `docs/next-wi`.

Workers commit coherent progress per WI. Their branches do not edit root
`status.md`, `run-state`, `next-wi`, the integrated WI statuses, the root log, or
generated root artifacts. WI-scoped review evidence uses collision-safe paths
or ids and names the exact reviewed code commit.

## 7. Traincars — continuation, execution, and clustering

After a WI reaches its required local commit/review boundary, the dispatcher
may authorize the same lane to pull its successor onto the train. Continuation
requires all of the following:

1. the current WI has exactly one unclaimed hard successor;
2. that successor is queued and not reserved elsewhere;
3. every other hard predecessor of the successor is already integrated or is an
   approved ancestor on this train;
4. the successor has no explicit exclusive conflict with another active train;
5. continuation does not cross a spine/gate/attestation boundary;
6. its critique/review policy does not require an integration checkpoint; and
7. the train has not reached the configurable safety cap (default four WIs).

The sequence ends when the current WI has zero or multiple hard successors, the
only successor joins another unintegrated branch, a blocker appears, a boundary
requires composition, or the cap is reached.

At a **fork**, the parent train integrates, then each newly ready child may take
a separate lane. At a **join**, all parent trains integrate, then the join WI
starts from the combined integration HEAD. A downstream WI is never built from
two unintegrated sibling branches.

**Execution model — one Build, one Review per traincar.** A traincar is the
review unit: one Build pass (planning/optimization included as each WI needs)
produces **one commit per WI** on the branch, then **one Review** covers the
traincar's combined diff. This single-review model is safe by construction
because the clustering rule (below) only groups **review-compatible** WIs into a
multi-WI traincar — off-spine, bounded, not critique-gated, no boundary crossing.
A strong, spine-touching, critique-verified, or high-risk WI runs as its **own
single-WI traincar** with its own review. Every WI stays a distinct
commit/evidence unit, and any material integration edit (§5.2) is reviewed again
regardless.

### Traincar clustering — the work-advisor (research-informed, design open)

Packing WIs into traincars is the open design piece. It is **resource-constrained
DAG scheduling with task clustering**, and the literature says keep it simple:

- **List scheduling (Graham, *Bell System Technical Journal*, 1966)** — greedily
  dispatching ready tasks to free workers in priority order is within `(2 − 1/m)`
  of optimal makespan for `m` workers, even with an imperfect priority. The "no
  optimal scheduler needed" license; it is already the shape of §4's dispatch loop.
- **HEFT (Topcuoglu, Hariri & Wu, *IEEE TPDS* 13(3):260–274, 2002)** — prioritize
  by *upward rank* (critical path to the exit) on heterogeneous workers. §4's
  `remaining hard-path length` ordering is the upward-rank heuristic; the model
  tiers are the heterogeneous workers.
- **DAG clustering / coalescing (Sarkar, MIT Press, 1989 — edge-zeroing; DSC —
  Yang & Gerasoulis, *IEEE TPDS*, 1994)** — the batch-vs-parallel trade-off as
  computation-vs-communication. Here the "communication cost" is per-traincar
  **integration + review overhead**: group WIs into one traincar when the overhead
  saved exceeds the parallelism and failure-isolation given up — so small
  mechanical off-spine WIs batch, substantial ones stay separate. Clustering must
  respect WI precedence (no traincar cycle).
- **LPT / bin packing (Graham, *SIAM J. Applied Math*, 1969 — the `4/3 − 1/3m`
  bound)** — balancing sized WIs across workers needs a per-WI size estimate,
  which is why the `EstTokens` column (§3.1) is a prerequisite.

Applied analogs to crib rather than reinvent: `make -j` / Ninja (job-limited DAG
dispatch); Bazel / Nx / Turborepo (build-target DAG + affected-set + caching);
merge queues — GitHub merge queue, Bors, and **Zuul**'s speculative dependent
pipelines — for the integration-ordering half (the §13 speculative-merge-queue
rung); Airflow **pools** + `priority_weight` and Temporal **durable execution**
for resource caps and the §11 recovery semantics.

**Estimates come from telemetry already collected.** The session logs record
`tokens`, `cost-usd`, `turns`, and `api-secs` per WI, so `EstTokens` can be
*calibrated from historical actuals* (by BuildTier / SpecRef size / file-touch
count) rather than guessed — and the scheduler is kept **robust to bad estimates**
(Graham's bound holds within ~2× even when sizes are wrong, so precision has
diminishing returns).

**Design path (in order):**

1. add the `EstTokens` estimate to the WI schema (draft-time, telemetry-calibrated);
2. design the clustering heuristic (the batch-vs-parallel rule above);
3. define the **traincar DAG** ingestion — traincars carry dependencies on other
   traincars, and a traincar whose dependencies are all integrated is fed to a
   free LLM worker thread as one opens up (list scheduling over the traincar DAG).

These three precede Slice D's dispatcher (§15).

## 8. Review semantics

- A review verdict belongs to `(WI or train scope, reviewed code HEAD)`, not to a
  lane name or mutable branch tip.
- Existing review-policy count, family heterogeneity, critique budget,
  escalation, and rework rules remain in force.
- A reviewer never approves another concurrent train implicitly.
- `CHANGES-REQUESTED` returns the same reservation to rework; it does not expose
  the WI to another lane.
- A failed/blocked train does not prevent disjoint ready work from continuing.
- If integration changes reviewed product files beyond mechanical conflict
  resolution, the integrator schedules a fresh review before advancing root.

The old global `docs/rework-wi` pointer becomes assignment-scoped dispatcher
state. Durable findings remain in review artifacts; the dispatcher reconstructs
which train owns them from the reviewed-head metadata.

## 9. Atomic serialized integration

The integration branch has one logical writer. For each ready train, in
deterministic queue order, the integrator:

1. creates a temporary integration branch/worktree from the exact current root
   HEAD (`llm/integrate/<train-id>`);
2. verifies reservation metadata, WI scope, train commit sequence, and the
   review verdict for the exact code HEAD;
3. applies the product/doc changes while excluding runtime reservation
   bookkeeping;
4. resolves overlap/conflicts against the already-integrated tree;
5. re-reviews if the resolution was material;
6. updates WI rows to `done` with their Deliverables, and records the largest
   delivery-phase advance among the composed trains (§10 Delivery `Phase`);
7. appends the durable integration/session evidence to `docs/log.md`;
8. regenerates root `status.md` and all generated artifacts;
9. runs the combined commit bar, and the full/gate bar when the train closes a
   slice, campaign, or gate;
10. creates one integration commit with `Integrated-WI` and `Train-Head`
    trailers; and
11. advances the integration ref from the expected old hash to the new hash
    using compare-and-swap semantics.

If root moved since step 1, the compare-and-swap fails harmlessly and the train
re-enters composition from the new HEAD. The main development branch is never
left half-applied: before the atomic ref advance, all mutation occurs on the
temporary integration worktree.

Cleanup is conservative. Integrated, clean train worktrees/branches may be
retained for diagnostics or removed later. The dispatcher never deletes an
unintegrated commit or dirty worktree automatically.

**Branch hygiene is advisory.** A rolling check (kit-idiomatic, like the push and
privacy advisories) lists `llm/train/*` and `llm/integrate/*` refs whose tip is
older than a threshold (default two days) and recommends cleanup —
`git for-each-ref --sort=committerdate refs/heads/llm/`, warn-only, never an
automatic delete. It splits branches already merged into the integration ref
(`git branch --merged`, safe to remove) from those still carrying unintegrated
commits (flagged louder as possibly stranded work). Automated pruning is a later
rung; for now the human decides.

## 10. `status.md`, `next-wi`, and run-state migration

### `docs/next-wi`

Delete it from the scaffold and remove all coordinator, prompt, BuildTier,
batching, check, test, and process dependencies. `Priority` supplies deliberate
ordering in the registry; the scheduler supplies the normal order. BuildTier is
looked up from each reserved WI directly.

### `docs/status.md`

It becomes an integrator-generated reference snapshot containing only:

- derived gate/bar pointers;
- queued/deferred/blocked counts and links to the WI dashboard;
- pending `Needs <human>` items linked to `open-items.md`;
- the last integrated train and current integration-queue summary; and
- project scope/constraints whose canonical homes are linked rather than copied.

It is not an agent resume surface and is never written on worker branches. The
trajectory R-B/R-C/R-D rules that require every open WI to be repeated in status
are retired and replaced, if status is present, by generated freshness.

### `docs/run-state`

Root run-state becomes a generated dispatcher outcome:

- `RUNNING` while eligible, reserved, reviewing, or integrable work exists;
- `NEEDS-HUMAN` when a required human act is the global next action;
- `BLOCKED` only when every unfinished active-queue WI is blocked/waiting with no
  recoverable train able to advance;
- `DONE` only when no queued/reserved/integrable work remains.

Workers have no tracked lane-local run-state. Their exit/result is runtime
dispatcher state plus committed evidence.

### `docs/run-phase`

Delete it. The PLAN/BUILD/REVIEW session phase was a single-lane global; in the
parallel model each lane's phase is its runtime state (§3.3 `building` /
`reviewing` / …) and model routing keys off that activity, not a tracked file.
Nothing reads a repo-global run-phase, and its routing wiring is removed.

### Delivery `Phase` (v2/v3)

Derive it; do not store a live pointer. The **current active phase** follows from
which `[phase]-[gN]` gate anchors are closed (already `derive_gate.py`'s basis);
at integration the integrator prefers the **largest phase bump** among the trains
it composes, so a phase advance made on one lane surfaces at merge. Remove the
per-SR `Phase` column **except** where it records a **forward deferral** — an SR
authored now but scheduled for a later phase (the phase-deferred exemption),
which is intent, not a derivable workflow fact. A repo that never defers drops
the column entirely. Because a campaign is only a WI attribute and never a
scheduling unit (§1.3), campaigns need no isolation machinery: campaign-tagged
WIs parallelize wherever they are off-spine, and the only serialization is spine
work itself (§5.1).

## 11. Crash safety and recovery

`out/dispatch/` is gitignored because it is runtime state, but it is persistent
on an ordinary process/OS crash and accelerates recovery:

```text
out/dispatch/
  manifest.json
  events.jsonl
  dispatcher.lock
  trains/<train-id>.json
```

Manifest writes use temp-file + flush + atomic replace. Events append before the
corresponding externally visible action where possible. The dispatcher reserves
durably before launching a worker.

The directory is nevertheless a **cache/journal, not authority**. Every startup
acquires the repo-level dispatcher lock and performs recovery before scheduling:

1. read the integrated WI registry and root integration trailers;
2. enumerate `llm/train/*` and `llm/integrate/*` branches;
3. enumerate linked worktrees and their dirty/clean state;
4. parse reservation commits and exact-head review records;
5. cross-check the runtime manifest when present;
6. reconstruct one ownership/state record per WI and train;
7. quarantine ambiguity or duplicate reservations; and
8. only then derive new work.

Recovery rules:

| Observed evidence | Recovery action |
| --- | --- |
| Train branch exists; worktree missing | Recreate the worktree from the branch |
| Worktree is dirty | Resume that WI with a reconcile-first prompt; never reset/stash automatically |
| Implementation commits exist; no valid review | Schedule review |
| Review approves the exact code HEAD | Restore `ready-to-integrate` |
| Review names an older HEAD | Re-review |
| Integration commit exists and WI is done | Restore `integrated`; cleanup is optional |
| Runtime manifest entry has no branch/worktree | Drop the stale cache entry after recording recovery |
| Two branches reserve one WI | Quarantine both; start neither until ownership is resolved |
| Integration staging branch exists | Resume/verify staging; root remains unchanged until CAS |
| Ownership cannot be proven | Fail closed for that WI and continue only disjoint proven work |

Kernel locks release when processes die. Stored PIDs are hints and are never
trusted across reboot. Frequent WI commits bound the amount of dirty recovery.

This contract covers a process or computer crash with the disk intact. Disk loss
or recovery on a fresh host requires train refs to have been pushed/mirrored;
that remains subject to `docs/push-policy`. The coordinator never silently
pushes a train when policy requires a human.

## 12. Pause, blackout, cost, and capacity

- Root `docs/pause` stops new reservations at the next dispatcher boundary;
  in-flight workers finish their current safe boundary and remain recoverable.
- Blackout starts no new worker/integration session but does not corrupt or
  discard running trains.
- `--jobs` is a ceiling, not a promise. Unavailable/cooling model routes,
  provider-specific account serialization, review requirements, and eligible
  frontier width may reduce actual concurrency.
- One worker failure cools/releases only its route and assignment as existing
  policy dictates; other disjoint trains continue.
- The banner reports active lanes, queued frontier, integration queue, and the
  cost/concurrency ceiling so parallel spend is visible.

## 13. Telemetry and adaptive policy

Record reason-coded events for frontier decisions, reservation, worker/reviewer
start/finish, continuation, fork/join, overlap, conflict, re-review, integration,
recovery, quarantine, and cleanup. Aggregate by `(train, WI, session)` so
parallel session numbers cannot collide.

Required measurements:

- ready-frontier width over time;
- active-worker utilization and idle reason;
- queue wait versus build/review/integration time;
- changed-path overlap and textual-conflict rates;
- semantic/integration rework and invalidated-review rates;
- train length, age, and continuation cutoff reason;
- recovery outcomes and time to resume;
- combined-bar failures after individually green trains.

The initial policy is two optimistic off-spine workers. Evidence, not intuition,
drives later changes: record repeated collisions as under-allocation evidence for
a human to correct in future WI drafts (§1.11), raise worker capacity when the
integration queue stays healthy, or lower/cap it when rework or provider pressure
dominates. Speculative merge-queue testing is a later rung,
not part of the first implementation.

## 14. Compatibility and downstream migration

The implementation must remain stdlib-only, Python 3.8+, Windows/POSIX.

Migration is explicit because this changes default execution:

1. `downstream-resync` documents that an upgraded repo **flips to the two-worker
   default** (a deliberate exercise of the framework) and the `--jobs 1` per-run
   escape hatch.
2. Existing `docs/next-wi` content is translated, if meaningful, into WI
   `Priority`, then the file is removed.
3. Legacy `active` WI rows are reconciled to queued + recovered reservation or
   returned to queued with a logged migration finding.
4. Existing long-lived `docs/tracks/*` lanes remain readable during one
   compatibility window; the new dispatcher does not schedule from them.
5. `--track` warns as deprecated and continues manual legacy behavior for that
   window; new launchers never emit it.
6. Status becomes generated only after the repository passes the new freshness
   check, preventing a half-migrated state where agents still act from prose.
7. A fresh scaffold ships `agent-resume` parallel-by-default at two workers and
   contains no `next-wi` or track directory.
8. `docs/run-phase` is deleted and its routing wiring removed; the delivery
   `Phase` column is dropped except on forward-deferred SRs (§10).
9. Before first parallel enable, existing `~` soft predecessor edges are audited
   and any that encode a *correctness* (not merely ordering) dependency are
   promoted to hard edges — the optimistic scheduler treats every soft edge as
   safe-to-run-concurrently, so a missed hard edge is the main silent-conflict
   risk. The registry validator confirms declared edges are well-formed but
   cannot detect a *forgotten* edge, so this audit is the confidence step.

## 15. Implementation slices and dependency plan

File these as separate WIs on ratification. Labels are provisional; WI ids come
from the registry at filing.

| Slice | Scope | Hard predecessors | Parallel implementation note |
| --- | --- | --- | --- |
| **A — Scheduler contract + schema** | `schedule.py`; `blocked`, `Priority`, `Exclusive`, `BlockRef`, `EstTokens`; frontier/explain/simulation tests | none | Foundation |
| **B — De-author status and remove next-wi** | prompt/process/check/bootstrap migration; generated root status contract | A | Can run beside C after A |
| **C — Worker assignment mode** | replace internal track assumptions with explicit WI/train/lane assignment; collision-safe logs/reviews | A | Can run beside B after A |
| **D — Dispatcher + worktree pool** | default `--jobs 2`; the drain→gate→build-out launch sequence (§4); traincar clustering + traincar-DAG dispatch (§7); reservations; dynamic refill; pause/blackout/model-capacity supervision | A, C | Central fan-out engine |
| **E — Change-train continuation** | unary-chain rule; fork/join behavior; caps; review-boundary composition | D | Can overlap F only if code ownership is split deliberately |
| **F — Atomic integrator** | staging branches; conflict/re-review; registry/log/status regen; CAS advance | B, D | Can overlap E only with bounded file ownership |
| **G — Recovery + fault injection** | journal; Git reconstruction; dirty/missing worktree; duplicate reservation; crash-at-every-boundary fixtures | D, F | Must prove deletion of `out/dispatch/` is recoverable |
| **H — Telemetry, scaffold, migration, dogfood** | projections; launchers; downstream-resync; two-real-WI trial; full cross-OS campaign | B, E, F, G | Campaign close |

The implementation campaign itself should exercise the new dependency design:
B and C are independent after A; E and F may proceed concurrently only after
their touched surfaces are split during planning; H is the explicit join.

## 16. Verification strategy

### Scheduler unit fixtures

- independent roots fill all available workers;
- direct and transitive hard dependencies never co-schedule;
- soft edges do not block;
- lowest-gate and Priority ordering are deterministic;
- blocked/deferred/reserved items are excluded with reason codes;
- shared Workstream/Campaign/SpecRef does not serialize;
- shared `Exclusive` keys do serialize;
- unary sequences continue; forks and joins stop/launch at the right points.

### Process/worktree integration fixtures

- two off-spine WIs build and review concurrently in separate linked worktrees;
- a free lane refills while another lane remains busy;
- one lane blocks/fails while another integrates;
- overlapping edits reach integrator reconciliation and combined tests;
- a material conflict resolution invalidates and renews review;
- a verbatim one-side conflict resolution integrates **without** re-review, while
  an integrator-authored hunk **forces** it (the §5.2 material bright line);
- the integrator records the largest delivery-phase advance among composed trains;
- the branch-age advisory lists stale `llm/*` refs and splits merged from
  unintegrated, never deleting;
- spine/gate work remains serialized;
- no worker edits root status, registry disposition, log, or generated output.

### Crash matrix

Inject termination after reservation, branch creation, dirty edit, WI commit,
review request, review verdict, integration apply, integration test, integration
commit, and immediately before/after root CAS. For each point:

- restart reconstructs exactly one owner;
- no WI is double-run or falsely done;
- no unintegrated commit/dirty tree is deleted;
- root is either entirely before or entirely after integration;
- deleting all of `out/dispatch/` still reconstructs from Git/worktrees;
- stale PIDs and released OS locks do not block recovery.

### Cross-platform and compatibility

- Windows and POSIX worktree/process/lock paths;
- `--jobs 1` behavior matches the serial semantic outcome;
- routing works with `docs/run-phase` absent (phase resolves per-lane);
- legacy `--track` compatibility window;
- existing managed routing, critique, pause, blackout, privacy, gate, and push
  policy tests remain green;
- fresh scaffold and downstream migration fixtures.

## 17. Campaign done-when

- A plain `agent-resume` launch on a fresh scaffold uses up to two workers
  without predefined tracks or `docs/next-wi`.
- The dispatcher derives and explains the frontier directly from the registry,
  reservations, and gate policy.
- Two real independent WIs execute concurrently and integrate serially; a unary
  dependent successor continues on its parent train; fork and join behavior is
  proven.
- Workers never use lane-local status/next/run-state files and never mutate root
  coordination truth.
- Root status is reference-only, integrator-generated, and freshness-gated.
- `docs/run-phase` is gone and model routing resolves per-lane; delivery phase is
  derived, with the integrator taking the largest bump at merge.
- Ordinary overlapping work is reconciled and revalidated; protected/exclusive
  work demonstrably serializes.
- The branch-age advisory reports stale `llm/` branches (merged vs. unintegrated)
  and never deletes them.
- A crash at every lifecycle boundary recovers without double assignment, lost
  commits, false completion, or half-integrated root state.
- Removing `out/dispatch/` before restart does not prevent reconstruction.
- `--jobs 1` remains available; Windows/POSIX suites and the full gate bar pass.
- Telemetry reports whether parallelism saved wall time and what prevented
  greater utilization, giving downstream adopters evidence for tuning.
