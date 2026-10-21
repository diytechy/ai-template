+++
id = "WI-968"
title = "attest's harness floor finds no .venv in a linked lane worktree, so no lane can take its review attestation"
workstream = "process"
sr_refs = []
specref = ""
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Deliverable

Cancelled in headless leg 08 (2026-10-21) before its claim: its premise was
the coordinator's wrong route, not a defect (wi-957 D-007). `integrate.py
attest` takes the primary checkout as `--root` and finds the lane by
`--branch`, running the review bar in the lane under the primary
checkout's interpreter; run from the lane with the default root, its floor
read the lane's own root. Run as designed, it attested WI-957's tip. Its
scope critique's round 1 (CHANGES-REQUESTED) and the drafter's reading are
kept under the leg's scratch root; the drafter's separate finding (the
bookkeeping and lane harness reads have no floor) is in status.md's
unfiled follow-ups. The route is now in the coordinator-cycle recipes.

## Context

The defect and its Trust section: [the spec of record](../../specs/WI-968.2026-10-21.md).

## Done-when

Each named test fails on the code before the change.

- In a real linked worktree (`git worktree add`) of a repository that
  declares the pinned toolchain and whose primary checkout holds a
  floor-satisfying `.venv`, `integrate.py attest --bar review` runs its bar
  under that interpreter and writes its attestation.
- The same worktree with no floor-satisfying `.venv` at the primary
  checkout refuses naming the floor, as today, and never runs under the
  ambient interpreter.
- A primary checkout's own lookup is unchanged.
- The coordinator-cycle recipes' attest bullet says how a lane attests.
