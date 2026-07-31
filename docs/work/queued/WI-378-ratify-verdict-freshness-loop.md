+++
id = "WI-378"
title = "Resolve the ratification/verdict-freshness loop: under gate-policy `autonomous` a reviewer's recorded verdict is what RATIFIES a re-attest window, but performing that ratification is a commit on a non-excluded path, so it immediately stales the verdict that authorized it and the queue refuses. Fired TWICE on WI-280 - the second time on a merge that altered no WI content at all - so the rounds a WI owes are bounded by trunk's commit rate, not its own risk. Three candidate shapes (document the ordering / widen the exclusion to bookkeeping + generated paths / forward-looking ratification) are compared with pros and cons in the spec."
workstream = "process"
specref = "docs/specs/WI-378.md"
buildtier = "medium"
safety_class = "ordinary"
+++
