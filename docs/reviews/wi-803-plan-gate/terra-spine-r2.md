Amended four cells; no IDs, statuses, or non-registry files changed.

- LLR-069 detail  
  Before: “A single run treats uncovered Done-when or finding clauses and missing SR/TC coverage as findings; a dual run retains uncovered clauses as report payload.”  
  After: “Either run treats an unexplained clause gap as a finding; a single run also treats an uncited item SR, or a verifying TC neither named nor excluded, as findings (an item SR cannot be excluded).”  
  Why: reflects the adjudicated DUAL policy and cite-only item SRs.

- IF-060 data  
  Before: “0 clean | 1 findings, including SINGLE gaps or SR/TC misses | 2 malformed input, including missing Done-when or findings”  
  After: “0 clean | 1 findings, including unexplained clause gaps or SINGLE SR/TC misses | 2 malformed input, including missing Done-when or findings”  
  Why: DUAL gaps now also produce exit 1.

- TC-069 expected  
  Before: “A reasoned exclusion passes; an unexplained SINGLE Done-when or finding gap, undeclared or reasonless exclusion, or missing SR/TC coverage exits 1 by name; a missing Done-when exits 2; DUAL report bytes remain unchanged; absent registries note without failure.”  
  After: “A reasoned exclusion passes; an unexplained clause gap in either run (SINGLE Done-when or finding, DUAL goal clause), undeclared or reasonless exclusion, an item SR no row cites (even if excluded), or a verifying TC neither named nor excluded exits 1 by name; a missing Done-when exits 2; DUAL report bytes remain unchanged; absent registries note without failure.”  
  Why: makes all new failure modes explicit.

- TC-069 evidence  
  Before: ended with `test_the_dual_report_is_byte_identical_to_the_pre_gate_report`.  
  After: names `test_dual_report_bytes_unchanged_and_unexplained_dual_gaps_fail`, both new DUAL-gap tests, `test_an_item_sr_cannot_be_excluded_only_cited`, and `test_plan_coverage_step.py::test_an_unexcluded_gap_in_plan_a_alone_bounces_only_a`.  
  Why: every cited function exists and covers the amended contract.

Checked `LLR-069`’s code symbols: no function was added, removed, or renamed, so its existing symbol list remains correct. IF-153 also remains accurate: reports still contain coverage/exclusions, SINGLE SR/TC diff, and DUAL pairwise diff.

Checks:

- `check_trajectory.py --strict` — passed: `clean (820 work item(s), 723 done (88%), 26 cancelled, graph acyclic).`
- `pytest -q -p no:cacheprovider -n 0 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-803-terra2 tests/test_plan_coverage.py tests/test_plan_coverage_step.py` — `31 passed in 4.42s`.

TOML load and touched-list assertions also passed.