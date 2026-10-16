# Handoff 2026-10-15h (attended): the process-text row through its checkpoint; the trunk-hold row's critiques; the owner's plausibility rulings

Overnight: stop

It replaces [handoff-2026-10-15g-attended-coordinator.md](handoff-2026-10-15g-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **On trunk this session** (no code changed on trunk):
  - `18cf71e62`: WI-925's scope critique round 1 dispositioned, both MAJORs
    adopted (the pre-filter takes the reader's merge-base delta; the Q8
    exemption's carrier contract), coordinator-2026-10-15 D-006.
  - `6903db9d5`: its confirming round dispositioned: the new rewind MAJOR
    dismissed by the owner as contrived, with the owner's word fix (Q8's
    exemption covers fast-forwards only); the B1 MINOR adopted as a
    Done-when item (D-009). The owner's rulings D-007 (WI-925 and WI-922 in
    parallel, superseded by D-010) and D-008 (the out-of-scope fail-opens).
  - The close-out commit: D-010, this handoff, status, the log fragment, two
    recipe lessons (§5).
- **Owner rulings this session** (all recorded):
  - D-010: **no lane is cut for WI-922 or WI-925** until each is re-scoped
    with the owner against the 2026-10-13 plausibility ruling, one at a time:
    shapes a supported route reaches stay (WI-925's Q3 trunk identity);
    forbidden hand acts become stated residue; then a fresh critique.
    D-008's row (the fail-open items 2, 4 and 5) and its fold of item 3 into
    WI-922 are re-checked in the same walk; nothing is filed yet.
  - wi-911 D-016 and D-017: the stronger dismissal language is folded into
    WI-911 (below).
- **The audit** (owner-asked, read-only):
  `C:/Projects/ai-template.wt/review-tmp/2026-10-15d-coord/h/audit-contrived-guards.md`.
  52 MAJORs accepted with code since 2026-10-08: 15 contrived, 8 unclear, 29
  plausible; every contrived one from Sol; costliest WI-834's shell grammar,
  WI-887's store record shapes, WI-881's interrupt windows, WI-852's alias
  refusal. Nothing is removed; any removal is its own row, after reading the
  original rationale. Keep the file until the owner has read it.
- **Lanes:**
  - `wi-911` (WI-911, B1 text, `single`), tip `9f35d60ea`, rebased on
    `c0dfd1823` (D-015, no code or row changed). The owner's text fix
    `01614b9df` (PROCESS.md §6 dismisses contrived scenarios; reachability
    gates every severity class; a spec's promise reaches only supported
    routes; the dispute brief weighs plausibility; eight pinning tests).
    The checkpoint is done: Terra's reconcile (`d83a83c80`, `cdcd10ee2`),
    sitting 010 (every LLR and TC blessed, act seq 117 `dcadf1481`; SR-234
    returned), the rework `8676e5c5f` (D-018), re-sit 011 (SR-233, SR-234,
    SR-236 and TC-334 blessed, act seq 118 `f7046f559`). Next: restore the
    trunk-only views on the lane (recipes §3), then the uncounted gate in
    convergence stance, three reviewers, from `c0dfd1823` to the tip.
  - `wi-923` (WI-923, `single`), tip `6eda84f81`: P2's re-run by the
    coordinator is recorded (trunk's code: 15833 holds, 161
    `PermissionError`s escaped; the change: 16184 holds, nothing escaped).
    Next, after WI-911 and WI-914 land: the rebase, the checkpoint, the gate,
    the landing.
  - `wi-914` (tip `58a937342`), `wi-922` (claimed, no worktree, held by
    D-010), `wi-912`, `wi-915`, `wi-916` (branches at `e92cec843`), WI-798
    and WI-902: unchanged. `wi-921` and `wi-913` branches stay until the
    open lanes have rebased.
- **Watermark** on trunk: WI 925; SR 239, LLR 337, IF 295, TC 367, OI 114;
  acts to seq 116 on trunk, 118 in the `wi-911` lane.
- **Strict lints on trunk:** `check_trajectory.py --strict` clean;
  `trace.py --strict` has LLR-292's one finding, which WI-914 fixes.
- **Smoke tier:** quiet readings 34.5 to 42.0 s this session, all at
  below-normal priority.
- **Full suite:** not run: no trunk code changed this session. The last run
  is the 2026-10-15g handoff's, at `cc307bcc5`.
- **No judgement is active**; the lease is handed back at close-out.
  `docs/work/pause` is tracked, unchanged this session.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-15d-coord/`,
  this session under `h/`: `check_rebase.py`, `cell_diff.py`,
  `check_vs_approved.py` (a lane's cells against trunk's approved bytes,
  named in-place edits allowed), `terra_resume.sh`, the dispositions
  scripts, `crit-925-r1/` and `crit-925-r2/`, the sitting briefs, the audit.
  The interim addenda in the root now carry the reachability gate.

## How to run reviews now

As the 2026-10-15g handoff says, with two changes until WI-911 lands:

- The scratch root's interim addenda (`review-addendum.md`,
  `review-convergence-addendum.md`, `critique-addendum.md`,
  `round2-block.md`) now carry the reachability gate on every severity class
  and the contrived-scenario clause (owner, 2026-10-15h); keep appending
  them as before. WI-911's gate is rendered from trunk's `review_brief.py`
  with `--root` at the lane, so these addenda are what its reviewers read.
- Triage every BLOCKER or MAJOR for plausibility before it costs a round or
  blocks a claim: one that needs a hand act the process forbids, or tools in
  an order no supported route produces, is dismissed in one recorded line
  (owner, 2026-10-15h; PROCESS.md §6 says so once WI-911 lands).

## The queue

| # | Row | Next |
|---|---|---|
| 1 | WI-911 | Restore the trunk-only views; the uncounted gate (convergence, three reviewers); then P5 (the rebase if trunk moved, the RESYNC entry re-anchored at the landing's parent, the close in its own commit, the bar and the full suite) and the landing through WI-921's armed hold |
| 2 | WI-922, WI-925 | The re-scope walk with the owner (D-010), one row at a time, with the audit beside it; then a fresh critique of each under the new language. D-008's fail-open row is decided in the same walk |
| 3 | WI-914 | B2: rebase after WI-911 lands; the checkpoint (the LLR-292 amendment sitting and its act); the uncounted gate; the landing |
| 4 | WI-923 | After WI-911 and WI-914 land: the rebase, the checkpoint (`amendment:TC-267;amendment:TC-329;amendment:LLR-270` under SR-227), the gate, the landing |
| 5 onward | as before | WI-912, WI-917, WI-916, WI-915, WI-902 (B4), WI-798, then P1 to P8 with WI-918, then leg 03's rows. WI-917 and WI-918 each owe their confirming scope-critique round before a claim |

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Read the audit** (path above) and say which contrived builds, if any,
  should become removal rows.
- **Confirm or overrule:**
  - `wi-911.toml` D-015 (the rebase), D-018 (sitting 010's return answered
    through TC-334 rather than LLR-311's SR-Refs).
  - `coordinator-2026-10-15.toml` D-006 (WI-925 round 1's two adoptions,
    including the Q8 exemption's fail-closed contract).
  - Still unseen from before: as the 2026-10-15g handoff lists.
- **Sitting 010's advisory:** no spine row obliges the successor row a
  SUCCESSOR ruling promises; its filing is procedural (WI-911's Trust).
  Whether it should be attested is yours to say.
- **The three-reviewer trial:** no review round ran this session; the
  counts stand as the 2026-10-15g handoff gives them. The audit adds that
  every contrived MAJOR since 2026-10-08 came from Sol.
- **Still open:** the `wi-880` worktree's uncommitted hook edit, and the
  old `coordinator-tools` folder. OI-98 and OI-105 wait on their conditions.
- **Noted for the queue, not yet filed:** as the 2026-10-15g handoff lists,
  less WI-925's fail-open list (now D-008 and D-010).

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
