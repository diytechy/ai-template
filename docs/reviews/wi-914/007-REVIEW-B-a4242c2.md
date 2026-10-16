Reviewed: a4242c242c1a6e85692638b941e34a07cc1f38ba

Verified (full-lane review, convergence stance; no earlier verdict, decision record or lane commit message read). I hunted three failure classes first. (1) Fail-open: the declared bar skipping a lint or letting a lint red pass. (2) Silent wrong content: the LLR-292 amendment changing the obligation, or the snapshot and act drifting from the live row. (3) Lost coverage: the landing check swapping `trace.py --strict-integrity` for a weaker form. Findings on each:
- **Fail-open.** I drove the real `run_menu.py` launch path, with `--file` pointing at a scratch stack.ini, over a `git archive` of the trunk base (cc98db557), where LLR-292 is still red. The line was the lane's own `[run] smoke` chain with stand-ins for only the pytest and budget steps. It exited 1 on `FINDING (requirement form): LLR LLR-292 Detail uses 'minimal'`, and the budget stand-in never ran. So a lint red fails the bar, and the budget step runs last.
- **Lost coverage.** `trace.py`'s `exit_code` (project-trajectory/scripts/trace.py:6338) makes `--strict` a superset of `--strict-integrity`, so the recipes §3 replacement loses nothing.
- **Silent wrong content.**
  - The LLR-292 Detail change is confined to the last clause. It names the measurable (perpendicular crossing count) and declares no bound on it, which is consistent with T8's "crossings minimized" judged residue (docs/rubrics/dashboard-usability.md:152). SR-054 and TC-305 are untouched.
  - The live and snapshot copies of low-level-requirements.toml have identical blob hashes (3fe91490c). acts.toml carries seq 120, re-attesting LLR-292, the next seq after trunk's 119.
  - At the base, `trace.py --strict` exits 1 on exactly that finding; at the tip it exits 0.
- **The regression test fails before the fix.** I ran `test_the_declared_commit_bar_runs_the_strict_lints_before_its_budget` (tests/test_smoke_budget.py:109) against the base stack.ini: FAIL. Against the tip: PASS.
- **No hidden authored change.** The only `[run]` value changed is `smoke` (docs/stack.ini:1278), and its `.desc` states the order and the reason.

Done-when coverage:
- LLR-292 amended and re-attested: verified by the diff, acts.toml:730, the snapshot, and base-vs-tip `trace.py --strict`.
- `[run] smoke` order: the regression test above.
- `CLAUDE.md`, session-protocol §3 and recipes §6 name the one command: inspected at CLAUDE.md:60, project-trajectory/skills/session-protocol/SKILL.md:84-97 and project-trajectory/skills/coordinator-cycle/references/recipes.md:608-614. No other home restates the old two-command bar (grep of AGENTS.md, the kit's own .md files, its skills, its agents and the coordinator templates).
- Builder and Terra briefs: .claude/agents/kit-builder.md:40 and scripts/coordinator/terra-spine-prompt.template.md:33, inspected.
- `CLAUDE.md` byte budget: 7,991 bytes of 8,500 (wc). The byte-budget-guard baselines (7,991 and 4,507) match the real sizes.
- Skill copies match their source: test_skills_sync passed.
- Closure and landing checks: project-trajectory/skills/spine-authoring/references/in-lane.md:35-40 and recipes.md:233, 396 and 424, inspected. I confirmed check.py runs the traceability step and `check_trajectory --strict` from DevStg-Impl (check.py:543, :580).
- Hooks unchanged: the diff stat shows nothing under project-trajectory/hooks/.
- RESYNC entry: project-trajectory/RESYNC_PACK.md:8482, anchored at the trunk base, prose only. test_resync_pack passed. It is the only shipped (scope: kit) file the lane touches; the other skills it edits are scope: this-repo, so K4 is met.
- Baseline manifest on trunk: docs/plans/2026-10-11-review-churn/baseline/baseline-manifest.md exists at cc98db557.
- Bar green on the tip: three of the bar's steps (`trace.py --strict`, `check_trajectory.py --strict` and `check_docs --stale`) exit 0. The round facts barred running the smoke tier, so the tier and its budget on the landing tip were not observed by this review.

Rubric (docs/rubrics/kit-change-review.md): K1, K3 and K4 are met; K2 does not apply (no SN or SR cell changed).

Commands:
- `git rev-parse HEAD` -> a4242c242c1a6e85692638b941e34a07cc1f38ba
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../gate/C/wi-914 tests/test_smoke_budget.py tests/test_check_smoke_budget.py tests/test_dogfood_sync.py tests/test_skills_sync.py tests/test_resync_pack.py tests/test_check_docs.py` -> `135 passed, 1 skipped in 86.87s` (1 skip is the posix-shell environment gate)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (929 work item(s), 804 done (87%), 30 cancelled, graph acyclic).` exit 0
- `python project-trajectory/scripts/trace.py --strict` (tip) -> `Traceability: SN=31 SR=131 LLR=303 TC=317 orphans=0 integrity=0 ... interface-findings=0 ac-advisories=1 paraphrase-advisories=3.` (no form-findings field) exit 0
- `python project-trajectory/scripts/trace.py --strict-integrity` (tip) -> same summary line, exit 0
- `python project-trajectory/scripts/check_docs.py --root . --stale` -> `check_docs: OK - 2689 doc(s), 3691 intra-repo link(s), 0 broken (1 orphan warning(s)).` exit 0
- `trace.py --strict` on a `git archive cc98db557` copy -> exit 1, `FINDING (requirement form): LLR LLR-292 Detail uses 'minimal'`, `form-findings=1`
- `run_menu.py --file <scratch probe-stack.ini> smoke` on the base copy (lane's chain, stand-ins for the pytest and budget steps) -> exit 1 at `trace.py --strict`; the budget stand-in did not run
- the regression test, called in-process with `STACK_INI` pointed at the base and then the tip stack.ini -> FAIL on base, PASS on tip
- `git status --short` in the worktree after all runs -> empty (nothing written)

Findings:
- [MINOR] project-trajectory/skills/coordinator-cycle/references/recipes.md:615 -> §6's second bullet still says "one timed run serves both halves of the bar: ... pass it to `check_smoke_budget.py --mode enforce --elapsed <s>`". The bullet above it now makes the bar the single declared `run.cmd smoke` command, which calls the budget step without `--elapsed`, so the tier runs twice inside it. A coordinator who follows the `--elapsed` advice has to hand-compose the chain, which is the route this row closes so that a round's bar cannot skip the strict lints. For clarity, rubric K1 -> reword the bullet: the declared command times the tier in its own last step, and `--elapsed` applies only to a wrapper that still runs every `[run] smoke` step (or drop the bullet) -> @owner

VERDICT: APPROVE findings=1
