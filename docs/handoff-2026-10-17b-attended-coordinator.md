# Handoff 2026-10-17b (attended): WI-928 landed, WI-931 gated and ready to land, WI-912's plan passed

Overnight: stop

It replaces [handoff-2026-10-17-attended-coordinator.md](handoff-2026-10-17-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **Landed this session:** WI-928 as `01a50050e`, on a quiet reading the
  owner gave (bar 2623 passed, budget 46.7 s), its RESYNC entry
  re-anchored at the squash (coordinator-2026-10-17 D-003). Its re-mint
  WI-938 closed as settled by the lane's sitting 003 and act 124
  (`2b2350add`).
- **The box:** the owner's own test runs loaded it for most of the
  session. Lane bars read 140 to 1832 s at below-normal priority, each
  beside its parent in the same window (owner, in session: follow
  coordinator-2026-10-16 D-012 as is). A landing still needs a quiet
  reading: ask the owner first.
- **Lanes:**
  - `wi-931` (the session kill drops its guards): rebased onto
    `2b2350add` (wi-931 D-005); P0's legs re-ran at that base and P7's
    at each new tip, all matching the plan's table; P8's records and
    verdict line are in the fragment. Counted round 1 (001 Sol
    CHANGES-REQUESTED 1 MAJOR, re-graded as answered by the checkpoint;
    002 Opus APPROVE 2 MINOR; D-006), the comment MINOR fixed, the
    checkpoint with the reconcile omitted (D-007), sitting 003 blessing
    SR-238, LLR-026 and TC-026 (act seq 125, `dfa037efa`), the
    convergence map (D-008), and the gate over the checkpoint tip `07bbfafcc` in convergence stance
    (004 Sol APPROVE 0; 005 Opus APPROVE 1 MINOR, a wording follow-up now
    in status.md's unfiled list; D-009), filed at `bb3acd1e2`. **Ready to
    land** on a quiet reading. At the landing: re-anchor its RESYNC entry
    at the landing's parent (002's F2), and archive the rebased tip with
    the pre-rebase tips the verdicts cite, none of them reachable today:
    `4e6b1318f`, `8b2b4870a` (it reaches critique 2's `7a4e14ce8`) and
    `db45cd9b9` (critique 1's).
  - `wi-912` (an adjudication sitting ends at its verdict): cut at
    `2b2350add` (wi-912 D-001); its single plan (DELTA within), the
    critique (Sol, one MINOR read as an APPROVE, adopted through the build
    brief: name P11's composed brief and pass `--brief-file`; D-002) and
    the pass record (`9169e850c`) are committed. **Next: dispatch the
    first build** (the plan's stages, one builder, stopping where the plan
    orders commits). It takes acts later: rebase it after WI-931 lands
    and check `acts.toml` for a duplicate seq.
  - `wi-929`: claimed, no commits, no worktree; move it to trunk's tip
    before cutting it (recipes section 2).
  - Unchanged: `wi-915`, `wi-916`, WI-798, WI-902, and the landed lanes'
    branches and worktrees.
- **Scope critiques:** the marking rows' confirming rounds both read
  APPROVE with no findings (WI-917 and WI-918, recorded in their specs'
  dispositions); each is claimable once the row it hard-needs is done.
- **Watermark** on trunk: WI 938; SR 239, LLR 337, IF 295, TC 367, OI 114;
  acts to seq 124 (WI-931's in-lane act 125 lands with it).
- **Strict lints:** clean on trunk and on every lane commit this session.
  The full suite at trunk's `2b2350add` (WI-928's landing and WI-938's
  close): 6019 passed, 22 skipped, 0 failed (24 min 23 s, below normal
  priority, on the loaded box).
- **No judgement is active**; the lease is handed back at close-out.
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-17-coord/`
  (per-lane folders, `lowprio.py`, WI-931's leg scripts and logs, its
  `parent-wt` detached worktree). Keep it until WI-931 lands.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say: two full-lane
reviewers per round, Codex Sol at medium (REVIEW-A) and Claude Opus at high
(REVIEW-B, launched with the Agent tool's `effort: "high"`), each at
below-normal priority while D-012 holds.

## The queue

The owner's order (coordinator-2026-10-16 D-004, D-006; coordinator-2026-10-17
D-002). Each row changes machinery, so each lands alone.

| # | Row | Next |
|---|---|---|
| 1 | WI-931 | Land it on a quiet reading (gated; re-anchor its RESYNC entry, archive the cited pre-rebase tips) |
| 2 | WI-912 | Dispatch the first build from the passed plan |
| 3 | WI-929 | After WI-912 (its soft edge); `none` |
| 4 | WI-917, WI-916, WI-915 | WI-917 is critique-confirmed; claim it once WI-912 is done |
| 5 | WI-925, WI-926, WI-927 | The hook rows, critique-clean |
| 6 onward | As before | WI-902 (B4), WI-798, then P1 to P8 with WI-918 (critique-confirmed), then leg 03's rows |

## For the owner

- **A quiet box** for WI-931's landing reading (D-012).
- **Push** `refactor_again` and `archive/lanes`.
- **Confirm or overrule:** coordinator-2026-10-17 D-003; wi-931 D-005 to
  D-008; wi-912 D-001 and D-002; and the ones the 2026-10-17 handoff
  lists (coordinator-2026-10-17 D-001, wi-935 D-001 to D-005, wi-928
  D-002 to D-005, wi-931 D-003 and D-004, and earlier unseen ones).
- **Still open from earlier handoffs:** the convergence-tag question; the
  `wi-880` worktree's uncommitted hook edit; the old `coordinator-tools`
  folder; OI-98 and OI-105, each waiting on its condition.

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
