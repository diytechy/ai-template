+++
id = "WI-378"
title = "Resolve the ratification/verdict-freshness loop: under gate-policy `autonomous` a reviewer's recorded verdict is what RATIFIES a re-attest window, but performing that ratification is a commit on a non-excluded path, so it immediately stales the verdict that authorized it and the queue refuses. Fired TWICE on WI-280 - the second time on a merge that altered no WI content at all - so the rounds a WI owes are bounded by trunk's commit rate, not its own risk. REFRAMED 2026-07-31 by owner direction and now DEPENDS on the concurrency-v2 design: with spine WIs serialised (WI-381) and the amendment detector corrected to ignore traced-not-ratified cells (WI-380), firing 2 cannot happen and most windows never open, so the option that would have weakened the fail-closed gate drops out entirely. What remains is the ordering documentation, which was always free - and possibly nothing else. Do not build before WI-380; measure what still fires first. The considered-and-set-aside options are kept in the spec as the record."
workstream = "process"
specref = "docs/specs/WI-378.md"
buildtier = "medium"
safety_class = "ordinary"
+++
