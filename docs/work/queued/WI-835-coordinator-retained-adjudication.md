+++
id = "WI-835"
title = "The coordinator adjudicates through the retained session, the loop's keep operation, from a Claude Code session"
workstream = "process"
sr_refs = ["SR-227"]
specref = "docs/reviews/wi-834-plan/002-sol-plan-review-r2.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 9
+++

## Context

Split from WI-834 as its part A (owner, 2026-10-05). The owner wants this part
built first, by the coordinator in its Claude Code session, so that the rest
of WI-834 runs through the build process it creates: the coordinator's
adjudications go to one retained session instead of a fresh subagent each
time. The spec was reviewed with WI-834 (two Sol rounds,
`docs/reviews/wi-834-plan/`); the lines below are that review's part A, as
amended.

**The gap.** The coordinator starts each adjudication as a fresh Claude Code
subagent, which reloads the spine and the briefs from nothing every cycle. The
retention layer that avoids this, the session service's keep operation
(`session_keep`, SR-227, LLR-270, verified on this box at WI-541), is reachable
only from the loop's route (`agent_loop.adjudication_keep`), and this repo's
`[adjudicator] context_reset_pct` is 0. At the dial, a retained session drains
and retires at the next clear point (`session_keep._before_launch`).

**One path.** Under the owner's rule of 2026-10-03, the coordinator's
adjudication goes through the same keep operation and the same
`out/adjudicator/` record as the loop's. A Claude Code subagent resumed by
message would be a second retention mechanism, outside the kit's keep
planning, dedicated-home overlay and bookkeeping. Independence stands: the
retained adjudicator never judges what its own session authored (Terra
authors, Opus judges), and OI-69 (b1) keeps `reset_on_same_artifact = false`.

**The sign-in.** With retention on, both routes' retained Claude sessions run
under the dedicated CLI home (OI-69 (e1)), which needs its own sign-in. The
owner signed in there on 2026-10-05; `claude auth status` under the home
reports `loggedIn: true`. A launch that needs the sign-in and finds none never
falls back to a fresh session (the owner's rule of 2026-10-03). It is refused,
naming dev-setup, where WI-834 part C offers the sign-in.

**Relation to S788.** WI-801 makes `ask` the only launcher for the loop and
the coordinator alike. This row's entry point is temporary: WI-801 deletes it
and moves its callers and tests to `ask`'s adjudicate kind. WI-802's "this
repo stays at 0" changes to the value set here.

**Owner rulings carried from WI-834 (2026-10-05):** (b) this repo's
`context_reset_pct` is 55; (e) OI-69 (e1) stands.

## Done-when

- The coordinator runs an adjudication through one entry point that composes
  an adjudication request and calls the session service's keep operation. The
  request carries:
  - the brief class;
  - the family and route;
  - the work item;
  - the governing template identity;
  - a lease duration tied to the call's deadline.
  The loop's composition of that request (`agent_loop.adjudication_keep`) is
  extracted once, and both routes use it. The entry point writes the session
  log, prints the verdict and uses the same `out/adjudicator/` record as the
  loop.
- No Claude Code subagent adjudicates. The `session-protocol` skill and the
  coordinator recipe direct the coordinator to this entry point. WI-801's
  Done-when gains the line deleting it and moving its callers and tests to
  `ask`.
- One sign-in probe reports the dedicated home as signed in, missing or
  unknown, using `claude auth status` under that home with no model call, and
  resolving the home without creating it. WI-834 part C's dev-setup report
  reuses this probe.
- On either route, a launch whose keep needs the sign-in is refused, naming
  dev-setup, when the probe reports missing or unknown. It never starts an
  automatic sign-in or falls back to a fresh session.
- Tests:
  - a second adjudication on the coordinator route resumes the first one's
    session;
  - a session at `context_reset_pct` drains and retires at the next clear
    point;
  - the loop's route composes the same request as before the extraction;
  - signed in, missing and unknown are each reported, and missing and unknown
    each refuse the launch.
- The sign-in is confirmed through the probe. Then this repo's
  `[adjudicator] context_reset_pct` is set to 55, and WI-802's "this repo
  stays at 0" line is amended in the same commit.
- Spine rows: SR-227 and LLR-270 state the coordinator route and the sign-in
  refusal, and an IF declares the entry point and the probe, with TCs. Terra
  authors these rows, and each passes the in-lane adjudication.
- The row's test bar: its affected modules' tests plus the smoke tier.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit. The coordinator entry
  point and the sign-in refusal are visible once retention is enabled.
