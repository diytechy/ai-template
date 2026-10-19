# WI-925 plan, revision 2: the trunk is the declared branch, and a spec move's own relink inside a claim copy's Done-when is not a Done-when change

## Revision 2: the critique's finding

Critique 1 (`docs/plans/WI-925/critique-1.md`) raised one finding. It was
checked against the spec and the code before anything changed.

- **F1 [MAJOR], P0's C2 probes: confirmed.** The spec's call C2 names the
  case: "a lane that refreshes from trunk takes trunk's relinked copy, so its
  build hold and merge slot compare the claim (before the relink) with the
  relinked copy; and the merge-time mint compares the same pair when that row
  closes." Revision 1 cut `wi-y` from `main` only after X's squash landing.
  That lane's tip, and every base it can be asked against, already hold the
  relinked Y copy. The code shows why no probe could then see the pair:
  - the merge slot, `integrate._done_when_refusal`, calls
    `kdone.lane_hold(root, branch, _head(root), ...)`: the claim copy at
    trunk's HEAD against the lane tip. Both were relinked;
  - the build hold, `agent_loop` (line 981), calls
    `kdone.lane_hold(root, "HEAD", worker["base"], ...)`, where the base is
    the merge base with trunk. That base was relinked too;
  - the mint, `intake` (line 1224), reads `kdone.claim_copy(root, before,
    ...)` against the closed copy, and both came from after the relink.

  So every probe compares two relinked copies and would record "not held"
  for a reach it never built. P0's C2 section below is rewritten: Y's lane is
  cut while Y still carries its original link, before X lands. That one lane
  history is kept across X's landing, Y's refresh and Y's close, and each
  hold point is probed at the step where the spec says the pair meets. The
  fix is not widened (C2 (a)): each observed hold is recorded and pinned as
  residue. Row P0 covers F1.

Nothing else changed from revision 1, except that P0's row names F1 and the
C2 test's name. The delta answer is unchanged.

Planner: fresh session, 2026-10-18. Spec:
`docs/work/active/wi-925/WI-925-trunk-ref-update-done-when.md`, read in full.
Its specref is WI-921's Trust section
(`docs/archive/work/complete/WI-921-hook-floor-done-when-census.md#trust`).
The owner rulings it relies on are its "Calls ruled at filing": Q3 (a) and
Q5 (a), ruled by the owner; C1 (a), C2 (a) and C3 (a), ruled by the
coordinator (coordinator-2026-10-15 D-020), for the owner to confirm or
overrule.

Code read at the lane tip `6533a2331` (the lane branch `wi-925` has no commits
of its own yet; its merge base with trunk `refactor_again` is that commit):
`agent_common.py` (`trunk_name`, `claim_base`, `default_base`,
`stale_terminal_assignment`), `agent_policy.py` (`PROCESS_ONLY_KEYS`,
`process_config`, `_coerce`, `config_conflicts`), `bootstrap.py`
(`set_process_key`, `_locate_process_key`, `apply_declared_policies`,
`main`), `agent_brief.py` (`reviewer_prompt`, `review_round_brief`),
`agent_loop.py` (the worker preflight's `--base` arm), `gen_verdict_rollup.py`
(`_off_trunk_refusal`, `main`), `handback.py` (`_lane_verdict`,
`_machine_line_refusal`, `close_partial`'s contract), `integrate.py`
(`staged_done_when_refusal`, `_done_when_refusal`, `_relinked_exactly`,
`_blob_bytes`), `plan_gate.py` (`_relinked`, `_close_homes`, `_claim_base`,
`staged_lines`, `commit_lines`), `spec_move.py` (`expected_relink`,
`_relink_inbound_links`), `kitlib/done_when.py` in full, `kitlib/plan_pass.py`
(`blob`), `kitlib/git.py`, `check.py` (`_changed_paths`'s work-branch arm),
`check_readability.py` (`_range_and_rev`), `review_brief.py` and
`adjudicate_brief.py` (their `default_base` reads), `check_trajectory.py`
(`holdbyrename_findings`), the shipped `hooks/pre-commit` (its
`done-when-blessed` comment), `process.toml.template` and `docs/process.toml`.
Tests read: `tests/conftest.py` (the `scaffold` fixture, `set_process_key`,
`SLOW_MODULES`), `tests/integrate_fixtures.py` (`git_repo`),
`tests/test_done_when_blessing.py` (fixtures and the WI-921 trunk-arm tests),
`tests/test_agent_loop_review.py` (the two `default_base` tests),
`tests/test_agent_loop_worker.py` (the single-checkout terminal refusal),
`tests/test_verdict_record.py` (the rollup's off-trunk test),
`tests/test_process_config.py` (the wrong-typed-dial test),
`tests/test_dogfood_sync.py` (the process.toml structure test) and
`tests/test_trajectory_holdban.py`.

The item's SRs are SR-156, SR-170 and SR-137
(`docs/requirements/system-requirements.toml`). Seventeen TCs verify them
(`docs/test/test-cases.toml`): TC-060, TC-130, TC-131, TC-132, TC-139,
TC-144, TC-145, TC-150, TC-205, TC-206, TC-257, TC-259, TC-317, TC-325,
TC-326, TC-327 and TC-328. A row below names each one, or the Excludes line
at the end gives the reason it is left out. Rows of record also read:
LLR-307, LLR-309, LLR-208, LLR-145, LLR-151 and LLR-337
(`docs/requirements/low-level-requirements.toml`); IF-179, IF-189, IF-261 and
IF-286 (`docs/requirements/interfaces.toml`); CMP-006 to CMP-009
(`docs/requirements/components.toml`); `docs/runtime-flows.md` (it names no
trunk reader, so it needs no edit); and the WI-921 entry in
`project-trajectory/RESYNC_PACK.md`.

## Architectural delta

The row does two of the four things:

- **A domain value changes.** The trunk's identity is now the declared
  branch name. Before, it was the primary checkout's branch, then the
  current branch, then the worker's base.
- **Outputs depend on a new input.** Every trunk reader now reads
  `docs/process.toml [policies] trunk`. That covers the done-when step's arms,
  the rollup's refusal, the lane base (`default_base`) and its readers, the
  reviewer prompt's trunk slot and `handback`'s verdict lookup. A refusal that
  names the key is a new output on each of these routes.

It adds no state. It crosses no new boundary:

- `agent_common` already reads `docs/process.toml` through `agent_policy`
  (IF-261).
- Every trunk reader already imports `agent_common`.
- `plan_gate` and `integrate` already import `spec_move`.
- `kitlib/done_when` imports no script. The relink oracle reaches it as an
  injected callable, the same way `trunk_name` and `lane_base` already reach
  `staged_hold`.

The change fits within the row, and the rows below carry it:

- the key and its schema row (P1);
- the reader and the deletion of its fallbacks (P2);
- each caller's refusal (P3);
- the extraction of the shared relink stage (P4), in its own commit before
  its new caller (P5);
- the interface rows IF-179, IF-286 and IF-189 (P9).

IF-189 is not in the Done-when's list. `default_base`'s data cell still says
"or None when its claim history is unreadable". Deleting the claim arm (P2)
makes that false, so the cell is amended with the other two. It is Drafted.

DELTA: within

## Steps, in build order

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P0 | The relink reproduction fixture, before any fix: the squash landing, the real-edit variant, and the C2 reach probes on one Y lane cut before X lands and kept across the landing, its refresh and its close; the result goes in the lane's log | D8; F1; SR-156; TC-325 | IF-286 (exercised, not changed) | |
| P1 | The declared key: the template and this repository carry `[policies] trunk`, the schema registers it as a `str`, bootstrap writes it from the branch being scaffolded on, one test helper declares it, and the dogfood test holds its structure | D7; D4; SR-137; SR-156; TC-150 | IF-261 (the policy reader's schema table; no seam change) | P0 |
| P2 | `trunk_name` reads the key or refuses; its fallbacks are deleted; `default_base` loses its claim-record arm; trunk-reading fixtures gain the key through the helper | D6; D4; D1; SR-156; TC-257; TC-326 | IF-179; IF-189 | P1 |
| P3 | Every caller refuses in turn, naming the key; the linked-worktree and single-checkout shapes are pinned at the done-when step, the reviewer slot and the rollup | D1; D2; D3; D4; D5; SR-156; SR-170; TC-325; TC-206; TC-205; TC-327; TC-367 | IF-179; IF-189; IF-286 | P2 |
| P4 | The shared relink stage, extracted (0 to A to B): `spec_move.exact_relink`, called by the claim recognizer and the plan gate, with their relink tests unchanged | D8; D18; SR-156; TC-139; TC-145; TC-132; TC-367 | intra-module (`spec_move` gains a pure function; `integrate` and `plan_gate` already import it, and no other module's seam moves) | P0 |
| P5 | The staged reader's relink exemption: a claim-copy modification that is exactly the same delta's inbound relink is not a change | D8; SR-156; TC-325; TC-326; TC-328 | IF-286 | P3; P4 |
| P6 | `staged_closes` deleted | D10; SR-156; TC-259; TC-325 | IF-286 | P5 |
| P7 | The hold-by-rename finding names a recovery the trunk floor permits | D11; SR-156 | intra-module (`check_trajectory`'s own finding text) | P0 |
| P8 | The shipped hook's `done-when-blessed` comment: the promise and the one residue list | D9; SR-156; TC-325 | no interface (a comment in the shipped hook) | P3; P5 |
| P9 | The spine, authored in the lane and sat at its checkpoint | D12; D13; D14; D15; D16; D17; D18; D19; SR-156; SR-170; SR-137; TC-325; TC-326; TC-206 | IF-179; IF-286; IF-189 | P1; P2; P3; P4; P5; P6; P8 |
| P10 | The RESYNC_PACK.md entry | D20; SR-156; SR-137 | IF-179; IF-286 (adopter-facing prose naming them) | P1; P2; P3; P5; P6; P8 |
| P11 | The bar on the lane tip, the full suite, the gate, and the landing; the bar again on the landing tip | D21; SR-156; SR-170; SR-137; TC-325; TC-326; TC-206; TC-150; TC-139; TC-145; TC-132; TC-205; TC-257; TC-259; TC-327; TC-328 | no interface (the bar, the gate and the squash cross no code seam) | P7; P9; P10 |

**Clauses covered by more than one row.** Each row does a separate part:

- **D1** (the heading "The trunk, declared" and its four cases): P2 builds
  the reader the cases depend on, and P3 adds the four cases.
- **D4:** P1 registers the key's type. P2 makes `trunk_name` refuse each
  shape. P3 makes each caller refuse in turn, and pins that a commit touching
  no claim copy is not refused.
- **D8:** P0 runs the reproduction first. P4 extracts the shared stage. P5
  adds the exemption and flips the fixture's assertion. If P0 does not
  reproduce, P4 and P5 drop (see "If P0 does not reproduce").
- **D18:** P4 moves the symbols, and P9 writes the `code_symbol` cells.

**The conditional rows.** P4 and P5 run only if P0 reproduces. If they drop:

- P0's fixture stays as a passing pin;
- P9's LLR-307 amendment drops the relink-exemption sentence (D13 says "if
  deliverable 3 stays");
- P9 writes D18's `code_symbol` cells unchanged (no symbol moved);
- the lane's log records deliverable 3 as dropped.

P6 then takes P3 as its predecessor in place of P5.

### P0: the relink reproduction fixture (D8, first)

The builder writes this before any other code change. It runs at the lane's
code as it stands, before P2, so it needs no trunk key: the fixture is a
single checkout on `main`, and today's `trunk_name` reads that correctly.

**The fixture.** It goes in `tests/test_done_when_blessing.py`, beside the
WI-921 trunk-arm tests, and reuses that module's `_git`, `_write`, `_commit`
and `_init`. Two claimed rows sit on trunk `main`:

- X: `docs/work/active/wi-x/WI-801-x.md`, with an ordinary Done-when;
- Y: `docs/work/active/wi-y/WI-802-y.md`. Y's Done-when has an item whose
  text carries a markdown link to X's spec,
  `[X](../wi-x/WI-801-x.md)`.

Both are committed on `main` in claim-subject commits. Then:

1. Cut a linked worktree on `wi-x` from `main`.
2. In that worktree, close X the way the ritual does: `spec_move.move_spec`
   moves the spec to `docs/archive/work/complete/WI-801-x.md`. The builder
   checks the call shape against `spec_move`'s CLI before using it. The move
   relinks every inbound link, Y's claim copy included. Commit it.
3. On `main`, run `git merge --squash wi-x`. This is the landing recipe.
4. Read `integrate.staged_done_when_refusal(main_root)`. That is the reader
   the hook's `done-when-blessed` step runs.

**The tests P0 adds.** Each asserts what the code does today.

- `test_a_squash_landing_that_relinks_another_claims_done_when_link_is_held`.
  It asserts the refusal names WI-802. If the assertion holds, the defect
  reproduces. P5 then flips the test to assert `None`, and renames it
  `..._is_not_held`.
- `test_a_squash_landing_with_a_real_edit_beside_the_relink_is_held`. The
  setup is the same, plus a reworded Y Done-when item, staged on `main`
  after the squash. It asserts the refusal names WI-802. It holds both
  before and after P5, and it is the pin that the exemption stays narrow.
- `test_a_relink_reaching_an_existing_lanes_claim_copy_across_the_landing`.
  These are C2's probes. They run on ONE history of Y's lane, built in this
  order (revision 2, F1). The point is that Y's lane exists, with Y's
  original link, before X lands:
  1. **Y's lane, cut before X lands.** After both claim commits, and before
     step 1 of the fixture above, cut a second linked worktree on `wi-y`
     from `main`. In it, commit one ordinary work file (say
     `src/y.txt`) that does not touch Y's spec. Record the shas: `y_claim`
     (Y's claim commit on `main`), `y_fork` (the merge base of `wi-y` and
     `main` at this point), and `y_tip0` (the lane tip). At `y_tip0`, Y's
     copy under `active/wi-y/` still links `../wi-x/WI-801-x.md`.
  2. **X lands.** Run the fixture's steps 1 to 3 and commit the squash on
     `main`. For this test the commit goes through `git commit
     --no-verify`, because the module does not install the hook; the
     same-delta hold is the first test's job, not this one's. Record
     `x_land`. Trunk's copy of Y under `active/wi-y/` is now the relinked
     one. The `wi-y` lane is untouched.
  3. **Probe (ii), the merge slot before Y refreshes.**
     `integrate._done_when_refusal(main_root, "wi-y", ["WI-802"])`. It
     compares the claim copy at trunk's HEAD (`x_land`, relinked) with the
     lane tip (`y_tip0`, original link). This is the "disagreeing" pair.
     The test also asks the build hold at the same point, with
     `kdone.lane_hold(lane_root, "HEAD", y_fork, "wi-y", ["WI-802"])`, so
     both readers of the un-refreshed lane are recorded.
  4. **Y refreshes.** In the `wi-y` worktree, `git merge --no-edit main`.
     That is the station refresh's merge of trunk in (`integrate.py`'s
     `refresh` docstring). The bar and trunk_step parts of the refresh are
     not needed to move the claim copy, so the test runs the merge alone.
     The builder confirms that against `integrate.refresh` and says so in
     the test's docstring. Record `y_tip1`. The lane's copy is now the
     relinked one.
  5. **Probe (i), the build hold after the refresh.** `kdone.lane_hold(lane_root,
     "HEAD", base, "wi-y", ["WI-802"])` twice. The first `base` is the
     lane's integration base as the worker reads it, the merge base of
     `wi-y` and `main` after the refresh (now `x_land`). The second is
     `y_claim`, the claim as the spec's sentence names it ("the claim
     (before the relink)"). The probe reads both. It does not go through
     `default_base` or `trunk_name`, because P0 runs before P2, and a
     switched or linked checkout would make today's `trunk_name` answer
     differently from the post-P2 reader. The base is computed with plain
     `git merge-base`. The merge slot is asked again here too, at `x_land`
     against `y_tip1`.
  6. **Probe (iii), the mint when Y closes.** In the `wi-y` worktree, close
     Y the ritual way (`spec_move.move_spec` to
     `docs/archive/work/complete/WI-802-y.md`) and commit. On `main`, run
     `git merge --squash wi-y`, commit with `--no-verify`, and record
     `y_land`. Then call
     `intake.intake_after_merge(main_root, x_land, y_land, {"WI-802": "merged"}, "wi-y")`,
     the call this module's `_intake` makes. It compares the claim copy at
     `before` (trunk's copy before Y's landing, which is relinked) with the
     closed copy. The test also reads `kdone.blessing_owed` directly for the
     pair (`y_claim`'s copy, the closed copy), which is the "same pair" as
     the spec's sentence has it. That way the recorded outcome says which
     of the two pairs the mint really compares.

  Each probe asserts what it observes on the code as it stands: held
  (naming WI-802) or `None`, and minted or not. The builder fixes each
  assertion to that observed outcome. The test's docstring says which
  pairs each probe compares, by sha name, so the pin cannot be read as a
  check of a pair it did not build.

  P5 does not change these assertions, because the exemption reads only a
  move in the same staged delta, and none of these probes stages one
  (D8's "Anything else ... is still a change"). If one of them changes
  after P5, the exemption reaches further than ruled, and that fails the
  build.

**The recorded result.** The builder runs the three tests and writes the
outcome of each in the lane's log fragment,
`docs/log.d/WI-925-trunk-ref-update-done-when.md`, under "Relink
reproduction (D8)". The outcomes are:

- reproduced or not;
- for C2, the result of each probe at its step: (ii) the merge slot and
  the build hold before the refresh; (i) the build hold at both bases, and
  the merge slot, after the refresh; (iii) the mint and the direct
  `blessing_owed` read when Y closes.

By C2 (a), every C2 probe that holds is stated residue: an owner ruling
releases each. The fix is not widened for them. Each one that holds is a hold,
so it fails closed: P8's one list carries it beside the re-cut residue, and
P9's LLR-307 points to that list rather than restating it. If none holds, the C2 test
pins that no hold is raised, and the log says that the lane was cut before
the landing, so the "none" covers the case the spec names.

### P1: the declared key (D7; part of D4)

- **Section.** The key goes in `[policies]`. The trunk's name is
  repository-wide authority over holds and gates, which is that section's
  role, and it needs no new header. The template line goes after `blackout`:

  ```toml
  # The integration branch (trunk) by name: the branch every lane is cut from
  # and lands on. Every reader that needs the trunk reads this line, in any
  # worktree; nothing guesses it from the branch a checkout is on. Absent,
  # empty, not a string, or naming no local branch, each of those readers
  # refuses and names this line. bootstrap.py writes it from the branch it
  # scaffolds on.
  trunk = "main"
  ```

  The comment keeps the greppable one-key-per-line shape (`process_shape_findings`).
- **This repository** (deliverable 8). `docs/process.toml` gains
  `trunk = "refactor_again"`. That is the branch every lane here is cut from
  and lands on today (the primary checkout's branch, and every recent lane's
  merge base). The value is the owner's: see risk R1.
- **Schema.** `agent_policy.PROCESS_ONLY_KEYS` gains
  `("policies", "trunk"): "str"`, with a comment saying why it is typed: a
  bare `trunk = 1` would otherwise read as absent with no diagnostic.
  `config_conflicts` then refuses a non-string value through
  `_key_value_findings`, like every dial. Emptiness and branch existence are
  `trunk_name`'s job (P2), not the config check's. The config check reads no
  git.
- **Bootstrap.** A new step in `apply_declared_policies` runs only when
  `docs/process.toml` was created by this run (`PROCESS_TOML_REL in
  outcome.created`). An adopter's existing file is never rewritten. The step:
  - reads `git -C <dest> symbolic-ref --short -q HEAD`. That names the
    branch even in an unborn repository, which is the branch git will create
    on the first commit;
  - writes it through `set_process_key(dest, "policies", "trunk", name)`;
  - when `dest` is no git repository, or HEAD is detached, keeps the
    template's value and prints one NOTE naming the key and the line to set.

  `--dry-run` prints and writes nothing, like the steps beside it.
- **The test helper** (deliverable 8, "one helper"): `conftest.declare_trunk(root,
  branch="main")`.
  - When `docs/process.toml` is absent, it writes the minimal file
    `[policies]\ntrunk = "<branch>"\n`. It does not seed the whole template,
    so a fixture gains no other dial.
  - Otherwise it calls `bootstrap.set_process_key(root, "policies", "trunk",
    branch, add_if_missing=True)`.

  Each fixture commits the file in its seed commit.

**Tests P1 adds:**

- `tests/test_process_config.py::test_a_non_string_trunk_is_refused_by_the_config_check`.
  `[policies]\ntrunk = 1\n` makes `config_conflicts` name `trunk` and
  "expected str". It fails before, because the key is unregistered and
  nothing is refused.
- `tests/test_bootstrap.py::test_a_scaffold_declares_the_branch_it_was_scaffolded_on`.
  It runs bootstrap into a fresh `git init` whose HEAD is set by
  `symbolic-ref` to `refs/heads/trunk-x` and is still unborn, then reads the
  key. A second case runs into a repository with a commit on `dev`, and both
  read back their branch. A third case, a non-repository destination, keeps
  `main` and prints the NOTE. It fails before, because the scaffolded file
  has no key.
- `tests/test_dogfood_sync.py::test_the_policy_home_declares_the_trunk_as_a_string`.
  It asserts that the template and `docs/process.toml` both declare
  `[policies] trunk` as a `str`. The existing section-by-section test then
  also holds it, once both carry it. It fails before, because neither
  declares it.

### P2: the reader (D6; part of D4 and D1)

- **`agent_common.TrunkUndeclared(ValueError)`.** It is the one refusal type,
  and its `str` is the message every caller prints. The message:
  - names `docs/process.toml [policies] trunk`;
  - states which shape failed: absent (including a file that does not
    parse), not a string, empty, or naming no `refs/heads/<name>`;
  - gives the line to add, `trunk = "<your integration branch>"`, under
    `[policies]`.
- **`trunk_name(root)`.** It reads
  `agent_policy.process_config(Path(root) / "docs")`, takes `[policies]
  trunk`, and requires a non-empty `str`. It confirms the branch with
  `git rev-parse --verify --quiet refs/heads/<name>`, then returns the
  name or raises.
  - The `worktree list` read, the `branch --show-current` read and the
    `worker` parameter are deleted.
  - `agent_brief`'s one call drops the `worker` argument.
  - The docstring's "HERE RATHER THAN IN agent_loop" paragraph stays. The
    sentence about the primary checkout goes.
  - It gains `Implements: SR-156, LLR-<new>`.
- **`default_base(root)` loses its claim-record arm.** The spec asks for the
  reading of the case that still reaches the arm. The arm runs only when the
  current branch equals the trunk name. Its docstring's case, a single
  checkout switched to the lane branch where the merge base "collapses to
  HEAD", arose because the current branch was read as trunk. With a declared
  trunk:
  - on a lane branch, the current branch is never the trunk. So
    `merge-base(trunk, HEAD)` is the lane's fork point, or its last refresh
    point, in a single checkout exactly as in a linked worktree;
  - on the trunk branch itself, `claim_base` looks for a claim subject
    `-> active/<trunk>`, which no claim writes. The arm then returns
    nothing, or `None` on an unreadable log.

  So no supported shape still needs the arm. It is deleted, and with it the
  "unreadable claim history" `None`. `default_base` now returns the merge
  base, or `head_sha` when there is no merge base, which is `None` only on an
  unborn HEAD. It lets `TrunkUndeclared` propagate.
  - `claim_base` stays. The worker's `claim` field, `dispatch` and the merge
    gate (WI-884) read it.
  - The ruled open item behind the arm (the 2026-09-03 "default_base goes
    blind on a resumed single-checkout worker", option (a)) stays met. The
    resumed single checkout reads a non-empty `base..HEAD`, and the test
    below pins it.
  - The docstrings that cite the old collapse change too:
    `agent_loop.py` near line 3138, `agent_brief.py` near line 1190, and
    `gen_verdict_rollup._off_trunk_refusal`'s.
- **Fixtures.** Each fixture builder that runs a trunk reader calls
  `declare_trunk` in its seed. The builder finds them with
  `grep -n "default_base\|trunk_name\|staged_done_when_refusal\|_off_trunk_refusal\|_lane_verdict\|staged_lines\|reviewer_prompt\|review_round_brief" tests/`
  and then with the full suite. The known set:
  - `tests/integrate_fixtures.py::git_repo`;
  - `test_done_when_blessing._init`;
  - the repo builders in `test_agent_loop_review.py` and
    `test_agent_loop_worker.py` (`_make_train_repo`);
  - `test_verdict_record.rounds_repo`;
  - the `test_handback`, `test_plan_gate`, `test_check_readability`,
    `test_step_path_trigger`, `test_integrate_admission` and
    `test_session_keep` repo builders.

  No test gets a copy of the key line.

**Tests P2 adds or changes:**

- New `tests/test_trunk_name.py`, in-process with no subprocess beyond
  `git`. It is kept off `SLOW_MODULES`, so the reader has a smoke-tier pin:
  - `test_a_repository_with_the_key_reads_it_and_one_without_refuses`. One
    real repository with two branches. Its primary checkout sits on `side`
    and the key names `main`, so the answer is `main`. Without the key it
    raises `TrunkUndeclared` naming `trunk`. It fails before, because the
    old reader answers `side` and never raises.
  - `test_the_reader_reads_no_worktree_list_and_no_current_branch`.
    `monkeypatch` wraps `ac.git` to raise `AssertionError` on
    `worktree list` or `branch --show-current`, then reads a declared trunk.
    It fails before, because the old reader runs `worktree list` first.
  - `test_each_undeclared_shape_is_refused_naming_the_key`, parametrized
    over the key absent, `trunk = 1`, `trunk = ""`, `trunk = "nosuch"`, and
    an unparseable `docs/process.toml`. Each raises `TrunkUndeclared`, and
    its text names `[policies] trunk` and the line to add. It fails before,
    because the old reader falls back and never raises.
- `tests/test_agent_loop_review.py::test_default_base_reads_the_claim_record_after_a_single_checkout_resume`
  is renamed to `test_default_base_keeps_the_trunk_boundary_after_a_single_checkout_resume`.
  - Its single-checkout half now asserts `default_base(trunk) == trunk_tip`.
    Before, it asserted the claim.
  - It keeps every evidence assertion: WI-1 is built, WI-777 is not, the
    endstate is DONE, and the row is not a stale terminal.
  - It fails before on the `trunk_tip` equality, because the old arm returns
    the claim commit.
- `test_default_base_refuses_an_unreadable_claim_history` is deleted with its
  arm. `test_default_base_lets_an_undeclared_trunk_refusal_through` replaces
  it, and `default_base` on a repository with no key raises
  `TrunkUndeclared`. That fails before, because the old reader never
  raises.
- `tests/test_agent_loop_worker.py::test_a_single_checkout_worker_keeps_the_terminal_refusal`
  gains the key and asserts the same as before.

### P3: every caller refuses in turn (D1 to D5)

Each caller catches `ac.TrunkUndeclared` at its own refusal shape:

| Caller | On `TrunkUndeclared` |
|---|---|
| `agent_loop` worker preflight (`base = ... or default_base(root)`) | prints the message, returns `EXIT_PREFLIGHT` |
| `agent_brief.reviewer_prompt` (the `{trunk}` slot) | raises `prompts.PromptError(str(exc))`, the brief's existing named refusal |
| `review_brief` (both `default_base` reads) | raises `BriefError(str(exc))`, which its `main` already reports |
| `adjudicate_brief._subject_claim` and the dispute brief's base read | raise `BriefError(str(exc))` |
| `gen_verdict_rollup._off_trunk_refusal` | returns the message as its refusal (exit 2). It reads the current branch first, and a detached HEAD still returns `""` without asking for the trunk, as today. |
| `handback._lane_verdict` | lets the exception through. `_machine_line_refusal` catches it and returns the message as the close's refusal, so a close cannot read "no verdict file" where the trunk is unknown. |
| `integrate.staged_done_when_refusal` | wraps the `kdone.staged_hold` call and returns the message. `staged_hold` calls `trunk_name()` and `lane_base()` only for a listed claim-copy change, so a commit touching no claim copy never reaches the read. |
| `plan_gate._claim_base` | reordered: when HEAD holds no `docs/work/active/<branch>/` folder (trunk, or any branch with no claim), it returns `"HEAD"` without calling `default_base`. Otherwise it calls `default_base`, and `TrunkUndeclared` becomes a hold line naming the key. The answer is unchanged where the key is declared, because `default_base` on such a branch was the merge base with itself, HEAD. |
| `check._changed_paths` (work-branch, empty-index arm) | maps the refusal to `None`, "changes unknown", so every opted-in step runs. That fails toward more checking, never toward a skipped step. |
| `check_readability._range_and_rev` | maps it to `None`, its existing "cannot be read" answer |
| `agent_common.stale_terminal_assignment` | maps it to `True`, the refusal it already fails toward |

The first seven are deliverable 2's named callers. The last four are
`default_base`'s other readers, which the grep found. Each keeps its existing
fail-closed answer, because a crash in a hook step would refuse every commit
over a key the commit does not need.

**Tests P3 adds.** Each is in the module that already holds its caller's
tests:

- `tests/test_done_when_blessing.py::test_a_linked_worktree_on_the_declared_trunk_holds_an_unblessed_done_when_change`
  (D2).
  - The primary checkout is on `side`. A linked worktree is on `main`, the
    declared trunk. A staged non-close Done-when change of WI-007's claim
    copy is refused, and passes once `_bless` puts a covering verdict in the
    index.
  - A second case does the same with an owner ruling (`done_when =
    "<digest>"`).
  - It fails before: the old reader reads `side` as trunk, so the change is
    "elsewhere" and is not judged (`None`).
- `test_a_single_checkout_on_a_branch_not_named_for_its_claim_does_not_judge_a_non_close_change`
  (D3). The single checkout is switched to `side`, and a staged non-close
  Done-when change gives `None`. It fails before, because the old reader
  reads `side` as trunk and holds it.
- `test_an_undeclared_trunk_refuses_each_caller_naming_the_key` (D4),
  parametrized over the four shapes. On each it asserts:
  - `staged_done_when_refusal` on `main` with a staged non-close change
    names `trunk`;
  - the worker preflight (`agent_loop` run as the module's existing
    preflight tests do) exits `EXIT_PREFLIGHT` naming `trunk`;
  - `reviewer_prompt` raises `PromptError` naming `trunk`;
  - `gen_verdict_rollup.main` returns 2 naming `trunk`;
  - `handback._machine_line_refusal` returns text naming `trunk`.

  It fails before, because nothing refuses.
- `test_a_commit_touching_no_claim_copy_is_not_refused_over_the_key` (D4's
  last sentence). With no key, a commit staging `notes.txt` on `main` gets
  `staged_done_when_refusal(...) is None`, and `plan_gate.staged_lines(...)
  == []`. It pins that no trunk read happens there. It passes before and
  after, and guards P3's `plan_gate` reorder. Without the reorder it fails
  after P2.
- `tests/test_agent_brief.py`, or the module that holds `reviewer_prompt`'s
  tests (the builder confirms which):
  `test_the_reviewer_prompts_trunk_slot_renders_the_declared_name` (D5). In
  a linked worktree on a lane, with the primary checkout on `side` and the
  key naming `main`, the rendered brief's trunk slot is `main`. It fails
  before, because the slot rendered `side`.
- `tests/test_verdict_record.py::test_a_work_branch_cannot_write_the_rollup_but_the_trunk_step_can`
  (D5, LLR-208). The test keeps its name, which TC-206's evidence cites. It
  gains a linked-worktree arm: with the primary checkout switched to `side`
  and a worktree on `main`, a write from that worktree returns 0. The lane
  worktree's refusal names "trunk is main". It fails before, because the old
  reader reads `side` as trunk and refuses the trunk worktree's write.

### P4: the shared relink stage (D8, D18; only if P0 reproduced)

This commit is the preparatory refactor, before its new caller.

- **The stage.** `spec_move.exact_relink(old, new, rel, remap) -> bool`. It
  is pure and takes bytes. It is `True` only when all of these hold:
  - `old` decodes as strict UTF-8;
  - `want = expected_relink(old_text, dirname(rel), remap)` differs from
    `old_text`. This is the non-empty rewrite;
  - `want.encode("utf-8") == new`, byte for byte.

  A `None` side is `False`. Docstring: `Implements: SR-156, LLR-145`.
- **How one stage serves both callers.** `plan_gate._relinked` requires a
  non-empty rewrite. `integrate._relinked_exactly` does not, but it guards
  `if not remap`. The stage requires a non-empty rewrite for both, and that
  subsumes the empty-remap guard, since an empty remap rewrites nothing.
  - For the claim recognizer, the stricter rule changes only one input: a
    listed `.md` modification whose old bytes the relink would leave
    unchanged. The ritual never writes such a file, because `_rewrite_md_links`
    writes only a file it changes. So the only entry it newly convicts is a
    mode-only change of a markdown file, which is not the ritual's write and
    is correctly no relink.
  - The plan gate's behaviour is unchanged.
- **The callers.**
  - `integrate._relinked_exactly` keeps its per-path loop and its raw reads
    (`_blob_bytes` of `tip^1:path` and `tip:path`), and calls
    `spec_move.exact_relink` for each path. Its `if not remap` and decode
    lines go.
  - `plan_gate._relinked` is deleted. Its call site in `build_paths` (and
    anywhere else the builder's grep finds) reads `plan_pass.blob` for both
    sides and calls `spec_move.exact_relink`.
- **Tests.** No new test here. The existing relink tests pass unchanged (D8):
  - `tests/test_integrate.py`: the CRLF relay, crashed-claim excuse and
    non-relink conviction tests (TC-145, TC-132);
  - `tests/test_plan_gate.py`: the close-homes relink tests (TC-367);
  - `tests/test_spec_move.py` (TC-139).

  The builder runs these three modules before and after the commit and
  records both results. Their bodies are not edited.
- **One pure test of the stage**:
  `tests/test_spec_move.py::test_exact_relink_is_the_rituals_bytes_and_nothing_else`.
  It covers a real relink, the same with a CRLF file, a non-UTF-8 parent, an
  empty rewrite, and one extra byte. Against the `HEAD` before P4 it fails
  with `AttributeError`, because the function does not exist.

### P5: the staged reader's exemption (D8; only if P0 reproduced)

- **`kitlib.done_when`.**
  - The index-delta read is split once. `_staged_delta(root)` returns
    `(entries, why)`. `staged_changes` classifies them, and `staged_hold`
    reads the entries once and uses them twice.
  - A new private `_relink_remap(entries)` returns `{active path: closed
    path}` for each close pair in the delta: a `D` under
    `active/<branch>/` with an `A` of the same work-item id under a closed
    folder (`_CLOSED_SPEC_RE`).
  - In `staged_hold`, a listed `("change", branch, wi_id)` is dropped before
    judging only when all of these hold:
    - its only entry is one `M` on one path;
    - the remap is non-empty;
    - `relinked(git_bytes(["show", "HEAD:" + path]), git_bytes(["show",
      ":" + path]), path, remap)` is `True`.

    Anything else stays a change: a second entry, a `D` and `A`, a `T`, a
    real edit beside the relink, an unreadable blob, or non-UTF-8 bytes.
    That keeps `classify_delta`'s deny-by-default unchanged.
  - **Signature.** `staged_hold(root, current_branch, trunk_name, lane_base,
    relinked)`. The oracle is injected because `kitlib` imports no script.
    `integrate.staged_done_when_refusal` passes `spec_move.exact_relink`.
    The module docstring's `Contract IF-286` text says so.
- **Tests.**
  - P0's first test is flipped to
    `test_a_squash_landing_that_relinks_another_claims_done_when_link_is_not_held`,
    asserting `None`. It fails before P5: P0 recorded the hold.
  - P0's real-edit test passes unchanged.
  - New: `test_a_relink_with_no_move_in_the_same_delta_is_still_a_change`. It
    hand-stages the relinked bytes of Y's copy on `main` with no move of X
    in the index, and the change is held. It pins the "same delta" bound.
    It passes before and after.
  - The C2 test keeps its recorded assertions.

### P6: `staged_closes` deleted (D10; call C1)

`kitlib/done_when.py` loses the function, its `__all__` entry, and its
sentences in the module docstring and in the `Contract IF-286` text. Its two
test assertions (in `tests/test_done_when.py`, per WI-921's plan; the
builder confirms by grep) move to `staged_changes`, asserting the same
closes through `kind == "close"`.

**Check:** `git grep -n staged_closes -- project-trajectory/scripts
project-trajectory/hooks tests` is empty. `RESYNC_PACK.md` is the one shipped
file that names it. WI-921's historical entry names it, and deliverable 9
requires this row's entry to say it is gone. That is a record of the removal,
not a use, and the plan reads D10's "no shipped file" as code, hooks and
tests. The coordinator confirms or overrules that reading at the checkpoint.

### P7: the hold-by-rename remedy (D11)

`check_trajectory.holdbyrename_findings` stops offering "or delete the
stranded claim". On trunk the floor refuses that commit, and no blessing
releases it. The new remedy is the route `handback` supports. `close_partial`
works on the lane's branch, so the branch ref must exist first. The text:

> close it PARTIAL through the kit's own path: restore `refs/heads/<branch>`
> first (rename the held ref back, or `git branch <branch> <sha>` at the
> claim commit, the one whose subject ends `-> active/<branch>
> (bookkeeping)`), then close the lane partial (the handback report) and
> land that close through the merge slot.

The builder confirms against `handback.close_partial` that a lane restored at
its claim commit closes partial. That is a lane with no commits past the
claim.

**Test:** `tests/test_trajectory_holdban.py::test_the_finding_names_a_recovery_the_trunk_floor_permits`.
On the renamed-ref fixture, it asserts that the output does not contain
"delete the stranded claim" and does contain `git branch` and "PARTIAL". It
fails before, because the old text offers the deletion.

### P8: the hook comment (D9)

The `done-when-blessed` comment in `project-trajectory/hooks/pre-commit` is
rewritten from deliverable 4, with WI-921's first sentences kept:

- **The promise.** Over the supported routes onto trunk (an ordinary commit,
  the squash landing, a hand close), a trunk commit is judged against its
  parent, on the declared trunk (`docs/process.toml [policies] trunk`), in
  any worktree.
- **The one residue list**, under PROCESS.md section 6's threat model. The
  comment cites the section; PROCESS.md is not edited.
  - "The routes outside it, each fails open:" and then the seven items of
    deliverable 4, in its order: amend; cherry-pick, revert or rebase; a
    plain `git merge` making a merge commit (the slot judges its own merge
    first); a hand fast-forward; git failing mid-commit at the work-tree
    question; the merge-time mint skipping an unreadable closed spec; a
    detached HEAD's non-close change (C3: this list holds it).
  - The comment's existing line stays: the landing sweep's mint flags
    after the fact.
- **The fail-closed residue that stays.** No route returns a claimed spec to
  the queue, so a hand return or re-cut of a claim copy on trunk is held.
  Beside it, by C2 (a), each C2 probe that P0 recorded as holding: a relink
  reaching a claim copy outside the same delta (an existing lane's merge
  slot or build hold after another row's landing, or the mint at its
  close) is held, and an owner ruling releases it.
- **Gone.** The single-checkout sentence goes. The linked-worktree shape was
  never in the comment, and it stays out. The count matches the list:
  "seven routes fail open, one fails closed", plus one more closed shape
  if P0 recorded a C2 hold. The count is written from the list as built.
- **The relink** (only if P5 stands). One sentence: a claim copy rewritten
  only by the inbound relink of a spec move in the same commit is not a
  change.

**Check:** a read-back against deliverable 4's list. Also, `grep -n "single
checkout\|primary checkout\|linked worktree" project-trajectory/hooks/pre-commit`
shows none of the dropped shapes. If WI-922 lands first, the block rebases on
its text (spec S6), and its entry is not touched.

### P9: the spine (D12 to D19)

The rows are authored in the lane, then judged at the lane's checkpoint
sitting, which ends with its act.

- **LLR-307** (D13):
  - The trunk sentence becomes "on the declared trunk, the branch the policy
    home names, in any worktree".
  - The residue sentences (amend, cherry-pick, the linked-worktree sentence)
    are replaced by one bound: "routes outside the supported commit routes
    are stated once, as residue, in the shipped hook's `done-when-blessed`
    comment".
  - The relink exemption is stated: a claim-copy modification whose bytes
    are exactly the inbound relink of a spec move the same staged change
    carries is not a change. Only if P5 stands; C2 residue named if P0's
    probes held.
  - "The close listing returns an unreadable staged-change reason with its
    closes." goes, with `staged_closes`.
  - `code_symbol`: `staged_closes` out; `_staged_delta` and
    `_relink_remap` in (P5).
- **LLR-208** (D14). "agent_common.trunk_name, the PRIMARY checkout's
  branch, so a single-checkout repo is its own trunk" becomes "the declared
  trunk (agent_common.trunk_name), in any worktree; with the trunk
  undeclared, the write is refused naming the declaration".
- **New LLR under SR-156** (D15), the next free id (LLR-339 today; another
  lane may take it first). Module `project-trajectory/scripts/agent_common.py`.
  `code_symbol = "TrunkUndeclared/trunk_name/default_base"`.
  - Title: "The trunk is one declared name".
  - Detail: the spec's proposed text (Scope answers S5), plus two
    sentences: the scaffold writes the declaration from the branch it
    scaffolds on, and a lane's integration base is its merge base with the
    declared trunk, in a single checkout as in a linked worktree.
  - `test_refs`: the new TC.
- **New TC** verifying SR-156, the new LLR, IF-179 and IF-189 (the next free
  id; TC-369 today):
  - Method: run `tests/test_trunk_name.py` and the P1, P2 and P3 tests.
  - Expected: the D1, D4, D6 and D7 outcomes.
  - Evidence: those node ids.
- **TC-325** (D16):
  - The method and expected name
    `test_a_trunk_commit_deleting_a_claim_copy_is_held_and_no_blessing_releases_it`
    (the deletion-only pin) and assert its outcome.
  - They gain P3's D2, D3 and D4 staged-arm tests and P0/P5's relink tests,
    or, if P5 dropped, the passing pin.
- **IF-179** (D17). Data: `trunk_name(root) -> the declared trunk's name, or
  raises TrunkUndeclared naming the key`. The notes drop "re-deriving it from
  git worktree list".
- **IF-286** (D17). The data cell points to the owner module's contract, and
  that contract text (P5, P6) carries the change: `staged_closes` gone, and
  `staged_hold`'s injected `relinked` oracle. Only the `notes` cell changes,
  if the sitting wants the change named.
- **IF-189** (not in D17's list; see the delta). Data:
  `default_base(root) -> the merge base with the declared trunk (HEAD on an
  unborn or unrelated history), or raises TrunkUndeclared`.
- **`code_symbol` cells** (D18). If P4 stood:
  - LLR-145 gains `exact_relink`;
  - LLR-337 loses `_relinked`;
  - LLR-151 is unchanged, because `_relinked_exactly` is not in its cell and
    stays in `integrate`. The sitting records that it was checked.

  If P4 dropped, all three are unchanged.
- **Unchanged** (D19): SR-156, SR-170, SR-137, SR-019, LLR-309 and TC-326.
  The builder confirms with `git diff --stat <claim base> --
  docs/requirements docs/test` that none of them moved.
- **Checks:** `trace.py --strict` and `check_trajectory.py --strict` are run
  before the sitting.

### P10: the RESYNC_PACK.md entry (D20)

There is one entry, anchored at the landing's parent, in the house shape:
"What changed", "Kit-owned files — overwrite", "What to do". Its heading is
"The trunk is declared by name; a spec move's relink is not a Done-when
change".

- **Forced migration.** Add `trunk = "<integration branch>"` under
  `[policies]` in `docs/process.toml`. Until the line is there, every route
  that reads the trunk refuses and names it: the worker preflight, the
  review briefs, the rollup write, the partial close, and the done-when step
  on a claim-copy change. `process.toml` is never replaced; this is a new
  setting the adopter takes.
- **The residue list.** It replaces WI-921's "One residue fails open"
  paragraph, by reference to the hook comment, and states the promise.
- **`staged_closes` is gone.** Read `staged_changes` and filter on
  `kind == "close"`.
- **`default_base`** no longer reads the claim record. On a branch it
  answers the merge base with the declared trunk.
- **Kit-owned files, one set:**
  - `process.toml.template` (reference only; the adopter adds the line);
  - `hooks/pre-commit` (re-copy to `.githooks/pre-commit`);
  - `scripts/agent_common.py`, `scripts/agent_policy.py` and
    `scripts/bootstrap.py`;
  - `scripts/agent_brief.py`, `scripts/agent_loop.py`,
    `scripts/review_brief.py` and `scripts/adjudicate_brief.py`;
  - `scripts/gen_verdict_rollup.py`, `scripts/handback.py`,
    `scripts/integrate.py` and `scripts/plan_gate.py`;
  - `scripts/check.py`, `scripts/check_readability.py` and
    `scripts/check_trajectory.py`;
  - `scripts/spec_move.py` and `scripts/kitlib/done_when.py`.

  The builder trims the set to the files the landing diff actually touches.

### P11: the bar and the landing (D21)

1. On the lane tip:
   - the commit bar, `run.cmd smoke` (the smoke tier within 60 s; the wall
     time is pasted);
   - `check_trajectory.py --strict`;
   - `trace.py --strict`;
   - the size and complexity ratchets. `agent_common.py`, `kitlib/done_when.py`,
     `integrate.py` and `plan_gate.py` move. Each stamp change is a reviewed
     bump or down-stamp with its reason, per
     `tests/test_module_size_ratchet.py`'s convention.
2. The full unfiltered suite, `python -m pytest -q -n auto`, at phase close.
   Its output is pasted.
3. The coordinator's fresh full-lane gate over that tip.
4. The landing by the squash recipe. The trunk-only views are regenerated,
   and the bar runs again on the landing tip: smoke, `check_trajectory.py
   --strict` and `trace.py --strict`, each pasted.

The TCs this row names but does not amend are run here, unchanged, through
their evidence modules: TC-150, TC-139, TC-145, TC-132, TC-205, TC-257,
TC-259, TC-327, TC-328 and TC-326.

## Risks

- **R1: this repository's value.** `docs/process.toml` will say
  `trunk = "refactor_again"`. When the owner moves the trunk (for example,
  back to `main`), that line must move in the same commit, or every trunk
  reader refuses. That is loud, not wrong. The owner should confirm the
  value at the checkpoint.
- **R2: CI checkouts.** GitHub Actions checks out a detached HEAD and may not
  fetch `refs/heads/refactor_again`. A test that runs a trunk reader against
  this repository's own root would then refuse in CI. The builder greps
  `tests/` for trunk readers called with `ROOT`, and points each one at a
  fixture or declares the trunk in a temporary copy. A test that hits this
  has a real dependency on the developer's box and is fixed, not skipped.
- **R3: fixture blast radius.** P2 makes the key mandatory for every fixture
  that reads the trunk. The known builders are listed in P2. The full suite
  is the arbiter, and each fix is one `declare_trunk` call in a fixture
  builder, never a copied key line.
- **R4: the smoke budget.** The new git-fixture tests go in modules already
  in `SLOW_MODULES` (`test_done_when_blessing`, `test_verdict_record`,
  `test_bootstrap`, `test_process_config`, `test_trajectory_holdban`), except
  `tests/test_trunk_name.py`, the in-process pin the smoke tier keeps for the
  reader. The smoke wall time is re-measured at P11.
- **R5: WI-922 and WI-926** share the hook comment block, and WI-922 also
  shares `plan_gate.py` (`_cap_problems`, next to P4's `_relinked`). The two
  rows share no function. Whichever lands second rebases (spec S6).

Excludes: TC-060; TC-130; TC-131; TC-144; TC-317 — they verify the trunk step's log compile and regeneration, the tracked pause, the lane and dispatch mechanics, and the coordinator context guard, none of which reads the trunk name, the lane base or a claim copy's Done-when; they run unchanged in P11's full suite.
