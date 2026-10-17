Reviewed: 777a53d7badab4f1591acd83520bf9e45c3fcdc0

Verified: Full-lane review, convergence stance, of 61ee4e165...777a53d7b under the brief's exclusions, against WI-935's spec and rubric docs/rubrics/kit-change-review.md. The failure classes I hunted first were fail-open (a red tier passing the bar, or the bar's tier differing from the one it replaced), then silent wrong content (stale prose). Both came up empty.

- Fail-open. I drove the shipped `main` in process for the pre-fix (61ee4e165) and the new script with a stand-in tier: exit codes 3, 0, 4 with a 0 s budget, 5, and -1, in both modes. The pre-fix script returns 0 on every red tier and 1 on red plus over budget. The new script returns the tier's own code (3/3/4/5) in both modes, 0 when green and within budget, and 1 when green and over budget in enforce mode. It prints the `smoke wall-clock budget:` line every time, and the red-tier note on every red run.
- CLI path. I also drove the script as a subprocess from a copied root with a stand-in `[product] test`, so `sys.exit` passes the code through. Codes 3 and 5 exit 3 and 5. An unrepresentable Windows code (-1 seen as 4294967295, or 3221225477) still exits nonzero (127 / 1), so it fails closed. That is a coverage-extension note, not a finding.
- Same tier. `smoke_argv` resolves `[product] test` plus `[tiers] smoke` to `<interpreter> -m pytest -q -n auto -m smoke`, the exact step the line drops. The new line is the spec's verbatim four-step chain, with the budget step last.
- Done-when map:
  - The step-list test pins the exact four steps and one tier step, and fails on the old five-step line (exact list equality).
  - `test_a_red_tier_exits_with_its_own_code_and_still_reports_its_time` covers the red-tier case. It fails on the pre-fix code, which returns 0 (observed above).
  - The green-within-budget case and the red-over-a-0-s-budget case are covered by the two sibling tests.
  - The four existing tests are unchanged in the diff and pass.
  - The new tests collect under `-m smoke`.
  - Exit coverage (zero passes, nonzero passes through, lint red first through `&&`) matches the code.
  - Per-agent skill copies are byte-identical (`cmp` across .claude, .agents and project-trajectory, for both skills).
  - `check_trajectory.py --strict` exits 0.
  - Not verified by me: the "bar green on the lane tip, pasted, with the log fragment's timings" item. The launcher barred the smoke tier, and docs/log.d is outside my reading scope.
- Rubric anchors:
  - K1/K2/K3: no spine row, `Implements:` tag or status changes.
  - K4: no shipped file changed, so no RESYNC entry is owed. Both skills are `scope: this-repo`, and bootstrap.py excludes them downstream.
- Stale-text sweep: no remaining live text says the bar runs the tier twice or first. Hits are only in historical handoffs.
- Disclosure: one repo-wide grep for `check_smoke_budget` printed a line of docs/decisions/wi-935.toml. I did not open or rely on it, and the findings below come from my own runs.

Commands:
- `git rev-parse HEAD` -> 777a53d7badab4f1591acd83520bf9e45c3fcdc0
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../gate-opus/wi-935 tests/test_check_smoke_budget.py tests/test_smoke_budget.py` (via lowprio.py) -> `11 passed in 7.24s`, exit 0
- `python project-trajectory/scripts/check_trajectory.py --strict` (via lowprio.py) -> `check_trajectory: clean (934 work item(s), 812 done (87%), 30 cancelled, graph acyclic).`, exit 0
- `python -m pytest --collect-only -m smoke tests/test_check_smoke_budget.py tests/test_smoke_budget.py` -> the new in-process cases are collected in the smoke tier
- `python -I gate-opus/probe/probe.py` (in process, pre-fix vs new `main`, with a stand-in tier) -> old 0/0/0/1/0/1/0/0, new 3/3/0/4/5/1/0/4294967295
- `python -I gate-opus/probe/cli/scripts/check_smoke_budget.py --mode warn|enforce` (a copy, with a stand-in `[product] test`) -> exits 3, 3, 0, 0, 5, 5, 127, 127, 1, 1

- [MINOR] scripts/check_smoke_budget.py:33 -> for clarity (K1): the new sentence says the dial "was settled by OI-52 ruling (a), 2026-08-23". docs/requirements/open-items.toml `[open_item.OI-52]` records `ruled_date = "2026-08-21"`. 2026-08-23 is WI-496's wiring date, the date CLAUDE.md and the session-protocol skill also attach to the ruling, and the spec prescribed it. A reader checking the record finds a different date -> say "OI-52 ruling (a) (ruled 2026-08-21; wired into the commit bar by WI-496, 2026-08-23)", or cite the ruling without a date -> @owner

VERDICT: APPROVE findings=1
