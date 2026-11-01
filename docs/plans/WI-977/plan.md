# WI-977 implementation plan: one work item per lane

Spec: `docs/work/active/wi-977/WI-977-one-work-item-per-lane.md` (specref:
`docs/plans/2026-10-11-review-churn/README.md` §15, the owner's revision-25
ruling). Lane: `wi-977`. The base is trunk `a1984f739`. Three-way reads for the
spine use ancestor `607cf609` (A), `contract_split` tip `961f9e47` (CS) and
this branch (H). Both commits resolve in this clone.

Item SRs: SR-144, SR-148, SR-156 (all amended); SR-026 (LLR-061's parent,
unchanged). Registries: `docs/requirements/system-requirements.toml`,
`docs/requirements/low-level-requirements.toml`, `docs/test/test-cases.toml`,
`docs/requirements/interfaces.toml`, `docs/requirements/components.toml`, and
`docs/runtime-flows.md` (the authored flows).

## Architectural delta

DELTA: none

The row adds no state, adds no value to any domain, makes no output depend on a
new input, and crosses no new boundary. It removes a value instead: `batch`
leaves the admission table's domain, and a lane's assignment narrows from an
ordered list to one id. The new refusals reuse exit paths that already exist:
the claim's nonzero refusal (IF-080 "nonzero exit on any refusal, with the
reason named"), the worker's preflight exit 2 (IF-015), the dispatcher's
existing "a composed part's refusal stops the run" path, and the closes'
`(None, refusal)` return (IF-137). I checked every interface row whose data
could name a symbol this row changes: IF-065, IF-093, IF-099, IF-136, IF-137,
IF-154, IF-173, IF-175, IF-194, IF-260 and IF-303. None names `parse_wi_list`,
`mechanical_close_order`, `assignment_block`, `open_claimed_specs` or
`claim_subject`. IF-154's `claim --wi --branch` already names one value, and
IF-099's `WORKER` row names the prompt, not its slots. So no IF or CMP row
changes, which matches spec S5. The worker template's `{assignment_block}`
slot is removed, and IF-099 makes the prompt non-overridable, so no adopter
holds a copy of the slot.

Re-answered for revision 2: still `none`. F1's fix reorders steps and moves
callers between steps. It adds no state, no domain value, no new input and no
new boundary. The one signature tightened beyond revision 1, the composer's
`TypeError` on a non-str, narrows an existing value's domain. It does not add
to it.

## Revision 2: what changed and why (critique-1 F1)

I checked F1 against the lane's code at `c3bd0d50c`. It is **confirmed in its
conclusion and refuted in one premise**:

- **Refuted premise.** In revision 1's order, a scalar id did not make `claim`
  iterate characters. `integrate.claim` normalizes a str today
  (`wi_ids = [wi_ids] if isinstance(wi_ids, str) else list(wi_ids)`,
  integrate.py:821), and so does `ac.claim_subject` (agent_common.py:1176). A
  dispatcher passing one str between revision 1's W3 and W4 claims correctly,
  and about 40 test callers already pass a str.
- **Confirmed defect 1: the claim edge.** Revision 1's W3 and W4 both hung off
  W2 alone, so building W4 first was allowed. That order leaves the dispatcher
  (dispatch.py:1119) passing its `batch` list into the newly refusing claim, and
  every dispatcher-driven test goes red. A real edge fixes it: the dispatcher
  moves to a str first (new W4), then the claim refuses lists (new W5).
- **Confirmed defect 2: the composer edge.** `station.mechanical_close_subject`
  does NOT normalize (`", ".join(wi_ids)`, station.py:146). Revision 1's W8 gave
  it a scalar before W9 changed the signature. That writes `W, I, -, 4, 0, 1`,
  which reds `test_handback.py:850` and stops the attestor's recomposition
  (verdict.py:829) from matching, so the close stops peeling.
- **A third instance F1 did not name.** `_launch` has two live callers. The
  fresh claim (dispatch.py:1125) passes `batch`. The parked resume
  (dispatch.py:1076) passes the full `_claimed_wi_ids` list. Revision 1
  narrowed `_launch` in W3 but fixed the parked caller only in W5, so between
  the two a parked lane handed a list to a scalar seam.

The new order puts each shared signature change into the same step as all of its live
callers, with no compatibility shim and no cycle:

| r1 step | r2 step | Ownership change |
|---|---|---|
| W5 resume | **W3** | Now first. It adds the multi-spec refusal on today's list seam. With one spec left, the list of one goes to `_launch` as today. |
| W3 admission | **W4** | It also narrows the lane seam (`_launch`, `_Lane`, the injected worker, `lane.py`) AND both callers: the fresh claim passes the one admitted id, and the parked resume passes the one id W3's rung guarantees. `integrate.claim` receives a str, which its current contract accepts. |
| W4 claim | **W5** | It depends on W4, so when the claim starts refusing lists, the dispatcher no longer sends one. Every remaining list caller (tests, fixtures, `ac.claim_base`'s re-composition) moves in this step. |
| W8 close | W8 | Its predecessor is now W5. `close_adjudication` moves its one row and calls the composer **under its current list contract** (`[wi_id]`), which is the call its existing test pins today. It drops its own `mechanical_close_order` call. |
| W9 peel | W9 | It owns the composer's narrowing to one id, with every live caller in the same step (handback's writer and re-export, `verdict.mechanical_close`, four test modules). Then it deletes `mechanical_close_order`/`_close_sort_key`, whose last reader (the attestor) changes in this step. |

**Strict-xfail hygiene, which keeps every intermediate step green.** W2's
refusal tests carry `xfail(strict=True)`, so a test turns red the moment its
code passes. Each code step therefore removes the marker from exactly the tests
it turns green, in the same commit: W3 the resume refusal, W4 the admission
pair, W5 the claim refusals and subject test, W6 the worker refusals, W7 the
slot test, W8 the two close refusals, and W9 the no-peel test. A step that
turned green a test whose marker it does not remove would red the bar, and that
is how a mis-ordered step shows up.

## Steps

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| W1 | Spine change set at the intent turn, test cases first | D1; D2; D3; SR-144; SR-148; SR-156; TC-058; TC-061; TC-138; TC-143; TC-144; TC-145; TC-146; TC-154; TC-156; TC-205 | IF-161 (the TC registry the rows land in); no code seam is crossed: these are registry rows only | |
| W2 | Failing tests first, committed alone before any code | D15; SR-144; SR-148; SR-156; SR-026; TC-061; TC-138; TC-143; TC-144; TC-145; TC-146; TC-205 | intra-module: test files only, no seam | W1 |
| W3 | Resume: a parked lane whose claim holds two or more specs stops the run (on today's list-form lane seam) | D8; F1; SR-156; TC-144 | IF-173; IF-136 | W2 |
| W4 | Admission retires the `batch` arm, and the lane seam carries one id: `_launch`, `_Lane`, the injected worker and `lane.py` narrow together with both of their callers (the fresh claim and the parked resume) | D5; D6; F1; SR-148; SR-156; TC-143; TC-144; TC-154; TC-058; TC-137 | IF-053; IF-173; IF-136 | W3 |
| W5 | Claim: one id in, deny-by-default, and the one-id claim subject, together with every caller still passing a list | D7; D13; F1; SR-156; TC-145; TC-139; TC-131; TC-317; TC-370 | IF-154; IF-080; IF-173; IF-065; IF-194 | W4 |
| W6 | Worker: `--wi` takes one id; preflight, assignment and walk read one id | D9; SR-026; TC-061; TC-026; TC-097; TC-257; TC-325; TC-326 | IF-136; IF-065; IF-015 | W4 |
| W7 | Prompt: the multi-row block, its slot and its notes go | D10; SR-026; TC-061 | IF-099; IF-260 | W6 |
| W8 | Close: partial and adjudication closes refuse zero or many specs; the adjudication close calls the subject composer under its current list contract | D11; F1; SR-144; TC-138; TC-156; TC-184; TC-254 | IF-137; IF-173 | W5 |
| W9 | Peel and the composer: one-row mechanical close only; `mechanical_close_subject` narrows to one id with all of its live callers (close writer, attestor, tests); the shared multi-row order goes | D12; F1; SR-156; SR-148; TC-205; TC-132; TC-360; TC-383 | IF-175; IF-303; IF-093 | W8 |
| W10 | Other claimed-set readers: refresh bar, residue and merged counts lose batch wording and arms | D14; SR-148; TC-146; TC-331 | IF-173 | W4; W5 |
| W11 | Ratchets and the leftover batch-test sweep | D15; SR-156 | intra-module: test baselines only, no seam | W3; W4; W5; W6; W7; W8; W9; W10 |
| W12 | Text: the PROCESS_OPTIONS paragraph, README row, headers, runtime flows and concurrency-v2 | D16; SR-148; SR-156 | no interface: prose only | W11 |
| W13 | One RESYNC entry | D17; D18 | no interface: pack prose only (IF-154's argv is unchanged) | W12 |
| W14 | Spine reconcile against the built code and the one checkpoint sitting | D3; D4; SR-144; SR-148; SR-156; TC-058; TC-061; TC-138; TC-143; TC-144; TC-145; TC-146; TC-154; TC-156; TC-205 | IF-161; no code seam: registry rows only | W13 |
| W15 | Generated pages, the commit bar and the strict lints on the landing tip | D19; D20; SR-144; SR-148; SR-156; SR-026 | no interface: regeneration and the bar only | W14 |

Excludes: TC-059; TC-060; TC-091; TC-147; TC-177; TC-183; TC-259; TC-313; TC-314; TC-327; TC-328; TC-369 — each verifies an arm of SR-148, SR-156 or SR-144 that this row leaves alone: kind classification and fail-closed safety class, the trunk-step regen, intake's replay and minting, the import-layer graph (no import is added or dropped), the red-TC census, review scope, ruling sync, OI readiness, the Done-when brief digest, the merge-time goalposts mint, and the trunk-name read. No code path they exercise changes, and the commit bar runs them unchanged.

Two clauses are covered by two rows each, deliberately, because each row does
a different half:
- D3 is covered by W1 and W14. W1 writes requirement cells that name no code.
  W14 makes the traced `module`/`code_symbol`/`evidence` cells follow the code
  as built, which cannot happen before the code exists.
- D15 is covered by W2 and W11. W2 converts or writes every refusal test, red
  first. W11 is the post-build sweep that proves no batch test or batch
  fixture is left, and re-stamps the ratchets the deletions move.
- F1 is covered by W3, W4, W5, W8 and W9 because it is an ordering defect
  across three shared contracts, not one deliverable. W3→W4 orders the
  `_launch` seam after its parked caller's refusal. W4→W5 orders the claim's
  list refusal after the dispatcher's move to a str. W8→W9 orders the
  composer's narrowing after the close writer drops its multi-row loop. Each
  row owns its own edge, and no row repeats another's change.

## Step detail

### W1: the spine change set (intent turn, TCs first)

The spine author (Terra, per the coordinator cycle) authors the whole set once,
before build round 1, in item 13's order: the ten TCs first, then the ten LLRs,
then the three SRs. It also writes the arms map (`spine-authoring`
`references/in-lane.md`). Statuses stay as they are (all 23 rows are Approved
today). No sitting happens at this step; W14 holds it.

- For each row, read A/CS/H with `git show 607cf609:<file>`,
  `git show 961f9e47:<file>` and the working copy, and port the meaning that the
  spec's "The spine" list gives that row, cell by cell. Do not copy CS's bytes.
  Where H rewrote a cell after the split (SR-148 acceptance, SR-156 acceptance,
  LLR-151 detail, LLR-058 detail, TC-061, TC-145), keep H's text and change only
  the batch meaning.
- LLR-152, LLR-207, TC-146 and TC-205: replace the batch clause only, in the
  same voice. TC-146's "a mixed batch bars as usual" becomes "a lane whose one
  row is any other kind bars as usual". TC-205's two-row-peels arm becomes "a
  mechanical close moving two rows does not peel". CS's primary-turn text does
  not come back.
- LLR-149 also repairs the stale "admit as the queued batch at
  single-approve's close" sentence so it states what `_admission` does: held
  attestation and gate rows drain and surface, and keep-nondependent never
  releases their hold.
- **Ruling 5 (D3).** Every cell restated whole (SR-144/148/156 per the spec;
  LLR-058 title, LLR-061, LLR-123, LLR-144, LLR-149, LLR-150, LLR-151, LLR-161;
  TC-058, TC-138, TC-143, TC-144, TC-154), and every replaced clause, names no
  code file, function, symbol or test module. LLR-061's restated detail today
  says "integrate.py's claim"; that has to become capability voice ("the
  branch the claim cut"). I also recommend replacing the literal `--wi` with
  "the worker's assignment argument" in requirement cells, because a CLI flag
  sits close enough to a code reference that a ruling-5 reading could catch it.
  The check before commit: grep every changed requirement/detail/method cell
  for `\.py`, `\w+_\w+\(`, `test_` and backticked identifiers, and expect
  none.
- Leave alone: "batch" in its other senses (LLR-148 "approved draft-SN
  batch", LLR-194/TC-019 "batched floor", LLR-240/TC-235 "assumption batch",
  TC-130), LLR-208's "traincar is one review scope", SR-026, every IF and CMP
  row, and spine exclusivity (item 16's).

### W2: tests first (D15)

One test commit, before any code, with each test under one evidence class
(coordinator cycle "Intent", step 2):

- **New behaviour (the refusals):** marked
  `@pytest.mark.xfail(strict=True, raises=(AssertionError, pytest.fail.Exception))`.
  Each one's red must reach its own assertion, never an `ImportError` or an
  `AttributeError` on a not-yet-written helper. So every refusal test drives an
  existing surface: `dsp._admission`, `dsp.run` with the injected worker,
  `integ.claim` and `integ.main([...])`, `ac.preflight`,
  `agent_loop.build_worker_assignment` and the `agent_loop` CLI,
  `agent_brief.worker_prompt`, `hb.close_partial`, `hb.close_adjudication`, and
  `kverdict.mechanical_close_attestation`. None of them calls a new function
  name.
- **Characterization (already-correct behaviour):** unmarked, with the
  adequacy witness written in the test, meaning the wrong implementation it
  would catch.

The rows below name each test and what it fails on today. Converting or
deleting the batch tests the spec's Context lists happens in the same commit
where the test's assertion inverts. Otherwise it happens in the code commit
that makes the old assertion false (each row names its own). Hand-made
multi-spec claim directories, which W3, W8 and W9 need (and which must
survive W5, after which `claim` refuses lists), are built by a fixture that commits the joined historical
subject and moves both specs by hand. That is the record the spec places
outside the promise (PROCESS.md §6), and it is the only way to drive those
refusals.

### W3: resume (D8; F1)

Code (`dispatch._admit_parked`): after the free/exclusive checks and **before**
`_pre_admit`, the cycle count and `_launch`, read
`integrate._claimed_wi_ids(root, branch)`. With two or more ids, print a
refusal naming the branch and its ids ("a lane carries exactly one work item;
close or land it by hand"), and stop the run through the same pattern as
`_claim_lanes`' branch-name refusal: with lanes live, freeze admission with
`state["fatal"] = ac.EXIT_PREFLIGHT` and drain; with none, return
`EXIT_PREFLIGHT`. Nothing is relaunched, no worktree is ensured, and no commit
is made. Zero cannot reach this point (`_parked_branches` requires a spec).
In this step the surviving one-element list still goes to `_launch` unchanged,
because `_launch` keeps its list contract until W4 narrows it together with
this caller. This step drops the strict-xfail marker on the new test below.

Tests (`tests/test_dispatch.py`):
- New `test_a_parked_lane_claimed_with_two_specs_stops_the_run`. The hand-made
  two-spec claim fixture (W2) plus the branch ref, then `drv.run(...)` with an
  injected worker. Expect rc `EXIT_PREFLIGHT`, the output naming the branch,
  `worker.calls == []`, HEAD and the branch tip unchanged, and both specs
  still in `active/<branch>/`. Fails today: the worker is relaunched with both
  ids.
- The existing parked-resume tests (`test_drive_resumes_a_parked_branch…`,
  `test_a_crashed_worker_stays_parked…`, `test_a_finished_branch_that_owes_a_round_is_resumed_not_integrated`,
  `test_a_review_owed_worker_stays_parked…`) pass unchanged. They are TC-144's
  single-item half ("a single-item lane resumes under the barrier").

### W4: admission and the one-id lane seam (D5, D6; F1)

Code (`project-trajectory/scripts/dispatch.py`):
- `_kind_action`: `spine` returns `"exclusive"`. The policy-table docstring
  row becomes `spine  exclusive  exclusive`.
- `_admission`: the `action == "batch"` arm goes. `admit-exclusive` always
  carries `[first_w]`. The docstring's payload table loses "all spine rows
  together" and "the queued approval batch".
- `_claim_lanes`/`_launch`/`_Lane`: the admitted assignment becomes one id.
  `_Lane.wi_id` is a str. `_launch(root, table, branch, wi_id, ...)`. The
  injected worker seam becomes `(root, branch, wi_id, args)`. The
  `"claiming {} on {}"` line names the one id. `integrate.claim(root, wi_id,
  ...)` receives a str, which today's `claim` accepts (integrate.py:821
  wraps a str in a one-element list). So this step needs no claim change, and
  W5 can then refuse lists without a dispatcher caller left sending one.
- **Both `_launch` callers narrow in this step (F1):** `_claim_lanes`
  (dispatch.py:1125) passes the one admitted id, and `_admit_parked`
  (dispatch.py:1076) passes the one id that W3's rung leaves
  (`(wi_id,) = wi_ids`). No caller of the narrowed seam is left on the list
  form between steps.
- `project-trajectory/scripts/lane.py`: `worker_argv`, `spawn_worker` and
  `run_worker` take `wi_id`, and `--wi` gets it bare (no `";".join`).
- The site the spec's Context missed: `rendering/traj_panels.py`
  `_ADMISSION_ARMS` loses `"batch"`. The barrier title and notes ("the batch
  runs alone ... one window, one owner sitting", around lines 673 and 850)
  become "the exclusive row runs alone, the sole toucher of trunk". Without
  this, `tests/test_traj_panels.py::test_station_barrier_and_admission_arms_pin_to_the_dispatcher`
  goes red the moment `batch` leaves `_kind_action`. Line 976 ("a phase's
  slices batch to one re-attestation sitting") is another sense of the word
  and stays.

Tests:
- `test_dispatch_admission.py::test_lanes_back_in_the_station_the_spine_batch_admits_together`
  becomes `..._the_first_spine_row_admits_alone`. Its assertion is
  `("admit-exclusive", ["WI-500"])`, which fails today because the payload is
  `["WI-500","WI-501"]`. `test_high_risk_admits_alone_not_batched` gets its name
  and comment reworded; the assertion is unchanged.
- New `test_dispatch_admission.py::test_no_kind_maps_to_a_batch_arm`:
  `_kind_action(k, h)` over every `schedule._KIND_CONCURRENCY` kind × held
  never returns `"batch"`, and `spine` returns `"exclusive"`. Fails today on
  `"batch"`.
- `test_dispatch.py::test_the_spine_batch_admits_first_and_together` becomes
  `test_spine_rows_admit_one_per_exclusive_turn`. It expects `worker.calls ==
  [("wi-501-alpha","WI-501"), ("wi-502-beta","WI-502"), ("wi-401-widget","WI-401")]`,
  two separate `claiming WI-50x on ... (exclusive)` lines, and no `;` in any
  claim line. Fails today: one call carries both ids.
- `test_dispatch.py::test_residue_settled_at_barrier_open_is_counted_in_the_drained_banner`:
  the two spine rows now admit in two turns. The residue branch stays two-row
  (a hand-made historical shape that `_residue_wi_count` still counts), and
  the total stays "5 WI(s) integrated". Its comments drop the batch premise.
- `test_loop_order.py::test_an_adjudication_row_outranks_a_spine_batch`
  becomes `..._outranks_a_spine_row` (comment only; it passes today).
- The worker fakes in `test_dispatch.py` (about five) and their
  `calls == [(branch, ("WI-…",))]` assertions (about 16, in `test_dispatch.py`,
  `test_handback.py`, `test_adoption_record.py` and `test_agent_loop_worker.py`)
  move to the scalar id.
- TC-137's `test_dispatch.py` cases run unchanged otherwise.
- This step drops the strict-xfail markers on the two admission tests above.

### W5: claim and the claim subject (D7, D13; F1)

Code (`project-trajectory/scripts/integrate.py`, `agent_common.py`):
- `claim(root, wi_id, branch, ...)`: its **first** rung, before the hooks
  rung, the context guard, `_claim_refusal` and `_dispatch_lock`, is a pure
  input check, `_claim_input_refusal(wi_id)`. Anything that is not a `str`
  fully matching `ac.WI_TOKEN_RE` (`^WI-\d+$`) refuses with
  `"claim takes exactly one work item id; got {!r} ..."`, which names the
  input. That one rule covers empty, separator-only, `;`/`,`/whitespace
  lists, and any list or tuple, including a one-element list. Nothing is
  locked, moved, committed, branched or worktree'd.
- CLI: `claim(root, normalize_wi_id(args.wi), args.branch)`. The `split(";")`
  goes, and case normalization stays. `normalize_wi_id` leaves anything that
  is not a bare `wi-NNN` unchanged, so the input rung sees `";"` and
  `"WI-1;WI-2"` exactly as typed.
- `_claim_refusal`, `_abandoned_claim`, `_claim_delta`, `_done_when_warning`
  and `_claim_locked` take one `wi_id`. The per-id loops and "a batch is one
  commit, whole" go. `_relinked_exactly` keeps its `remap` dict (now one pair),
  and its "one entry per batched spec" wording goes.
- `ac.claim_subject(wi_id, branch)` takes one id and raises `TypeError` on a
  non-str. `integrate._claim_subject` follows. The history reader
  `ac.claim_base` stops composing through the writer: it accepts a subject
  `claim: <ids> -> active/<branch> (bookkeeping)` whose `;`-split ids are all
  WI tokens, so the two historical joined subjects (`2f660cb7a`, `794de60d5`)
  still read as claims. `ac.loop_claimed` and `kitlib/provenance.py`'s
  `claim: .+ -> active/{branch}` pattern already accept the joined form and
  are left alone.

Tests (`tests/test_integrate.py`):
- `test_a_spine_batch_claims_as_one_commit` becomes
  `test_a_multi_item_claim_refuses_before_any_state_change`. It runs
  `integ.claim(root, ["WI-501","WI-502"], "wi-501-alpha")`, then the CLI
  `--wi "WI-501;WI-502"`, `--wi "WI-501,WI-502"` and `--wi "WI-501 WI-502"`.
  Each must return 1 and name the input, with no branch ref, HEAD unchanged,
  both specs still in `queued/`, no `out/agent-loop.lock` left behind and no
  worktree registered. Fails today: the list form claims both (rc 0, subject
  `claim: WI-501;WI-502 …`).
- New `test_an_empty_claim_refuses_before_the_lock` (driven, D7):
  `integ.main(["claim","--wi",";","--branch","x","--root",…])` and
  `--wi ""` return 1, name the input, and leave no branch `x` and HEAD
  unchanged. Fails today: `[]` passes every rung (the spec's fail-open).
- New `test_the_claim_subject_composes_one_id_only`: `ac.claim_subject(["WI-1","WI-2"], "b")`
  raises `TypeError`, and `ac.claim_subject("WI-1","b")` is today's string.
  Fails today: the list is joined.
- New characterization `test_a_historical_joined_claim_still_reads_as_a_claim`
  (D13, driven on a fixture holding one). Trunk carries a hand commit
  `claim: WI-569;WI-575 -> active/wi-569-x (bookkeeping)` moving both specs
  `queued/ -> active/wi-569-x/`. `ac.claim_base(root, "wi-569-x")` returns
  that sha, readable. `ac.loop_claimed` reads it as a claim. The provenance
  claim pattern matches it. Adequacy witness, written in the test: a reader
  that composed through the narrowed one-id writer would return `(None, True)`.
- Callers moved to a str id: `test_blackout_window.py`,
  `test_coordinator_guard.py` (×4), `test_coordinator_guard_e2e.py`,
  `test_bookkeeping.py`, the `batch_repo` fixture in `test_handback.py` (today
  `integ.claim(root, list(wids), …)` at line 992, which becomes the hand-made
  two-spec fixture here and not in W8, because this step is the one that
  refuses its list), and `test_integrate_station.py:562` (its list argument
  moves here; W10 later renames and re-asserts the test).
  `integrate_fixtures.py:214` (`claim_subject([wid], …)`),
  `test_dispatch.py:967` (`claim_subject(ids, …)`) and
  `test_dispatch.py::hand_finished_branch` pass one id, or write the joined
  historical subject literally for multi-row residue. `ac.claim_base`'s
  re-composition through `claim_subject` (agent_common.py:1246) changes in
  this same step (above), so the narrowed writer has no list caller left.
  This step drops the strict-xfail markers on the three refusal and subject
  tests above.
- Order check: every in-process list caller of `claim`/`claim_subject` in
  scripts is gone by the end of W4 (the dispatcher) or changes in this step.
  The builder confirms it with `rg -n "claim\(root, \[|claim\(root, list\(|claim_subject\(\["`
  over `project-trajectory/scripts` and `tests`, and expects no hits after
  this step.
- Regression run: TC-145, TC-139 (the claim's one move ritual), TC-131 (the
  pause rung), TC-317 (the guard rungs), TC-370 (the hooks rung). Their
  evidence modules must pass.

### W6: worker, preflight, assignment and walk (D9)

Code:
- `agent_common.parse_wi_list` is replaced in place by
  `parse_wi_id(spec) -> str`, the one home for the worker's grammar. A value
  that is not exactly one `WI_TOKEN_RE` token after outer `strip()` raises
  `ValueError` naming the value. Empty, separator-only, `;`, `,` and inner
  whitespace lists, a malformed token (`WI-`, `wi-201`, `junk`) and a repeated
  id (`WI-201;WI-201`, which holds a separator) all fail. The re-export at
  `agent_loop.py:265` follows.
- The shared preflight (`agent_common.preflight`, worker block) parses one id
  and checks that one row (registry presence, `stale_terminal_assignment`).
- `agent_loop.build_worker_assignment`: `wi = parse_wi_id(args.wi)`. The dual
  check is on the one row. `worker["assigned"] = (wi,)`. **Decision:** the
  worker view keeps its `assigned` key as a one-element tuple built from the
  single parsed id, rather than being renamed. About 15 evidence readers in
  `agent_loop.py`/`agent_brief.py` and 19 test fixtures read it, and none can
  observe two ids once the parse refuses them. Renaming would churn every
  reader without changing behaviour. This goes in the decisions record.
- The walk, `current_assignment_wi`, becomes `return worker["assigned"][0]`.
  The `remaining` list, the `rework_wi or assigned[-1]` fallback and the
  four-row-batch docstring go, and the two-part predicate stays with the
  brief's readers (spec, "Unchanged": the completion predicate). `rework_wi`
  stays as the rework banner's text only.
- `stale_terminal_assignment` **stays**, and its docstring loses the batch
  story. A one-row finished lane that still owes a review round is resumed
  with its one row already `done` on the lane (`_parked_branches` and
  `_round_owed`), and without this rung the preflight would refuse it as
  stale. That is driven today by
  `test_dispatch.py::test_the_worker_preflight_accepts_the_resumed_finished_lane`,
  which is single-row. The coverage table's close row ("that spec already
  terminal on the lane keeps today's answer") assumes the same.
- `--wi` help: "the one claimed work item this worker builds, e.g. 'WI-201';
  a list is refused". The traincar/list wording goes. The banners
  (`worker_exit_banner`, `_done_endstate`) name the one id.

Tests (`tests/test_agent_loop_worker.py`, `test_agent_loop_policy.py`):
- `test_parse_wi_list_orders_and_validates` becomes
  `test_the_worker_refuses_any_assignment_but_one_id`, driven through
  `ac.preflight(wt, "stub-agent", Namespace(wi=v, train=None, interactive=False))`.
  For `""`, `";"`, `"WI-201;WI-204"`, `"WI-201,WI-204"`, `"WI-201 WI-204"`,
  `"WI-201;WI-201"`, `"WI-"` and `"wi-201"`, there is one failure naming the
  value. `"WI-201"` gives no assignment failure. Fails today: the list values
  pass.
- `test_worker_multi_wi_assignment_builds_in_order` becomes
  `test_a_list_assignment_exits_preflight_before_a_provider_launches`. The
  `agent_loop` CLI with `--wi "WI-201;WI-204"` exits 2, and the fake provider's
  control file records no launch. Fails today: it builds both.
- `test_build_worker_assignment_good_base_parses_wi_list` becomes the one-id
  form: `worker["assigned"] == ("WI-201",)`. A `"WI-201;WI-204"` value is
  refused (rc `EXIT_PREFLIGHT`). Fails today: it returns the list.
- New `test_the_wi_help_names_one_work_item`: the parser's `--wi` help
  contains "one" and no `;` example. Fails today on `'WI-201;WI-204'`.
- `test_agent_loop_policy.py::test_worker_exit_banner_returns_code_and_prints`
  moves to one row (`[WI-201]`). The two-row banner goes.
- Regression run: TC-026 (headless resume), TC-097 (the dual-plan worker
  refusal on the one row), TC-257, TC-325 and TC-326 (the Done-when hold reads
  the one id through `assigned`).

### W7: the prompt (D10)

Code: `agent_brief.assignment_block` is deleted, along with its `__all__`
entry and the `agent_loop.py:308` alias. `worker_prompt` loses its `assigned`
parameter and the `assignment_block=` fill. The `agent_loop.py:421` caller
follows. `prompts/worker.template.md` loses the `{assignment_block}` slot, its
"Slots:" mention and the "{assignment_block} IS EMPTY FOR A ONE-ROW LANE"
operator note. The opening sentence's batch clause ("— plus, when the lane was
claimed as a batch, the sibling rows listed with it …") also goes, because it
is batch-only wording. That is the only byte the one-row render loses, and the
decisions record says so.

Tests:
- `test_worker_batch_prompt_names_every_assigned_row_and_its_state` becomes
  `test_the_worker_template_has_no_assignment_block_slot`. The raw template
  text holds no `{assignment_block}`. Fails today.
- New characterization `test_the_one_row_prompt_renders_as_today`: render
  `worker_prompt` for a one-row lane and compare it with a golden string
  captured from today's render, minus the removed clause. Adequacy witness: a
  template edit that dropped or reordered an Assignment line would fail it.
- Regression: TC-061's other `test_agent_loop_worker.py` cases.

### W8: the closes (D11; F1)

Code (`project-trajectory/scripts/handback.py`):
- `close_partial`: right after `integrate._claimed_specs`, refuse
  `len(specs) != 1`. Zero keeps today's text. Two or more give
  `"a lane closes exactly one claimed work item; trunk claims {n} for {branch}: {ids}"`.
  This comes before `_lane`, the immutability rung, any report, the residue
  commit and any move. The loop over specs becomes the one spec. `written`
  becomes the one report, and the restore still runs on its refusal paths. The
  "every report THIS CALL has written" comment goes.
- `open_claimed_specs` becomes a one-spec predicate, "is the one claimed spec
  still in `active/<branch>/` on the lane", with its "ONE HOME FOR THE BATCH
  FILTER" docstring reduced. Today's two answers for an already-terminal spec
  stay: the immutability refusal, then the `[]` no-op for the partial close,
  and the `(None, None)` no-op for the adjudication close.
- `close_adjudication`: the same `len(specs) != 1` refusal, placed before
  `_lane` and any archive. It moves its one row. The `moved_rows` loop and its
  `station.mechanical_close_order(moved_rows)` call (handback.py:1001) go, and
  `closed` becomes `[wi_id]`. The subject is composed **under the composer's
  current list contract**, `station.mechanical_close_subject([wi_id])`, which
  is byte-identical to today's one-row subject. So `test_handback.py:850`
  (`subject == mechanical_close_subject(["WI-401"])`) and the attestor's
  recomposition (verdict.py:829, still list-form until W9) keep agreeing at
  the end of this step (F1). The `WI:` trailer's `", ".join(closed)` names the
  one id. The composer's signature is not touched here. W9 narrows it with
  every caller at once.

Tests (`tests/test_handback.py`):
- `batch_repo` is already the hand-made two-spec claim fixture by this step
  (W5 converted it when `claim` began refusing lists). Its batch-close tests
  are converted here, in the commit where their assertions invert.
- This step drops the strict-xfail markers on the two close refusals below.
- New `test_a_partial_close_of_a_two_spec_claim_refuses_before_any_report`:
  refusal text naming the count, no `docs/handbacks/` file, no new lane
  commit, and both specs still in `active/` on the lane and on trunk. Fails
  today: it closes both.
- New `test_an_adjudication_close_of_a_two_spec_claim_refuses_before_any_move`:
  same shape. Fails today: it archives both.
- `test_the_mechanical_close_no_ops_when_a_batch_row_already_closed` and
  `test_a_partial_close_skips_a_row_the_lane_already_closed` (the batch-row
  closes) become the two refusals above. `test_an_adjudication_batch_still_closes_the_row_that_is_open`
  becomes `test_an_adjudication_close_moves_its_one_row` (characterization).
  `test_a_partial_close_with_every_row_already_terminal_is_a_no_op` keeps its
  one-row form. The zero-spec refusal test stays as is.
- TC-156's restore arm: an injected `spec_move.move_spec` refusal after the
  single report is written restores that report, leaving the claim and the
  terminal state unchanged (existing test, re-pointed to the one report).
- Regression run: TC-138, TC-156, TC-184, TC-254 (the consolidation close
  shares `close_adjudication`).

### W9: the peel and the composer (D12; F1)

Code:
- `kitlib/verdict.py` `_closed_wi_ids` requires **exactly one** paired
  `active/<branch>/` deletion and `complete/` addition, and returns `[wi_id]`.
  Any other count returns `None` and declines to peel, failing toward more
  review. With exactly one deleted row the one-source-branch clause is implied,
  so it would be dead code by the docstring's own argument. It is replaced by
  the one-row clause, and the docstring says why.
- `mechanical_close` keeps returning `(parent, ids)`, a one-element list, so
  `adoption_record._commit_close` (`wi not in closed[1]`) is untouched.
- **The composer narrows with every live caller in this one step (F1).**
  `station.mechanical_close_subject(wi_id)` takes one str, formats it without
  a join, and raises `TypeError` on a non-str, so a stray list caller fails
  loudly instead of writing a subject that drifts. The callers change in the
  same commit:
  `handback.close_adjudication` (`mechanical_close_subject(wi_id)`, the
  re-export at handback.py:154 kept as the same object);
  `verdict.mechanical_close` (verdict.py:829 composes from the one id
  `_closed_wi_ids` returns); `tests/test_adoption_record.py:100`;
  `tests/test_handback.py:850`; `tests/test_loop_provenance.py:910-913` (its
  `["WI-401", "WI-402"]` multi-row case goes, and the one-row case stays);
  and `tests/test_verdict_record.py` at 1909 (the `_mechanical_close`
  helper), 1971 (`"NOT-A-WI-ID"`), 2053-2057 (the canonical-order assertion,
  deleted with the order) and 2077.
- `kitlib/station.py`: `mechanical_close_order` and `_close_sort_key` are
  then deleted. After W8, their only reader left is `verdict._closed_wi_ids`
  (verdict.py:693), which changes in this step, so no reader is left behind.
  The `verdict.py` import follows. The builder confirms it with
  `rg -n "mechanical_close_order|_close_sort_key|mechanical_close_subject\(\["`
  over `project-trajectory/scripts` and `tests`, and expects no hits.
- This step drops the strict-xfail marker on the no-peel test below.

Tests:
- `test_verdict_record.py::test_a_two_row_batch_close_peels_under_one_canonical_order`
  becomes `test_a_mechanical_close_moving_two_rows_does_not_peel`. Fails today:
  it peels. Its `_mechanical_close` helper drops the
  `ks.mechanical_close_order` call.
- `test_a_close_reaching_into_a_second_lanes_claims_does_not_peel` still
  passes (two deletions), now through the one-row clause. Its comment says so.
- `test_handback.py:671`'s comment (which names the shared ordering) is
  reworded to the one-row writer-attestor agreement. The test itself passes
  unchanged across W8 and W9.
- `test_disposition_adoption.py` `_closed_wi_ids` cases (TC-360) and
  `test_adoption_record.py` (TC-383) run unchanged. They are one-row closes.
- TC-205's evidence cell drops the deleted test name (W14). TC-132 runs as a
  regression.

### W10: the other readers of the claimed set (D14)

They keep their code; only batch-only wording and arms go.
- `integrate._lane_bar_directives`: "a mixed batch runs it" becomes "any other
  kind runs it". The strictest-among-rows selection becomes the one row's key
  (`bars[0] if bars else None`). The `_BAR_GATES` tuple stays for validation,
  and its "so a batch takes the STRICTEST" comment goes.
- `dispatch._residue_wi_count` keeps its sum (one per branch, and a hand-made
  historical residue still counts truthfully). Its docstring drops "a spine
  batch is ONE branch carrying several WIs".
- `_poll`'s merged count becomes `state["merged"] += 1` per merged lane (the
  lane carries one id). The comment goes.
- `integrate.py` `_claimed_wi_ids` and `_claimed_specs`, and the merge slot's
  `", ".join(wi_ids)` lines, stay as they are: readers of what the claim wrote.

Tests: `test_integrate_station.py::test_a_mixed_claim_still_runs_the_bar`
becomes `test_a_lane_whose_one_row_is_ordinary_runs_the_bar`, claiming WI-402
(ordinary) alone. Characterization: it would catch a no-bar arm that keyed on
"any adjudication row". TC-146 and TC-331 run as regressions.

### W11: ratchets and the leftover sweep (D15)

- `tests/test_complexity_ratchet.py` is an exact-match census. Every function
  whose C901 dropped (`_admission`, `claim`, `_claim_refusal`, `close_partial`,
  `close_adjudication`, `current_assignment_wi`, `_closed_wi_ids`, and any
  other) is re-stamped downward in the same commit, with a dated reason, as
  that file requires.
- `tests/test_module_size_ratchet.py` is declared `linecounts` in
  `docs/stack.ini [generated]`, which makes it trunk-owned. Its re-stamp is
  the landing squash's (W15), and it is not committed on the lane. If it reds
  in the lane, the builder reports the deltas for the coordinator.
- Final sweep: `rg -n -i "batch|WI-201;WI-204|;\".join\(wi_ids|parse_wi_list|assignment_block|mechanical_close_order"`
  over `project-trajectory/scripts` and `tests`. Every hit left is a named
  other sense (act-ledger batch approvals, `--approves`, the consolidation
  verdict, `intake.py sweep --merged`, the phase-close "batch", the scoped
  unpause), and the sweep output goes in the lane's iteration log.

### W12: text (D16)

- `project-trajectory/PROCESS_OPTIONS.md`: delete the "Multi-WI assignments
  (WI-133 → the scheduler)" paragraph (lines 1118–1122), which still offers
  `--wi "WI-a;WI-b"`. Run the `byte-budget-guard` skill before and after,
  report the byte delta, and restamp its watched-row table. The dogfood copies
  under `.claude/skills/` and `project-trajectory/skills/` stay in sync.
- `project-trajectory/README.md` `dispatch.py` row: "spine WIs then admit
  TOGETHER as one batch (one re-attest window)" becomes "each spine row admits
  alone, one per exclusive turn". The `lane.py` row's "moving its specs"
  becomes "its spec".
- The `dispatch.py` header: "EXCLUSIVELY and BATCHED … one owner sitting"
  becomes one row per exclusive turn. The stale keep-nondependent sentence is
  corrected to the surface arm (LLR-149). The `agent_loop.py` header's
  `--wi "WI-###[;WI-###…]"` and the multi-WI paragraph (around lines 84–105)
  become one id. The `lane.py` docstrings follow.
- `docs/runtime-flows.md` (around line 180): "the batch admits alone" becomes
  "the exclusive row admits alone".
- `docs/concurrency-v2.md`: §A4's flowchart nodes ("spine batch has
  priority", "Admit ALL spine WIs together") and its "batched" prose; §A4.1;
  §A4.4 (the component-scoped batching design note); the §A6.1 passage keeping
  `--wi 'WI-201;WI-204'`; and the §A8 rows naming "the queued batch". Each is
  marked superseded by a note at §A4 naming review-churn item 15 and WI-977,
  and states one item per lane, with the design history kept rather than
  deleted.
- Left alone: dated history (`docs/archive/`, handoffs, the redesign docs,
  `docs/ratify/`, logs, reviews), the deferred WI-808 spec and
  `docs/status.md`.

### W13: one RESYNC entry (D17, D18)

Append `### One work item per lane: the spine batch retires [since a1984f739]`
to `project-trajectory/RESYNC_PACK.md`. The anchor is the lane's base, the
trunk commit after its claim, following the convention of the entries before
it, and `tests/test_resync_pack.py` checks that it exists. The entry states:
spine rows admit one per exclusive turn (N re-attestation windows for N rows);
`integrate.py claim --wi` and `agent_loop --wi` take exactly one id, so a
script or launcher passing a list fails; a parked lane claimed with several
rows refuses to resume, so an adopter closes or lands such a lane before
upgrading; the worker template lost a slot (kit-owned, overwritten); no data
migrates. It says that it supersedes the batch sentences of the
`[since 81cac0e1]` dispatcher entries (lines 779 and 2681) and of the
`[since f4ca1bd5]` "Four batch-lane defects" entry (line 4716), and each of
those gains a one-line "(superseded in part by …)" pointer, per §1.3's pair
rule. `python scripts/check_resync.py` is green.

### W14: reconcile and the one checkpoint sitting (D3, D4)

- Traced cells follow the code (D3): LLR-061 `code_symbol` drops
  `assignment_block` and its `module` keeps the brief; LLR-149, LLR-150,
  LLR-151, LLR-144 and LLR-207 `code_symbol` add any new rung function (for
  example `_claim_input_refusal`) and drop deleted ones. Every new function
  carries an `Implements:` line for its LLR. TC `evidence` cells name the
  renamed or added tests (TC-143, TC-144, TC-145, TC-146, TC-061, TC-138,
  TC-205, which today names the deleted `test_a_two_row_batch_close_peels_under_one_canonical_order`).
  `trace.py --strict` and `check_trajectory.py --strict` are clean.
- Re-run the ruling-5 grep from W1 over the final cells.
- One checkpoint sitting judges the 23 amended rows against the built code.
  The coordinator acts from its verdict (`coordinator_adjudicate.py act`).
  Nothing is held for the owner: the SR, LLR and TC rungs sit above
  `human_approval_through` in `docs/process.toml`, which I have not paraphrased
  here and the coordinator reads at the act.

### W15: generated pages and the bar (D19, D20)

- On the lane, the builder only *checks* the regeneration diff and does not
  commit it (generated artifacts are trunk-owned):
  `gen_arch_map.py --cli-doc` (the `docs/cli-reference.md` `--wi` and
  `claim --wi` rows), `gen_prompt_catalog.py` (`prompts/CATALOG.md`, whose
  worker digest changes), `gen_trajectory.py` (PROJECT_STATE.html, the
  admission arms), the components and interface references, and the module-size
  linecounts. The landing squash regenerates and commits them, per the
  coordinator cycle §3.
- Per-commit bar on the lane: `run_menu.py smoke` (both strict lints, the docs
  staleness check, `check_resync.py`, the smoke tier). On the landing tip, both
  strict lints are clean, and the full unfiltered suite
  (`python -m pytest -q -n auto`) runs once in the merge slot. The real output
  is pasted.

## Decisions to record (`docs/decisions/wi-977.toml`)

1. The in-process `claim` takes a `str` and refuses any list, including a
   one-element list (deny-by-default). Callers pass the id.
2. Dispatch and lane carry a scalar id. The worker's internal `assigned` view
   stays a one-element tuple built from the one parsed id (W6's reason).
3. `stale_terminal_assignment` stays, because one-row finished lanes owing a
   round depend on it (W6). This answers the spec Context's "exists for a
   batch lane".
4. The worker prompt's opening batch clause is removed. The one-row render
   otherwise equals today's (W7).
5. The peel's one-source-branch clause is replaced by the one-row clause that
   implies it (W9).
6. The dashboard's admission vocabulary and barrier text change with the
   dispatcher (W4). The spec's Context did not list this site, but its sync pin
   forces it.

## Risks

- Hand-made two-spec claim fixtures are the only way to drive W3, W8 and W9.
  Their shape is fixed by the two historical commits, not invented.
- The exact-match ratchets (complexity in the lane, module size at landing)
  are the likeliest red after the deletions. W11 owns them.
- This row changes the claim and the closes the coordinator cycle runs on, so
  it lands alone (spec S6) and before the managed loop is unpaused.
