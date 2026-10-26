# Handoff 2026-10-25d (headless leg 22): P6 filed and landed as WI-979; WI-971 landed; WI-966 and WI-977 claimed

It replaces [handoff-2026-10-25c-leg21-coordinator.md](handoff-2026-10-25c-leg21-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 22 (loop session
`20261025T055732Z-64b2b6`, coordinator session
`ccf9f9e0-06af-4288-a57a-92c4b07f1df6`) filed P6, ran four scope critiques
and their confirming rounds, claimed four rows under one scoped unpause,
passed three single plans, and landed WI-971 and WI-979. It carries no
`Overnight: stop` line: the next rows move without the owner.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** the filings (`15fe570b2`, `dc7e9db4b`), the scoped unpause
  (`42997ceab`, four claims, the restore `a1984f739`), WI-971's landing
  (`deebc18f6`), WI-979's (`489678a52`), then this close-out. Both lane tips
  are archived in `archive/lanes`; both sweeps minted nothing.
- **Lane `wi-966`** (worktree `C:/Projects/ai-template.wt/wi-966`, at
  `a1984f739`, no commits of its own; headless-marked by its claim):
  scope critique passed (planmode none). Next: move the branch to trunk's
  tip (it has no commit of its own), then Terra's intent turn (SR-137's
  line-shape and two-reader clauses out, its one-home, duplicate and
  invalid-dial obligations kept; IF-037's data cell; SN-028's and SR-031's
  premise wording), tests, code. SN-028 is on a held rung: its act is the
  owner's, on trunk after the landing (D-023's route).
- **Lane `wi-977`** (worktree `C:/Projects/ai-template.wt/wi-977`, tip
  `2970c3879`, base `a1984f739`; headless-marked): plan, critique 1 (one
  MAJOR), the one revision, critique 2 (APPROVE, one MINOR) and the pass
  record are committed (wi-977 D-001). Next: rebase onto trunk's tip
  (records only, so before any build), then Terra's intent turn for the
  plan's spine step (TCs first), then the build in the plan's stages; the
  critique 2 MINOR binds W4's build brief (the dispatcher's merged-lane
  count moves with the one-id lane change).
- **Lane `wi-976`:** the owner re-claimed it attended (`c230f5b32`) and
  ruled wi-976 D-023: SN-036's act moves to trunk after the landing (the
  held-rung lane rule refuses a MEANING act from a lane); the lane was reset
  to the re-claim and the act commit kept under the tag
  `attended/wi-976-sn036-act`; tip `734a0be1e` records D-023. Owed in the
  lane: amend the Done-when's "The owner-held step" to that route and have
  a sitting bless the edit; then P11 (TC-211's re-judge over sitting 016's
  brief and verdict) and the landing, as leg 21's D-022 says, with the
  RESYNC re-anchor and `scripts/kitlib/bootstrap_manifest.py` added to its
  overwrite list (D-021). Its rebase now meets WI-979's section 4 in
  `spine-questions.md` and two new RESYNC entries.
- **Lane `wi-963`:** unchanged, holds for the owner (OI-115).
- **Watermark** on trunk: WI 979, SR 246, LLR 359, IF 308, TC 398, OI 116;
  acts to seq 159 (160 and 161 lane-held in wi-976).
  - Lane-held ids: wi-963 LLR-342 and TC-373; wi-976 LLR-360 and TC-399.
  - A new lane's Terra floor is SR-247, LLR-361, TC-400 and IF-309.
- **Machinery landed this leg** (revision 37: the next machinery landing
  waits until the cycle has run through these steps): WI-971 changed every
  per-commit rule's lane walk and squash range (exercised by WI-979's own
  landing); WI-979 changed the single-plan prompt (a skill line) and the
  LLR sittings' questions (section 4, put only to the first LLR sitting at
  a component scope or a re-cut). The next LLR sitting (WI-976's, WI-966's
  or WI-977's) runs through the second.
- **Smoke ceiling:** `max-tests` 3410 (trunk's tier about 3310). The bar's
  CPU reading on WI-979's staged squash was 649.3 s against `cpu-seconds =
  540` under another project's load (a WARN only `run.cmd audit` judges).
- **Full suite** at `489678a52`, from a detached worktree, in two halves:
  3751 passed, 21 skipped (66:06) and 3605 passed, 12 skipped (22:17).
- **Usage:** this close-out's ingest recorded this session, its sub-agents
  and leg 21's tail. The next close-out passes
  `--session ccf9f9e0-06af-4288-a57a-92c4b07f1df6`.
- **Strict lints:** clean on trunk. No judgement is active;
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** this leg's root `C:/Projects/ai-template.wt/review-tmp/2026-10-25d-leg22/`
  may go; keep leg 21's and leg 20's roots until WI-976 lands and the
  leg-07 root until WI-963 lands. Free disk read 8.3 GB at close-out.

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
| 3 | WI-976 | Movable (wi-976 D-023): the Done-when's owner-held step amended to the trunk route and blessed at a sitting, then P11 and the landing alone; the owner re-takes SN-036's act on trunk after it |
| 4 | Filing P8 | Waits on its filing calls (P6 landed as WI-979) |
| 5 | WI-966 | Claimed: to trunk's tip, then intent, tests, code; it lands before item 10 step 5 |
| 6 | WI-977 | Claimed, plan passed: rebase, intent, then the build; it lands alone, after WI-976, before the managed loop is unpaused |

**Never claimed by a leg:** WI-684 (waits on OI-98, the owner's re-sync),
WI-795 (OI-105, then WI-820), WI-908 (the owner present), WI-964 (the
owner's Mac), WI-827 (attended only; it never lands from a lane), WI-967
(OI-115's placeholder), WI-978 until OI-116 is ruled, and every row under
`docs/work/deferred/` (D-011, D-016).

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).

## For the owner

- **SN-036's act, on trunk after WI-976 lands** (your D-023): the lane's
  Done-when amendment and its sitting come first; then the same
  `intake.py snapshot` command, re-taken on trunk.
- **Rule OI-116** (WI-978: does the WI space ride the watermark carrier,
  re-opening revision 33? recommendation (a), spine only).
- **Rule OI-115** (WI-963's settlement fix; recommendation (a)).
- **Push `refactor_again`** so WI-910's landing tip can carry CI's state, or
  rule that the WSL POSIX evidence route (wi-931 D-002) stands in for CI on
  that Done-when item (coordinator-2026-10-25 D-001).
- **Hold the FileBackup re-sync (OI-98) until WI-976 lands** (D-003).
- **Confirm or overrule:**
  - wi-979 D-002 (high risk: the coordinator raised a reviewer's MINOR to
    MAJOR by reach, which cost a fix round and a second round), D-001 and
    D-003;
  - coordinator-2026-10-25 D-010 to D-013, notably D-010 (the rubric seeded
    and adopter-owned; the Architect role, the dual-plan planner line and
    the dry run's other anchor edits left out of WI-979) and D-013 (WI-979
    claimed beside the table's rows);
  - wi-971 D-001, D-002; wi-977 D-001 (the planner's calls);
  - wi-976 D-017 to D-022, coordinator-2026-10-25 D-006 to D-009,
    wi-976 D-001 to D-016, coordinator-2026-10-25 D-001 to D-005, wi-878
    D-001 to D-008 and WI-920's re-judge departures (carried).
- **Still open from earlier handoffs**, every item they listed:
  coordinator-2026-10-24 D-001 to D-005 and wi-856 D-001 to D-006;
  coordinator-2026-10-23 D-001 to D-005 (D-002 and D-004 high risk) and
  wi-851 D-001 to D-014; coordinator-2026-10-22 D-002 to D-004, wi-850
  D-001 to D-012 (D-002 high risk), wi-961 D-010 to D-017 and the earlier
  items those handoffs carried; the `--wi` primary-checkout preflight call
  (wi-960 D-016); removing the temporary `Bash(codex exec *)` allow rule;
  your owner-held rows.
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
