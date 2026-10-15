# Handoff 2026-10-15 (attended): the plan gate's lane passed its three review rounds; its checkpoint is next

Overnight: stop

It replaces [handoff-2026-10-14c-attended-coordinator.md](handoff-2026-10-14c-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **Landed on trunk this session:** only the close-out commit (this
  handoff, status, the log fragment and four recipe lessons). No code
  changed on trunk; no full suite is owed.
- **Lanes:**
  - `wi-913` (WI-913, G), tip `b9de474d7`: the intent pass (`96b00df1d`:
    Terra's set from SR-154 down, with the coordinator's retag and the
    IF-295 contract body), three full-lane review rounds in the trial shape
    and two fix builds. Round 3 ran in convergence stance and all three
    reviewers approved with MINORs only. Its decisions record,
    `docs/decisions/wi-913.toml`, has D-001 to D-006: the IF-295 seam, the
    review shape, each round's dispositions and trial tally, and D-005's
    map of every accepted finding to its regression test. The row text the
    checkpoint owes is on the lane's spine change list
    (`<scratch root>/wi-913/spine-changes.md`), one section per round.
  - `wi-914` (WI-914, B2), tip `58a937342`: the intent pass (`737ab5c54`,
    LLR-292's Detail, so `trace.py --strict` exits 0 in the lane) and round
    1, filed. Sol's one MAJOR is the checkpoint's owed act, and Opus's one
    MINOR is fixed (D-002). The lane waits at its checkpoint: its sitting
    and act keep landing order, after WI-913 and WI-911.
  - `wi-911`, `wi-912`, `wi-915` and `wi-916`: claimed, with branches at
    `e92cec843` and no worktree or commit (unchanged).
  - WI-798 and WI-902 are unchanged.
- **Watermark** on trunk (unchanged): WI 918; SR 239, LLR 326, IF 293, TC
  351, OI 114; acts to seq 112. The `wi-913` lane holds LLR-337, TC-367 and
  IF-295, above `wi-798`'s LLR-336 and TC-366 and `wi-902`'s IF-294 (a floor,
  wi-913 D-004).
- **Strict lints on trunk:** `check_trajectory.py --strict` clean;
  `trace.py --strict` has LLR-292's one finding, which WI-914 fixes.
- **A trunk defect, confirmed and not yet filed:** WI-841's
  `done-when-blessed` step is registered in `check.py` but missing from
  the shipped pre-commit hook's `--run-steps` floor, with no path trigger,
  so the hook never runs it (the WI-913 round-3 builder's stop-and-report;
  wi-913 D-005).
- **No judgement is active**, and the lease is handed back at close-out.
  `docs/work/pause` is tracked and unchanged.
- **Scratch root, kept:** `C:/Projects/ai-template.wt/review-tmp/2026-10-14-coord/`.
  Beside last session's material, it now holds `review-addendum.md` and
  `review-convergence-addendum.md` (appended to review briefs until WI-911
  lands, recipes §7), `rowdiff.py` (a registry cell differ, HEAD against
  the working tree), and each lane's rounds, briefs, coverage plans and
  basetemps. Keep each lane's folder until that lane lands.

## How to run reviews now

As the 2026-10-14c handoff says (the 2026-10-11 handoff's section, with
`critique-addendum.md` on every critique brief), plus recipes §7's new
bullet: append `review-addendum.md` to every review brief, and
`review-convergence-addendum.md` too for a convergence round (the last
allowed round and the post-checkpoint gate).

## The queue

Every row changes the cycle's machinery, so each lands alone, after the
cycle has run through the last one's change.

| # | Row | Next |
|---|---|---|
| 1 | WI-913 (G) | The checkpoint. Resume Terra (session `01a13dc2-d1f7-7851-9102-28d6f8c99d81`, from the lane) to reconcile the whole set against the code from the spine change list's round sections, keeping approved text verbatim and adding to it (recipes §5). Rebase onto trunk's tip; run the closure checks; then one combined sitting: amendments SR-154, LLR-313 and TC-333 (LLR-069's and LLR-302's trace-cell edits are back-link upkeep, D-004), first approvals LLR-337 and TC-367; IF rows carry no status. Then the uncounted post-checkpoint gate (three reviewers, convergence stance), then land. At the landing, file on trunk one successor row for the hook's unjudged landing shapes (D-006) |
| 2 | *to file* | WI-841's `done-when-blessed` step into the shipped hook's floor, with a test that drives the hook's own step list and a RESYNC entry; a mechanism change that lands alone. File it on trunk with its scope critique |
| 3 | WI-911 | B1's text, `single`: its plan goes through the landed gate, so it builds after WI-913 lands |
| 4 | WI-914 | B2: its checkpoint (the LLR-292 amendment sitting and its act) after WI-913 and WI-911 land and it rebases; then the uncounted gate and the landing |
| 5 onward | as the 2026-10-14c table, rows 4 to 10 | WI-912, WI-917, WI-916, WI-915, WI-902 (B4), WI-798, then P1 to P8 with WI-918, then leg 03's rows |

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Confirm or overrule:**
  - `docs/decisions/coordinator-2026-10-14.toml`, as the 2026-10-14c
    handoff lists (D-005, the plan gate's design, is high-risk).
  - The lanes' records: `wi-913.toml`.
    - D-001 is the new IF-295 for the gate's command line.
    - D-003 and D-004 fixed MINORs inside rounds that ran for MAJORs
      anyway, instead of filing successor rows.
  - `wi-914.toml` D-001 and D-002.
- **The three-reviewer trial, first lane** (WI-913, three rounds), by
  accepted finding:
  - **Sol:** two of the lane's three MAJORs, the non-string planmode
    fail-open (round 1) and the hook that never ran the gate (round 2).
  - **Opus:** one MAJOR, the dispute numbering at the cap, which it
    reproduced by running.
  - **Fable:** no MAJOR. It found the most MINORs (fifteen), several of
    them unique (the critique-round pattern, the CRLF compare, two hook
    shapes).
  - On WI-914, only Sol's owed-act MAJOR and one Opus MINOR.
  - The counts per round are in D-003, D-004 and D-006. About four more
    lanes are owed before the trial's call.
- **Still open** (from the 2026-10-14c handoff): the `wi-880` worktree's
  uncommitted hook edit, and the old `coordinator-tools` folder. OI-98 and
  OI-105 wait on their conditions.
- **Noted for the queue, not yet filed:** about 150 `RESYNC_PACK.md`
  entries sit under its §4 while its §1.3 tells an adopter to apply only
  §3's (a row before the FileBackup re-sync); and the baseline manifest
  counts regressions two ways (15 strict, 26 by the site test), so the
  phase-4 re-measure must name one.

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
