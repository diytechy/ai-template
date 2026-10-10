+++
id = "WI-893"
title = "A hand merge on trunk judges the commits it brings in, as OI-113 rules"
workstream = "process"
sr_refs = ["SR-140"]
specref = "docs/requirements/open-items.toml#OI-113"
needs = ["OI-113", "WI-892"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by the coordinator on 2026-10-10 as WI-828's successor and the queued
placeholder that puts OI-113 on the owner's surface: an open item is filed
together with the queued row that cites it. WI-828 closed partial after its
first build round found that walking HEAD..MERGE_HEAD refuses every station
refresh (trunk's squash landings carry text and act in one commit by
design), and that nothing declares the trunk the walk would need to skip.
WI-828's spec, Trust table and the parked round-1 diff
(C:/Projects/ai-template.wt/wi-828-round1-parked.patch, outside the
repository) are the starting point.

The ruling of OI-113 writes this row's Done-when and Trust section in the
same commit, as the rule for citing rows requires.
