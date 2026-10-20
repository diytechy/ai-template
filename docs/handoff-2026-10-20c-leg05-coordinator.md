# Handoff 2026-10-20c (headless leg 05): WI-955 and WI-956 landed

It replaces [handoff-2026-10-20b-leg04-coordinator.md](handoff-2026-10-20b-leg04-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. This was the fifth headless leg
under WI-946's launcher (loop session `20261019T185432Z-8e4f05`). It filed
queue row P1 (review-churn item 13's review gate) as four rows, and landed
the first two. Like the last handoff, it carries no `Overnight: stop` line:
the next row moves without the owner.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** `155a621bb` files WI-955 to WI-958; `79f0567e3` and
  `d83ab4512` record their scope critiques and confirming rounds;
  `046117078`, the claims and `72c81fcdb` are the scoped unpause for
  WI-955 and WI-956. `be80354d9` lands WI-955 (squash of wi-955);
  `ed84e2510` lands WI-956 (squash of wi-956); `ccd9881f3` mints its
  re-mint WI-959 and `c1c1ac918` closes it as already settled (act 143).
  The close-out commit follows. `archive/lanes` is at `55ee4e624`: both
  lanes' tips (wi-955 `3a4faf00c`, wi-956 `746f871de`; neither rebased
  after a verdict).
- **What the two landings change for every later session:**
  - **Lanes run test cases before code** (WI-955; coordinator-cycle SKILL
    §3 "Intent"): Terra's intent turn authors the whole set, TC rows
    included, before build round 1 (a `single` row after its pass
    record), from the spine brief's new intent form; round 1's first
    commit is the tests, each new behaviour as a strict expected
    assertion failure; the code commit removes the marks. The reviewer
    template now asks the three test-adequacy questions and the
    duplication question.
  - **One bar attestation grammar** (WI-956): `Bar-Green:` now carries
    `bar=<review|landing|no-bar>` and `tests=<digest|none>`; the refresh
    writes `bar=landing` (or `no-bar`) through the one producer, and
    `integrate.py attest --branch <b> --bar review --tests <files...>`
    writes a `review` record. A lane refreshed before `ed84e2510` carries
    the old trailer, which is no longer read: it refreshes again. Nothing
    yet refuses a review without a `review` record: that is WI-957.
  - `docs/stack.ini` `[bars] review` names the run menu's smoke action,
    with no default (coordinator-2026-10-20 D-002).
- **Lanes:** none open. `wi-955` and `wi-956` branches and worktrees
  remain, archived.
- **Watermark** on trunk: WI 959; SR 240, LLR 340, IF 297, TC 370, OI 114;
  acts to seq 143.
- **Strict lints:** clean on trunk.
- **Tests this leg:** the full unfiltered suite at `c1c1ac918`, from a
  detached scratch checkout: 6723 passed, 28 skipped, 0 failed (16 min 57
  s). Both landings' bars on the staged squash: every lint green, the tier
  over its 60 s budget beside an equal parent reading on the loaded box
  (owner, 2026-10-17).
- **No judgement is active**; the lease is handed back at close-out.
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-20c-leg05/`
  holds this leg's drafts, briefs, verdicts and bar logs, and two detached
  worktrees (`parent-wt`, `full-wt`; remove with `git worktree remove`).
  Nothing in it is owed; it may be deleted, as may the leg 04 root.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say: two full-lane
reviewers per round, Codex Sol at medium (REVIEW-A) and Claude Opus at high
(REVIEW-B, launched with the Agent tool's `effort: "high"`), each given
only its rendered brief.

## The queue

The owner's order (coordinator-2026-10-16 D-004, D-006; coordinator-2026-10-17
D-002, D-008), turned toward headless runs (coordinator-2026-10-18 D-004,
D-006). Each row that changes machinery lands alone, after the cycle has
run through the last landing's changed steps.

| # | Row | Next |
|---|---|---|
| 1 | WI-953 | WI-902's disposition, after the owner routes the plan cap's FIX (below) |
| 2 | WI-957 | Ready (its needs WI-956 landed); scope critique and confirming round already APPROVE 0: claim under one scoped unpause, then the single plan, Terra's intent set, tests first, the rounds. From its landing every coordinator review render refuses an unattested tip, so the recipes' commit step becomes `integrate.py attest` |
| 3 | WI-958 | After WI-957 lands (hard edge); scope critique and confirming round already APPROVE 0 |
| 4 onward | As before | P2 to P8, then leg 03's rows; WI-940 after the batch |

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).
Row 1 waits on the owner, so a leg starts at row 2.

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Route WI-902's plan-cap FIX** (wi-902 D-011): a third plan revision
  that takes sitting 016's ruling, or another route. WI-953, its
  disposition row, waits on that choice.
- **Confirm or overrule:** coordinator-2026-10-20 D-001 to D-003, wi-955
  D-001 to D-006 and wi-956 D-001 to D-010. The riskiest: **D-002** (high
  risk): WI-956's review bar is a new required key with no default, a
  forced downstream migration that the RESYNC entry states; D-001, P1 split
  at birth into four rows; D-003, WI-958's hard edge on the unfiled P4
  rejected (P4's own spec must carry WI-958's gate across the batch's
  retirement); wi-956 D-004, the interface data cells re-graded from a
  MAJOR to the checkpoint; and wi-955 D-003 and wi-956 D-003, a fix round's
  two stages run in one builder dispatch. Also the earlier lists: wi-798
  D-010 to D-024, wi-897 D-001 to D-007, wi-902 D-011,
  coordinator-2026-10-19 D-003 and D-004, and the ones before them.
- **The named-tests `--basetemp`** (status.md's follow-ups): `attest`
  appends pytest's flag to an adopter's `[product] test`, as WI-956's spec
  mandated; a non-pytest adopter's `attest --tests` is red. Yours to
  choose: a declared placeholder the adopter opts into, or a pytest-only
  note in the template.
- **SR-227's wording:** unchanged from the last handoff (its credential
  clause names a dedicated CLI home no family has now).
- **Still open from earlier handoffs:** the convergence-tag question; the
  `wi-880` worktree's uncommitted hook edit; the old `coordinator-tools`
  folder; the optional guard-matcher reinstall; OI-98, OI-105 and OI-114,
  each waiting on its condition.

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
