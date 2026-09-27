+++
id = "WI-653"
title = "Report an out-of-vocabulary stakeholder status once, on the integrity floor: amend LLR-216 and drop the frame-class report"
workstream = "scripts"
specref = "docs/log.d/2026-09-26-owner-rulings-oi82-oi94.md"
buildtier = "medium"
safety_class = "spine"
priority = 3
+++

## Context

OI-93 ruled 2026-09-26: option (a). Approved TC-215 puts an out-of-vocabulary stakeholder status in the always-on integrity class and approved LLR-216 puts it in the frame class, so WI-628's build reports it twice under `--strict`. Keep the integrity report (status vocabulary is schema, judged the same way on every tier); draft LLR-216's amendment dropping its status clause (status left Approved) and remove the frame-class report in the same change. The ruling delegates the amendment to an amendment adjudication: file it, or add LLR-216 to the next one the queue holds.

## Done-when

- LLR-216 carries a drafted amendment without its status clause, and an adjudication for it is filed or joined.
- A test shows one finding, in the integrity class, for a stakeholder row with an out-of-vocabulary status.
- The commit bar and `trace.py --strict-integrity` pass.
