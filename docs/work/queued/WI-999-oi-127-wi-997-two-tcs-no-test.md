+++
id = "WI-999"
title = "OI-127's ruling: how the tag migration proceeds past two test cases with no test"
workstream = "process"
sr_refs = ["SR-157"]
specref = "docs/requirements/open-items.toml"
needs = ["OI-127"]
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Context

Filed by hand in headless leg 33 (2026-11-04) with OI-127, as the queued
placeholder row a pending open item is filed with (OI-102): it carries the
owner's decision to the queue. The tag-migration row's Done-when stops the row
where no test verifies a case, and its planner found two such cases (OI-127
states the evidence and the options; coordinator-2026-11-04 D-007).

## Done-when

- [ ] The owner rules OI-127, and the ruling commit replaces this list with
      the work the ruling routes (OI-102): for option (a), the partial close
      and its disposition; for (b), the two cases filed as their own rows and
      the stale-part item amended; for (c), the preparatory rows. This row
      closes citing the ruling, or becomes the routed work.
