# Handoff 2026-10-15g (attended): the hook-floor row landed and its successor filed; the store-lock row through its first round

Overnight: stop

It replaces [handoff-2026-10-15f-attended-coordinator.md](handoff-2026-10-15f-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **Landed on trunk this session** (code changed: WI-921's hook, step
  reader and census):
  - `9d0f1c54b`: WI-921's squash. P5 ran in the lane first: the rebase onto
    `9ddc5ee2a` (no code or row changed, D-019), the RESYNC entry
    re-anchored there, the close in its own commit, the bar and the full
    suite at the close tip, then the uncounted gate in convergence stance:
    `012-REVIEW-A-5ba44ea` (Sol) APPROVE, `013-REVIEW-B-5ba44ea` (Fable)
    APPROVE with 2 MINORs, `014-REVIEW-B-5ba44ea` (Opus) APPROVE with 4,
    one shared; every MINOR carried to WI-925 (D-020). Its armed
    `done-when-blessed` step judged its own close and the landing, and
    passed both.
  - `cec661845`: the sweep's re-mint, WI-924; `d6b4d42a7`: WI-924 closed as
    already settled (sitting 011, act 116; the registries equal their
    anchors).
  - `cc307bcc5`: WI-925 filed, the owner's successor (wi-921 D-014): the
    trunk reference-update hold. The owner ruled its eight filing calls in
    session, each as recommended ("Calls ruled at filing"); Q3 forces a
    one-line adopter migration (a declared `trunk` key).
  - `archive/lanes` `485a37188`: WI-921's final tip `e1e5fb9df` and the
    pre-rebase tips `e810210a8` and `363ec972a`.
  - The close-out commit: this handoff, status, the log fragment, three
    recipe lessons.
- **Lanes:**
  - `wi-921`: landed. Its branch and worktree stay until the open lanes
    have rebased, like `wi-913`'s.
  - `wi-911` (WI-911, B1 text, `single`), tip `d9376ea14`, unchanged: next
    the rebase onto trunk's tip, then the checkpoint (Terra, session
    `01a14070-6bc6-7b80-bde5-97286c2ce5e3`, reconciles
    `wi-911/spine-changes.md`; the closure check; one combined sitting),
    the uncounted gate, and the landing through WI-921's now-armed hold.
  - `wi-923` (WI-923, `single`), tip `b971ea636`, on base `4c216fd2f`:
    Terra's intent `24fabf54b` (session
    `01a141bb-bb17-7852-925c-5d31e5ad3239`; LLR-270's STORE clause, TC-267
    and TC-329 by addition, checked addition-only); full-lane round 1 filed
    (`001` Sol CHANGES-REQUESTED, 1 MINOR; `002` Fable APPROVE; `003` Opus
    APPROVE, 1 MINOR). Both MINORs are the planned checkpoint item and the
    P2 stress re-run, so the counted rounds are done at one (D-002). Next:
    the coordinator's P2 re-run by the plan's method (a detached worktree
    for trunk's code); then, after WI-911 and WI-914 land, the rebase, the
    checkpoint (Terra reconciles; the closure check; one combined sitting,
    `amendment:TC-267;amendment:TC-329;amendment:LLR-270` under SR-227),
    the gate and the landing.
  - `wi-922` (claimed, no worktree), `wi-914` (tip `58a937342`), and
    `wi-912`, `wi-915` and `wi-916` (branches at `e92cec843`): unchanged.
    Move each to trunk's tip before its first commit. WI-798 and WI-902 are
    unchanged. The `wi-913` branch stays until the open lanes have rebased.
- **Watermark** on trunk: WI 925; SR 239, LLR 337, IF 295, TC 367, OI 114;
  acts to seq 116.
- **Strict lints on trunk:** `check_trajectory.py --strict` clean;
  `trace.py --strict` has LLR-292's one finding, which WI-914 fixes.
- **Smoke tier:** quiet readings 35.6 to 47.9 s. Under the owner's
  foreground load the tier read 189 to 236 s; the owner chose below-normal
  priority for local test jobs, the parent was timed in the same window,
  and every landing reading was quiet.
- **Full suite:** at WI-921's close tip, 5979 passed, 22 skipped, and one
  detached-worktree red on the trunk-only `docs/stage`, cleared by
  re-deriving (D-020); on trunk's tip `cc307bcc5`: 5980 passed, 22 skipped, none failed (756.5 s at below-normal priority).
- **No judgement is active**, and the lease is handed back at close-out.
  `docs/work/pause` is tracked, unchanged this session.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-15d-coord/`,
  this session under `g/`: `lowprio.py`, `full_suite.sh`,
  `check_addition.py`, `add_decision.py`, `close_remint.py`,
  `file_successor.py`, the successor draft; `wi-921/gate/`;
  `wi-923/r1/`, its intent prompt, report and `arms-map.md`.

## How to run reviews now

As the 2026-10-15f handoff says, with the recipes' new lines (§7): run
local test jobs at below-normal priority when the owner asks, and resume a
Claude reviewer that lost its own background run rather than replacing it.

## The queue

| # | Row | Next |
|---|---|---|
| 1 | WI-911 | The rebase; the checkpoint (Terra's reconcile, the closure check, one combined sitting); the uncounted gate; the landing through WI-921's armed hold |
| 2 | WI-914 | B2: rebase, then its checkpoint (the LLR-292 amendment sitting and its act) after WI-911 lands; the uncounted gate; the landing |
| 3 | WI-923 | P2's re-run now; after WI-911 and WI-914 land, the rebase, the checkpoint, the gate, the landing |
| 4 | WI-925 | Its scope critique (with `critique-addendum.md`; Sol from `trunk-tmp`), dispositions and a confirming round, before a claim (`single`). Its build order against WI-922, which also edits the hook, is the owner's to set |
| 5 onward | as before | WI-912, WI-917, WI-922, WI-916, WI-915, WI-902 (B4), WI-798, then P1 to P8 with WI-918, then leg 03's rows. WI-917 and WI-918 each owe their confirming scope-critique round before a claim |

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Confirm or overrule:**
  - `wi-921.toml` D-019 (P5's rebase, re-anchor and readings, with the
    gate's evidence mapping) and D-020 (the gate's triage: every MINOR to
    WI-925; the full suite's one red explained).
  - `wi-923.toml` D-002 (round 1's triage: the counted rounds done at one).
  - Still unseen from before: as the 2026-10-15f handoff lists.
- **The three-reviewer trial:** WI-921's gate (convergence): round-costing
  0 each; MINORs Sol 0, Fable 2, Opus 4, one shared. WI-923 round 1:
  round-costing 0 each; MINORs Sol 1, Fable 0, Opus 1, both the same
  checkpoint item. With WI-921 landed, about one more lane is owed before
  the trial's call.
- **Still open:** the `wi-880` worktree's uncommitted hook edit, and the
  old `coordinator-tools` folder. OI-98 and OI-105 wait on their conditions.
- **Noted for the queue, not yet filed:**
  - WI-925's Trust section reports four consumers that fail open outside
    its scope ("Consumers that fail open today", items 2 to 5: the
    work-tree probe in `staged_changes`, a detached HEAD in `_staged_base`,
    `intake`'s silent skip of an unreadable closed spec, and the hook's
    exit 0 when the scripts directory is missing): file or fold them.
  - Carried from the 2026-10-15f handoff's list, unchanged (sitting 010's
    incident for WI-912; shipped text citing this repository's records;
    stale return-route references; the 2026-10-15e list).

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
   (medium), Claude Fable (medium) and Claude Opus (high) review in parallel,
   a trial (the handoff's "How to run reviews now"); the independent adjudicator
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
