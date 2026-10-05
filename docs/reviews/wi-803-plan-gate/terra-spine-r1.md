Amended only spine registries; no IDs allocated and no statuses changed.

| Row / cell | Before | After | Why |
|---|---|---|---|
| LLR-069 title | “Rival-plan coverage comparison” | “Plan coverage gate” | It now covers both dual and single modes. |
| LLR-069 code_symbol | “parse_goal/parse_plan/check_plan/find_cycle/format_report” | “parse_goal/parse_plan/check_plan/find_cycle/format_report/_cells/_plan_header/parse_excludes/verifying_tcs/ref_problem/_covers_findings/_interfaces_findings/check_excludes/gap_findings/spine_diff/diff_findings/_plan_section/_malformed/_read/_declared/load_item/_parse_args/_check_one/_load_gate” | Includes every newly tagged function. |
| LLR-069 detail | “Parses rival plan tables; resolves clause/SR/IF coverage; validates dependencies; emits pairwise differences and distinct findings/malformed/absent-registry outcomes. Commensurable plans emit per-plan and pairwise coverage; findings (bad refs or plan graphs) exit 1, malformed inputs exit 2, and an absent registry notes without failing.” | “Uses one plan-table grammar for dual goal and single item runs. Resolves clause, SR, TC and interface references; validates dependencies and reasoned exclusions; emits coverage and pairwise differences. A single run treats uncovered Done-when or finding clauses and missing SR/TC coverage as findings; a dual run retains uncovered clauses as report payload. Findings exit 1, malformed input (including an item with no Done-when items) exits 2, and an absent registry notes without failing.” | Pins the implemented gate semantics. |
| IF-060 data | “0 clean \| 1 findings \| 2 malformed input” | “0 clean \| 1 findings, including SINGLE gaps or SR/TC misses \| 2 malformed input, including missing Done-when or findings” | Updates the exit-code alphabet. |
| IF-152 data | “--goal, --root, --out, then the plan paths” | “--goal \| --item [--findings], --root, --out, then the plan paths” | Records the additive CLI surface. |
| IF-153 data | “the --out coverage report: uncovered clauses per plan — the payload the critic and arbiter briefs embed” | “the --out coverage report: coverage and exclusions, a SINGLE SR/TC diff, and a DUAL pairwise diff” | Captures both report modes. |
| IF-242 requestors | `["scripts/integrate", "scripts/intake", "scripts/agent_loop"]` | `["scripts/integrate", "scripts/intake", "scripts/agent_loop", "scripts/plan_coverage"]` | `plan_coverage` imports and calls `kitlib.done_when`. |
| TC-069 method | “Run rival plan coverage, reference, graph, absent-registry, and malformed-input cases.” | “Run dual and single plan coverage, reference, graph, exclusion, SR/TC-diff, absent-registry, and malformed-input cases.” | Covers the expanded test scope. |
| TC-069 expected | “Clean plans emit pairwise coverage; findings exit 1; malformed inputs exit 2; absent registries note without failure.” | “A reasoned exclusion passes; an unexplained SINGLE Done-when or finding gap, undeclared or reasonless exclusion, or missing SR/TC coverage exits 1 by name; a missing Done-when exits 2; DUAL report bytes remain unchanged; absent registries note without failure.” | States the tested pass/fail conditions. |
| TC-069 evidence | “tests/test_plan_coverage.py” | Named nine concrete `test_plan_coverage.py` functions for exclusions, D/F gaps, SR/TC diff, malformed input, and DUAL byte identity. | Evidence now names real tests that cover the claims. |

Builder-list disposition:

- Confirmed the 19 newly `Implements: SR-155, LLR-069`-tagged functions and added all to LLR-069.
- Confirmed the LLR, TC-069, IF-060, IF-242, IF-152, and IF-153 amendments.
- Declined adding SR-154 to LLR-069: the module’s tags name SR-155 only, and the WI-788 matrix assigns the future SR-154 integration row to `S788-single-plan`.
- Refuted the IF-057 amendment: it is the `interfaces.toml` registry seam. The item spec and test-case registry are separate inputs, not information carried by IF-057.

Checks:

- `check_trajectory.py --strict`: passed — `clean (819 work item(s), 721 done (88%), 26 cancelled, graph acyclic).`
- `trace.py --strict`: expected nonzero due to pre-existing `LLR-292 Detail uses 'minimal'`; summary: `orphans=0 integrity=0 ... form-findings=1`.
- Required pytest command was started with `-n 0` and the literal required base temp. Its initial invocation returned exit 0 from the shell wrapper, but its child processes continued. Subsequent clean attempts hit Windows `WinError 32` cleanup locks in `C:/Projects/ai-template.wt/review-tmp/wi-803-terra` (17 passed, 4 setup errors on the isolated run). Manual removal of that generated test directory was blocked by environment policy.

Unsettled: the final full pytest result needs rerunning once the fixed base-temp directory can be cleared without Windows locks.