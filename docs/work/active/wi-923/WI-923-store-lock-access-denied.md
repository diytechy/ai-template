+++
id = "WI-923"
title = "A runtime-store lock contender that Windows refuses as access denied, while the lock is being deleted, waits or is refused instead of crashing"
workstream = "process"
sr_refs = ["SR-227"]
buildtier = "quick"
safety_class = "ordinary"
priority = 5
specref = "docs/specs/WI-923.md"
planmode = "single"
needs = []
+++

## Context

Filed on trunk on 2026-10-15 by the attended coordinator (coordinator-2026-10-15
D-004), from a load-sensitive red in the smoke tier: on Windows, the runtime
store's lock treats only an exists error as a held lock, so a contender that
meets the holder's in-progress delete crashes on an access-denied error. What
failed, the cause in the code and the probes that confirmed it are its spec
of record, `docs/specs/WI-923.md`.

## Deliverables

One lane, one landing.

1. **The create's outcomes, read once at the primitive**
   (`session_keep.py`, `_try_lock` and `dir_lock`; shipped, so a RESYNC
   entry). The exclusive create has four outcomes, each with one reading:
   - **created:** the lock is the caller's (as today);
   - **refused as existing:** held, and the stale rule applies (as today);
   - **refused as access denied:** held, and retried within the wait like
     an existing lock. On Windows this is a name whose delete is in progress.
     On POSIX it is a permission fault, and the retries cost only the pauses.
     `kitlib/observation.write_atomic` already takes this shape for a
     Windows-transient `PermissionError`, with no platform branch;
   - **any other refusal:** raised as itself, at once (as today).

   Past the wait, a lock still held raises `StoreBusy`, as today. When the
   last refusal was access denied, the `StoreBusy` message says so beside the
   lock path (Q1).

   No caller changes. `keep_for`, `_apply_now`, `take_warm_lease` and
   `coordinator_guard`'s sites already handle `StoreBusy`.
2. **Contract text** (shipped, same entry). IF-273's contract body in the
   module docstring, and `dir_lock`'s docstring, state the four outcomes and
   the deadline rule.

## Done-when

- **Tests** (`tests/test_session_keep.py`, smoke tier). None uses a thread
  or depends on timing; the retry's pause may be stubbed. Each injects at the
  lock's exclusive create only, so a record write's own file creates are
  untouched.
  - The create refuses once as access denied (`PermissionError`, errno
    `EACCES`), then behaves normally. `dir_lock` takes the lock, yields and
    releases it, and nothing escapes. This fails on trunk's code.
  - Every create refuses as access denied, with the wait already spent.
    `dir_lock` raises `StoreBusy`, whose message names the lock path and the
    access refusal. This fails on trunk's code.
  - The create refuses with another error (for example `ENOSPC`). The error
    is raised as itself after one attempt, not as `StoreBusy`. This passes
    before and after, and pins the default.
  - The observed path. A route's first call takes the lease. A second first
    call, with `lease_wait` 0, has its first lock create refused as access
    denied. It runs unretained and names why ("runs unretained" on stderr),
    and the store still holds only the first call's lease. This fails on
    trunk's code, where the `PermissionError` escapes `keep_for`.
- TC-329's `test_two_concurrent_first_calls_mint_one_session_and_run_one_unretained`
  and TC-317's `test_the_store_lock_excludes_a_second_holder` pass unchanged,
  in the smoke tier at `-n auto`.
- **A stress run on Windows**, recorded in the lane log. Several threads take
  and release the real `dir_lock` for 10 s. On the change, no exception
  escapes and no two threads hold the lock at once. On trunk's code,
  `PermissionError`s escape. The harness is a scratch script, not a suite
  test.
- **The change's trace rows** are authored in the lane and, where their text
  changes, sat at its checkpoint:
  - IF-273's contract body in the code states the rule (deliverable 2);
  - TC-267's method and expected gain the primitive cases: a lock create
    refused as access denied is retried as held, one refused so to the
    deadline is refused as busy and named, and any other refusal is raised.
    Its `verifies` gains IF-273, and its evidence names the three tests;
  - TC-329's method gains the observed-path case, and its evidence names the
    test;
  - LLR-270's STORE paragraph gains the rule in one clause, in behaviour
    voice and naming no code, only if the sitting reads it as design the row
    does not already carry;
  - SR-227 is unchanged. It already requires a held session to be waited on
    and then run unretained, stating why, and the retention state to be
    written by one writer at a time.
- `RESYNC_PACK.md` carries one entry for `session_keep.py`, anchored at the
  landing's parent. The store and lease lock reads an access-denied create as
  held. A persistent access fault on the lock now ends in `StoreBusy` after
  the wait, naming the fault, instead of an immediate `PermissionError`. No
  forced migration.
- The bar is green on the landing tip:
  - the smoke tier within its budget;
  - `check_trajectory.py --strict` clean;
  - `trace.py --strict` with no finding beyond LLR-292's, or none once
    WI-914 has landed.

## Scope answers

- **S1:** one landable unit. The reading, its contract text and its tests
  are one change: the tests are red without it, and the text is false
  without it.
- **S2:** no. The lock file's authority over the store's and the lease's
  writers is LLR-270's and LLR-300's, and is unchanged. This row changes how
  the primitive reads one refusal of its own create. No file's content is
  read, and no file gains authority over a hold, an act or a gate. So no
  `## Trust` section.
- **S3:** closed by enumeration, with a declared default. The create has four
  outcome classes, and each has one reading (deliverable 1); any other
  refusal is raised, as today. The deadline rule has one reading too: held
  past the wait raises `StoreBusy`, naming an access refusal when that was
  the last. Both platforms are covered: on Windows the refusal clears within
  the release, and on POSIX it is a fault, refused as busy after the wait and
  named.
- **S4:** `single`. The row promises behaviour over an input space: the
  exclusive create's four outcome classes, read on Windows and on POSIX
  (S3). That alone is enough, however cheaply each outcome is tested. The
  row has no Trust section, edits one script family (`session_keep.py`)
  and changes one seam's contract text (IF-273).
- **Architectural delta:** none. No state, domain value, input or boundary is
  added. One more create outcome maps to the existing held state.
- **B3 and B4:** the reading uses only the create's own answer at that
  moment and recomputes nothing from history. No Done-when item needs an
  owner act or credential.
- **Dependencies:** no `needs`.
  - wi-798 (active) rewrites much of `session_keep.py`, including the IF-247
    docstring paragraph next to IF-273's, and its tests. It does not touch
    `_try_lock` or `dir_lock`. Whichever lands second rebases.
  - WI-906 (queued) handles `StoreBusy` at the coordinator lease's hook sites
    on the same primitive. Neither row needs the other. After this row, a
    transient access refusal there no longer reaches WI-906's paths.
  - WI-800 (queued) re-homes the store and inherits the primitive.
  - No third-party dependency.

## Calls ruled at filing

The owner ruled the drafter's one call in session, as recommended
(2026-10-15); coordinator-2026-10-15 D-004 records the filing.

- **Q1: what a persistent access refusal reads as.**
  - **(a) Ruled:** held to the deadline, then `StoreBusy`, naming the
    access refusal. This keeps IF-273's one failure ("raises StoreBusy when
    the lock stays held past `wait`"). Every caller already handles that
    failure safely, and it is `write_atomic`'s no-branch shape. Residue:
    when a store directory refuses writes, `keep_for` reports "held by the
    store lock" for `lease_wait` and then runs unretained, because its line
    does not carry `StoreBusy`'s text. That needs a fault on an untracked
    per-clone directory the same user created, which is improbable.
  - **(b) Not taken:** at the deadline, re-raise the `PermissionError` when no attempt
    found the lock existing. This is more honest about the fault, but it adds
    a deadline-time discriminator. A contended lock whose last attempt hit
    the delete window would then crash at the deadline.
  - **(c) Not taken:** read access denied as held on Windows only, and raise it at once
    elsewhere. This adds a platform branch for a reading (a) already makes
    harmless on POSIX.
- **Considered and not taken: releasing by rename.** Moving the lock's name
  away before deleting it removes the window at its source (the third probe
  met no refusals). But it leaves the create's assumption false for the other
  deleter, the stale takeover, and for a person. It adds a second name per
  release. The create-side reading is the one owning boundary, and the
  injected test holds the change to it.

## Critique dispositions

Round 1 (Codex Sol, medium, 2026-10-15; CHANGES-REQUESTED, one finding):

- **S4, MAJOR: adopted.** `planmode = "single"`, and S4 now reads: "The
  row promises behaviour over an input space: the exclusive create's four
  outcome classes, read on Windows and on POSIX (S3). That alone is enough,
  however cheaply each outcome is tested."

Round 2 (Codex Sol, medium, 2026-10-15; a confirming round in convergence
stance): APPROVE, no findings; the adoption confirmed in the spec as quoted.
