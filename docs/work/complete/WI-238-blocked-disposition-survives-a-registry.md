+++
id = "WI-238"
title = "blocked_disposition survives a registry without a BlockRef column - extend the schema in-transaction or fail loudly (2026-07-19 field finding)"
workstream = "unattended"
sr_refs = ["SR-097"]
buildtier = "medium"
safety_class = "high-risk"
order = 235
+++

## Deliverable

_rewrite_wi_rows now ADOPTS an absent updated column (the WI-229 registry-extension precedent): appends it to the header + writes the value on the target row via extracted _wanted_columns/_load_registry_rows helpers; untouched rows stay byte-identical under the file's OWN dominant line ending (raw csv read preserves quoted multi-line cells; ragged legacy rows read the new column as empty via DictReader) and an unreadable/headerless registry fails loudly naming the column so blocked_disposition resets with no commit (log-append extracted to _append_blocked_log to hold the C901 budget). 7 unit/integration regressions in test_agent_loop_integrate.py; work-items.template.csv already carried BlockRef so no scaffold change.
