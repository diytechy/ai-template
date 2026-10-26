# Handoff 2026-10-26b (headless leg 24): WI-966 through round 1; WI-977's intent set begun; Codex at its usage limit

It replaces [handoff-2026-10-26a-leg23-coordinator.md](handoff-2026-10-26a-leg23-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 24 (loop session
`20261025T055732Z-64b2b6`, coordinator session
`c1cbad62-9897-4bf9-ac8e-59086e43e7e4`) built WI-966 through its first
counted round and began WI-977's intent set, then met the Codex account's
usage limit, which stops every Terra and Sol call until its reset.

Resume-not-before: 2026-11-02T00:05

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** this close-out only, on `07e135e5f`. No landing this leg.
  `check_trajectory` warns that WI-982's and WI-983's spec filename stems
  run 40 characters (ceiling 37): shorten each at its scope critique.
- **Codex:** the account's usage limit, first met at 06:44 local on
  2026-10-26; the CLI names its reset 2026-11-02 00:00 local (re-probed
  08:00 and 08:49). The launcher waits for the line above
  (coordinator-2026-10-26 D-004).
- **Lane `wi-966`** (worktree `C:/Projects/ai-template.wt/wi-966`, tip
  `942d50126`, base `07e135e5f`; headless-marked; `check-lane` passes):
  intent set (D-001, D-002), tests first (D-003), code (D-004), a
  fail-closed fix stage (D-005 high risk, D-006), counted round 1 at
  `5c805ce` with every finding MINOR (D-007, D-008). The tip carries the
  review bar's attestation at `5c805ce` for its nine `--tests` files
  (D-007's round names them). Next: the checkpoint. Terra, resumed,
  reconciles the whole set against the settled code from the spine change
  list in D-003, D-004, D-006 and D-008 (HATS=SN-028); the closure check;
  one combined sitting (SN-028's amendment ruled CLARITY or MEANING: its
  act is the owner's on trunk either way, on WI-976's route); then the
  uncounted gate in convergence stance, with Sol back in REVIEW-A. D-008's
  two code findings are successor rows at the landing unless the sitting
  routes them to the builder.
- **Lane `wi-977`** (worktree `C:/Projects/ai-template.wt/wi-977`, tip
  `d799eb543`, rebased onto `07e135e5f`; headless-marked; `check-lane`
  passes): plan passed (D-001); the intent set's first part committed,
  incomplete (D-002 lists the rows W1 still owes). Next: Terra resumed to
  finish W1, then the build in the plan's stages; critique 2's MINOR binds
  W4's build brief.
- **Lane `wi-963`:** unchanged, holds for the owner (OI-115).
- **Watermark** on trunk: WI 983, SR 246, LLR 360, IF 308, TC 399, OI 117;
  acts to seq 161. Neither lane allocated an id.
  - Lane-held ids: wi-963 LLR-342 and TC-373.
  - A new lane's Terra floor is SR-247, LLR-361, TC-400 and IF-309.
- **Machinery:** the run-through coordinator-2026-10-26 D-001 waits for
  is half done: WI-966's intent turn ran through WI-976's author-prompt
  hat block (wi-966 D-002); its checkpoint sitting has not run yet.
- **Smoke ceiling:** `max-tests` 3410 (trunk's tier 3300). WI-966's bar
  read CPU 483.5 to 493.1 s against `cpu-seconds = 540`.
- **Full suite:** not run this leg; trunk's code did not change. Last run
  at `acbf24dc1` (leg 23).
- **Usage:** this close-out's ingest recorded this session, its sub-agents
  and leg 23's tail. The next close-out passes
  `--session c1cbad62-9897-4bf9-ac8e-59086e43e7e4`.
- **Strict lints:** clean on trunk and in `wi-966`. No judgement is active;
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** this leg's root `C:/Projects/ai-template.wt/review-tmp/2026-10-26b-leg24/`
  holds the round's briefs and the builders' basetemps; it may go once
  WI-966's checkpoint has run. Leg 20's to 23's roots may go; keep the
  leg-07 root until WI-963 lands.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say, through the route:

- Two full-lane reviewers run per round: Codex Sol at medium (REVIEW-A,
  `codex_call.py REVIEW-A`) and Claude Opus at high (REVIEW-B, launched
  with the Agent tool's `effort: "high"`). Each gets only its rendered
  brief.
- In a headless leg, launch REVIEW-B first.
- Every render refuses a tip with no attested review bar for its
  `--tests`, so attest the tip first.
- While Codex has been unavailable for more than two hours, a fresh
  independent Claude reviewer fills REVIEW-A, recorded in the lane's
  decisions (wi-966 D-007).

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
| 4 | WI-966 | Round 1 clean of BLOCKER and MAJOR: the checkpoint (Terra's reconcile, the sitting), then the gate; it lands before item 10 step 5 |
| 5 | WI-977 | Plan passed; intent set part 1 committed: Terra finishes W1, then the build; it lands alone, before the managed loop is unpaused |

**Never claimed by a leg:** WI-684 (waits on OI-98, the owner's re-sync),
WI-795 (OI-105, then WI-820), WI-908 (the owner present), WI-964 (the
owner's Mac), WI-827 (attended only; it never lands from a lane), WI-967
(OI-115's placeholder), WI-978 until OI-116 is ruled, WI-980 and WI-981
(OI-117), the successor rows WI-982 and WI-983 until the owner orders
them into this table, and every row under `docs/work/deferred/` (D-011,
D-016).

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).

## For the owner

- **Codex's usage limit** (reset 2026-11-02 00:00 local): every Terra and
  Sol call fails until then, and the launcher waits for the
  `Resume-not-before:` line. To resume sooner, switch the Codex account
  (`codex logout`, `codex login`) and restart the launcher; or rule
  whether a Claude session may stand in for the spine author
  (coordinator-2026-10-26 D-004's alternative).
- **SN-036's act, on trunk** (OI-117, its owner row WI-981):
  `intake.py snapshot --approves stakeholder-needs=docs/log.d/2026-10-25-wi976-sn036-ruling.md --reattests SN-036`,
  adding `--verdict docs/reviews/wi-976/016-ADJUDICATE-9d6ad4c.md` where
  the route asks for it, in its own commit; then rule OI-117, which
  releases WI-981 and lets the re-mint WI-980 close citing the act.
- **SN-028's amendment** (WI-966) will need your act on trunk after the
  landing, as SN-036's does; Terra reads it as MEANING (wi-966 D-002).
- **The FileBackup re-sync (OI-98)**: WI-976 has landed, so it is
  unblocked (coordinator-2026-10-25 D-003).
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
  - wi-966 D-005 (high risk: a privacy key the parse holds outside
    `[policies]` fails closed in every reader, a misplaced copy winning
    over `[policies]` and the legacy file), D-001 to D-004 and D-006 to
    D-008 (D-007: REVIEW-A filled by a Claude reviewer while Codex is
    out); wi-977 D-002; coordinator-2026-10-26 D-004;
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
