# Handoff 2026-10-15b (attended): the plan gate has landed; two hook rows are drafted to file

Overnight: stop

It replaces [handoff-2026-10-15-attended-coordinator.md](handoff-2026-10-15-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **Landed on trunk this session:**
  - `b803dd019`: WI-913, the plan gate (squash of `wi-913`). Sittings 010
    and 011 ran in the lane (acts 113 to 115); the uncounted gate
    (`docs/reviews/wi-913/012` to `014`) approved with MINORs only. A
    `single` row now plans in its lane, through `review_brief.py plan`,
    `critique --plan` and `plan-file`, before the `plan-gate` step releases
    its build.
  - `2962022f8`: the landing sweep minted WI-919 and WI-920.
  - `4cdbe977a`: WI-919 closed as already settled (the re-mint).
  - The close-out commit: this handoff, status, the log fragment,
    `coordinator-2026-10-15.toml` and the recipe lessons.
- **Owner ruling, 2026-10-15, in session** (recorded in `wi-913.toml`
  D-008): SR-154 carries the single-plan hold under its one `shall`, with
  the approved sentence reordered so its unattended condition scopes only
  the routing predicate, over a separate SR or a waiver.
- **Lanes:**
  - `wi-914` (WI-914, B2), tip `58a937342`: unchanged. It rebases onto
    trunk (now carrying WI-913) before its checkpoint.
  - `wi-911`, `wi-912`, `wi-915` and `wi-916`: claimed, with branches at
    `e92cec843` and no worktree or commit. Move each to trunk's tip before
    its first commit (recipes §2).
  - WI-798 and WI-902 are unchanged. The `wi-913` worktree is removed; its
    branch stays until the open lanes have rebased.
- **Watermark** on trunk: WI 920; SR 239, LLR 337, IF 295, TC 367, OI 114;
  acts to seq 115. WI-913's floor spent LLR-327 to LLR-336, TC-352 to
  TC-366 and IF-294 for `wi-798` and `wi-902`, so `trace.py --strict` lists
  them as spent until those lanes land (wi-913 D-004).
- **Strict lints on trunk:** `check_trajectory.py --strict` clean;
  `trace.py --strict` has LLR-292's one finding, which WI-914 fixes.
- **Queued as real work:** WI-920, TC-055's declared-trigger re-judge,
  minted by the landing sweep.
- **No judgement is active**, and the lease is handed back at close-out.
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-14-coord/`
  keeps `wi-914/`, the two by-hand review addenda (still appended until
  WI-911 lands) and `critique-addendum.md`. The new
  `C:/Projects/ai-template.wt/review-tmp/2026-10-15-coord/drafts/` holds
  the two row drafts, with the planner's notes and probes.

## How to run reviews now

As the 2026-10-15 handoff says, with one addition (wi-913 D-009, now in
recipes §7): a convergence brief's reading exclusion names the lane's
decisions record beside `docs/reviews/`.

## The queue

Every row changes the cycle's machinery, so each lands alone, after the
cycle has run through the last one's change.

| # | Row | Next |
|---|---|---|
| 1 | *to file* | The hook-floor row (draft `drafts/row-hook-floor.md`): a census over every built-in check step, `done-when-blessed` put in the shipped hook's floor, a RESYNC entry. File it on trunk with its scope critique and dispositions |
| 2 | *to file* | WI-913's successor (D-006; draft `drafts/row-landing-shapes.md`): the landing shapes the hook does not judge, plus D-010's two MINORs (SR-154's single-plan predicate with its own condition; the gate's unreachable cap branch). Rule its Q1 to Q3 at filing, then its scope critique |
| 3 | WI-911 | B1's text, `single`: the first row to plan through the landed gate. Cut its lane from trunk's tip; the planner writes the in-lane plan; one Sol critique (`review_brief.py critique --plan`), filed with `plan-file`; the pass record; then the build |
| 4 | WI-914 | B2: rebase, then its checkpoint (the LLR-292 amendment sitting and its act) after WI-911 lands; the uncounted gate; the landing |
| 5 onward | as the 2026-10-14c table, rows 4 to 10 | WI-912, WI-917, WI-916, WI-915, WI-902 (B4), WI-798, then P1 to P8 with WI-918, then leg 03's rows |

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Confirm or overrule:**
  - `docs/decisions/coordinator-2026-10-14.toml`, as the 2026-10-14c
    handoff lists (D-005, the plan gate's design, is high-risk; its Q7 put
    the gate under SR-154, which your 2026-10-15 ruling kept).
  - `wi-913.toml` D-001 to D-010:
    - D-007 and D-008: the checkpoint's authoring calls; D-008 also records
      your ruling.
    - D-009: the gate's reading exclusion.
    - D-010: the gate's MINORs.
  - `wi-914.toml` D-001 and D-002; `coordinator-2026-10-15.toml` D-001
    (the two rows drafted, not filed).
- **The three-reviewer trial after its first lane** (WI-913, three rounds
  plus the gate), by accepted finding:
  - **Sol:** two of the lane's three MAJORs, and the gate's one unique
    MINOR.
  - **Opus:** one MAJOR; at the gate, two MINORs, both shared with Fable.
  - **Fable:** no MAJOR; the most MINORs, including the gate's unique dead
    branch.
  - About four more lanes are owed before the trial's call.
- **Still open** (from the 2026-10-14c handoff): the `wi-880` worktree's
  uncommitted hook edit, and the old `coordinator-tools` folder. OI-98 and
  OI-105 wait on their conditions.
- **Noted for the queue, not yet filed:**
  - About 150 `RESYNC_PACK.md` entries sit under its §4 while its §1.3
    tells an adopter to apply only §3's (a row before the FileBackup
    re-sync).
  - The baseline manifest counts regressions two ways (15 strict, 26 by
    the site test), so the phase-4 re-measure must name one.
  - The planner's two side findings: `archive/lanes` contains every
    archived lane tip, so the gate's hold on a squash no branch contains
    reads such a tip as attributed (unreachable at a normal landing, where
    the tip is archived after its squash); and trunk's doc-refs check
    reports 99 dangling paths.
  - Three interface rows for the coverage command omit the attended brief
    renderer as a participant (wi-913 D-010, to the plan's item 11
    migration).

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
