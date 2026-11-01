# Handoff 2026-11-01b (headless leg 27): WI-977 landed; the queue holds for the owner

Overnight: stop

It replaces [handoff-2026-11-01a-leg26-coordinator.md](handoff-2026-11-01a-leg26-coordinator.md)
as the resume map. The procedure is in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 27 ran under loop session
`20261031T174835Z-e602ab`; its coordinator session was
`f59c0ba2-2861-47f9-a38b-8d00fd787f69`. It landed WI-977 and closed its
re-mint. Every other row in the queue table holds for the owner, so this
handoff carries the stop line.

## State (trunk `refactor_again`, nothing pushed)

- **WI-977 landed** as `dc7e2a5cf` (one work item per lane: both `--wi`
  flags, the claim, the resume and the closes take exactly one id). Before
  the squash:
  - the lane rebased onto `cf21e8c0e` with the same stable patch-id, and
    its RESYNC entry re-anchored there (wi-977 D-026);
  - the unchanged-rows check passed for verdicts 005 to 007 (traced cells
    only since);
  - WI-966's machinery rule was read as not holding the landing:
    bootstrap's writer is not a cycle step (D-026, for confirm or
    overrule).
- **The act:** the act turn from verdict 005 alone was refused by the
  snapshot, so one whole-set combined sitting,
  `docs/reviews/wi-977/014-ADJUDICATE-fddc055.md`, judged all 23 rows. It
  blessed 22 rows MEANING+BLESS and found LLR-058 CLARITY. One act (seq
  163) re-attested them all (D-027; the recipe now says so).
- **The re-mint** WI-986 is closed: the SR, LLR and TC registries equal
  their anchors.
  - The stakeholder-needs, interfaces and components registries differ
    from their anchors, as they did before this landing.
  - SN-028's and SN-036's acts are the owner's (OI-118, OI-117).
- **Archive:** `archive/lanes` carries the rebased tip `261ff7634` and the
  pre-rebase tip `4800ebd03`. The `wi-977` branch and worktree are kept,
  as for earlier lanes.
- **Lane `wi-963`:** unchanged; it holds for the owner (OI-115).
- **Watermark:** WI 986, SR 246, LLR 360, IF 308, TC 399, OI 118. Acts run
  to seq 163.
  - Lane-held ids: wi-963 holds LLR-342 and TC-373.
  - A new lane's Terra floor is SR-247, LLR-361, TC-400 and IF-309.
- **Bars:**
  - Smoke on the staged squash: 3301 passed, CPU 504.8 s against
    `cpu-seconds = 540`, which is within the limit.
  - The full suite on the landed trunk (`33bcc8cf5`): 7423 passed and 32
    skipped, in 23 min 34 s. `trace.py --strict` and
    `check_trajectory.py --strict` are clean.
- **Usage:** both ingest runs exited 0. The next close-out passes
  `--session f59c0ba2-2861-47f9-a38b-8d00fd787f69`.
- **Pause:** `docs/work/pause` is tracked and unchanged, and no judgement
  is active.
- **Scratch:** this leg's root is
  `C:/Projects/ai-template.wt/review-tmp/2026-11-01b-leg27/`. It and leg
  26's root may go now. Keep the leg-07 root until WI-963 lands.
- **WI-977's follow-ups** are listed under status.md's "Unfiled
  follow-ups":
  - the gates' MINORs (D-023, D-025);
  - the `lane_completion` reader (D-017);
  - two stale `code_symbol` tokens (D-024);
  - the parked `WI-*.md` coverage note (D-015).

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
coordinator-2026-10-17 D-002, D-008. It was turned toward headless runs by
coordinator-2026-10-18 D-004 and D-006. It also follows:

- the owner's 2026-10-20 rulings (coordinator-2026-10-20 D-008 to D-019);
- coordinator-2026-10-21 D-004 to D-006;
- the owner's 2026-10-23 direction that a scope critique settles a row's
  scope and never grows it (the rubric's S7);
- rows 6 and 7 by coordinator-2026-10-25 D-009 and D-013.

Each row that changes machinery lands alone, after the cycle has run
through the last landing's changed steps. WI-977 changed the claim, the
worker's `--wi`, the resume and the closes. The next machinery landing waits
until a lane has been claimed and closed through them.

**Only the rows in this table are claimed**, in order and under their
`needs`. No row in it can move without the owner, hence the stop line.

| # | Row | Next |
|---|---|---|
| 1 | WI-963 | Held: OI-115 (the owner); recount its module size at the rebase |
| 2 | WI-910 | Held: its Done-when checks CI's macOS and Linux state on the landing tip, which needs a push (coordinator-2026-10-25 D-001) |
| 3 | Filing P8 | Waits on its filing calls (P6 landed as WI-979) |

**Never claimed by a leg:**

- WI-684 (waits on OI-98, the owner's re-sync);
- WI-795 (OI-105, then WI-820);
- WI-908 (the owner present);
- WI-964 (the owner's Mac);
- WI-827 (attended only; it never lands from a lane);
- WI-967 (OI-115's placeholder);
- WI-978, until OI-116 is ruled;
- WI-980 and WI-981 (OI-117);
- WI-984 and WI-985 (OI-118);
- the successor rows WI-982 and WI-983, until the owner orders them into
  this table;
- every row under `docs/work/deferred/` (D-011, D-016).

The queue runs in headless legs (the `coordinator-cycle` skill's section 7)
once the owner adds a movable row and drops the stop line.

## For the owner

- **Unblock the queue:** rule OI-115 (WI-963's settlement fix;
  recommendation (a)), or push `refactor_again` so WI-910's landing tip
  carries CI's state. Alternatively, rule that the WSL POSIX evidence route
  (wi-931 D-002) stands in for CI on that Done-when item
  (coordinator-2026-10-25 D-001). Also make P8's filing calls, or order
  WI-982 and WI-983 into the table (each owes its scope critique before its
  claim). Then drop `Overnight: stop`.
- **SN-028's act, on trunk** (OI-118, its owner row WI-985), unchanged:
  `intake.py snapshot --approves stakeholder-needs=<your ruling record> --reattests SN-028`,
  adding `--verdict docs/reviews/wi-966/007-ADJUDICATE-d8f6fd3.md`; then
  rule OI-118. Keep or drop SN-028's `shell` tag (sitting 003).
- **SN-036's act, on trunk** (OI-117, its owner row WI-981), unchanged:
  `intake.py snapshot --approves stakeholder-needs=docs/log.d/2026-10-25-wi976-sn036-ruling.md --reattests SN-036`,
  adding `--verdict docs/reviews/wi-976/016-ADJUDICATE-9d6ad4c.md`; then
  rule OI-117 (WI-981, WI-980).
- **The FileBackup re-sync (OI-98):** unblocked since WI-976 landed.
  WI-966 changes what an adopter's policy file may hold. WI-977's RESYNC
  entry: both `--wi` flags take one id, and a parked multi-row lane must
  land or close before the upgrade.
- **Rule OI-116** (WI-978; recommendation (a), spine only).
- **Confirm or overrule:**
  - from this leg: wi-977 D-026 (the machinery-rule reading) and D-027
    (the whole-set sitting 014 in place of three act turns);
  - carried from leg 26: wi-977 D-015 to D-025. Note especially:
    - D-019, D-020 and D-021, the coordinator's openly recorded mechanical
      repairs to Terra's cells;
    - D-024's tag for `_stop_run`, which names two LLRs;
    - D-016's one-line `agent_loop.py` size bump;
  - carried from leg 25: wi-966 D-009 to D-017; coordinator-2026-10-31
    D-001 and D-002; wi-977 D-003 to D-014;
  - carried from leg 24: wi-966 D-005 (high risk), D-001 to D-004 and
    D-006 to D-008; wi-977 D-002; coordinator-2026-10-26 D-004;
  - carried from leg 23: wi-976 D-024 (high risk) and D-025 to D-029;
    coordinator-2026-10-26 D-001 (high risk), D-002 and D-003;
  - carried from leg 22:
    - wi-979 D-002 (high risk), D-001 and D-003;
    - coordinator-2026-10-25 D-001 to D-013;
    - wi-971 D-001 and D-002;
    - wi-977 D-001;
    - wi-976 D-001 to D-022;
    - wi-878 D-001 to D-008;
    - WI-920's re-judge departures.
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
