# Handoff 2026-10-26a (headless leg 23): WI-976 landed; OI-117 and WI-981 to WI-983 filed; WI-966 and WI-977 at trunk's tip

It replaces [handoff-2026-10-25d-leg22-coordinator.md](handoff-2026-10-25d-leg22-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 23 (loop session
`20261025T055732Z-64b2b6`, coordinator session
`b0e50d15-3f31-4e62-9db7-77c35ff39fec`) rebased and landed WI-976, filed
the owner row for SN-036's act with its open item and two successor rows,
and brought WI-966 and WI-977 to trunk's tip. It carries no
`Overnight: stop` line: the next rows move without the owner.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** WI-976's landing (`574cfcd53`), the sweep's re-mint WI-980
  (`37b30c751`), the filings (`acbf24dc1`), then this close-out. The lane's
  tips (the rebased tip, the pre-rebase tip `734a0be1e` the verdicts cite,
  and the replay chain `348518b27`) are archived in `archive/lanes`.
- **WI-976 landed** without SN-036's act, as the owner ruled (wi-976
  D-023): sitting 024 blessed the Done-when's new route. TC-211's re-judge
  (P11) recorded a FAIL, its finding ruled SUCCESSOR by sitting 021, so
  TC-211's observation of record is that fail until WI-983 re-inspects it.
- **Lane `wi-966`** (worktree `C:/Projects/ai-template.wt/wi-966`, at
  `acbf24dc1`, no commits of its own; headless-marked by its claim): scope
  critique passed (planmode none). Next: Terra's intent turn (SR-137's
  line-shape and two-reader clauses out, its one-home, duplicate and
  invalid-dial obligations kept; IF-037's data cell; SN-028's and SR-031's
  premise wording), tests, code. SN-028 is on a held rung: its act is the
  owner's, on trunk after the landing (WI-976's route). Its intent turn
  amends a need, so it is the first author turn through WI-976's hat block.
- **Lane `wi-977`** (worktree `C:/Projects/ai-template.wt/wi-977`, tip
  `b1438674c`, rebased onto `acbf24dc1`, records only; headless-marked):
  plan, two critiques and the pass record (wi-977 D-001). Next: Terra's
  intent turn for the plan's spine step (TCs first), then the build in the
  plan's stages; the critique 2 MINOR binds W4's build brief (the
  dispatcher's merged-lane count moves with the one-id lane change).
- **Lane `wi-963`:** unchanged, holds for the owner (OI-115).
- **Watermark** on trunk: WI 983, SR 246, LLR 360, IF 308, TC 399, OI 117;
  acts to seq 161.
  - Lane-held ids: wi-963 LLR-342 and TC-373.
  - A new lane's Terra floor is SR-247, LLR-361, TC-400 and IF-309.
- **Machinery landed this leg** (revision 37): WI-976 changed the
  sitting-brief composer (the hat block, the amendment arm's own module)
  and the spine-author prompt. The next mechanism landing waits until a
  sitting and an author turn have run through them: WI-966's intent turn
  and its checkpoint sitting do (coordinator-2026-10-26 D-001).
- **Smoke ceiling:** `max-tests` 3410 (trunk's tier 3300). The bar's CPU
  reading on WI-976's staged squash was 579.5 s against `cpu-seconds =
  540` (a WARN only `run.cmd audit` judges).
- **Full suite** at `acbf24dc1`, from a detached worktree, in two halves:
  3515 passed, 8 skipped (23:24) and 3862 passed, 25 skipped (23:14).
- **Usage:** this close-out's ingest recorded this session, its sub-agent
  and leg 22's tail. The next close-out passes
  `--session b0e50d15-3f31-4e62-9db7-77c35ff39fec`.
- **Strict lints:** clean on trunk. No judgement is active;
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** this leg's root `C:/Projects/ai-template.wt/review-tmp/2026-10-26a-leg23/`
  and leg 20's, 21's and 22's roots may go; keep the leg-07 root until
  WI-963 lands. Free disk read 8.5 GB at close-out.

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
D-019), coordinator-2026-10-21 D-004 to D-006, and the owner's 2026-10-23
direction that a scope critique settles a row's scope and never grows it
(the rubric's S7); rows 6 and 7 by coordinator-2026-10-25 D-009 and D-013.
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
| 4 | WI-966 | Claimed, at trunk's tip: intent, tests, code; it lands before item 10 step 5 |
| 5 | WI-977 | Claimed, plan passed, rebased: intent, then the build; it lands alone, before the managed loop is unpaused |

**Never claimed by a leg:** WI-684 (waits on OI-98, the owner's re-sync),
WI-795 (OI-105, then WI-820), WI-908 (the owner present), WI-964 (the
owner's Mac), WI-827 (attended only; it never lands from a lane), WI-967
(OI-115's placeholder), WI-978 until OI-116 is ruled, WI-980 and WI-981
(OI-117), the new successor rows WI-982 and WI-983 until the owner orders
them into this table, and every row under `docs/work/deferred/` (D-011,
D-016).

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).

## For the owner

- **SN-036's act, on trunk** (OI-117, its owner row WI-981):
  `intake.py snapshot --approves stakeholder-needs=docs/log.d/2026-10-25-wi976-sn036-ruling.md --reattests SN-036`,
  adding `--verdict docs/reviews/wi-976/016-ADJUDICATE-9d6ad4c.md` where
  the route asks for it, in its own commit; then rule OI-117, which
  releases WI-981 and lets the re-mint WI-980 close citing the act.
- **The FileBackup re-sync (OI-98)** was held until WI-976 landed
  (coordinator-2026-10-25 D-003); it has landed.
- **Order or re-scope the two successor rows:** WI-982 (both adjudication
  routes widen a sitting's hats by the authoring work item's tags; sitting
  004) and WI-983 (a decomposition round's brief names a stopping-boundary
  line, and TC-211 is re-inspected; sitting 021). Each owes its scope
  critique before its claim.
- **Rule OI-116** (WI-978: does the WI space ride the watermark carrier?
  recommendation (a), spine only) and **OI-115** (WI-963's settlement fix;
  recommendation (a)).
- **Push `refactor_again`** so WI-910's landing tip can carry CI's state, or
  rule that the WSL POSIX evidence route (wi-931 D-002) stands in for CI on
  that Done-when item (coordinator-2026-10-25 D-001).
- **Confirm or overrule:**
  - wi-976 D-024 (high risk: the replay of acts 160 and 161 rebuilt by
    `git commit-tree`, each act commit's snapshot copy set to its live
    file at that commit, so the registry-integrity step passes), and
    D-025 to D-029 (the rebase's test fix, P11 before the Done-when edit
    and Sol as its inspector, the round's triage, the Done-when text);
  - coordinator-2026-10-26 D-001 (high risk: WI-976 landed as the run-through
    of WI-979's changed steps, the single-plan prompt line not yet run),
    D-002 (WI-980 held on OI-117) and D-003 (the successor filings; sitting
    021 was judged by the session that wrote the record under judgement,
    which it disclosed);
  - carried from leg 22: wi-979 D-002 (high risk), D-001 and D-003;
    coordinator-2026-10-25 D-010 to D-013; wi-971 D-001, D-002; wi-977
    D-001; wi-976 D-017 to D-022, coordinator-2026-10-25 D-006 to D-009,
    wi-976 D-001 to D-016, coordinator-2026-10-25 D-001 to D-005, wi-878
    D-001 to D-008 and WI-920's re-judge departures.
- **Still open from earlier handoffs**, every item they listed:
  coordinator-2026-10-24 D-001 to D-005 and wi-856 D-001 to D-006;
  coordinator-2026-10-23 D-001 to D-005 (D-002 and D-004 high risk) and
  wi-851 D-001 to D-014; coordinator-2026-10-22 D-002 to D-004, wi-850
  D-001 to D-012 (D-002 high risk), wi-961 D-010 to D-017 and the earlier
  items those handoffs carried; the `--wi` primary-checkout preflight call
  (wi-960 D-016); removing the temporary `Bash(codex exec *)` allow rule;
  filing your 2026-10-25 ruling that an owner-held step is an open item
  (attended); your owner-held rows.
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
