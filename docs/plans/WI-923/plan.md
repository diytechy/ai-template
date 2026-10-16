# WI-923 plan: a store-lock create refused as access denied is read as held, retried within the wait, and refused as busy and named past it

Spec: `docs/work/active/wi-923/WI-923-store-lock-access-denied.md`. Its specref, `docs/specs/WI-923.md`, is the spec of record: the observed failure, its cause in `_try_lock` and `dir_lock`, and the three probes that placed the Windows window. The owner ruling the spec relies on is Q1 (a), under "Calls ruled at filing": a persistent access refusal is held to the deadline, then raises `StoreBusy` naming it. coordinator-2026-10-15 D-004 records the filing.

The item's SR is SR-227 (`docs/requirements/system-requirements.toml`), and this row leaves it unchanged (D13). Twelve TCs verify it (`docs/test/test-cases.toml`): TC-266, TC-267, TC-268, TC-303, TC-321, TC-322, TC-323, TC-324, TC-329, TC-330, TC-341 and TC-351. P1 and P4 amend TC-267 and TC-329. The Excludes line at the end gives the reason for the other ten. TC-317 verifies IF-273 but not SR-227; P1 names it because D6 runs its store-lock test.

Line numbers refer to `project-trajectory/scripts/session_keep.py` at the lane's trunk base, `4c216fd2f`.

## Steps, in build order

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | The create's four readings and the deadline rule in `_try_lock` and `dir_lock`, their contract text, four smoke tests written red-first, and the two TCs' evidence cells | D1; D2; D3; D4; D5; D6; D9; D10; D11; SR-227; TC-267; TC-329; TC-317 | IF-273 (its contract text gains the readings and the deadline rule; its signature, its yield and its one failure stay); IF-248 (keep_for, unchanged, which the observed-path test drives); IF-247 (the record that test reads) | |
| P2 | The Windows stress run: the real dir_lock under six threads for 10 s, on trunk's code and on the change, recorded in the lane log | D7; SR-227 | IF-273 (the harness takes and releases the real primitive through its contract) | P1 |
| P3 | The RESYNC_PACK.md entry for session_keep.py, with no forced migration | D14; SR-227 | IF-273 (the entry states its changed reading for adopters) | P1 |
| P4 | The trace rows: Terra drafts TC-267, TC-329 and the conditional LLR-270 clause at intent, and one combined sitting judges them at the checkpoint, which ends with the act | D8; D10; D11; D12; D13; SR-227; TC-267; TC-329 | IF-273 (TC-267's verifies gains it) | P1 |
| P5 | The lane's tip made final (rebased if trunk moved, entry re-anchored, row closed, bar green), then the fresh full-lane gate over that tip | D14; SR-227 | no interface: the rebase, close, bar and gate cross no code seam | P2; P3; P4 |
| P6 | The landing: the gated tip squashed onto the trunk commit it was gated on, the trunk-only views regenerated, the bar run on the landing tip | D15; D16; D17; D18; SR-227 | no interface: the squash, regeneration and bar cross no code seam | P5 |

DELTA: none

**Clauses covered by two rows, each split stated.**

- **D10:** P1 writes TC-267's evidence (the three primitive tests) together with the tests, because TC evidence is a trace field the builder keeps current on each commit. P4 writes its method, expected and `verifies`, and the checkpoint sits them.
- **D11:** P1 writes TC-329's evidence (the observed-path test). P4 writes its method, and the checkpoint sits it.
- **D14:** P3 writes the entry, anchored at the lane's trunk base. P5 sets its final anchor: the trunk commit P6 lands on.

**Architectural delta: none.** The four questions, answered against the code at the base:

- **Does it add a state?** No. The lock is free or held, as before, and an access-denied create maps to held. No record field, file, lock name or setting is added.
- **Does it add a value to a domain?** No. At its seam the primitive still has three outcomes: it yields the directory, it raises `StoreBusy` past the wait, or it raises any other `OSError` at once. What changes is where one refusal lands: a `PermissionError` moves from "raised at once" to "held". The three-way reading that `_try_lock` hands `dir_lock` stays inside the module.
- **Does an output depend on a new input?** No. `StoreBusy`'s message gains the access refusal, read from the same create the primitive already makes, at that moment. Nothing is read from history, from a file's content, or from a clock beyond the existing deadline.
- **Does it cross a new boundary?** No. The change stays in `_try_lock` and `dir_lock`. No import, caller, seam or file is added. IF-273's row keeps its cells; only its contract text in the code gains the rule (P1).

So no row carries an architecture change, and no refactor is owed.

**Scope answers the plan keeps** (the spec's S2 to S4, B3 and B4):

- **S2:** no file gains authority over a hold, an act or a gate. The change reads one answer of its own create, never a file's content, so the spec has no Trust section and the plan adds none.
- **S3:** the input space is closed by enumeration, with a declared default. There are four create outcomes (created, existing, access denied, any other), one deadline rule, and both platforms (P1).
- **S4:** `single` holds. The row promises behaviour over that input space.
- **B3:** the reading uses only the create's answer at that moment (C3).
- **B4:** no Done-when item needs an owner act or credential. D7 needs only the Windows box the coordinator runs on.

## P1: the create's readings and the deadline rule (deliverables 1 and 2)

**Today, at the base.** `_try_lock` (lines 312 to 325) makes the exclusive create at line 315 and reads only `FileExistsError` (line 316) as the lock held. `dir_lock` (lines 290 to 309) retries only that. Any other refusal escapes `dir_lock`, `store_lock` (line 286) and every caller. Windows refuses the create as access denied while the holder's delete of the name is still running. The contender then crashes whichever caller it serves:

- `keep_for`, which catches only `StoreBusy` (line 1261);
- `_apply_now` (line 864);
- `take_warm_lease` (line 1743);
- a coordinator-guard hook or command.

**The change.** It touches only `_try_lock`, `dir_lock`, `dir_lock`'s docstring and the module docstring's IF-273 paragraph.

- `_try_lock` stays the one reader of the create's answer and reads each of the four outcomes one way:
  - **created:** the lock is the caller's, and the pid is written, as today;
  - **refused as existing** (`FileExistsError`): held, and the stale rule runs as today, so a lock older than two minutes is unlinked and a later attempt can take it;
  - **refused as access denied** (`PermissionError`, C1): held, and nothing else is done (C2);
  - **any other refusal:** it propagates from `_try_lock` unchanged, at once.
- `_try_lock` returns which of its three readings it made: the lock is ours, held as existing, or held as access denied. The builder names the shape. One fitting shape is `None` when the lock is ours, and otherwise a short text saying why it is held: empty for an existing lock, and the refusal's own text (errno and strerror) for an access-denied create. No function but `dir_lock` sees this return.
- `dir_lock` keeps its loop, its 0.05 s pause and its deadline. It retries both held readings alike and remembers only the last one (C3). Past the deadline it raises `StoreBusy`. The message is the lock path, as today, followed by the access refusal when the last reading was access denied. One example: `<directory>/.lock (last create refused as access denied: [Errno 13] Permission denied)`. The builder chooses the words. The test anchors only on the lock path and the words `access denied`.
- No function, import or caller is added or changed:
  - `keep_for`, `_apply_now` and `take_warm_lease` already turn `StoreBusy` into their documented outcomes, and `store_lock` passes it through;
  - coordinator_guard's twelve `dir_lock` sites are unchanged. A `StoreBusy` there ends as it does today (WI-906 owns it). A transient refusal no longer reaches them.
- **Contract text (D9).** IF-273's paragraph in the module docstring keeps its sentence verbatim and gains the four readings and the deadline rule. `dir_lock`'s docstring states the same in its own words. `store_lock`'s ("Raises StoreBusy past `wait`.") stays true and unchanged. The registry row IF-273 keeps its cells. A draft of the paragraph's addition: "The exclusive create is read once. Created, the lock is the caller's. Refused as existing, it is held and the stale rule applies. Refused as access denied (a `PermissionError`, which Windows returns while a holder's delete of the lock is still running), it is held and retried within `wait` like an existing lock. Any other refusal is raised as itself, at once. Past `wait`, StoreBusy names the lock path and, when the last create was refused as access denied, that refusal."

**Tests (D1 to D5),** in `tests/test_session_keep.py`. The module is not in `SLOW_MODULES`, so it runs in the smoke tier. The tests come first: the builder runs them on the unchanged module (red), then makes the change (green), and reports both runs with their commands (the kit-builder rules).

- **One helper,** beside the store-lock tests: `_refuse_lock_creates(monkeypatch, code, times=None)` wraps `os.open`.
  - It records any call whose path's name is `.lock` and whose flags carry `os.O_EXCL`.
  - The first `times` of those calls, or all of them when `times` is None, raise `OSError(code, os.strerror(code), path)`. Python constructs that as a `PermissionError` for `EACCES`.
  - Every other call goes to the real `os.open`. A record's temporary file is also created exclusively (`tempfile.mkstemp`), but its name is `<stem>…tmp`, so it is untouched, and so is every store marker.
  - It returns the recorded attempts. Every test asserts how many were refused, so an injection that misses cannot pass vacuously on trunk's code.
- **No thread, and nothing depends on timing.**
  - The retry pause is stubbed with `monkeypatch.setattr(keep.time, "sleep", lambda s: None)`, as an existing test in the module already does.
  - Tests 1 and 4 keep the default 10 s wait, which one instant retry never approaches.
  - Test 2 passes `wait=0`, where the deadline has passed by construction, because `time.monotonic` never goes back.
  - Test 3 refuses once and then lets the create through, so a wrong retry shows up as a missing exception, never as a wait.
- **The four tests,** each with what it does on trunk's code:
  1. `test_a_lock_create_refused_once_as_access_denied_is_retried_and_taken` (D2). One `EACCES` refusal, then normal. Inside `with keep.dir_lock(tmp_path / "store")` the lock file exists, and after the block it is gone. There are two attempts, one refused, and nothing is raised. **On trunk:** fails, because the `PermissionError` escapes `dir_lock`.
  2. `test_a_lock_create_refused_as_access_denied_past_the_wait_is_busy_and_named` (D3). Every create is refused `EACCES`, with `wait=0`. `dir_lock` raises `StoreBusy` after one attempt, and its message contains the lock path and `access denied`. **On trunk:** fails, because a `PermissionError` escapes where `StoreBusy` is expected.
  3. `test_any_other_lock_create_refusal_is_raised_at_once` (D4). One `ENOSPC` refusal, then normal. `dir_lock` raises that `OSError` (errno `ENOSPC`, not `StoreBusy`) after one attempt, and makes none of the later creates the injection would allow. **On trunk:** passes. It pins the default.
  4. `test_a_first_call_whose_lock_create_is_refused_as_access_denied_runs_unretained` (D5).
     - `_keep(tmp_path, ON)` takes the route's lease and writes a lease-only record.
     - The injection then refuses one create `EACCES`.
     - A second `_keep(tmp_path, ON, lease_wait=0)` returns None.
     - stderr says `runs unretained` and names the first call's holder. That shows the retried create took the store lock and met the lease.
     - The store holds one record, still lease-only and leased to the first call, and no marker.

     **On trunk:** fails, because the `PermissionError` escapes `keep_for`.
- Tests 1 to 3 go after `test_the_store_lock_excludes_a_second_holder`, in the TC-267 store section. Test 4 goes after the TC-329 first-mint tests. `errno` and `os` join the module's imports.
- **D6.** Two existing tests stay byte-identical: the diff touches no line of TC-329's `test_two_concurrent_first_calls_mint_one_session_and_run_one_unretained` or TC-317's `test_the_store_lock_excludes_a_second_holder`. Both pass in the smoke tier at `-n auto`, in the coordinator's re-run of the commit bar. The builder's own runs use `-n 2` (its rules). TC-317's row is not amended: it already verifies IF-273, at the Full tier.

**Trace fields, written with the tests.** TC-267's evidence gains tests 1 to 3, and TC-329's gains test 4. Each is appended to its cell by a guarded replace (recipes §5). No function is added, so no `Implements:` tag or `code_symbol` entry changes. LLR-270's `code_symbol` already lists `dir_lock`. Proposed row text goes on the lane's spine change list for P4.

**Done when:**

- the red and green runs above are recorded;
- the touched modules (`tests/test_session_keep.py`, `tests/test_coordinator_guard.py`) and the smoke tier are green;
- `check_trajectory.py --strict` is clean;
- `check_complexity.py --report` reads 15 or below for both functions;
- ruff format and ruff check are clean.

The coordinator re-runs the claimed results and the commit bar before committing.

**Iteration** (coordinator-cycle §3). The lane's first review is a full-scope Sol review of this build. Each fix round:

- answers its round file with a coverage plan first;
- confirms each finding on the real code path before changing anything;
- gets a narrow review.

A contested finding goes to a dispute sitting. A fix round's behaviour change folds into P3's one entry.

## P2: the Windows stress run (D7)

The harness is a scratch script, never in the lane: `stress_dir_lock.py`, under the coordinator's dated scratch root (session-protocol §3). It runs with `C:/Projects/ai-template/.venv/Scripts/python.exe` (3.11.9) on the Windows box.

- **Method.**
  - It takes three arguments: `--scripts <dir>` (the `project-trajectory/scripts` to import `session_keep` from, so one script measures both codes), `--threads 6` and `--seconds 10`.
  - It makes a fresh temporary directory outside every checkout.
  - Each thread, until the deadline, takes and releases the real `dir_lock` on that directory with the default wait. Inside the lock it increments a shared holder count under a `threading.Lock`, records any count above one as an overlap, and decrements the count on the way out.
  - Every exception is caught and counted by type, and the loop goes on.
  - It prints one line, `holds=<n> overlaps=<n> escaped=<type: count, ...>`, and exits non-zero on any overlap or escaped exception.
- **Trunk's code:** a detached scratch worktree at the lane's trunk base (`git worktree add --detach <scratch>/base-wt <base>`), removed afterwards. Expected: `PermissionError`s escape (the spec's probe saw 106 in about 9,600 holds) and no overlap.
- **The change:** the lane's `project-trajectory/scripts`, once the code has settled (no BLOCKER or MAJOR in the last narrow round). Expected: holds, no overlap, nothing escaped. If a later round changes `session_keep.py`, this reading is taken again.
- **Recorded** in the lane log fragment, `docs/log.d/WI-923-store-lock-access-denied.md`: both summary lines and the harness's parameters. Each line carries its `fig:` marker naming the command and the code's revision (session-protocol §4). `check_doc_refs.py` judges `docs/log.d/` strictly, so the fragment names the harness by its file name, never as a backticked path. The builder runs both readings first, and the coordinator re-runs them before recording.
- **If a run does not show what it should:**
  - a trunk run with no escape is repeated, up to three runs, and every reading is recorded; if trunk never reproduces, that is reported, not claimed;
  - any escaped exception on the change, `StoreBusy` included, is a defect for the build. It is reported with its traceback, and D7 is not claimed.
- Adds no suite test, as D7 requires.

## P3: the RESYNC_PACK.md entry (D14)

The builder writes the entry in the first build round (the kit-builder rules), in `project-trajectory/RESYNC_PACK.md`, after the last entry before §5. Its heading is `### The store and lease lock reads an access-denied create as held [since <the lane's trunk base>]`, followed by the pack's "Anchored at the preceding commit" parenthetical. P5 sets its final anchor.

- **What changed.**
  - `scripts/session_keep.py`'s `dir_lock` is the exclusive-file lock under the retained-session store (`out/adjudicator/.lock`) and the coordinator lease (`out/coordinator/.lock`). It now reads a create refused as access denied as the lock held, and retries it within the wait.
  - Windows refuses that way while the holder's delete of the lock is still running. Under contention that `PermissionError` used to escape every caller at random: a retained call's keep, a finished call's bookkeeping and release, a keep-warm lease, and a coordinator-guard hook or command.
  - A persistent access fault on the lock now ends in `StoreBusy` after the wait, its message naming the access refusal beside the lock path, instead of in an immediate `PermissionError`. On POSIX that fault is a store directory that refuses writes.
  - Any other refusal is raised at once, as before.
- **Kit-owned files — overwrite:** `scripts/session_keep.py`.
- **What to do.** Overwrite the file. No migration is forced: no registry, setting or record format changes. Code of your own that catches `PermissionError` around `dir_lock` or `store_lock` no longer sees the lock's access refusal. It arrives as `StoreBusy`, after the wait.

The lane keeps one entry: a fix round's change folds into it (recipes §3). No test is added. `tests/test_resync_pack.py` (a slow module) runs green after the entry is written, and again after P5's re-anchor.

## P4: the trace rows (D8, D10 to D13; coordinator-cycle §3, intent and checkpoint)

The rows are drafted once against P1's first build and judged once against settled code.

- **Intent, after P1's first build commit.** Terra, in the lane's one retained session, authors the whole change set from the anchor, SR-227, down, with the arms map.
  - Approved rows are amended by addition: each approved cell stays verbatim, and the new text is added in contract voice (recipes §5).
  - The coordinator checks the set mechanically before committing it without a sitting:
    - removing the addition from each changed cell gives the approved bytes;
    - list cells stay lists;
    - the files are UTF-8 with LF line endings.
  - **TC-267 (D10).**
    - Its method gains the primitive cases: a lock create refused as access denied is retried and the lock taken; one refused that way through the wait raises busy, naming the lock and the refusal; any other refusal is raised after one attempt.
    - Its expected gains the reading: an access-denied create is retried as held, one refused that way to the deadline is refused as busy and named, and any other refusal is raised.
    - Its `verifies` gains IF-273. That cell is not among the builder's trace fields, so it is Terra's.
    - P1 wrote its evidence.
  - **TC-329 (D11).** Its method gains the observed-path case: a second first call whose first store-lock create is refused as access denied, with no lease wait, runs unretained naming why, and the store keeps only the first call's lease. Its expected stays, because "no two first calls mint at once" already states that outcome. P1 wrote its evidence.
  - **LLR-270 (D12).**
    - Terra drafts one clause for the STORE paragraph, placed after the sentence on the store lock's exclusive file, in behaviour voice and naming no code. For example: "a create of that file refused as access denied is read as the lock held and retried within the wait, and a lock still held when the wait ends is refused as busy, naming an access refusal when that was the last".
    - The clause is drafted so that the set is closed: TC-267's new expected clause then matches a requirement sentence (recipes §5).
    - The sitting is asked whether LLR-270 already carries this design. If it reads that it does, the clause is reverted to the approved bytes and LLR-270 leaves the act. The arms map then points TC-267's clause at the existing sentences: LLR-270's exclusive-file lock, and SR-227's bounded wait and one writer at a time.
  - **SR-227 (D13).** Unchanged. It already requires a held session to be waited on and then run unretained, stating why, and the retention state to be written by one writer at a time. The set carries it as the anchor. `git diff <the lane's trunk base> -- docs/requirements/system-requirements.toml` stays empty through the landing.
  - IF-273's contract body is code (P1). Sol reviews it; no sitting does, because interface rows carry no approval status.
- **The checkpoint,** once a narrow round has no BLOCKER or MAJOR:
  1. **The latch** (coordinator-cycle §4): the lanes due to land ahead of this one have landed, and this lane has rebased, so its acts and the id watermark pull up.
  2. **Reconcile:** Terra, resumed, reconciles the set against the settled code and the spine change list.
  3. **The closure check:**
     - `trace.py --strict-integrity` and `check_trajectory.py --strict`;
     - arm coverage, judged against the map;
     - each TC expected clause matched to a sentence of an LLR or SR in the set.
  4. **The sitting:** one `combined` sitting, amendment kind only: `amendment:TC-267;amendment:TC-329`, plus `amendment:LLR-270` if it was drafted, with SR scope SR-227. Returns are routed (text to Terra, code to the builder) and re-sat.
  5. **The act:** the amendment act re-attests the blessed rows. It anchors TC-267's and TC-329's evidence, and TC-267's `verifies`, with them. A traced cell changed after the act is re-anchored in the lane as its last spine commit (`intake.py snapshot --approves`, recipes §3).

  P4 ends with the act. The fresh full-lane gate is P5's last step.
- Adds no test. P1's tests are the evidence the amended rows cite.

## P5: the lane's tip made final, then the gate (coordinator-cycle §4; recipes §3; C4)

Everything authored that lands is on this tip before the gate reviews it. In order:

1. **Rebase** onto trunk's tip if trunk moved since P4's latch. recipes §4 sets the merge rules: for RESYNC, both sides' entries, trunk's first; for registries, per table. Then check `acts.toml` for duplicate act seqs. A rebase that changes code or authored rows repeats P4's affected checkpoint, and a duplicate seq retakes the act there.
2. **The trunk-only views** match the base's bytes. They are `PROJECT_STATE.html`, the generated part of `docs/status.md`, `docs/stage`, `docs/open-items.html`, `docs/requirements/components.derived.toml`, `docs/cli-reference.md`, `docs/interface-reference.md` and `docs/reviews/rollup/` (recipes §3). The lane regenerates none of them, so this is a check, and any view that moved is restored.
3. **Re-anchor P3's entry** at the commit the lane now sits on. While trunk holds still, that commit is the landing's parent (D14). `tests/test_resync_pack.py` runs again.
4. **Close the row in the lane,** in its own commit (recipes §3, "Close the row"):
   - `## Deliverable` is filled and placed before `## Context`;
   - `specref = ""`;
   - `spec_move.py` moves the spec to `docs/archive/work/complete/` (never with `--archive`);
   - the spec of record moves to `docs/archive/specs/WI-923.<close date>.md`, because R-F refuses a live spec that no open row cites (D17);
   - if `docs/status.md`'s hand text names the id, the same commit scrubs it;
   - the lane log fragment carries P2's readings and this tip's bar totals, each figure with its `fig:` marker.
5. **The bar on this tip:**
   - the commit bar: the smoke tier timed once and passed to `check_smoke_budget.py --mode enforce --elapsed <s>`, read quiet (recipes §6), plus `check_docs.py --root . --stale`;
   - `check_trajectory.py --strict` clean;
   - `trace.py --strict` with no finding beyond LLR-292's (none once WI-914 has landed);
   - `trace.py --strict-integrity`;
   - `check_complexity.py --mode enforce`;
   - `check_docs.py --root . --strict-orphans`, because the lane adds docs: the plan records, the fragment and the archived spec;
   - two slow modules the smoke tier skips: `tests/test_resync_pack.py` (the pack's anchors) and `tests/test_coordinator_guard_e2e.py` (the primitive's other user, driven through its command line).
6. **The fresh full-lane gate, last.** `review_brief.py review --scope full` runs from the lane's trunk base to this tip, with `--tests tests/test_session_keep.py`, in the reviewer set the coordinator runs. Each verdict is filed as the lane's round file.

**On the gate's verdict.**

- **An APPROVE, or MINORs only:** go to P6. A MINOR the coordinator adopts is either fixed and gated again by another fresh full-lane review, or recorded for a successor. Nothing authored changes after the gated tip.
- **A BLOCKER or MAJOR:** the close is rewound. The lane is reset to the commit before it, and the discarded commit is archived as an extra parent on `archive/lanes`, because the adjudication entry point refuses a sitting on a row no longer under `active/`. The lane iterates, holds P4's checkpoint again if rows change, and runs P5 again.

Adds no test.

## P6: the landing (D15 to D18; recipes §3)

- **Precondition.** Trunk's HEAD is the commit P5 rebased onto, the one the entry names. If trunk moved, P5 runs again from step 1, gate included.
- **Squash** `wi-923` on trunk with `git merge --squash`. The message cites the gate's round files by the names read from disk. There is no `git stash` between the squash and its commit. It is one commit, or two if the lane recorded an owner overrule (recipes §3).
- **Regenerate** with `trunk_step.py --regen`. By hand, that means both `gen_arch_map.py` forms with `--src project-trajectory/scripts`, plus `docs/ratify/CURRENT.md`. `docs/interface-reference.md` then carries IF-273's new contract text (D9). Nothing authored is added.
- **The bar on the staged landing, before the commit:**
  - the smoke tier within its budget (D16): no more than `max-tests` members, and the enforce check under 60 s, re-measured quiet if a loaded reading breaches;
  - `check_trajectory.py --strict` clean (D17);
  - `trace.py --strict` with no finding beyond LLR-292's, or none once WI-914 has landed (D18);
  - `trace.py --strict-integrity` on the staged squash, and `check_complexity.py --mode enforce` on the merged tree (recipes §3).
- **After the commit:**
  - archive the tips to `archive/lanes`, with any rewound close as an extra parent;
  - sweep with `intake.py sweep --merged "WI-923" --branch wi-923 --before <trunk before> --after <landing>`;
  - close the re-mint, citing the act.
- Adds no test.

## Interfaces, components and runtime flows

- **Interfaces** (`docs/requirements/interfaces.toml`):
  - **IF-273** (`scripts/session_keep` to `scripts/coordinator_guard`, CMP-008): its contract text in the code gains the readings and the deadline rule (P1). The row's cells stay, including its `data` ("raises StoreBusy") and `v1`. TC-317 verifies it today, and TC-267 joins it (P4).
  - **IF-248** (the keep call surface): unchanged. `keep_for`'s `StoreBusy` branch now also meets a held access refusal, and `_apply_now` and `take_warm_lease` keep their returns. A transient refusal no longer breaks IF-248's promise that none of the producers raises `StoreBusy` and only a failed publication raises `OSError`.
  - **IF-247** (the record): unchanged. The observed-path test reads it.
  - **IF-272** (the primary checkout's `out/`): unchanged.
  - No IF row is added, and no seam is proposed.
- **Components** (`docs/requirements/components.toml`): CMP-008 (W3 Autonomy) holds `session_keep` and `coordinator_guard`. No component is added or split.
- **Runtime flows** (`docs/runtime-flows.md`): Flow 5 (SR-227, LLR-270) draws the retained keep's planning around a blackout, not the store lock's create, and no flow draws the lock. No flow changes, and every flow's citations stay valid.

## Calls this plan makes that the spec does not settle

These go to the lane's decisions record for the owner to confirm or overrule (coordinator-cycle §5).

- **C1. "Access denied" is read as Python's `PermissionError`.**
  - It is the class D2's test injects and the class `kitlib/observation.write_atomic` already retries.
  - Python raises it for two errnos, `EACCES` and `EPERM`. So an `EPERM` refusal reads the same way: held, then `StoreBusy` naming it after the wait. On POSIX that is a permission fault such as an immutable directory.
  - Reading `EACCES` alone would raise an `EPERM` refusal at once as a `PermissionError`. That is the crash shape this row removes, for a fault the ruled reading (Q1 (a)) already treats as busy after the wait.
  - The tests inject `EACCES`, the code the spec's probes saw.
- **C2. The stale rule is not applied to an access-denied refusal.**
  - The rule ages an existing lock, and an access-denied create names none to age.
  - On Windows the name is already being deleted, by its holder or by a stale takeover, so a second unlink would race that delete. On POSIX the directory refuses writes, so the unlink would fail too.
  - The refusal is retried on the existing lock's pause and deadline, with no backoff of its own.
- **C3. The message reflects the last attempt only,** as the spec says ("when the last refusal was access denied"). Suppose an earlier attempt met the delete window but the last attempt found the lock existing: the message reads as today, the path alone. The loop keeps no other history.
- **C4. The row closes in the lane, before the final gate (P5).**
  - session-protocol §4 orders the close before the final verdict round, and the merge slot counts `docs/work/` in the tree a verdict names. So the gated tip should be the tree that lands.
  - coordinator-cycle §4 step 3 lists "close the row" among the landing's trunk steps. This lane leaves only the squash, the regeneration, the archive and the sweep for trunk.
  - The cost is that a gate finding rewinds the close (R5).

## Risks

- **R1. wi-798 (active) rewrites `session_keep.py` around this lane's edits.** It rewrites the IF-247 paragraph beside IF-273's and the module's tests, and it amends LLR-270 and TC rows for accounts. Whichever lane lands second rebases:
  - the docstring and the tests keep both sides;
  - the registries merge per cell (recipes §4);
  - a same-cell merge in LLR-270's detail or in TC-267's cells repeats the affected checkpoint.

  If the sitting reads LLR-270's clause as already carried, the LLR-270 overlap disappears.
- **R2. The smoke membership ceiling is close.** `docs/stack.ini` declares `max-tests = 2600`. The tier collects 2590 at the lane's base, so this row's four tests make 2594. <!-- fig: cmd="python -B -m pytest -q -m smoke --collect-only -p no:cacheprovider" rev=4c216fd2f -->
  - Lanes landing first add tests of their own.
  - The commit that takes the tier past the ceiling re-stamps it, with its reason, a `fig:` line and a decision (recipes §6). No test leaves the tier to make room.
  - Four in-process tests add next to nothing to the 60 s budget.
- **R3. TC-267's new expected clause needs a requirement sentence** (recipes §5). P4's LLR-270 draft and the arms map carry it either way the sitting reads D12.
- **R4. The stress run depends on load.** P2's repeat rule covers trunk's side. On the change's side, any escape is a defect, never a retry.
- **R5. The gate is taken on a closed tip.**
  - A gate finding rewinds the close (P5).
  - If trunk moves between the gate and the landing, P5 runs again, because the anchor and the rebase change the gated tree.
  - So the coordinator takes the gate only when this row is next to land.
- **R6. Q1's ruled residue.** It needs a persistent access fault, which is improbable: the fault must sit on an untracked per-clone directory the same user created.
  - Under such a fault, `keep_for` waits out its lease wait (120 s by default), with each attempt costing the store lock's 10 s wait, then runs unretained saying "held by the store lock", without `StoreBusy`'s text.
  - A coordinator-guard call waits its 10 s before its `StoreBusy`, where today it fails at once.

  Q1 (a) ruled this residue, and the row does not change it.
- **R7. Cross-platform behaviour.** The code has no platform branch, and the tests inject the refusal, so they run the same on the Linux, macOS and Windows CI jobs. Only P2's measurement is Windows-only, and it is not a suite test.

## Excluded TCs

Excludes: TC-266; TC-268; TC-303; TC-321; TC-322; TC-323; TC-324; TC-330; TC-341; TC-351 — they verify SR-227 arms this row does not change: the off dial, keep-warm, codex compaction, the coordinator route, the retained request's identity, the sign-in probe and its refusal, the long-lived credential, blackout retirement and review scopes. Each is at the Smoke tier, so each runs unchanged in the smoke tier on every lane commit, on P5's tip and on the landing tip.

## Not in this plan

- Q1's ruled residue (R6) stays as ruled.
- WI-906 handles `StoreBusy` at the coordinator lease's hook sites. After this row, a transient access refusal no longer reaches them.
- WI-800 re-homes the store and inherits the primitive unchanged.
- Surfaced while planning, not fixed here: `dir_lock`'s release swallows a failed unlink (lines 306 to 309). That leaves the lock to the two-minute stale rule, so every contender in that window waits out its wait and gets `StoreBusy`. The release is outside the create-side boundary this row owns (the spec's "Considered and not taken: releasing by rename").
