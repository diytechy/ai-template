Reviewed: 737ab5c54f74dbd1b1c07edccdbb7f7ff6af3436

## Verified

`git rev-parse HEAD` printed 737ab5c54f74dbd1b1c07edccdbb7f7ff6af3436. Before hunting, I named the failure classes this change admits, in severity order. (1) Fail-open: the declared bar hides or skips a lint red. (2) Silent wrong content: the LLR-292 amendment changes what the row means. (3) Instruction drift: a bar home still restates the old two-step bar.

I drove the real path, `run_menu.py --file <stub> smoke`, on a `git archive` copy of 737ab5c in my scratch area. In the stub, only the pytest tier and the budget re-run were replaced by `python -c` markers; the three lint steps were the reviewed literal lines.
- On the reviewed tree the chain exits 0 and reaches the budget step.
- With LLR-292's pre-fix clause put back ("no claim is made that crossing count is minimal"), `trace.py --strict` prints `FINDING (requirement form): LLR LLR-292 Detail uses 'minimal' — no test can settle it — name the measurable`. The chain stops before the budget marker and exits 1. So the bar fails closed under cmd.exe `&&`, and the amendment is what clears trunk's last strict red.

The new test `test_the_declared_commit_bar_runs_the_strict_lints_before_its_budget` FAILS against `aac06695e`'s `docs/stack.ini` (AssertionError at tests/test_smoke_budget.py:119) and passes at the tip.

K1: LLR-292's new Detail is true. The T8 critique keeps "crossings minimized" as judged residue (docs/rubrics/dashboard-usability.md:157,177). The obligation, SR-054, TC-305 and Status are unchanged (K3). The in-lane.md claim that the traceability step starts at DevStg-Impl matches check.py:747 (`STAGE_IMPL`).

K4: the only changed `scope: kit` file is spine-authoring/references/in-lane.md, and it has a RESYNC entry `[since aac06695e]`. byte-budget-guard, session-protocol and coordinator-cycle are `scope: this-repo`, which bootstrap.py:1903 never materializes. The `.claude/skills` and `.agents/skills` copies are byte-identical to source (cmp). CLAUDE.md is 7,991 bytes, matching the stamped baseline and under the 8,500 cap. Nothing under project-trajectory/hooks/ changes. The excluded generated and telemetry paths have no diff in range. The phase-0 baseline manifest is on trunk at the lane base (fa4bd0c49).

Done-when map:
- LLR-292 names the measurable: covered (trace --strict exit 0; pre-fix red observed).
- An amendment sitting's act re-attests LLR-292: UNCOVERED in range. By the cycle, the act is the lane's last spine commit after rebase (coordinator-cycle §4), so it is pending, not a defect. The landing must carry it.
- `[run] smoke` order: covered by the new test.
- CLAUDE.md, session-protocol §3 and recipes §6 name the bar; the builder and Terra briefs: read, as stated.
- Byte budget and skill copies: test_skills_sync passed; cmp identical.
- Closure check (in-lane.md, recipes §1) and landing check (recipes §3): read, as stated. See the one finding.
- Hooks unchanged: empty diff.
- RESYNC entry: present, test_resync_pack passed. If trunk moves before landing, re-anchor it at the landing's parent.
- Baseline manifest: present.
- Bar green on the landing tip: partially verified. The lint steps are green: trace --strict exit 0, check_trajectory --strict clean, check_docs --stale OK. Per the brief, I did not run the smoke tier or the budget step.

Note: `trace.py --strict` in the worktree rewrote the gitignored docs/test/report.md, and nothing tracked changed. `git status` is clean.

## Commands

- `git rev-parse HEAD` -> 737ab5c54f74dbd1b1c07edccdbb7f7ff6af3436
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r1/C/wi-914 tests/test_smoke_budget.py tests/test_check_smoke_budget.py tests/test_dogfood_sync.py tests/test_skills_sync.py tests/test_resync_pack.py tests/test_check_docs.py` -> 135 passed, 1 skipped in 115.68s (the skip is the posix-shell environment gate)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> check_trajectory: clean (913 work item(s), 798 done (87%), 30 cancelled, graph acyclic). exit=0
- `python project-trajectory/scripts/trace.py --strict` -> Traceability: SN=31 SR=131 LLR=302 TC=316 orphans=0 integrity=0 ... drafts=1 ... interface-findings=0 ac-advisories=1 paraphrase-advisories=3. exit=0
- `python project-trajectory/scripts/check_docs.py --root . --stale` -> check_docs: OK - 2589 doc(s), 3675 intra-repo link(s), 0 broken (1 orphan warning(s)). exit=0
- probe on the archive copy: `run_menu.py --file stub-stack.ini smoke` -> exit=0 (reached STUB-BUDGET). With LLR-292's pre-fix clause restored: FINDING (requirement form) LLR-292 'minimal'; exit=1; STUB-BUDGET not reached.
- probe: `pytest tests/test_smoke_budget.py::test_the_declared_commit_bar_runs_the_strict_lints_before_its_budget` against aac06695e's stack.ini -> 1 failed (AssertionError, tests/test_smoke_budget.py:119)

## Findings

- [MINOR] project-trajectory/skills/coordinator-cycle/SKILL.md:195 -> K4-adjacent dogfood drift (no rubric anchor fits exactly; the nearest is the "don't restate a rule" principle that K-anchors serve). Land step 3 still names `check_trajectory.py --strict` as the landing check. Recipes §3 (project-trajectory/skills/coordinator-cycle/references/recipes.md:309) now replaces it with the commit bar on the staged squash, which also carries `trace.py --strict`. A coordinator reading only the SKILL summary would skip `trace.py --strict` at landing. -> Have step 3 point at the bar ("run the commit bar on the staged squash") or drop the command and defer to recipes §3, then re-sync both copies. -> @coordinator

VERDICT: APPROVE findings=1
