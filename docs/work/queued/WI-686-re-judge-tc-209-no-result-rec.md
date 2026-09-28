+++
id = "WI-686"
title = "re-judge TC-209: no result recorded [sha256:3b7866818926] at merge 77fb093"
workstream = "process"
sr_refs = ["SR-184"]
specref = "docs/test/test-cases.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "rejudge"
adjudicates = ["TC-209"]
+++

## Context

The merge checkpoint at 77fb093 found observation test case TC-209 due for re-judging.

- What changed: no result has been recorded for it.
- Method: Follow the Critique acceptance provenance inspection in docs/test/inspection-procedures.md#critique-acceptance-provenance-inspection; inspect a complete record, an abnormal record missing reviewer/rubric/intent/anchor, and a fully populated record whose rubric is copied from the verifying TC without independent SN/SR derivation.
- Expected: Complete independently derived provenance is accepted; each missing field or TC-copied rubric without independent SN/SR derivation is an Inspection finding; artifact quality remains Critique's judgment.
- Declared inputs: docs/test/inspection-procedures.md; SR-184
- Result lifetime: 90 days
- Latest result: none
- Inputs digest at 77fb093: sha256:3b786681892687d3693a3e398aa8bb7f653acf2d36ed17214d35bee07b590c88

The check that filed this hashed the declared inputs and ran no model. Re-judge the case by its Method and record the result with `python scripts/record_observation.py --tc TC-209 --outcome pass|fail --by "<who or what observed>"`.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- TC-209 -> docs/test/inspection-procedures.md#critique-acceptance-provenance-inspection-result
