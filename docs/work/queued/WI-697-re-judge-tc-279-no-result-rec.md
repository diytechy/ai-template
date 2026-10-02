+++
id = "WI-697"
title = "re-judge TC-279: no result recorded [sha256:cf0861ee8f1d] at merge bcf1e9a"
workstream = "process"
specref = "docs/test/test-cases.toml"
buildtier = "medium"
safety_class = "adjudication"
needs = ["WI-667"]
brief = "rejudge"
adjudicates = ["TC-279"]
+++

## Context

The merge checkpoint at bcf1e9a found observation test case TC-279 due for re-judging.

- What changed: no result has been recorded for it.
- Method: Follow the sampled new-reader inspection in docs/test/inspection-procedures.md#sampled-new-reader-inspection: draw the declared number of parts at random from the source the project's readability and structure measures cover, give each to a reader who has not worked on it, and have that reader say, from the part's code and the records linked to it and without asking its author, what the part does and why it exists; record each statement beside the part's linked requirement and design rows.
- Expected: Each sampled reader states what the part does and why it exists, in agreement with the part's linked rows; a reader who cannot, or whose statement contradicts those rows, is a failing sample and falsification evidence against DA-011
- Declared inputs: docs/test/inspection-procedures.md; DA-011; project-trajectory/scripts; docs/requirements/system-requirements.toml; docs/requirements/low-level-requirements.toml
- Result lifetime: 90 days
- Latest result: none
- Inputs digest at bcf1e9a: sha256:cf0861ee8f1dfb8f0fbd5c026dfdbb1e60894baf9006c2319fabeffbd17ea9a2

The check that filed this hashed the declared inputs and ran no model. Re-judge the case by its Method and record the result with `python scripts/record_observation.py --tc TC-279 --outcome pass|fail --by "<who or what observed>"`.
Held 2026-09-28 by the kit itself: `adjudicate_brief.compose` refuses this row's re-judge brief ("TC-279 has no `Verifies` cell"). TC-279 is an assumption-only observation case: it evidences DA-011 and verifies no SR or LLR. A brief that cannot be composed is a hold for a human, never a downgrade to an ordinary session (the module's rule 3). The composer gap is folded into WI-667. This row waits there, and closing it now would let the next merge re-mint it.


## Owner position 2026-09-30 (open; not yet a ruling)

The owner recalls earlier discussion and doubts that an assumption can be
*verified*: it can only be *asserted*, and its Status is the likely right
record, following the other spine registries. If that holds, TC-279 (an
observation case that "verifies" DA-011) is mis-modelled, and the fix is to the
model, not a composer arm. Decide this before WI-667's first Done-when is built.

Proposed ruling 2026-10-02: see WI-667's "Proposed ruling". Under it TC-279 stays
as a falsification check only (a failing sample is evidence against DA-011; a
passing one proves nothing), and this re-judge still waits on WI-667's narrowed
first Done-when.
