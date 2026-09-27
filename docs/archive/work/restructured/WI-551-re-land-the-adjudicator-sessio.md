+++
id = "WI-551"
title = "Retain adjudicator sessions through the session service's keep operation, inert at dial 0"
workstream = "process"
specref = "docs/archive/work/complete/WI-550-dispose-the-close-recorded-at.md"
needs = ["WI-579", "WI-580", "WI-620"]
buildtier = "strong"
priority = 3
safety_class = "ordinary"
supersedes = "WI-540"
+++

## Deliverable

Restructured into WI-620.

## Context

Drafted by WI-550 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

Rewritten on 2026-09-26 by the owner-approved backlog audit: the scope below
replaces the drafted re-land of the WI-540 patch.

The adjudicator's session retention is still wanted. OI-69 ruled it (a
retained transcript behind a context-percent dial, not a persistent actor), its
design is `docs/plans/2026-08-29-adjudicator-session-retention-plan.md` §2–§4,
and WI-541 verifies it on this machine before the dial is turned. What changed
is where it lands. The owner's S7 ruling makes one session service, WI-620, the
path for every model call: "S10's retention is a service operation, not a
per-role addition", and "the keep-warm ping is an ordinary recorded call, not a
direct `run_session` call"
(`docs/plans/2026-09-23-owner-notes-spine-sessions-and-tests.md` §3.1). The
control-window ruling adds that "the retained adjudicator patch is not applied
for the window" (`docs/ai-template-redesign-2026-09-05-codex/CONTROL-DECISION.md`).
So this row is WI-620's keep operation, for adjudicator sessions.

IN SCOPE, built on what WI-620 exposes:

- resume by session id through each provider's adapter, per route;
- occupancy after each adjudication, read from the latest request's prompt
  (WI-605), never from cumulative usage;
- drain at the dial and retire at a clear point, retire at once on an errored
  or timed-out session, and the other reset inputs the plan's §3.4 lists;
- keep-warm as an ordinary call through the service, recorded like any other;
- the `[adjudicator]` table in `docs/process.toml` and
  `project-trajectory/process.toml.template`, shipped at
  `context_reset_pct = 0`, where the whole layer is inert: no session id
  minted, no resume argument, and every adjudication a fresh session exactly as
  today.

Reference material, not a patch to apply:
`docs/work/handback/wi-540-adjudicator-retention-layer.patch`, the WI-540 lane's
build (about 90% complete and REVIEW-A-addressed) of the session store, the
per-family resume forms, the occupancy readers and their tests. Its spine
amendments were written against IF-174, which is burned; a seam this row
declares takes a fresh id.

The WI-540 lane's blocker, recorded as the DESIGN-CHECK gate failing, was
operational rather than a defect in the layer: the design-check route hit its
provider's usage limit, and the rework's full-suite runs were then lost to the
session's time cap until the stall guard closed the lane (`docs/log.md`, the
2026-08-31 sitting, run 6). WI-580's one-turn close bar addressed that stall,
so this row inherits no gate failure to reproduce.

NOT IN SCOPE: builder and reviewer retention (S10,
`docs/plans/2026-09-23-owner-notes-spine-sessions-and-tests.md` §3.4: builders
are a separately ruled experiment, reviewers never); verifying the layer on
this machine and turning the dial on (WI-541, then the owner).

Strong tier: it changes the session runtime every role shares.

## Done-when

- Adjudicator retention runs through the session service's keep operation:
  resume, occupancy, drain and reset, and keep-warm each go through the
  service's act and record steps, and no role or provider code launches or logs
  a retained session on its own (grep evidence).
- With `context_reset_pct = 0`, a test shows the layer inert: no session id
  minted, no resume argument, and the launch identical to a fresh session's.
- With the dial on, tests pin the reset rules (drain at the dial, retire at a
  clear point, retire at once on an errored session) and each provider's resume
  and occupancy parsing from recorded fixtures.
- A keep-warm ping appears in the session log like any other call.
- The `[adjudicator]` table ships at 0 in both `docs/process.toml` and the
  template, with matching structure, and the commit bar passes.
