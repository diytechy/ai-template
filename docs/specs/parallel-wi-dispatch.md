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
10. **The coordinator `docs/run-phase` file is retired; the SR delivery `Phase` is
    left as-is.** The global PLAN/BUILD/REVIEW pointer is deleted: a build-out
    lane routes from its own activity (build, then review), and a train's branch
    carries a `{phase}-{gate}` name so its delivery phase is visible — and
    crash-recoverable — without per-train phase state. Delivery-phase shifts
    happen only at gates, and gate/spine work (SN/SR/TC) is serial and upfront
    (§4), so there is no concurrent phase to derive or reconcile; the SR `Phase`
    column and the derived-gate model are untouched by this campaign. Because a
    campaign is only a WI attribute (§1.3), campaign-tagged WIs parallelize
    wherever off-spine; the only serialization is spine work itself (§5.1).
11. **`Exclusive` keys and hard edges are declared at planning time and enforced by
    the dispatcher — but it never invents or silently mutates them.** They are set
    when a WI is drafted (allocating its resources), and the scheduler serializes
    on them at runtime (§5.1); that is their purpose. What the dispatcher must
    *not* do is infer, add, or reactively enforce a rule it was not given. An
    *undeclared* runtime collision is evidence the WI setup under-allocated: it is
    recorded and reconciled (§5.2) without pausing the run, and corrected upstream
    in how future WIs are drafted.

## 2. Terms and ownership

| Term | Meaning | Owner |
| --- | --- | --- |
| **Workstream / Campaign** | Human grouping and dashboard categorization | WI registry |
| **Hard predecessor** | Correctness edge that blocks readiness | WI registry |
| **Soft predecessor** | Advisory ordering only; never a safety edge | WI registry |
| **Exclusive key** | Exceptional semantic resource that cannot be mutated concurrently | WI registry (declared at draft, enforced by the scheduler); the dispatcher never invents keys — undeclared collisions are recorded, not enforced |
| **Frontier** | Queued WIs whose hard predecessors are integrated done | Scheduler, derived |
| **Reservation** | Dispatcher claim preventing another worker from owning the WI | `refs/llm/reservations/WI-###` (durable) + dispatcher journal (cache) |
| **Lane** | Temporary worker process and linked worktree | Dispatcher |
| **Change train** | One branch carrying an ordered dependency chain of one or more WIs | Lane, dispatcher-authorized |
| **Integration queue** | Reviewed trains waiting to compose into the development branch | Integrator |
| **Integration branch** | Dispatcher-owned aggregation branch `refs/heads/llm/integration`, published by CAS to the selected development branch | Integrator only |

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
- `EstTokens` — a draft-time size estimate feeding the traincar clustering
  heuristic (§7), calibrated from session-log telemetry and kept advisory (the
  scheduler stays robust to a wrong estimate).
- `SafetyClass` — planning-time classification used by the shared safety
  classifier: `ordinary|spine|gate|attestation|protected|high-risk`. It is
  required for newly queued WIs. A migrated queued WI remains `unclassified`
  until audited and fails closed for dispatch; empty is never silently treated
  as `ordinary`.

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
- `ready` — every hard predecessor is integrated `done`, or is an
  **accepted-on-train** ancestor (locally green and committed on the same
  dispatcher-authorized train, not yet reviewed);
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
During downstream migration a repo **flips to the two-worker default only after
its soft-edge and SafetyClass audits pass** (§14) — those audits are what make
optimistic parallelism safe, so until both pass the repo runs `--jobs 1`, and the
promotion to two workers is a recorded, deliberate step. Running `agent-resume`
remains the permission-bypass consent act; a second parallel-consent file is
unnecessary.

### The launch sequence — reconcile, gate, then build-out

A launch does not jump straight into parallel build-out; it establishes a clean
baseline and clears the gated spine first, in three stages:

1. **Reconcile owned trains to a clean baseline.** Before planning fresh
   traincars, resolve every dispatcher-owned branch — `llm/train/*` and
   `llm/integrate/*`, **not** manual `llm/*` branches: integrate the recoverable,
   resume the incomplete with a reconcile-first prompt (§11), and **quarantine**
   only the genuinely stuck (ambiguous ownership, or a train needing a human). A
   quarantined train never halts the run — disjoint ready work still proceeds
   (§8). The prior traincar schedule is then **discarded** and re-derived fresh —
   new WIs may have been added, so it is stale; only active reservations survive,
   never a stale prospective plan.
2. **Clear the gated spine, serially, whole-project.** Gate-affecting work is not
   fanned out — concurrent spine writes are the hazard §5.1 forbids. G1
   requirement work (draft/reopen SN/SR) runs as one coherent whole-project pass;
   if the gate needs human ratification the run **exits for ratification** — under
   `attended` (a human ratifies each batch) or `single-ratify` (a human ratifies
   once at the `[g2]` close); under `autonomous` an independent LLM reviewer's
   verdict closes the gate and the run continues. G2 decomposition (LLR/TC) then
   runs the same way, with the same ratification exit. Only a drafted, decomposed,
   ratified spine proceeds.
3. **Plan and dispatch build-out.** With the spine settled, the work-advisor
   scans the unblocked frontier and packs WIs into **traincars** (§7), then runs
   the steady-state loop below — dispatching any traincar whose dependencies are
   integrated to a free worker as one opens up. The traincar DAG records grouping
   and dependencies, not a static execution sequence: among dependency-clear
   traincars, the dispatcher honors explicit human Priority first, then takes the
   one with the most downstream dependents.

For each scheduling event the dispatcher:

1. loads the integrated WI registry;
2. reconciles existing reservations and trains (§11);
3. computes the dependency-ready frontier;
4. applies the lowest-gate-first hard filter;
5. excludes blocked, deferred, reserved, protected-conflicting, and explicitly
   exclusive-conflicting WIs;
6. packs survivors into the current traincar DAG (§7), then orders eligible
   traincars by `(gate class, Priority descending, transitive
   downstream-dependent count descending, remaining hard-path length descending,
   first WI id)`;
   and
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

### Deterministic safety classification

`schedule.py` owns one pure classifier shared by validation, dashboard,
traincar packing, and dispatch. Its inputs are the WI's declared `SafetyClass`,
gate/phase, hard edges, `Exclusive` keys, and applicable review/critique policy;
its output is a scheduling class plus reason codes. The ordered rules are:

1. `spine`, `gate`, and `attestation` serialize whole-project and cannot join a
   multi-WI traincar;
2. `protected` serializes whole-project; narrower semantic-resource locking uses
   declared `Exclusive` keys instead;
3. `high-risk`, a critique requirement, or a review policy requiring an
   integration checkpoint forces a single-WI traincar;
4. only classified `ordinary` work is eligible for optimistic multi-WI packing;
   and
5. missing, invalid, or contradictory input returns `unclassified`, fails closed
   for that WI, and does not stop disjoint classified work.

The dispatcher does not infer or rewrite `SafetyClass`, review boundaries,
hard edges, or keys. `ready --explain` exposes the classifier's reason codes so
the same decision is inspectable everywhere it is enforced.

Declaration is not accepted blindly. The validator conservatively cross-checks
`SafetyClass` against structural evidence available before dispatch: a `SpecRef`
or declared deliverable surface resolving into SN/SR/LLR/TC registries or their
tracked documents requires `spine`; gate derivation, `docs/gate`, or ratification
scope requires `gate`; attestation scope requires `attestation`; and applicable
critique/review policy must agree with any claimed `ordinary` class. A mismatch
is a hard validation finding and classifies that WI as `unclassified`; the
validator never silently upgrades or edits the declaration. Because structural
checks cannot detect omitted scope, first parallel enable also requires the
planning audit in §14.

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
- any genuine conflict resolution — including taking one side (`ours`/`theirs`)
  verbatim, or a hand-authored merge — invalidates the old approval and requires a
  focused re-review of the composed change;
- the combined commit bar always runs, even after a clean textual apply.

**When integration re-review is required.** A clean, conflict-free apply (a 3-way
merge with no conflict), and a generated artifact recreated from reviewed sources,
never re-review. **Any genuine conflict resolution does** — *including* choosing
one side (`ours`/`theirs`) verbatim, because a conflict means two reviewed changes
were incompatible and one was dropped; byte-identity proves only *where the text
came from*, not that the composed result satisfies both WIs. Hand-authored
reconciliation likewise re-reviews. The renewed review is **focused** on the
composed conflict and the requirements it touches — it does not repeat every
original review.

Telemetry records overlap, conflict, re-review, and rollback rates. A repeated
collision is **under-allocation evidence** (§1.11): the affected train is
reconciled, returned to rework, or quarantined when human judgment is required,
while disjoint eligible work continues. A human reviews the pattern in
retrospect, declaring an `Exclusive` key or hard edge on any *not-yet-run* WI
that shares the resource (it cannot un-collide work already done). The
dispatcher enforces only *declared* keys, never one of its own invention, and
the system does not demand speculative path metadata before evidence shows a
need.

## 6. Lane and branch lifecycle

For each accepted candidate the dispatcher:

1. chooses a unique train id, e.g. `v3-g3-WI-180-a31f` — a `{phase}-{gate}` prefix
   recording the delivery phase and gate the train builds within;
2. creates one off-history reservation metadata commit with `git commit-tree`
   (the base tree and parent plus the train id and complete WI list), then
   atomically creates the train branch and one fixed reservation ref per
   constituent WI using one `git update-ref --stdin` transaction with
   zero-old-value checks; the train branch initially points at the exact
   integration base, not at the off-history reservation commit;
3. creates/reuses a linked worktree leased to the train branch;
4. writes the runtime reservation cache atomically;
5. launches an internal worker with explicit `--wi`, `--train`, and worktree
   arguments; and
6. records the process identity as a lease hint, never as proof of life.

The durable reservation is the atomically created set of Git refs:

```text
refs/llm/reservations/WI-180
refs/llm/reservations/WI-181
```

Every constituent ref points to the same reservation metadata commit. Its fixed
name makes the zero-old-value check an atomic uniqueness claim for that WI; the
commit maps the complete traincar to its id and exact base. `git commit-tree`
does not update product history, check out files, or run product commit hooks.
If any WI is already reserved, the transaction fails and none of the traincar's
refs or branch is created. The first real WI commit still carries `WI`, `Train`,
and `Base` trailers; recovery cross-checks those trailers and `git merge-base`
against the reservation commit. Integration, blocking, or release deletes the
applicable reservation refs transactionally only after their durable disposition
has advanced; the unreachable metadata object is then left to ordinary Git
garbage collection.

The worker prompt is assembled from `AGENTS.md`, the WI row, its `SpecRef`, its
predecessor context, the current train diff, and any rework finding. It does not
resume from `status.md` and does not read `docs/next-wi`.

Workers commit coherent progress per WI. Their branches do not edit root
`status.md`, `run-state`, `next-wi`, the integrated WI statuses, the root log, or
generated root artifacts. WI-scoped review evidence uses collision-safe paths
or ids and names the exact reviewed code commit.

## 7. Traincars — continuation, execution, and clustering

A traincar is a provisional grouping of review-compatible WIs plus its
dependencies on other traincars. It does not dictate a static global sequence:
the dispatcher dynamically list-schedules dependency-clear traincars, reserving
a selected traincar's constituent WIs when it assigns the traincar to a lane.
The prospective grouping is discarded and recomputed after any integration,
block, failure, registry change, or reservation release; only active
reservations survive recomputation.

Within an assigned traincar, after a WI reaches its local commit boundary
(locally green and committed, not yet reviewed), the same lane may continue to
the traincar's next successor. Continuation requires all of the following:

1. the reserved traincar names that successor as the next WI after the current
   WI's single hard-successor edge;
2. every other hard predecessor of the successor is already integrated or is an
   accepted-on-train ancestor on this train;
3. the safety classifier still permits the grouping — no newly visible
   exclusivity, boundary, or review-policy conflict has appeared; and
4. the train has not reached the configurable safety cap (default four WIs).

The sequence ends when the current WI has zero or multiple hard successors, the
only successor joins another unintegrated branch, a blocker appears, a boundary
requires composition, or the cap is reached.

If one constituent WI blocks, the WI — not the traincar — receives the durable
`blocked` disposition and `BlockRef` through the serialized integrator. The
traincar is dissolved: unstarted constituents are released to `queued`, the
traincar DAG is recomputed, and no descendant that depends on the blocked WI may
integrate. Already completed constituents that do not depend on the blocked WI
may still proceed through their required review and integration. A traincar is a
runtime scheduling structure and never inherits or writes a project-level
`blocked` status of its own.

The same cleanup rule applies to every other early traincar end: after preserving
any completed constituent scope that can still proceed independently, the
dispatcher transactionally releases every unstarted constituent reservation,
dissolves the obsolete grouping, and recomputes the traincar DAG. A newly visible
exclusivity, boundary, review-policy conflict, failure, or safety-cap cutoff
therefore cannot strand reservation refs for work the lane will not consume.

At a **fork**, the parent train integrates, then each newly ready child may take
a separate lane. At a **join**, all parent trains integrate, then the join WI
starts from the combined integration HEAD. A downstream WI is never built from
two unintegrated sibling branches.

**Execution model — one Build and one review cycle per traincar.** A traincar is
the indivisible review scope: one Build pass (planning/optimization included as
each WI needs) produces **one commit per WI** on the branch, then one review
cycle covers the traincar's complete combined diff. That cycle uses however many
independent reviewers the applicable review count, reviewer-family, critique,
and complexity policies require; it is not split into separate per-WI reviews.
A successor within the train depends on its predecessor
being **accepted-on-train** (locally green and committed), not reviewed — the
review comes once, at the end — and **no constituent WI becomes `done` until the
whole train is reviewed and integrated atomically** (§9). This single-review model
is safe by construction because the clustering rule (below) only groups
**review-compatible** WIs into a multi-WI traincar — off-spine, bounded, not
critique-gated, no boundary crossing. A strong, spine-touching, critique-verified,
or high-risk WI runs as its **own single-WI traincar** with its own review. Every
WI stays a distinct commit/evidence unit, and any integration conflict resolution
(§5.2) triggers a focused re-review regardless.

For a multi-WI traincar, policy aggregation is deterministic: its scheduling
Priority is the highest constituent Priority (preserving the human override);
its transitive downstream-dependent count is the number of distinct traincars
reachable from any constituent after clustering; its remaining hard-path length
is the maximum remaining constituent-to-terminal hard-edge length;
its BuildTier is the strongest constituent tier; its reviewer count is the
maximum required by any constituent or by the traincar's computed complexity;
and its required reviewer families are the union of constituent requirements. A
constituent whose policy requires individual critique, spine review, or an
integration checkpoint is not aggregated — the safety classifier places it in
a single-WI traincar.

### Traincar clustering — the work-advisor (research-informed)

Packing WIs into traincars is **resource-constrained DAG scheduling with task
clustering** (list scheduling + DAG clustering + bin packing). The prior art — its
sources, applied analogs, and the reason its guarantees do **not** transfer to
this setting — is the `parallel-scheduling` knowledge pack
([docs/knowledge/parallel-scheduling.md](../knowledge/parallel-scheduling.md));
**no approximation bound is claimed for this system**. The normative rule it
distils:

- **Structural rank** — after the registry's human `Priority`, greedy list
  scheduling uses transitive downstream-dependent count and then critical-path
  length (§4); a cost-weighted, HEFT-style rank is a later upgrade.
- **Batching** — group WIs into one traincar only when the per-traincar
  **integration + review overhead** saved exceeds the parallelism and
  failure-isolation given up — small mechanical off-spine WIs batch, substantial
  ones stay separate — and never so as to create a traincar cycle (clustering
  respects WI precedence).

**Cost signal.** Calibrate `EstTokens` from telemetry already logged (`tokens`,
`cost-usd`, `turns`, `api-secs`) rather than guessing, and prefer **wall / API
seconds** over raw tokens as the scheduling cost — tokens do not capture review
and integration latency. Keep the scheduler robust to a wrong estimate.

**Design path (front of the campaign, in order):**

1. add the `EstTokens` estimate to the WI schema (draft-time, telemetry-calibrated);
2. design the clustering heuristic (the batch-vs-parallel rule above);
3. define the **traincar DAG** ingestion — traincars carry dependencies on other
   traincars, and a traincar whose dependencies are all integrated is fed to a
   free LLM worker thread as one opens up (list scheduling over the traincar DAG).

These three are foundational to Slice D's dispatcher (§15) — built with it, not
deferred.

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

1. creates a temporary integration branch/worktree from the exact current
   integration HEAD (`llm/integrate/<train-id>`);
2. verifies reservation metadata, WI scope, train commit sequence, and the
   review verdict for the exact code HEAD;
3. applies the product/doc changes while excluding runtime reservation
   bookkeeping;
4. resolves overlap/conflicts against the already-integrated tree;
5. re-reviews if the resolution was material;
6. updates WI rows to `done` with their Deliverables;
7. appends the durable integration/session evidence to `docs/log.md`;
8. regenerates root `status.md` and all generated artifacts;
9. runs the combined commit bar, and the full/gate bar when the train closes a
   slice, campaign, or gate;
10. creates one integration commit with `Integrated-WI` and `Train-Head`
    trailers; and
11. advances the integration ref from the expected old hash to the new hash
    using compare-and-swap semantics.

If the integration ref moved since step 1, the compare-and-swap fails harmlessly
and the train re-enters composition from the new HEAD. The main development
branch is never left half-applied: before the atomic ref advance, all mutation
occurs on the temporary integration worktree.

The concrete integration ref is `refs/heads/llm/integration`. At launch the
dispatcher creates or reconciles it from the selected project development branch
and checks it out only in its dedicated integration worktree. The user's primary
worktree remains on that selected development branch — never on
`llm/integration` — while workers and the ordinary checkout never mutate the
integration ref. After a successful integration CAS, the dispatcher publishes
the integration HEAD only when the primary development worktree is clean. Because
the development-ref CAS and the worktree sync are two steps, the publish is made
crash-identifiable by a **durable publication-intent ref** rather than the
disposable `out/dispatch/` journal: before the CAS the dispatcher writes
`refs/llm/publish-intent` pointing at a metadata object that records the
integration target hash, the **expected old development hash**, and the selected
development ref. It then advances the development ref with a second CAS against
that expected old hash, synchronizes the clean worktree's index and files to the
target using fast-forward/reset semantics (never a merge), and deletes the intent
ref **only after** the sync succeeds. This bounds the reset: a reset fires only
when **both** the index tree and the tracked worktree are exactly at the intent's
expected old hash (untracked files are left untouched, and a checkout obstruction
defers synchronization rather than deleting anything); any divergence means edits
landed in the CAS-to-sync window, so publication is deferred and the checkout is
left untouched and reported, never reset — the intent ref, not a guessed ancestor,
is what tells recovery which hash was pre-publication even when several integration
commits have accumulated while publication was deferred. If
the development ref moved to a third hash (neither the expected old hash nor the
target), no publication occurred and the second CAS fails harmlessly. The
singleton intent then follows an explicit lifecycle so a failed attempt is never
mistaken for an in-flight one: the integrator keeps the stale intent as recovery
evidence while it recomposes from the new development HEAD, then **transactionally
replaces** it — an expected-old-value CAS on `refs/llm/publish-intent` against the
stale object it observed, so two racing recompositions cannot both replace it —
with the new attempt's metadata. An existing intent is reused only when all three
fields — target, expected old hash, and development ref — match exactly; a
differing intent is never silently overwritten. If the development ref
is instead already at the target, a prior attempt's publication succeeded, so the
intent is deleted once the worktree sync is confirmed. If the worktree is
dirty at the outset, publication is deferred and the checkout is left untouched
and reported, never reset/stashed automatically. A manual update to
`llm/integration` itself is likewise detected by its CAS and forces recomposition.

### Blocked-disposition integration

A worker-reported blocker uses a smaller serialized transaction rather than the
successful `done` path. The integrator validates the named WI, `BlockRef`, and
committed evidence; starts from the current integration HEAD; changes only that
WI to `blocked`; appends the durable log evidence; regenerates status and derived
artifacts; runs the applicable documentation/registry bar; commits with
`Blocked-WI`, `BlockRef`, and `Train` trailers; and advances the integration ref
by CAS. Only after that CAS succeeds does it transactionally delete the blocked
WI's reservation ref, release unstarted constituent reservations, dissolve the
traincar, and recompute the traincar DAG. Completed constituents independent of
the blocked WI retain reservations and proceed through their required review;
dependent descendants cannot integrate. A CAS race recomposes this disposition
transaction exactly as it does a successful integration.

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

Delete it outright from fresh scaffolds and migrated repositories. Its former
content is not translated into `Priority` or any other scheduling state: the WI
DAG, gate class, registry `Priority`, and the scheduler are the complete ordering
contract. Migration may record the old declared value in its log for audit, then
removes the file.

Removal includes every live dependency, not only the file itself:

- coordinator selection, prompt scope, telemetry/session labels, rework
  precedence, BuildTier pins, and the old `;`-batch behavior in `agent_loop.py`;
- gate-first/check logic and trajectory/dashboard projections;
- launcher prompts, bootstrap/scaffold manifests, process and skill prose, and
  the work-item template documentation; and
- tests and generated architecture/dashboard outputs that encode those former
  behaviors.

The dispatcher supplies the WI/train assignment explicitly. BuildTier is looked
up directly from each reserved WI; review findings and rework ownership are
assignment-scoped dispatcher state. Historical logs, reviews, and archived specs
may retain `next-wi` references as history, but no live instruction or executable
surface reads, writes, validates, generates, or links it.

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

Delete the global file. A build-out lane routes from its own activity — build,
then review — and its train branch is named `{phase}-{gate}` (e.g.
`llm/train/v3-g3-WI-180-…`), so the delivery phase is recoverable from the branch
after a crash, without `out/dispatch/`. The richer routing phases (PLAN,
DESIGN-CHECK, CRITIQUE, G1/G2 drafting) are **not** build-out activities: they
belong to the serial, upfront gate/spine pass (§4), not a parallel lane, so they
need no per-lane global pointer. Nothing reads a repo-global run-phase, and its
routing wiring is removed.

### Delivery `Phase` (v2/v3)

**Left unchanged by this campaign.** The SR `Phase` column is authored
scope/deferral metadata consumed by the derived-gate model (`derive_gate.py`),
and phase shifts occur only at gates — during serial, upfront gate/spine work,
never on a parallel build-out train. So there is nothing to derive or reconcile
at merge: the column, its meaning, and the gate derivation stay exactly as they
are. A train's `{phase}-{gate}` branch name simply records which already-ratified
phase it builds within. Because a campaign is only a WI attribute and never a
scheduling unit (§1.3), campaigns need no isolation machinery — campaign-tagged
WIs parallelize wherever off-spine, and the only serialization is spine work
itself (§5.1).

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

1. enumerate the dispatcher-owned evidence first: `refs/heads/llm/integration`,
   `llm/train/*`, `llm/integrate/*` branches, `refs/llm/reservations/*`, the
   `refs/llm/publish-intent` ref, and the integration trailers on the development
   branch;
2. resolve the integration authority from that evidence — **presence** of
   `refs/heads/llm/integration` makes it the authoritative integrated disposition
   (the development branch is its published projection, not the recovery
   authority); **absence with no dispatcher-owned evidence** is a genuine cold
   start, so initialize it from the selected development branch; **absence while
   owned train/integrate/reservation/intent refs or integration trailers exist**
   is a deleted or corrupt ref — reconstruct it only if uniquely provable from
   that evidence, else fail closed, never silently blessing the development branch;
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
| Reservation ref exists; train worktree missing | Recreate the worktree from its train branch |
| Reservation ref metadata disagrees with train branch/trailers | Quarantine that WI/train; start neither until ownership is resolved |
| Train claims a WI without its reservation ref | Quarantine that WI/train mismatch; do not recreate authority from cache alone |
| Integration staging branch exists | Resume/verify staging; `llm/integration` remains unchanged until its CAS |
| `llm/integration` is ahead of the selected development branch | Idempotently resume publication: write (or confirm) the publication-intent ref, verify a clean worktree at its expected old hash, perform the development-ref CAS, synchronize by fast-forward/reset, then delete the intent |
| Publication-intent ref exists and the development ref already equals its integration target, but the worktree/index still match the intent's expected old hash | Re-run the idempotent clean fast-forward/reset sync to the target and delete the intent; do not classify the mechanically stale checkout as user-dirty. If the worktree diverges from that expected old hash, edits landed in the CAS-to-sync window — defer and report, never reset |
| Selected development branch moved or diverged from unpublished integration | Recompose the authoritative integration result from the new development HEAD, verify it, and retry publication; never re-dispatch a WI already done on `llm/integration` |
| `refs/heads/llm/integration` absent and no dispatcher-owned evidence | Genuine cold start: initialize it from the selected development branch |
| `refs/heads/llm/integration` absent but owned train/integrate/reservation/intent refs or integration trailers exist | Deleted/corrupt ref: reconstruct only if uniquely provable from that evidence, else fail closed — never initialize from the development branch |
| Ownership cannot be proven | Fail closed for that WI and continue only disjoint proven work |

Kernel locks release when processes die. Stored PIDs are hints and are never
trusted across reboot. Frequent WI commits bound the amount of dirty recovery.

This contract covers a process or computer crash with the disk intact. Disk loss
or recovery on a fresh host requires the whole authoritative ref set — the
`refs/heads/llm/integration` ref, `llm/train/*` and `llm/integrate/*` branches,
`refs/llm/reservations/*`, and the `refs/llm/publish-intent` ref (equally
necessary to finish or abandon an interrupted publish) — to have been
pushed/mirrored explicitly; the custom `refs/llm/reservations/*` and
`refs/llm/publish-intent` namespaces are not assumed to follow an ordinary branch
push (unlike the `refs/heads/llm/*` branches). An unmirrored `llm/integrate/*`
staging branch carries unique conflict resolution and renewed review evidence not
present on its train branch; without it, that work is reconstructable only by
recomposing and re-reviewing the train from the integration HEAD, so mirroring the
staging branch is what preserves in-progress composition across disk loss.
Mirroring remains subject to `docs/push-policy`; the coordinator never silently
pushes any ref when policy requires a human.

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

1. `downstream-resync` documents that an upgraded repo runs `--jobs 1` until its
   soft-edge and SafetyClass audits (items 9–10) pass, then **flips to the
   two-worker default** as a recorded, deliberate promotion; `--jobs 1` remains
   the per-run escape.
2. Existing `docs/next-wi` is logged once for migration audit and then removed;
   its content is not translated into `Priority`, dependencies, or a traincar.
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
8. `docs/run-phase` is deleted and its routing wiring removed; the SR `Phase`
   column and the derived-gate model are left unchanged (§10).
9. Before first parallel enable, existing `~` soft predecessor edges are audited
   and any that encode a *correctness* (not merely ordering) dependency are
   promoted to hard edges — the optimistic scheduler treats every soft edge as
   safe-to-run-concurrently, so a missed hard edge is the main silent-conflict
   risk. The registry validator confirms declared edges are well-formed but
   cannot detect a *forgotten* edge, so this audit is the confidence step.
10. Before first parallel enable, every open WI receives a reviewed `SafetyClass`.
    The validator cross-checks structurally visible spine/gate/attestation and
    review-policy evidence (§4), while the audit catches omitted or indirect
    scope the repository graph cannot prove. Any mismatch or unaudited row keeps
    that WI `unclassified`; the migration cannot promote the repo to `--jobs 2`.

## 15. Implementation slices and dependency plan

File these as separate WIs on ratification. Labels are provisional; WI ids come
from the registry at filing.

| Slice | Scope | Hard predecessors | Parallel implementation note |
| --- | --- | --- | --- |
| **A — Scheduler contract + schema** | `schedule.py`; `blocked`, `Priority`, `Exclusive`, `BlockRef`, `EstTokens`, `SafetyClass`; pure safety classifier; frontier/explain/simulation tests | none | Foundation |
| **B — De-author status and remove next-wi** | delete the file and all runtime, prompt, routing, rework, telemetry, check, process/skill, scaffold, projection, generated-output, and test dependencies; generated root status contract | A | Can run beside C after A |
| **C — Worker assignment mode** | replace internal track assumptions with explicit WI/train/lane assignment; collision-safe logs/reviews | A | Can run beside B after A |
| **D — Dispatcher + worktree pool** | default `--jobs 2`; the reconcile→gate→build-out launch sequence (§4); traincar clustering + traincar-DAG dispatch (§7); reservations; dynamic refill; pause/blackout/model-capacity supervision | A, C | Central fan-out engine |
| **E — Change-train continuation** | unary-chain rule; fork/join behavior; caps; review-boundary composition | D | Can overlap F only if code ownership is split deliberately |
| **F — Atomic integrator** | staging branches; dispatcher-owned integration ref/worktree; conflict/re-review; successful and blocked-disposition CAS paths; registry/log/status regen; transactional reservation-ref release | B, D | Can overlap E only with bounded file ownership |
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
- lowest-gate and human Priority ordering are deterministic, and Priority wins
  over downstream-dependent count within one gate class;
- blocked/deferred/reserved items are excluded with reason codes;
- shared Workstream/Campaign/SpecRef does not serialize;
- shared `Exclusive` keys do serialize;
- every `SafetyClass` and review-policy input produces the same scheduling class
  and reason codes across CLI, validator, dashboard, and dispatcher;
- missing/contradictory safety input fails closed only for the affected WI;
- an `ordinary` declaration with structurally visible spine, gate, attestation,
  critique, or review-boundary evidence fails validation rather than upgrading
  silently;
- unary sequences continue; forks and joins stop/launch at the right points.

### Process/worktree integration fixtures

- two off-spine WIs build and review concurrently in separate linked worktrees;
- a free lane refills while another lane remains busy;
- one lane blocks/fails while another integrates;
- a blocker durably marks only its WI, releases/dissolves its traincar after CAS,
  and recomputes unaffected work;
- overlapping edits reach integrator reconciliation and combined tests;
- a material conflict resolution invalidates and renews review;
- a clean, conflict-free apply integrates **without** re-review; any conflict
  resolution — including a verbatim one-side pick — forces a focused re-review
  (§5.2);
- the branch-age advisory lists stale `llm/*` refs and splits merged from
  unintegrated, never deleting;
- spine/gate work remains serialized;
- mixed traincar policy selects the strongest BuildTier, maximum reviewer count,
  and union of reviewer families; boundary-requiring WIs remain single-WI;
- a dirty ordinary checkout remains untouched after integration while the
  dispatcher-owned integration ref/worktree advances cleanly;
- no worker edits root status, registry disposition, log, or generated output.

### Crash matrix

Inject termination during the atomic multi-WI reservation-ref transaction and
after reservation, branch creation, dirty edit, WI commit, review request,
review verdict, blocked-disposition apply, integration apply, integration test,
integration commit, immediately before/after integration-ref CAS, the
publication-intent write and its transactional replacement, and immediately
before/after the development-publication CAS and clean-worktree synchronization.
For each point:

- restart reconstructs exactly one owner;
- no WI is double-run or falsely done;
- no unintegrated commit/dirty tree is deleted;
- `llm/integration` is atomically either entirely before or entirely after
  integration;
- the development ref and its worktree are in exactly one of three recoverable
  states — fully unpublished, fully synchronized to the integration target, or
  recoverably in-between with a valid publication-intent ref proving the
  expected-old and target hashes — so recovery finishes or safely abandons the
  publish, never leaving an unclassifiable fourth state;
- an unpublished integration commit remains authoritative and is published
  idempotently rather than making its already-done WIs ready again;
- a crash between the development-ref CAS and the worktree sync is recognized via
  the publication-intent ref and idempotently synchronized — never reported as
  user dirt, never reset over edits that diverge from the intent's expected old hash;
- an identical existing publication-intent is reused, a differing one is never
  overwritten, and the transactional replacement is an expected-old-object CAS on
  `refs/llm/publish-intent`;
- a failed development CAS retains the old intent through recomposition and then
  replaces it; a crash immediately before or after that replacement recovers
  deterministically to exactly one intent (never a lost or duplicated attempt);
- deleting all of `out/dispatch/` still reconstructs from Git/worktrees;
- every constituent reservation reconstructs from
  `refs/llm/reservations/*`, including before its first WI commit;
- stale PIDs and released OS locks do not block recovery.

### Cross-platform and compatibility

- Windows and POSIX worktree/process/lock paths;
- `--jobs 1` behavior matches the serial semantic outcome;
- routing works with `docs/run-phase` absent — a build-out lane's phase resolves
  from its activity and its `{phase}-{gate}` branch name, recoverable without
  `out/dispatch/`;
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
- `docs/run-phase` is gone; a build-out lane routes from its activity and its
  `{phase}-{gate}` branch name, and the SR `Phase` column / derived-gate model are
  unchanged.
- Ordinary overlapping work is reconciled and revalidated; protected/exclusive
  work demonstrably serializes.
- The branch-age advisory reports stale `llm/` branches (merged vs. unintegrated)
  and never deletes them.
- A crash at every lifecycle boundary recovers without double assignment, lost
  commits, false completion, or half-integrated authoritative state or
  unclassifiable publication state.
- Removing `out/dispatch/` before restart does not prevent reconstruction.
- `--jobs 1` remains available; Windows/POSIX suites and the full gate bar pass.
- Telemetry reports whether parallelism saved wall time and what prevented
  greater utilization, giving downstream adopters evidence for tuning.
