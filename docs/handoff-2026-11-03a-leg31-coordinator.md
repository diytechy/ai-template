# Handoff 2026-11-03a (headless leg 31): WI-963 landed; P8's rows filed; the queue waits on the owner

Amended in place 2026-11-03 (attended): the owner ordered WI-993, WI-991,
WI-982 and WI-983 into the queue table (coordinator-2026-11-03 D-003), so
the leg's stop line is dropped and those rows run next. The owner then
ruled OI-125 (a) on each call (coordinator-2026-11-03 D-004), so P8's rows
move too.

It replaces [handoff-2026-11-02b-leg30-coordinator.md](handoff-2026-11-02b-leg30-coordinator.md)
as the resume map. The procedure is in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 31 ran under loop session
`20261103T054112Z-32c0bd`; its coordinator session was
`044a4df9-f452-40c7-89a6-ae69b29804d1`. It ran queue row 1 (WI-963) from its
rebase to its landing, and queue row 3 (WI-992, P8's filing). Row 2 (WI-910)
and the three filed P8 rows wait on the owner.

## State (trunk `refactor_again`, nothing pushed)

- **WI-963 landed** as `c57796e63`, alone, from a hand squash after
  `check-lane` passed. The trunk mint files no amendment row for a row the
  merged range settled, judged from the act ledger's `copied` record, so
  it holds on a squashed landing. Its own landing's sweep minted nothing.
  - Rebased onto `25a7e4599` (pre-rebase tip `6e3efc56f`); LLR 364 and TC
    403 reserved at carrier commit `3a8986276`, and LLR-342 and TC-373
    renumbered to them.
  - The FIX of dispute sitting 007, built after OI-115 (a). The builder's
    first rule turned the WI-926 replay red. The coordinator then narrowed
    it with a second arm (wi-963 D-014), and both gate reviewers showed
    that arm settles a routed cell restored between two acts. Dispute 013
    kept the arm (F1 DISMISS) and ordered its limit stated and pinned
    (F2 FIX). The second gate's Sol MAJOR went to dispute 018: FIX, text
    only, scoping Done-when item 1 under a later copy. Both scopes sit in
    the claim copy's Trust section (the pass record stays bound), judged
    in sittings 014 and 019.
  - The third gate: Sol APPROVE 0, Opus APPROVE with 3 MINORs, which
    became status.md follow-ups. Whole-set sitting 022 led to acts seq 169
    and 170.
  - Tips archived (`499bd3de8`) with the pre-rebase tips `6e3efc56f`,
    `0ae2c5b60` and `6cef95f30`; the worktree is removed and the branch
    kept.
  - Decisions: wi-963 D-013 to D-026; coordinator-2026-11-03 D-001.
- **P8 filed** (`f6f38bcee`): WI-994 (test files name their test cases on
  the `Implements:` line), WI-995 (the review test set derived from the
  row's SRs; needs WI-994) and WI-996 (the strict-mark check and the
  required `[bars] red_mark` key; needs WI-995). Each owes its scope
  critique and cites OI-125 (three calls the drafters left to the owner,
  ruled (a) on each on 2026-11-03).
  WI-992 is closed citing the filing (coordinator-2026-11-03 D-002).
- **Watermark** (trunk): WI 996, SR 246, LLR 364, IF 308, TC 403, OI 125.
  Acts run to seq 170. The carrier holds WI-978's and WI-963's
  reservation records.
- **Bars:**
  - smoke on the landing's staged squash: 3376 passed, 3 skipped (CPU
    466.1 s, within);
  - both strict lints clean;
  - the full suite at close-out: 7598 passed, 28 skipped in 31 minutes.
- **Usage:** both ingest runs exited 0. The next close-out passes
  `--session 044a4df9-f452-40c7-89a6-ae69b29804d1`.
- **Pause:** `docs/work/pause` is tracked and unchanged this leg, and no
  judgement is active.
- **Scratch:**
  - this leg's root is `C:/Projects/ai-template.wt/review-tmp/2026-11-03a-leg31/`
    (P8's drafts and notes under `p8/`);
  - the leg-07 and leg-30 roots may go now that WI-963 has landed.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say, through the route:

- Two full-lane reviewers run per round: Codex Sol at medium (REVIEW-A,
  `codex_call.py REVIEW-A`) and Claude Opus at high (REVIEW-B, launched
  with the Agent tool's `effort: "high"`). Each gets only its rendered
  brief.
- In a headless leg, launch REVIEW-B first, and tell it never to hand a
  test run to a background sub-agent.
- Every render refuses a tip with no attested review bar for its
  `--tests`, so attest the tip first.

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
through the last landing's changed steps. WI-963's changed step (the
landing sweep's check of a minted amendment row against the lane's own
act) runs at the next landing.

**Only the rows in this table are claimed**, in order and under their
`needs`.

| # | Row | Next |
|---|---|---|
| 1 | WI-910 | Held on OI-124: its Done-when checks CI's macOS and Linux state on the landing tip, which needs a push, or the owner rules the WSL POSIX route (coordinator-2026-10-25 D-001) |
| 2 | WI-994, WI-995, WI-996 (P8) | OI-125 ruled (a) on each call, folded into the rows. Run each row's scope critique (fresh Sol), dispositions and confirming round, in `needs` order, before any claim. No tag-migration row exists yet: WI-994's Done-when now files it, and WI-995's gate waits on it here |
| 3 | WI-993 | Ordered in by the owner (coordinator-2026-11-03 D-003). Scope critique (fresh Sol), dispositions and confirming round, then claim. Its spec of record is `docs/specs/WI-993.md` |
| 4 | WI-991 | Ordered in by the owner. TC-055's re-judge by its Method (the recipes' section 8); a fail is recorded as a fail |
| 5 | WI-982 | Ordered in by the owner. Scope critique, dispositions and confirming round, then claim |
| 6 | WI-983 | Ordered in by the owner. Scope critique, dispositions and confirming round, then claim |

**Never claimed by a leg:**

- WI-684 (waits on OI-98, the owner's re-sync);
- WI-795 (OI-105, then WI-820);
- WI-908 (OI-122: the owner present);
- WI-964 (OI-123: the owner's Mac);
- WI-827 (OI-121: attended only; it never lands from a lane);
- every row under `docs/work/deferred/` (D-011, D-016).

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).
The prompt's last step, re-ordering leg 03's rows against the plan, is the
owner's.

## For the owner

- **OI-124** (WI-910: push `refactor_again`, or rule the WSL POSIX route),
  and OI-121 to OI-123 (WI-827, WI-908, WI-964), unchanged.
- **WI-963's reading, to confirm or overrule:**
  - wi-963 D-014: the coordinator's narrowing was the defect both gate
    reviewers found; the record says so.
  - wi-963 D-019 and D-024: Done-when items 1 and 5 are scoped in the
    Trust section, not the Done-when. A reader of the archived Done-when
    alone sees them unbounded.
  - The landing's one known cost (sitting 018): a lane whose act turn
    re-attests a row with a routed-cell change, then approves another row
    in the same registry, still mints that row, which the sweep step
    closes citing the act.
- **The FileBackup re-sync (OI-98):** unblocked. Fix the act ledger
  entry's overwrite list first (it misses `scripts/acceptance_record.py`, a
  follow-up). The re-sync now also carries WI-963's entry (no migration).
- **Confirm or overrule:**
  - from this leg: wi-963 D-013 to D-026 (D-014 and D-019 especially);
    coordinator-2026-11-03 D-001 and D-002;
  - carried from leg 30: wi-978 D-013 to D-021 (D-014 and D-021 especially);
    coordinator-2026-11-02 D-001 and D-002; WI-978's RESYNC forced change
    and its fold reading (wi-978 D-004);
  - carried from leg 29: coordinator-2026-11-01 D-008 and D-009; wi-963
    D-012; wi-978 D-001 to D-012 (D-002, D-004 and D-005 especially);
  - carried from leg 28: coordinator-2026-11-01 D-005 to D-007; wi-987
    D-001 to D-005; wi-967 D-001 to D-005;
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
- **Push** `refactor_again`, `archive/lanes` and `id-carrier`.

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
