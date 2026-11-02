# Handoff 2026-11-01c (headless leg 28): WI-987 and WI-967 landed; WI-963 rebases next

It replaces [handoff-2026-11-01b-leg27-coordinator.md](handoff-2026-11-01b-leg27-coordinator.md)
as the resume map. The procedure is in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 28 ran under loop session
`20261101T190826Z-4e6480`; its coordinator session was
`fc5c6ac3-0b9d-4124-a19a-6b715a62e2e7`. It ran the scope critiques of
queue rows 1, 2 and 4, claimed rows 1 and 2 under one scoped unpause, and
landed both. It closed out at 34% occupancy rather than start row 3's
rebase and build.

## State (trunk `refactor_again`, nothing pushed)

- **WI-987 landed** as `308259971`: the open-items page lists every owing
  stakeholder need and stakeholder from `baseline_snapshot.needs_owing`;
  SN-028 and SN-036 now show in section 2. Single plan (one revision),
  sitting 003 MEANING+BLESS of LLR-271 and TC-269, act seq 164. Its re-mint
  WI-988 is closed (`37bcca3b8`).
- **WI-967 landed** as `9a5952fb0`: every new act-ledger entry records
  `copied` (the registry files its act wrote); a legacy entry reads as copy
  set unknown; the whole-file and commit-bound rules refuse an omission.
  New LLR-361 and TC-400, approved at re-sit 004 (after sitting 003's two
  returns), act seq 165, whose own entry is the first to carry `copied`.
  The lane rebased onto `37bcca3b8` before its gate (wi-967 D-004). The
  sweep minted nothing.
- **WI-978's scope critique** (owed since filing) is answered: two findings
  adopted, the confirming round APPROVE (coordinator-2026-11-01 D-007). It
  is claimable.
- **Archive:** `archive/lanes` carries wi-987's tip `11b581033` and
  wi-967's rebased tip `180697811` with its pre-rebase tip `df8222518`. The
  `wi-987` and `wi-967` branches and worktrees are kept, as for earlier
  lanes.
- **Lane `wi-963`:** unchanged; it now rebases onto `9a5952fb0` (row 3).
- **Watermark:** WI 988, SR 246, LLR 361, IF 308, TC 400, OI 118. Acts run
  to seq 165.
  - Lane-held ids: wi-963 holds LLR-342 and TC-373.
  - A new lane's Terra floor is SR-247, LLR-362, TC-401 and IF-309.
- **Bars:**
  - Smoke on WI-987's staged squash: 3301 passed; CPU 616.0 s against
    `cpu-seconds = 540` (reported only, a load reading; `run.cmd audit`
    judges it). On WI-967's: 3301 passed, CPU 507.0 s, within.
  - `trace.py --strict` and `check_trajectory.py --strict` clean at both
    landings. The full suite's result at close-out is in this leg's log
    fragment.
- **Usage:** both ingest runs exited 0. The next close-out passes
  `--session fc5c6ac3-0b9d-4124-a19a-6b715a62e2e7`.
- **Pause:** `docs/work/pause` is tracked and byte-identical to before the
  unpause (`3f4b989df`), and no judgement is active.
- **Scratch:** this leg's root is
  `C:/Projects/ai-template.wt/review-tmp/2026-11-01c-leg28/`; leg 27's root
  may go now. Keep the leg-07 root until WI-963 lands.
- **Follow-ups** from both lanes' gates are under status.md's "Unfiled
  follow-ups" (wi-967 D-005, wi-987 D-001 and D-005). The RESYNC overwrite
  list's missing `scripts/acceptance_record.py` matters before the
  FileBackup re-sync.

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
coordinator-2026-10-25 D-009 and D-013 and coordinator-2026-11-01 D-003.

Each row that changes machinery lands alone, after the cycle has run
through the last landing's changed steps. WI-967 changed the act ledger's
writer and its commit-time check: the next lane's act turn runs through
them.

**Only the rows in this table are claimed**, in order and under their
`needs`.

| # | Row | Next |
|---|---|---|
| 1 | WI-963 | Rebase onto `9a5952fb0`; its claim copy takes the trunk copy's OI-115 Done-when item (coordinator-2026-11-01 D-004); recount its module size at the rebase; build settlement from the ledger's `copied`; its act turn runs WI-967's changed step |
| 2 | WI-978 | Claim (its critique is confirmed, D-007) under the next scoped unpause. Machinery: lands alone, after row 1's act has run WI-967's step |
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
- the successor rows WI-982 and WI-983, until the owner orders them into
  this table;
- every row under `docs/work/deferred/` (D-011, D-016).

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).

## For the owner

- **WI-967's spec grew past three times its filing size** with its adopted
  critique dispositions (2463 to 8412 bytes; coordinator-2026-11-01 D-006),
  including a Trust section whose shared Ruling is yours to confirm or
  overrule. The row has landed on it.
- **Rows still held:** push `refactor_again` so WI-910's landing tip
  carries CI's state, or rule that the WSL POSIX evidence route (wi-931
  D-002) stands in for CI on that Done-when item (coordinator-2026-10-25
  D-001). Make P8's filing calls, or order WI-982 and WI-983 into the table
  (each owes its scope critique before its claim).
- **SN-028's act, on trunk** (OI-118, its owner row WI-985), unchanged:
  `intake.py snapshot --approves stakeholder-needs=<your ruling record> --reattests SN-028`,
  adding `--verdict docs/reviews/wi-966/007-ADJUDICATE-d8f6fd3.md`; then
  rule OI-118. Keep or drop SN-028's `shell` tag (sitting 003). It now
  shows on the open-items page while owed.
- **SN-036's act, on trunk** (OI-117, its owner row WI-981), unchanged:
  `intake.py snapshot --approves stakeholder-needs=docs/log.d/2026-10-25-wi976-sn036-ruling.md --reattests SN-036`,
  adding `--verdict docs/reviews/wi-976/016-ADJUDICATE-9d6ad4c.md`; then
  rule OI-117 (WI-981, WI-980).
- **The FileBackup re-sync (OI-98):** unblocked. Two new RESYNC entries
  this leg: the open-items page's needs section, and the act ledger's
  `copied` record (fix its overwrite list's missing
  `scripts/acceptance_record.py` first: a follow-up).
- **Confirm or overrule:**
  - from this leg: coordinator-2026-11-01 D-005 to D-007; wi-987 D-001 to
    D-005; wi-967 D-001 to D-005. Note especially:
    - wi-987 D-003 and wi-967 D-003, each re-grading a round-1 MAJOR (code
      traced to no LLR that states it) to checkpoint-owed spine text;
    - wi-987 D-002 and wi-967 D-002, the coordinator's openly recorded
      repairs to Terra's cells;
    - coordinator-2026-11-01 D-006's design calls: the `copied` field and
      the commit as the legacy boundary;
  - from the attended amendment: coordinator-2026-11-01 D-001 to D-003;
  - carried from leg 27: wi-977 D-026 and D-027;
  - carried from leg 26: wi-977 D-015 to D-025 (D-019 to D-021 repairs,
    D-024's tag, D-016's size bump);
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
