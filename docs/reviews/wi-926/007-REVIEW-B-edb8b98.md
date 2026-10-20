Reviewed: edb8b98b31660a63cfd78630bde4cd0ba938f3ff

Verified. This is a full-lane review in the convergence stance (range 5245ac82c..edb8b98b3, checkout confirmed at edb8b98b3). I hunted the worst classes first. Fail-open first: can the check read "on" when no kit hook will run, can a route commit or launch before the check, or can a hook still exit 0 with no scripts? Then false refusals in supported workflows: the primary checkout, linked lane worktrees, relative and absolute `core.hooksPath`, and a route started from a subdirectory.

- `kitlib/commit_hooks.hooks_refusal` (project-trajectory/scripts/kitlib/commit_hooks.py:125) asks git once (`rev-parse --path-format=absolute --git-path hooks --git-common-dir --show-toplevel`). It admits only `<top>/.githooks` or `<common>/../.githooks` with `pre-commit` and `commit-msg` present as files (executable on POSIX). Anything else is denied by default. It reads no environment variable and takes only `root`.
- I drove the real function on real checkouts:
  - this lane worktree (absolute `core.hooksPath` naming the primary's `.githooks`) and the primary checkout both read "on";
  - a scratch repo with a relative `.githooks` reads "on" from its top and from a subdirectory (git resolves the relative path against the top).
- Each of the six route entries calls the check first, and so does `overnight_legs.main`. I confirmed this by reading the diff and through the census:
  - `agent_loop.main`, after `_resolve_root` and before the lock and the loop marker;
  - `session_service.act`, before the blackout and with the keep released;
  - `bookkeeping.commit`;
  - `integrate.claim`, `integrate.refresh` and `integrate.integrate`;
  - `coordinator_guard.take`, before the session-id check.
- `coordinator_adjudicate` catches `HooksOffRefused` beside `BlackoutRefused`. `through_blackout` lets it propagate without waiting.
- `hooks/pre-commit`, `hooks/commit-msg` and `hooks/pre-push` each refuse with exit 1, naming the cause and the three fixes, when no kit scripts dir is findable. The privacy and loop-marker special cases are deleted. `pre-push`'s privacy read moved into a function that reads the same thing it read before.
- Red-before. I copied the reviewed tree to scratch (`git archive`) and put back the base versions of the six route files, `overnight_legs.py`, `coordinator_adjudicate.py` and the three hooks. Under the posix-shell gate, every refusal case failed there (39 failed / 45 passed), including:
  - all 10 `test_hooks_on_routes` refusal cases;
  - the inverted half of `test_hook_honors_kit_scripts_dir_override`;
  - `test_each_hook_refuses_when_the_kit_scripts_cannot_be_found` and `test_privacy_and_loop_commits_get_the_same_scripts_refusal`;
  - `test_pre_push_honors_kit_scripts_dir`.
- The posix-shell-gated hook tests are skipped by the brief's command on this box. I re-ran them with Git\bin on PATH: 140 passed, 1 skipped.
- K2: SR-240 names no carrier, and its acceptance is capability-voiced.
- K3: the new `Implements: SR-240, LLR-340` tags point at symbols in LLR-340's `code_symbol`. No Status flips.
- The byte-budget table matches `wc -c` (CLAUDE.md 8159, AGENTS.template.md 9998, skill 4527).
- `RESYNC_PACK.md` carries the entry and names the forced change.

Done-when coverage:
- (1) The check. Unset, `.git/hooks`, another dir, empty, missing hook, non-exec (POSIX), not a work tree, failing git, relative, absolute and both linked-worktree forms: tests/test_commit_hooks.py. On Windows the non-exec case is skipped; I confirmed it by reading the code. The repair named for a missing or non-executable hook is not the setup command: see MINOR 2.
- (2) Six routes refuse before work and run as today with hooks on: tests/test_hooks_on_routes.py plus the existing route suites through `hooks_on`. Red-before confirmed.
- (3) Take records no holder: `test_take_refuses_a_hookless_checkout_and_records_no_holder`. Red-before confirmed.
- (4) Hooks refuse with no scripts, privacy and loop cases included: tests/test_pre_commit_hook.py and tests/test_pre_push_hook.py. Red-before confirmed.
- (5) Census plus mutation test: tests/test_hooks_on_census.py.
- (6) No override: `test_the_check_reads_no_override`.
- (7) Guide line and byte delta: CLAUDE.md, AGENTS.template.md and the byte-budget table.
- (8) Spine rows present. The out-of-grant SR-020 amendment is MINOR 3; the stale counterparts are MINOR 1.
- (9) RESYNC entry present.
- (10) Bar on the landing tip: not run here, by the round facts (no full suite and no smoke tier).

Coverage-extension notes (fail closed, no severity):
- The lease's successor install through the SessionStart hook does not pass `take`. A hookless successor's claim still refuses at `integrate.claim`.
- A submodule's or `--separate-git-dir` checkout reads "not on".

Commands:
- `git rev-parse HEAD` -> edb8b98b31660a63cfd78630bde4cd0ba938f3ff
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../g-opus/wi-926 <the 36 listed modules>` -> `1492 passed, 102 skipped in 1418.66s` (88 skips from the posix-shell gate)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (948 work item(s), 836 done (88%), 30 cancelled, graph acyclic).` (exit 0; the WARNs are about other WIs, plus the expected WI-926 trailer advisory)
- With Git\bin on PATH: `python -m pytest ... tests/test_commit_hooks.py tests/test_pre_commit_hook.py tests/test_pre_push_hook.py tests/test_process_config.py tests/test_hooks_on_routes.py tests/test_hooks_on_census.py` -> `140 passed, 1 skipped in 102.23s`
- Red-before, on the scratch tree with the base routes and hooks put back: `python -m pytest ... tests/test_hooks_on_routes.py tests/test_hooks_on_census.py tests/test_pre_commit_hook.py tests/test_pre_push_hook.py` -> `39 failed, 45 passed in 83.54s`
- Probe: `hooks_refusal` on the scratch repo top and subdir, this lane worktree and the primary checkout -> `None` for all four

- [MINOR] docs/requirements/interfaces.toml:1914 -> IF-194's notes ("the commit-msg hook reads it by name only to fail closed when the floor cannot run") and IF-197's rationale at docs/requirements/interfaces.toml:1939 ("the hook carries only the knowledge of whether the loop marker is set, which it needs to fail closed when the harness cannot run") no longer match the code. This diff deleted `loop_marked`, and project-trajectory/hooks/commit-msg no longer reads `KIT_LOOP_SESSION` at all (it refuses every commit when no kit scripts dir is found). These are the counterparts of the changed commit-msg contract, and they were neither carried nor named as kept (K1). -> amend both Drafted cells: the hook reads no marker, and the floor's absence refuses every commit -> @owner
- [MINOR] project-trajectory/scripts/kitlib/commit_hooks.py:116 -> The spec's Done-when (docs/work/active/wi-926/WI-926-hooks-on-at-launch.md:196-199) says that a missing `pre-commit`/`commit-msg` and a non-executable hook each read "not on" with a refusal naming "the cause and the setup command". The code names `_RESTORE` (`git checkout -- .githooks` / re-run bootstrap) or `_MAKE_EXECUTABLE` instead, and tests/test_commit_hooks.py asserts those. The code's reading is the correct one, since setup only sets `core.hooksPath` and repairs neither cause, and SR-240, LLR-340 and IF-297 already say "applicable repair". So the spec of record and the built behaviour diverge in wording only (for clarity). -> amend the Done-when item to "names the cause and the repair for that cause" through the spec's authority, so the spec matches the spine rows and the tests -> @owner
- [MINOR] docs/requirements/system-requirements.toml:131 -> SR-020's (Approved) acceptance gained the pre-push scripts-lookup refusal sentence, but the spec's spine list grants only SR-019's acceptance, LLR-019/LLR-020 detail, LLR-140, LLR-300, IF-186 and IF-246, and does not name SR-020 (K3: an approved row changes only where the spec grants it). Semantically the carry is right: LLR-020's amended detail would otherwise exceed its parent. -> record the grant for SR-020 in the spec's spine list, or in the checkpoint sitting that judges the lane's rows, so the amendment has its authority on record -> @owner
- [MINOR] docs/test/test-cases.toml:259 -> TC-370's evidence omits four tests that carry Done-when cases: tests/test_commit_hooks.py::test_git_hooks_dir_is_not_on (`.git/hooks`), ::test_an_empty_hooks_path_is_not_on, ::test_a_directory_that_is_not_a_work_tree_is_not_on, and ::test_a_linked_worktree_is_on_with_the_main_worktrees_absolute_githooks (the configuration this repository itself runs) (for clarity). -> add the four node ids to TC-370's evidence -> @owner

VERDICT: APPROVE findings=4
