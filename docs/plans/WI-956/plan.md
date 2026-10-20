# WI-956 implementation plan: one tree-bound bar attestation

Spec: `docs/work/active/wi-956/WI-956-tree-bound-bar-attestation.md`
(specref: review-churn README item 13, precondition 2). Item SR: SR-156.
Planner: fresh session, read-only. Lane worktree: `C:/Projects/ai-template.wt/wi-956`.

Revision 2 (the plan's one allowed revision), answering critique round 1
(`docs/plans/WI-956/critique-1.md`, one finding).

## Disposition of the critique's findings

- **F1 [MAJOR], adopted: confirmed against the code.** P3's
  `test_the_refresh_and_attest_commit_through_one_producer` drives
  `integ.attest`, and the lane's `integrate.py` has no `attest` (nor
  `_attest_commit`) today; `attest` is first delivered by P5, which depends on
  P3. So P3 could not run its own stated test in the declared build order, and
  adding the edge P5 -> P3 would make a cycle. The fix moves that cross-route
  test, and its TC-205 evidence entry, to P5, where both callers exist. P3
  keeps one test it can run alone: the refresh commits through the producer
  (`test_the_refresh_commits_through_the_shared_producer`, wrapping
  `integ._attest_commit` and driving only `refresh`). D5 stays delivered by P3
  (the refresh writes `landing` / `no-bar` through the producer); P5 adds the
  proof that both routes share it. Rows P3 and P5 cite F1. No other row, edge
  or test changes.

## The architectural-delta question

The WI does three of the four things. It adds a **value to a domain**: the
`Bar-Green:` trailer gains a closed `bar=` set (`review`, `landing`, `no-bar`)
and a `tests=` field. It makes an **output depend on a new input**: a `review`
attestation is produced from the command declared in a new `docs/stack.ini`
key, `[bars] review`. And it **crosses a new boundary**: a new CLI verb,
`integrate.py attest`, on the integrator's argv, exit-code and call surfaces.
It adds no new state (no file, marker or store; the record is the commit
trailer, as it already is) and no new component or module. The verifier stays
in `kitlib/verdict.py`, so no Drafted IF row is minted (S5).

Every one of these changes sits inside modules this item owns
(`kitlib/verdict.py`, `integrate.py`) and on interface rows it amends in place
(IF-175, IF-173, IF-154, IF-080, IF-022). No refactor outside the lane is
needed. The table rows below make the change explicitly.

Revision 2 changes no part of this answer: F1 moves one test between rows and
adds no state, domain value, input or boundary.

DELTA: within

## Steps

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | Spine checkpoint, TC-first: amend LLR-207 (grammar, verifier, the landing restriction on `refresh_attestation`, the shared producer, `attest`) and amend TC-205, TC-132 and TC-370 to name the tests P2–P5 add, before any code | D1; D7; SR-156; TC-205; TC-132; TC-370 | no interface: registry rows only, no code seam crossed |  |
| P2 | One grammar and one verifier in `kitlib/verdict.py`: `format_bar_green`, `bar_attestation`, `tests_digest`, the `BAR_NAMES` / `LANDING_BARS` sets; `refresh_attestation` narrowed to refresh subject + verifier + bar in {landing, no-bar}; IF-175 data cell amended | D1; D2; D3; D6; SR-156; TC-205 | IF-175 | P1 |
| P3 | One producer in `integrate.py` (`_attest_commit`): stage, run the given bar, shed residue, `write-tree`, commit with the trailer, re-verify, otherwise undo. `refresh` moves onto it for `landing` / `no-bar`; `_merge_ready` refuses a `review`-only tip and names both bars; the existing refresh fixtures move to the new grammar. Its tests drive only `refresh` and `_merge_ready`, which exist at this step (F1) | D1; D3; D5; F1; SR-156; TC-132; TC-144; TC-205 | IF-175; IF-173 | P2 |
| P4 | The review bar's one declaration: `[bars] review` in `project-trajectory/stack.ini.template` (`python scripts/check.py --jobs 0 --tier smoke`) and in `docs/stack.ini` (this repo's `[run] smoke` line); its one reader `_review_bar_command` through `kitlib.config.read_stack_ini`, refusing with no default; IF-022 data cell gains `bars` | D1; D4; SR-156; TC-132 | IF-022 | P1 |
| P5 | `integrate.py attest --branch <b> --bar review --tests <files...> [--message-file <f>]`: commit hooks first, worktree holding the branch, key read, dirty-worktree refusal, then the review bar and the named tests under `[product] test` with a per-lane `--basetemp`, then the shared producer. IF-154, IF-080 and IF-173 data cells gain `attest`; the hooks-on census gains the route. Owns the cross-route test that `refresh` and `attest` commit through one producer, moved here from P3 (F1) | D1; D4; D5; F1; SR-156; TC-132; TC-205; TC-370 | IF-154; IF-080; IF-173; IF-022 | P3; P4 |
| P6 | Records: `docs/runtime-flows.md` Flow 4 names the landing bar; the `worker.template.md` `Bar-Green` sentence names the bar field; integrate/verdict docstrings; one `RESYNC_PACK.md` entry (the grammar change and the new key); the module-size ratchet re-stamp for `integrate.py` | D7; SR-156 | IF-173; IF-022 | P5 |
| P7 | Landing: re-anchor the RESYNC entry at the landing's parent; commit bar green; `check_trajectory.py --strict` and `trace.py --strict` clean; LLR-207's amendment judged at the lane's sitting; trunk-only regenerations left to the landing | D7; SR-156; TC-205; TC-132; TC-144; TC-370 | no interface: landing bookkeeping, no code seam crossed | P6 |

Excludes: TC-131; TC-139; TC-145; TC-257; TC-259; TC-317; TC-325; TC-326; TC-327; TC-328; TC-369 — each verifies an SR-156 arm this item does not touch (the pause home, spec_move's relink, the claim lock, review-scope evidence, the coordinator guard, Done-when blessing, the declared trunk name). None of them reads the `Bar-Green:` trailer, `refresh_attestation`, `work_tip`, `governing_rev`, `_merge_ready` or `docs/stack.ini` `[bars]`. They run unchanged in the full suite at landing and need no amendment.

## Step detail

### P1: spine checkpoint (TC-first)

- **LLR-207** (`docs/requirements/low-level-requirements.toml`, Approved, so
  it becomes Modified and gets re-attested at the sitting):
  - `module` gains `;project-trajectory/scripts/integrate.py`.
  - `code_symbol` gains `format_bar_green/bar_attestation/tests_digest` on the
    verdict module and `attest/_attest_commit/_review_bar_command/_run_review_bar/_unstaged_dirt`
    on the integrate module.
  - `detail` replaces the sentence "refresh_attestation validates a station
    refresh from its subject, first parent, commit tree and Bar-Green trailer"
    with the grammar. It is one label line,
    `Bar-Green: tree=<40 hex> work=<40 hex> bar=<review|landing|no-bar> tests=<64 hex|none> <summary>`,
    at column 0, exactly one per message. The verifier returns the fields only
    when tree and work equal the commit's own tree and first parent and `bar`
    is in the set. `refresh_attestation` is the refresh subject plus that
    verifier plus `bar` in {landing, no-bar}, so `work_tip` and the read-only
    walk never peel a `review` attestation. One producer writes every
    attestation and undoes on any failed write. The old trailer without `bar=`
    is not read.
- **TC-205** (`docs/test/test-cases.toml`): `method` gains the grammar arms
  (D2), the digest arms (D6) and the review-not-peeled arms (D3). `evidence`
  gains every `tests/test_bar_attestation.py::...` case listed under P2, the
  three D5 refresh cases P3 adds to `tests/test_integrate_station.py`, and
  the cross-route producer case P5 adds there (F1). The three existing
  `test_integrate_station.py` refusal citations stay, with their fixtures
  moved (P3).
- **TC-132**: `method` gains the attest arms (D4) and the review-only
  merge-ready refusal (D3). `evidence` gains `tests/test_integrate_attest.py`.
- **TC-370**: `evidence` gains
  `tests/test_hooks_on_routes.py::test_attest_refuses_a_hookless_checkout`.
  `method`'s "every route" already covers the new census row.
- SR-156 is unchanged. Its acceptance ("the declared bar green on the composed
  tree") already carries the landing bar. The spec's conditional applies here:
  if the sitting rules that LLR-207's amendment does not carry the `review`
  record, a derived SR plus its TC is drafted TC-first in this lane, and P2–P5
  keep their shape.
- Tests added: none. This row writes the rows the next rows' tests answer to.

### P2: grammar, verifier and digest (`kitlib/verdict.py`, 539 SLOC now, stays under the 1000 threshold)

- **`tests_digest(paths)`**: `"none"` for an empty set. Otherwise
  `sha256("\n".join(sorted(set(normalized))) + "\n")`, where a path is
  normalized by changing `\` to `/` and dropping a leading `./`. It has one
  home, so the producer here and WI-957's dispatch check compare the same
  value.
- **`format_bar_green(tree, work, bar, tests, summary)`**: the one writer of
  the line. It raises on a bar outside `BAR_NAMES`, so the writer cannot emit
  what the verifier refuses.
- **`bar_attestation(root, rev)`** returns a `BarAttestation(tree, work, bar,
  tests, summary)` NamedTuple, or `None`. It reads the message with
  `git log -1 --format=%B`. It finds the lines that start with the label
  `station.BAR_GREEN` at column 0, without stripping. It requires exactly one
  such line, and that line must fully match
  `^Bar-Green:\s+tree=([0-9a-f]{40})\s+work=([0-9a-f]{40})\s+bar=(\S+)\s+tests=([0-9a-f]{64}|none)(?:\s+(\S.*))?$`.
  The bar must be in `BAR_NAMES`, `rev^{tree}` must equal `tree`, and `rev^1`
  must equal `work`. An unreadable commit gives `None`.
- **`refresh_attestation(root, branch, rev=None)`** keeps its signature and
  its `(work, summary)` return, so `work_tip`, `_peel_target`,
  `governing_rev`, `_merge_ready` and the `integrate` re-export are unchanged
  callers. It is the refresh-subject check, then `bar_attestation`, then
  `bar in LANDING_BARS`.
- IF-175 `data` gains "the bar attestation's grammar, verifier and tests
  digest".
- Tests added in the new module **`tests/test_bar_attestation.py`**, registered
  in `tests/conftest.py` `SLOW_MODULES` because it uses real git fixtures. The
  smoke tier holds 2966 of its 2970 `max-tests` ceiling, measured in the lane
  with `pytest -m smoke --collect-only`, so no new case enters smoke. Each case
  fails on the code before the change, in one of two ways. Most call
  `kv.bar_attestation`, `kv.tests_digest` or `kv.format_bar_green`, which do
  not exist yet, so they fail with AttributeError. The cases marked
  *behavioural* also fail on the old reader's behaviour, because the old
  `_ATTEST_RE` accepts `tree= work= <anything>`:
  - D2 `test_a_trailer_naming_its_own_tree_and_parent_verifies_for_each_bar`
    (review, landing, no-bar).
  - D2 `test_a_wrong_tree_is_not_an_attestation`.
  - D2 `test_a_wrong_parent_is_not_an_attestation`.
  - D2 `test_a_trailer_without_bar_is_not_an_attestation` (*behavioural*: the
    old grammar on a refresh subject; `refresh_attestation` must return None,
    and the old code returns the tuple).
  - D2 `test_an_unknown_bar_is_not_an_attestation` (*behavioural*:
    `bar=nightly` on a refresh subject).
  - D2 `test_a_trailer_without_tests_is_not_an_attestation`.
  - D2 `test_a_trailer_quoted_mid_line_is_not_an_attestation` (the label after
    other text on the line, with a true tree and parent).
  - D2 `test_two_label_lines_are_not_an_attestation`.
  - D6 `test_the_tests_digest_is_the_same_for_the_same_set_in_any_order`
    (permutations, a duplicate, `./` and `\` spellings).
  - D6 `test_the_tests_digest_differs_for_a_different_set` (one path added,
    one swapped; the empty set is `none`).
  - D3 `test_work_tip_never_peels_a_review_attestation` (*behavioural*: a
    commit with the refresh subject and a verified `bar=review` trailer. The
    old code peels it and the new code must not.)
  - D3 `test_governing_rev_never_peels_a_review_attestation` (*behavioural*:
    the same commit carrying a work change. `governing_rev` must return it,
    not its parent.)
  - D3 `test_a_verified_refresh_still_peels_under_the_new_grammar` (`landing`
    and `no-bar`, at both `work_tip` and `governing_rev`).

### P3: one producer; the refresh on it; `_merge_ready` (`integrate.py`)

- **`_attest_commit(wt, root, branch, bar, tests, run_bar, message)`**: the
  stage the refresh and `attest` share (PROCESS.md §3, 0→A→B).
  1. Read the ignored-file baseline.
  2. `run_bar()` returns `(ok, out, summary)`. It runs on the index as staged,
     and both callers guarantee that the worktree equals the index.
  3. `_shed_residue`.
  4. On red, return a refusal. Nothing is committed and the index is
     untouched.
  5. Run `write-tree`, then
     `commit --allow-empty -m with_loop_trailer(message + "\n\n" + format_bar_green(...))`.
     A hook refusal returns a refusal with HEAD unmoved.
  6. Re-verify with `bar_attestation(root, branch)`. It must equal the bar,
     the tree and the digest that were written. Otherwise run
     `reset --soft <pre-commit tip>` and refuse. A soft reset keeps the index
     as it was staged.
  7. Return `(sha, None)`.
- **`refresh`** keeps its preflight, merge and trunk step, and its `add -A`.
  It then calls `_attest_commit(bar="no-bar" if skip_bar else "landing",
  tests=(), run_bar=lambda: _refresh_bar(...), message=<the current subject
  and body>)`. Its outer `undo` (`reset --hard work_tip`) runs on every
  refusal, as today. After the producer returns, the existing
  `refresh_attestation(root, branch) is None` self-check stays, because it is
  the refresh-subject half. `_refresh_bar`'s summaries are unchanged
  (`bar PASS (...)`, `no-bar (adjudication, §A5.2)`), so the existing
  summary assertions hold.
- **`_merge_ready`**: when `refresh_attestation` returns None and
  `bar_attestation(root, branch)` is a verified `review`, it refuses with
  "its tip carries a verified `review` Bar-Green attestation; the merge slot
  requires `landing` or `no-bar`", naming both bars (the Trust ruling).
  Otherwise the refusal is the current one.
- IF-173 `data` is touched in P5 (attest). IF-175 is crossed by the new
  `bar_attestation` and `format_bar_green` imports.
- Fixtures moved to the new grammar, so that every existing refresh test
  passes (D5):
  - `tests/test_integrate_station.py`: `FORGED_TRAILER` becomes the
    `bar=landing tests=none` form, so the forgery is still refused by tree and
    parent and not by grammar. The STATED-limit test's hand-forged trailer
    becomes `format_bar_green(tree, parent, "landing", "none", ...)` and is
    still accepted by design. `test_a_work_commit_that_quotes_the_trailer...`
    is unchanged and is still not peeled.
  - `tests/test_verdict_record.py::_refresh_commit` writes the new grammar
    through `kv.format_bar_green`.
  - `tests/test_dispatch.py` (TC-144) and `tests/test_loop_provenance.py` go
    through `integ.refresh`. Their fixtures are not changed, and they are run
    to prove it.
- Tests added. All fail before the change.
  - In `tests/test_integrate_station.py`:
    - D5 `test_the_refresh_trailer_names_the_landing_bar`.
      `bar_attestation(...).bar == "landing"` and `tests == "none"`. Fails
      before: there is no `bar=` field and no `bar_attestation`.
    - D5 `test_the_adjudication_refresh_names_no_bar`. `bar == "no-bar"`.
      Fails before for the same reason.
    - D5 `test_the_refresh_commits_through_the_shared_producer`.
      `monkeypatch` wraps `integ._attest_commit`, drives a refresh (bar run)
      and an adjudication refresh, and asserts the wrapper recorded `landing`
      and `no-bar`. Fails before: `_attest_commit` does not exist. It drives
      only `refresh`, so it runs at this step (F1); the cross-route case that
      also drives `attest` is P5's.
  - In the new module `tests/test_integrate_attest.py` (SLOW, the
    `integrate_fixtures` station repo):
    - D3 `test_merge_ready_refuses_a_tip_carrying_only_a_review_attestation`.
      The refusal names `review` and `landing`. Fails before: the old regex
      reads the review trailer on a refresh subject as merge-ready. Without
      the refresh subject, the named-bars wording is still new.

### P4: the review bar's declaration and its one reader

- In `project-trajectory/stack.ini.template`, add a commented `[bars]`
  section stating its contract: the command a `review` attestation runs, a
  full shell line, with `python` the harness interpreter, and no default. The
  shipped value is `review = python scripts/check.py --jobs 0 --tier smoke`.
- In `docs/stack.ini`, add `[bars]` with `review = <this repo's [run] smoke
  line verbatim>`. Extend the header's Contract IF-022 paragraph to name the
  section. `tests/test_dogfood_sync.py` requires the template's sections in
  the live file, and this keeps both in step. `tests/test_stack_profile.py`
  compares the scaffold to the template byte for byte, so it stays green
  without a golden.
- **`_review_bar_command(root)`** returns `(command, None)` or
  `(None, refusal)` and reads only through `_kitconfig.read_stack_ini`. It
  refuses, naming `docs/stack.ini`, the key `[bars] review` and the cause, on
  any of: an absent file, an absent section or key, an empty or
  whitespace-only value, or a `StackIniError`. There is no fallback to
  `[run] smoke` or `check.py` (D-002). It is the key's only reader. The
  verifier never reads it.
- IF-022 `data` gains `bars`. Its notes already name `scripts/integrate` among
  the stack.ini readers.
- Tests are under P5. The reader is driven through the `attest` CLI.

### P5: the `attest` verb

- **`attest(root, branch, bar, tests, message_file=None)`**, in this order:
  1. `hooks_refusal(root)`.
  2. `_worktree_holding(root, branch)`, refusing when no worktree holds the
     branch.
  3. `_review_bar_command(root)`.
  4. `_unstaged_dirt(wt)`: `git status --porcelain -z`. Any entry whose
     worktree column is not a blank is dirt. That covers a tracked change not
     staged and an untracked, non-ignored file (`??`). Ignored files are not
     listed, so they do not count. It refuses, naming the paths.
  5. A message file whose text contains a column-0 `Bar-Green:` line is
     refused. Without a message file, the subject is composed as
     `attest: <branch> bar=review`.

  Only after all of these does `_attest_commit` run, with
  `run_bar = _run_review_bar(wt, root, command, tests, branch)`.
- **`_run_review_bar`**:
  - Runs the declared shell line with `shell=True` and the harness
    interpreter's directory first on `PATH`, the same rule `run_menu` states
    for `[run]` lines.
  - If it is green and `tests` is non-empty, it then runs `[product] test`
    through `ac._declared_test_command(ini, py=harness_python)` with the named
    test paths appended and
    `--basetemp=<tempdir>/<repo-name>-attest-<branch>`, a directory outside
    the worktree and one per lane.
  - Green is exit 0 for each step. The summary is `review bar PASS (<n> named
    tests)`.
- CLI: a subparser `attest` with
  - `--branch` (required),
  - `--bar` (`choices=["review"]`: `landing` and `no-bar` are only the
    refresh's),
  - `--tests` (`nargs="*"`),
  - `--message-file`.

  The exit is nonzero on any refusal, with the reason named, through `fail`.
- Records: IF-154 `data` gains
  `attest --branch --bar --tests --message-file`. IF-080 `data` gains
  `attest`. IF-173 `data` gains `attest`.
- `tests/test_hooks_on_census.py` `ROUTES` gains
  `(SCRIPTS / "integrate.py", "attest", "root", ())`.
- Tests added in `tests/test_integrate_attest.py`. Every case fails before the
  change because `integ.attest` and the CLI verb do not exist. The bar and
  `[product] test` are stubs that record their order, as in the station
  fixtures:
  - D4 `test_attest_commits_staged_work_carrying_a_trailer_that_verifies`.
    The staged file is in the commit. `bar_attestation` gives
    `bar == "review"` and `tests == tests_digest(named)`.
  - D4 `test_attest_with_nothing_staged_writes_an_empty_commit_that_verifies`.
    The tree equals the parent's, and the attestation verifies.
  - D4 `test_a_red_review_bar_commits_nothing_and_leaves_branch_and_index`.
    The branch rev and `git write-tree` are equal before and after, and a red
    named test arm is included.
  - D4 `test_attest_refuses_a_dirty_worktree_before_running_the_bar`. It
    covers an unstaged tracked edit and an untracked file. Each refuses and
    the bar stub records no run. An ignored file does not refuse.
  - D4 `test_attest_refuses_a_missing_review_bar_key_naming_it`. It covers an
    absent section, an absent key, a whitespace value and an unparseable file
    (a duplicate section). The refusal names `[bars] review` and
    `docs/stack.ini`, no bar runs and no commit is made.
  - D4 `test_the_named_tests_run_after_the_review_bar_under_the_lanes_basetemp`.
  - D4 `test_a_hook_refused_attest_commit_leaves_branch_and_index`. A
    `commit-msg` hook in the fixture exits 1.
  - D4 `test_a_rewritten_attest_commit_is_undone_by_the_self_check`. A
    rewriting hook moves the tree. After the soft reset, the branch and index
    are as staged.
  - D4 `test_a_message_file_carrying_the_label_is_refused_before_the_bar`.
  - D4 `test_the_attest_cli_is_the_route_a_builder_calls`. A `run_py`
    subprocess, exit 0 and exit 1.
  - D5 / F1 `tests/test_integrate_station.py::test_the_refresh_and_attest_commit_through_one_producer`
    (moved here from P3). `monkeypatch` wraps `integ._attest_commit`, then
    drives a refresh and an attest and asserts the wrapper recorded both
    `landing` and `review`. Fails before: neither `_attest_commit` nor
    `attest` exists. It runs at this step because both callers now exist.
  - D4 `tests/test_hooks_on_routes.py::test_attest_refuses_a_hookless_checkout`.
    The census row is checked by the existing
    `test_each_route_calls_the_check_first`.

### P6: records

- `docs/runtime-flows.md` Flow 4: "commit a Bar-Green trailer naming the
  `landing` bar (or `no-bar`), the tree it barred and its work parent". The
  slot line becomes "...does the tip attest its OWN tree for the landing
  bar?". The `review` attestation enters a flow with its consumer (WI-957 /
  WI-958), not here: no flow reads it yet.
- `project-trajectory/prompts/worker.template.md`: the "attests it with a
  `Bar-Green:` trailer naming the tree it barred" sentence names the bar
  field (`bar=landing`). The prompt catalog digest is a trunk-only
  regeneration and is left to the landing.
- Docstrings: the `integrate.py` module docstring (the `Bar-Green: tree=<sha>
  work=<sha>` paragraph and the op list), the `refresh` docstring, and the
  `verdict.py` module and `refresh_attestation` docstrings state the new
  grammar. The honest bound is unchanged: accident, not intent.
- `project-trajectory/RESYNC_PACK.md`: one §3 entry, anchored
  `[since <lane base>]` for now (`scripts/check_resync.py` is in the commit
  bar). It says:
  1. The trailer grammar gains `bar=` and `tests=`, and no reader reads the
     old form.
  2. A lane whose tip is an old-grammar refresh commit is no longer peeled.
     Reset it to that commit's `work=` sha, then refresh again. The drain also
     re-refreshes a lane that is not merge-ready.
  3. Add `[bars] review` to `docs/stack.ini` with the shipped value, or the
     project's own commit bar. Without it, `attest` refuses, and so does
     review dispatch once WI-957 and WI-958 land. This is the forced
     migration under D-002.
- `tests/test_module_size_ratchet.py`: `integrate.py` (baseline 1559 SLOC)
  grows by `attest`, its reader, its dirt predicate, the review-bar runner and
  the subparser. The refresh's commit-and-verify block moves into the
  producer, so the net growth is less than the gross. The figure is measured
  with `check_complexity.module_sloc` at build and stamped as a reviewed
  upward re-stamp naming WI-956. The reason is that the producer must sit
  beside the refresh it is extracted from: a new module would need an LLR, a
  component tag and IF rows that the spec rules out (S5).
- `docs/complexity-baseline` has no `refresh` row, so the extracted producer
  and `attest` must each stay under the per-function ceiling. That is checked
  at the commit bar.

### P7: landing

- Rebase onto trunk and re-anchor the RESYNC entry `[since <landing's
  parent>]`.
- Run the commit bar (`run.cmd smoke`, `run_menu.py smoke` from a shell),
  which includes `trace.py --strict`, `check_trajectory.py --strict`,
  `check_docs`, `check_resync` and the smoke tier against its 60 s budget.
  Paste the real output.
- The full suite with `-n auto` runs at the landing refresh, the bar declared
  for the stage. The new SLOW modules run there, together with TC-144's
  `test_dispatch.py` and TC-205's `test_verdict_record.py`.
- LLR-207's amendment, and the TC-205, TC-132 and TC-370 amendments, are
  judged at the lane's sitting.
- Trunk-only artifacts are regenerated at the landing, not committed in the
  lane: `docs/cli-reference.md` (the new verb), `docs/ratify/CURRENT.md` (the
  Modified rows), `components.derived.toml`, the prompt catalog and the
  dashboard.
- **Landing hazard.** WI-956 lands through the trunk-vintage integrator. Its
  own refresh commit is old-grammar, and the trunk-vintage slot verifies it,
  so it merges. After the merge, any other lane whose tip is an old-grammar
  refresh commit (for example WI-955's, if it refreshed first) is reset to
  that commit's `work=` sha before its next refresh. That is the RESYNC
  entry's step, applied in this repo by the coordinator.

## Risks and checks named for the critic

- **The wrong peel destroys committed work.** The `work_tip` path stays
  `refresh_attestation`, which is strictly narrower than before: it adds two
  required fields and a bar restriction. So the change can only peel less,
  never more. The *behavioural* D3 cases pin this in both directions.
- **The index promise in D4** depends on two things. The producer never runs
  `add` for `attest`, and its only post-commit undo is `reset --soft`. The
  hard reset stays the refresh's, in its outer `undo`.
- **The smoke ceiling** is at 2966 of 2970. Every new case goes into a SLOW
  module, so the smoke tier and its budget are unchanged.
