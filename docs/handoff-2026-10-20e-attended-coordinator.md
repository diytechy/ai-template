# Handoff 2026-10-20e (attended): the owner's consolidation rulings; WI-963 filed

It replaces [handoff-2026-10-20d-leg06-coordinator.md](handoff-2026-10-20d-leg06-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. After headless leg 06 closed the
overnight run (`--max-legs 6 reached`), an attended session took the
owner's rulings on four rows of the WI-788 program that later review-churn
rulings had overtaken, from a read-only consolidation drill, and applied
them in one records-only commit. Two independent reviews of that commit
(Codex Sol and Claude Opus, both medium) and a queue audit followed; their
verified findings and a second round of owner rulings cleaned the queue
(coordinator-2026-10-20 D-013 to D-020). No lane moved. It carries no
`Overnight: stop` line: WI-962, WI-963 and WI-940 move without the owner.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** `08fc2fb2f` applies the rulings (coordinator-2026-10-20 D-008
  to D-012); the close-out commit follows. `archive/lanes` is unchanged.
  - **WI-953** (WI-902's disposition) now carries the owner's route under
    "Owner route" (D-008): a third plan revision taking sitting 016's FIX,
    one confirming critique in convergence stance, then the build. Its
    sitting drafts that successor; it no longer waits on the owner.
  - **WI-963** is new (D-009): the trunk mint never mints an amendment row
    for a row the merged range already settled (the S11 plan's section 4.2
    filter). Its scope critique runs before its claim.
  - **WI-810** and **WI-807** are cancelled (D-009, D-010); WI-808 gains the
    fenced-lock line and drops its WI-807 edge; WI-812 and WI-813 drop
    their WI-810 edge (D-012).
  - **WI-817** is deferred (D-011): it folds into item 10's config program
    as its first row and returns to queued/ when item 10's steps 3 to 6 are
    filed.
  - **Round 2** (D-013 to D-020): WI-963's spec corrected from both reviews
    (absence reads as no acts, whole-row comparison, anchored on SR-178);
    the recipes gain the Owner-route append for a disposition sitting;
    WI-940 re-scoped in place (D-014: no bar fails on seconds, the run
    menu's audit judges them); WI-906 cancelled as contrived (D-015);
    sixteen rows deferred for the owner's review of their re-scopes (D-016:
    WI-799, WI-800, WI-801, WI-804, WI-805, WI-808, WI-809, WI-811 to
    WI-816, WI-832, WI-833, WI-857); WI-795 needs WI-820 (D-018); WI-910
    split, its Mac run filed as WI-964 (D-019). WI mark 964.
- **Lane `wi-957`** (worktree `C:/Projects/ai-template.wt/wi-957`, base
  `64b8d686c`, tip `804c8011c`): plan `7f3833550`, critique-1 APPROVE 0
  `d0411d424`, pass record `85a68024a`; Terra's intent set `9015acd72`
  (SR-241, LLR-341, TC-371, TC-372, all Drafted; Terra session
  `01a15b92-e996-71b1-98c6-f8a280edc55e`); the tests first, twelve strict
  xfail cases `6fe5e26a9`; the code, the skill text and one RESYNC entry
  (anchored `[since 64b8d686c]`) `804c8011c`. No review has run. The
  review render on the lane now refuses its own tip, as designed: it
  carries no `review` attestation. `integrate.py attest` refused the code
  commit because the smoke tier ran 96.9 s against its 60 s budget, every
  test green (wi-957 D-003). On this box the tier reads 70 to 112 s
  whatever else runs, so the lane held for the owner (wi-957 D-004). The
  owner ruled it on 2026-10-20 (coordinator-2026-10-20 D-014): no bar fails
  on seconds, WI-940 carries the change and lands first. After WI-940
  lands: rebase WI-957 onto trunk and re-anchor its RESYNC entry, then an
  attest with nothing staged writes the empty attestation commit; then
  counted round 1.
- **Lane `wi-962`** (worktree `C:/Projects/ai-template.wt/wi-962`, base
  `e79075c46`, tip `1bd47e778`): plan `96c6e7040`, critique-1
  (CHANGES-REQUESTED, one MINOR, read as an approve) `3581b5726`, pass
  record `a218281e1`; Terra's intent set `899b9b97f` (SR-031, LLR-021,
  TC-021, TC-031 and IF-037 amended, IF-298 new; Terra session
  `01a15c29-40f7-7da2-9b33-22e70f939abf`); the tests first, 72 strict xfail
  cases `1bd47e778`. Claimed by headless leg 06, so it lands headless.
  **Next:** the code stage, the plan's P2 to P4, P5's non-registry parts
  (`docs/runtime-flows.md` Flow 3, the prose claims, the contract bodies)
  and P6's RESYNC entry, with the marks removed. Points for that builder's
  brief, from the test builder (wi-962 D-002): the unreadable refusal must
  say `cannot be read or parsed`, and the failed-read refusal must name
  `check_privacy.py` and `--hook-policy`; `test_meta_repo_hook` asserts
  that `KIT_SCRIPTS_DIR` appears in `hooks/pre-commit`, so either a comment
  there survives or the test's subject moves to `kit-python.sh`. Three
  tests tag a TC whose evidence does not list them (the review posture
  test and the no-text-read pin under TC-031, the bootstrap test under
  TC-021): the checkpoint's reconcile. Then counted round 1, both
  reviewers. Its reviews render through trunk's `review_brief.py`, which
  has no attestation gate yet.
- **Strict lints:** clean on trunk.
- **Watermark** on trunk: WI 963; SR 240, LLR 340, IF 297, TC 370, OI
  114; acts to seq 143. Lane-held ids: wi-957 holds SR-241, LLR-341,
  TC-371 and TC-372; wi-962 holds IF-298. A later lane's Terra takes these
  as its floor.
- **Tests this session:** the commit bar on the records-only commit: both
  strict lints clean, 2969 passed, 3 skipped; the budget step read 403.1 s
  against 60 s (load; coordinator-2026-10-17 D-011). No code changed, so
  no full suite ran.
- **No judgement is active**; the lease is handed back at close-out.
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** the consolidation drill, the queue audit, both reviews and
  the ruling notes are at `C:/Projects/ai-template.wt/review-tmp/2026-10-20e-consolidation/`
  (`consolidation-drill.md`, `queue-audit.md`, `sol-review.md`,
  `opus-review.md`, `owner-rulings-2026-10-20.md`); keep them until the
  deferred rows' re-scopes are reviewed. The leg 06 scratch root's
  `p8-draft/` is still kept until P8 is filed.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say: two full-lane
reviewers per round, Codex Sol at medium (REVIEW-A) and Claude Opus at high
(REVIEW-B, launched with the Agent tool's `effort: "high"`), each given
only its rendered brief.

## The queue

The owner's order (coordinator-2026-10-16 D-004, D-006; coordinator-2026-10-17
D-002, D-008), turned toward headless runs (coordinator-2026-10-18 D-004,
D-006), with the owner's 2026-10-20 rulings (coordinator-2026-10-20 D-008 to
D-019). Each row that changes machinery lands alone, after the cycle has
run through the last landing's changed steps.

**Only the rows in this table are claimed**, in order and under their
`needs`. When no row in it can move without the owner, the leg closes out
with the `Overnight: stop` line. The superseded "leg 03's rows" table is
retired.

| # | Row | Next |
|---|---|---|
| 1 | WI-962 | In its lane: the code stage, then the rounds, the checkpoint, the gate and the landing |
| 2 | WI-963 | The first new build (D-009): scope critique and its confirming round (its Trust ruling is D-020, for the owner to confirm), then claim under one scoped unpause. Touches `intake.py`; lands alone |
| 3 | WI-940 | Re-scoped by the owner (D-014): scope critique over its `## Owner re-scope` and the confirming round, then claim (single plan). Changes both bars' budget step; lands alone, and releases WI-957 |
| 4 | WI-953 | WI-902's disposition sitting on the owner's route (D-008): compose the `disposition` brief, then append the row's `## Owner route` section verbatim, chained with `&&` (recipes section 1, Adjudication step 1), and check the brief carries it. Then the successor it drafts: the third plan revision, one confirming critique, the build, before P4 and P5 |
| 5 | WI-957 | After WI-940 lands: rebase onto trunk, re-anchor its RESYNC entry, the empty attestation commit, counted round 1 |
| 6 | WI-958 | After WI-957 lands (hard edge) |
| 7 | WI-960, then WI-961 | Cleared for a claim; built after WI-957 lands (WI-960's soft edge: the same review steps) |
| 8 | WI-850, WI-851, WI-856, WI-878, WI-910, WI-920 | Under their `needs`, each scope-critiqued at its claim (WI-910 as split by D-019) |
| 9 | Filings P3 to P6, P8 | P3 ends in an owner act; P4 and P5 after WI-953's successor lands (P5's spec asks D-009's question: does the WI space ride the carrier, and folds in WI-810's "sequential sittings never collide on an id"); P6 starts with the W3 dry run; P8 waits on its filing calls |

**Never claimed by a leg:** WI-684 (waits on OI-98, the owner's re-sync),
WI-795 (OI-105, then WI-820), WI-908 (the owner present), WI-964 (the
owner's Mac), WI-827 (attended only; it never lands from a lane), and every
row under `docs/work/deferred/` (D-011, D-016).

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).

## For the owner

- **Review the deferred rows' re-scopes** (D-016): the drill file under
  Scratch drafts one per row. Each returns to queued/ with its re-scope
  applied. The two that gate the managed loop's unpause are WI-809 (cut to
  the loop's act turn) and P4.
- **Your owner-held rows:** WI-827 (SN-029's amendment: the text, then your
  act), WI-908, WI-964 (your Mac, after WI-910 lands), and WI-684 and
  WI-795 behind their open items.
- **Confirm or overrule** coordinator-2026-10-20 D-012, D-013 and D-020
  (high risk: WI-963's Trust ruling); D-008 to D-011 and D-014 to D-019
  are your own rulings.
- **P8's filing calls** (drafts in the scratch root's `p8-draft/`, split
  three ways: the test-file TC tag and its one reader; the derived review
  test set and its refusals; the strict-mark commit check): the tag
  token (the drafter proposes the existing `Implements:` line); two forced
  downstream migrations (the tags, and a new required `[bars] red_mark`
  key); and refusing a code-touching row that names no SR (8 of 36 open
  rows today).
- **Push** `refactor_again` and `archive/lanes`.
- **Confirm or overrule:** coordinator-2026-10-20 D-004 to D-007 (high
  risk: **D-005**, WI-960's three filing calls, the spool for a call
  outside a lane among them; **D-006**, WI-962's refusal of an unparseable
  policy file at the hooks, a forced change for adopters); wi-957 D-001 to
  D-004; wi-962 D-001 and D-002. Still open from the last handoff:
  coordinator-2026-10-20 D-001 to D-003 (D-002 high risk), wi-955 D-001 to
  D-006, wi-956 D-001 to D-010, and the lists before them.
- **The named-tests `--basetemp`**, **SR-227's wording** and the items
  still open from earlier handoffs: unchanged from the last handoff.

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
