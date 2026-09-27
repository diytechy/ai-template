+++
id = "WI-653"
title = "Report an out-of-vocabulary stakeholder status once, on the integrity floor: amend LLR-216 and drop the frame-class report"
workstream = "scripts"
specref = ""
buildtier = "medium"
safety_class = "spine"
priority = 3
+++

## Deliverable

An out-of-vocabulary stakeholder status is now reported ONCE, in the
always-on integrity class (TC-215), under both `--strict-integrity` and
`--strict`. `frame_rules._stakeholder_row_findings` no longer checks status
vocabulary, and the `STATUS_VALUES` import it left unused is removed. A
MISSING status is still a frame failure through `STK_REQUIRED`.

- **Amendment (in place, status left Approved, for WI-664's joint
  adjudication):** LLR-216's `detail` drops its status clause and says that
  status vocabulary is schema, reported once by the integrity floor. TC-215
  needed no amendment: its method already names the integrity floor and
  asserts no frame finding.
- **Evidence:** `tests/test_stakeholders.py::test_a_status_outside_the_vocabulary_is_one_integrity_finding`
  was red first (`assert 2 == 1`: an integrity line and a frame line), then
  green. The builder's module run was `90 passed`.
- **Adopter note:** a RESYNC_PACK entry, "A stakeholder status outside the
  vocabulary is reported once, on the integrity floor".
- **Review:** codex Sol judged it SOUND with no findings
  (`docs/reviews/2026-09-26-wave3/sol-wi653.md`).

## Context

OI-93 ruled 2026-09-26: option (a). Approved TC-215 puts an out-of-vocabulary stakeholder status in the always-on integrity class and approved LLR-216 puts it in the frame class, so WI-628's build reports it twice under `--strict`. Keep the integrity report (status vocabulary is schema, judged the same way on every tier); draft LLR-216's amendment dropping its status clause (status left Approved) and remove the frame-class report in the same change. The ruling delegates the amendment to an amendment adjudication: file it, or add LLR-216 to the next one the queue holds.

## Done-when

- LLR-216 carries a drafted amendment without its status clause, and an adjudication for it is filed or joined.
- A test shows one finding, in the integrity class, for a stakeholder row with an out-of-vocabulary status.
- The commit bar and `trace.py --strict-integrity` pass.
