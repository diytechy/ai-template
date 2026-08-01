+++
id = "WI-383"
title = "RULED 2026-07-31 (docs/concurrency-v2.md §A1 and §A6.1) - the design is ruled into log.md's Decisions, so this row is CLAIMABLE. RESCOPED 2026-07-31 from a vocabulary fix to a classifier collapse, because the vocabulary confusion turned out to be a symptom. schedule.py runs FIVE scheduling classes on one ladder (spine-serial, protected-serial, single-wi, ordinary, unclassified) and uses that one ladder for two different jobs: _GATE_RANK makes the class decide WHO GOES FIRST while classify() makes the same class decide WHAT MAY SHARE THE STATION. That conflation is why protected-serial and single-wi look like different things when both simply mean run alone, and why a critique is stuck serial although nothing about a critique touches product code. SPLIT INTO TWO INDEPENDENT AXES: concurrency (exclusive|parallel, derived from the declared kind) and rank (an integer, low first, then Priority, then downstream count, then hard-path length, then id). The table: spine = exclusive rank 0, opens a re-attest window, runs a bar; adjudication = exclusive rank 1, NO bar; attestation/gate = exclusive rank 2, closes a window, no bar; protected = exclusive rank 3; high-risk and PlanMode=dual = exclusive rank 4; critique = PARALLEL rank 5, no bar; ordinary = parallel rank 6. Missing or structurally-contradicted stays unclassified and fails closed. WHAT THIS DELETES: SCHED_PROTECTED, SCHED_SINGLE_WI and SCHED_SPINE_SERIAL collapse into one exclusive value, _GATE_RANK becomes the rank axis it was pretending to be, and opens-a-window stops being inferred from the concurrency class. CARRIES THE SESSION-GROUPING DISPOSITION, NOW RULED - session grouping is REMOVED, not wired: with lanes, packing two WIs into one session is strictly worse than two lanes (same throughput, worse attribution, and the coupling the recorded 19 reservations -> 8 integrations -> 0 gate-verified history already indicts), so classify()'s packing distinction, the section 7 continuation guard and the exit-10 ASSIGNMENT-END arm all delete. agent_loop --wi 'WI-201;WI-204' SURVIVES with exactly one caller left: the dispatcher admitting the spine batch (WI-381), the one case where N WIs genuinely must share one window and one owner sitting. And critique going parallel is safe precisely because single-wi no longer prevents anything - the packing it was drawn against is gone. RE-AFFIRMED 2026-07-31 against the concurrency-v2 §A9.1 addition (the program-close row WI-390): that section adds a NEW row's scope - the spine amendment, connectivity, prose and stamps that no single builder can own - and changes nothing in this row's own scope, so this row stands as written."
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
needs = ["~WI-386"]
+++

## Deliverable

The classifier no longer answers two questions with one word. `schedule.py`
carries **two tables keyed by the same declared kind** — `_KIND_CONCURRENCY`
(`exclusive` = runs alone | `parallel`) and `_KIND_RANK` (an integer, low
first) — and `classify()` returns `(concurrency, rank, reasons)`. §A1's ruled
numbers are written verbatim: `spine` 0, `attestation`/`gate` 2, `protected` 3,
`high-risk`/`PlanMode=dual` 4 exclusive; `critique` **5 and parallel**,
`ordinary` 6. Rank 1 is a documented gap for the `adjudication` kind WI-388
adds, so that row adds a mapping instead of renumbering a ruled table.

`SCHED_SPINE_SERIAL`, `SCHED_PROTECTED` and `SCHED_SINGLE_WI` are gone,
collapsed into the one `exclusive` value they always meant. `_GATE_RANK` is
gone; `order_key` takes the RANK, not the classification, so the concurrency
axis is not in the ordering decision. **That is a convention, not a structural
guarantee** — round 1 of REVIEW-A drove `order_key(w, concurrency, …)` past the
whole suite with byte-identical counts while genuinely reordering the frontier,
so the claim is retracted and replaced by a test that convicts that edit (see
below). `is_schedulable_class` → `is_schedulable`, and a quarantine refuses BOTH
axes (`CONCURRENCY_UNCLASSIFIED`, `RANK_UNCLASSIFIED`), never one.

Session grouping is **removed, not wired** (§A6.1): the §7 continuation
re-check, the `exit 10 ASSIGNMENT-END` arm, `EXIT_TRAIN_END` itself, the
worker's `sched` scheduler view and `agent_loop`'s `schedule` import all
deleted. `agent_loop --wi 'WI-201;WI-204'` survives for its one remaining
caller, the dispatcher admitting the spine batch. `agent_loop.py` 3026 → 2973
lines and `run_iteration` 23 → 20 complexity, both ratchets re-stamped
downward.

**Deviation:** the `checkpoint` classifier input was deleted as well. §A1's
ruled table does not name it, `load_wis` never emitted the key (so it was
reachable only from hand-built dicts), and its entire meaning was "do not pack
me" — with packing gone it prevents nothing.

**Two axes, pinned independently** — each pin mutation-proved, because round 1
found two that could not fail:

- Rank 4 (`high-risk`) and rank 5 (`critique`) are adjacent and land on opposite
  concurrency values → rank does not determine concurrency.
- The five exclusive kinds hold four distinct ranks → concurrency does not
  determine rank. Read off `sched._KIND_CONCURRENCY`/`_KIND_RANK`, not off the
  test file's own copy of §A1, so the mutation that makes concurrency fully
  determine rank reds this pin (it did not before).
- A `Priority`-driven reorder leaves every concurrency answer untouched.
- **The ordering axis is pinned at its call site**: a frontier whose leading run
  is four kinds sharing one concurrency value and holding ranks 0/2/3/4. Feed
  the concurrency string to the sort instead and all four tie, dropping the
  spine WI from first to fourth. Nothing hands `order_key` a literal.

The reserved rank-1 gap has its own test. `tests/test_schedule.py` constructs
every registry it reads (40 tests, all in-process).

**Naming.** The emitted record key is `exclusive_keys`, not `exclusive`: the
`Exclusive` COLUMN is a set of named mutex keys and has nothing to do with the
`exclusive` CONCURRENCY value, and leaving two ideas one word apart in the
module whose whole diagnosis is an overloaded word would have been the same
mistake twice. Stated at the axis header, at `_exclusive_conflicts`, in the
module docstring, and asserted on the wire.
