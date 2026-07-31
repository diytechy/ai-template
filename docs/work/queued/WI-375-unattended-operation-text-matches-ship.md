+++
id = "WI-375"
title = "Make PROCESS_OPTIONS' \"Unattended operation (walk-away runs)\" describe the flow that actually ships. Two defects today: (1) the section (:542) promises \"a coordinator grinds work from a single entry point while nobody watches\" while that entry point exits 2 with a map, and it describes the model in terms of `integrate.py claim` and `agent_loop.py --wi` as steps without naming what invokes them; (2) the capability table (:29) cites `docs/run-*` as a live mechanism and that artifact does not exist - `ls docs/run-*` returns No such file or directory, it was deleted with the dispatcher at Phase 5. This is shipped kit text every adopter reads to decide whether to wire up walk-away runs. Hard-gated behind WI-374 because the section must describe the flow that exists - but NOTE defect (2) is wrong regardless: if WI-374 stalls or is re-scoped, split that half out and fix it alone. Includes searching for any OTHER kit text still promising the retired dispatcher's behaviour, rather than assuming these two sites are all of them."
workstream = "docs"
specref = "docs/specs/unattended-entry-point.md#s2--make-the-process-text-true-again"
buildtier = "quick"
priority = 3
safety_class = "ordinary"
needs = ["WI-374"]
+++
