# Handoff 2026-10-18c (attended): WI-942 and WI-915 landed; WI-927 through its fix round; three builds in

Overnight: stop

It replaces [handoff-2026-10-18b-attended-coordinator.md](handoff-2026-10-18b-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **Landed this session:**
  - WI-942 (the merge slot reads an acted row's registry from its id) as
    `5790639d4`: the gate's one MAJOR named the act still owed, re-graded
    (wi-942 D-005), and the act turn took act seq 129. The sweep's re-mint
    WI-945 is closed as already settled (`7c0242c9e`).
  - WI-915 (one `docs/stack.ini` reader) as `b120c4722`: both gate reviewers
    APPROVE 0; the rebase touched only RESYNC_PACK (wi-915 D-006); the sweep
    minted nothing.
  - Tips of both are archived to `archive/lanes`.
- **Lanes:**
  - `wi-927` at `9bbcfb351` (base `2268a9a8c`; pre-rebase tip `7d8032e10`
    to archive beside `56d92994a`): intent (P4, Terra's retained session
    `01a14fe5-d655-7423-8395-7a69f1a2f012`) and P5 committed together
    (`3b26e922b`, D-005); counted round 1 filed (Sol 1 MINOR; Opus 2 MAJOR,
    2 MINOR; D-006); fix round 1 committed (D-007). The coordinator's WSL run
    at `9bbcfb351`: the lane's pseudo-terminal cases pass; only two
    `run.command` reds remain, which fail at the base too. Next: counted
    round 2, then the checkpoint (Terra reconciles REVIEW-B F3, a Done-when
    amendment, and F4, SR-229's wording, from
    `C:/Projects/ai-template.wt/review-tmp/2026-10-18c/wi927-fix/spine-changes.md`),
    the combined sitting, the gate, the rebase (re-anchor its RESYNC entry),
    the act, land; at the landing, amend status.md's `hooks --enable`
    mention and WI-897's queued row (the plan's deliverable 6).
  - `wi-943` at `2a37a5c04` (base `b120c4722`; pre-rebase tip `9b168865a`):
    build round 1 (D-001) and intent (P4, Terra's retained session
    `01a15016-4f89-7593-a7f8-6b9726508484`; D-002) committed. Next: counted
    round 1, then on.
  - `wi-925` at `79fce549f`, rebased onto `2268a9a8c` (pre-rebase tip
    `a9a9ad61b`): build stage 1 (P0 to P3, the RESYNC entry begun) is
    **built and uncommitted** in the worktree, backed up as
    `C:/Projects/ai-template.wt/uncommitted-2026-10-18c/wi-925-build1.patch`.
    P0 reproduced, so P4 and P5 go ahead. Before its commit it needs the
    coordinator's rulings on the builder's stop items: `plan_gate._claim_base`
    answers `"HEAD"` for an undeclared trunk on a branch with no claim folder
    (the plan's reorder broke a refresh-merge test; the builder flags the arm
    as close to a fallback, which the owner's no-fallback rule forbids); a
    pinned single-checkout test's assertions changed; four fixture and
    refusal-shape departures; `scripts/check_resync.py` edited to refuse on an
    undeclared trunk; `docs/process.toml` gains `trunk = "refactor_again"`
    (confirm). The smoke tier's one red is the module-size ratchet
    (`agent_common.py` 1073, `bootstrap.py` 1517, `check.py` 1310,
    `integrate.py` 1554), which the commit re-stamps with reasons. Its new
    LLR is tagged `LLR-339` in code; WI-926's build tags `SR-240, LLR-339`
    too: renumber one lane's ids before either mints (an id floor).
  - `wi-926` at `57fdaa33d`, rebased onto `2268a9a8c` (pre-rebase tip
    `0eb9c31c6`): build round 1 (P1 to P9, P11, P12) **built and
    uncommitted**, backed up as
    `C:/Projects/ai-template.wt/uncommitted-2026-10-18c/wi-926-build1.patch`.
    Its commit needs Terra's P10 rows first, since `check_trajectory --strict`
    errors until an LLR names the new `kitlib/commit_hooks` module's CMP (the
    builder proposes CMP-008); its spine change list is beside the patch. The
    smoke tier read 85.0 s, and the build is the cause (the routes test and a
    `git init` per test in about 400 smoke tests): move `test_hooks_on_routes`
    to `SLOW_MODULES` per the plan's rule and re-measure before the commit.
  - Unchanged: WI-798, WI-902, and the landed lanes' branches and worktrees.
- **Watermark** on trunk: WI 945 (WI-945 minted and closed); SR 239,
  LLR 338, IF 296, TC 368, OI 114; acts to seq 129.
- **Strict lints:** clean on trunk and on every lane commit this session.
- **Full suite** at trunk's `b120c4722`: 6297 passed, 22 skipped, 0 failed
  (20 min 40 s, beside builders).
- **No judgement is active**; the lease is handed back at close-out.
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-18c/` holds
  WI-927's fix spine change list (owed at its checkpoint); delete the rest
  once read. `C:/Projects/ai-template.wt/uncommitted-2026-10-18c/` holds the
  two build backups and their spine change lists: delete it once both
  builds are committed.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say: two full-lane
reviewers per round, Codex Sol at medium (REVIEW-A) and Claude Opus at high
(REVIEW-B, launched with the Agent tool's `effort: "high"`), each given
only its rendered brief.

## The queue

The owner's order (coordinator-2026-10-16 D-004, D-006; coordinator-2026-10-17
D-002, D-008). Each row changes machinery, so each lands alone.

| # | Row | Next |
|---|---|---|
| 1 | WI-927 | Counted round 2, checkpoint (F3, F4), sitting, gate, rebase, act, land |
| 2 | WI-943 | Counted round 1, then on |
| 3 | WI-925 | Rule the stop items, re-stamp the ratchet, commit stage 1; stages 2 and 3 |
| 4 | WI-926 | Terra's P10, re-tier the routes test, commit; counted round 1 |
| 5 onward | As before | WI-918, WI-902 (B4), WI-798, then P1 to P8, then leg 03's rows; WI-940 after the batch |

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Decide before the first headless run:** status.md's two launcher
  follow-ups from WI-917's rounds (unchanged).
- **Confirm or overrule:** wi-942 D-004, D-005 (D-005 re-grades the gate's
  MAJOR, an act still owed, as the act turn's to answer); wi-915 D-004 to
  D-006 (D-004: the coordinator fixed the two wording MINORs itself);
  wi-927 D-005 to D-007 (D-005: TC-345 also verifies LLR-300 and its SRs);
  wi-943 D-001, D-002 (D-002: the spec-directed replacements of approved
  phrases); and the ones the 2026-10-18b handoff lists.
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
