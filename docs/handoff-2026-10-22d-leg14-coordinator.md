# Handoff 2026-10-22d (headless leg 14): WI-961 landed, WI-850 ready to claim

It replaces [handoff-2026-10-22c-leg13-coordinator.md](handoff-2026-10-22c-leg13-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 14 (loop session
`20261021T045653Z-213020`, coordinator session
`67c35148-be64-47e7-8265-d07c5131bd3f`) took WI-961 through its checkpoint,
three sittings, the gate and the act, and landed it alone; it then answered
WI-850's scope critique on trunk and ran its confirming round, which passed.
It carries no `Overnight: stop` line: the next rows move without the owner.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** WI-961 landed as `775290553` (act seq 153), then WI-850's
  critique answers (`deaff29ec`) and this close-out. The full suite ran
  once at `deaff29ec`: 7199 passed, 33 skipped in 18:51.
- **WI-961 is closed.** Its spec is archived
  (`docs/archive/work/complete/WI-961-subagent-usage-ingest.md`), its lane
  tips are in `archive/lanes`, the sweep minted nothing, and the registries
  equal their anchors. Its worktree `C:/Projects/ai-template.wt/wi-961`
  and branch remain; nothing reads them. As a machinery change, its step
  ran once: this close-out's usage ingest recorded this session and its six
  sub-agents, and leg 13's session whole; each run exited 0 in about 1.5 s
  over 41 worktrees (D-009's owed measure). From now on each close-out runs
  the pair the skill's sections 6 and 7 name; this session's id is
  `67c35148-be64-47e7-8265-d07c5131bd3f`, so the next close-out passes it
  as `--session` to record this leg's tail.
- **WI-850 is ready to claim.** Its leg-12 critique is answered on trunk
  (a Trust section, `planmode = "single"`, the dispositions;
  coordinator-2026-10-22 D-002), and its confirming round read APPROVE
  findings=0 (D-003). Claim it under one scoped unpause; its single plan
  runs first in the lane. Its first Done-when act settles SR-224's chain
  (LLR-281 and TC-291 approved under a Drafted SR-224) on a released rung.
  The plan settles where the shared two-tree reader lands (WI-963's held
  lane adds one), the in-lane skill line on a parent "approved for its
  current text", and the advisory it retires.
- **Lane `wi-963`:** unchanged, holds for the owner (OI-115). It holds
  LLR-342 and TC-373.
- **Watermark** on trunk: WI 972, SR 244, LLR 356, IF 307, TC 395, OI 115;
  acts to seq 153.
  - Lane-held: wi-963 LLR-342 and TC-373.
  - A new lane's Terra floor is SR-245, LLR-357, TC-396 and IF-308.
- **Spooled logs:** WI-850's two critiques (legs 12 and 14) and this
  close-out's usage ingest.
- **Strict lints:** clean on trunk. **No judgement is active**;
  `docs/work/pause` is tracked and unchanged.
- **Scratch:**
  - Keep `C:/Projects/ai-template.wt/review-tmp/2026-10-22d-leg14/`
    until WI-850 lands: its Trust draft (`wi850-trust-draft.md`, with the
    planner's notes) and its confirming verdict (`crit850c/`).
  - `C:/Projects/ai-template.wt/review-tmp/2026-10-22c-leg13/` may go:
    WI-961's results are recorded.
  - Keep `C:/Projects/ai-template.wt/review-tmp/2026-10-21-leg11/` for
    WI-850's first critique, and the leg-07 root until WI-963 lands.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say, through the route:

- Two full-lane reviewers run per round: Codex Sol at medium (REVIEW-A,
  `codex_call.py REVIEW-A`) and Claude Opus at high (REVIEW-B, launched
  with the Agent tool's `effort: "high"`). Each gets only its rendered
  brief.
- In a headless leg, launch REVIEW-B first.
- Every render refuses a tip with no attested review bar for its
  `--tests`, so attest the tip first.

## The queue

The owner's order (coordinator-2026-10-16 D-004, D-006; coordinator-2026-10-17
D-002, D-008), turned toward headless runs (coordinator-2026-10-18 D-004,
D-006), with the owner's 2026-10-20 rulings (coordinator-2026-10-20 D-008 to
D-019) and coordinator-2026-10-21 D-004 to D-006. Each row that changes
machinery lands alone, after the cycle has run through the last landing's
changed steps (WI-961 changed the close-out: its ingest ran at this
close-out).

**Only the rows in this table are claimed**, in order and under their
`needs`. When no row in it can move without the owner, the leg closes out
with the `Overnight: stop` line.

| # | Row | Next |
|---|---|---|
| 1 | WI-850 | Claim under one scoped unpause; the single plan, then intent, tests, code, rounds, checkpoint, gate, act and landing. Its first act settles SR-224's chain |
| 2 | WI-963 | Held: OI-115 (the owner) |
| 3 | WI-851, WI-856, WI-878, WI-910, WI-920 | Under their `needs`, each scope-critiqued at its claim (WI-910 as split by D-019) |
| 4 | Filings P3 to P6, P8 | P3 ends in an owner act. P4 and P5 may file; P5's spec asks D-009's question (does the WI space ride the carrier?) and folds in WI-810's "sequential sittings never collide on an id". P6 starts with the W3 dry run. P8 waits on its filing calls |
| 5 | WI-966 | Scope critique and its confirming round, then the claim; it lands before item 10 step 5 |
| 6 | WI-971 | Scope critique at its claim; it touches the hook and slot walk WI-969 added, so it lands alone |

**Never claimed by a leg:** WI-684 (waits on OI-98, the owner's re-sync),
WI-795 (OI-105, then WI-820), WI-908 (the owner present), WI-964 (the
owner's Mac), WI-827 (attended only; it never lands from a lane), WI-967
(OI-115's placeholder), and every row under `docs/work/deferred/` (D-011,
D-016).

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).

## For the owner

- **Rule OI-115** (WI-963's settlement fix; recommendation (a)). It holds
  WI-963 at its gate tip.
- **Confirm or overrule:**
  - coordinator-2026-10-22 D-002 (high risk): WI-850's Done-when now reads
    "a TC for every SR and LLR it verifies" (an IF row it cites is no
    parent; counting IF rows would make 114 approved TCs standing
    findings), and its standing finding stays an integrity finding, as
    the Done-when states (the planner's option a; option b would make it
    `--strict` only);
  - coordinator-2026-10-22 D-003 (WI-850's confirming round);
  - wi-961 D-010 to D-017, in particular:
    - D-011: after the counted rounds, an arms map found 25 coverage
      gaps, and a builder stage added characterization tests before the
      sitting (no code change);
    - D-012, D-013 and D-015: the coordinator's byte-exact row-text edits
      before the sittings (TC-390's link, TC-394's home sentence, three
      clauses, LLR-355's two phrasings and IF-306's data), each judged by
      the next sitting;
    - D-017: the gate's five MINORs went to status.md's follow-ups.
  - the earlier D-001 (WI-961 claimed on its standing critique) and wi-961
    D-001 to D-009, from the last handoff.
- **Still open from the last handoff**, every item it listed:
  - the `--wi` primary-checkout preflight call (wi-960 D-016);
  - removing the temporary `Bash(codex exec *)` allow rule;
  - wi-960 D-001 to D-016;
  - the earlier lists that handoff carried forward;
  - your owner-held rows.
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
