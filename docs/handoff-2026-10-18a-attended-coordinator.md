# Handoff 2026-10-18a (attended): WI-917 landed; seven lanes planned, three built

Overnight: stop

It replaces [handoff-2026-10-17e-attended-coordinator.md](handoff-2026-10-17e-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **Landed this session:** WI-917 (a headless coordinator leg is a marked
  autonomous run, every commit carrying its `Loop-Session` trailer) as
  `396ff9f44`, after counted round 1 (Sol APPROVE 0; Opus APPROVE 3 MINOR)
  and the gate in convergence stance (Sol APPROVE 0; Opus APPROVE 1 MINOR,
  round 1's F1 again). No sitting was owed. Tips archived (`cbf3cf3c1`);
  the sweep minted nothing. Its MINORs are status.md's unfiled follow-ups,
  two of them to weigh before the first headless run, which stays the
  owner's call (coordinator-2026-10-18 D-001: the attended cycle runs
  nothing WI-917 changed, so no later landing waits on it).
- **Claimed this session** under the second scoped unpause (`d4347c821`,
  restored byte-identical at `f4c33e461`): WI-942 and WI-943
  (coordinator-2026-10-17 D-008).
- **Lanes** (each `single`; plans by fresh Claude Opus planners, critiques
  by Codex Sol at medium, every record committed alone behind its bar):
  - `wi-916`, cut at `6533a2331`: planned and passed (critique 1 APPROVE
    0); build round 1 committed (`f881d233d`: `scripts/check_resync.py`
    wired into `[run] smoke`); counted round 1 filed (`65d2962bc`: Sol
    APPROVE 0; Opus CHANGES-REQUESTED, 2 MINOR). Next: wi-916 D-002's open
    triage of F1 (a re-anchored base entry counts as new, against
    deliverable 1's text): a Done-when gap and a fix round with F2's
    wording, or a MINOR for the follow-ups. It owes no spine rows.
  - `wi-942`, cut at `396ff9f44`: planned and passed (critique 1 APPROVE
    0); build round 1 (P1, P2, P3, P5) committed (`0bfb35933`), with
    LLR-278's `code_symbol` and TC-278's evidence kept current (wi-942
    D-001). Next: Terra's intent
    turn for P4 (LLR-278 detail, TC-278 method and expected), counted
    round 1, the checkpoint sitting, the gate, the act turn, landing. It
    lands before plan item 14's retirement lane.
  - `wi-943`, cut at `396ff9f44`: planned and passed (critique 1 APPROVE
    0, pass `9b168865a`). Its build waits for WI-942's landing
    (coordinator-2026-10-18 D-002).
  - `wi-915`, cut at `6533a2331`: critique 1 one MAJOR, the one revision,
    critique 2 APPROVE 0 (pass `3b8315008`); build stage 1 committed
    (`1699ccf82`, the characterization grid). Next: a fresh builder for
    stage 2, P2 to P9 as one refactor commit with P8's re-stamps inside it
    (wi-915 D-001).
  - `wi-927`, cut at `6533a2331`: critique 1 one MAJOR, the revision,
    critique 2 APPROVE 0 (pass `56d92994a`). Next: build round 1.
  - `wi-925` and `wi-926`, cut at `6533a2331`: each at the plan cap, its
    second critique CHANGES-REQUESTED with one MAJOR (`5f3e73bfb`,
    `87404bd10`). Next: one dispute sitting each (coordinator-2026-10-18
    D-003; recipes section 1, "Single plan", step 7); anything but an
    accepted DISMISS goes to the owner and the lane closes partial.
  - Unchanged: WI-798, WI-902, and the landed lanes' branches and
    worktrees (`wi-917`'s included).
- **Watermark** on trunk: WI 944; SR 239, LLR 338, IF 296, TC 368, OI 114;
  acts to seq 128.
- **Strict lints:** clean on trunk and on every lane commit this session.
  The smoke budget read OVER on every commit (69 to 346 s, the box loaded
  by up to five planners, five critics, two reviewers, builders and the
  full suite); every code-changing commit took a same-window pair, each
  reading the parent as high or higher except WI-915's stage 1, whose
  module sits outside the tier.
- **Full suite** at trunk's `396ff9f44`: 6137 passed, 22 skipped, 0 failed
  (42 min 23 s, beside lane bars and reviewers); 50 more than 2026-10-17e's
  6087, WI-917's two new test modules.
- **No judgement is active**; the lease is handed back at close-out.
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-18a/` may be
  deleted once the owner has read this handoff; nothing in it is owed.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say: two full-lane
reviewers per round, Codex Sol at medium (REVIEW-A) and Claude Opus at high
(REVIEW-B, launched with the Agent tool's `effort: "high"`), each given
only its rendered brief.

## The queue

The owner's order (coordinator-2026-10-16 D-004, D-006; coordinator-2026-10-17
D-002, D-008). Each row changes machinery, so each lands alone.

| # | Row | Next |
|---|---|---|
| 1 | WI-916 | Triage F1 (wi-916 D-002), then the fix round or the gate; land |
| 2 | WI-942 | Terra's intent turn, counted round 1, checkpoint sitting, gate, act, land |
| 3 | WI-915 | Stage 2 build, then rounds |
| 4 | WI-927 | Build round 1, then rounds |
| 5 | WI-925, WI-926 | One dispute sitting each at the plan cap (D-003) |
| 6 | WI-943 | Build after WI-942 lands (D-002) |
| 7 onward | As before | WI-918 (ready since WI-917 landed), WI-902 (B4), WI-798, then P1 to P8, then leg 03's rows; WI-940 after the batch |

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Decide before the first headless run:** status.md's two launcher
  follow-ups from WI-917's rounds (trunk bound once per run; a descent
  check on `archive/lanes`).
- **Confirm or overrule:** coordinator-2026-10-18 D-001 to D-003; wi-917
  D-003 to D-005; wi-916 D-001, D-002; wi-915 D-001; wi-942 D-001; and the ones the
  2026-10-17e handoff lists.
- **Still open from earlier handoffs:** the convergence-tag question; the
  `wi-880` worktree's uncommitted hook edit; the old `coordinator-tools`
  folder; OI-98 and OI-105, each waiting on its condition.

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
