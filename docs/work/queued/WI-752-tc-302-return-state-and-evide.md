+++
id = "WI-752"
title = "TC-302 return: state and evidence LLR-289's terminal-row resolution (a wi_refs entry naming an archived work item is no finding), and drive the checker, not only the scheduler, on a repo with no open-items registry"
workstream = "process"
sr_refs = ["SR-148"]
specref = "docs/test/test-cases.toml"
buildtier = "quick"
priority = 3
safety_class = "spine"
bar = "DevStg-Tests"
+++

## Context

Drafted by WI-751 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

IN SCOPE: exactly the text replacements below, copied as written, in one Drafted
row, plus one test. `Status` stays `Drafted`. Do not reword, extend or "improve"
any other part of these cells or of any other cell. A replacement that differs
from the words given here is a new obligation, and the adjudication at this
merge will return it.

THE DEFECT, confirmed at 83db9d75. LLR-289 (approved in this act) resolves
wi_refs "against live and terminal work rows". That clause is what makes it safe
to check ruled history, which points mostly at archived work. TC-302's Method
never states it, so a checker resolving only against queued and active rows
passes TC-302 as written. The case is already tested, by
`test_only_queued_rows_are_held_and_a_drained_frontier_still_lists_gates`
(no finding for an archived WI-688), but that test is outside TC-302's Evidence.
Separately, the Method claims an absent registry yields no finding, yet neither
Evidence test calls `check_trajectory.open_item_wi_ref_findings` on a repo with
no open-items registry. The behaviour holds: a probe at 83db9d75 returns `[]`.

1. **TC-302 (Drafted)**, `method`: replace `assert one finding naming the item and the missing work id; an example row and absent registry yield none.` with `assert one finding naming the item and the missing work id; a wi_refs entry naming a work item that exists only in the terminal archive yields none; an example row and an absent registry yield none from the checker.`
2. **TC-302 (Drafted)**, `evidence`: append `; tests/test_open_item_readiness.py::test_only_queued_rows_are_held_and_a_drained_frontier_still_lists_gates` to the existing value.
3. **Test.** In `tests/test_open_item_readiness.py::test_examples_and_absent_registry_are_inert`, after `path.unlink()`, add `assert ct.open_item_wi_ref_findings(tmp_path, []) == []`. No code changes. Nothing else in TC-302 changes: not `verifies`, `expected`, `level`, `tier` or `phase`.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-058 [project-trajectory/scripts/schedule.py :: ready/frontier/evaluate] tests: (see TC-058) — WI-DAG frontier + deterministic traincar ordering
- LLR-059 [project-trajectory/scripts/schedule.py :: classify/safety_class] tests: (see TC-059) — Pure safety classifier
- LLR-060 [project-trajectory/scripts/trunk_step.py :: REGEN_STEPS/regen] tests: (see TC-060) — next-wi/run-phase retirement + generated status/run-state
- LLR-089 [project-trajectory/scripts/schedule.py :: kind_of/classify] tests: (see TC-091) — Structural safety cross-check
- LLR-123 [project-trajectory/scripts/schedule.py :: frontier/evaluate] tests: (see TC) — Deterministic traincar ordering
- LLR-131 [project-trajectory/scripts/schedule.py :: classify] tests: (see TC) — Contradiction-safe dual-plan class

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-009 scripts/check_trajectory -> scripts/check: exit-code 0 clean · 1 hard error · 2 usage
- IF-010 scripts/gen_arch_map <- scripts/check;scripts/trunk_step: cli --doc | --cli-doc | --contracts-doc | --src | --mode | --check | --strict-parse | --backlink-coverage | --str…
- IF-150 scripts/gen_arch_map -> scripts/check;scripts/trunk_step: exit-code 0 current · 1 a stale target under --check, an unparseable module under --strict-parse, or coverage below the…
- IF-012 scripts/gen_okf -> scripts/check;scripts/trunk_step: exit-code 0 clean, vacuous or opted out · 1 stale, missing or extra bundle file under --check
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-023 docs/work/ -> scripts/check_trajectory;external:downstream adopter: file one Markdown spec per row; status is the directory
