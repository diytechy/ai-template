# Handoff 2026-10-24a (headless leg 17): WI-856 landed

It replaces [handoff-2026-10-23b-leg16-coordinator.md](handoff-2026-10-23b-leg16-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 17 (loop session
`20261024T053017Z-23122f`, coordinator session
`c7ff479b-0c16-437a-b229-9e2eae7bb6ca`) re-critiqued WI-856 at its claim,
answered the critique in its spec, claimed it alone, built, reviewed and
judged it, and landed it alone. It carries no `Overnight: stop` line: the
next rows move without the owner.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** the owner's two scope-critique commits (`202a7bb96`,
  `aa1215540`), WI-856's spec revision (`5bc5dd7cc`), the scoped unpause
  (`f535c9212`), the claim (`96faaeeda`) and the byte-identical restore
  (`3b9f2b44f`), then WI-856's landing (`b65b30462`, act seq 158), the
  sweep's re-mint WI-974 (`11ee1b42e`) closed as settled (`fb165bd0f`),
  then this close-out. The full suite's result at this close-out is in
  the close-out commit's message.
- **WI-856 is closed.** Its spec is archived
  (`docs/archive/work/complete/WI-856-edge-a-row-with-no-needs.md`), its
  lane tip is in `archive/lanes`, and the four spine registries equal
  their anchors. Its worktree `C:/Projects/ai-template.wt/wi-856` and
  branch remain; nothing reads them. The step it changed (the
  consolidation close's queue-with-edge transform) is not a step of the
  per-lane cycle, so it holds no later landing (coordinator-2026-10-24
  D-003).
- **Lane `wi-963`:** unchanged, holds for the owner (OI-115). It holds
  LLR-342 and TC-373; recount `acceptance_record.py`'s size at its rebase
  (the last handoff's note stands).
- **Watermark** on trunk: WI 974, SR 246, LLR 359, IF 308, TC 398, OI 115;
  acts to seq 158.
  - Lane-held: wi-963 LLR-342 and TC-373.
  - A new lane's Terra floor is SR-247, LLR-360, TC-399 and IF-309.
- **Smoke ceiling:** `max-tests` is 3410 (WI-856's re-stamp; the tier
  counts 3282).
- **Usage:** this close-out's ingest recorded this session and its
  sub-agents, and leg 16's tail (its exits are in the close-out commit's
  message). The next close-out passes
  `--session c7ff479b-0c16-437a-b229-9e2eae7bb6ca`.
- **Strict lints:** clean on trunk. **No judgement is active**;
  `docs/work/pause` is tracked and unchanged.
- **The box:** another project's speech-synthesis jobs loaded this
  workstation through the leg (smoke bars 2:43 to 60 minutes; four
  timing-bound smoke cases and one unnamed attest red were load-sensitive,
  filed under status.md's follow-ups). Give every bar the whole cap.
- **Scratch:**
  - `C:/Projects/ai-template.wt/review-tmp/2026-10-24a-leg17/` may go once
    read: WI-856's results are recorded (its critiques, builder notes,
    arms map and bar logs are there if wanted).
  - `2026-10-23a-leg16/`, `2026-10-22e-leg15/`, `2026-10-22d-leg14/` and
    `2026-10-21-leg11/` may go.
  - Keep the leg-07 root until WI-963 lands.

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
D-019), coordinator-2026-10-21 D-004 to D-006, and the owner's 2026-10-23
direction that a scope critique settles a row's scope and never grows it
(the rubric's S7). Each row that changes machinery lands alone, after the
cycle has run through the last landing's changed steps.

**Only the rows in this table are claimed**, in order and under their
`needs`. When no row in it can move without the owner, the leg closes out
with the `Overnight: stop` line.

| # | Row | Next |
|---|---|---|
| 1 | WI-963 | Held: OI-115 (the owner); recount its module size at the rebase |
| 2 | WI-878, WI-910, WI-920 | Under their `needs`, each scope-critiqued at its claim (WI-910 as split by D-019); WI-878 (a dispute sitting's binding records the findings file it ruled) is next, and likely owes a Trust section (the coverage gate reads the file) |
| 3 | Filings P3 to P6, P8 | P3 ends in an owner act. P4 and P5 may file; P5's spec asks D-009's question (does the WI space ride the carrier?) and folds in WI-810's "sequential sittings never collide on an id". P6 starts with the W3 dry run. P8 waits on its filing calls |
| 4 | WI-966 | Scope critique and its confirming round, then the claim; it lands before item 10 step 5 |
| 5 | WI-971 | Scope critique at its claim; it touches the hook and slot walk WI-969 added, so it lands alone |

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
  - coordinator-2026-10-24 D-001 and D-002 (WI-856's scope critique and
    its claim alone) and D-003 (WI-856's changed step holds no later
    landing);
  - wi-856 D-001 to D-006, notably D-001 (the intent set and the tests in
    one commit before the code), D-002 (the smoke ceiling 3280 to 3410)
    and D-003 (round 1's MINORs fixed in a pre-checkpoint stage, one
    consolidation not adopted).
- **Still open from the last handoff**, every item it listed:
  - coordinator-2026-10-23 D-001 to D-005 (D-002 and D-004 high risk) and
    wi-851 D-001 to D-014;
  - coordinator-2026-10-22 D-004, wi-850 D-001 to D-012 (D-002 high
    risk), coordinator-2026-10-22 D-002 and D-003, wi-961 D-010 to D-017
    and the earlier items those handoffs carried;
  - the `--wi` primary-checkout preflight call (wi-960 D-016);
  - removing the temporary `Bash(codex exec *)` allow rule;
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
