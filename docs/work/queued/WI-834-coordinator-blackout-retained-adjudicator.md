+++
id = "WI-834"
title = "Blackout pauses lanes on both routes; the coordinator's adjudicator is retained; run checks the workstation first"
workstream = "process"
sr_refs = ["SR-227", "SR-229", "SR-230"]
specref = "docs/reviews/wi-834-plan/001-sol-plan-review.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 9
+++

## Context

Owner direction 2026-10-05: the highest-priority row, so that other work items
can run through the coordinator's in-lane build process. It stays one row by
the owner's choice (2026-10-05), so its Done-when is grouped into three parts,
each with its own tests:
- part A, the coordinator's retained adjudication;
- part B, the blackout pause;
- part C, run's workstation check and the sign-in step.

The parts land as one lane.

**What the window is for (owner, 2026-10-05).** The window marks a high-usage
range that is best avoided to save credits. The goal is to keep usage inside it
to a minimum while every lane reaches a good pause point. Lanes have taken
hours, so a lane is not expected to drain before the window starts. It pauses
and resumes. Inside the window no session is pinged to keep it warm, and new
sessions boot once the window has ended.

**The loop already pauses this way.** `agent_loop.wait_out_blackout` runs
before every new session. A lane claimed before the window stays claimed and
idle, and it gets a new session after the window.

**The coordinator does not.** Nothing on the coordinator's path reads
`[policies] blackout`: not the guarded claim, not the session service, and not
the guard's hooks. Every hook entry point returns early while
`context_guard_pct` is 0. A coordinator session claims, builds, reviews and
adjudicates straight through an armed window. This repo's value is `""`
(disabled since 2026-09-04); the shipped template's `12:00-12:00` is disabled
too.

**Same methods, no new structure.** The coordinator pauses with the pieces the
kit already has. Claude Code's hooks stand in for the loop's session boundary,
which an interactive session lacks:
- one window function;
- the lane's branch, worktree and committed step records as its pause state.
  A lane stays `active`; a scheduled wait keeps the claim and adds no held
  state (OI-70; `docs/work/README.md`: active means claimed). A stop the owner
  must act on still closes partial;
- the handoff as the resume map;
- the guard's injected context.

The owner resumes the coordinator after the window, so no relaunch happens
across it.

**Adjudicator gap.** The coordinator starts each adjudication as a fresh Claude
Code subagent, which reloads the spine and the briefs from nothing every
cycle. The retention layer that avoids this, the session service's keep
operation (`session_keep`, SR-227, LLR-270, verified on this box at WI-541), is
reachable only from the loop's route (`agent_loop.adjudication_keep`), and this
repo's `[adjudicator] context_reset_pct` is 0. At the dial, a retained session
drains and retires at the next clear point (`session_keep._before_launch`).

**One path.** Under the owner's rule of 2026-10-03, the coordinator's
adjudication goes through the same keep operation and the same
`out/adjudicator/` record as the loop's. A Claude Code subagent resumed by
message would be a second retention mechanism, outside the kit's keep
planning, dedicated-home overlay and bookkeeping. Independence stands: the
retained adjudicator never judges what its own session authored (Terra
authors, Opus judges), and OI-69 (b1) keeps `reset_on_same_artifact = false`.

**The window and retention (owner, 2026-10-05; overrules OI-69 (c2)).** No
keep-warm ping fires inside the window. A retained session is not resumed
across it: the cache lives about an hour, so a transcript resumed after a
seven-hour window would replay uncached, which costs more than a new session
that reads only its brief. Nothing runs at the window's start (OI-69 (a1): no
daemon), so the retirement is lazy, at the first keep call after the window.

**The sign-in.** With retention on, both routes' retained Claude sessions run
under the dedicated CLI home (OI-69 (e1)), which needs its own sign-in. The
user is offered it in exactly one place: dev-setup, which run calls first. The
loop's launcher (`agent-resume.*`) offers nothing. On any route, a launch that
needs the sign-in and finds none is refused with a pointer to dev-setup; it
never falls back to a fresh session.

**Relation to S788.** WI-801 makes `ask` the only launcher for the loop and
the coordinator alike. This row's coordinator entry point is temporary.
WI-801 deletes it and moves its callers and tests to `ask`'s adjudicate kind.
WI-802's "this repo stays at 0" changes to the value set here.

**Review.** Sol (gpt-6.1-sol, high) reviewed this spec before building
(specref: NOT YET SOUND, one BLOCKER and seven MAJOR). The coordinator
confirmed the load-bearing claims against the code; every fix below is
accepted by the owner (2026-10-05).

**Owner rulings, 2026-10-05:**
- (a) The window keeps usage to a minimum while every lane reaches a good pause
  point (above).
- (b) This repo's `context_reset_pct` is 55, the value WI-802 ships in the
  template.
- (c) The window bites whenever it is armed, whether or not the context guard
  is on (`context_guard_pct`).
- (d) A session already in flight when the window starts finishes, within its
  existing bounds (the loop's behaviour today). To be revisited if it spends
  too much inside the window.
- (e) OI-69 (e1) stands. The owner signed in under the dedicated home on
  2026-10-05; `claude auth status` there reports `loggedIn: true`.
- (f) In the window, the coordinator session is encouraged to write its
  handoff and close down. Adjudication may still run to bring open lanes to
  their pause point. The owner resumes the coordinator after the window.
- (g) A bare double-click of run calls dev-setup first, so dependencies are
  verified before the user is handed the repository's tasks. That check
  includes the dedicated home's sign-in, offered with consent. The check is
  NOT on the agent-resume path.
- (h) One row, not three.

## Done-when

### Part A: the coordinator's retained adjudication

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
- A launch whose keep needs the dedicated home's sign-in, and finds none, is
  refused on either route, naming dev-setup.
- Tests:
  - a second adjudication on the coordinator route resumes the first one's
    session;
  - a session at `context_reset_pct` drains and retires at the next clear
    point;
  - a missing sign-in refuses the launch.
- The sign-in is confirmed (`claude auth status` under the home). Then this
  repo's `[adjudicator] context_reset_pct` is set to 55 (ruling (b)), and
  WI-802's "this repo stays at 0" line is amended in the same commit.

### Part B: the blackout pause

- **One window function.** It answers both "is `t` inside a window?" and "when
  did the most recent window end before `t`?". Admission, launch, the hooks and
  retirement all call it, and it is the only reader of `[policies] blackout`.
  - A window that wraps past midnight belongs to its start weekday, so a
    Friday-night window continues into Saturday and a Sunday-night window
    does not exist. This fixes today's use of the current date
    (`agent_common.blackout_wake`).
  - The end is exclusive, as today.
  - The window is read as declared at the call, so a changed value applies
    from then on.
- **The launch boundary.** The session service refuses a launch inside the
  window for every caller. The loop handles the refusal by waiting and
  retrying (its existing `blackout_wait`). That also covers the loop's
  interactive route and recovery probes, which reach the service directly.
  The one admitted launch is an adjudication of a work item whose row is
  `active`. Claims are refused inside the window, so an active row is a lane
  claimed before it. The rule is derived from the registry, with no
  caller-selected flag. IF-246 is amended.
- **Claim admission.** On every route but the live dispatcher's
  (`dispatch_lock_held`), a claim inside the window is refused, naming the UTC
  end. The check runs before the context guard's dial check, so it applies
  with the guard off. Outside the window the guard's decision is unchanged.
  IF-271, SR-229 and LLR-300 are amended, since each states guard-off
  admission as unconditional.
- **The hooks.** While a window is armed, the guard's hooks run whether or not
  the context guard is on. The blackout drain is computed from the clock at
  each call, never latched, so nothing needs clearing after the window. The
  context-threshold latch is unchanged. Inside the window, PreToolUse denies
  the main session (not a subagent) these calls:
  - a new `Agent` call;
  - a `SendMessage` that resumes a subagent;
  - a `Bash` or `PowerShell` call naming a model CLI as any command word,
    including after `timeout`, `env` and `VAR=value` prefixes and in `&&`,
    `||`, `;` and `|` chains.
  The CLI names come from the executables in `docs/agents.toml`'s
  `cmd_template` cells, never from a hand-kept list. Script wrappers are not
  inspected. Instead, the coordinator's launch scripts call a guard subcommand
  that exits nonzero inside the window. The hook is supervision within that
  coverage, not inspection of arbitrary shell programs. IF-274 is amended
  (`tool_name`, `tool_input`) and IF-275 (the denial response).
- **The coordinator's close-down.** Inside the window, SessionStart and the
  monitored events tell the main session to:
  1. bring each open lane to its pause point, using wrap-up adjudication where
     a step needs it;
  2. write the handoff naming each lane and its next obligation;
  3. end the session.
  A relaunch request is neither written nor launched inside the window. At
  SessionEnd inside the window, a pending request is cancelled and recorded
  as `blackout`; no successor starts. SR-230 and LLR-301 are amended. To
  resume, the owner reopens the same session, which still holds the lease, or
  releases and takes the lease for a fresh one. The `session-protocol`
  close-out recipe states both, and no longer says every close-out requests a
  relaunch.
- **The pause point.** It is the last finished step whose evidence is
  committed. A lane whose next step is a review, rework or any launch the
  window refuses stops there, and the handoff names that obligation; the
  review cycle is not completed to reach a pause. An in-flight call finishes
  within its existing bounds (ruling (d)). The coordinator's stop is
  encouraged, not enforced (ruling (f)).
- **Retention across the window.** No keep-warm ping fires inside it. A wrap-up
  adjudication inside it may resume the retained session. At the first keep
  call after a window, a session whose last use is before that window's end is
  retired with the reset reason `blackout`, overriding pending-chain
  continuity, and a new session is minted. A record without a last-use time
  retires. OI-69 (c2) is overruled in the same commit.
- Tests:
  - the window function's boundary fixtures: the end minute, a wrap across
    Friday to Saturday and across Sunday to Monday, a weekend, disabled, a
    changed value, and a missing last-use time;
  - on both routes, a lane claimed before the window starts no session inside
    it except a wrap-up adjudication of an active row, and resumes after it
    under a new session;
  - a review-next lane pauses with the obligation in the handoff, and a
    wrap-up verdict that requires rework waits;
  - with the context guard off, the hooks deny each listed call form, the
    claim is refused, and no relaunch is written or launched;
  - a pending relaunch at SessionEnd inside the window is cancelled.

### Part C: run checks the workstation first

- A bare `run` (the double-click, no arguments) calls dev-setup's check before
  the menu, in every shipped `run.*` launcher template. If anything is
  missing, it offers dev-setup's consent-first install, item by item, then
  shows the menu. `run <name>` and `run --list` (the agent surface) never
  prompt.
- dev-setup's check reports the dedicated home's sign-in as signed in,
  missing or unknown, using `claude auth status` under that home with no model
  call. The check resolves the home without creating it.
- The consent step states what the sign-in command does: it sets the CLI's
  config-home variable for that one command only, so the sign-in lands in the
  adjudicator's own home, and the user's normal login and every other
  repository are left alone. Accepting runs the interactive sign-in. Denying
  leaves configuration and credentials unchanged.
- The step appears only while retention is on. `agent-resume.*` gains no
  check, and a launch with a missing sign-in is refused (part A).
- Tests:
  - a bare run calls the check before the menu;
  - the direct and list forms never call it;
  - signed in, missing and unknown are each reported, and a denial changes
    nothing.

### The whole row

- Spine rows:
  - SR-229, SR-230 and a new SR for the pause and the resume after the window,
    in capability voice with no concrete artifact (ruling R2);
  - SR-227 and LLR-270 for the coordinator route and the lazy retirement;
  - LLR-300, LLR-301, IF-246, IF-271, IF-274 and IF-275, amended, plus an IF
    for the window function and the entry point, and TCs for each site;
  - the run launcher's interface row (IF-048), amended;
  - IF-278's owner and token transfer rule, kept;
  - the affected runtime flow in `docs/runtime-flows.md`, updated in the same
    change.
  Terra authors these rows, and each passes the in-lane adjudication.
- The row's test bar: its affected modules' tests plus the smoke tier.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit.
  - The window's changes are visible only once an adopter arms a window: a
    coordinator then closes down inside it, and a retained adjudicator retires
    across it.
  - The coordinator entry point and the sign-in refusal are visible once
    retention is enabled.
  - A bare run now runs dev-setup's check first.
