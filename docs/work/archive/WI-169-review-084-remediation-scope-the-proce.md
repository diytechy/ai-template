+++
id = "WI-169"
title = "Review 084 remediation - scope the Process-tab loop box/arrow CSS to the wrapper div.loop (kill the nested double racetrack) + de-tautologize the TC-056 degree assertion"
workstream = "dashboard"
sr_refs = ["SR-055"]
needs = ["WI-165"]
buildtier = "strong"
order = 168
+++

## Deliverable

Scoped the default and responsive racetrack/return-arrow CSS to wrapper div.loop elements so nested ol.loop stage lists cannot draw a second track; removed self-declared degree attributes; hardened TC-056 and its tests around the actual shared-entry grid span and wrapper-only border/arrow structure; regenerated OKF and trajectory outputs.
