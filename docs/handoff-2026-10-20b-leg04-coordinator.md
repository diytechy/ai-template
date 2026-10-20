# Handoff 2026-10-20b (headless leg 04): WI-798 landed

It replaces [handoff-2026-10-20a-leg03-coordinator.md](handoff-2026-10-20a-leg03-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. This was the fourth headless leg
under WI-946's launcher (loop session `20261019T185432Z-8e4f05`). It
rebased WI-798's lane 245 commits onto trunk, ran its three counted rounds,
the cap's dispute sitting, the checkpoint and the gate, and landed it. Like
the last handoff, it carries no `Overnight: stop` line: the phase-1 rows
move without the owner.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** `2c8ff804e` lands WI-798 (squash of wi-798); `c44d0bd29` is
  the sweep's mint of WI-954, its re-mint, and `e779b328c` closes WI-954 as
  already settled (sitting 017, acts 141 and 142). The close-out commit
  follows. `archive/lanes` is at `8ca84f1fc`: WI-798's rebased tip
  `918276180` and its pre-rebase tip `9437d0a1f`, which verdicts 001 to 004
  cite.
- **What WI-798's landing changes for every later session:**
  `coordinator_adjudicate.py`'s default entry is
  `ANTHROPIC-OPUS-STRONG@ADJUDICATOR`, a declared token account, for the
  sitting and the act turn alike; `signin` prints
  `signin [ADJUDICATOR] token: <status>`. `AGENT_CLAUDE_TOKEN_FILE` is still
  the variable to set. A qualified entry launches under its account's own
  home or token, with competing ambient credentials withheld; a qualified
  OpenCode entry composes from a declared base environment. The landing
  changes machinery the cycle runs on: the next sitting and act turn run
  through it, and the next machinery landing may follow them.
- **Lanes:** none open. The landed lanes' branches and worktrees remain
  (`wi-798` among them, archived).
- **Watermark** on trunk: WI 954; SR 240, LLR 340, IF 297, TC 370, OI 114;
  acts to seq 142 (WI-798's re-attest and first approval).
- **Strict lints:** clean on trunk.
- **Tests this leg:** the full unfiltered suite at `e779b328c`, from a
  detached scratch checkout: 6658 passed, 28 skipped, 0 failed (23 min 12
  s). WI-798's landing bar on the staged squash: 2963 passed, every lint
  green, the tier 96.6 s against its parent's 100.0 s on the same loaded
  box, both over the 60 s budget (owner, 2026-10-17).
- **No judgement is active**; the lease is handed back at close-out.
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-20-leg04/`
  holds this leg's briefs, verdicts, plans and bar logs. Nothing in it is
  owed, and it may be deleted, as may the 2026-10-19e root.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say: two full-lane
reviewers per round, Codex Sol at medium (REVIEW-A) and Claude Opus at high
(REVIEW-B, launched with the Agent tool's `effort: "high"`), each given
only its rendered brief.

## The queue

The owner's order (coordinator-2026-10-16 D-004, D-006; coordinator-2026-10-17
D-002, D-008), turned toward headless runs (coordinator-2026-10-18 D-004,
D-006). Each row that changes machinery lands alone, after the cycle has
run through the last landing's changed steps.

| # | Row | Next |
|---|---|---|
| 1 | WI-953 | WI-902's disposition, after the owner routes the plan cap's FIX (below) |
| 2 onward | As before | P1 to P8, then leg 03's rows; WI-940 after the batch |

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).
Row 1 waits on the owner, so a leg starts at row 2: its first row is
scope-critiqued, then claimed under one scoped unpause.

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Route WI-902's plan-cap FIX** (wi-902 D-011): a third plan revision
  that takes sitting 016's ruling, or another route. WI-953, its
  disposition row, waits on that choice.
- **Confirm or overrule:** wi-798 D-010 to D-024. The riskiest: D-010, the
  act turn runs under the declared account (a path the spec did not name,
  met at the rebase); D-015, a qualified OpenCode launch composes from a
  declared base environment, so a route that relied on an undeclared
  ambient variable must now declare it; D-018, the provisioning hint is
  prose with no shell syntax; D-021, the review owed after the cap's fix
  round was taken as the gate over the checkpoint tip; and D-023, one
  whole-set sitting authorized the act after three split re-sits. Also
  the earlier lists: wi-897 D-001 to D-007, wi-902 D-011,
  coordinator-2026-10-19 D-003 and D-004, and the ones before them.
- **SR-227's wording:** it still binds its credential and sign-in clause to
  "a family that uses a dedicated CLI home", which no family has now; its
  account-level children (LLR-270, LLR-305, LLR-336) are approved. The
  wording is yours, at its next amendment.
- **Optional:** to take the new guard matcher on this workstation, remove
  the guard groups from `.claude/settings.local.json` and run the consented
  install again.
- **Still open from earlier handoffs:** the convergence-tag question; the
  `wi-880` worktree's uncommitted hook edit; the old `coordinator-tools`
  folder; OI-98, OI-105 and OI-114, each waiting on its condition.

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
