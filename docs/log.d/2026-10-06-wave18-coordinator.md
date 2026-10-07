Deferred open items: OI-98, OI-105, OI-106, OI-107

## 2026-10-06 — Wave-18 coordinator: the adjudication batch; four rows land, the Done-when blessing stays on its lane

The coordinator claimed the owner's four-row batch (WI-838 to WI-841) plus
WI-842 under one scoped unpause (`465cceab`, the pause restored byte-identical
in `d69e04f3`). WI-842 was filed at the session start: the wave-17 holder's
coordinator lease had stranded, and the owner asked that releasing it stop
needing their attention. Roles as before: Claude Opus builds (kit-builder,
medium), GPT Terra (medium) authors rows, Codex 6.1 Sol (high) reviews, and the
retained Claude Opus adjudicator judges through `coordinator_adjudicate.py`
from each lane.

### Landed

- **WI-839** (`2648d1dd`): PROCESS_OPTIONS.md states the module-size ratchet's
  lane-carried re-stamp that `integrate.py` already implements, and
  concurrency-restructure §5.2/§5.3 link to it. Sol round 1 asked for a RESYNC
  entry; the pack's own precedent for prose-only corrections confirmed it.
- **WI-842** (`f9265d99`, act 41): `coordinator_guard.py handback`. The holder
  frees its own lease at close-out, refused for any other caller and only by
  the holder's own pending relaunch (Sol round 1 found that a crashed
  predecessor's request blocked it). SR-229, LLR-300, TC-316 and TC-318 were
  re-attested; the WI-843 re-mint was closed citing act 41.
- **WI-838** (`0ccebafb`, acts 42 and 43): a route's first retained mint writes
  a lease-only record before launch, and a mint lands only on its own lease
  (Sol round 1 found that a late first mint could replace a finished
  replacement). Adjudication 001 returned LLR-270 for two general clauses
  Terra had dropped. They were answered in the lane; 002 blessed it and 003
  approved TC-329. The WI-844 re-mint was closed citing act 42.
- **WI-840** (`76b1d212`): `tmp_path_retention_policy = failed` and one dated
  scratch root per session. A full run on the lane left 193 MB where wave 16
  recorded about 4 GB; the quiet-box smoke tier ran in 37.0 s and 38.3 s against
  the 60 s budget.

### WI-841 stays on its lane

The in-lane Done-when blessing took five builder rounds and seven Terra rounds.
Sol's findings:

- Round 1 (five MAJORs): archive closes slipped the hold, a combined sitting's
  acts had no scope, intake read only the first Dispositions block, the brief
  lacked the spec's Context, and an empty combined verdict validated.
- Rounds 2 to 4: the WIDENED check missed, in turn, cross-registry acts, the
  CSV carrier and the markdown needs carrier.

The adjudicator re-attested seven amended rows. It approved LLR-309 and TC-326
and returned the rest. The answers came in the lane:

- an unreadable claim failed open, and now holds;
- LLR-308 was split, with the combined sitting under derived SR-232;
- LLR-262's wording was restated.

The session stopped at the 50% context guard with one builder round (the
markdown carrier, through the kit's one carrier reader), a Terra round, a Sol
round and two adjudication sittings owed.

### Environment

- **Codex:** the plan limit was hit at about 20:09 and reset at 23:02. The
  owner signed in to Codex again.
- **The adjudicator's dedicated Claude home** could not refresh its OAuth token
  from 21:17. Four calls failed, each leaving `.oauth_refresh.lock` behind.
  The first failure retired the retained session as unusable.
  - Removing the lock (owner-directed) did not help; the owner's re-sign-in
    did.
  - The root cause is not established. The probe's blind spot, the retirement
    on an auth failure and the unrecorded provisioning belong to WI-834's
    sign-in step.

### Full suite

At trunk `76b1d212` (detached worktree, fixed basetemp under the session's
dated root): 5291 passed, 17 skipped, 0 failed, in 711.0 s (11:50); the basetemp held 206 MB afterwards (WI-840's retention policy) and was deleted once recorded.

### 2026-10-07 — WI-841 finished past the guard, at the owner's direction

The owner directed that WI-841 close in this session rather than at a relaunch
(coordinator D-010). Builder rounds 6 to 19 and Terra rounds 8 to 21 answered
Sol and the adjudicator. At the owner's request the hand path's last gate became
a fresh, full-lane review (D-011). Eleven such gates ran, and each but the last
found real defects that crossed rounds:

- a rejected or failed sitting still released the holds;
- the readers parsed more loosely than the validator;
- the loop recorded acceptance from syntax alone;
- released-tier acts skipped acceptance;
- coverage matched verdict kinds, not the rows judged (the owner ruled row
  coverage in scope);
- the build hold sat inside one return arm;
- machine lines crossed line boundaries.

The fixes ended each class rather than its instance:

- one parser, per physical line;
- an acceptance outcome recorded by the route that ran the call;
- one accepted-verdict reader for every consumer;
- row-tied act authority;
- one carrier resolver;
- one dispatch-point hold.

The eleventh gate, `2874ff0a`, was SOUND. Landing needed a copy act
re-anchoring TC-326/TC-327's traced-only evidence (D-012). The squash first
landed under the wrong message and was amended before any push (D-013).
Landed as `68e0ee87`, acts to seq 59; the re-mint WI-845 is closed.

The adjudicator's dedicated home failed to refresh again after the owner's
clean `/login`, so the headless refresh failure is reproducible, not a bad
credential. The owner chose the long-lived token: WI-846. Filed: WI-847 (the
loop's reviewer resumes within a lane, with a fresh full-lane merge gate).
