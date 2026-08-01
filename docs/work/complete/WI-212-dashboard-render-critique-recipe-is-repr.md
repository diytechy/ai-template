+++
id = "WI-212"
title = "Dashboard render-critique recipe is reproducible and captures the true landing fold"
workstream = "tooling"
needs = ["WI-189"]
buildtier = "quick"
order = 211
+++

## Deliverable

Added the pinned npm lockfile required by the documented npm ci setup; moved the landing-fold screenshot ahead of tab clicks so Playwright cannot scroll the narrow page before capturing the viewport; regenerated all 36 declared screenshots.
