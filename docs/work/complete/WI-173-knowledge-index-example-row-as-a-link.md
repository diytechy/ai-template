+++
id = "WI-173"
title = "Knowledge index example row as a link - the scaffolded pack index's example row labels the pack with a code-span so a copied row leaves the pack an orphan for check_docs; render the example Label as a markdown link (093-REVIEW-A MINOR)"
workstream = "scripts"
needs = ["WI-152"]
buildtier = "quick"
order = 172
+++

## Deliverable

Changed the scaffolded pack-index example label from a code span to [`example`](README.md), a valid self-link whose row instructs replacing both label and target with the pack file; this demonstrates the reachable-pack pattern while keeping a fresh scaffold free of a fake pack and broken links. Bootstrap contract test pins the linked example.
