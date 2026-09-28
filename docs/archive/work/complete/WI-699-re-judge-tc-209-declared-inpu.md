+++
id = "WI-699"
title = "re-judge TC-209: declared inputs changed [sha256:4fe5d49b9bef] at merge d79e039"
workstream = "process"
sr_refs = ["SR-184"]
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "rejudge"
adjudicates = ["TC-209"]
+++

## Deliverable

Re-judged at 8bebd4cf in the coordinator's hand lane (build/wi-698), `OUTCOME: RECORDED result=pass`. Verdict: `docs/reviews/wi-699-re-judge-tc-209-declared-inpu/`. Result record: `docs/test/observations/TC-209.2026-09-28T074512Z.toml`, written by the kit's observation writer.

## Context

The merge checkpoint at d79e039 found observation test case TC-209 due for re-judging.

- What changed: its declared inputs changed since its result TC-209.2026-09-28T070936Z.toml was judged: docs/test/inspection-procedures.md; SR-184.
- Method: Follow the Critique acceptance provenance inspection in docs/test/inspection-procedures.md#critique-acceptance-provenance-inspection; inspect a complete record, an abnormal record missing reviewer/rubric/intent/anchor, and a fully populated record whose rubric is copied from the verifying TC without independent SN/SR derivation.
- Expected: Complete independently derived provenance is accepted; each missing field or TC-copied rubric without independent SN/SR derivation is an Inspection finding; artifact quality remains Critique's judgment.
- Declared inputs: docs/test/inspection-procedures.md; SR-184
- Result lifetime: 90 days
- Latest result: TC-209.2026-09-28T070936Z.toml (pass, observed 2026-09-28T07:09:36Z, expires 2026-12-27T07:09:36Z)
- Inputs digest at d79e039: sha256:4fe5d49b9bef28a0b8bbff24f5a0b6c7c3873cecd2a22700428aaa6cf4d5d4c9

The check that filed this hashed the declared inputs and ran no model. Re-judge the case by its Method and record the result with `python scripts/record_observation.py --tc TC-209 --outcome pass|fail --by "<who or what observed>"`.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- TC-209 -> docs/test/inspection-procedures.md#critique-acceptance-provenance-inspection-result
