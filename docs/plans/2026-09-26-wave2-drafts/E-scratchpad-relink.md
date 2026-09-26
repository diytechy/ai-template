+++
id = "WI-@E@"
title = "Keep a claim's relink from rewriting the owner's scratchpad, so a dirty scratchpad stops refusing the claim"
workstream = "unattended"
specref = "project-trajectory/scripts/integrate.py"
buildtier = "medium"
safety_class = "ordinary"
priority = 4
+++

## Context

The claim relinks references to the spec it moves from `queued/` to
`active/`. That rewrite can reach the owner's scratchpad, which the
bookkeeping helper refuses to write over when dirty, so an owner whose
uncommitted notes name the id has the claim refused by name. The owner's
scratchpad is owner-only: no kit step should rewrite it at all.

IN SCOPE: exclude the owner-only paths (`OWNER_ONLY_PATHS`) from the relink's
rewrite set, test it, and state in the claim's contract that the owner's
notes are never rewritten.

## Done-when

- A test with a dirty owner scratchpad naming the claimed id shows the claim
  succeeds and leaves the scratchpad byte-identical.
- The commit bar passes.
