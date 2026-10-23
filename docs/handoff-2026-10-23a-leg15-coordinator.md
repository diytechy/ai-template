# Handoff 2026-10-23a (headless leg 15): WI-850 landed

It replaces [handoff-2026-10-22d-leg14-coordinator.md](handoff-2026-10-22d-leg14-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 15 (loop session
`20261021T045653Z-213020`, coordinator session
`03270a70-1d76-469b-a1ed-77649dd6cc3d`) claimed WI-850 alone, settled
SR-224's chain in its own act, built, reviewed and judged the row, and
landed it alone. It carries no `Overnight: stop` line: the next rows move
without the owner.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** the scoped unpause (`413f1d825`), the claim (`4352a8635`) and
  the byte-identical restore (`ad67e4b3f`), then WI-850's landing
  (`90ddd6f5f`, acts seq 154 and 155), then this close-out. The full suite ran once at `90ddd6f5f`: 7246 passed, 33 skipped in 19:11.
- **WI-850 is closed.** Its spec is archived
  (`docs/archive/work/complete/WI-850-child-approved-after-parent.md`), its
  lane tip is in `archive/lanes`, the sweep minted nothing, and the four
  spine registries equal their anchors. Its worktree
  `C:/Projects/ai-template.wt/wi-850` and branch remain; nothing reads
  them. As a machinery change (a new pre-commit step and a third
  lane-commit rider), its step has run once: the `parent-first` step ran
  at the landing commit and passed. The next lane's commits and acts meet
  it; an act that flips a child before its parent is now refused.
- **Lane `wi-963`:** unchanged, holds for the owner (OI-115). It holds
  LLR-342 and TC-373. Its rebase onto this trunk meets two things: the
  two-tree reader `_tier_reads`, which WI-850 carried byte-identical but
  for its `Implements:` line (one conflicting line), and
  `acceptance_record.py` at 998 SLOC, so the rebased file crosses the
  1000-SLOC ratchet and needs the ruling WI-850's plan R1 names (a
  reviewed baseline entry, or a decomposition).
- **Watermark** on trunk: WI 972, SR 246, LLR 358, IF 308, TC 397, OI 115;
  acts to seq 155.
  - Lane-held: wi-963 LLR-342 and TC-373.
  - A new lane's Terra floor is SR-247, LLR-359, TC-398 and IF-309.
- **Usage:** this close-out's ingest recorded this session and its five
  sub-agents (spooled), and leg 14's tail (unchanged); both runs exited 0.
  The next close-out passes `--session 03270a70-1d76-469b-a1ed-77649dd6cc3d`.
- **Strict lints:** clean on trunk. **No judgement is active**;
  `docs/work/pause` is tracked and unchanged.
- **Scratch:**
  - `C:/Projects/ai-template.wt/review-tmp/2026-10-22e-leg15/` may go:
    WI-850's results are recorded (its arms maps and the builder's stage
    notes are there if wanted).
  - `C:/Projects/ai-template.wt/review-tmp/2026-10-22d-leg14/` and
    `2026-10-21-leg11/` may go: WI-850 has landed.
  - Keep the leg-07 root until WI-963 lands.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say, through the route:

- Two full-lane reviewers run per round: Codex Sol at medium (REVIEW-A,
  `codex_call.py REVIEW-A`) and Claude Opus at high (REVIEW-B, launched
  with the Agent tool's `effort: "high"`). Each gets only its rendered
  brief.
- In a headless leg, launch REVIEW-B first.
- Every render refuses a tip with no attested review bar for its
  `--tests`, so attest the tip first.

## The queue

The owner's order (coordinator-2026-10-16 D-004, D-006; coordinator-2026-10-17
D-002, D-008), turned toward headless runs (coordinator-2026-10-18 D-004,
D-006), with the owner's 2026-10-20 rulings (coordinator-2026-10-20 D-008 to
D-019) and coordinator-2026-10-21 D-004 to D-006. Each row that changes
machinery lands alone, after the cycle has run through the last landing's
changed steps (WI-850 changed the commit hook and the slot's riders: the
next lane's commits and act turn run through them).

**Only the rows in this table are claimed**, in order and under their
`needs`. When no row in it can move without the owner, the leg closes out
with the `Overnight: stop` line.

| # | Row | Next |
|---|---|---|
| 1 | WI-963 | Held: OI-115 (the owner); its rebase needs the module-size ruling above |
| 2 | WI-851, WI-856, WI-878, WI-910, WI-920 | Under their `needs`, each scope-critiqued at its claim (WI-910 as split by D-019); WI-851 (held-rung rows protected by state) is next |
| 3 | Filings P3 to P6, P8 | P3 ends in an owner act. P4 and P5 may file; P5's spec asks D-009's question (does the WI space ride the carrier?) and folds in WI-810's "sequential sittings never collide on an id". P6 starts with the W3 dry run. P8 waits on its filing calls |
| 4 | WI-966 | Scope critique and its confirming round, then the claim; it lands before item 10 step 5 |
| 5 | WI-971 | Scope critique at its claim; it touches the hook and slot walk WI-969 added, so it lands alone |

**Never claimed by a leg:** WI-684 (waits on OI-98, the owner's re-sync),
WI-795 (OI-105, then WI-820), WI-908 (the owner present), WI-964 (the
owner's Mac), WI-827 (attended only; it never lands from a lane), WI-967
(OI-115's placeholder), and every row under `docs/work/deferred/` (D-011,
D-016).

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).

## For the owner

- **Rule OI-115** (WI-963's settlement fix; recommendation (a)). It holds
  WI-963 at its gate tip; its rebase will also need a module-size call
  (above).
- **Confirm or overrule:**
  - coordinator-2026-10-22 D-004 (WI-850 claimed alone);
  - wi-850 D-002 (high risk): SR-224's chain settled by approving SR-224,
    not by demoting LLR-281 and TC-291; its Requirement now reads "The kit
    shall hold every skill description to the declared description
    floor: the descriptions it ships are at or above it, and its
    skills-index check fails, naming the skill, on any description
    shorter than it" (sittings 001 to 003);
  - wi-850 D-008: round 1's one MAJOR (the set's sitting owed) re-graded
    to the checkpoint, costing no fix round;
  - wi-850 D-009: SR-245 split into the standing finding (SR-245) and
    commit admission (SR-246), and the coordinator's byte-level edits to
    two LLR details before their sitting;
  - wi-850 D-010: an independent arms map's 6 gaps closed before the
    sitting by eleven characterization tests and Terra's wording;
  - wi-850 D-001, D-003 to D-007, D-011, D-012.
- **Still open from the last handoff**, every item it listed:
  - coordinator-2026-10-22 D-002 and D-003, wi-961 D-010 to D-017 and the
    earlier items that handoff carried;
  - the `--wi` primary-checkout preflight call (wi-960 D-016);
  - removing the temporary `Bash(codex exec *)` allow rule;
  - your owner-held rows.
- **Push** `refactor_again` and `archive/lanes`.

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
