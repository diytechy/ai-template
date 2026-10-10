+++
id = "WI-897"
title = "The coordinator guard's hook costs less per tool call: a narrowed PreToolUse matcher and deferred imports"
workstream = "process"
sr_refs = ["SR-229"]
specref = "project-trajectory/scripts/coordinator_guard.py"
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by the coordinator on 2026-10-10 at the owner's request. The guard's
hook starts a fresh Python process on all eight hook events, and two of them,
PreToolUse and PostToolUse, fire on every tool call. Measured on the 4-core
workstation (loaded, so indicative only): starting the interpreter takes about
110–130 ms. A no-op `coordinator_guard.py hook` (not the holder, no blackout)
takes about 300–400 ms, of which importing `agent_common` is about 120 ms.
That is about 0.6 s of hook time per tool call, or roughly ten minutes over a
1,000-call coordinator session. The other six events fire once per turn or
less and are out of scope.

Anchor: SR-229 (the coordinator context guard), as amended by WI-834.

Deliverables, each independently landable; (1) lands first because it is a
pure refactor:

1. **Deferred imports.** The hook path for a call with nothing to do needs
   only the config read, `agent_policy.blackout_at` (`agent_common.blackout_at`
   re-exports it) and the `session_keep` lock. Import `agent_common` and
   `agent_route` only in the functions that use them (`model_clis`,
   `launch_reason`'s callers), and `argparse` only on the CLI path that is not
   `hook`. Behaviour is unchanged.
2. **A PreToolUse matcher.** The guard's PreToolUse group in
   `project-trajectory/agent-hooks/claude.settings.json` gains
   `"matcher": "Agent|SendMessage|Bash|PowerShell"`, exactly the keys of
   `LAUNCH_TOOLS` and `SHELL_TOOLS`; a test pins the two equal, so a tool added
   to either cannot be silently left unmatched. `guard_hooks.bind`
   copies the group whole, so `coordinator_guard.py hooks --enable` carries the
   matcher into the machine-local settings. PreToolUse's only job there is
   WI-834's blackout denial, and these are the tools `launch_reason` can deny.

   Rationale to confirm before building (2): `PreToolUse` is also in
   `MONITORED`, so today it measures context too. WI-822's claim-boundary case
   ("the next reply crosses it, and its first tool call is a claim") is refused
   both by the PreToolUse measurement and by `integrate.claim`'s own reading
   with no hook run. A claim runs through Bash, so the matcher keeps that path.
   For any other tool, the latch instruction is delayed by at most that one
   call, until its PostToolUse.

Out of scope: a long-lived helper process the hook signals (a new lifecycle
and a single point of failure), and interpreter flags such as `-I` (too small
to measure on this box).

## Done-when

- (1) A test pins the hook's no-op path as not importing `agent_common` or
  `agent_route` (for example, a subprocess hook call that then checks
  `sys.modules`). The existing coordinator-guard tests pass unchanged.
- (2) The example's guard PreToolUse group carries the matcher, and
  `hooks --enable` writes it. A blackout denial still fires for each tool in
  WI-834's list, and the WI-822 claim-boundary fixture still refuses.
  `tests/test_dogfood_sync.py` and `tests/test_run_devsetup.py` pass.
- Re-measure a no-op hook call before and after on a quiet box and record both
  in the lane log.
- LLR-300 and IF-274 are amended if (2) makes them untrue (they state which
  events the guard runs on); traced cells otherwise.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry for (2) anchored at a trunk commit. An adopter re-runs
  `coordinator_guard.py hooks --enable` to pick up the matcher.
