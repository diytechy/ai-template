+++
id = "WI-751"
title = "adjudicate: LLR-288, LLR-289, TC-301, TC-302 - spine row(s) authored Drafted on merged trunk 579cd18..9dbb510 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-288", "LLR-289", "TC-301", "TC-302"]
+++

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- LLR-288 authored in `docs/requirements/low-level-requirements.toml`
- LLR-289 authored in `docs/requirements/low-level-requirements.toml`
- TC-301 authored in `docs/test/test-cases.toml`
- TC-302 authored in `docs/test/test-cases.toml`

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.

## Dispositions

The adjudication is recorded at
`docs/reviews/wi-751-adjudicate-llr-288-llr-289/001-ADJUDICATE-83db9d7.md`,
under the governing line `OUTCOME: RETURN rows=4`. LLR-288, LLR-289 and TC-301
are approved and anchored in this lane's approval commit. TC-302 is RETURNED and
stays `Drafted`, every cell byte-exact. This is one draft: one lane, and one
adjudication at its merge.

```toml
title = "TC-302 return: state and evidence LLR-289's terminal-row resolution (a wi_refs entry naming an archived work item is no finding), and drive the checker, not only the scheduler, on a repo with no open-items registry"
workstream = "process"
safety_class = "spine"
buildtier = "quick"
priority = 3
specref = "docs/test/test-cases.toml"
sr_refs = ["SR-148"]
bar = "DevStg-Tests"
```

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
