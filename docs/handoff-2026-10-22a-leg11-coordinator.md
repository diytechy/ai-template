# Handoff 2026-10-22a (headless leg 11): WI-969 landed; WI-960 building

It replaces [handoff-2026-10-21d-leg10-coordinator.md](handoff-2026-10-21d-leg10-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 11 (loop session
`20261021T045653Z-213020`) planned, built, reviewed, sat and landed WI-969,
closed its re-mint, filed one successor row, and took WI-960 from its P0
through P3. It carries no `Overnight: stop` line: WI-960 moves without the
owner.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** WI-969 landed as `802f72327` (act seq 149: SR-148, LLR-153,
  LLR-161, LLR-312, TC-147, TC-156, TC-254 re-attested; act seq 150:
  LLR-335, LLR-345, TC-360, TC-383 approved). A disposition can adopt an
  already-filed successor; the close records it, and the pre-commit hook's
  new `adoption-record` step and the merge slot's rider judge every record.
  Its re-mint WI-970 closed as already settled (`987d9fcc0`); WI-971 filed
  (`4c418cd53`, the consolidation MINORs every WI-969 round raised).
  `archive/lanes` holds WI-969's rebased and pre-rebase tips. The full
  suite ran once at `4c418cd53`: 7065 passed, 33 skipped (3248.61 s on a
  box other sessions loaded).
- **Lane `wi-960`** (worktree `C:/Projects/ai-template.wt/wi-960`, rebased
  onto `4c418cd53`, tip `4ea5f3122`): P0's spec amendment is committed and
  confirmed (Sol, convergence stance, APPROVE findings=0); P1's intent set
  (Terra, retained session `01a16357-3fd5-7460-b031-56c1fba9eca3`: SR-243
  derived, LLR-346, TC-384, TC-385; LLR-269, TC-265, IF-246 amended by
  addition), P2's tests and P3's service are committed, each attested.
  **Next:** settle wi-960 D-005's open point first (the shipped
  `gitignore.template` does not ignore `out/sessions/`, so a downstream
  repository's first spooled log dirties the primary checkout and freezes
  claims): in the lane with a regression test and a Deliverables
  amendment outside the Done-when, or as its own row landing first
  (skill §3, Iterate step 8); record the call. Then P4 (the entry point
  `scripts/coordinator/codex_call.py`), P5, P6, P7, the counted rounds
  (its count starts at zero), the checkpoint, the gate and the landing.
- **Lane `wi-963`:** unchanged, holds for the owner (OI-115). It holds
  LLR-342 and TC-373.
- **Watermark** on trunk: WI 971, SR 242, LLR 345, IF 304, TC 383, OI 115;
  acts to seq 150. Lane-held: wi-963 LLR-342, TC-373; wi-960 SR-243,
  LLR-346, TC-384, TC-385. The next lane's Terra floor is SR-244, LLR-347,
  TC-386, IF-305.
- **Strict lints:** clean on trunk. **No judgement is active**;
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-21-leg11/`
  (WI-960's arms map, spine change list and build brief live there); the
  leg-07 root stays until WI-963 lands.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say: two full-lane
reviewers per round, Codex Sol at medium (REVIEW-A) and Claude Opus at high
(REVIEW-B, launched with the Agent tool's `effort: "high"`), each given
only its rendered brief. Every render refuses a tip with no attested
review bar for its `--tests`: attest the tip first.

## The queue

The owner's order (coordinator-2026-10-16 D-004, D-006; coordinator-2026-10-17
D-002, D-008), turned toward headless runs (coordinator-2026-10-18 D-004,
D-006), with the owner's 2026-10-20 rulings (coordinator-2026-10-20 D-008 to
D-019) and coordinator-2026-10-21 D-004 to D-006. Each row that changes
machinery lands alone, after the cycle has run through the last landing's
changed steps (WI-969 changed the pre-commit hook and the merge slot's
riders; three trunk commits have run the new hook step, and no lane has
yet landed through the slot since).

**Only the rows in this table are claimed**, in order and under their
`needs`. When no row in it can move without the owner, the leg closes out
with the `Overnight: stop` line.

| # | Row | Next |
|---|---|---|
| 1 | WI-960 | In its lane: wi-960 D-005's open point, then P4 onward (above). WI-961 follows it (hard edge) |
| 2 | WI-963 | Held: OI-115 (the owner) |
| 3 | WI-850, WI-851, WI-856, WI-878, WI-910, WI-920 | Under their `needs`, each scope-critiqued at its claim (WI-910 as split by D-019) |
| 4 | Filings P3 to P6, P8 | P3 ends in an owner act. P4 and P5 may file now that WI-969 has landed; P5's spec asks D-009's question (does the WI space ride the carrier?) and folds in WI-810's "sequential sittings never collide on an id". P6 starts with the W3 dry run. P8 waits on its filing calls |
| 5 | WI-966 | Scope critique and its confirming round, then the claim; it lands before item 10 step 5 |
| 6 | WI-971 | Scope critique at its claim; it touches the hook and slot walk WI-969 added, so it lands alone |

**Never claimed by a leg:** WI-684 (waits on OI-98, the owner's re-sync),
WI-795 (OI-105, then WI-820), WI-908 (the owner present), WI-964 (the
owner's Mac), WI-827 (attended only; it never lands from a lane), WI-967
(OI-115's placeholder), and every row under `docs/work/deferred/` (D-011,
D-016).

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).

## For the owner

- **Rule OI-115** (WI-963's settlement fix; recommendation (a)). It holds
  WI-963 at its gate tip.
- **Confirm or overrule:**
  - wi-969 D-001: the minted successor's spec carried no Done-when, so the
    lane copied WI-902's spec of record into it byte for byte and a
    done-when sitting blessed it (the mint gap is a follow-up: a
    disposition's successor with `planmode = "single"` and a `specref` to
    a spec of record but no Done-when of its own);
  - wi-969 D-020 (the indented-fence class taken at MAJOR over Opus's
    MINOR), D-022 and D-027 (WI-971 filed from MINORs, not from a dispute
    SUCCESSOR), and D-002 to D-026 otherwise;
  - wi-960 D-001 to D-005 (D-004: 41 existing tests moved onto claimed
    lanes; D-005: the gitignore gap's route, the next leg's call);
  - and every item the last handoff listed: wi-958 D-001 to D-019 (D-008
    high risk), coordinator-2026-10-21 D-001 to D-006, wi-957 D-005 to
    D-014, wi-940 D-001 to D-011 (D-009 high risk), wi-963 D-001 to D-011,
    wi-962 D-001 to D-007.
- **Still open from the last handoff:**
  - review the deferred rows' re-scopes (D-016; WI-809 and P4 gate the
    managed loop's unpause);
  - your owner-held rows: WI-827, WI-908, WI-964, and WI-684 and WI-795
    behind their open items;
  - confirm or overrule coordinator-2026-10-20 D-012, D-013 and D-020, and
    D-001 to D-007 (high risk: D-002, D-005, D-006);
  - P8's filing calls; wi-955 D-001 to D-006; wi-956 D-001 to D-010;
  - the named-tests `--basetemp`, SR-227's wording, and the lists before
    them.
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
