## 2026-09-07 — Supervisor review of the stopped approval control, and the resume prompt

Read-only review of `0f106ce9`, the stopped segment `b830f202`..`79115aab` and
the stop `70a17cab`, against live source. Both recorded findings were
re-derived independently and accepted: the short-sha candidate against
`primary_approval._HEX40`, and the empty `kind` a `dual` draft with no declared
`safety_class` yields, which keeps `adjudication_review_owed` from ever seeing
`high-risk`.

Four findings added in
[the review](../reviews/2026-09-07-control-approval-supervisor-review.md):

1. **Proportionality.** 8,298 is gross insertions. Scripts `+2828 -1016`, tests
   `+2529 -812`, docs/prompts/registries `+2941 -226`, with 716 lines removed
   from `handback`/`integrate`/`kitlib.verdict`. Roughly 1,100 lines of new
   machinery. Adjudication was not previously working on trunk: `handback._lane`
   refused a primary checkout holding the branch. The owner's primary-checkout
   ruling invalidated the branch key the close, the bar and publication were
   built on, so the volume is consequence, not overreach.
2. **`primary_approval.absorption_census` duplicates queued `WI-596`**, an
   overlap flagged twice before implementation and not taken as a dependency.
   One home has to win.
3. **Lock semantics.** `out/integrate.lock` has exactly two contenders,
   `integrate.integrate()` and `primary_adjudication.run`, so it excludes the
   merge drain and nothing else; claims, lanes, intake and regeneration sit
   behind the separate coordinator lock. `_take_os_lock` is non-blocking, so a
   contender fails fast rather than queueing — no deadlock or backlog is
   reachable by holding it across model turns. During a primary turn the
   station is idle by construction (`dispatch._admission`, "only into an idle
   station"), so the exclusion is doing no work; its real value is
   cross-process. The durable blocker is `primary_publication.writer_refusal`
   reading the on-disk pending turn, which is what survived the SIGINT.
4. **`integrate._slot`'s docstring is now false** on the primary path: it still
   claims the slot is "held for well under a second" and calls the design
   speculative.

The ordered work list and a kickoff prompt for a fresh session are added to
[the handoff](../handoff-2026-09-07.md#resume-prompt-2026-09-07-after-the-stop);
status and the observations record point at both. No code, policy, registry,
queue or pause change in this sitting, and no approval of any disputed cell.

Deferred open items: none.
