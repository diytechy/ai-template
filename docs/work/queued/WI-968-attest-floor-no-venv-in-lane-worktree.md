+++
id = "WI-968"
title = "attest's harness floor finds no .venv in a linked lane worktree, so no lane can take its review attestation"
workstream = "process"
sr_refs = []
specref = "docs/specs/WI-968.md"
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Context

The defect and its Trust section: [the spec of record](../../specs/WI-968.md).

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
