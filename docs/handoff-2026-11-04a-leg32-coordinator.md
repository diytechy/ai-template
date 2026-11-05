# Handoff 2026-11-04a (headless leg 32): WI-994 landed; the queue's scope critiques settled; WI-997 is next

It replaces [handoff-2026-11-03a-leg31-coordinator.md](handoff-2026-11-03a-leg31-coordinator.md)
as the resume map. The procedure is in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 32 ran under loop session
`20261104T181017Z-49d2cc`; its coordinator session was
`20ac602d-9199-4930-828f-d2de719510ea`. It ran queue row 2's scope critiques,
built and landed WI-994, and ran the scope critiques of rows 3, 5 and 6. It
closed out at about 36% of its window, because WI-997's lane would not have
fitted.

## State (trunk `refactor_again`, nothing pushed)

- **WI-994 landed** as `880ad86e1`, alone, from a hand squash after
  `check-lane` passed. Test files name their test cases on the `Implements:`
  line, read by one reader beside the code-side grammar, which refuses a
  misplaced, malformed, unknown or unreadable tag through `check_trajectory`.
  It tags no file: WI-997 does.
  - Plan: one revision (a size stamp ordered after the commit that moved it),
    second critique APPROVE, pass record bound.
  - Two counted rounds and the convergence gate. Round 1's MAJOR (a wrapped
    list dropped its tail with no finding) was fixed; round 2 had no BLOCKER
    or MAJOR. The gate: Opus APPROVE with four MINORs, Sol one MINOR, all five
    in status.md's follow-ups (wi-994 D-007).
  - Sitting 005 returned all seven rows on four cell edits, code not in
    question; sitting 006 approved the whole set, and act seq 171 took it.
  - Rebased onto `dca41256c` before the gate, the only conflict the watermark;
    the judged rows compared unchanged. Tips archived with the pre-rebase tip
    `73f0a1578`; the worktree is removed and the branch kept.
  - The landing's sweep minted nothing, so WI-963's changed step ran clean.
- **Scope critiques:**
  - WI-994, WI-995, WI-996, WI-997, WI-998, WI-982 and WI-983: confirmed,
    each APPROVE at its confirming round, or first round for WI-997.
  - WI-993: answered, but held on OI-126 (below). Its confirming round runs
    after the ruling.
- **Filed:** WI-997 (the tag migration, which WI-995 now needs), WI-998 (the
  TC-211 re-inspection split out of WI-983), and OI-126.
- **Watermark** (trunk): WI 998, SR 246, LLR 365, IF 308, TC 409, OI 126.
  Acts run to seq 171.
- **Bars:**
  - smoke on the landing's staged squash: 3376 passed, 3 skipped (CPU 531.4 s,
    within; earlier readings this leg were 559 to 574 s under load, reported
    only);
  - both strict lints clean;
  - the full suite at close-out, two halves at `880ad86e1`: 7654 passed, 29
    skipped (16:55 and 15:33).
- **Usage:** both ingest runs exited 0. The next close-out passes
  `--session 20ac602d-9199-4930-828f-d2de719510ea`.
- **Pause:** `docs/work/pause` is tracked, restored byte-identical after
  WI-994's claim, and no judgement is active.
- **Scratch:** this leg's root is
  `C:/Projects/ai-template.wt/review-tmp/2026-11-04-leg32/`; the leg-31 root may
  go now that its rows are filed.

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

The owner's order stands (the replaced handoff's citations, and
coordinator-2026-11-03 D-003 and D-004). Each row that changes machinery lands
alone, after the cycle has run through the last landing's changed steps.
WI-994's changed step (the tag findings in `check_trajectory`) runs on every
bar, so it has run.

**Only the rows in this table are claimed**, in order and under their
`needs`. WI-997 is in it by WI-994's Done-when and coordinator-2026-11-04 D-002.

| # | Row | Next |
|---|---|---|
| 1 | WI-910 | Held on OI-124: push, or the owner rules the WSL POSIX route |
| 2 | WI-997 | Critique done. Claim, plan (`single`), then build. About 2100 scripted tags; it lands alone, and its review judges the seed script's equivalence evidence. It stops and reports any stale evidence part no test verifies |
| 3 | WI-995 | Critique confirmed. Claim once WI-997 lands |
| 4 | WI-996 | Critique confirmed. Claim once WI-995 lands |
| 5 | WI-993 | Held on OI-126. After the ruling: its confirming round, then claim |
| 6 | WI-991 | TC-055's re-judge by its Method (the recipes' section 8); a fail is recorded as a fail |
| 7 | WI-982 | Critique confirmed. Claim |
| 8 | WI-983 | Critique confirmed. Claim |

**Never claimed by a leg:**

- WI-684 (waits on OI-98, the owner's re-sync);
- WI-795 (OI-105, then WI-820);
- WI-908 (OI-122: the owner present);
- WI-964 (OI-123: the owner's Mac);
- WI-827 (OI-121: attended only; it never lands from a lane);
- WI-998 (off the table until a sample exists, below);
- every row under `docs/work/deferred/` (D-011, D-016).

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).
The prompt's last step, re-ordering leg 03's rows against the plan, is the
owner's.

## For the owner

- **OI-126** (new; holds WI-993): one row or several, and whether a held-rung
  item appears at the landing or at the sitting. WI-993's filing grew past three
  times its size (2175 to about 11100 bytes) under its adopted dispositions.
- **OI-124** (WI-910: push `refactor_again`, or rule the WSL POSIX route), and
  OI-121 to OI-123 (WI-827, WI-908, WI-964), unchanged.
- **This leg's readings, to confirm or overrule:**
  - coordinator-2026-11-04 D-003: WI-996 keeps revision 20's static check, so a
    skipped test left marked is not refused and only the procedure and the
    reviewers catch it; overruling reopens revision 20. Its drafter also reads
    the plan's CI-matrix remark as covering green-after only.
  - coordinator-2026-11-04 D-002: WI-997's equality check ships with no dial,
    so an adopter with evidence cells and no tags reads one finding per part.
  - coordinator-2026-11-04 D-004: WI-982's branchless sweep keeps today's
    behaviour (an empty cell, the row's own tags), close to your no-fallback
    rule.
  - coordinator-2026-11-04 D-005: WI-983 is split, and **no scheduled row is
    known to draft the decomposition round WI-998's sample needs**, so TC-211's
    fail stands until one does.
  - WI-994's `## Trust` Ruling and WI-997's, as the skill routes them to you.
- **The FileBackup re-sync (OI-98):** unblocked. Fix first the act ledger
  entry's overwrite list and the tag entry's PROCESS classing (both in
  status.md's follow-ups).
- **Confirm or overrule:**
  - from this leg: wi-994 D-001 to D-007 (D-004 especially);
    coordinator-2026-11-04 D-001 to D-006 (D-002, D-003 and D-004 especially);
  - carried from leg 31: wi-963 D-013 to D-026 (D-014 and D-019 especially);
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
