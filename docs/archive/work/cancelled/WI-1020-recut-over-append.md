+++
id = "WI-1020"
title = "The recipe that amends an accepted row by addition names the re-cut as the alternative when the row no longer fits"
workstream = "process"
sr_refs = ["SR-186"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 4
+++

## Deliverable

Cancelled on trunk before its scope critique (2026-11-21, the operator's
answer to queue-drill HANDOFF §3.3 N5). One case stood behind it, and
variant F's text migration (F-8) rewrites accepted LLR text at scale, so the
amendment rule belongs there: F-8 states when accepted text is rewritten in
place, when a row is re-cut under PROCESS.md §5, and amends the add-only
recipe line to match. The operator's separate point, that the recipes name a
model ("Terra") where they mean the authoring role, is filed as WI-1037.

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
