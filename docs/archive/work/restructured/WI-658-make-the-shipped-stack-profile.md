+++
id = "WI-658"
title = "Make the shipped stack profile's generated-artifact list match what the regeneration writes"
workstream = "scripts"
specref = "project-trajectory/stack.ini.template"
buildtier = "medium"
safety_class = "ordinary"
priority = 4
+++

## Deliverable

Restructured into WI-656.

## Context

The shipped `stack.ini.template` `[generated]` section declares three
artifacts (`PROJECT_STATE.html`, `docs/okf/`, the status block), while
`trunk_step.REGEN_STEPS` names the writes of every regeneration step (the
open-items view, the stage cache, the derived components, the CLI and
interface references, the approval brief, the verdict rollup, and more).
`integrate._abandoned_claim` and `audit` still read the `[generated]` list, so
an adopter's list decides what those treat as generated, and it lags.

This repository's own `docs/stack.ini` declares a longer list by hand, which
is why the lag shows downstream first.

IN SCOPE: decide one home for "what is generated" (derive the readers from
the regeneration steps' declared writes, or ship a template list a test holds
equal to them) and make the readers use it. Say in the resync pack what an
adopter's hand-kept list becomes.

## Done-when

- A test fails when a regeneration step writes a path the generated set
  omits, or the reverse.
- `integrate._abandoned_claim` and `audit` read the one home.
- A resync-pack entry names what an adopter must do, and the commit bar passes.
