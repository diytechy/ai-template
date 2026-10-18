Reviewed: b6878a31c81f80999140d037515c97597c1762e9

## WI-917 full-lane review (independent, Claude Opus), range 6533a2331..b6878a31c

**Verified.** The checkout is the reviewed commit (`git rev-parse HEAD` printed b6878a31c81f80999140d037515c97597c1762e9). Worst failure classes I looked for first: fail-open in the after-leg audit or `check-lane`, meaning an unmarked or foreign commit that reaches trunk, `archive/lanes` or a marked lane without stopping the run; a failed or unparseable git read taken as an empty range; and a leg running unmarked. What I found right:

- **The marker.** `prepare_run` (scripts/coordinator/overnight_legs.py:141) reads the block, calls `provenance.mark_loop_process()` once in the launcher's own process and logs the session, before any leg. Legs inherit it through `subprocess.run` with no `env=`. A well-formed inherited marker is kept and a malformed one is replaced, which is the function's own contract.
- **The prompt.** It is the session prompt, then the stripped block, then `loop_provenance_note()`. It goes in on stdin, and the CLI is resolved with `shutil.which`. An absent, directory, non-UTF-8, empty or whitespace-only block, or an empty note, returns 2 before `newest_handoff` is reached.
- **Every git read fails closed.** Every read goes through `read()`, which raises AuditStop on an unexpected exit. `log_records` refuses a record without a NUL or a SHA, `snapshot` refuses a malformed line, a detached HEAD is refused, and a trunk missing from either snapshot is refused. An empty `for-each-ref` cannot pass.
- **The trunk and archive rules.** Trunk's descent is checked with `merge-base --is-ancestor`, answering exit 0 or 1 only. Trunk's and archive's first-parent additions are judged against the run's session. An archive created in the leg is judged over `after --not <every pre tip>`.
- **The lane rule.** Other created or moved branches go through `provenance.loop_lane_window`, then `loop_trailer_refusal` with no session, which is the slot's reading (compared with integrate.py:1232-1282).
- **The audit runs first.** It runs before the leg's exit code, the lease and handoff checks, so a refused commit is named whatever else the leg did.
- **Real scenarios.** I drove `pre_leg`/`audit` on real repositories with a probe of my own: a marked claim, then an unmarked plumbing commit on the kept lane, then a marked squash stops the run, naming the commit.
- **Pre-fix code fails.** I ran the lane's two test files against the pre-change launcher (`git show 6533a2331:scripts/coordinator/overnight_legs.py` overlaid on a `git archive` of the tip in my scratch folder): 49 failed, 1 passed. The one pass is the block/skill-link text test, which reads files the overlay kept.
- **Skill copies.** The three skill copies are byte-identical (`diff -r` of project-trajectory/skills/coordinator-cycle against .claude/ and .agents/).
- **Scope.** The skill is `scope: this-repo` (bootstrap.py:1903 lists it as never materialized), and scripts/coordinator/ and tests/ sit outside the kit. No shipped file changes, so no RESYNC entry is owed (K4 clean). No SN/SR/LLR/TC row and no `Implements:` tag changes (K1, K2 and K3 not engaged).
- **The block.** scripts/coordinator/headless-leg.md carries all four of deliverable 2's statements, opens with the marker check and cites rulings 35 and 36 and D-016. SKILL §7 carries deliverable 3: the trailer on every commit, foreground only, the owner-held list and its default, the lane-mode rule, the re-claim with the missed-re-claim replay, and `check-lane` before a squash. Recipes §1 steps 4 and 7, §3 (squash, archive, message files) and §7 point to it.
- **Test isolation.** conftest's autouse `_no_loop_marker_leaks` keeps the launcher's direct `os.environ` write from leaking between tests.

**Done-when coverage:**

| Done-when item | Covering test |
| --- | --- |
| Two legs, one marker | `test_two_legs_see_one_well_formed_marker_the_same_in_both` |
| Inherited marker kept or replaced | `test_an_inherited_well_formed_marker_is_kept_and_a_malformed_one_is_replaced`, plus the in-process `test_the_run_marks_itself_once_*` |
| Prompt composition | `test_each_leg_gets_the_session_prompt_then_the_block_then_the_provenance_line` |
| Absent, unreadable or empty block exits 2 | `test_a_missing_unreadable_or_empty_block_refuses_the_run_before_any_leg`, `test_an_empty_provenance_note_*` |
| Trunk or archive commit unmarked, foreign, or trunk rewound | `test_a_leg_that_adds_an_unmarked_foreign_or_rewinding_trunk_or_archive_commit_stops_the_run`, `test_the_trunk_rule_*` |
| Unmarked commit in a marked lane, then a marked commit or squash; `check-lane` before the squash | `test_a_leg_that_adds_an_unmarked_commit_to_a_lane_it_marked_stops_the_run_naming_it` (4 cases), `test_check_lane_refuses_a_marked_lane_holding_an_unmarked_commit_before_the_squash` |
| Another run's replayed session passes | `test_a_lane_whose_replayed_commits_carry_another_runs_session_passes` |
| A failed read is never an empty range | `test_a_git_read_that_fails_after_a_leg_stops_the_run_and_check_lane_refuses`, `test_every_failed_audit_read_*`, `test_a_failed_range_read_is_never_an_empty_range`, `test_check_lane_refuses_when_a_read_fails` |
| All-marked leg runs the next | `test_a_leg_whose_commits_all_carry_the_runs_trailer_runs_the_next_leg` |
| Skill copy sync | `diff -r`, identical |
| Plan gate | plan_gate.py ok |
| Smoke tier | Not run: the brief forbids it. It is the landing bar's. |

**Outside the finding lines.** These do not move the count.

- **Pre-existing slot fail-open.** `integrate._loop_claimed` (project-trajectory/scripts/integrate.py:1239-1240) reads a failed claim `git log` as "not claimed" (`out if code == 0 else ""`). At the slot, a loop-claimed lane with no later writer commit would then read as a person's lane. This range does not change it. The launcher's own copy correctly fails closed.
- **check_docs orphan.** The `check_docs --strict-orphans` FAIL is the git-ignored, locally regenerated docs/test/report.md (written by trace.py, `.gitignore:17`). It is not a tracked file and not this range's doing.

**Commands:**

- `git rev-parse HEAD` -> b6878a31c81f80999140d037515c97597c1762e9
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-18a/wi917-r1-opus/wi-917 tests/test_overnight_legs.py tests/test_overnight_legs_git.py` -> `50 passed in 40.56s`. The first attempt hit INTERNALERROR because the scratch folder did not exist yet; I created it and re-ran.
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (941 work item(s), 821 done (87%), 30 cancelled, graph acyclic).` Its WARNs are overlap advisories only, including WI-917/WI-918 sharing SR-209, which the split ruling intends.
- The same pytest, run against the pre-change overnight_legs.py overlaid on a `git archive` of the tip in the scratch folder -> `49 failed, 1 passed in 22.11s`
- `python -m pytest ... tests/test_module_size_ratchet.py tests/test_prompts.py` (the other tests naming coordinator-cycle) -> `66 passed in 4.86s`
- `python project-trajectory/scripts/plan_gate.py --root .` -> `ok    plan-gate  no 'single' row of this lane builds before its plan passes`
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=131 LLR=304 TC=318 orphans=0 integrity=0 ...`
- `python project-trajectory/scripts/check_docs.py --root . --strict-orphans` -> `check_docs: FAIL - 0 broken link(s), 1 orphan(s), 0 README finding(s) across 2788 doc(s).` The one orphan is the ignored docs/test/report.md above.
- `diff -r project-trajectory/skills/coordinator-cycle .claude/skills/coordinator-cycle` and the same against .agents/ -> identical
- The probe script `C:/Projects/ai-template.wt/review-tmp/2026-10-18a/wi917-r1-opus/probe/probe.py`, real git repositories through `ol.pre_leg`/`ol.audit`:
  - p1 (a lane created, given an unmarked commit, squashed marked and deleted within one leg) -> `p1 audit passes: trunk 2 commit(s); archive/lanes absent`
  - p1b (the same, lane kept) -> `p1b stop: lane wi-1 holds 6f913d7bb3 - commit 'unmarked lane work' carries no Loop-Session trailer`
  - p2 (the primary checkout's HEAD left on wi-2 before the leg, then an unmarked commit on main) -> `p2 trunk judged as: refs/heads/wi-2`, `p2 audit passes: trunk 0 commit(s); archive/lanes absent; lane main window none`

**Findings:**

- [MINOR] scripts/coordinator/overnight_legs.py:247 -> `pre_leg` re-derives trunk from the primary checkout's HEAD at every leg. A leg that leaves that checkout on another branch makes the next leg's audit judge that branch as "trunk". Real trunk is then judged only by the lane rule, which treats it as a person's lane and judges nothing. I confirmed this by running probe p2: an unmarked commit on `main` passes. It is reachable only off procedure: kit commands run from trunk, and the launcher usually stops first on "wrote no new handoff". (B1: confirmed by running) -> bind trunk's ref once per run in `prepare_run`, and stop the run when a leg ends with HEAD naming another branch. That is a single owning boundary, so no unrepresentable-construction clause is owed. -> @owner
- [MINOR] scripts/coordinator/overnight_legs.py:332 -> the two-snapshot binding cannot see a branch created and deleted inside one leg. Such a branch is in neither snapshot, so it is not even logged as deleted. An unmarked plumbing or `--no-verify` commit on it can reach trunk through a marked squash, or on a merge's second parent, with no rule judging it. I confirmed this by running probe p1, which passes, while p1b with the lane kept stops. The spec's S3 "Default" promises that the audit judges "every commit the leg added to trunk, to `archive/lanes` and to any branch it created or moved". It is reachable only off procedure: the recipes never delete a lane, and the commit floor refuses an unmarked porcelain commit. (B1: confirmed by running) -> state the gap in the launcher docstring and in the WI's Trust/S3 text: a ref created and deleted within one leg, and a merge's non-first-parent commits on trunk, are outside the binding. This cannot be made unrepresentable here: git allows ref deletion and plumbing commits, and the launcher observes only ref outcomes, so the wording, not a new guard, is the fix. -> @owner
- [MINOR] scripts/coordinator/overnight_legs.py:287 -> `lane_claimed` is a third copy of "the newest claim of a branch on trunk's first-parent line". The other two are project-trajectory/scripts/integrate.py:1232 `_loop_claimed` and project-trajectory/scripts/agent_common.py:1205. When WI-918 teaches the slot to read the re-claim, this copy must change in step or the "merge slot's own rule" drifts (CLAUDE.md "Consolidate, don't duplicate"). -> have WI-918's provenance-module move take one claim reader with a checked read that both the slot and the launcher call. Until then, name this copy in WI-918's spec as a site it must update. No guard is added. -> @owner

VERDICT: APPROVE findings=3
