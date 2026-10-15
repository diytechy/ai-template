# Handoff 2026-10-14 (attended): batch 1 is filed and critiqued; dispositions are next

Overnight: stop

It replaces [handoff-2026-10-11-attended-coordinator.md](handoff-2026-10-11-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **Landed on trunk this session** (no code changed; no full suite owed):
  - the queue's "pre" fix: WI-910 names its spec of record,
    `docs/specs/WI-910.md`, so `check_trajectory.py --strict` is clean on
    trunk (`45d867e51`);
  - row M, the phase-0 baseline manifest, in
    `docs/plans/2026-10-11-review-churn/baseline/` (plan revision 38,
    `fa4bd0c49`);
  - batch 1 filed as six rows, each with scope answers and its open calls
    ruled (`ff64d366b`, `dd66a7a37`). WI-805 is amended for G's split, and
    WI-809 now carries the managed loop's act turn (owner, 2026-10-14).
- **Strict lints on trunk:** `check_trajectory.py --strict` clean;
  `trace.py --strict` has LLR-292's one finding, which WI-914 fixes.
- **No lease is held after the handback; no judgement is active.**
  `docs/work/pause` is tracked and unchanged.
- **Lanes:** WI-798 and WI-902 are unchanged from the previous handoff (its
  "State" bullets still hold), and nothing new is claimed.
- **Watermark** on trunk: WI 916; the spine spaces are unchanged (SR 239,
  LLR 326, IF 293, TC 351, OI 114); acts to seq 112.
- **Scratch root, kept:** `C:/Projects/ai-template.wt/review-tmp/2026-10-14-coord/`.
  It holds the critique briefs and verdicts (`crit-<wi>-<round>/`), the
  by-hand anchors appended to every critique brief until WI-911 lands
  (`critique-addendum.md`), the planner drafts (`drafts/`, including B4's)
  and M's intermediates. Delete it only after B4 is filed.
- **The scratch checkout** `C:/Projects/ai-template.wt/trunk-tmp` is detached
  at `dd66a7a37`; the critiques run from it (recipes §1).

## How to run reviews now

Unchanged: follow the previous handoff's "How to run reviews now" until
WI-911 lands and the skill says the same. For a scope critique, render the
brief with `review_brief.py critique`, append `critique-addendum.md` from
the scratch root (S3, S4, the delta and dependency anchors, B3, B4), and
launch Sol from `trunk-tmp` at the committed tip.

## The queue

The batch's edges are all soft, so the batch is claimed under one scoped
unpause; the order below is the landing order, and each row's Done-when
carries its holds (the plan gate before a `single` build; row M before any
landing). Every row except M changes the cycle's machinery, so each lands
alone, after the cycle has run through the last one's change.

| # | Row | Next |
|---|---|---|
| 1 | Scope critiques returned | All six verdicts came back before the handback, in the scratch root's `crit-<wi>-<round>/`: WI-911 round 2, 1 MAJOR and 1 MINOR; WI-912, 1 MAJOR; WI-913, 1 MAJOR and 1 MINOR; WI-914, APPROVE with none; WI-915, 1 MINOR; WI-916, 1 MINOR. Disposition each finding in its row's "Critique dispositions" section (adopted, quoting the spec text, or rejected with a reason), then one fresh confirming round per row that adopted anything |
| 2 | B4 | File WI-902's record-at-close amendment from `drafts/WI-902-amendment.md`, ruling its five questions, with its lane record (`drafts/WI-902-lane-record.md`: acts 113–117 none landing, decisions D-001 to D-010 sorted, ids kept or minted). The same commit records the owner's 2026-10-14 verdict on coordinator-2026-10-11 D-005 (`owner = "overruled"`, the previous handoff's B4 row text as `review`), since the amendment is the work item that overrule must change. Then its scope critique |
| 3 | Claim | One scoped unpause for WI-911 to WI-916 |
| 4 | WI-913 (G) | Build first: `planmode = "none"`, built without the gate it builds (D-005) |
| 5 | WI-911 | B1's text, `single`: its plan through the landed gate |
| 6 | WI-914 | B2, `none`: may build beside the above; lands after WI-911. Its LLR-292 act is trunk's next act (113) |
| 7 | WI-912 | B1's verdict/act split, `single` |
| 8 | WI-916 | The RESYNC-presence check, `single`, after WI-914 |
| 9 | WI-915 | B3, `single` |
| 10 | WI-902 (B4) | The reshape, `single`, before P4 and P5 |
| 11 | WI-798 | Its remaining steps, as the previous handoff states |
| 12 | P1–P9, then leg 03's rows | As the previous handoff's queue table states; re-order leg 03's rows against the plan with the owner. At that step, amend WI-801 (it deletes `coordinator_adjudicate.py`, so it must carry WI-912's act turn) |

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Confirm or overrule** this session's delegated decisions,
  `docs/decisions/coordinator-2026-10-14.toml` D-001 to D-005 (D-005, the
  plan gate's design, is marked high-risk). The batch rows' Trust rulings
  (WI-912, WI-913, WI-916) come to you after their critiques.
- **Still open from the previous handoff:** the `wi-880` worktree's
  uncommitted hook edit (keep or discard, then remove the worktree), and the
  old `coordinator-tools` folder (delete once the repo copy has run on a
  second machine). OI-98 and OI-105 wait on their conditions.
- **Noted for the queue, not yet filed:** about 150 `RESYNC_PACK.md` entries
  sit under its §4 while its §1.3 tells an adopter to apply only §3's, so an
  adopter following §1.3 would skip them; worth a row before the FileBackup
  re-sync. And the baseline manifest counts regressions two ways (15 strict,
  26 by the site test): the phase-4 re-measure must name one.

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
