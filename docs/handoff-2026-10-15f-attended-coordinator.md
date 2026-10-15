# Handoff 2026-10-15f (attended): the hook-floor row through its checkpoint; the store-lock row through its plan gate and first build

Overnight: stop

It replaces [handoff-2026-10-15e-attended-coordinator.md](handoff-2026-10-15e-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **Landed on trunk this session** (no trunk code changed; no full suite
  owed): `c11eb456b`, the scoped unpause for WI-923; `7848b6c62`, its
  claim; `4c216fd2f`, the pause restored byte-identical; then the close-out
  commit (this handoff, status, the log fragment, four recipe lessons).
- **Lanes:**
  - `wi-921` (WI-921, `single`), tip `e810210a8`, rebased onto `4c216fd2f`
    (pre-rebase tip `0bb65332e`, archived). 004 F1 (an amend is judged
    against HEAD) was ruled by the owner in session: a successor row, not a
    build here (D-014); the spec's Trust section states the residue (amend,
    cherry-pick, revert, rebase, non-conflicting merge commit, hand
    fast-forward, a linked-worktree commit on trunk). Fix round 3
    (`d9f306659`, D-015); round 3, the last counted, in convergence stance,
    filed (D-016): no round-costing code finding. The text fix and pin after
    it (`b776e13af`). The checkpoint: Terra's reconcile (`0668ff387`, D-017,
    with one byte-exact coordinator deletion); sitting 010 discarded (D-018:
    composed single-kind, its verdict carried a section the one parser
    refuses, after its act was committed; archived on `archive/lanes`);
    the returns reworked (`c66e451cf`); sitting 011, combined, valid:
    MEANING rows=5, all blessed (`9c040afb1`), and its act re-attests
    LLR-019, LLR-307, LLR-309, TC-019 and TC-325 (`e27289620`). Next: P5
    (the close in the lane, the RESYNC entry re-anchored at the landing's
    parent, the full suite), the uncounted gate in convergence stance
    (three reviewers), the landing; then file the owner's successor row
    (below) on trunk. It lands before WI-911.
  - `wi-911` (WI-911, B1 text, `single`), tip `d9376ea14`: the text fix
    after round 3 (D-014: the convergence command prints no commit message;
    shipped comments cite no review records, keeping WI ids and dated
    rulings; lane-added test comments cite no rounds). Next: after WI-921
    lands, the rebase; the checkpoint (Terra, session
    `01a14070-6bc6-7b80-bde5-97286c2ce5e3`, reconciles
    `wi-911/spine-changes.md`; the closure check; one combined sitting); the
    uncounted gate; the landing, through WI-921's armed hold.
  - `wi-923` (WI-923, `single`), claimed this session, tip `a62cdb456`:
    plan `c49c879ff` (DELTA none), critique 1 `553317b83` (one MINOR,
    carried to the build), pass `61c6d2afa`; build round 1, the plan's P1 to
    P3 (`a62cdb456`, D-001): an access-denied lock create reads as held, is
    retried, and past the wait is refused as busy naming the cause; four
    smoke tests red-first; the builder's preliminary stress readings in the
    lane's log fragment. Next: Terra's intent (P4: TC-267, TC-329, the
    conditional LLR-270 clause; the builder's proposals in
    `wi-923/spine-changes.md`), full-lane round 1 (three reviewers), and,
    once the code settles, the coordinator's own P2 re-run by the plan's
    method (a detached worktree for trunk's code).
  - `wi-922` (claimed, no worktree), `wi-914` (tip `58a937342`), and
    `wi-912`, `wi-915` and `wi-916` (branches at `e92cec843`): unchanged.
    Move each to trunk's tip before its first commit. WI-798 and WI-902 are
    unchanged. The `wi-913` branch stays until the open lanes have rebased.
- **Watermark** on trunk: WI 923; SR 239, LLR 337, IF 295, TC 367, OI 114;
  acts to seq 115 (unchanged on trunk; WI-921's lane holds its act).
- **Strict lints on trunk:** `check_trajectory.py --strict` clean;
  `trace.py --strict` has LLR-292's one finding, which WI-914 fixes.
- **Smoke tier:** every coordinator bar read within budget, 38 to 51 s. The
  WI-923 builder's two readings (65.2 s, 73.6 s) were taken while three
  reviewers loaded the box; the quiet reading was 48.5 s.
- **No judgement is active**, and the lease is handed back at close-out.
  `docs/work/pause` is tracked, restored byte-identical.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-15d-coord/`:
  `bar.sh`; `render_r.sh`, which now appends
  `review-convergence-handline.md` to a convergence round's briefs itself;
  the addenda; `wi-921/` (round 3's renders, `cov-r3-*`, the spine change
  list, the arms map, `sit/` and `sit2/`); `wi-911/` (`cov-r4-*`);
  `wi-923/` (`plan/`, `pcrit-1/`, the build brief, the spine change list,
  `probe/stress_dir_lock.py`).

## How to run reviews now

As the 2026-10-15e handoff says, except that `render_r.sh` appends the
convergence hand line itself; and a checkpoint sitting is always composed
`combined`, with kind-prefixed ids (recipes §1, new this session).

## The queue

| # | Row | Next |
|---|---|---|
| 1 | WI-921 | P5 (close in the lane, re-anchor, full suite); the uncounted gate (convergence, three reviewers); the landing; file the successor row on trunk. It lands before WI-911 |
| 2 | WI-911 | After WI-921 lands: the rebase, the checkpoint (Terra's reconcile, the closure check, one combined sitting), the uncounted gate, the landing through WI-921's armed hold |
| 3 | WI-914 | B2: rebase, then its checkpoint (the LLR-292 amendment sitting and its act) after WI-911 lands; the uncounted gate; the landing |
| 4 | WI-923 | Terra's intent (P4); full-lane round 1; fix rounds as needed; P2's re-run; the checkpoint; the gate; the landing |
| 5 onward | as before | WI-912, WI-917, WI-922, WI-916, WI-915, WI-902 (B4), WI-798, then P1 to P8 with WI-918, then leg 03's rows. WI-917 and WI-918 each owe their confirming scope-critique round before a claim |

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Confirm or overrule:**
  - `wi-921.toml` D-014 (your in-session ruling on 004 F1, as recorded),
    D-015 (fix round 3 and the evidence mapping), D-016 (round 3's
    triage), D-017 (the reconcile, with the coordinator's byte-exact
    deletion of one contradictory lane-added sentence), D-018 (sitting 010
    discarded and the lane rewound; the coordinator's composition error).
  - `wi-911.toml` D-014 (the narrowed triage: WI ids and dated rulings stay
    in shipped comments).
  - `wi-923.toml` D-001 (round 1's three calls).
  - Still unseen from before: as the 2026-10-15e handoff lists.
- **The three-reviewer trial,** WI-921 round 3 (convergence): round-costing
  0 each (Sol's MAJOR was the checkpoint item); MINORs Sol 0, Fable 3,
  Opus 4, and Opus's merge-commit residue was the one accepted text fix.
  About two more lanes are owed before the trial's call.
- **Still open:** the `wi-880` worktree's uncommitted hook edit, and the
  old `coordinator-tools` folder. OI-98 and OI-105 wait on their conditions.
- **Noted for the queue, not yet filed:**
  - The owner's successor (wi-921 D-014), filed on trunk at WI-921's
    landing: judge a commit against its real parent at the branch-ref
    update (git's reference-transaction hook), covering amends,
    cherry-picks, reverts, rebases, non-conflicting merge commits, hand
    fast-forwards and linked-worktree commits on trunk, with its own scope
    critique and Trust ruling (it would run under `--no-verify`, could
    refuse a fetched fast-forward, and needs git 2.28).
  - Sitting 010's incident (an act committed on a verdict the one parser
    refuses, before the entry point's form check) is evidence for WI-912,
    the verdict/act split: carry it into that row's scope or plan.
  - Shipped text citing this repository's records outside WI-911's change:
    `docs/plans` paths in 13 scripts, review round numbers in about 30, and
    decision ids in 3 (wi-911 D-014).
  - Stale `handback.hand_back` return-route references in the docstrings
    of `spec_move.py`, `intake.py`, `integrate.py` and `dispatch.py`, and
    in an approved LLR's detail (wi-921 D-015; extends the 2026-10-15e
    list's `spec_move.py` item).
  - Carried from the 2026-10-15e handoff's list, unchanged.

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
