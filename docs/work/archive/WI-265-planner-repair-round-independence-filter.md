+++
id = "WI-265"
title = "Planner repair-round independence filter (owner ruling 2026-07-21, repo-review-2026-07-21 L-28 remaining design question): the mechanical-repair prompt filters the coverage report to the implicated plans OWN FAIL lines - the rival plans coverage diff never enters a planners context (anchoring biases the build toward convergence, defeating two-planner independence at the cheapest gaming point). Rides with the already-applied L-28 mechanical fixes (stale exit-2 report ignore); test: repair prompt for plan A contains no plan-B diff content"
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
order = 262
+++

## Deliverable

plan_runner mechanical-repair prompt filtered to the implicated plan own FAIL lines via _repair_critique (empty own-fails -> generic instruction, never the rival coverage diff); full coverage_report reaches only critic/arbiter hats. Adversarial REVIEW-A APPROVE f=1 (MINOR pre-existing/unreachable substring match, deferred).
