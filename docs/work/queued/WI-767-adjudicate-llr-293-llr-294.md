+++
id = "WI-767"
title = "adjudicate: LLR-293, LLR-294, TC-279, TC-306, TC-307 - spine row(s) authored Drafted on merged trunk 122816d..1f1dc64 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-293", "LLR-294", "TC-279", "TC-306", "TC-307"]
+++

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- LLR-293 authored in `docs/requirements/low-level-requirements.toml`
- LLR-294 authored in `docs/requirements/low-level-requirements.toml`
- TC-279 amended in `docs/test/test-cases.toml` (Inputs, MinWorkItems, Rubric, Trigger)
- TC-306 authored in `docs/test/test-cases.toml`
- TC-307 authored in `docs/test/test-cases.toml`

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.

## Dispositions

Verdict: `docs/reviews/wi-767-adjudicate-llr-293-llr-294/001-ADJUDICATE-30ee386.md`
(RETURN on all four rows). TC-279 was not shown. It stays Drafted for an
adjudication after WI-667 lands, and this draft does not cover it.

```toml
title = "Rework LLR-293, LLR-294, TC-306 and TC-307 so each row states only what its module does, and every clause is verified"
workstream = "process"
buildtier = "medium"
safety_class = "spine"
sr_refs = ["SR-215"]
priority = 2
```

These four rows stay Drafted. Rework them, then a fresh first-approval
adjudication rules on them.

- **LLR-293:** remove the two `intake.py rejudge --checkpoint ...` sentences.
  Commands are intake.py's behaviour (`_cmd_rejudge`, tagged LLR-255), and the
  release one restates LLR-255. Give the stage-gate entry one home: an
  amendment to LLR-255 through the amendment route, or a new intake.py LLR.
  Verify it with a case that claims that row: a new TC, not TC-248, which
  WI-766's successor is amending. Also close the gap that no gate-preparation
  surface names the stage-gate command, the way the release checklist's
  required item names the release one (LLR-255). If the lane concludes
  SR-215's "when a stage gate is checked" should narrow instead, raise it
  against WI-766's successor and do not edit SR-215 here.
- **LLR-294:** drop "Creation requires the numbered rubric first". Its one home
  is PROCESS.md "Observation judgement", and no code performs it. Keep the
  check_trajectory wiring clauses only if a case claiming LLR-294 verifies
  them.
- **TC-307:** cover LLR-294's check_trajectory wiring: the warnings print
  before the no-WI return and are never promoted under `--strict`. Either cite
  `tests/test_rejudge.py::test_trajectory_rubric_warning_survives_strict_and_no_work_items`
  in Evidence and Method, or move that clause to a sibling case.
- **TC-306:** make Expected agree with its Method and SR-215. An undeclared
  trigger keeps input-change firing under the floor, so "only the declared
  trigger fires" is wrong.

Out of scope: SR-215, LLR-254, TC-248 and the TC-036/055/209/210/211/247
cells (WI-766's successor), TC-279 (WI-667's adjudication), and any code
change beyond the stage-gate surface.
