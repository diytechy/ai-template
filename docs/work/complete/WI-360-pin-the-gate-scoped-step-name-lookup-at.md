+++
id = "WI-360"
title = "Pin the gate-scoped step-name lookup at an explicit LOW gate: WI-355's REVIEW-A verified 'format is findable at any gate' by probe but the suite asserts it only at gate=all, so a refactor making check.py steps() filter its returned table would break the documented behaviour with the suite green. One assertion at G1 closes it (docs/reviews/WI-355-REVIEW-A.md MINOR 2)."
workstream = "scripts"
buildtier = "medium"
priority = 2
safety_class = "ordinary"
+++

## Deliverable

DONE 2026-07-29. The G1 findability assertion for the `format` step sits next to the gate=all one in tests/test_check_harness.py::test_step_gate_honours_an_explicit_gate — a forward regression pin (nothing was broken), closing WI-355 REVIEW-A MINOR 2.
