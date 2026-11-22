+++
id = "WI-1038"
title = "TC-428 and TC-429 verify LLR-395 once it is accepted, in place of SR-157"
workstream = "process"
sr_refs = ["SR-157"]
needs = ["WI-1019"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 3
planmode = "none"
+++

## Deliverable

Cancelled on trunk (2026-11-22), superseded by WI-1048. The first automated
adjudication sitting (WI-1047) returned LLR-395 for having no test case, and
the parent-first rule refused this row's re-pointing of the accepted TC-428
and TC-429 at a `Drafted` LLR: a circle. WI-1048 broke it with TC-475, a
`Drafted` test case verifying LLR-395 over the same tests (each now tagged
TC-475) plus the failing-declared-test clause, so LLR-395 and TC-475 are
accepted together. Re-pointing TC-428 and TC-429 afterwards would only give
LLR-395 three cases on the same tests.

## Context

Filed on trunk on 2026-11-21 by the queue-drill coordinator, from WI-1019's
build. WI-1019 mints LLR-395 (`Drafted`, under SR-157) to state WI-1001's
rule that an accepted automated test case no test file declares is a
finding. Its scope critique asked that TC-428 and TC-429 verify LLR-395 in
place of SR-157. The builder found that the parent-first rule (SR-245 and
LLR-357 at the trace, SR-246 and LLR-358 at the commit) refuses an
`Accepted` test case verifying a `Drafted` LLR, so WI-1019 lands the row and
leaves the two test cases as they are.

This row waits for LLR-395's first acceptance, which the dial releases to
automated adjudication. It is claimable only once LLR-395 reads `Accepted`;
before that, the edit is refused by the checks, so there is nothing to
build.

## Done-when

- [ ] LLR-395 reads `Accepted` at the claim; if it does not, the row is not
      claimed.
- [ ] TC-428 and TC-429 name LLR-395 in place of SR-157 in their `verifies`
      cell (IF-263 kept), changing no other cell, and `trace.py --strict`
      stays clean.
- [ ] The Deliverable lists the drift on TC-428 and TC-429 for automated
      adjudication.
