+++
id = "WI-167"
title = "Tripwire path coverage - REVIEW_POLICY_PATHS misses the meta-repo kit-script layout (project-trajectory/scripts/)"
workstream = "unattended"
needs = ["WI-059"]
buildtier = "medium"
order = 166
+++

## Deliverable

Extended REVIEW_POLICY_PATHS with the project-trajectory/scripts/ variants of score_reviews.py + agent_route.py (kept the downstream scripts/ entries) so the implementer-touched-review tripwire fires when an implementer edits a routing referee in this meta-repo's own kit-script home, not only the downstream scaffolded layout; regression test covers both layouts, Windows separators, and a non-referee sibling negative. Expected by-design side effect (076-DESIGN-CHECK): this commit touches a now-listed path, so its own review round fires the tripwire once.
