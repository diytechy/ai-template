# Handoff 2026-10-22b (headless leg 12): WI-960 landed

It replaces [handoff-2026-10-22a-leg11-coordinator.md](handoff-2026-10-22a-leg11-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 12 (loop session
`20261021T045653Z-213020`) settled wi-960 D-005's open point in the lane,
built WI-960's P4 to P7, ran its two counted rounds, one fix round, the
checkpoint (two sittings), the gate and the act turn, landed it, and closed
its re-mint. It carries no `Overnight: stop` line: the next rows move
without the owner.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** WI-960 landed as `a7fec6dd9` (act seq 151: LLR-269, TC-265,
  LLR-270, TC-268 re-attested; act seq 152: SR-243, LLR-346, TC-384,
  TC-385 approved). Every Sol and Terra call now goes through
  `scripts/coordinator/codex_call.py` on the session service (roles
  `REVIEW-A`, `CRITIQUE`, `AUTHOR`; `--resume` reads the lane's newest
  committed `AUTHOR` log); a call outside a claimed lane spools its log
  under the primary checkout's `out/sessions/spool/` and commits nothing.
  `sol_review.sh`, `terra_author.sh`, `luna_review.sh` and `layout.sh`
  are gone. Its re-mint WI-972 closed as already settled (`5328a8933`).
  `archive/lanes` holds WI-960's rebased and pre-rebase tips. The full
  suite ran once at `5328a8933`: 7127 passed, 33 skipped (1986 s).
- **The route is machinery the cycle runs on:** this leg's own rounds and
  Terra turns ran through the lane's copy, and the next lane's reviews are
  the first through trunk's. A defect is fixed forward in a lane; where it
  blocks the fix's own review, that one launch runs by hand, attended and
  recorded (the WI-960 spec's "Machinery landing alone").
- **Spooled logs** (one so far, WI-850's scope critique) are machine-local
  until WI-800's harvest lands; this repository ignores all of `out/`.
- **WI-850's scope critique** ran from the detached `trunk-tmp` checkout
  at `c06a7e101` through the route (its log spooled): CHANGES-REQUESTED
  findings=3, kept at
  `C:/Projects/ai-template.wt/review-tmp/2026-10-21-leg11/l12-crit850/WI-850-scope-critique.md`.
  Its dispositions go into WI-850's spec on trunk, then the confirming
  round, before its claim.
- **Lane `wi-963`:** unchanged, holds for the owner (OI-115). It holds
  LLR-342 and TC-373.
- **Watermark** on trunk: WI 972, SR 243, LLR 346, IF 304, TC 385, OI 115;
  acts to seq 152. Lane-held: wi-963 LLR-342, TC-373. The next lane's
  Terra floor is SR-244, LLR-347, TC-386, IF-305.
- **Strict lints:** clean on trunk. **No judgement is active**;
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-21-leg11/`
  (keep the WI-850 critique; the rest may go once read); the leg-07 root
  stays until WI-963 lands.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say, through the route:
two full-lane reviewers per round, Codex Sol at medium (REVIEW-A,
`codex_call.py REVIEW-A`) and Claude Opus at high (REVIEW-B, launched with
the Agent tool's `effort: "high"`), each given only its rendered brief. In
a headless leg launch REVIEW-B first: the harness runs two launches one
after the other, and REVIEW-A's call commits its log in the lane when it
returns. Every render refuses a tip with no attested review bar for its
`--tests`: attest the tip first.

## The queue

The owner's order (coordinator-2026-10-16 D-004, D-006; coordinator-2026-10-17
D-002, D-008), turned toward headless runs (coordinator-2026-10-18 D-004,
D-006), with the owner's 2026-10-20 rulings (coordinator-2026-10-20 D-008 to
D-019) and coordinator-2026-10-21 D-004 to D-006. Each row that changes
machinery lands alone, after the cycle has run through the last landing's
changed steps (WI-960 changed the coordinator's codex launch route and the
session service's record).

**Only the rows in this table are claimed**, in order and under their
`needs`. When no row in it can move without the owner, the leg closes out
with the `Overnight: stop` line.

| # | Row | Next |
|---|---|---|
| 1 | WI-961 | Its `needs` (WI-960) is met: scope critique at its claim (a row born before S3 to S6 is re-critiqued), then plan and build. It counts nested agents (revision 37) |
| 2 | WI-963 | Held: OI-115 (the owner) |
| 3 | WI-850, WI-851, WI-856, WI-878, WI-910, WI-920 | Under their `needs`, each scope-critiqued at its claim (WI-910 as split by D-019). WI-850's critique is done (above): its dispositions and confirming round come first |
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
- **Decide** whether a `--wi` worker preflight refuses the primary
  checkout: since WI-960, a worker there, even on its claimed branch,
  spools its BUILD, ATTEST and REVIEW logs, so the loop's committed-evidence
  readers (the red cap, the logged rounds, the session numbering) see none
  (wi-960 D-016, 008 F2; the managed loop is paused, so nothing reaches it
  today).
- **The temporary `Bash(codex exec *)` allow rule** in
  `.claude/settings.local.json`: no recipe launches `codex exec` from the
  shell any more (the route launches it through the session service).
  Remove it when you choose.
- **Confirm or overrule:**
  - wi-960 D-006 (the spool's gitignore line built in the lane, not as its
    own row), D-009 (the spec's Trust ruling restated to the code's rule:
    an unreadable claim read adds no claim), D-012 (Terra's checkpoint
    turn fresh through the route; two evidence cells it narrowed
    restored), and D-001 to D-016 otherwise;
  - and every item the last handoff listed: wi-969 D-001 to D-027 (D-001's
    mint gap, D-020, D-022, D-027), wi-958 D-001 to D-019 (D-008 high
    risk), coordinator-2026-10-21 D-001 to D-006, wi-957 D-005 to D-014,
    wi-940 D-001 to D-011 (D-009 high risk), wi-963 D-001 to D-011,
    wi-962 D-001 to D-007.
- **Still open from the last handoff:**
  - review the deferred rows' re-scopes (D-016; WI-809 and P4 gate the
    managed loop's unpause);
  - your owner-held rows: WI-827, WI-908, WI-964, and WI-684 and WI-795
    behind their open items;
  - confirm or overrule coordinator-2026-10-20 D-012, D-013 and D-020, and
    D-001 to D-007 (high risk: D-002, D-005, D-006);
  - P8's filing calls; wi-955 D-001 to D-006; wi-956 D-001 to D-010;
  - the named-tests `--basetemp`, SR-227's wording, and the lists before
    them.
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
