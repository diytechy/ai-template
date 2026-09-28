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
Judged 2026-09-28 (`docs/reviews/wi-688-re-judge-tc-211-no-result-rec/001-ADJUDICATE-fe96ec6.md`, confirmed by Codex Sol): `OUTCOME: NEEDS-JUDGEMENT result=-`. Both of the Expected's clauses hold on the half of the sample that exists. The Method also reads the decomposition's SR-161 applicability or no-finding record, which LLR-183 states is not yet produced. The owed act is to ship the SR-161 producer, produce the record for this decomposition, re-run the procedure over the complete sample, and record. This row stays open so that the merge checkpoint does not re-mint it (wave-5 ruling 31). Folded (the adjudicator's finding, upheld by Sol): `docs/test/inspection-procedures.md` hand-restates earlier results inside a declared input, while `docs/test/observations/` is the one writer; a hand refresh of that prose stales the records it reports. Whoever re-runs this procedure replaces the result prose with a pointer to the observation records, and re-records the cases that file's change stales.

