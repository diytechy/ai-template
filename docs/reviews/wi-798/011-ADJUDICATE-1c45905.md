# WI-798 dispute sitting 011 at 1c45905 (range 9c4971543..ca90862fc)

## A009-F1: a qualified OpenCode launch drops the loop marker

**Observed.** In `session_service._ambient_base`, a declared account whose CLI
has a `BASE_ENVIRONMENT` inherits only the names in that base. The opencode base
lists platform, home, temp, locale and proxy names, but not
`kitlib.provenance.LOOP_SESSION_ENV` (`KIT_LOOP_SESSION`).

I called `_compose` on an ambient environment holding `PATH`,
`KIT_LOOP_SESSION` and `OPENAI_API_KEY`, with an `opencode` account and its two
home variables. At this range the result is `OPENCODE_CONFIG`, `PATH`,
`XDG_DATA_HOME`, so the marker is gone. I ran the same script against a
worktree at `6a70de32a^` and it returns the marker, which confirms the
regression the finding states. Both launch paths compose through this rule:
the retained path (`compose_env`, reached through `act`) and the unretained one
(`launch_env`). Either way, every session the loop launches on a qualified
OpenCode entry runs without the marker.

**Why it matters.** The marker is what the commit floors read:

- `check.py --loop-trailer` refuses a loop commit that has no trailer, or the
  wrong one.
- `_held_status_refusal` refuses a loop commit that moves a status the dial
  holds for a human (SR-208).

With the marker dropped, both floors read that child as a person and pass.
The held-status refusal therefore fails open at the point where the commit is
made. The trailer floor's failure moves to the merge slot instead, where an
unmarked lane commit parks the lane.

LLR-247 states that "child sessions inherit it". The IF-194 notes make
inheritance the whole mechanism: "every child inherits it ... without any
launcher passing it on". So the lane breaks behaviour the spine requires.

**Scope.** This needs nothing outside PROCESS.md §6's bound. A qualified
OpenCode account is a configuration that this lane itself ships (IF-245's
opencode home variables, account tables for every CLI). The unattended loop is
the kit's own route, and it sets the marker in its own process
(`agent_loop.main`, `dispatch.run`) before launching through this function. No
hostile binary, hand edit or contrived ordering is involved.

**The fix.** It is cheap and stays inside the lane's construction: the
kit-owned marker must survive the one composition boundary. Name it once from
`kitlib.provenance` among the names a declared base always keeps; it is not a
credential. Then pin inheritance through a qualified OpenCode launch.

This is convergence-class, because it disables a commit-time guard for that
session. So it cannot be a successor, and it is not one to escalate: the
remedy is unambiguous.

RULING: A009-F1 FIX a qualified OpenCode account's declared base (session_service.BASE_ENVIRONMENT via _ambient_base) drops KIT_LOOP_SESSION, so loop-launched sessions on that route lose the provenance marker LLR-247/IF-194 require children to inherit, disabling the commit-time loop-trailer and held-status floors for them (a regression from 6a70de32a^, reproduced); keep the kit-owned marker through the one composition rule and test it through a qualified OpenCode launch
