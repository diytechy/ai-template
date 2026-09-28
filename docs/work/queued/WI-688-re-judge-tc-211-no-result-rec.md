+++
id = "WI-688"
title = "re-judge TC-211: no result recorded [sha256:aa064ee9542c] at merge 77fb093"
workstream = "process"
sr_refs = ["SR-186"]
specref = "docs/test/test-cases.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "rejudge"
adjudicates = ["TC-211"]
+++

## Context

The merge checkpoint at 77fb093 found observation test case TC-211 due for re-judging.

- What changed: no result has been recorded for it.
- Method: Follow the decomposition proportionality inspection in docs/test/inspection-procedures.md#decomposition-proportionality-inspection; inspect the complete chain and an extra paraphrasing child.
- Expected: A child within a required tier with no independent decision or verification purpose is an Inspection finding; otherwise the review records that independent value and why further splitting stops.
- Declared inputs: docs/test/inspection-procedures.md; SR-186
- Result lifetime: 90 days
- Latest result: none
- Inputs digest at 77fb093: sha256:aa064ee9542c8e0a739956123890095f8f44aa74e05f96bcc41f96c70c2ca7fb

The check that filed this hashed the declared inputs and ran no model. Re-judge the case by its Method and record the result with `python scripts/record_observation.py --tc TC-211 --outcome pass|fail --by "<who or what observed>"`.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- TC-211 -> docs/test/inspection-procedures.md#decomposition-proportionality-inspection-result
