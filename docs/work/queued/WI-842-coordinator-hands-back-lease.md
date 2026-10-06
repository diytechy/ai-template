+++
id = "WI-842"
title = "A closing coordinator hands its lease back, so the next session takes it without the owner's release"
workstream = "process"
sr_refs = ["SR-229"]
specref = "docs/archive/specs/WI-822.2026-10-05.md"
buildtier = "quick"
safety_class = "ordinary"
priority = 9
+++

## Context

Filed by hand by the wave-18 coordinator on 2026-10-06, at the owner's
question. The coordinator lease passes in exactly two ways (WI-822, LLR-300): to
a relaunched successor at its `SessionStart`, or by the owner's recorded
release. The session-protocol skill's close-out requests the relaunch only when
the drain latch fires. A coordinator that closes out before that writes its
handoff and stops. The owner then pastes the handoff's session prompt into a new
session, so no relaunch runs, and the next session's take is refused until the
owner runs `release`.
That happened at the starts of waves 17 and 18. The owner does not want to give
this step attention in every cycle.

SR-229's rationale keeps the owner's release for a lease "whose holder has
gone". A holder that closes out has not gone: it can hand the lease back
itself, as a recorded event, which leaves the integrity argument intact.

## Done-when

- `coordinator_guard.py` gains a holder's hand-back. Only the current holder
  (by session id) may run it. It frees the lease and records a `handback` event
  naming the handoff it closed with, which must carry a session prompt, as
  `request-relaunch` requires. Any other caller is refused and told the owner
  releases.
- A latched drain does not block the hand-back; the hand-back clears it with
  the lease, as a successor's take does.
- The coordinator's close-out step (the session-protocol skill, source then
  mirrors via `bootstrap.py --sync`) runs the hand-back as its last act after
  writing the handoff, unless it requested a relaunch.
- Tests: the holder's hand-back frees the lease and the next take succeeds;
  another session's hand-back, and one naming a handoff with no session
  prompt, are refused and leave the lease unchanged; a drained holder can hand
  back. Dial 0 still writes nothing.
- SR-229's rows (LLR-300 and its TCs) state the hand-back and pass adjudication
  on the one adjudication path.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit.
