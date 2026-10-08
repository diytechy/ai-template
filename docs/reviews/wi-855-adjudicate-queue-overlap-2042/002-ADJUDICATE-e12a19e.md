# ADJUDICATE — WI-855 — re-sitting: the home WI-798 retires, at e12a19ed

A re-sitting of one question from the first sitting
(`001-ADJUDICATE-2d74139.md`, whose six edges and findings stand). The lane's
full-lane review (Codex 6.1 Sol, high) returned UNSOUND with one MAJOR: WI-798
retires the per-family home, WI-846 authenticates it and WI-834 checks it, and
nothing orders the removal after either. The coordinator confirmed the facts
and left the direction of any order to this sitting. This file supersedes 001
for the close: its last line restates the complete typed block.

Disclosure. I read WI-798, WI-834, WI-846 and WI-847 in `docs/work/queued/`;
the WI-788 design README (the owner's checkpoint ruling, A1 and A2, first; then
its change list, items 3, 21 and 22); its ch.2 §2 (session families), §4
(store, accounts and homes) and §9 (S788-accounts); OI-110 (ruled (b) on
2026-10-08) in `docs/requirements/open-items.toml`; D-029 in
`docs/decisions/wi-788.toml`; and, to check the seam, `session_keep.py`
(`HOME_VARIABLES`, `dedicated_home`, `dedicated_home_env`) and
`session_service.py` (the home overlay and the sign-in probe). I also read
`consolidate.parse_machine_line` and `reconcile_refusal`, to keep this file
readable by the close. HEAD stayed at e12a19ed throughout. WI-797 and WI-835
are complete (`docs/archive/work/complete/`).

**1. The overlap is real.** All three rows are claimable today once the pause
lifts. WI-798 needs only WI-797, which is complete. WI-846 lost its OI-110
wait with the ruling. WI-834 waits only on WI-846, by the first sitting's edge.
All three change one seam. `session_keep.dedicated_home` is "the one path rule,
read by the launch and by the sign-in probe". `dedicated_home_env` lays that
home over the route's environment, and `session_service`'s probe and
`require_signin` read it. In that seam:

- WI-846 adds the long-lived token at launch and turns the probe into a check
  that the token file is present.
- WI-834's part C has dev-setup read the same home through
  `session_keep.keep_config` and offer the `claude setup-token` step.
- WI-798 retires the seam: "the per-family home is gone" (README change 3,
  ch.2 §4: "a call runs under its account's home whether or not it is
  retained").

The danger is not a textual conflict at rebase. A builder can resolve that.
The danger is a deliverable undone with licence. WI-798's Done-when names no
token, no probe and no dev-setup step, and its Context cites README change 3
as authority for the retirement. If WI-798 lands second, its builder deletes
the family home and finds WI-846's and WI-834's tests bound to it. Its spec
then reads those tests as obsolete with the home. The token step, the
token-presence probe and dev-setup's sign-in offer go with them. The
adjudicator falls back to an interactive OAuth sign-in, which is the failure
WI-846 exists to end (refresh failures on 2026-10-06 and 2026-10-07, each
fixed by the owner signing in by hand). No gate catches this, because the
deletion matches WI-798's text. If WI-798 instead lands between WI-846 and
WI-834, WI-834's part C is written against a home that no longer exists.

**2. Which row waits: WI-798, after WI-834.** I weighed what each order delays.

- *WI-846 and WI-834 wait on WI-798.* This delays the owner's operational fix
  for the unattended adjudicator and WI-834, the row the owner named the
  highest priority (2026-10-05). They would wait behind a strong-tier row that
  carries a live login-isolation check, D-029's unverified state and a RESYNC
  migration of route configuration. It also holds back the whole existing
  chain WI-846 → WI-834 → WI-847 → WI-800. Rejected.
- *WI-798 waits on WI-834*, which reaches WI-846 through the first sitting's
  edge. Only two rows wait that would not have waited anyway. One is WI-798.
  The other is WI-817, the only row whose `needs` reach WI-798 without already
  passing through WI-834. WI-800 already waits on WI-847, which waits on
  WI-834. WI-814 and WI-815 wait on WI-801, which waits on WI-800. So the S788
  critical path is unchanged, except that it grows by any time WI-798 takes
  beyond the WI-852 → WI-847 branch, which runs beside it after WI-834.
  B12's "homes come first" orders WI-798 before the other S788 code rows. It
  still does; it never ordered WI-798 before the retrospective's rows. WI-834's
  ruling (e), "OI-69 (e1) stands" (2026-10-05), is consistent with this order:
  the dedicated home serves until WI-798 retires it, and WI-798 then carries
  the home's authentication across.
- *No edge, with an obligation on whichever lands second.* Rejected. A WI-798
  claimed while WI-846 is still in flight cannot carry a deliverable that has
  not landed. The first sitting's rule holds: two rows that can be claimed on
  the same day and would collide get an edge.

Sol proposed this direction. I reached it independently, on the delay
comparison above.

**3. The Done-when obligation falls on WI-798 alone.** With the edge, WI-846
and WI-834 build exactly as filed, against the dedicated home that exists when
they land. They need no new text. WI-798 lands second and must carry their
work. Its Done-when bullet "the per-family home is gone" licenses deletion as
written. The bullet below makes the retirement a migration: the
authentication, the probe and the dev-setup step move to the account home, and
none is retired.

One risk the bullet covers without ruling on it: the migrated home becomes a
non-ambient Claude account, which D-029 holds unverified until the
login-isolation check passes. The bullet requires that the adjudicator signed
in before the row is still signed in after it. How D-029's state applies to a
token-authenticated account is for WI-798's builder to settle, and its spine
rows to state, within that requirement. The bullet does not choose how a
second token-authenticated Claude account would declare its token variable.
OI-110 (b) declares one variable and tracks no path. Anything beyond the one
migrated account is WI-798's to argue in its spine rows, under the same rule.

WI-847 against WI-798 was also checked and gets no edge. Once enacted, both
wait on WI-834 and stay unordered between themselves. WI-847 adds a review
class to the keep operation; it never names a home. If WI-847 lands first, its
retained reviewer runs under the family home, which WI-798's existing rule
("whether or not it is retained") already moves to the account home. A
session dropped by the move costs one reload (ch.2 §4), and WI-847's tests
(resume within a lane, a fresh merge-gating round, dial off) do not depend on
which home is used. If WI-847 lands second, there is nothing to carry.

- [MAJOR] WI-798 / WI-846 / WI-834 -> WI-798 retires the per-family home
  (`session_keep.dedicated_home`, the one path rule the launch and the sign-in
  probe read). WI-846 authenticates that home with the owner's long-lived
  token, and WI-834's part C checks its sign-in. All three are claimable on the
  same day, and nothing orders them. WI-798's Done-when, landing second,
  licenses deleting both rows' work as part of the retired home. -> add the
  edge WI-798 needs WI-834 (WI-834 already needs WI-846). Give WI-798 the
  Done-when bullet below, so that the retirement migrates the token
  authentication, the probe and dev-setup's sign-in step to the account home
  and deletes none of them.

```toml
done_when = [{ row = "WI-798", bullet = "The per-family home's authentication moves to the account home and is not retired with it (WI-846, WI-834). This repo's dedicated Claude home becomes a declared account. A retained Claude launch under that account still reads the owner's long-lived token at launch through the environment variable OI-110 (b) declares: nothing about the path is tracked, and the token is never written to a log, prompt, record or commit. An unset variable, or a missing or unreadable token file, is still refused before launch, naming dev-setup, and an authentication failure still retires no session. The sign-in probe and dev-setup's check and `claude setup-token` offer report on that account's home. The adjudicator that ran signed in before this row runs signed in after it. WI-846's and WI-834's tests stay green, re-pointed at the account home rather than deleted, and the RESYNC entry states the migration." }]
```

OUTCOME: QUEUE-WITH-EDGE needs=WI-834;WI-847;WI-800;WI-851;WI-808;WI-801;WI-798 absorbs=-
