+++
id = "WI-1020"
title = "The recipe that amends an accepted row by addition names the re-cut as the alternative when the row no longer fits"
workstream = "process"
sr_refs = ["SR-186"]
specref = "docs/archive/work/complete/WI-1017-llrs-yield-to-design.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 4
+++

## Context

Filed on trunk at WI-1017's landing (2026-11-21), from the evidence sample
in its Deliverable ("Causes outside the guidance", row 3). One case in the
sample (wi-977's finding 008 F6: LLR-149 repeats a sentence), so the
operator may cancel this row.

The coordinator's recipe "Brief Terra to amend an accepted row by addition"
guards against lost obligations, and it makes accepted rows grow where a
re-cut would retire and mint. PROCESS.md §5's design replacement (WI-1017)
now says when a row is re-cut instead.

## Done-when

- [ ] The recipe points at PROCESS.md §5's design replacement as the
      alternative to appending when the row no longer fits the design, and
      keeps addition as the route when it does.
