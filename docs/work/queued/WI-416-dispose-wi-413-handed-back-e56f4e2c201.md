+++
id = "WI-416"
title = "dispose: WI-413 handed back (e56f4e2c201a) - cancel / defer / re-queue with drafted follow-up / surface an open item (a disposition row never hands back; R3)"
workstream = "process"
specref = "docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md"
buildtier = "strong"
safety_class = "adjudication"
+++

## Context

The handed-back spec is `docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md`; its `## Handback` section says:

> Returned unfinished from lane `wi-413-bare-sweep-dedup-token`: NEEDS-HUMAN: a correct fix needs a return-event identity PERSISTED AT HANDBA…

Outcomes (R3): cancel / defer / re-queue with drafted follow-up / surface an open item. Clearing its blockref re-queues it; moving it to cancelled/ (reason in the Deliverable) cancels it; a drafted follow-up goes in THIS row's ## Dispositions section; an open item goes to docs/requirements/open-items.csv.
