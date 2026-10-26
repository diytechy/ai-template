# WI-971 plan — the per-commit rules share one walk, and the work specs one listing

Item: `docs/work/active/wi-971/WI-971-adoption-record-shared-walk.md` (planmode
`single`, anchor SR-148, specref `docs/decisions/wi-969.toml` D-022 and D-027).
Lane: `wi-971`. The row changes no behaviour. It moves three copies of one
traversal and two copies of one listing onto a shared stage each, below every
caller.

DELTA: none

Why none. The WI adds no state, no domain value, and no input any output
depends on. It crosses no new boundary. The code moves into two modules
`docs/kernel-modules-allow` already declares shared kernels, `kitlib/git.py`
and `kitlib/registry.py`, and every caller already imports one of them
(`text_then_act`, `adoption_record`, `plan_gate`, `check` and `integrate` import
`kitlib.git`; `acceptance_record` and `adoption_record` import
`kitlib.registry`). The cross-component rule exempts an edge into a declared
kernel, so the move needs no IF row. One edge is added inside the kernel
(`kitlib.registry -> kitlib.git`, both CMP-006, with no cycle because
`kitlib.git` imports no kitlib module), and one edge goes away
(`plan_gate -> text_then_act`). No row of `docs/requirements/interfaces.toml`
changes its owner, requestors or data: IF-303 still lists `tree_specs`,
`validate_at` and `commit_adoption_record_lines` with the same results, and
IF-304 and IF-295 keep their argv and exit codes. No component row of
`docs/requirements/components.toml` changes. The only registry edits are
traced cells (LLR `module`/`code_symbol`, TC `evidence`). These are silent by
ruling (`acceptance_record.SPINE_TRACED_CELLS`; coordinator-cycle §3: "traced-only
updates owe no sitting"), so no spine row is authored and no sitting is owed.
In `docs/runtime-flows.md`, Flow 3 (the pre-commit floor) and Flow 4 (the merge
slot) keep every participant and step: the walk is still called by the same hook
steps and by the same slot rung.

## Reading of the Done-when

- **D1, "each rule keeps its own range read, refusal text, remedy and squash
  policy".** Read as follows. The owner holds only what the copies share:
  - the HEAD / MERGE_HEAD read of the commit being made;
  - the walk (each listed commit, oldest first, each rider in turn, lazy);
  - the staged squash's HEAD..tip step (does the tip contain HEAD, list the
    range, walk it).

  Each rule keeps four things to itself:
  - **what an unlistable range means**, passed in as the rule's own line, or
    None. Text then act reads None as "no squash to exempt", and the adoption
    record refuses with its own line.
  - **its refusal text and remedy.** These stay inside its riders and its hint
    constants (`SQUASH_REBASE_HINT`, `SQUASH_HINT`, `REMEDY`,
    `TEXT_THEN_ACT_REMEDY`).
  - **its squash policy:**
    - Text then act and held-status admit a squash only when their paths are
      byte-equal to the tip's (`text_then_act.squash_walk`).
    - The adoption record also judges the index against `[HEAD, tip]`.
    - The plan gate walks HEAD..tip with no ancestry test, once per local
      branch containing the tip, and holds an unattributed tip by name.
  - **the slot's and the plan gate's own `--topo-order` range reads.**

  "The plan gate where it shares the shape" therefore means this: the plan
  gate rides the shared walk and the shared HEAD / MERGE_HEAD read. Its range
  read stays its own, because its policy differs on both counts (topo order,
  and no ancestry test).
- **D1, "no import cycle is needed to register a rider".** `LANE_COMMIT_RIDERS`
  stays in `text_then_act`, where `integrate` and three test modules read it.
  The walk moves below it, so `adoption_record` reaches the walk through
  `kitlib.git` and never imports `text_then_act`. Its docstring's cycle reason
  and `_squash_walk` are deleted.
- **D2, "each keeping its own view".** The listing returns every path under
  `docs/work` and `docs/archive/work`, at a tree or the index, whose file name
  begins `WI-` and ends `.md`, in git's order. That is the exact filter both
  copies apply today. The id reading stays in each view, so neither view's
  output changes:
  - `acceptance_record._tree_specs` returns `{id: path}`: the id is the file
    name's first two dash fields, a `-000` example is dropped, and the last
    path wins.
  - `adoption_record._spec_paths` returns `{id: [path, ...]}`: the id comes
    from `_SPEC_PATH`, and every path is kept, so `_spec_at`'s "N specs carry
    one id" refusal still fires.
  - `adoption_record.tree_specs` is the listing narrowed to `docs/work/`, its
    relpath taken from the work root.

  `_tree_text` becomes the module's one spec read, with `rev` None meaning
  the index, and `_spec_at` calls it instead of its inline copy. This is the
  second listing-plus-read pair the Context names.

## The design

**`kitlib/git.py`** (kernel; module docstring gains a "THE LANE-COMMIT WALK"
section stating that the owner never decides what an unlistable range means)

- `staged_heads(root) -> (head, merging)`: HEAD's id, `""` before the first
  commit; MERGE_HEAD's id, `""` when no merge is in progress (both read with
  `rev-parse --verify --quiet`, stripped).
- `lane_commit_walk(root, commits, riders)`: moved verbatim from
  `text_then_act`, its `riders` now required (the leaf knows no rider; every
  live caller already passes them).
- `squash_lines(root, head, tip, riders, unlisted)`: None when `tip` does not
  contain `head` (`merge-base --is-ancestor`); `unlisted` (the caller's own
  lines, or None) when `rev-list --reverse head..tip` fails; else every line
  `riders` report for those commits, oldest first, through
  `lane_commit_walk`.
- `squash_commits` is unchanged except that its docstring names the adoption
  record as a reader too.

The kitlib functions call one another, and their callers call them, through
module attributes (`_kitgit.lane_commit_walk`, never a `from ... import`
binding inside the three rules). The spy tests depend on that.

**Callers re-homed (stage A):**

- `text_then_act`:
  - `lane_commit_walk` is deleted.
  - `squash_walk(root, head, tip, paths, riders)` keeps its signature (check's
    held-status step calls it). It returns None unless the staged `paths` are
    byte-equal to the tip's, else `_kitgit.squash_lines(..., None)`.
  - `staged_text_then_act_lines` reads `staged_heads`, keeping its
    `squashed` parameter. The module still reads no file, and the existing
    tests call it with and without the parameter.
  - The module docstring and the `LANE_COMMIT_RIDERS` comment say the walk is
    `kitlib.git`'s.
- `adoption_record.staged_adoption_record_lines`:
  - It reads `staged_heads`. On a merge it is judged against `[head, merging]`
    as today.
  - Otherwise `walked = _kitgit.squash_lines(root, head, tip,
    (commit_adoption_record_lines,), ["cannot list the squashed commits
    {}..{}"...])` when a squash tip exists.
  - `walked is None` → judged against HEAD alone, plus `SQUASH_HINT` when a
    squash was in progress. Otherwise the result is `walked +` the index
    judged against `[head, tip]`. These are the same lines and the same order
    as today.
  - `_squash_walk` is deleted.
- `plan_gate`:
  - `staged_lines` reads `staged_heads`.
  - `landing_refusal` and `_squash_lines` call `_kitgit.lane_commit_walk`.
    `_squash_lines` keeps its `for-each-ref --contains` lane lookup, its
    `--topo-order` range, its read-failure line and `_unattributed_squash`.
  - `import text_then_act` is dropped (it is now unused).
- `integrate._each_lane_commit`: `from kitlib.git import git_out,
  lane_commit_walk` (one import line, so integrate's SLOC is unchanged). Its
  `--topo-order` range read and refusal text are unchanged.
- `check._held_status_refusal` reads `staged_heads`: the fourth copy of the
  HEAD / MERGE_HEAD read. `_held_squash_refusal` still calls
  `text_then_act.squash_walk`, so held-status's squash rides the shared walk
  with no further edit.

**`kitlib/registry.py`** (kernel; stage B)

- `WORK_SPEC_ROOTS = ("docs/work", "docs/archive/work")` and
  `tree_spec_paths(root, rev)`: `ls-files --` (rev None) or
  `ls-tree -r --name-only <rev> --` over both roots through
  `_kitgit.git_paths` (NUL-safe, so the quoted and non-UTF-8 path cases of
  `test_ruling_sync` keep passing). It keeps only names `WI-*.md`, in
  listing order, and returns None when git cannot list.
- `adoption_record.SPEC_ROOTS` becomes an alias of `WORK_SPEC_ROOTS`. It still
  scopes `_touched_ids`' diff. `acceptance_record`'s `WORK_DIR` /
  `ARCHIVE_WORK_DIR` stay, because other rules there read them.

## Steps

Two stages, in the order the spec fixes. Each stage is a tests commit
followed by a code commit, and the bar is green at every commit. The
tests-first commits follow coordinator-cycle §3 Intent:
- A test of new structure carries
  `@pytest.mark.xfail(strict=True, raises=(AssertionError, pytest.fail.Exception))`
  and reaches its own assertion. Spies are set with
  `monkeypatch.setattr(..., raising=False)`. A pin of a new function first
  asserts `hasattr(module, name)`. So the red is never an AttributeError.
- A characterization test is unmarked and states its adequacy witness in its
  docstring.
- The code commit removes the marks.

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | Stage A tests, committed alone: the in-process walk pin module and the three rules' squash-through-the-shared-walk tests (named under Tests) | D1; D3; SR-148; TC-383 | no seam (test modules only) | |
| P2 | The traversal owner in `kitlib/git.py`: `staged_heads`, `lane_commit_walk` (moved, riders required), `squash_lines` (ancestry, range listing, the caller's unlisted line), docstring section | D1; SR-148; TC-383 | no seam: `kitlib/git.py` is a declared shared kernel (`docs/kernel-modules-allow`), so caller edges into it need no IF row | P1 |
| P3 | Text then act, the held-status step, the merge slot and the plan gate onto the owner: `text_then_act.lane_commit_walk` deleted, `squash_walk` rebuilt on `squash_lines`, `staged_heads` in `text_then_act`, `plan_gate` and `check`, `integrate` and `plan_gate` calling `kitlib.git.lane_commit_walk`, `plan_gate`'s `text_then_act` import dropped; every rule's range read, refusal text, remedy and squash policy unchanged | D1; D3; SR-148; TC-331; TC-383 | IF-295 (plan-gate step, contract unchanged); IF-196 and IF-308 (held-status and parent-first riders, unchanged, still walked); IF-303 (`commit_adoption_record_lines` still a rider) | P2 |
| P4 | The adoption record onto the owner: `staged_adoption_record_lines` on `staged_heads` and `squash_lines` with its own unlisted line, `SQUASH_HINT` and index-against-`[HEAD, tip]` policy; `_squash_walk` and its import-cycle reason deleted; module docstring's "THE SQUASH LANDING" re-pointed | D1; D3; SR-148; TC-383 | IF-303; IF-304 (step argv, output line and exit codes unchanged) | P2 |
| P5 | Stage A bookkeeping, in P2–P4's commit: traced LLR cells, TC evidence, README rows, the RESYNC entry, module-size re-stamps (all listed under Bookkeeping) | D1; D4; SR-148; TC-383 | no interface (traced registry cells and docs) | P3; P4 |
| P6 | Stage B tests, committed alone: the in-process listing pin module and the real-git view characterization (named under Tests) | D2; D3; SR-148; TC-313; TC-383 | no seam (test modules only) | P5 |
| P7 | The one work-spec listing: `kitlib.registry.WORK_SPEC_ROOTS` and `tree_spec_paths`; `acceptance_record._tree_specs`, `adoption_record._spec_paths` and `adoption_record.tree_specs` become views over it, each keeping its id reading, duplicate handling and error; `_tree_text` becomes the one spec read and `_spec_at` calls it | D2; SR-148; TC-313; TC-360; TC-383 | IF-303 (`tree_specs` returns the same entries; contract unchanged); no seam for `kitlib/registry.py`, a declared kernel | P6 |
| P8 | Stage B bookkeeping, in P7's commit: traced LLR cells, TC evidence, README kitlib row, the RESYNC entry's overwrite list, re-stamps | D2; D4; SR-148; TC-313; TC-383 | no interface (traced registry cells and docs) | P7 |
| P9 | The landing evidence: the bar, the named suites, the unchanged-tests diff and the lints on the landing tip (commands under Verification) | D3; D4; SR-148; TC-383; TC-360; TC-313; TC-314; TC-156; TC-331 | no seam (verification only) | P8 |

Excludes: TC-058; TC-059; TC-060; TC-091; TC-097; TC-143; TC-146; TC-147; TC-154; TC-183; TC-254 — these verify SR-148's work-selection clauses: the frontier order and the safety classifier (`schedule`), the generated status surface (`trunk_step`, `gen_trajectory`), the dual-plan class, the admission table (`dispatch`), the adjudication kind's rank, the red-TC loop-order census, the intake replay (`intake`) and the consolidation close (`consolidate`). None of that code, nor anything it imports from the touched functions, changes here. Each still runs, unchanged, in the bar or the phase-close suite.

## Tests

Each test is listed with what it fails on before its stage's code. The tests
are named here and the builder keeps these names.

**P1 (stage A, new structure: strict xfail until P2–P4)**

- `tests/test_kitlib_lane_walk.py`: new, smoke tier, in-process, no git
  (`kitlib.git.git_out` replaced by a fake). It is the shared owner's own
  in-process pin. Before P2 every test fails at its `hasattr(kgit, ...)`
  assertion.
  - `test_the_walk_asks_each_rider_of_each_commit_in_order_and_skips_empty_reports`
  - `test_the_walk_is_lazy_so_a_caller_stopping_at_the_first_report_judges_no_later_commit`
  - `test_staged_heads_reads_head_and_merge_head_and_answers_empty_when_absent`
  - `test_squash_lines_is_none_when_the_tip_does_not_contain_head`
  - `test_squash_lines_answers_the_callers_line_when_the_range_cannot_be_listed`
    (and None when the caller passed None)
  - `test_squash_lines_returns_every_commits_lines_oldest_first`
- `tests/test_text_then_act.py::test_a_squash_landing_is_judged_through_the_shared_walk`
  - Fixture: the admitted rebased-lane squash from
    `test_a_squash_landing_is_admitted_only_when_its_lane_commits_pass`.
  - A spy wraps `kitlib.git.lane_commit_walk`.
  - Asserts the result is unchanged (`[]`), and that the spy saw exactly
    `rev-list --reverse HEAD..tip` with riders `(tta.commit_text_then_act_lines,)`.
  - Before P3 the spy is never called, because the walk is
    `text_then_act`'s own.
- `tests/test_adoption_record.py::test_a_squash_landing_is_judged_through_the_shared_walk`
  - Fixture: `test_a_rebased_lanes_squash_landing_is_admitted`'s.
  - Spy as above.
  - Asserts `ar.main` exits 0, and that the spy saw the HEAD..tip commits with
    riders `(ar.commit_adoption_record_lines,)`.
  - Before P4 the spy is never called, because `_squash_walk` walks privately.
- `tests/test_plan_gate.py::test_a_squash_landing_is_judged_through_the_shared_walk`
  - Fixture: the unbound build squashed onto trunk from
    `test_a_build_without_a_pass_record_is_refused_at_the_hook_and_the_landing`.
  - Spy as above.
  - Asserts `gate.staged_lines` still holds `src/app.py`, and that the spy saw
    `rev-list --reverse --topo-order HEAD..tip` with one rider whose
    `__qualname__` begins `lane_rider`.
  - Before P3 the spy is never called, because the plan gate calls
    `text_then_act.lane_commit_walk`.

**P6 (stage B)**

- `tests/test_kitlib_spec_listing.py`: new, smoke tier, in-process.
  - `test_the_listing_reads_both_spec_roots_at_a_tree_or_the_index`
    - `kitlib.git.git_paths` is replaced by a fake that records argv. The test
      asserts `ls-files --` for None and `ls-tree -r --name-only <rev> --` for
      a rev, over both roots.
    - It asserts the `WI-*.md` filter, listing order, and None for an
      unlistable tree.
    - Strict xfail: it fails at `hasattr(kregistry, "tree_spec_paths")`.
  - `test_one_listing_serves_both_views`
    - `kitlib.registry.tree_spec_paths` is replaced by a recording fake
      (`raising=False`). Its fixed listing holds WI-005 twice (queued, and
      archive complete), WI-000, and WI-007 under `active/<branch>/`.
    - Asserts `acceptance_record._tree_specs` gives single paths with no
      WI-000 and the last path winning.
    - Asserts `adoption_record._spec_paths` gives every path, WI-000 included.
    - Asserts `adoption_record.tree_specs` gives work-root relpaths only.
    - Asserts the fake was called once per view, and that a None listing gives
      None, OSError naming the tree, and OSError naming `docs/work`
      respectively.
    - Strict xfail: before P7 the fake is never called, because both views
      list for themselves.
- `tests/test_adoption_record.py::test_each_spec_view_keeps_its_shape_over_one_tree`
  - A characterization test, unmarked, real git, in that slow module. It is
    the same tree committed to a tmp repo, read at `HEAD` and at the index.
  - Asserts both views as above, plus `ar._spec_at(root, "HEAD", both_paths)`
    raising "2 specs carry one id".
  - Adequacy witness, in its docstring: it fails for an implementation that
    serves one view to both callers. Either duplicates collapse for the
    adoption record, so the refusal never fires, or `-000` and duplicates
    reach the ruling sync.
  - It passes before and after P7.

**Existing tests (D3)** are not edited: `tests/test_text_then_act.py`,
`tests/test_adoption_record.py`, `tests/test_plan_gate.py`,
`tests/test_ruling_sync.py`, `tests/test_held_status_git.py`,
`tests/test_parent_first.py`, `tests/test_disposition_adoption.py`,
`tests/test_handback.py` and `tests/test_integrate_admission.py` only gain the
functions above. The one sanctioned edit outside them is
`tests/test_module_size_ratchet.py`, re-stamped downward wherever a baselined
module shrinks (`check.py`, by one `staged_heads` line, and `acceptance_record.py`
if its SLOC moves). The ratchet's own rule requires that re-stamp.

## Bookkeeping (P5, P8)

Every edited registry cell is traced, so none needs a sitting.

- **LLR traced cells.**
  - Every LLR whose `code_symbol` names a moved symbol, or whose `Implements:`
    tag now sits in kitlib, gains `project-trajectory/scripts/kitlib/git.py`
    (stage A) or `.../kitlib/registry.py` (stage B) in `module`. In
    `code_symbol` it gains `staged_heads` / `squash_lines` / `tree_spec_paths`
    and loses `_squash_walk`.
  - Rows: LLR-345 (adoption record), LLR-298 (the slot's walk, `_tree_specs`),
    LLR-302 (text then act; already lists `kitlib/git.py`), LLR-337 (plan
    gate), LLR-358 (parent-first, lists `lane_commit_walk`), LLR-246
    (held-status, `squash_walk`; already lists `kitlib/git.py`), LLR-335
    (`tree_specs` / `_tree_text`).
  - The tags on the moved functions keep their LLR ids and add those of the
    rules now calling them (LLR-345, LLR-337).
  - `check_trajectory.py`'s CodeSymbol crosscheck must show no new finding on
    these rows against the lane base.
- **TC evidence** (traced): TC-383 gains the adoption squash-walk test, the
  view characterization and both pin modules. TC-173 gains the text-then-act
  squash-walk test. TC-367 gains the plan-gate squash-walk test. TC-313 gains
  `test_kitlib_spec_listing.py`.
- **Docs.**
  - `project-trajectory/README.md`: the `text_then_act.py` row stops claiming
    the walk ("It also holds the one lane-commit walk ...") and says the walk
    is `kitlib.git`'s, `LANE_COMMIT_RIDERS` still here.
  - The README's `scripts/kitlib/` row names the lane-commit walk and the
    work-spec listing.
  - Docstrings that cite `text_then_act.lane_commit_walk` (`plan_gate`,
    `integrate`, `adoption_record`, `held_status`) are re-pointed.
  - The `docs/kernel-modules-allow` reason for `kitlib/git.py` names the walk
    beside `git_out`.
- **RESYNC.** One `project-trajectory/RESYNC_PACK.md` §3 entry,
  "The per-commit rules share one lane-commit walk and one work-spec listing",
  anchored at the lane's trunk base as `scripts/check_resync.py` reads it.
  - Added in P5, its overwrite list extended in P8.
  - **What changed:** the walk and the squash range moved to `kitlib/git.py`,
    and the listing to `kitlib/registry.py`. `text_then_act.lane_commit_walk`
    is now `kitlib.git.lane_commit_walk`. Every refusal text, exit code and
    step line is unchanged.
  - **What to do:** no adopter action beyond taking the scripts. Nothing is
    migrated, and no setting or registry format changes. Code of the
    adopter's own that imported `text_then_act.lane_commit_walk` imports it
    from `kitlib.git`.
  - **Kit-owned files — overwrite:** `scripts/kitlib/git.py`,
    `scripts/kitlib/registry.py`, `scripts/text_then_act.py`,
    `scripts/adoption_record.py`, `scripts/plan_gate.py`, `scripts/integrate.py`,
    `scripts/check.py`, `scripts/acceptance_record.py`, `README.md`.
  - This satisfies D4: no migration is forced.
- **Trunk-only views** (`PROJECT_STATE.html`, `components.derived.toml`,
  `docs/interface-reference.md`, `docs/cli-reference.md`) are not committed in
  the lane. The landing regenerates them (coordinator-cycle recipes §3).

## Verification (P9; every command in the foreground, interpreter
`C:/Projects/ai-template/.venv/Scripts/python.exe`, from the lane root)

1. The named suites, including the slow modules the smoke tier drops:
   `python -m pytest -q -n auto tests/test_kitlib_lane_walk.py
   tests/test_kitlib_spec_listing.py tests/test_text_then_act.py
   tests/test_adoption_record.py tests/test_plan_gate.py tests/test_ruling_sync.py
   tests/test_held_status.py tests/test_held_status_git.py tests/test_parent_first.py
   tests/test_parent_first_git.py tests/test_disposition_adoption.py
   tests/test_handback.py tests/test_integrate_admission.py tests/test_import_layers.py
   tests/test_module_size_ratchet.py tests/test_complexity_ratchet.py
   tests/test_bootstrap.py tests/test_resync_pack.py`. Split it if one run
   would pass the 10-minute tool cap.
2. The commit bar: `python project-trajectory/scripts/run_menu.py smoke`
   (both strict lints, docs staleness, the RESYNC entry check, the smoke tier).
3. D3's "unchanged": `git diff <trunk base> -- tests/test_text_then_act.py
   tests/test_adoption_record.py tests/test_plan_gate.py tests/test_ruling_sync.py`
   shows added lines only (no `^-` line outside the hunk headers).
4. The import graph: `test_import_layers` stays green with its deferred window
   unmoved (no deferred edge is added; `plan_gate -> text_then_act` leaves at
   module level), and `grep -n "text_then_act" project-trajectory/scripts/adoption_record.py`
   finds no import.

## Risks and how the plan meets them

- **A spy that cannot see the call.** If a rule binds `from kitlib.git import
  lane_commit_walk`, the P1 tests stay red. The design requires attribute
  calls in the three rules and inside `kitlib.git`. `integrate`'s bound import
  is outside every spied path.
- **Line order on a lane with merges.** Text then act and the adoption record
  keep plain `rev-list --reverse`, while the plan gate and the slot keep
  `--topo-order`. No rule's order changes, so no existing assertion on joined
  lines moves.
- **Squash policy drift.** The adoption record keeps judging the index against
  `[HEAD, tip]` and does not adopt text then act's byte-equal-paths gate.
  Adopting it would refuse a lane close judged against HEAD alone. That is
  why `squash_lines` carries no paths, and the paths gate stays in
  `text_then_act.squash_walk`.
- **The listing narrowing a view.** The shared filter is the exact
  name filter both copies apply. `_SPEC_PATH`'s stricter grammar stays inside
  the adoption view only, so the ruling sync still sees every `WI-*.md` it saw.
