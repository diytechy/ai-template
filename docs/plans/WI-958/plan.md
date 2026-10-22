# WI-958 implementation plan: the loop's review gate and the red-round cap (revision 2)

Planner: a fresh session, read-only over the lane worktree
`C:/Projects/ai-template.wt/wi-958` at `d9b9d30f0`. Sources read: the spec
`docs/work/active/wi-958/WI-958-loop-review-gate-and-red-cap.md`, its specref
(`docs/plans/2026-10-11-review-churn/README.md` §13, precondition 3,
revisions 17, 18 and 20), the closed predecessors WI-956 and WI-957
(`docs/archive/work/complete/`), the code named below, and the round-1
critique `docs/plans/WI-958/critique-1.md`.

## What changed since revision 1, and why

Both critique findings were checked against the plan text and the code
before any change. Both are **confirmed**.

- **F1 (build order, D5's exit-12 assertion): confirmed.** Revision 1's
  `test_red_count_survives_a_resume_and_a_green_resets_it` asserted that the
  resumed run exits `12`, yet P6 removed its mark and only P7 implements
  `red_cap_stop`. P6 would have exposed a red test. Fix: the D5 test is
  split. The P6 half asserts the durable count only (through
  `kverdict.red_rounds`, with an iteration budget that ends the run after
  the red it is meant to make). The exit-12 half is a separate test whose
  mark P7 removes. P7 still depends on P6; no cycle is added.
- **F2 (recovery at the cap): confirmed.** In `agent_loop.py`, `main` calls
  `resume_owed_round(...)` (line 4012) and then `run_loop(ctx)`, whose first
  act is `run_iteration`. Under revision 1, a lane resumed with
  `red_rounds_max` red records already committed (a stop after the
  cap-reaching telemetry commit and before the exit) reached
  `review_draw_gate`'s existing-red-record branch. That branch dropped the
  queue and routed BUILD without committing a new record, so the cap check
  never ran and a further build launched. A green build could then reset an
  exhausted count. Fix (design item 6): the cap decision is also taken at
  the loop's recovery boundary, the top of `run_loop`, before the first
  `run_iteration`. No session of any kind starts before it. The
  post-record check for a newly reached cap stays as it was. A new resume
  test seeded at exactly the cap is added (P7).
  - **Why there is no third call inside the gate's existing-red branch,
    as the critique also suggests.** In a running loop, that branch is
    reached only when a red record already exists for the build commit.
    That record was either written in this process, and its post-record
    check already ran, or it predates this run, and the run-start check
    already ran over it. Neither path can reach the branch at the cap, so a
    third call there would be dead code. The run-start test pins the case
    the critique names.

## The architectural-delta answer

DELTA: within

The WI does all four things the question asks about, and every one fits
inside the families the spec names. None needs a refactor this WI does not
own. The revision changes none of these four answers: the run-start check
reads the same count and returns the same exit.

- **A new state.** A red round. It lives in the lane's committed session
  logs (the record), plus an in-process `RoutingState` flag that drops a
  queued round.
- **A new value in a domain.** It adds three:
  - exit code `12` (`EXIT_RED_CAP`) in the loop's alphabet (IF-015);
  - one new `# phase:` value, `ATTEST`, for the loop's own record of a
    producer run it makes at a review draw (see the design, item 4);
  - two session-log header keys, `bar-red` and `bar-summary`.
- **An output that depends on a new input.** Whether a review is drawn,
  and whether the run starts at all, now depends on the tip's verified
  `review` attestation and the lane's red records (IF-175), and on
  `[build] red_rounds_max` (IF-037).
- **A new boundary crossing.** `agent_loop` becomes a requestor of
  `integrate.attest` (IF-173). `dispatch` reads the red-round count through
  `kitlib/verdict` (IF-175, where it is already a requestor).

No component changes (S5). The interface and domain edits are rows P4–P7
and P9 below.

## Design decisions the build follows

1. **One producer, called as it is.** The loop calls WI-956's
   `integrate.attest(root, train, "review", [])` in-process. Without P8 the
   test set is empty, so the record says `tests=none`. A refusal of any kind
   counts as red (S3: "exit 0 or anything else"), with its refusal text as
   the cause. That includes a red bar, a dirty worktree, hooks off and an
   undeclared `[bars] review`.
   - No second entry point is added. `attest` refuses a branch that the main
     checkout holds (`_lane_off_trunk`). A dispatched worker always runs in
     its lane worktree, so that refusal never fires in a real run.
   - The loop's test fixtures, which today run the worker on the primary
     checkout, move into a linked lane worktree instead (row P2). Adding a
     "checkout-bound" variant of `attest` would have been a second route
     around a refusal (fix-SPOF rule).
2. **The attestation at the event.** In `run_iteration`, after
   `session_commit_range` and before `session_service.record`, the loop
   attests when all of these hold:
   - the session committed;
   - its phase is BUILD, `""` or DESIGN-CHECK;
   - routing is managed and `rp_int >= 1`;
   - every assigned WI carries its trailer (`train_evidence`), which is the
     same condition `schedule_review_round` already checks.

   Attesting before `record` means a red result is written into this build
   session's own log header (`bar-red: <build sha>`, `bar-summary: <one
   line>`), which deliverable 3 asks for. Session logs are append-only
   evidence (`kverdict.log_history`), so this is the one moment the build's
   log can carry the record.
   - **Green:** the empty attestation commit sits on the build commit, and
     the telemetry commit lands above it. Both are record-only, so the review
     walk finds the attestation. `set_train_range` names the attested sha as
     the reviewed commit.
   - **Red:** `committed_build_rounds` keeps `on_committed_build`, skips
     `schedule_review_round`, and sets `worker["rework"]` to the refusal text
     (the bar's failure tail). That is the field a CHANGES-REQUESTED round's
     findings ride into the next build prompt today (`apply_rework_scope`).
   - The critique round is left as it is: the spec gates review only.
3. **One choke point at the draw.** `review_draw_gate(ctx)` runs at the top
   of `run_iteration`, before `routed_session`, whenever
   `st.review_queue` is non-empty. That single check covers fresh rounds,
   post-narrow rounds (`complete_review_round`), resumed rounds
   (`resume_owed_round`) and adjudication rounds
   (`schedule_adjudication_round`). The gate:
   - asks `kverdict.review_attestation(root, HEAD, [])`, the walk through
     record-only commits. If the attestation verifies, the round proceeds.
   - Otherwise it names the build commit as `kverdict.governing_rev(root,
     train)`.
   - If that commit already carries a red record, the gate drops the queue
     (a new `RoutingState.refuse_round()`), routes BUILD next, and puts the
     recorded summary in the rework text. The producer does not run again.
     At the cap this branch is unreachable, because the run-start check
     (item 6) precedes every draw.
   - If it carries no record, the gate runs the producer exactly once and
     records the result (item 4). Green proceeds. Red drops the queue,
     takes the post-record cap check (item 6), and below the cap rebuilds
     with the tail.
4. **Recovery is recorded at the draw, in a log of its own.** A producer run
   at the draw is recorded through the session-record writer the loop
   already uses (`agent_common.write_session_log` +
   `commit_telemetry`).
   - The record is a log whose phase is `ATTEST`. It carries the same
     `bar-red` / `bar-summary` header for a red, and `outcome = GREEN|RED`.
   - Existing logs are never rewritten. The "recorded then" of the Trust
     section is literal.
   - Every reader of `# phase:` is checked to treat `ATTEST` as inert:
     `last_build_family` (BUILD only), `kverdict.review_logs` (review phases
     only), `next_session_number` (counts it, which is correct), and the
     iteration index. A test pins each one.
5. **One count reader, shared by the loop and the dispatcher:**
   `kverdict.red_rounds(root, branch, base) -> RedCount(count, last_summary)`
   in `kitlib/verdict.py`.
   - It finds the newest verified `review` attestation in `base..branch`.
     It then reads every session log those commits added (through
     `log_history`, as the commit that added it), and collects the
     `bar-red` shas that are not ancestors of that green commit.
     **Distinct shas** give the count, so a red recorded twice counts once.
   - A log git cannot show counts as one red, keyed by its path. A history
     git cannot list at all answers `None`, which both callers read as "at
     the cap" (toward the close, never away from it).
   - **Why not `agent_loop.py`, as the spec places it:** the dispatcher's
     close reason must name the same count. `kitlib/verdict` already owns
     the session-log grammar (`session_log`, `log_history`) and the bar
     verifier, and IF-175 already lists both `agent_loop` and `dispatch` as
     requestors. One reader in either module's own file would be a second
     reader for the other. The loop remains the reader's one caller that
     acts on the count. The round-1 critique judged this relocation sound
     ("consumes IF-175 instead of duplicating it"). It stays open to the
     sitting's overrule.
6. **The cap.**
   - `kitlib/config.py` gains `red_rounds_max(root) -> (int, None) |
     (None, refusal)`, the one reader of the key.
   - The ruling: an absent `[build]` table or key reads `3`. An absent,
     unreadable or unparseable file is refused. So is a `[build]` that is
     not a table, naming the line it sits on. A present value that is not
     an int, is a bool, or is below 1 is refused, naming
     `docs/process.toml:<line>` and the key. The line is found by scanning
     the text, because tomllib reports no position for a valid key; its
     parse-error message already carries one.
   - **Two preflights call the reader, both before any session.** The
     worker's is `resolve_session_setup`, which returns `EXIT_PREFLIGHT`.
     The drive's is `dispatch._session_config_refusal`, the pre-claim rung,
     so no lane is claimed and then parked by a worker that can never start.
   - **The worker's cap decision is one helper, `red_cap_check(ctx)`, with
     two callers.** It returns `EXIT_RED_CAP` or `None`. When
     `red_rounds(...)` is at least the max, or is `None`, it writes a
     `RED CAP — N consecutive red rounds` stop banner and returns
     `EXIT_RED_CAP = 12`.
     - **(a) Recovery, at run start (F2).** The first statement of
       `run_loop`, before the first `run_iteration`. It reads the committed
       count only. It runs no producer and starts no builder or reviewer.
       A lane resumed already at the cap therefore ends there, whatever
       `resume_owed_round` queued and whichever recovery branch the gate
       would have taken.
     - **(b) After each committed red record**, at the event (item 2) or
       at the draw (item 4). This catches a cap reached during the run.

     The code is defined in `agent_common` after the retired 10 and
     `RESTART = 11`, and re-exported in `agent_loop`.
   - **The dispatcher** adds 12 to `_WORKER_OUTCOMES`. `_lane_close` then
     calls `handback.close_partial` with typed fields:
     - `reason`: "red bar cap: N consecutive red rounds
       (`[build] red_rounds_max = M`); last bar: <summary>", read through
       `kverdict.red_rounds` at the lane's merge base;
     - `split_decided_by = "adjudicator"`;
     - `suggested_tier = "medium"`;
     - `not_delivered` naming the red bar.

     The drain's existing `_refresh_or_quarantine` then quarantines a lane
     whose landing bar is red, with no new code. Close and quarantine are
     the existing red arm. No new stop (OI-70).
7. **Size budgets.**
   - `agent_loop.py` sits at its SLOC baseline of 2436
     (`tests/test_module_size_ratchet.py`). The gate's call sites are the
     loop's own scheduling arms, so they stay in it as small helpers:
     `attest_build`, `review_draw_gate`, `red_cap_check` and
     `record_bar_result`. `run_iteration` gains one call per arm, and
     `run_loop` gains one, so the complexity ratchet's per-function figures
     hold.
   - The net growth (target: under 90 SLOC) is a reviewed downward-only
     baseline bump, with its reason in `docs/decisions/wi-958.toml`. A new
     module would cost a new IF row and a bootstrap MAPPING row for less
     code than it moves.
   - `kitlib/verdict.py` (635 SLOC), `kitlib/config.py` (185),
     `dispatch.py` (739) and `agent_common.py` (1097 baseline; one constant
     and two header keys, re-stamped if it moves) stay within their budgets.
8. **Out of scope, stated:**
   - Unmanaged mode and review policy 0 draw no reviews, so they attest
     nothing and the cap never arms.
   - A red on an intermediate constituent of a multi-WI train is not
     attested: no round is due, as today.
   - P8's scoped test set.
   - P4's port of this gate across the batch's retirement (S6).

## Plan

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | Spine change set, TC-first (Terra, one dispatch, all `Drafted`). (a) A derived SR, labelled derived, under SN-004/SN-008: "a lane whose build stays red for the declared count of consecutive rounds closes partial, reporting that as its own outcome". Its LLR names `[build] red_rounds_max`, the red record keyed by build commit, the count's reset at a verified review attestation, the cap decision at run start and after each red record, exit 12 and the dispatcher's typed close. (b) The loop's LLR under SR-241: "a loop review is drawn only over a verified `review` attestation; a missing one runs the producer once, red never draws". SR-241's requirement text ("an attended launcher") is amended to name both routes; if the sitting prefers SR-154 as the parent, that is its call. (c) New TCs, one per Done-when group D2–D9, each naming its test module from P3. The D8 TC names the resume-at-the-cap case as well as the in-run cap. (d) TC-082's method gains the attestation precondition. TC-169 is re-read: the cap is a distinct outcome beside the stall, so a new TC carries it and TC-169 keeps its text. | SR-154; SR-144; SR-172; SR-241; TC-082; TC-169; F2 | no interface: registry text only (intra-module) |  |
| P2 | Move the loop's review fixtures onto the real topology, green on today's code. A `conftest` helper `lane_checkout(repo, branch)` adds a linked worktree for the train branch and leaves `main` checked out in the primary (`hooks_on` already reads "on" in a linked worktree). `declare_review_bar(repo, ctl)` writes `docs/stack.ini [bars] review` as a `sys.executable` one-liner that exits 1 when `ctl/bar_red` exists, appends one line to `ctl/bar_runs.txt` per run, and prints `BAR-FAIL-MARKER` on red. `managed_repo` and every loop fixture whose tests assert a review round (`test_agent_loop_review.py`, `_routing`, `_critique`, `_worker`, `test_loop_provenance.py`; the build lists them with a `grep -lE` over `tests/` for the REVIEW-A, review-round and `managed_repo` patterns) return the lane worktree as the run root. `_commit_config` moves `main` with `update-ref`, since `branch -f` refuses a branch checked out elsewhere. Commit only when every touched module is green unchanged. | SR-154; TC-082; TC-084; TC-048; TC-085; TC-257 | IF-015 (the loop run surface the fixtures drive; no seam changes) | P1 |
| P3 | The failing tests, committed alone before any code, each `@pytest.mark.xfail(strict=True, raises=(AssertionError, pytest.fail.Exception))`, plus stubs so every red reaches an assertion: `EXIT_RED_CAP = 12`, a `kverdict.red_rounds` stub returning count 0, and a `kitlib.config.red_rounds_max` stub returning `(3, None)`. Module `tests/test_agent_loop_review_gate.py` is new and registered in `SLOW_MODULES`; its in-process pins are the config and verdict-reader units below. The tests, what each fails on today, and the row that removes each mark are listed under "Named tests". Every exit-12 assertion sits in a test whose mark only P7 removes (F1). | D1; SR-154; SR-144; SR-172; SR-241; F1; F2 | IF-015; IF-175; IF-037 | P2 |
| P4 | `[build] red_rounds_max`: the reader `kitlib.config.red_rounds_max` (the ruling in design item 6, naming file, line and cause) and its two preflight callers (`agent_loop.resolve_session_setup` before any session; `dispatch._session_config_refusal` before any claim). Add `[build]` with a comment block and `red_rounds_max = 3` to `project-trajectory/process.toml.template` and `docs/process.toml`, in matching position; `test_dogfood_sync.py` pins the section in both. The value lands on `LoopContext`. Removes the P3 marks for D7 and D9. | D7; D9; SR-154; SR-172 | IF-037 | P3 |
| P5 | The red record and its count in `kitlib/verdict.py`: the header grammar (`bar-red: <40-hex sha>`, `bar-summary: <one line>`), a pure formatter the loop writes through, a parser, and `red_rounds(root, branch, base)` (design item 5: the newest verified `review` attestation resets the count, distinct shas, an unreadable log counts toward the cap, an unlistable history answers `None`). `agent_common.write_session_log` gains the two header keys in its key order. Removes the P3 marks for the reader-level unit tests of D5 and D6. | D5; D6; SR-154; TC-205; TC-259 | IF-175; IF-065 | P3 |
| P6 | The loop's gate. `attest_build` at the event (design item 2: before `session_service.record`; a red goes into the build log's header and `worker["rework"]`; a green re-points `set_train_range` at the attested sha). `review_draw_gate` at the one choke point (design item 3), with `RoutingState.refuse_round()`. `record_bar_result` writes the `ATTEST` log at a draw through `write_session_log` + `commit_telemetry` (design item 4). The `# phase:` readers are confirmed inert for `ATTEST`. Removes the P3 marks for D2, D3, D4 and the loop-integration tests of D5 and D6. Those tests assert the count and the records only, never an exit code. The exit-12 tests stay marked until P7 (F1). | D2; D3; D4; D5; D6; SR-154; SR-241; TC-082; TC-257; F1 | IF-173 (agent_loop becomes a requestor of `attest`); IF-175; IF-065; IF-246 | P4; P5 |
| P7 | The cap's exit and close. `red_cap_check` (design item 6), called (a) first in `run_loop`, before any session, the recovery boundary for a lane resumed at the cap (F2), and (b) after each committed red record. It writes the RED CAP banner and returns `EXIT_RED_CAP`, which is defined in `agent_common` and re-exported. `dispatch._WORKER_OUTCOMES` gains the code, and `_lane_close` closes the lane partial through `handback.close_partial` with the typed fields (design item 6), reading the count through `kverdict.red_rounds` at the lane's merge base. The drain's existing quarantine handles a red landing bar. Removes the P3 marks for D8 and for D5's exit-12 resume test (F1), and for the at-the-cap resume test (F2). | D5; D8; SR-144; SR-172; TC-138; TC-169; F1; F2 | IF-015; IF-137; IF-175 | P5; P6 |
| P8 | The coordinator's cap text in `coordinator-cycle` SKILL §3, "Rounds, the cap and the convergence round": count each red `integrate.py attest` as a red round in the lane's decisions record, and at `[build] red_rounds_max` consecutive red rounds close the lane partial (recipes §8, "Close a lane partial"). All three copies are byte-identical (`project-trajectory/skills/`, `.claude/skills/`, `.agents/skills/`; the spec says "both", but the tree has three and `test_skills_sync.py` binds all three). Removes the P3 mark for D10. | D10 | no interface: skill text only (intra-module) | P4 |
| P9 | Records. IF-015: its data cell and the `Contract IF-015` body in the `agent_loop.py` header gain `12 RED-CAP` (at run start for a lane resumed at the cap, or after a red record). IF-037's data and its contract body in `docs/process.toml` gain `build`. IF-173's requestors gain `scripts/agent_loop`. IF-175's data and contract body gain the red record and count. Regenerate `docs/interface-reference.md` and the other derived artifacts on the coordinator's landing list. `docs/runtime-flows.md`: Flow 4's decided-exit arm names the red cap, and Flow 1 gains one note that a worker draws review only on an attested tip and checks the cap before its first session. `PROCESS_OPTIONS.md`: one bullet beside REVIEW-OWED for exit 12; check the byte budget with `byte-budget-guard`. One RESYNC entry covers the new setting with its shipped `3` (adopters add the setting only; `process.toml` is never replaced), the new exit code 12 for launchers that read codes, and the kit-owned files to overwrite. Re-stamp the `agent_loop.py` ratchet entry with its reason in `docs/decisions/wi-958.toml`. | D11; SR-154; SR-144 | IF-015; IF-037; IF-173; IF-175 | P6; P7; P8 |
| P10 | Landing. The commit bar is green (`run.cmd smoke`), and `check_trajectory.py --strict` and `trace.py --strict` are clean on the landing tip. The P1 rows are judged at the lane's sitting (the derived SR and the SR-241 amendment among them). The RESYNC entry is anchored `[since <landing parent>]`. The full suite runs once as the gate's bar. TC-371 runs with SR-241's amendment. | D11; SR-154; SR-144; SR-172; SR-241; TC-371; TC-205 | IF-015; IF-037; IF-173; IF-175 | P9 |

Excludes: TC-046; TC-083; TC-156; TC-177; TC-184; TC-331; TC-333; TC-361; TC-362; TC-363; TC-364; TC-365; TC-366; TC-367 — their evidence modules (`test_agent_route`, `test_score_reviews`, `test_handback`/`test_handback_records` admission paths, `test_kitlib_station`, `test_import_layers`, `test_integrate_admission`, `test_review_brief*`, `test_plan_filing`/`test_plan_pass`, `test_accounts`, `test_adjudicator_token`, `test_run_devsetup`, `test_plan_gate`) cover code and fixtures this WI does not change (`handback.py`, `integrate.py`, `agent_route.py`, `score_reviews.py`, `review_brief.py` and the account and plan gates are untouched), so they are neither amended nor newly run; the landing's full suite runs them unchanged.

## Named tests (row P3), and what each fails on today

Every test below lands strict-xfail in P3. The row that removes its mark is
named after the arrow. No test whose mark P5 or P6 removes asserts an exit
code that only P7 produces (F1).

- **`test_red_bar_draws_no_review_records_a_red_round_and_rebuilds_with_the_tail`**
  (D2, removed in P6).
  - Setup: managed fixture, `ctl/bar_red` present, `done_after = 1`.
  - Asserts: no reviewer model in `models.txt`; no `*-REVIEW-A-*.md`; the
    first build's committed log carries `bar-red: <its build sha>`; the
    second build prompt contains `BAR-FAIL-MARKER`.
  - Fails today: the loop draws REVIEW-A right after the first committed
    build, and no log carries `bar-red`.
- **`test_green_bar_attests_once_then_draws_the_review`** (D3, P6).
  - Asserts: exactly one commit in `base..HEAD` carries a `Bar-Green:` line
    that `kverdict.bar_attestation` verifies as `bar=review tests=none`; it
    is older than the REVIEW-A verdict commit; `bar_runs.txt` has one line.
  - Fails today: no attestation commit exists.
- **`test_resumed_round_on_an_unattested_tip_runs_the_producer_once`** (D4,
  P6).
  - Setup: a lane with its WI trailer committed, no attestation and no
    verdict, then a fresh run. Parametrized green and red.
  - Asserts: `bar_runs.txt` has exactly one line. Green: the round is drawn
    and an `ATTEST` log records the result. Red: no reviewer is drawn.
  - Fails today: `resume_owed_round` draws the reviewer with no bar run.
- **`test_post_narrow_and_adjudication_rounds_draw_only_over_a_verified_attestation`**
  (D4, P6).
  - Setup: CHANGES-REQUESTED, then a green rework, a narrow APPROVE and the
    fresh full round. A second case: an ADJUDICATE commit whose
    `schedule_adjudication_round` owes a round.
  - Asserts: every REVIEW log's reviewed sha satisfies
    `kverdict.review_attestation(...)`, and the narrow-to-full transition
    runs no extra bar.
  - Fails today: no attestation exists anywhere.
- **`test_red_count_survives_a_resume_and_a_green_resets_it`** (D5, loop
  half, P6; F1). This is revision 1's D5 test with its exit-code assertion
  moved out.
  - Setup: `red_rounds_max = 5`, so no cap fires. Run 1 makes two reds and
    stops on `--max-iterations`. Run 2, a fresh process, makes one red and
    stops on its own iteration budget. A second sequence: red, green, red,
    red.
  - Asserts: after run 2, `kverdict.red_rounds(...).count == 3`, and run 2's
    first build prompt carries run 1's recorded `BAR-FAIL-MARKER` tail.
    After the second sequence, the count is 2.
  - Fails today: no `bar-red` record is written, so the stub's 0 stands.
- **`test_red_count_survives_a_resume_to_the_cap_and_exits_12`** (D5 and
  D8, worker side, P7; F1).
  - Setup: `red_rounds_max = 3`. Run 1 makes two reds and stops on its
    iteration budget. Run 2, a fresh process, makes one red.
  - Asserts: run 2 exits `12`, with the RED CAP banner naming 3.
  - Fails today: no exit 12.
- **`test_a_lane_resumed_at_the_cap_exits_12_before_any_session`** (D8 and
  D5, recovery, P7; F2).
  - Setup: a lane whose committed logs already carry exactly
    `red_rounds_max` distinct `bar-red` records with no green attestation
    after them, its tip's WI trailer committed (so `resume_owed_round`
    queues a round). This is the state a stop leaves after the cap-reaching
    telemetry commit and before the exit. The red records are made by
    running the loop with `red_rounds_max = 5` for three reds; the key is
    then set to `3` and committed, and the loop is resumed. A second case
    is one record fewer.
  - Asserts, at the cap: the exit is `12` with the RED CAP banner, and
    `models.txt`, `bar_runs.txt` and `git rev-list --count HEAD` are all
    unchanged by the resumed run (no builder, no reviewer, no producer
    run). One record fewer: no exit 12, and the resumed run launches a
    build.
  - Fails today: the resumed run draws the owed reviewer.
- **`test_an_interrupted_red_is_rechecked_once_at_the_draw_and_counted_once`**
  (D6, P5 and P6).
  - Setup: a build commit with no attestation and no record (the crash
    after the red result), then a resume.
  - Asserts: `bar_runs.txt` has one line, and an `ATTEST` log records
    `bar-red` for that sha. In-process, logs carrying `bar-red` for one sha
    twice give `red_rounds(...).count == 1`.
  - Fails today: no recheck, and the stub reads 0.
- **`test_attest_phase_is_inert_to_every_phase_reader`** (D6, P6).
  - Asserts: an `ATTEST` log is skipped by `last_build_family` and
    `kverdict.review_logs`, and is counted by `next_session_number`.
  - Fails today: no `ATTEST` log is ever written. The assertion on its
    presence fails first.
- **`test_unparseable_process_toml_and_a_non_table_build_refuse_at_preflight`**
  (D7, P4).
  - Runs through the worker and through `dispatch._session_config_refusal`.
  - Asserts: exit 2; stderr names `docs/process.toml` and the cause; no
    `models.txt` (no session); no claim commit.
  - Fails today: the loop starts sessions.
- **`test_red_cap_exits_with_its_own_code_and_one_fewer_does_not`** (D8,
  worker side, P7).
  - Asserts: with `red_rounds_max = 2` and two reds, exit 12 and the RED CAP
    banner. With three reds allowed, the same two reds end on the iteration
    budget (exit 6).
  - Fails today: no exit 12.
- **`tests/test_dispatch.py::test_a_red_cap_exit_closes_the_lane_partial_with_typed_fields_and_the_drain_quarantines_it`**
  (D8, dispatcher side, P7).
  - Setup: a stand-in worker exits 12 on a lane whose landing bar is red.
  - Asserts: the `partial/` report's reason names the count and the last
    bar summary; `split_decided_by = "adjudicator"`; after the drain, the
    lane carries the quarantine `.patch`.
  - Fails today: 12 is not a decided outcome, so `_lane_close` takes the
    crash path and the claim stays in `active/`.
- **`tests/test_process_config.py::test_red_rounds_max_reads_3_when_absent_and_refuses_each_bad_value`**
  (D9, P4; in-process, smoke tier).
  - Asserts: an absent table or key reads 3. Each of `0`, `-1`, `true`,
    `"3"` and `3.0` is refused, naming `docs/process.toml:<line>` and
    `red_rounds_max`.
  - Fails today: the stub accepts everything.
- **`test_a_bad_red_rounds_max_refuses_before_any_session`** (D9, P4).
  - Asserts: through the loop's CLI, exit 2, the line named, and no
    `models.txt`.
  - Fails today: sessions start.
- **`tests/test_prompts.py::test_coordinator_cycle_states_the_red_round_cap_citing_the_key`**
  (D10, P8).
  - Asserts: §3 cites `[build] red_rounds_max` and "Close a lane partial".
    `test_skills_sync.py` keeps the three copies byte-identical.
  - Fails today: the text is absent.

## Risks the critic should weigh

- **Fixture churn (P2) is the largest cost.** If moving the loop fixtures
  into a linked worktree breaks a test for a reason unrelated to this WI,
  P2 stops. That is reported, and not worked around with a checkout-bound
  `attest`.
- **The count reader's home** (design item 5) relocates "in
  `agent_loop.py`" to `kitlib/verdict.py`. It is a deliberate call, open to
  overrule.
- **Every loop launch now needs a readable `docs/process.toml`.** The trunk
  reader (WI-925) already requires the file, so no adopter migrates for it.
  The RESYNC entry still says so.
- **The run-start cap check costs one history read per launch.** It is the
  same `red_rounds` walk the post-record check already makes, over the
  lane's `base..HEAD` range. It runs only when managed with `rp_int >= 1`,
  the only mode in which the cap arms.
