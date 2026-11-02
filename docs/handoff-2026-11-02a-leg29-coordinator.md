# Handoff 2026-11-02a (headless leg 29): WI-963 held on OI-119; WI-978 built, its rounds done

It replaces [handoff-2026-11-01c-leg28-coordinator.md](handoff-2026-11-01c-leg28-coordinator.md)
as the resume map. The procedure is in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 29 ran under loop session
`20261102T035202Z-8dc8b4`; its coordinator session was
`9c217bef-0ddc-40a3-81e0-8fff79680181`. It rebased queue row 1 and filed its
hold for the owner, then claimed row 2 and ran it from the plan through the
last review round. It closed out at 35% occupancy rather than start row 2's
final rebase and self-reservation.

## State (trunk `refactor_again`, nothing pushed)

- **WI-963 (row 1) rebased and held.** The lane `wi-963` is rebased onto
  `35226d1af` (pre-rebase tip `0ae2c5b60`) and committed at `6e3efc56f`;
  its six affected modules pass (273 tests) and `check-lane` passes. Its
  claim copy took OI-115's Done-when item (coordinator-2026-11-01 D-004),
  which moves the Done-when digest from the pass record's
  `sha256:371fa4c3f41d21b6` to `sha256:f8c62f4a13affe14`. The plan gate
  therefore refuses the landing and every build commit, and the plan cap is
  spent. **OI-119** is filed pending with its placeholder WI-989 (OI-102),
  and WI-963's needs cite it (`3ec0e0e62`; coordinator-2026-11-01 D-008,
  wi-963 D-012). Removing the item from the Done-when restores the recorded
  digest exactly. The FIX build waits on the ruling, and so does the
  module-size recount.
- **WI-978 (row 2) claimed, built, rounds done.** Claimed under one scoped
  unpause (`b16b8cf6f`, claim `429627146`, pause restored byte-identical
  `c6e982882`). The lane `wi-978` is at `658a59434`, base `c6e982882`.
  - Single plan: critique 1 CHANGES-REQUESTED (two MAJOR), one revision,
    critique 2 APPROVE, pass record `e4fd25b61`. The Done-when digest is
    `sha256:587fd9be4e5f28c2`, unchanged since then.
  - Intent set (Terra): SR-174 amended and kept, LLR-362 and LLR-363, TC-158
    amended, TC-401 and TC-402, IF-101 widened. The coordinator restored
    TC-158's dropped status and phase cells (wi-978 D-002).
  - Build in four attested stages: tests first, then deliverable 1, then
    deliverable 2, then the text.
  - Round 1: 3 MAJOR fixed. Round 2: 1 MAJOR fixed, and one re-graded to
    P14 (D-005). Round 3 (convergence): one MAJOR went to sitting 008, which
    ruled FIX; the fix was built. The uncounted convergence review after it
    had one MAJOR, which sitting 012 ruled DISMISS refuted.
  - No BLOCKER or MAJOR is open. The convergence maps are D-007 and D-010.
  - The spec's design paragraph on the fold gained one clarifying
    parenthesis, outside the Done-when (D-004).
  - The builder's spine change list for the checkpoint, items 1 to 38, is
    `C:/Projects/ai-template.wt/review-tmp/2026-11-01d-leg29/build-978/spine-change-list.md`.
    The checkpoint MINORs are listed in D-003, D-005, D-008 and D-011.
  - Open in-surface code MINORs: 009-REVIEW-A F4; 010-REVIEW-B F1, F2 and
    F6; 006-REVIEW-B F5 and F7 (D-012).
  - The slot's own claim reader was not consolidated: it also serves
    `dispatch.py` and `handback.py`, outside the surface (D-006). Make it a
    follow-up at the landing.
- **Watermark** (trunk): WI 989, SR 246, LLR 361, IF 308, TC 400, OI 119.
  Acts run to seq 165.
  - Lane-held ids: wi-963 holds LLR-342 and TC-373; wi-978 holds LLR-362,
    LLR-363, TC-401 and TC-402.
  - A new lane's Terra floor is SR-247, LLR-364, TC-403 and IF-309.
- **Bars:** smoke on trunk at the OI-119 filing: 3301 passed (CPU 489.0 s).
  At the unpause and the restore it was 599.4 s and 616.6 s, over the
  540 s budget (reported only). Each WI-978 stage and fix passed
  `integrate.py attest`'s review bar. Both strict lints are clean on trunk.
  No trunk code changed this leg, so the close-out ran no full suite.
- **Usage:** both ingest runs exited 0. The next close-out passes
  `--session 9c217bef-0ddc-40a3-81e0-8fff79680181`.
- **Pause:** `docs/work/pause` is tracked and byte-identical, and no
  judgement is active.
- **Scratch:** this leg's root is
  `C:/Projects/ai-template.wt/review-tmp/2026-11-01d-leg29/`. Keep it until
  WI-978 lands, since it holds the spine change list. Leg 28's root may go.
  Keep the leg-07 root until WI-963 lands.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say, through the route:

- Two full-lane reviewers run per round: Codex Sol at medium (REVIEW-A,
  `codex_call.py REVIEW-A`) and Claude Opus at high (REVIEW-B, launched
  with the Agent tool's `effort: "high"`). Each gets only its rendered
  brief.
- In a headless leg, launch REVIEW-B first, and tell it never to hand a
  test run to a background sub-agent.
- Every render refuses a tip with no attested review bar for its
  `--tests`, so attest the tip first. WI-978's list is the seventeen
  modules in its last attest (`82e4ca1a7`).

## The queue

The owner's order: coordinator-2026-10-16 D-004, D-006, and
coordinator-2026-10-17 D-002, D-008, turned toward headless runs by
coordinator-2026-10-18 D-004 and D-006; the owner's 2026-10-20 rulings
(coordinator-2026-10-20 D-008 to D-019); coordinator-2026-10-21 D-004 to
D-006; the owner's 2026-10-23 direction that a scope critique settles a
row's scope and never grows it (the rubric's S7); rows ordered by
coordinator-2026-10-25 D-009 and D-013 and coordinator-2026-11-01 D-003 and
D-009.

Each row that changes machinery lands alone, after the cycle has run
through the last landing's changed steps. WI-978's own act turn runs
WI-967's changed step (coordinator-2026-11-01 D-009).

**Only the rows in this table are claimed**, in order and under their
`needs`.

| # | Row | Next |
|---|---|---|
| 1 | WI-978 | Run the plan's P14: rebase onto trunk's tip, re-anchor the RESYNC entry, reserve this row's own LLR and TC ids through the built `--reserve-ids` verb, renumber the drafted rows if the ranges differ, and commit the folded watermark. The verb writes the carrier branch `refs/heads/id-carrier`, which the launcher's post-leg audit judges as a lane: before the first reservation, confirm the carrier commit carries the leg's `Loop-Session` trailer. If it does not, hold P14 for an attended session. Then the open code MINORs (D-012's call), P15's checkpoint (Terra's turn fills the prompt's new `RESERVED` slot), the gate, the act and the landing, alone |
| 2 | WI-963 | Held on OI-119. After the ruling: rebase onto its commit (and onto WI-978's landing), build the FIX (settlement read from the ledger's `copied`; dispute sitting 007's remedy), recount the module sizes, then its act turn and landing |
| 3 | WI-910 | Held: its Done-when checks CI's macOS and Linux state on the landing tip, which needs a push (coordinator-2026-10-25 D-001) |
| 4 | Filing P8 | Waits on its filing calls (P6 landed as WI-979) |

**Never claimed by a leg:**

- WI-684 (waits on OI-98, the owner's re-sync);
- WI-795 (OI-105, then WI-820);
- WI-908 (the owner present);
- WI-964 (the owner's Mac);
- WI-827 (attended only; it never lands from a lane);
- WI-980 and WI-981 (OI-117);
- WI-984 and WI-985 (OI-118);
- WI-989 (OI-119's placeholder);
- the successor rows WI-982 and WI-983, until the owner orders them into
  this table;
- every row under `docs/work/deferred/` (D-011, D-016).

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).

## For the owner

- **OI-119** (new, WI-963): choose how its plan binds again. The
  recommendation is (a): move OI-115's item, text unchanged, from WI-963's
  Done-when to its Trust section in the ruling commit. That restores the
  pass record's digest exactly. The other routes are (b), a plan round past
  the cap with a re-cut lane, and (c), a plan-gate change. The recipes now
  route such an item to the Trust section at the ruling.
- **WI-978's fold reading** (wi-978 D-004): the fold takes from the carrier
  tip its records and the marks they justify, never its other mark lines.
  The Done-when item still reads true over that, and the spec's design
  paragraph gained one clarifying parenthesis. Confirm or overrule.
- **WI-978's RESYNC forced change** (010-REVIEW-B F2 and 006-REVIEW-B F7):
  the entry refuses a local `git merge --squash` of an unclaimed branch
  that adds registry ids, where the spec's Done-when says a trunk-only
  repository is unaffected. This is a follow-up at the landing unless you
  rule the line.
- **Rows still held:** push `refactor_again` so WI-910's landing tip
  carries CI's state, or rule that the WSL POSIX evidence route (wi-931
  D-002) stands in for CI on that Done-when item (coordinator-2026-10-25
  D-001). Make P8's filing calls, or order WI-982 and WI-983 into the table
  (each owes its scope critique before its claim).
- **SN-028's act, on trunk** (OI-118, its owner row WI-985), unchanged:
  `intake.py snapshot --approves stakeholder-needs=<your ruling record> --reattests SN-028`,
  adding `--verdict docs/reviews/wi-966/007-ADJUDICATE-d8f6fd3.md`; then
  rule OI-118. Keep or drop SN-028's `shell` tag (sitting 003).
- **SN-036's act, on trunk** (OI-117, its owner row WI-981), unchanged:
  `intake.py snapshot --approves stakeholder-needs=docs/log.d/2026-10-25-wi976-sn036-ruling.md --reattests SN-036`,
  adding `--verdict docs/reviews/wi-976/016-ADJUDICATE-9d6ad4c.md`; then
  rule OI-117 (WI-981, WI-980).
- **The FileBackup re-sync (OI-98):** unblocked. Fix the act ledger
  entry's overwrite list (it misses `scripts/acceptance_record.py`, a
  follow-up) first.
- **Confirm or overrule:**
  - from this leg: coordinator-2026-11-01 D-008 and D-009; wi-963 D-012;
    wi-978 D-001 to D-012. Note especially:
    - wi-978 D-002, the coordinator's restore of TC-158's dropped cells;
    - wi-978 D-004, the fold reading and the spec parenthesis;
    - wi-978 D-005, the self-reservation MAJOR re-graded to P14;
    - coordinator-2026-11-01 D-009, WI-978 moving past the held WI-963;
  - carried from leg 28: coordinator-2026-11-01 D-005 to D-007; wi-987
    D-001 to D-005; wi-967 D-001 to D-005 (wi-987 D-003 and wi-967 D-003
    re-grades; their D-002 repairs; D-006's design calls). WI-967's spec
    grew past three times its filing size, including a Trust section whose
    shared Ruling is yours;
  - from the attended amendment: coordinator-2026-11-01 D-001 to D-003;
  - carried from leg 27: wi-977 D-026 and D-027;
  - carried from leg 26: wi-977 D-015 to D-025;
  - carried from leg 25: wi-966 D-009 to D-017; coordinator-2026-10-31
    D-001 and D-002; wi-977 D-003 to D-014;
  - carried from leg 24: wi-966 D-005 (high risk), D-001 to D-004 and
    D-006 to D-008; wi-977 D-002; coordinator-2026-10-26 D-004;
  - carried from leg 23: wi-976 D-024 (high risk) and D-025 to D-029;
    coordinator-2026-10-26 D-001 (high risk), D-002 and D-003;
  - carried from leg 22: wi-979 D-002 (high risk), D-001 and D-003;
    coordinator-2026-10-25 D-001 to D-013; wi-971 D-001 and D-002; wi-977
    D-001; wi-976 D-001 to D-022; wi-878 D-001 to D-008; WI-920's re-judge
    departures.
- **Still open from earlier handoffs:**
  - coordinator-2026-10-24 D-001 to D-005, and wi-856 D-001 to D-006;
  - coordinator-2026-10-23 D-001 to D-005 (D-002 and D-004 high risk), and
    wi-851 D-001 to D-014;
  - coordinator-2026-10-22 D-002 to D-004, wi-850 D-001 to D-012 (D-002
    high risk), wi-961 D-010 to D-017, and the earlier items those
    handoffs carried;
  - the `--wi` primary-checkout preflight call (wi-960 D-016);
  - removing the temporary `Bash(codex exec *)` allow rule;
  - filing your 2026-10-25 ruling that an owner-held step is an open item
    (attended);
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
