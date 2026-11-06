+++
id = "WI-1001"
title = "An approved automated test case with no tagged test is a strict finding, so an approved chain cannot stand undelivered with every bar green"
workstream = "process"
sr_refs = ["SR-157"]
specref = "docs/specs/WI-1001.md"
needs = ["WI-997"]
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Context

Filed by hand on 2026-11-05 (attended), routed by OI-127's ruling. See the
spec of record for why. It needs WI-997, because with no tags every TC would
read as untested. Owes its scope critique before its claim, which settles
two things: how a case whose evidence names a debt row reads (TC-165 and
TC-166 until WI-1000 and WI-999 close), and how a lane's test-first window
reads, where a case is approved before its test exists.

## Done-when

- [ ] An Approved TC with `automated = "Yes"` and no test declaring it is a
      WARN, and an ERROR under `--strict`.
- [ ] It lands green on trunk: 0 findings, each exception named in the row.
- [ ] Regressions name each arm.
- [ ] RESYNC entry, if the finding reaches adopters.
- [ ] Review bar: A+B (REVIEW-A plus an independent REVIEW-B).
