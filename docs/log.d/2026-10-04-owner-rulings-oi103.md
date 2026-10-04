Deferred open items: none

## 2026-10-04 — The owner rules OI-103: WI-788's lane-state design questions

The owner's words are quoted in OI-103's `decision` cell in
[../requirements/open-items.toml](../requirements/open-items.toml), with the
coordinator's reading. In short:

- Q1 (a), with a principle: nothing the tool runs writes to trunk directly. Every change reaches trunk through a work item's lane and its merge. Claims, mints, plan-id allocation and keep-warm or telemetry records each become lane-side, or part of the merge under the station authority, so the merge is the only tool writer to trunk. The owner's own approvals rarely happen while the loop runs. WI-788's design says, for each of today's trunk writers, how it moves.
- Q2: a sitting never waits while holding the lock. Anything owed to the owner, and any rows still unsettled when rounds run out, are minted (each open item with its placeholder row) and handled after the merge, through those rows. S11's ruled exhaustion behaviour (3 returns, then land) stands.
- Q3 (b): the adjudicator has the final call on whether a reviewer's request is respected or ignored, so no new independent review is drawn to endorse a resolution. S11 Q4's final review of the post-act tree still checks the adjudicator's own writes, and it does not reopen a dispute the adjudicator resolved.
- Q4 (a): one squash commit per item on trunk, with the lane tip kept in archive/lanes, on both the loop and the hand path.
- Q5: a configuration dial, "planned items build at a lower tier than their planner", default false. When it is on, an item whose plan came from a strong-tier planner builds at medium. It replaces LS3's scope threshold and B8's typed-scope requirement; the plan's identity and the planner's tier are still recorded so that the dial can be applied.
- Q6 (b): keep today's recovery at the agent's discretion (the reconcile note, the leftover stash, the as-is partial commit). The usage harvest (U1) still applies.

WI-788's Done-when carries these. Q5 supersedes LS3's scope threshold and amendment
B8's typed scope; Q6 leaves today's recovery paths in place.
