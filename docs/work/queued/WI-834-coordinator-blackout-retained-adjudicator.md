+++
id = "WI-834"
title = "The blackout window pauses every lane at a step boundary and boots new sessions after it, on the loop and coordinator routes alike, and the coordinator's adjudicator is one retained session"
workstream = "process"
sr_refs = ["SR-227", "SR-229"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 9
+++

## Context

Owner direction 2026-10-05: the highest-priority row, so that other work items
can run through the coordinator's in-lane build process.

**What the window is for (owner, 2026-10-05).** The window marks a high-usage
range that is best avoided to save credits. The goal is to keep usage inside it
to a minimum while every lane reaches a good pause point. Lanes have taken
hours, so a lane is not expected to drain before the window starts. It pauses
and resumes. Inside the window no session is pinged or resumed; new sessions
boot once the window has ended.

**The loop already pauses this way.** `agent_loop.wait_out_blackout` runs
before every new session. A lane claimed before the window stays claimed and
idle, and it gets a new session after the window. The loop's gap is the
session already in flight when the window starts, which runs on until its
session timeout.

**The coordinator does not.** Nothing on the coordinator's path reads
`[policies] blackout`: not the guarded claim (`coordinator_guard.
claim_refusal`), not the session service, and not the guard's hooks. A
coordinator session claims, builds, reviews and adjudicates straight through
an armed window. This repo's value is `""` (disabled since 2026-09-04); the
shipped template's `12:00-12:00` is disabled too.

**Same methods, no new structure.** The coordinator pauses with the pieces the
kit already has, and Claude Code's hooks stand in for the loop's session
boundary, which an interactive session lacks:
- the window predicate (`agent_common.blackout_wake`);
- the lane's branch, worktree and step records as its pause state. A lane
  stays `active`, with no held state and no new directory (OI-70: a lane
  closes or stays claimed; it is never parked by renaming a ref);
- the handoff as the resume map;
- the guard's drain latch and relaunch, which wait out the window with the
  loop's own `blackout_wait`.

**Adjudicator gap.** The coordinator starts each adjudication as a fresh Claude
Code subagent, which reloads the spine and the briefs from nothing every
cycle. The retention layer that avoids this, the session service's keep
operation (`session_keep`, SR-227, LLR-270, verified on this box at WI-541), is
reachable only from the loop's route (`agent_loop.adjudication_keep`), and this
repo's `[adjudicator] context_reset_pct` is 0. Resetting at a threshold is
already the layer's rule: a retained session resets ahead of provider
compaction at `context_reset_pct`.

**One path.** Under the owner's rule of 2026-10-03, the coordinator's
adjudication goes through the same keep operation and the same
`out/adjudicator/` record as the loop's. Resuming a Claude Code subagent by
message would be a second mechanism: it is not measured by
`context_reset_pct`, and it is lost at the guard's relaunch. Independence
stands: the retained adjudicator never judges what its own session authored
(Terra authors, Opus judges), and OI-69 (b1) keeps
`reset_on_same_artifact = false`.

**The window and retention (owner, 2026-10-05; overrules OI-69 (c2)).** No
keep-warm ping fires inside the window, and no retained session is resumed
across it. The cache's lifetime is about an hour, so a transcript resumed after
a seven-hour window would replay uncached. That costs more than a new session
that reads only its brief, so the retained session is retired when the window
starts.

**Relation to S788.** WI-801 makes `ask` the only launcher for the loop and
the coordinator alike. This row's coordinator entry is the adjudicate route
that WI-801 absorbs as `ask`'s adjudicate kind, so no second launcher outlives
WI-801. WI-802's "this repo stays at 0" changes to the value set here.

**Owner rulings, 2026-10-05:**
- (a) The window keeps usage to a minimum while every lane reaches a good pause
  point (above).
- (b) This repo's `context_reset_pct` is 55, the value WI-802 ships in the
  template.
- (c) The window bites whenever it is armed, whether or not the context guard
  is on (`context_guard_pct`).
- (d) A session already in flight when the window starts finishes (the loop's
  behaviour today). To be revisited if it spends too much inside the window.
- (e) OI-69 (e1) stands: the retained session runs under its dedicated CLI
  home, where the owner signed in on 2026-10-05. A `claude -p` probe under
  that home answered on 2026-10-05.

## Done-when

- One predicate: `agent_common.blackout_wake` over `[policies] blackout`
  remains the only reader of the window, and every site below calls it.
- No new model session starts inside the window, on any route:
  - the loop waits at its session boundary (unchanged);
  - the session service refuses a launch on any other route;
  - the guard's PreToolUse hook denies the lease holder a new `Agent` tool call
    and a Bash call whose command starts a model CLI. The CLI names come from
    the executables in `docs/agents.toml`'s `cmd_template` cells, never from a
    hand-kept list. IF-275 is amended: the hook refuses exactly these calls and
    no other.
- While the window is armed, a claim on any route but the live dispatcher's is
  refused inside it, and the refusal names the UTC end. Outside the window, on
  a weekend, or with the window disabled, admission is unchanged.
- A session already in flight when the window starts finishes, bounded by its
  existing session timeout, on either route (owner ruling (d), 2026-10-05: an
  in-flight item should generally finish within the hour; to be revisited if
  measured usage inside the window says otherwise). No session starts after it
  inside the window, and the lane resumes from its record after the window.
- At the window's start, the coordinator pauses:
  - the guard latches drain mode at its next hook reading;
  - the coordinator brings each open lane to its step record without starting
    a session, writes the handoff naming each lane and its next step, and ends;
  - the relaunch it requests starts the successor only once the window has
    ended, waiting with `blackout_wait`;
  - a coordinator session that starts inside the window is told the same at
    `SessionStart`, and its relaunch waits too.
- At the window's start, each retained adjudicator session is retired with the
  reset reason `blackout`. No keep-warm ping fires inside the window, and the
  first adjudication after it mints a new session. OI-69 (c2) is overruled in
  the same commit.
- The coordinator runs an adjudication through the session service's keep
  operation, using one entry point that takes the composed brief file and the
  route. The entry point:
  - writes the session log;
  - prints the verdict;
  - uses the same `out/adjudicator/` record as the loop.
  No Claude Code subagent adjudicates. The `session-protocol` skill and the
  coordinator recipe direct the coordinator to this entry point, and WI-801's
  Done-when gains the line that `ask` absorbs it.
- Tests:
  - On both routes, a lane claimed before the window starts no session inside
    it, and it resumes after the window under a new session from its branch and
    worktree. The coordinator route resumes through the delayed relaunch and
    the handoff.
  - On the coordinator route, a second adjudication resumes the first one's
    session, and a session reaching `context_reset_pct` resets before its next
    call.
  - After a coordinator relaunch outside the window, the successor's first
    adjudication resumes the retained session. Across the window, it mints a
    new one.
- The retained Claude session has a working login in its dedicated CLI home
  (`out/adjudicator/home/anthropic`, OI-69 (e1)), confirmed by a one-line
  `claude -p` probe under that home. Then this repo's `[adjudicator]
  context_reset_pct` is set to 55 (owner ruling (b)). WI-802's "this repo
  stays at 0" line is amended in the same commit.
- Spine rows:
  - SR-229 (or a new SR) states the window's admission refusal, and a new SR
    states the pause at a step boundary and the resume after the window;
  - SR-227 and LLR-270 state the coordinator route and the retirement at the
    window;
  - IF-275 is amended, and TCs cover each site.
  Terra authors these rows, and each passes the in-lane adjudication.
- The row's test bar: its affected modules' tests plus the smoke tier.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit. The change is visible to an
  adopter only once they arm a window. A coordinator then pauses its lanes and
  ends inside the window, and the retained adjudicator is retired at its start.
