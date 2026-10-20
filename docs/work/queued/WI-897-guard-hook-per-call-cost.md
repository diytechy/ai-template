+++
id = "WI-897"
title = "The coordinator guard's hook costs less per tool call: a narrowed PreToolUse matcher and deferred imports"
workstream = "process"
sr_refs = ["SR-229"]
specref = "project-trajectory/scripts/coordinator_guard.py"
buildtier = "quick"
safety_class = "ordinary"
priority = 3
planmode = "single"
needs = []
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
   copies the group whole, so the consented install (`hooks --offer`, as
   dev-setup's offer and the take at a terminal run it) carries the matcher
   into the machine-local settings it writes. PreToolUse's only job there is
   WI-834's blackout denial, and these are the tools `launch_reason` can deny.

   **The event and tool contract (2) settles.** The guard's PreToolUse group
   runs for exactly four tool names, `Agent`, `SendMessage`, `Bash` and
   `PowerShell`; a call to any other tool runs no guard at PreToolUse. Every
   other guard group stays unmatched: PostToolUse and PostToolUseFailure still
   run the guard for every tool, and the other events are unchanged. The
   hook's own monitored event set (`MONITORED`) is unchanged. For a tool
   outside the four, two things move:
   - the context measurement that latches drain mode, and the latch
     instruction it injects, happen at that call's PostToolUse (or
     PostToolUseFailure when the call fails), after the call instead of
     before it;
   - the drain reminder and the blackout window's close-down reminder count
     only the events the hook receives, so their every-twentieth cadence
     spans more tool calls.

   Nothing that refuses moves. The blackout denial is a PreToolUse answer for
   exactly these four tools (`launch_reason` names no other). A claim runs
   through a shell tool, and `integrate.claim`'s own reading
   (`claim_refusal`) refuses it with no hook run, which covers WI-822's
   claim-boundary case ("the next reply crosses it, and its first tool call
   is a claim"). The promise reaches the kit's shipped example and the
   consented install that copies it (PROCESS.md §6, the supported
   workflows); a hand-edited matcher is residue (`## Trust`).

Out of scope: a long-lived helper process the hook signals (a new lifecycle
and a single point of failure), and interpreter flags such as `-I` (too small
to measure on this box).

## Trust

Deliverable (2) gives a file authority over a hold. The guard PreToolUse
group's matcher, in the machine-local settings Claude Code reads, decides
which tool calls the blackout denial can refuse and which calls the context
guard measures before they run. This is a trust boundary in the sense of
`project-trajectory/PROCESS.md` §3, "When a guard is owed". The row adds no
reader of its own: the carriers below, their producers and their failure
rulings are WI-927's, and this row keeps them unchanged.

- **Carriers and their producers.**
  - **The kit's `agent-hooks/claude.settings.json`:** reviewed kit content.
    Bootstrap copies it to `.claude/settings.json.example`; an absent source
    is skipped, and an existing destination is kept unless forced. A failed
    copy is a failed scaffold or re-sync step, never an installed guard.
  - **`.claude/settings.json.example`:** read by the guard-hooks reader for
    the state reading and the install's copy of each group.
  - **`.claude/settings.local.json`:** written only by the consented install,
    through the kit's atomic write (a temporary sibling replaced whole; a
    failed write raises and leaves the old file), then read again.
- **Consumers, by path:**
  - `project-trajectory/scripts/kitlib/guard_hooks.py` (the state reading and
    the install);
  - `project-trajectory/scripts/coordinator_guard.py` (`hooks`, the lease
    take, and the `hook` the settings run);
  - the readiness checks and offers in
    `project-trajectory/scripts/dev-setup.template.sh`,
    `project-trajectory/scripts/dev-setup.template.ps1`, and this
    repository's `scripts/dev-setup.sh` and `scripts/dev-setup.ps1`, each
    through `coordinator_guard.py`, never through a matcher parser of its
    own;
  - Claude Code's hook dispatcher (external), which applies the matcher.
- **Rulings.**
  - Absent, unreadable, unparseable and malformed inputs keep WI-927's
    rulings: an absent install happens only after a yes; an unreadable,
    unparseable or malformed file reads `occupied` and nothing is written;
    a take goes on only at `none`, at `on`, or after a consented install
    whose re-read reads `on`. A failed or partial install is never read as
    installed. This row changes no reader, so it adds no ruling there.
  - The state reading is by command name, so it does not attest the
    matcher. An older, unmatched PreToolUse group reads `on` and runs the
    guard on every tool, which costs time and refuses nothing it should
    not. The upgrade is the RESYNC entry's remove-and-consent route;
    nothing migrates automatically.
  - The matcher's alternatives are exactly the keys of `LAUNCH_TOOLS` and
    `SHELL_TOOLS`, pinned by a test, so a tool added to either cannot be
    left unmatched. If Claude Code reads the matcher as an unanchored
    pattern, a longer tool name containing one of the four also reaches the
    hook: that costs a call and denies nothing, since `launch_reason` names
    only the four.
  - The hook's own failure directions are unchanged and not broadened:
    malformed stdin or a caught failure prints to stderr, denies nothing and
    exits 0 (IF-274, IF-281), and a response is IF-275's JSON. An empty
    response, a failed call or a timeout is neither a denial nor a
    measurement.
- **Residue, stated once** (PROCESS.md §6; none of these is promised):
  - a running Claude Code session uses the settings it loaded (`/hooks` or a
    restart picks up a new install);
  - Claude Code's own handling of a malformed settings file, and of a hook
    that outruns its 30-second timeout;
  - a hand-edited matcher;
  - a shipped example holding JSON `null` reads `none`, a gap already among
    status.md's unfiled follow-ups, which this row leaves as it is.

## Done-when

- (1) A test pins the hook's no-op path as not importing `agent_common` or
  `agent_route` (for example, a subprocess hook call that then checks
  `sys.modules`). The existing coordinator-guard tests pass unchanged.
- (2) The example's guard PreToolUse group carries the matcher, and the
  consented install writes it into settings that hold no guard group. A
  test pins the matcher's alternatives equal to the keys of `LAUNCH_TOOLS`
  and `SHELL_TOOLS`. The example's PostToolUse and PostToolUseFailure guard
  groups carry no matcher. A blackout denial still fires for each tool in
  WI-834's list, and the WI-822 claim-boundary fixture still refuses.
  `tests/test_dogfood_sync.py` and `tests/test_run_devsetup.py` pass.
- (2) The moved measurement, pinned for a tool outside the four (`Read`):
  past the threshold, the hook given that tool's PostToolUse latches drain
  mode and injects the instruction, and so does its PostToolUseFailure;
  inside a blackout window, each tells the close-down at its cadence and
  denies nothing.
- Re-measure a no-op hook call before and after on a quiet box and record both
  in the lane log.
- The lane's checkpoint reads LLR-300, IF-274, IF-275 and IF-281 against the
  event and tool contract in Context. Each sentence the matcher makes untrue
  is amended, and the lane's decisions record why each of the four otherwise
  stays true; traced cells otherwise.
- RESYNC_PACK: an entry for (2) anchored at a trunk commit. The guard state is
  read by command name, so a matcher-only change still reads `on` and nothing
  reinstalls the groups: an adopter who wants the new matcher removes the
  installed guard groups from the machine-local settings and runs the
  consented install again (the next first run reads `absent`, asks, and
  installs the new ones). `hooks --enable` no longer exists (WI-927).

## Scope answers

- **S1:** two deliverables, each independently landable: (1) the deferred
  imports, a behaviour-preserving refactor, lands first; (2) the matcher,
  with its pins, its traced-row reading and its RESYNC entry, lands second.
  They stay in one row on purpose: both answer the same per-call cost, and
  the measurement Done-when item reads them together.
- **S2:** yes; see `## Trust`.
- **S3:** a closed space. The matcher is an enumerated four-name set, equal
  to the two tool tables by a pin; every other tool name is outside it by
  default and runs no guard at PreToolUse. The events are the example's
  eight, unchanged.
- **S4:** `single`. The row has a Trust section and crosses the settings
  install and the hook runtime.
- **S5, the architectural delta:** whether the guard runs before a call now
  depends on a new input, the tool's name, through the matcher. Within the
  row's scope: Context's event and tool contract carries it. No state, no
  domain value and no new boundary in the kit's own code; no refactor row
  is owed.
- **S6, dependencies:** `needs = []`. WI-927, which this row's RESYNC entry
  follows, has landed. No third-party dependency.
- **B1:** the matcher's equality pin, stated in Context, is a Done-when item.
- **B3:** the state reading reads the settings as they are now; nothing past
  is recomputed.
- **B4:** no Done-when item needs an owner act or credential.

## Critique dispositions

Round 1 (Codex Sol, medium, 2026-10-19; CHANGES-REQUESTED, four MAJORs;
the row predates S3 to S5, so the round re-critiqued it whole):

- **S2, MAJOR (no Trust section): adopted.** The row gains `## Trust`,
  which names the three carriers and their producers, every consumer by
  path, and the rulings. It reads "This row changes no reader, so it adds no
  ruling there", "The state reading is by command name, so it does not
  attest the matcher", and "The hook's own failure directions are unchanged
  and not broadened". The residue lists the running session's loaded
  settings, Claude Code's own malformed-settings and timeout handling, and a
  hand-edited matcher. Not adopted: the critique asked for a new ruling on a
  parseable but structurally malformed example. WI-927 already rules a
  malformed settings file `occupied`, and its one gap, an example holding
  JSON `null`, is a filed follow-up; this row adds no reader, so the Trust
  section names that gap as residue instead of fixing it here.
- **S3/S5, MAJOR (the provisional rationale): adopted.** Context's
  "Rationale to confirm before building (2)" is replaced by "The event and
  tool contract (2) settles": "exactly four tool names", "PostToolUse and
  PostToolUseFailure still run the guard for every tool", the latch and its
  instruction moving to the call's PostToolUse or PostToolUseFailure, the
  reminders' cadence spanning more calls, and "Nothing that refuses moves",
  with the claim's own reading and the supported-workflow bound. The
  Done-when gains the equality pin, the unmatched PostToolUse and
  PostToolUseFailure groups, and "The moved measurement, pinned for a tool
  outside the four", success and failure both, beside the existing denial
  for each of the four. The LLR-300 and IF-274 item becomes "The lane's
  checkpoint reads LLR-300, IF-274, IF-275 and IF-281 against the event and
  tool contract", amending or recording each.
- **S4, MAJOR (no planmode): adopted.** The frontmatter reads
  `planmode = "single"`, and Scope answers S4 gives the reason.
- **S2, MAJOR (the "Review bar: A" line): adopted in part.** The line is
  deleted: the row is reviewed as every lane is, with no single-reviewer
  exception. Not adopted: the replacement link and a Trust entry for the
  review gate. The review shape is the coordinator-cycle skill's procedure,
  not a carrier this row gives authority, and restating it in a row is the
  copy the kit's one-home rule forbids.
