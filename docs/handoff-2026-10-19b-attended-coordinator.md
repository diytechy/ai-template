# Handoff 2026-10-19b (attended): WI-925 and WI-926 rebased onto trunk's tip; the queue turns to headless legs

It replaces [handoff-2026-10-19a-attended-coordinator.md](handoff-2026-10-19a-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The owner asked this short attended
session for the two lanes' rebases only, then the launcher: like the last
handoff it carries no `Overnight: stop` line (owner, coordinator-2026-10-18
D-006), so the owner starts `scripts/coordinator/overnight_legs.py` and the
queue below runs in headless legs (the skill's section 7).

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** no landing this session. Its only commit is this close-out
  (docs, and the recipes' rebasing lessons).
- **Lanes** (every one committed, its tree clean), both now based on
  trunk's `342bd95ef`:
  - `wi-925` at `5f896e3b3`, pre-rebase tip `81d271c6d` (archived at
    landing beside `a9a9ad61b`); D-005 records the rebase. Stage 1 (P0 to
    P3) and stage 2 (P4 to P8) committed (its D-001 to D-004; the owner's
    two calls in D-002: keep the plan gate's undeclared-trunk arm, and
    declare `trunk = "refactor_again"`). Next: stage 3, Terra's first turn
    for P9 (the new LLR-339 and TC-369, LLR-307, LLR-208, TC-325, IF-179,
    IF-189, IF-286, LLR-337's detail, whether LLR-156's `code_symbol` takes
    `declare_scaffold_trunk`, and the claim-relink residue its D-004 flags),
    from `C:/Projects/ai-template.wt/review-tmp/2026-10-18d/wi925-s2/`
    (`stage1-spine-changes.md` and `spine-changes.md`); then P10's RESYNC
    completion; then counted round 1. The rebase replayed with two
    conflicts (RESYNC_PACK, the module-size ratchet); the ratchet is
    re-stamped against trunk's numbers with the lane's reasons.
  - `wi-926` at `93a141a9e`, pre-rebase tip `d15adb2de` (archived at
    landing beside `0eb9c31c6`); D-004 and D-005 record the rebase and
    its slow-tier fallout. Build round 1 and intent committed (its D-001
    to D-003); Terra's retained session
    `01a15060-3db9-7d72-9752-9100bf897959`. Next: counted round 1. The
    rebase resolved eleven conflicts. LLR-300's detail now keeps WI-927's
    approved sentence and this lane's addition side by side (the lane's
    first, in the take's code order), for the checkpoint to judge. Trunk's
    new take test now builds a hooked checkout, and `max-tests` is
    re-stamped 2825 to 2970. In the slow tier, three rebase interactions
    are fixed in tests (D-005): WI-927's console take cases and the
    launcher fixture's `prepare_run` fake.
    **Owed by round 1's builder, before the landing's bar:**
    - `test_done_when_blessing.py::test_the_scaffold_hooks_floor_resolves_and_passes_on_a_clean_tree`
      fails at the pre-rebase tip too (D-005): the lane's `_init` calls
      `hooks_on`, whose stubs overwrite the scaffold's own pre-commit
      hook, so the test reads a stub.
    - The tier cost (D-004): the rebased tier reads above trunk's in
      adjacent runs (102.2 s against 86.3 s, 118.6 s against
      95.1 s, then 233.2 s against 133.1 s), where at its old base it
      read at its parent's. The lane's hooked-checkout fixtures run git
      per test, and three smoke modules about double. The builder
      re-tiers, or has a fixture that already fakes the kit's shared
      readers fake the hooks reader too.
  - The two lanes still share many files (integrate.py, agent_loop.py, the
    shipped pre-commit hook, RESYNC_PACK, the ratchet and a dozen test
    modules): the second to land rebases onto the first (recipes section 4).
  - Unchanged: WI-798, WI-902, and the landed lanes' branches and
    worktrees (`wi-946` among them, archived).
- **Id floor** (wi-925 D-003, wi-926 D-002), unchanged: wi-925 holds LLR-339
  and TC-369; wi-926 holds SR-240, LLR-340, TC-370 and IF-297, and its
  rebased watermark reads SR 240, LLR 340, IF 297, TC 370, WI 950.
- **Watermark** on trunk, unchanged: WI 950; SR 239, LLR 338, IF 296, TC 368,
  OI 114; acts to seq 134.
- **Strict lints:** clean on trunk and on both lanes' new commits.
- **Tests this session** (no trunk code changed, so no full suite was run;
  the last stands, 6437 passed at `bba694e69`): wi-925's tier 2813 passed,
  0 failed, and trunk's 13 changed test modules on it 753 passed, 0 failed;
  wi-926's tier 2836 passed, 0 failed, and trunk's and its own changed
  test modules on it 1892 passed, 4 failed (three fixed in D-005, then
  80 passed over their two modules; the fourth is the lane's own, above).
  wi-925's own 25 changed test modules on it 1117 passed, 0 failed.
- **No judgement is active**; the lease is handed back at close-out.
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-19a/` holds
  this session's bar logs; nothing in it is owed. Its detached `parent-wt`
  and `old926-wt` worktrees are removed at close-out. The 2026-10-18d root keeps only
  `wi925-s2/`, owed at WI-925's P9.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say: two full-lane
reviewers per round, Codex Sol at medium (REVIEW-A) and Claude Opus at high
(REVIEW-B, launched with the Agent tool's `effort: "high"`), each given
only its rendered brief.

## The queue

The owner's order (coordinator-2026-10-16 D-004, D-006; coordinator-2026-10-17
D-002, D-008), turned toward headless runs (coordinator-2026-10-18 D-004,
D-006). Each row changes machinery, so each lands alone.

| # | Row | Next |
|---|---|---|
| 1 | WI-925 | Stage 3: Terra's P9, P10; counted round 1 |
| 2 | WI-926 | Counted round 1 (its builder answers D-004's tier cost before the landing) |
| 3 onward | As before | WI-897 (amend its queued row first, per WI-927's plan deliverable 6), WI-902 (B4), WI-798, then P1 to P8, then leg 03's rows; WI-940 after the batch |

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).
A leg brings an owner-held step to a safe point and lists it under the next
handoff's "For the owner". A leg continues the lanes claimed attended (rows
1 and 2) as they stand, with no re-claim. Its first loop-writer commit
opens the lane's trailer window, the attended commits before it, this
session's rebase commits among them, stay exempt, and `check-lane` passes
them at landing (coordinator-2026-10-18 D-006). The next machinery lane
lands only after a headless leg has run under WI-946's launcher (the
skill's landing rule).

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Start the overnight launcher**, `scripts/coordinator/overnight_legs.py`
  (its docstring states the options; `--dry-run` launches no leg). This
  handoff carries no stop line.
- **Confirm or overrule:** wi-925 D-005 and wi-926 D-004 and D-005 (the
  rebases; D-004 also re-stamps `max-tests`, and D-004 and D-005 edit
  three of trunk's new tests to build a hooked checkout or the
  launcher's new shape); and
  the ones the 2026-10-19a handoff lists (wi-946 D-010 to D-012; wi-918
  D-005 to D-008; wi-946 D-005 to D-009; wi-943 D-006 to D-008; wi-918
  D-001 to D-004; wi-946 D-001 to D-004; and the 2026-10-18e list).
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
