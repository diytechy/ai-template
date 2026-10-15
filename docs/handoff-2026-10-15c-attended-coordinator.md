# Handoff 2026-10-15c (attended): the hook rows are filed and claimed; WI-911's plan passed the gate

Overnight: stop

It replaces [handoff-2026-10-15b-attended-coordinator.md](handoff-2026-10-15b-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **Landed on trunk this session** (no code changed; no full suite owed):
  - `c2b20453b`: WI-921 and WI-922 filed (coordinator-2026-10-15 D-002).
  - `f3f532ce1`: their round-1 critique dispositions, three MAJORs adopted.
    WI-921 gains a Trust section, becomes `single`, and absorbs the fix for
    its step's two-commit fail-open (D-003, high-risk).
  - `36b1ef6bf`: round 2 confirms both, APPROVE with no findings.
  - `e2ccc5851`, `3d834c5a9`, `841cf3694`, `769224e01`: one scoped unpause,
    the two claims, the byte-identical restore.
  - The close-out commit: this handoff, status, the log fragment and five
    recipe lessons.
- **Owner rulings, 2026-10-15, in session** (all as recommended; in the
  specs' "Calls ruled at filing" and in D-002 and D-003):
  - WI-921 Q1: a census test, not a derived floor.
  - WI-922 Q1: the close-by-content rule stays. Q2: a merge git commits
    itself stays out of reach. Q3: text-then-act is left alone; whether
    `ruling-sync` and `held-status` share the shape is a status.md
    follow-up.
  - Queue order: WI-921 lands once WI-911's plan has passed (now true), and
    WI-911 then lands through its armed hold; WI-922 lands after WI-917.
  - The done-when step's two-commit fail-open is fixed in WI-921: a trunk
    commit that changes a claim copy's Done-when is judged against its
    parent. So a trunk amendment of a claimed row's Done-when now owes its
    blessing in its own commit (D-003, flagged for your review).
- **Lanes:**
  - `wi-911` (WI-911, B1 text, `single`), tip `89bb71838`: the first row
    through the plan gate. Plan `1726fce66`; critique 1, one MAJOR
    (`1211b5508`); the one revision `8c361b7a7`; critique 2, APPROVE
    (`6a9c50c2c`); pass record `89bb71838`. Its decisions record has D-001
    to D-003. Next: the first build.
  - `wi-921` (WI-921, `single`), worktree at `769224e01`: its plan step is half done. Plan
    `3924a127e` (12 of 12 clauses, `DELTA: within`); critique 1, one MAJOR
    (`363ec972a`): the full-lane gate runs before the close, the RESYNC
    re-anchor and the regeneration, so it would not review the tip that
    lands. The lane has no decisions record yet; its critique took wi-911
    D-001's preface and a write-only-the-verdict line.
  - `wi-922` (WI-922, `single`): claimed, branch at `769224e01`, no
    worktree or commit.
  - `wi-914` (WI-914, B2), tip `58a937342`: unchanged.
  - `wi-912`, `wi-915` and `wi-916`: branches at `e92cec843`, no worktree
    or commit. Move each to trunk's tip before its first commit.
  - WI-798 and WI-902 are unchanged. The `wi-913` branch stays until the
    open lanes have rebased.
- **Watermark** on trunk: WI 922; SR 239, LLR 337, IF 295, TC 367, OI 114;
  acts to seq 115 (unchanged apart from WI).
- **Strict lints on trunk:** `check_trajectory.py --strict` clean;
  `trace.py --strict` has LLR-292's one finding, which WI-914 fixes.
- **No judgement is active**, and the lease is handed back at close-out.
  `docs/work/pause` is tracked, restored byte-identical.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-15b-coord/`
  keeps both rows' critiques (`crit-92N-r1`, `-r2`), WI-921's Trust draft
  with its notes (`crit-921-r1/trust-draft.md`, part C), WI-911's plan
  briefs and critiques (`wi-911/`), WI-921's planner brief (`wi-921/`), and
  `critique-addendum.md` and `round2-block.md`. The 2026-10-14 root still
  keeps `wi-914/` and the review addenda.

## How to run reviews now

As the 2026-10-15b handoff says, plus the recipes' new lines for the plan
step (§1 "Single plan", §7): a plan critique takes `critique-addendum.md`
under a plan preface; the second plan critique needs a reading-scope block
added by hand; and the coordinator files every plan critique itself.

## The queue

Every row changes the cycle's machinery, so each lands alone, after the
cycle has run through the last one's change.

| # | Row | Next |
|---|---|---|
| 1 | WI-921 | Its plan's one revision (`review_brief.py plan --revise`, a fresh Opus planner) answering critique 1's MAJOR; the gate with `--findings docs/plans/WI-921/critique-1.md`; a second critique in convergence stance (reading-scope block by hand, recipes §1); the pass record. Then the build, three-reviewer rounds, the checkpoint (TC-325 and TC-019 at least; LLR-309 or LLR-307 if the sitting reads deliverable 5 as new), the gate, and the landing. It lands before WI-911 |
| 2 | WI-911 | B1's text: the first build from the passed plan (the build brief names `docs/plans/WI-911/plan.md`), built beside WI-921; then rounds, the checkpoint, the gate. It lands after WI-921, through its armed hold |
| 3 | WI-914 | B2: rebase, then its checkpoint (the LLR-292 amendment sitting and its act) after WI-911 lands; the uncounted gate; the landing |
| 4 onward | as the 2026-10-14c table, with WI-922 after WI-917 | WI-912, WI-917, WI-922, WI-916, WI-915, WI-902 (B4), WI-798, then P1 to P8 with WI-918, then leg 03's rows |

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Confirm or overrule:**
  - `coordinator-2026-10-15.toml` D-002 (the filing) and D-003 (high-risk:
    your queue and fail-open rulings, and the trunk-amendment consequence).
  - `wi-911.toml` D-001 to D-003: how the plan critiques were briefed and
    filed by hand.
  - WI-921's and WI-922's Trust sections, in their specs.
  - Still unseen from before: `coordinator-2026-10-14.toml` (D-005 is
    high-risk), `wi-913.toml` D-001 to D-010, `wi-914.toml` D-001 and
    D-002, and `coordinator-2026-10-15.toml` D-001.
- **The three-reviewer trial:** no full-lane review ran this session (the
  critiques are Sol's alone), so the counts stand as the 2026-10-15b
  handoff gives them. About four more lanes are owed before the trial's
  call.
- **Still open:** the `wi-880` worktree's uncommitted hook edit, and the
  old `coordinator-tools` folder. OI-98 and OI-105 wait on their conditions.
- **Noted for the queue, not yet filed:**
  - The plan critique's renderer (WI-913's gate) lets the critic run the
    filing step and commit, and its second-round brief names no reading
    exclusion (wi-911 D-002 and D-003). It belongs in WI-922's lane, which
    re-touches the gate, or a row of its own.
  - The Trust drafter's other notes (`crit-921-r1/trust-draft.md`, part C):
    intake's mint skips an unreadable closed spec without a word, against
    its own docstring; IF-255 lists no `done_when` field and omits
    `kitlib/done_when` as a consumer; a lane-side close on a detached HEAD
    or alias passes the hook (WI-922's class; the landing re-judges it).
  - Carried from before: about 150 `RESYNC_PACK.md` entries under its §4
    while §1.3 says apply only §3's; the baseline manifest's two regression
    counts (15 strict, 26 by the site test); `archive/lanes` reading as
    attributed at the gate, and trunk's 99 dangling doc-refs; three
    interface rows that omit the attended brief renderer.

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
