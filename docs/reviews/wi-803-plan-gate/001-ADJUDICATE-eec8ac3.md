# 001 — ADJUDICATE (independent, Claude Opus) — WI-803 plan gate, spine rows at `eec8ac3c`

Adjudicator: independent Claude Opus. I authored none of WI-803's code or rows.
Anchors: `docs/archive/last_approved/` (LLR, TC: copied at `5be0bc4d`, equal to
trunk `883b3edf`); IF rows against trunk `883b3edf:docs/requirements/interfaces.toml`.
Code read: `project-trajectory/scripts/plan_coverage.py`, `plan_coverage_step.py`,
`tests/test_plan_coverage.py`, `tests/test_plan_coverage_step.py`.

## Basis (probed, not trusted)

- Lane bar: `pytest tests/test_plan_coverage.py tests/test_plan_coverage_step.py
  tests/test_dual_plan_round.py`: **38 passed**.
- **Mutation probes** on a scratch copy (`review-tmp/wave14/adj803-mut`), 22
  single-point mutants of `plan_coverage.py`. Each mutant was run against (a) the
  TC-069 `evidence` node list as amended and (b) the two whole test files.
  - Killed by both: DUAL gaps not findings (M1), item SR excludable (M2),
    reasonless exclusion still excludes (M11), excluded TC still missing (M12),
    `F#` ignored (M14), empty Done-when not malformed (M15), `excluded:` lines
    dropped (M16), pairwise diff dropped (M17), SINGLE diff findings dropped
    (M20), and an unknown ref in `Excludes:` accepted (M21).
  - **Survive the amended evidence list, killed by the whole file**: unknown
    SR/TC ref accepted (M3), cycle undetected (M4), unknown predecessor accepted
    (M5), duplicate `Plan-WI` accepted (M6), unknown IF accepted (M7), plan
    without a table exits 1 (M8), goal without clauses exits 1 (M9), an absent
    SR registry becomes a finding (M10), and a rationale-less `Proposed:`
    accepted (M18). These are exactly the reference, graph, absent-registry and
    malformed-input cases TC-069's `method` still names.
  - Survive both (test gaps; code review's, not row truth): a TC verifying a
    *non-item* SR pulled into the SINGLE diff (M13), and a row citing nothing
    accepted (M19).
- **Replacement texts checked**: applied on the scratch copy, `trace.py --strict`
  shows no new form finding or advisory on LLR-069, TC-069, IF-153 or IF-161 (the
  only form finding is the pre-existing LLR-292). The 31 plan-coverage tests
  stay green. An earlier IF-153 draft that kept the "payload" clause hit the
  160-character `Data` ceiling. That clause's home is the owner's
  `Contract IF-153:` body, which still states it.
- **Act dry run** (`baseline_snapshot.refresh_refusal`, read-only):
  `--approves` on both registries plus `--reattests LLR-069,TC-069` is not
  refused. The absorbed set is LLR-069, TC-069 and, outside this act's write
  scope, `components.toml` CMP-006. CMP-006 is another act's drift; this lane
  did not touch it.

## Rulings

- [RETURN] LLR-069 detail -> before: rival-plan comparison only, with uncovered clauses as payload; "findings (bad refs or plan graphs) exit 1", malformed exits 2, an absent registry notes -> after: one grammar for DUAL and SINGLE runs; an unexplained clause gap is a finding in either run; SINGLE adds an uncited item SR and an unanswered TC as findings; "Findings exit 1" -> the obligation moved (MEANING: a gapped DUAL plan that exited 0 now exits 1, and the SINGLE run is new). But the cell is RETURNED for two reasons. (1) It drops the old text's classification "(bad refs or plan graphs) exit 1". The new text says the run "resolves references" and "validates dependencies", but it classifies only the gaps as findings, so an implementation that exits 2 (malformed) on an unknown SR or a predecessor cycle satisfies it. The code still makes those findings: mutants M3–M7 and M18, and the IF-060 contract "1 says the plans were read and something in them is wrong". (2) "a verifying TC" has no object. Read as "any TC", it would demand every registry TC be named; the code diffs only TCs verifying an item SR (`spine_diff`, `plan_coverage.py:450-453`).
  - old: `Uses one plan-table grammar for dual goal and single item runs. Resolves clause, SR, TC and interface references; validates dependencies and reasoned exclusions; emits coverage and pairwise differences. Either run treats an unexplained clause gap as a finding; a single run also treats an uncited item SR, or a verifying TC neither named nor excluded, as findings (an item SR cannot be excluded). Findings exit 1, malformed input (including an item with no Done-when items) exits 2, and an absent registry notes without failing.`
  - new: `Uses one plan-table grammar for dual goal and single item runs. Resolves clause, SR, TC and interface references; validates dependencies and reasoned exclusions; emits coverage and pairwise differences. Either run treats an unexplained clause gap as a finding; a single run also treats an uncited item SR, or a TC verifying one that no row names nor excludes, as findings (an item SR cannot be excluded). Findings (these gaps, and bad references, plan graphs or exclusions) exit 1, malformed input (including an item with no Done-when items) exits 2, and an absent registry notes without failing.`
  - `title` ("Rival-plan coverage comparison" -> "Plan coverage gate") is clarity on its own; the row is MEANING through `detail`. `code_symbol` is a traced cell; its 24 names match the module's `Implements: SR-155, LLR-069` tags plus the five original symbols.
- [RETURN] TC-069 expected/evidence -> before: clean plans emit pairwise coverage; findings exit 1; malformed inputs exit 2; absent registries note -> after: a reasoned exclusion passes; an enumerated set of gap and exclusion findings exits 1; "a missing Done-when exits 2"; DUAL report bytes unchanged; absent registries note -> the oracle moved (MEANING: the pre-gate DUAL fixture's run now expects exit 1). But the cells are RETURNED. (1) `expected` narrows the oracle below what the code enforces and what `method` still runs. It lists no exit for a bad reference or plan graph (the old "findings exit 1"). It narrows "malformed inputs exit 2" to the Done-when case alone, though a goal with no clauses, a plan with no table and a missing file still exit 2. It drops "clean plans emit pairwise coverage". (2) `evidence` (a traced cell, judged here for truth) was narrowed from the whole file to 13 nodes. It names none of the reference, graph, absent-registry or no-table/no-clause tests that `method` names. Nine mutants (M3–M10, M18) pass the cited evidence, and every one of them is killed by the whole file. Restoring the whole file keeps the step-module node.
  - expected old: `A reasoned exclusion passes; an unexplained clause gap in either run (SINGLE Done-when or finding, DUAL goal clause), undeclared or reasonless exclusion, an item SR no row cites (even if excluded), or a verifying TC neither named nor excluded exits 1 by name; a missing Done-when exits 2; DUAL report bytes remain unchanged; absent registries note without failure.`
  - expected new: `A reasoned exclusion passes and clean plans emit per-plan and pairwise coverage; a bad reference or plan graph, an unexplained clause gap in either run (SINGLE Done-when or finding, DUAL goal clause), an undeclared or reasonless exclusion, an item SR no row cites (even if excluded), or a TC verifying an item SR that no row names nor excludes exits 1 by name; malformed input, a missing Done-when included, exits 2; DUAL report bytes remain unchanged; absent registries note without failure.`
  - evidence old: `tests/test_plan_coverage.py::test_single_plan_covering_or_excluding_every_clause_passes; tests/test_plan_coverage.py::test_single_plan_missing_a_done_when_item_exits_1_naming_it; tests/test_plan_coverage.py::test_an_exclusion_without_a_reason_is_a_finding; tests/test_plan_coverage.py::test_an_exclusion_of_an_undeclared_clause_is_a_finding; tests/test_plan_coverage.py::test_single_sr_tc_diff_names_an_uncovered_sr_and_an_unnamed_tc; tests/test_plan_coverage.py::test_single_tc_excluded_with_a_reason_passes; tests/test_plan_coverage.py::test_open_review_findings_are_clauses_on_a_replan; tests/test_plan_coverage.py::test_an_item_without_done_when_is_a_malformed_input; tests/test_plan_coverage.py::test_dual_report_bytes_unchanged_and_unexplained_dual_gaps_fail; tests/test_plan_coverage.py::test_a_dual_gap_excluded_with_a_reason_passes; tests/test_plan_coverage.py::test_a_dual_gap_fails_naming_only_its_plan; tests/test_plan_coverage.py::test_an_item_sr_cannot_be_excluded_only_cited; tests/test_plan_coverage_step.py::test_an_unexcluded_gap_in_plan_a_alone_bounces_only_a`
  - evidence new: `tests/test_plan_coverage.py; tests/test_plan_coverage_step.py::test_an_unexcluded_gap_in_plan_a_alone_bounces_only_a`
  - `method` (the new wording) is clarity-plus-scope and true as written.
- [MEANING] IF-060 data -> `0 clean | 1 findings | 2 malformed input` -> exit 1 now includes unexplained clause gaps (either run) and SINGLE SR/TC misses; exit 2 includes a missing Done-when or an empty findings file -> a DUAL plan with an unexcluded gap moves from 0 to 1, so the alphabet's meaning moved. True of the code (`_check_one`, `load_item`, `_declared`). The row is `Drafted`: no attestation to keep or re-take.
- [MEANING] IF-152 data -> `--goal, --root, --out, then the plan paths` -> `--goal | --item [--findings], --root, --out, then the plan paths` -> a new mode and a new flag on the argv surface. True of `_parse_args` (mutually exclusive required group; `--findings` refused without `--item`). `Drafted`.
- [RETURN] IF-153 data -> before: uncovered clauses per plan, the brief payload -> after: coverage and exclusions, a SINGLE SR/TC diff, "a DUAL pairwise diff" -> the report's content grew (MEANING). RETURNED because "a DUAL pairwise diff" is untrue of a reachable case. `format_report` writes the pairwise diff for any run over two or more plans, a SINGLE run included (IF-152's plan paths are plural in both modes; `plan_coverage.py:524-539`), and PROCESS.md says this cell is fed verbatim into planner briefs. The dropped "payload" clause is not restored: the cell has a 160-character ceiling, and the owner's `Contract IF-153:` body carries that property.
  - old: `the --out coverage report: coverage and exclusions, a SINGLE SR/TC diff, and a DUAL pairwise diff`
  - new: `the --out coverage report: coverage and exclusions per plan, a SINGLE SR/TC diff, and a pairwise diff over two or more plans`
- [MEANING] IF-242 requestors -> integrate, intake, agent_loop -> plus `scripts/plan_coverage` -> a new requestor of the seam. True: `load_item` calls `kitlib.done_when.items` (`plan_coverage.py:594`). `Drafted`.

## Terra's two refusals

- **No SR-154 on LLR-069: upheld.** SR-154's text is independent review routing
  across families. It demands no plan gate, so citing it would be the silent
  mis-trace that the spine-authoring skill §2(c) forbids. **Standing trace
  finding (not this lane's to fix):** LLR-069's SINGLE run is not demanded by
  any SR's text today. SR-155 is contested planning rounds only, and nothing
  invokes `--item` yet (no caller in `scripts/` or `prompts/`). Its parent
  arrives where the approved matrix puts it: S788-single-plan amends SR-154 for
  "planning and the dial" and adds the LLR/TC under it (design README
  `:212`, `:221`). That row's Done-when should carry re-parenting LLR-069's
  SINGLE run (or moving it to the new LLR), so the derivation does not stay
  silent.
- **No IF-057 change: upheld, but incomplete.** IF-057 is the `interfaces.toml`
  format seam, and plan_coverage reads that file as before. The matrix
  entry traces to a pre-existing mislabel: `plan_coverage_step.py:10` and
  `plan_artifacts.py:7` call `plan_coverage.py` "IF-057", and IF-057's own
  `notes` describe the coverage report. Both are separate findings. But the
  refusal names the test-case registry as "a separate input" and stops there.
  That input IS a declared seam, **IF-161** (`docs/test/`, an enumerated
  consumer list). This lane makes `plan_coverage` a new reader of it
  (`verifying_tcs`, `_load_gate` `:681`), and IF-161 does not list it. Owed
  in this lane with the RETURN round (IF-161 `consumers`, a `Drafted` row):
  - old: `["scripts/acceptance_record", "scripts/adjudicate_brief", "scripts/agent_loop", "scripts/baseline_snapshot", "scripts/check_doc_refs", "scripts/check_flows", "scripts/check_trajectory", "scripts/gen_okf", "scripts/gen_release_checklist", "scripts/intake", "scripts/spine_rules", "scripts/trace", "scripts/traj_parse", "external:downstream adopter"]`
  - new: `["scripts/acceptance_record", "scripts/adjudicate_brief", "scripts/agent_loop", "scripts/baseline_snapshot", "scripts/check_doc_refs", "scripts/check_flows", "scripts/check_trajectory", "scripts/gen_okf", "scripts/gen_release_checklist", "scripts/intake", "scripts/plan_coverage", "scripts/spine_rules", "scripts/trace", "scripts/traj_parse", "external:downstream adopter"]`

## Aftermath (not taken: the coordinator gates the act on the code review)

LLR and TC sit on a rung `human_approval_through = "DevStg-Boundary"`
releases, so once the RETURN text lands byte-exact I would bless both MEANING
rows myself. That needs a fresh ruling on the landed text, a `002-ADJUDICATE-<sha>.md`
in this folder. The IF rows are all `Drafted` (221 of 221 in the registry).
A `Drafted` row never drifts and owes no act, so `interfaces.toml` stays out of the
snapshot.

VERDICT: MEANING rows=6
