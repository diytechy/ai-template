Reviewed: 627e98adcb7065f2ba36a2803873be8b589c26b9

Verified: HEAD is the reviewed commit. I read the scoped diff in full: scripts/check_smoke_budget.py, both test files, docs/stack.ini [run] smoke, and the three copies each of the coordinator-cycle recipes and the session-protocol skill. I also read the spec docs/work/active/wi-935/WI-935-bar-runs-tier-once.md. The worst failure class this change admits is fail-open: the bar passing a red tier now that the budget step's timed run is the bar's only tier run. I hunted that first.

I drove the real `main` of both the pre-fix script (61ee4e165) and the tip script in process, with stand-in tiers. The tip passes the tier's own code through in both modes: tier codes 1, 3, 4 and 5 each return the same code, over budget or not. A green tier returns the budget verdict. The pre-fix script returned 0 for a red tier in both modes, and 1 rather than 4 for a red tier over budget in enforce mode. So test_a_red_tier_exits_with_its_own_code_and_still_reports_its_time and test_a_red_tier_over_budget_reports_both_and_exits_with_its_code both fail on the pre-fix code, as the Done-when requires.

I checked the chain through run_menu's own runner path (`subprocess.run(line, shell=True)`, cmd.exe on this box). A nonzero code from the last `&&` step comes back unchanged (3 and 5), and an earlier red step (2) stops the chain. So the bar is nonzero exactly when a lint is red, the tier is red, or the tier breaches the budget. Tier failures are reported only when no lint is red.

POSIX `sys.exit` truncates codes modulo 256, which could in principle turn a nonzero code into 0. pytest's codes are 0 to 5 and a signal-killed child's code is negative, so no reachable code wraps to 0.

The ordering claim also holds. The lints' one root write is the gitignored docs/test/report.md, and every test that reads a report.md reads a scaffold's, through a `root` argument.

All seven tests in tests/test_check_smoke_budget.py are collected under `-m smoke`, so the new cases stay in the tier. The four existing cases are byte-unchanged in the diff. The skill copies under .claude/, .agents/ and project-trajectory/skills/ are byte-identical (sha1 334c2b6b for recipes.md and 85d3ce6f for SKILL.md).

On K4: both skills are `scope: this-repo`, and bootstrap excludes them ("never materialized downstream"). scripts/, tests/ and the [run] section are repo-own, so no RESYNC entry is owed. K1 to K3 do not apply: the diff changes no requirement row and no `Implements:` tag.

Done-when coverage map:

| Done-when item | Coverage |
|---|---|
| (1) The step list, with exactly one tier step | tests/test_smoke_budget.py::test_the_declared_commit_bar_runs_the_strict_lints_before_its_budget. It fails on the old line, whose first element is the direct pytest step. |
| (2) A red tier returns 3 in both modes | test_a_red_tier_exits_with_its_own_code_and_still_reports_its_time. Red before the fix: confirmed. |
| (3) A green tier within budget, and a red tier over a 0 s budget | test_a_green_tier_within_budget_exits_zero and test_a_red_tier_over_budget_reports_both_and_exits_with_its_code. |
| (4) The four existing tests pass unchanged | Yes. |
| (5) Coverage S3 | Probe across codes 0/1/3/4/5, plus the `&&` chain probe. |
| (6) The quiet-bar paste and timings in the log fragment | Not reproduced. docs/log.d is excluded from my reading scope, and the round facts forbid running the smoke tier. |
| (7) The texts, and byte-identical copies | Verified. |
| (8) `check_trajectory.py --strict` exits 0 | Verified. |

Disclosure: the brief's own `trace.py --strict-integrity` run rewrote the gitignored docs/test/report.md in the lane worktree. `git status --porcelain` stays empty, and I made no other write there.

Commands:
- `git rev-parse HEAD` -> 627e98adcb7065f2ba36a2803873be8b589c26b9
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp <brief's path> tests/test_check_smoke_budget.py tests/test_smoke_budget.py` (via lowprio.py) -> `11 passed in 5.80s` (posix-shell gate unsatisfied; 0 skips in these files)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (934 work item(s), 812 done (87%), 30 cancelled, graph acyclic).` exit 0 (4 pre-existing WARNs on other WIs)
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=131 LLR=303 TC=317 orphans=0 integrity=0 ... interface-findings=0 ac-advisories=1 paraphrase-advisories=3.` exit 0
- `python -m pytest --collect-only -m smoke tests/test_check_smoke_budget.py` -> `7 tests collected`
- In-process probe of the pre-fix and tip `main` with stand-in tiers (r1-opus/probe/probe.py). Pre-fix: tier 3 -> 0/0 (warn/enforce); tier 4 over budget -> 0/1. Tip: tier 3 -> 3/3; tier 4 over budget -> 4/4; tier 5 -> 5/5; tier 1 over budget -> 1/1; tier 0 -> 0/0.
- `&&`-chain probe through `subprocess.run(..., shell=True)` -> (0,3)->3, (0,5)->5, (2,0)->2, (0,0)->0

Findings:
- [MINOR] .github/workflows/test.yml:104 -> for clarity. The smoke-budget job's comment still sends readers to "scripts/check_smoke_budget.py for the full measurement, and the owner's queued dial question". This diff rewrote that docstring passage to say OI-52 ruling (a), 2026-08-23, settled the dial. The pointer now names text that no longer exists, and the spec's claim that test.yml "stays true as written" is wrong at this phrase. -> Reword the clause to "and OI-52 ruling (a), which settled the dial", or drop it. -> @owner (anchor: none; CLAUDE.md "Dogfood the philosophy")
- [MINOR] docs/stack.ini:78 -> for clarity. The [smoke-budget] comment still says "`--mode warn` is the local default (report-only) for convenience". The diff corrected the same claim in the script's docstring, because the local commit bar runs `--mode enforce`. The twin was left standing in a second home. -> Mirror the docstring's new wording: the default stays warn for a hand run, while the commit bar, CI and [step:smoke] enforce. Better, state it once and point to the other home. -> @owner (anchor: none; CLAUDE.md single-source-of-truth)

VERDICT: APPROVE findings=2
