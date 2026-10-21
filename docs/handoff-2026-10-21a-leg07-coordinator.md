# Handoff 2026-10-21a (headless leg 07): WI-962 landed; WI-963 and WI-940 claimed and built in part

It replaces [handoff-2026-10-20e-attended-coordinator.md](handoff-2026-10-20e-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 07 (loop session
`20261021T045653Z-213020`) landed queue row 1, filed the shape-rule
retirement row its lane routed findings to, and claimed queue rows 2 and 3
under one scoped unpause. It carries no `Overnight: stop` line: WI-963 and
WI-940 both move without the owner.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** WI-962 landed as `141657bb0` (the hooks read the policy file
  through one parse; sitting 003 blessed SR-031, LLR-021, LLR-031, TC-021
  and TC-031, act seq 144 taken in the lane); its re-mint WI-965 closed as
  already settled (`fd535dc56`); WI-966 filed (`592951e8b`: the policy
  file's line-shape rule retirement, carrying the sites and findings
  wi-962 D-004 (c) and D-007 routed there; its scope critique runs before
  its claim); WI-963's and WI-940's scope critiques answered and confirmed
  (`af9eb31d4`; coordinator-2026-10-21 D-001 to D-003); the pause deleted
  (`b3821d0d9`), both rows claimed, and the pause restored byte-identical
  (`7f8e57192`). `archive/lanes` holds wi-962's tips (`0dfc3dfce`). The
  full suite ran once at `7f8e57192`: 6811 passed, 32 skipped (891 s).
- **Lane `wi-963`** (worktree `C:/Projects/ai-template.wt/wi-963`, base
  `7f8e57192`, tip `411de18f0`): plan, two critiques, pass record; Terra's
  intent set `37ce6cd17` (LLR-342 and TC-373 Drafted, LLR-153 and LLR-158
  amended by addition, IF-091's data widened); the tests first
  `004f88249`; the code `36e0c8e6b`; counted round 1 filed
  (`001-REVIEW-A-36e0c8e`, `002-REVIEW-B-36e0c8e`, all MINOR, `411de18f0`).
  **Next:** the small pre-checkpoint builder stage wi-963 D-005 (b) to (d)
  names (a routed-traced test case and its contrast; the refusal's recovery
  wording at every site; the two consolidation MINORs inside the lane's
  surface), then the checkpoint: Terra's reconcile (TC-373's tier to Full,
  LLR-342's recovery wording; the change list is
  `wi-963-spine-changes.md` under the leg's scratch root), the closure
  check, one combined sitting, the gate in convergence stance after the
  convergence map, the rebase, the act turn, the landing. Terra's session
  id is in the intent turn's log (`terra-963.log` under the scratch root);
  record it in wi-963's decisions at the next turn.
- **Lane `wi-940`** (worktree `C:/Projects/ai-template.wt/wi-940`, base
  `7f8e57192`, tip `fa1aecde8`): plan, two critiques, pass record; the
  move with IF-302 (Drafted) and LLR-026's traced cells `cf3d01417`
  (wi-940 D-002, D-003); the conftest's shared prototypes and the private
  job input `fa1aecde8` (P2 only). **Next:** the plan's P3 to P6 (the CPU
  meter, the keys and their stamped values, the audit's smoke part, the
  warn mode for both bars and for `[step:smoke]` and the CI job per
  coordinator-2026-10-21 D-001), each a stage committed alone; then
  counted round 1. The plan holds the lane for the owner if the stamping
  readings spread wider than 1.5x or the WSL reading exceeds the budget.
  IF-302's data and notes cells go to the checkpoint's reconcile
  (`wi-940-spine-changes.md`). Terra's session id is in `terra-940.log`.
- **Lane `wi-957`**: unchanged (tip `804c8011c`); after WI-940 lands,
  rebase, re-anchor its RESYNC entry, the empty attestation commit, counted
  round 1.
- **Watermark** on trunk: WI 966; SR 240, LLR 340, IF 298, TC 370, OI 114;
  acts to seq 144. Lane-held ids: wi-957 holds SR-241, LLR-341, TC-371 and
  TC-372; wi-963 holds LLR-342 and TC-373; wi-940 holds IF-299 to IF-302
  (it minted IF-302; IF-299 to IF-301 are spent by its floor, record them
  at its landing, never retire them). A later lane's Terra takes these as
  its floor.
- **Strict lints:** clean on trunk and in both lanes.
- **No judgement is active**; the lease is handed back at close-out.
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-21-leg07/`
  (briefs, verdicts, spine change lists, Terra logs, bar logs); keep it
  until both lanes land. The 2026-10-20e scratch root is kept as before.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say: two full-lane
reviewers per round, Codex Sol at medium (REVIEW-A) and Claude Opus at high
(REVIEW-B, launched with the Agent tool's `effort: "high"`), each given
only its rendered brief.

## The queue

The owner's order (coordinator-2026-10-16 D-004, D-006; coordinator-2026-10-17
D-002, D-008), turned toward headless runs (coordinator-2026-10-18 D-004,
D-006), with the owner's 2026-10-20 rulings (coordinator-2026-10-20 D-008 to
D-019). Each row that changes machinery lands alone, after the cycle has
run through the last landing's changed steps.

**Only the rows in this table are claimed**, in order and under their
`needs`. When no row in it can move without the owner, the leg closes out
with the `Overnight: stop` line.

| # | Row | Next |
|---|---|---|
| 1 | WI-963 | In its lane: the pre-checkpoint stage, the checkpoint, the gate, the landing. Touches `intake.py`; lands alone |
| 2 | WI-940 | In its lane: P3 to P6, then the rounds. Changes both bars' budget step; lands alone, after WI-963 lands and the cycle has run a landing through it, and releases WI-957 |
| 3 | WI-953 | WI-902's disposition sitting on the owner's route (D-008): compose the `disposition` brief, then append the row's `## Owner route` section verbatim, chained with `&&` (recipes section 1, Adjudication step 1), and check the brief carries it. Then the successor it drafts: the third plan revision, one confirming critique, the build, before P4 and P5 |
| 4 | WI-957 | After WI-940 lands: rebase onto trunk, re-anchor its RESYNC entry, the empty attestation commit, counted round 1 |
| 5 | WI-958 | After WI-957 lands (hard edge) |
| 6 | WI-960, then WI-961 | Cleared for a claim; built after WI-957 lands (WI-960's soft edge: the same review steps) |
| 7 | WI-850, WI-851, WI-856, WI-878, WI-910, WI-920 | Under their `needs`, each scope-critiqued at its claim (WI-910 as split by D-019) |
| 8 | Filings P3 to P6, P8 | P3 ends in an owner act; P4 and P5 after WI-953's successor lands (P5's spec asks D-009's question: does the WI space ride the carrier, and folds in WI-810's "sequential sittings never collide on an id"); P6 starts with the W3 dry run; P8 waits on its filing calls |
| 9 | WI-966 | Filed this leg: scope critique and its confirming round, then claim; it lands before item 10 step 5 |

**Never claimed by a leg:** WI-684 (waits on OI-98, the owner's re-sync),
WI-795 (OI-105, then WI-820), WI-908 (the owner present), WI-964 (the
owner's Mac), WI-827 (attended only; it never lands from a lane), and every
row under `docs/work/deferred/` (D-011, D-016).

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).

## For the owner

- **Confirm or overrule** coordinator-2026-10-21 D-001 (high risk:
  WI-940's other two enforce callers, the stage bar's `[step:smoke]` and
  CI's `smoke-budget` job, move to warn mode under your "no bar fails on
  seconds"; the alternative is the audit's smoke part in the CI job),
  D-002 and D-003; wi-962 D-001 to D-007; wi-963 D-001 to D-006; wi-940
  D-001 to D-004.
- **WI-966's place in the queue:** filed at row 9; it is the deletion row
  WI-962's spec split off, before item 10 step 5.
- **Still open from the last handoff:** review the deferred rows'
  re-scopes (D-016; WI-809 and P4 gate the managed loop's unpause); your
  owner-held rows (WI-827, WI-908, WI-964, and WI-684 and WI-795 behind
  their open items); confirm or overrule coordinator-2026-10-20 D-012,
  D-013 and D-020 (high risk: WI-963's Trust ruling, whose text WI-963's
  revised spec keeps); P8's filing calls; coordinator-2026-10-20 D-001 to
  D-007 (high risk D-002, D-005, D-006); wi-957 D-001 to D-004; wi-955
  D-001 to D-006; wi-956 D-001 to D-010; the named-tests `--basetemp`,
  SR-227's wording, and the lists before them.
- **Push** `refactor_again` and `archive/lanes`.

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator, running ATTENDED in an interactive
session with the owner. Ask the owner at real decision points; record every
other call in docs/decisions/. Background tasks and notifications are fine
here (this is not a headless leg).

1. Take the lease FIRST, with your transcript so occupancy is readable:
   `python project-trajectory/scripts/coordinator_guard.py take --transcript "$(ls ~/.claude/projects/*/$CLAUDE_CODE_SESSION_ID.jsonl | head -1)"`.
   If the take is refused, report why and stop.
2. Read, in order: CLAUDE.md; docs/status.md; the newest handoff (the one
   status.md's RESUME HERE names), all of it; the Status and every "Owner
   rulings" section of docs/plans/2026-10-11-review-churn/README.md
   (2026-10-11 through revision 37) and its pointer-rules.md; the
   coordinator-cycle skill and its references/recipes.md;
   your memory index (review-churn-program-rulings first).
3. Run reviews the way the handoff's "How to run reviews now" says. It
   overrides the skill where they differ, until batch row B1 lands and the
   skill says the same.
4. Work the handoff's queue table in order: the "pre" trunk fix and the
   baseline manifest (M); file and
   land B1, then the plan gate G, then B2–B4 (B4 is WI-902's reshape), each
   filed on trunk with its scope critique and dispositions first; then
   continue WI-798; then P1–P9 under the dependencies their rows name; then
   re-order leg 03's rows against the plan with the owner. Claim under
   one scoped unpause per batch (a reviewed deletion commit, the claims, a
   byte-identical restore). Cut lanes from trunk's tip and land them one at a
   time. Roles: Claude Opus builds (kit-builder agent, medium); GPT Terra
   (medium) authors spine text in one retained session per lane; Codex Sol
   (medium) and Claude Opus (high) review in parallel (coordinator-2026-10-16
   D-008; the handoff's "How to run reviews now"); the independent adjudicator
   judges spine text and disputes through coordinator_adjudicate.py from the
   lane (set AGENT_CLAUDE_TOKEN_FILE to the token file's path from memory
   first; never read the file), never a sub-agent.
5. Before each landing commit: regenerate the views, run the smoke bar and its
   budget, run trace.py --strict and check_trajectory.py --strict, and read
   the summaries for failures.
6. Close out when `coordinator_guard.py status` reads 40% or more, at the
   latch, or when the owner says so (session-protocol section 4): land or
   safely commit every lane; update docs/status.md (forward-only); write a NEW
   handoff whose `## Session prompt (paste to start the next session)` block is
   this prompt, copied verbatim, keeping the `Overnight: stop` line unless the
   owner asks for headless legs; write a log fragment; fold procedural lessons
   into the coordinator-cycle skill; run the full suite once if code changed;
   commit; then `coordinator_guard.py handback --handoff <the new handoff>`.

Never: push or merge to main; rule an open item or sign an owner-held act;
leave docs/work/pause deleted; read OWNER_SCRATCHPAD.md or the adjudicator's
token file; self-review or adjudicate through a sub-agent; change ~/.claude
settings or install software; bypass a commit hook.
```
