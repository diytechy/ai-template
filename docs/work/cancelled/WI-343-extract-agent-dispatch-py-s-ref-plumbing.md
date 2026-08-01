+++
id = "WI-343"
title = "Extract agent_dispatch.py's ref plumbing (docs/dupes-allow: ref-namespace 5, ref-transaction 2, atomic-json 1, trailer-scan 1, reservation-release 3 = 12 sanctioned blocks). Four contracts are each stated at several sites in agent_dispatch.py: reading and writing a JSON metadata commit under a ref namespace (rev-parse -> log -1 --format=%B -> json.loads; commit-tree to write, across the conflict and blocked namespaces); the `git update-ref --stdin` prepare/commit transaction shared by reservation create and release, where only one of the two sites carries the comment explaining the bytes-not-text-mode rule that keeps Windows from writing \"start\\r\"; the write-temp-then-os.replace atomic JSON write; the trailer log scan; and release_reservations paired with its `release-failed` journal event, which today a site can omit. Triaged by READING the blocks under WI-340, not by their path relation. Extraction, not sanction, is the precedent here (WI-304)."
workstream = "scripts"
needs = ["WI-340"]
buildtier = "medium"
priority = 0
safety_class = "ordinary"
order = 340
+++

## Deliverable

RETIRED 2026-07-29, concurrency-restructure Phase 5 item 7 — MOOT, exactly as
the §6 fate table predicted: `agent_dispatch.py` was deleted whole at the Phase
5 item-1 commit, taking every block this row proposed to extract with it. The
census classes it names (`ref-namespace` 5, `ref-transaction` 2,
`reservation-release` 3, `trailer-scan` 1) dissolved in the same commit's
census re-derive; `atomic-json` had already been retired by WI-348. Nothing to
extract remains. Retired rather than closed: the work was never done — its
subject ceased to exist.
