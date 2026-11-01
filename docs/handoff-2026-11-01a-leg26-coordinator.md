# Handoff 2026-11-01a (headless leg 26): WI-977 gated twice, ready to land

It replaces [handoff-2026-10-31a-leg25-coordinator.md](handoff-2026-10-31a-leg25-coordinator.md)
as the resume map. The procedure is in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 26 ran under loop session
`20261031T174835Z-e602ab`; its coordinator session was
`47f2e95e-8df7-43ff-ac18-8a19ad7a82f1`. It took WI-977 through:

- two counted rounds and one fix round;
- the W14 checkpoint (sittings 005, 006 and 007);
- a gate, whose one MAJOR dispute 011 ruled FIX;
- a second gate, all MINOR.

The lane is at a safe committed point and owes only its landing.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** unchanged since `41dfbb17e` apart from this close-out commit.
  This leg changed no trunk code.
- **Lane `wi-977`** (worktree `C:/Projects/ai-template.wt/wi-977`):
  - The tip is `4800ebd03`, rebased onto `41dfbb17e`. The rebase moved only
    paths the lane does not touch. The RESYNC entry is re-anchored
    `[since 41dfbb17e]` (D-022).
  - The lane is headless-marked: it was claimed and built under the loop
    marker, so it lands headless.
  - Every one of the 23 rows is judged:
    - sitting 005 blessed SR-144, SR-148, SR-156 and TC-146, and found
      LLR-058 CLARITY;
    - re-sit 006 blessed sixteen rows;
    - re-sit 007 blessed LLR-207 and TC-205.
  - After the sittings only traced cells changed: dispute 011's FIX
    (D-024). This includes the `code_symbol` of LLR-143 and LLR-312, which
    are outside the set.
  - **Next is the landing.** Rebase if trunk moved. Run the unchanged-rows
    check of each verdict's rows from the verdict's own commit to the tip.
    Take the act turns: `coordinator_adjudicate.py act` from
    `docs/reviews/wi-977/005-ADJUDICATE-a7ebe2f.md`, `006-ADJUDICATE-e49def4.md`
    and `007-ADJUDICATE-982f443.md`. 005's act carries LLR-058's CLARITY
    re-anchor. Then follow recipes §3: squash, regenerate, the bar, close,
    archive the tips, sweep and the re-mint.
  - Run `overnight_legs.py check-lane wi-977` before the squash.
  - At W15, regenerate `docs/cli-reference.md` (it still shows the old
    `--wi` list help) and `prompts/CATALOG.md`.
  - The review bar's `--tests` list is the lane's seventeen touched modules
    (D-021, D-022).
- **Machinery-landing rule:** WI-966 changed the policy readers and
  bootstrap's in-place policy writer. Every hook commit and agent route this
  leg ran used the new readers. No bootstrap scaffold or re-sync has run
  through the new writer outside the test suite. The landing leg decides
  whether that holds WI-977's landing, and records the call.
- **Follow-ups owed at WI-977's landing** (file them, or list them for the
  owner):
  - the gates' MINORs (D-023, D-025). Among them, the sentence in
    `PROCESS_OPTIONS.md` that still offers batched dev slices: an adopter
    who follows it meets a preflight refusal (fail-closed). The worker
    template's "focus row first" line is another;
  - `agent_brief.lane_completion` has no production reader (D-017);
  - two stale `code_symbol` tokens (LLR-058 `ready`, LLR-161
    `_split_lines`; D-024);
  - the coverage-extension note on an id-less parked `WI-*.md` (D-015).
- **Lane `wi-963`:** unchanged; it holds for the owner (OI-115).
- **Watermark** on trunk is unchanged: WI 985, SR 246, LLR 360, IF 308,
  TC 399, OI 118; acts to seq 162.
  - WI-977 allocated no id.
  - Lane-held ids: wi-963 holds LLR-342 and TC-373.
  - A new lane's Terra floor is SR-247, LLR-361, TC-400 and IF-309.
- **Smoke:** the tier read 3301 tests on the lane, CPU 488 to 490 s
  against `cpu-seconds = 540`, which is within the limit.
- **Full suite:** not run this close-out. Trunk code did not change, and
  the lane's code runs in full at its landing.
- **Usage:** both ingest runs exited 0. The next close-out passes
  `--session 47f2e95e-8df7-43ff-ac18-8a19ad7a82f1`.
- **Strict lints:** clean on trunk and in `wi-977`. No judgement is
  active, and `docs/work/pause` is tracked and unchanged.
- **Scratch:** this leg's root is
  `C:/Projects/ai-template.wt/review-tmp/2026-10-31b-leg26/`. It holds the
  briefs, Terra prompts and checker scripts. It may go once WI-977 lands.
  Leg 25's root may go too. Keep the leg-07 root until WI-963 lands.

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
through the last landing's changed steps.

**Only the rows in this table are claimed**, in order and under their
`needs`. When no row in it can move without the owner, the leg closes out
with the `Overnight: stop` line.

| # | Row | Next |
|---|---|---|
| 1 | WI-963 | Held: OI-115 (the owner); recount its module size at the rebase |
| 2 | WI-910 | Held: its Done-when checks CI's macOS and Linux state on the landing tip, which needs a push (coordinator-2026-10-25 D-001) |
| 3 | Filing P8 | Waits on its filing calls (P6 landed as WI-979) |
| 4 | WI-977 | Ready to land: the act turns from sittings 005 to 007, then the squash. It lands alone, before the managed loop is unpaused |

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

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).

## For the owner

- **SN-028's act, on trunk** (OI-118, its owner row WI-985), unchanged:
  `intake.py snapshot --approves stakeholder-needs=<your ruling record> --reattests SN-028`,
  adding `--verdict docs/reviews/wi-966/007-ADJUDICATE-d8f6fd3.md`; then
  rule OI-118. Keep or drop SN-028's `shell` tag (sitting 003).
- **SN-036's act, on trunk** (OI-117, its owner row WI-981), unchanged:
  `intake.py snapshot --approves stakeholder-needs=docs/log.d/2026-10-25-wi976-sn036-ruling.md --reattests SN-036`,
  adding `--verdict docs/reviews/wi-976/016-ADJUDICATE-9d6ad4c.md`; then
  rule OI-117 (WI-981, WI-980).
- **The FileBackup re-sync (OI-98)**: unblocked since WI-976 landed.
  WI-966 changes what an adopter's policy file may hold; WI-977, once
  landed, makes both `--wi` flags take one id (its RESYNC entry).
- **Order or re-scope the two successor rows** WI-982 and WI-983; each
  owes its scope critique before its claim.
- **Rule OI-116** (WI-978; recommendation (a), spine only) and **OI-115**
  (WI-963's settlement fix; recommendation (a)).
- **Push `refactor_again`** so WI-910's landing tip can carry CI's state, or
  rule that the WSL POSIX evidence route (wi-931 D-002) stands in for CI on
  that Done-when item (coordinator-2026-10-25 D-001).
- **Confirm or overrule:**
  - from this leg, wi-977 D-015 to D-025. Note especially:
    - D-019, D-020 and D-021, the coordinator's openly recorded mechanical
      repairs to Terra's cells: a misplaced module cell, double-encoded
      characters, and base words restored;
    - D-024's tag for `_stop_run`, which names two LLRs;
    - D-016's one-line `agent_loop.py` size bump.
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
