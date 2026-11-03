# Handoff 2026-11-02b (headless leg 30): WI-978 landed; the queue waits on the owner

It replaces [handoff-2026-11-02a-leg29-coordinator.md](handoff-2026-11-02a-leg29-coordinator.md)
as the resume map. The procedure is in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 30 ran under loop session
`20261102T035202Z-8dc8b4`; its coordinator session was
`238aa103-2701-454c-bac3-3c193c849fa7`. It ran queue row 1 (WI-978) from its
final rebase to its landing. Every other row waits on the owner, so this
handoff carried `Overnight: stop`.

**Amended in place on 2026-11-02 (attended), after the owner ruled
OI-119 (a) and took SN-028's and SN-036's act:** the stop line is dropped
and queue row 1 moves (coordinator-2026-11-02 D-003; commits d58f22e0b to
cb11c4f85).

## State (trunk `refactor_again`, nothing pushed)

- **WI-978 landed** as `889498874`, alone, from a hand squash after
  `check-lane` passed.
  - P14: rebased cleanly onto `2f4ebb2a5`, with the patch id unchanged.
    The lane's own LLR 362-363 and TC 401-402 were reserved through the
    built verb, which created the carrier `refs/heads/id-carrier` at
    `58c902c22` (with the leg's trailer). The audit reads that branch as a
    person's lane; `check-lane id-carrier` passes.
  - The checkpoint: sittings 013 and 014. The gate found one MAJOR, ruled
    FIX by dispute sitting 018 and built in fix round 4. Then a second
    reconcile and whole-set sitting 019, which approved every row and
    blessed SR-174 and TC-158. The second gate found MINORs only. Acts
    took seqs 166 and 167.
  - The re-mint WI-990 is closed (`59d37fab9`). WI-991, the re-judge of
    TC-055 whose declared trigger fired, is open and is not in the queue
    table.
  - The lane's tips are archived with its pre-rebase tip `658a59434`. Its
    worktree is removed; the branch stays.
  - Decisions: wi-978 D-013 to D-021; coordinator-2026-11-02 D-001, D-002.
- **Every lane now reserves before drafting.** Both landing routes refuse
  an added registry id outside a reservation of the lane's claimed work
  item, and refuse a retired number. The recipes' "reserve before
  drafting" holds: before a spine author's turn, the coordinator reserves
  the draft's counts (`trace.py --reserve-ids WI-NNN SPACE=N,...`, from
  the lane) and fills the prompt's `RESERVED` slot.
- **WI-963** (OI-119 ruled (a) on 2026-11-02; before then held on it): `landing_id_refusal`, run read-only against
  its tip, refuses LLR-342 and TC-373 as unreserved. After the ruling and
  its rebase onto trunk, it reserves its LLR and TC ids, renumbers the
  rows if the ranges differ, and only then lands.
- **Watermark** (trunk): WI 991, SR 246, LLR 363, IF 308, TC 402, OI 119.
  Acts run to seq 167. The carrier holds WI-978's reservation records.
- **Bars:**
  - smoke on the staged squash: 3376 passed, 3 skipped (CPU 544.3 s,
    over the 540 s budget, reported only);
  - both strict lints clean on the landing tip;
  - the full suite at close-out: 7566 passed, 32 skipped in 28 minutes.
- **Usage:** both ingest runs exited 0. The next close-out passes
  `--session 238aa103-2701-454c-bac3-3c193c849fa7`.
- **Pause:** `docs/work/pause` is tracked and unchanged this leg, and no
  judgement is active.
- **Scratch:**
  - this leg's root is `C:/Projects/ai-template.wt/review-tmp/2026-11-02b-leg30/`;
  - leg 29's root (`2026-11-01d-leg29`) may go now that WI-978 has landed;
  - keep the leg-07 root until WI-963 lands.

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
through the last landing's changed steps. WI-978's changed steps (the
reservation before a spine turn, the landing's `reserved-ids` check and the
carrier fold) run at the next lane's spine turn and landing.

**Only the rows in this table are claimed**, in order and under their
`needs`.

| # | Row | Next |
|---|---|---|
| 1 | WI-963 | OI-119 ruled (a) at d58f22e0b, its Done-when digest again the pass record's. Rebase onto trunk's tip, reserve its LLR and TC ids (`--reserve-ids`) and renumber LLR-342 and TC-373 if the ranges differ, build the FIX (settlement read from the ledger's `copied`; dispute sitting 007's remedy), recount the module sizes, then a checkpoint for any renumbered row, its act turn and landing |
| 2 | WI-910 | Held on OI-124: its Done-when checks CI's macOS and Linux state on the landing tip, which needs a push, or the owner rules the WSL POSIX route (coordinator-2026-10-25 D-001) |
| 3 | WI-992 (P8) | Held on OI-120, P8's filing calls; after the ruling, re-draft P8's rows (the drafts were lost with leg 06's scratch root) and file each owing its scope critique |

**Never claimed by a leg:**

- WI-684 (waits on OI-98, the owner's re-sync);
- WI-795 (OI-105, then WI-820);
- WI-908 (OI-122: the owner present);
- WI-964 (OI-123: the owner's Mac);
- WI-827 (OI-121: attended only; it never lands from a lane);
- WI-993 (the owner-held-step rule's build), until the owner orders it into
  this table; it owes its scope critique first;
- WI-991 (TC-055's re-judge), until the owner orders it into this table;
- the successor rows WI-982 and WI-983, until the owner orders them into
  this table;
- every row under `docs/work/deferred/` (D-011, D-016).

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).

## For the owner

- **WI-978's RESYNC forced change** (010-REVIEW-B F2, 006-REVIEW-B F7):
  the entry refuses a local `git merge --squash` of an unclaimed branch
  that adds registry ids, where the spec's Done-when says a trunk-only
  repository is unaffected. It landed as written; rule the line, or leave
  it among status.md's follow-ups.
- **WI-978's fold reading** (wi-978 D-004): the fold takes from the carrier
  tip its records and the marks they justify, never its other mark lines.
  Confirm or overrule.
- **OI-120 to OI-124** (filed 2026-11-02, attended): P8's filing calls,
  and the owner-held steps of WI-827, WI-908, WI-964 and WI-910 (push
  `refactor_again`, or rule the WSL POSIX route). Each renders on
  `open-items.html`.
- **The FileBackup re-sync (OI-98):** unblocked. Fix the act ledger
  entry's overwrite list first (it misses `scripts/acceptance_record.py`,
  a follow-up). The re-sync now carries WI-978's forced change: a lane
  open at upgrade reserves and renumbers before it lands.
- **Confirm or overrule:**
  - from this leg: wi-978 D-013 to D-021 and coordinator-2026-11-02 D-001
    and D-002. Note especially:
    - wi-978 D-014, the coordinator's restore of six symbols to LLR-362's
      `code_symbol`;
    - wi-978 D-021, the second gate's MINORs left as follow-ups;
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
