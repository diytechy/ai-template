# Handoff 2026-10-22c (headless leg 13): WI-961 through its counted rounds

It replaces [handoff-2026-10-22b-leg12-coordinator.md](handoff-2026-10-22b-leg12-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 13 (loop session
`20261021T045653Z-213020`, coordinator session
`3958b449-70cf-4328-ab90-b46ea845fb0c`) claimed WI-961 alone, passed its
single plan at the cap through one dispute sitting, ran P0's probes,
Terra's intent turn, the test commit, the code, two counted rounds (the
second APPROVE from both reviewers), one fix round, P8's live run and a
consolidation stage. Nothing landed. It carries no `Overnight: stop`
line: the next rows move without the owner.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** unchanged in code since leg 12; this leg's trunk commits are
  the scoped unpause (`7684e3c49`), the claim (`c0b78cc49`), the
  byte-identical restore (`1d6484cc5`) and this close-out. The full suite
  did not run: no code changed on trunk.
- **Lane `wi-961`** (claimed headless, so it lands headless; worktree
  `C:/Projects/ai-template.wt/wi-961`, base `1d6484cc5`, clean tip
  `8566393ad`, attested for the review bar over
  `tests/test_claude_transcripts.py tests/test_usage_ingest.py
  tests/test_usage_ingest_git.py tests/test_prompts.py
  tests/test_frame_context.py`):
  - plan: `docs/plans/WI-961/` (critique 1 and 2, pass record from
    dispute sitting 002's DISMISS);
  - P0's probes, the intent set, both rounds, the fix round and P8 are in
    `docs/decisions/wi-961.toml` D-001 to D-009 (D-007 holds the
    convergence map);
  - the intent set (Drafted): SR-244 (derived, SN-026, performance),
    LLR-347 to LLR-356, TC-386 to TC-395, IF-305; IF-065, IF-245 and
    IF-246 amended by addition;
  - rounds: `docs/reviews/wi-961/003`, `004` (round 1, CHANGES-REQUESTED),
    `005`, `006` (round 2, APPROVE, MINORs only).
- **WI-961's next steps, in order:**
  1. The checkpoint: Terra resumed through the route
     (`codex_call.py AUTHOR --resume --wi WI-961`) reconciles the whole set
     against the settled code. Its change list is
     `C:/Projects/ai-template.wt/review-tmp/2026-10-22c-leg13/builder/spine-changes.md`
     (items 3, 5, 6, 7, 8, 10 and 11 are row text; 1, 2, 4 and 9 were
     applied as trace cells) together with D-008's list: LLR-347's finality
     arm and TC-388; SR-244's rationale, acceptance and coverage bound;
     IF-245's and IF-246's data; LLR-356's module cell; and IF-305 split
     per PROCESS.md section 8 into the inbound arguments row and outbound
     stdout and exit-code rows. The split's new IF rows need `Contract`
     bodies in `usage_ingest.py` (the builder), TC-391 and TC-394 citing
     them, and the frame test's untied pin. Brief the derived SR's
     perspective record into the same turn (recipes section 5).
  2. The closure check, then one `combined` sitting over every new row.
  3. Restore the trunk-only views, then rebase onto trunk's tip. This
     close-out is a docs-only commit the lane does not touch.
  4. The gate in convergence stance, after the D-007 map gains the
     consolidation (no behaviour change; its existing tests).
  5. The act turn, then `check-lane` and the landing. The lane lands
     alone: it changes the session-log writer and adds the close-out
     command the cycle then runs.
  6. Once landed, the first close-out ingest measures the double-count
     scan's cost over this repository's worktrees (D-009).
- **Lane `wi-963`:** unchanged, holds for the owner (OI-115). It holds
  LLR-342 and TC-373.
- **Watermark** on trunk: WI 972, SR 243, LLR 346, IF 304, TC 385, OI 115;
  acts to seq 152.
  - Lane-held: wi-961 SR-244, LLR-347 to LLR-356, TC-386 to TC-395 and
    IF-305; wi-963 LLR-342 and TC-373.
  - wi-961's IF-305 split will take IF-306 and up.
  - Another lane's Terra floor is SR-245, LLR-357, TC-396 and IF-308.
- **Spooled logs:** WI-850's scope critique (leg 12). P8's scratch-root
  runs spooled only under the scratch root, never this repository's
  spool.
- **Strict lints:** clean on trunk and on the lane tip. **No judgement is
  active**; `docs/work/pause` is tracked and unchanged.
- **Scratch:**
  - Keep `C:/Projects/ai-template.wt/review-tmp/2026-10-22c-leg13/`: the
    spine change list, P0's probe outputs and P8's runs.
  - Keep `C:/Projects/ai-template.wt/review-tmp/2026-10-21-leg11/` for
    WI-850's critique.
  - Keep the leg-07 root until WI-963 lands.

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
D-019) and coordinator-2026-10-21 D-004 to D-006. Each row that changes
machinery lands alone, after the cycle has run through the last landing's
changed steps (WI-960 changed the coordinator's codex launch route and the
session service's record).

**Only the rows in this table are claimed**, in order and under their
`needs`. When no row in it can move without the owner, the leg closes out
with the `Overnight: stop` line.

| # | Row | Next |
|---|---|---|
| 1 | WI-961 | Claimed: the checkpoint, the gate, the act and the landing, as State above says |
| 2 | WI-963 | Held: OI-115 (the owner) |
| 3 | WI-850, WI-851, WI-856, WI-878, WI-910, WI-920 | Under their `needs`, each scope-critiqued at its claim (WI-910 as split by D-019). WI-850's critique is done (leg 12): its dispositions and confirming round come first |
| 4 | Filings P3 to P6, P8 | P3 ends in an owner act. P4 and P5 may file; P5's spec asks D-009's question (does the WI space ride the carrier?) and folds in WI-810's "sequential sittings never collide on an id". P6 starts with the W3 dry run. P8 waits on its filing calls |
| 5 | WI-966 | Scope critique and its confirming round, then the claim; it lands before item 10 step 5 |
| 6 | WI-971 | Scope critique at its claim; it touches the hook and slot walk WI-969 added, so it lands alone |

**Never claimed by a leg:** WI-684 (waits on OI-98, the owner's re-sync),
WI-795 (OI-105, then WI-820), WI-908 (the owner present), WI-964 (the
owner's Mac), WI-827 (attended only; it never lands from a lane), WI-967
(OI-115's placeholder), and every row under `docs/work/deferred/` (D-011,
D-016).

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).

## For the owner

- **Rule OI-115** (WI-963's settlement fix; recommendation (a)). It holds
  WI-963 at its gate tip.
- **Confirm or overrule:**
  - coordinator-2026-10-22 D-001: WI-961 was claimed with its 2026-10-20
    critique standing; no re-critique was run;
  - wi-961 D-001 to D-009, in particular:
    - D-001: the plan-cap sitting dismissed a torn-log finding as outside
      the threat model;
    - D-003 and D-007: the open hand-back finding was fixed by finish
      notices;
    - D-006: P8 was re-graded to its planned place after the rounds.
- **Still open from the last handoff**, every item it listed:
  - the `--wi` primary-checkout preflight call (wi-960 D-016);
  - removing the temporary `Bash(codex exec *)` allow rule;
  - wi-960 D-001 to D-016;
  - the earlier lists that handoff carried forward;
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
