# Handoff 2026-10-31a (headless leg 25): WI-966 landed; WI-977 built through W13, round 1 next

It replaces [handoff-2026-10-26b-leg24-coordinator.md](handoff-2026-10-26b-leg24-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 25 (loop session
`20261031T174835Z-e602ab`, coordinator session
`06c9d5bc-78c2-4fd3-841c-8cb5508bd256`) found Codex back (a probe at 12:49
local), took WI-966 through its checkpoint, a gate, a dispute fix round, a
second checkpoint and a second gate, and landed it; then built WI-977 from
its intent set through plan step W13.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** WI-966 landed at `2aaf9f66f` (sitting 007's amendment act
  re-attests SR-031, LLR-031, TC-031, SR-137, LLR-155, TC-150, LLR-156 and
  TC-152); the sweep minted the re-mint WI-984; `55fe67d82` filed OI-118,
  its owner row WI-985 and WI-984's needs on OI-118 (coordinator-2026-10-31
  D-002). The gate's five MINORs are follow-ups in status.md's unfiled list
  (wi-966 D-017). `check_trajectory` still warns on WI-982's and WI-983's
  40-character spec stems (ceiling 37): shorten each at its scope critique.
- **Machinery-landing rule:** WI-966 changed the policy readers every hook
  and agent route takes, and bootstrap's in-place policy writer; WI-977's
  landing waits until the cycle has run through those (any hook commit
  and any agent route has, since this leg's commits ran through them; a
  bootstrap scaffold or re-sync has not).
- **Lane `wi-977`** (worktree `C:/Projects/ai-template.wt/wi-977`, tip
  `056ef98d4`, rebased onto `55fe67d82`; headless-marked): the intent set
  is complete (D-002, D-003), and plan steps W2 to W13 are built and
  committed one stage each through the attested bar (D-004 to D-014; no
  strict expected failure remains). The tip is an empty attestation
  commit carrying the review bar over the lane's fourteen touched test
  modules (`tests/test_dispatch.py`, `test_dispatch_admission.py`,
  `test_integrate.py`, `test_integrate_station.py`,
  `test_agent_loop_worker.py`, `test_agent_loop_policy.py`,
  `test_handback.py`, `test_verdict_record.py`, `test_loop_order.py`,
  `test_loop_provenance.py`, `test_adoption_record.py`,
  `test_coordinator_guard.py`, `test_blackout_window.py`,
  `test_resync_pack.py`); that bar ran 50 minutes under load. Next: counted
  round 1 (no stance) over `55fe67d82..056ef98d4` with that `--tests`
  list, REVIEW-B first; then W14 (Terra's reconcile from the spine change
  lists in D-005 to D-013, the closure check, one combined sitting with
  HATS as the plan's W14 names) and the gate; W15 at the landing. Open
  readings for the reconcile: `lane_completion` has no production reader
  since W7 (D-009, D-013); LLR-152's module names `schedule.py` while its
  arm lives in `integrate._lane_bar_directives` (D-012).
- **Lane `wi-966`:** landed; its worktree may go. Its tips are in
  `archive/lanes` (`baa6db923`).
- **Lane `wi-963`:** unchanged, holds for the owner (OI-115).
- **Watermark** on trunk: WI 985, SR 246, LLR 360, IF 308, TC 399, OI 118;
  acts to seq 162. WI-977 allocated no id.
  - Lane-held ids: wi-963 LLR-342 and TC-373.
  - A new lane's Terra floor is SR-247, LLR-361, TC-400 and IF-309.
- **Smoke ceiling:** `max-tests` 3410 (trunk's tier 3300; WI-977's lane
  3301). The tier read CPU 437 to 581 s against `cpu-seconds = 540` this
  leg, over only under load (reported; the audit judges it).
- **Full suite:** run at `55fe67d82` this close-out, two halves from the
  detached critique checkout: 3515 passed, 8 skipped (16:29) and 3893
  passed, 25 skipped (12:39).
- **Usage:** this close-out's ingest recorded this session, its
  sub-agents and leg 24's tail (both runs exit 0). The next close-out
  passes `--session 06c9d5bc-78c2-4fd3-841c-8cb5508bd256`.
- **Strict lints:** clean on trunk and in `wi-977`. No judgement is
  active; `docs/work/pause` is tracked and unchanged.
- **Scratch:** this leg's root
  `C:/Projects/ai-template.wt/review-tmp/2026-10-31a-leg25/` holds the
  briefs, the stage briefs (`wi977-stage-common.md`) and the builders'
  basetemps; it may go once WI-977's round 1 is filed. Leg 24's root may
  go; keep the leg-07 root until WI-963 lands.

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
| 4 | WI-977 | Built through W13: counted round 1, then W14's checkpoint and the gate; it lands alone, before the managed loop is unpaused |

**Never claimed by a leg:** WI-684 (waits on OI-98, the owner's re-sync),
WI-795 (OI-105, then WI-820), WI-908 (the owner present), WI-964 (the
owner's Mac), WI-827 (attended only; it never lands from a lane), WI-967
(OI-115's placeholder), WI-978 until OI-116 is ruled, WI-980 and WI-981
(OI-117), WI-984 and WI-985 (OI-118), the successor rows WI-982 and WI-983
until the owner orders them into this table, and every row under
`docs/work/deferred/` (D-011, D-016).

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).

## For the owner

- **SN-028's act, on trunk** (OI-118, its owner row WI-985):
  `intake.py snapshot --approves stakeholder-needs=<your ruling record> --reattests SN-028`,
  adding `--verdict docs/reviews/wi-966/007-ADJUDICATE-d8f6fd3.md` where
  the route asks for it, in its own commit; then rule OI-118, which
  releases WI-985 and lets the re-mint WI-984 close citing the act.
  Sitting 003 notes that SN-028 still carries the tag `shell`, which
  reached CROSS-PLATFORM for the retired sh parse: keep or drop it.
- **SN-036's act, on trunk** (OI-117, its owner row WI-981), unchanged:
  `intake.py snapshot --approves stakeholder-needs=docs/log.d/2026-10-25-wi976-sn036-ruling.md --reattests SN-036`,
  adding `--verdict docs/reviews/wi-976/016-ADJUDICATE-9d6ad4c.md`; then
  rule OI-117 (WI-981, WI-980).
- **The FileBackup re-sync (OI-98)**: unblocked since WI-976 landed
  (coordinator-2026-10-25 D-003). WI-966 changes what an adopter's policy
  file may hold and makes bootstrap's in-place flags refuse a form they
  cannot edit (its RESYNC entry).
- **Order or re-scope the two successor rows** WI-982 and WI-983; each
  owes its scope critique before its claim.
- **Rule OI-116** (WI-978; recommendation (a), spine only) and **OI-115**
  (WI-963's settlement fix; recommendation (a)).
- **Push `refactor_again`** so WI-910's landing tip can carry CI's state, or
  rule that the WSL POSIX evidence route (wi-931 D-002) stands in for CI on
  that Done-when item (coordinator-2026-10-25 D-001).
- **Confirm or overrule:**
  - wi-966 D-009 to D-017 (D-013: the fix round's bootstrap.py size bump,
    1517 to 1599 SLOC; D-017: the gate's MINORs as follow-ups);
    coordinator-2026-10-31 D-001, D-002; wi-977 D-003 to D-014 (D-004:
    two handback tests converted at W2; D-007: agent_common.py's one-line
    bump; D-014: the RESYNC anchor at the lane's rebased base);
  - carried from leg 24: wi-966 D-005 (high risk) and D-001 to D-004,
    D-006 to D-008; wi-977 D-002; coordinator-2026-10-26 D-004;
  - carried from leg 23: wi-976 D-024 (high risk) and D-025 to D-029;
    coordinator-2026-10-26 D-001 (high risk), D-002 and D-003;
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
