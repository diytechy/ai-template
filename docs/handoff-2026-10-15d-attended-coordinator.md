# Handoff 2026-10-15d (attended): both hook-and-text lanes are built and in review

Overnight: stop

It replaces [handoff-2026-10-15c-attended-coordinator.md](handoff-2026-10-15c-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **Landed on trunk this session:** no lane landed and no trunk code
  changed. The close-out commit carries this handoff, status, the log
  fragment and four recipe lessons; before it, `3a988cb86` filed WI-923, a defect a load-sensitive smoke red showed (the runtime store's lock crashes on Windows when an exclusive create meets the holder's in-progress delete), before its scope critique (coordinator-2026-10-15 D-004).
- **Lanes:**
  - `wi-921` (WI-921, `single`), tip `a877ee506`. The plan step is done:
    rebased onto trunk's tip (`e474f51dd`, D-003); the one revision
    (`f06bd16eb`) answered critique 1's MAJOR; critique 2, Sol in
    convergence stance, APPROVE with no findings (`cc61cfdcc`); pass record
    `5f3583bfd`. D-004 to D-010 record the plan's seven calls for the owner.
    Build round 1 (P1 to P3) at `d8a636d1b`; Terra's intent set (SR-156,
    LLR-307, LLR-309, TC-325, TC-019, by addition) at `bd4d7da21`.
    Full-lane review round 1 at `bd4d7da21`: filed `a877ee506` (D-011): 001 Sol CHANGES-REQUESTED, 2 MAJORs (F1, a claimed spec whose path git quotes, such as a non-ASCII slug, passes the trunk arm unblessed; F2, the intent rows are unjudged at the reviewed tip); 002 Fable APPROVE, 4 MINORs; 003 Opus APPROVE, 3 MINORs.
    Next: triage round 1 (F1's reachability under the review threat model; F2 reads as carried by the plan's own P4 checkpoint, to confirm or send to a dispute sitting), a fix round if F1 stands, round 2, the checkpoint (P4), then P5 and the gate. Per its plan (C7, R6), the row closes in the lane
    before the final gate, and the gate is taken only when the row is next
    to land.
  - `wi-911` (WI-911, B1 text, `single`), tip `6e2ad9f7f`. Rebased onto
    trunk's tip before its build (D-004). Build round 1 in three stages:
    P6(a)'s pin `59487bbcf`, the move alone `ac48b7a73`, the rest
    `8637c011e` (P2 to P11, P13), with `max-tests` re-stamped 2600 to 2715
    (D-005). Terra's intent set at `bd52ffaf5` (D-007: two approved phrases
    of SR-233 that Terra reworded were restored). Full-lane round 1
    (counted round 1) at `bd52ffaf5`, filed `36f18cbfc`: 001 Sol
    CHANGES-REQUESTED, 1 MINOR; 002 Fable APPROVE, 3 MINORs; 003 Opus
    CHANGES-REQUESTED, 1 MAJOR and 4 MINORs (D-009). Fix round 2 at
    `6e2ad9f7f` (D-010): the reviewer template's reading scope excludes
    decision records and plan critiques, by construction. Next: full-lane
    round 2 (counted round 2, ordinary stance) at `6e2ad9f7f`; then, with
    no BLOCKER or MAJOR, the checkpoint (Terra reconciles, with the
    spine-wording MINORs on the change list; the closure check; one
    combined sitting), then the uncounted convergence gate. It lands after
    WI-921.
  - `wi-922` (WI-922, `single`): claimed, branch at `769224e01`, no worktree
    or commit. It lands after WI-917.
  - `wi-914` (WI-914, B2), tip `58a937342`; `wi-912`, `wi-915` and
    `wi-916`: branches at `e92cec843`, no commit. Move each to trunk's tip
    before its first commit. WI-798 and WI-902 are unchanged. The `wi-913`
    branch stays until the open lanes have rebased.
- **Watermark** on trunk: WI 923; SR 239, LLR 337, IF 295, TC 367, OI 114; acts to seq 115.
- **Strict lints on trunk:** `check_trajectory.py --strict` clean;
  `trace.py --strict` has LLR-292's one finding, which WI-914 fixes.
- **Smoke tier:** both lanes' bars were read while other lanes' builders or
  reviewers loaded the box; several readings breached 60 s with the parent
  as slow or slower in the same window (each commit message records both).
  Re-measure each lane quiet before its landing.
- **No judgement is active**, and the lease is handed back at close-out.
  `docs/work/pause` is tracked, unchanged this session.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-15c-coord/`
  holds `bar.sh` (the commit bar: smoke timed by wall clock, the budget on
  that reading, the strict lints), the addenda copied from the earlier
  roots, both lanes' briefs, plans, spine change lists (`wi-9NN/spine-changes.md`),
  arms maps, review renders (`wi-9NN/r1/{A,B,C}`) and WI-911's coverage
  plans (`wi-911/cov-r2-*.md`).

## How to run reviews now

As the 2026-10-15c handoff says, plus two lessons now in the recipes: a
lane that changes the reviewer template is rendered by trunk's
`review_brief.py review --root <lane>` (recipes §7), and an intent or
reconcile set is checked mechanically for verbatim approved text (recipes §5).
WI-911's fix moves the reading-scope exclusion into the template only when it
lands; until then convergence briefs keep the hand-appended
`review-convergence-addendum.md`.

## The queue

| # | Row | Next |
|---|---|---|
| 1 | WI-921 | Triage round 1 (two MAJORs from Sol), a fix round if F1 stands, round 2, the checkpoint (P4), P5 (the close in the lane, the re-anchor, the full suite) and the gate, then the landing. It lands before WI-911 |
| 2 | WI-911 | Full-lane round 2 at `6e2ad9f7f`; then the checkpoint and the gate. It lands after WI-921, through its armed hold |
| 3 | WI-914 | B2: rebase, then its checkpoint (the LLR-292 amendment sitting and its act) after WI-911 lands; the uncounted gate; the landing |
| 4 | WI-923 | Filed this session (the store-lock defect): its scope critique and dispositions before any claim; Q1 is the owner's to confirm or overrule (coordinator-2026-10-15 D-004) |
| 5 onward | as before | WI-912, WI-917, WI-922, WI-916, WI-915, WI-902 (B4), WI-798, then P1 to P8 with WI-918, then leg 03's rows |

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Confirm or overrule:**
  - `wi-921.toml` D-004 to D-010, the passed plan's calls C1 to C7 (D-004,
    off-git judges nothing, is flagged high-risk), and D-001 to D-003.
  - `wi-911.toml` D-004 to D-010: the pre-build rebase, the `max-tests`
    re-stamp (D-005), the finding-tag form (D-006), the restored SR-233
    phrases (D-007), the review framing (D-008), round 1's triage (D-009),
    and fix round 2 with its two residues (D-010: a revised plan can still
    name an earlier critique finding, and every review now skips decision
    records).
  - `coordinator-2026-10-15.toml` D-004: the filing of WI-923 and its Q1
    default (a lock refusal that never clears becomes the busy refusal,
    naming the cause).
  - Still unseen from before: as the 2026-10-15c handoff lists.
- **The three-reviewer trial:** WI-911's round 1 is the trial's first
  full-lane round in this program's queue: round-costing findings Opus 1,
  Sol 0, Fable 0; MINORs Sol 1, Fable 3, Opus 4. WI-921's round 1: round-costing findings Sol 2 (pending triage), Fable 0, Opus 0; MINORs Fable 4, Opus 3. About three
  more lanes are owed before the trial's call.
- **Still open:** the `wi-880` worktree's uncommitted hook edit, and the
  old `coordinator-tools` folder. OI-98 and OI-105 wait on their conditions.
- **Noted for the queue, not yet filed:**
  - WI-911's plan removes recipes §7's by-hand addendum bullet, and
    `critique --plan` renders no severity-by-reachability text, so a FIRST
    plan critique after WI-911 lands judges with the plan rubric alone (the
    builder's stage-3 report). No round-1 reviewer raised it; put it to
    round 2's triage or file it at the landing.
  - The two census reasons WI-921's builder wrote from the steps rather than
    from cited text (`assumption-evidence`, `vocabulary`).
  - Carried from the 2026-10-15c handoff's list, unchanged.

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
