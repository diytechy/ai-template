# Handoff 2026-10-21c (headless leg 09): WI-957 and WI-953 landed; WI-958 through P4; WI-960's plan passed

It replaces [handoff-2026-10-21b-leg08-coordinator.md](handoff-2026-10-21b-leg08-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 09 (loop session
`20261021T045653Z-213020`) landed WI-957 and WI-953, claimed WI-958 and
WI-960, and built WI-958 through its plan's P4. It carries no
`Overnight: stop` line: WI-958, WI-960 and WI-969 move without the owner.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** WI-957 landed as `8c32cf2a9`: a review brief renders only over
  the tip's attested review bar (act seq 146: SR-241, LLR-341, TC-371;
  TC-372 retired). WI-953 landed as `4299f4ff8` (PARTIAL upheld) and the
  sweep minted **WI-969**, WI-902's successor on the owner's route. The
  claims of WI-953, WI-958 and WI-960 ran under one scoped unpause
  (`08d9629d7`, restored byte-identical at `352d5d722`; coordinator-2026-10-21
  D-005). `archive/lanes` holds both landed lanes' tips. The full suite
  ran once at `801495010`: 6898 passed, 33 skipped (894.96 s).
- **Lane `wi-958`** (tip `778a60657`, base `801495010`; plan passed at
  critique 2): P1 (Terra's intent set: SR-242, LLR-343, LLR-344, TC-375 to
  TC-382, SR-241 and TC-082 amended), P2, P3 and P4 committed (wi-958
  D-001 to D-005). **Next:** P5 (the red record and count in
  `kitlib/verdict.py`), then P6 to P9, each a builder stage the
  coordinator verifies and commits; then counted round 1 (attest first:
  `integrate.py --root "$REPO" attest --branch wi-958 --bar review --tests
  <its modules>`). Terra's session: `01a15fbf-ef89-7f53-821c-799cc4caa08c`.
  The builder's spine change list: `wi-958-spine-changes.md` under the
  scratch root. 14 strict xfails remain for P5 to P7.
- **Lane `wi-960`** (tip `e11daba71`, base `801495010`): plan, critique 1
  (two MAJOR), one revision, critique 2 APPROVE 0, pass record. **Next:**
  its plan's P0, a spec amendment (Settlement 1 and Trust gain the
  close-first case) judged by one confirming critique before any test; a
  refusal closes the lane partial. Keep the Done-when unchanged (an edit
  unbinds the pass record). Then P1, Terra's intent turn, with an id floor
  above wi-958's (SR-243, LLR-345, TC-383, IF-303).
- **Lane `wi-963`:** unchanged, holds for the owner (OI-115). It holds
  LLR-342 and TC-373.
- **Watermark** on trunk: WI 969, SR 241, LLR 341, IF 302, TC 374, OI 115;
  acts to seq 146. Lane-held: wi-958 SR-242, LLR-343, LLR-344, TC-375 to
  TC-382; wi-963 LLR-342, TC-373.
- **Strict lints:** clean on trunk and in each lane. **No judgement is
  active**; `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-21-leg07/`
  (leg 09's files under `l9-*`). Keep it until WI-963 and WI-958 land.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say: two full-lane
reviewers per round, Codex Sol at medium (REVIEW-A) and Claude Opus at high
(REVIEW-B, launched with the Agent tool's `effort: "high"`), each given
only its rendered brief. Every render now refuses a tip with no attested
review bar for its `--tests`: attest the tip first.

## The queue

The owner's order (coordinator-2026-10-16 D-004, D-006; coordinator-2026-10-17
D-002, D-008), turned toward headless runs (coordinator-2026-10-18 D-004,
D-006), with the owner's 2026-10-20 rulings (coordinator-2026-10-20 D-008 to
D-019) and coordinator-2026-10-21 D-004 and D-005. Each row that changes
machinery lands alone, after the cycle has run through the last landing's
changed steps (WI-957's review render ran through its own gate this leg;
the next lane's first review round runs it again).

**Only the rows in this table are claimed**, in order and under their
`needs`. When no row in it can move without the owner, the leg closes out
with the `Overnight: stop` line.

| # | Row | Next |
|---|---|---|
| 1 | WI-958 | In its lane: P5 to P9, then round 1, the checkpoint, the gate and the landing. Lands alone |
| 2 | WI-969 | WI-902's successor on the owner's route (coordinator-2026-10-20 D-008): a claim (one scoped unpause), then the third plan revision carrying sitting 016's FIX, one confirming critique in convergence stance, and the build. Its scope is WI-902's spec unchanged, so no new scope critique is owed (record it). Before P4 and P5 |
| 3 | WI-960 | In its lane: P0 (the spec amendment and its confirming critique), then P1 onward. WI-961 follows it (hard edge) |
| 4 | WI-963 | Held: OI-115 (the owner) |
| 5 | WI-850, WI-851, WI-856, WI-878, WI-910, WI-920 | Under their `needs`, each scope-critiqued at its claim (WI-910 as split by D-019) |
| 6 | Filings P3 to P6, P8 | P3 ends in an owner act. P4 and P5 come after WI-969 lands; P5's spec asks D-009's question (does the WI space ride the carrier?) and folds in WI-810's "sequential sittings never collide on an id". P6 starts with the W3 dry run. P8 waits on its filing calls |
| 7 | WI-966 | Scope critique and its confirming round, then the claim; it lands before item 10 step 5 |

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
  - coordinator-2026-10-21 D-005 (the batch claim) and D-001 to D-004;
  - wi-957 D-009 to D-014 (D-011: TC-372 retired, the cycle skill's text
    pinned by its own test outside the spine, as at wi-918; D-014: the
    gate's two MINORs to the unfiled follow-ups);
  - wi-958 D-001 to D-005 (D-004: the RESYNC entry placed at P3 for
    `check_resync`; D-004 and D-005: two size-ratchet re-stamps);
  - and every item the last handoff listed: wi-940 D-001 to D-011 (D-009
    high risk), wi-963 D-001 to D-011, wi-957 D-005 to D-008, wi-962 D-001
    to D-007.
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
