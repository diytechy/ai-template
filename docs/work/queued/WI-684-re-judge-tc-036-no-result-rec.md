+++
id = "WI-684"
title = "re-judge TC-036: no result recorded [sha256:2f2f30dfba87] at merge 77fb093"
workstream = "process"
sr_refs = ["SR-036"]
specref = "docs/test/test-cases.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "rejudge"
adjudicates = ["TC-036"]
+++

## Context

The merge checkpoint at 77fb093 found observation test case TC-036 due for re-judging.

- What changed: no result has been recorded for it.
- Method: Inspect a re-sync done per ADOPTING.md section 6 against the docs/kit-version diff — kit-owned taken wholesale, generated docs regenerated, filled-in files preserved. Process doc + downstream-resync skill; no automated test.
- Expected: Satisfies SR-036 AcceptanceCriteria
- Declared inputs: project-trajectory/ADOPTING.md; project-trajectory/skills/downstream-resync/SKILL.md; SR-036
- Result lifetime: 90 days
- Latest result: none
- Inputs digest at 77fb093: sha256:2f2f30dfba872273c9250558dcde22783dad0a144e4d94e761ca0124f200e336

The check that filed this hashed the declared inputs and ran no model. Re-judge the case by its Method and record the result with `python scripts/record_observation.py --tc TC-036 --outcome pass|fail --by "<who or what observed>"`.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- TC-036 -> project-trajectory/ADOPTING.md
