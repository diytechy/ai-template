+++
id = "WI-700"
title = "re-judge TC-210: declared inputs changed [sha256:2eb6379200f0] at merge d79e039"
workstream = "process"
sr_refs = ["SR-185"]
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "rejudge"
adjudicates = ["TC-210"]
+++

## Deliverable

Re-judged at 8bebd4cf in the coordinator's hand lane (build/wi-698), `OUTCOME: RECORDED result=pass`. Verdict: `docs/reviews/wi-700-re-judge-tc-210-declared-inpu/`. Result record: `docs/test/observations/TC-210.2026-09-28T074513Z.toml`, written by the kit's observation writer.

## Context

The merge checkpoint at d79e039 found observation test case TC-210 due for re-judging.

- What changed: its declared inputs changed since its result TC-210.2026-09-28T071102Z.toml was judged: docs/test/inspection-procedures.md; SR-185.
- Method: Follow the requirement and interface counterpart review inspection in docs/test/inspection-procedures.md#requirement-and-interface-counterpart-review-inspection; inspect a semantic change record and an abnormal reference-existence-only record.
- Expected: The counterpart decision is explicit; reference-existence evidence alone is found insufficient.
- Declared inputs: docs/test/inspection-procedures.md; SR-185
- Result lifetime: 90 days
- Latest result: TC-210.2026-09-28T071102Z.toml (pass, observed 2026-09-28T07:11:02Z, expires 2026-12-27T07:11:02Z)
- Inputs digest at d79e039: sha256:2eb6379200f0c2cf6ef3088d68f9ba0727a8706f52994863a2666dc43caa3199

The check that filed this hashed the declared inputs and ran no model. Re-judge the case by its Method and record the result with `python scripts/record_observation.py --tc TC-210 --outcome pass|fail --by "<who or what observed>"`.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- TC-210 -> docs/test/inspection-procedures.md#requirement-and-interface-counterpart-review-inspection-result
