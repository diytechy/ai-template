+++
id = "WI-617"
title = "Run the OI-37 absolutes sweep over the needs, then the SRs, and route the rewrites for approval (S1)"
workstream = "requirements"
needs = ["WI-616"]
specref = "docs/requirements/open-items.toml#OI-37"
buildtier = "strong"
priority = 2
safety_class = "spine"
+++

## Context

OI-37's ruling (2026-08-18): "An absolute in a need is a promise every child
must keep under every condition ... Read the needs for unwarranted absolutes as
a class." SN-006 was rewritten; the class-wide sweep never followed. The
sister plan's S1 (2026-09-23) asks for it as its own item, needs first, using
the extended check's output.

Classify each absolute: over a closed domain the system controls it is fine;
over the open world or open time it is bounded, or carried as an assumption
row once the assumption tier exists; a prohibited mechanism in a need is a
design decision to move down a tier. Needs are held for the owner
(`human_approval_through = "DevStg-Needs"`), so the sweep proposes rewrites as
Drafted amendments and approves nothing.

## Done-when

- Every absolute the check reports in a need is classified with a one-line
  reason, and then every one in an SR.
- Rewrites land as amendments for the approval route (needs to the owner's
  brief, SRs to the adjudicator); none is approved in the lane.
- Open-world absolutes that are really assumptions are listed for the
  assumption tier's C2, not written into it.
