# Handoff 2026-10-25c (headless leg 21): WI-976 acted to its owner-held step; P4 and P5 filed; item 12's W3 dry run

It replaces [handoff-2026-10-25b-leg20-coordinator.md](handoff-2026-10-25b-leg20-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 21 (loop session
`20261025T055732Z-64b2b6`, coordinator session
`52bd6156-6e74-4d3a-a1c3-ccaec8ab2e37`) built WI-976's composer fix, re-sat
its whole set, passed the post-gate gate, rebased and took every act but
SN-036's; filed P4 and P5; and ran item 12's W3 dry run. It carries no
`Overnight: stop` line: the next rows move without the owner.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** WI-977's filing (`aed0364fd`), WI-978's and OI-116's
  (`e39fff2dc`), then this close-out.
- **Lane `wi-976`** (worktree `C:/Projects/ai-template.wt/wi-976`, tip
  `94705e63f`, rebased onto `e4a3a4ccd`; headless-marked, so it lands
  headless after its re-claim reads as the merge slot reads it):
  - the composer fix: the amendment arm moved into `amendment_brief.py`
    (`b6a72d6ca`, structural alone), then the retired-row fix (`7d9f4143d`);
    Terra's reconcile of LLR-167, TC-161 and LLR-273 (wi-976 D-017, D-018);
  - whole-set re-sits `015` (LLR-273 returned for an added module name,
    answered in the lane, D-019) and `016-ADJUDICATE-9d6ad4c.md` (every
    released row blessed, both removals included; SN-036 MEANING on its
    held rung, recommended to the owner). `016` is the act's verdict and
    TC-211's sample, its brief committed beside it; `011`, `012` and `015`
    are chain evidence;
  - the gate over `14f786d1a` (`017`/`018`): Sol APPROVE findings=0; Opus 4
    MINORs (D-021): one goes in at the landing (below), two are status.md
    follow-ups, one is D-015's again;
  - act seqs **160** (re-attest LLR-167, TC-161, LLR-273, SR-161, LLR-183,
    TC-178, SR-165, TC-211; retire LLR-297 and TC-312) and **161** (LLR-360,
    TC-399 approved), lane-held; the bar green after them (D-022).
- **Next for WI-976:** the owner's SN-036 act (below); then P11, TC-211's
  re-judge by a fresh session over `016`'s brief and verdict under the
  amended procedure, recorded through the observation writer and in the
  procedure's result section; then the landing, alone: rebase onto trunk
  (re-anchor the RESYNC entry at the landing's parent, and add
  `scripts/kitlib/bootstrap_manifest.py` to the entry's kit-owned overwrite
  list, D-021), `check-lane` exit 0, the act seqs above trunk's, file
  RB1-F1's successor on trunk from sitting `004`'s binding.
- **Lane `wi-963`:** unchanged, holds for the owner (OI-115).
- **Watermark** on trunk: WI 978, SR 246, LLR 359, IF 308, TC 398, OI 116;
  acts to seq 159 (160 and 161 lane-held in wi-976).
  - Lane-held ids: wi-963 LLR-342 and TC-373; wi-976 LLR-360 and TC-399.
  - A new lane's Terra floor is SR-247, LLR-361, TC-400 and IF-309.
- **Smoke ceiling:** `max-tests` 3410 (trunk's tier 3289). The bar's CPU
  reading in the lane was 556.4 s against `cpu-seconds = 540` (a WARN only
  `run.cmd audit` judges).
- **Full suite:** at the lane tip `94705e63f`, from a detached worktree, in
  two halves: 4166 passed, 25 skipped (19:41); 3188 passed, 8 skipped, 1
  failed (12:08). The red, `test_this_repo_s_committed_stage_is_current`,
  is the detached worktree's trunk-only stage; re-derived, it passed.
- **Usage:** this close-out's ingest recorded this session, its sub-agents
  and leg 20's tail. The next close-out passes
  `--session 52bd6156-6e74-4d3a-a1c3-ccaec8ab2e37`.
- **Strict lints:** clean on trunk and on the lane tip. No judgement is
  active; `docs/work/pause` is tracked and unchanged.
- **Scratch:** keep `C:/Projects/ai-template.wt/review-tmp/2026-10-25c-leg21/`
  and leg 20's root until WI-976 lands; this leg's `full-wt` detached
  worktree may go (`git worktree remove --force`). Keep the leg-07 root
  until WI-963 lands.

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
(the rubric's S7); row 7 added by coordinator-2026-10-25 D-009. Each row that
changes machinery lands alone, after the cycle has run through the last
landing's changed steps.

**Only the rows in this table are claimed**, in order and under their
`needs`. When no row in it can move without the owner, the leg closes out
with the `Overnight: stop` line.

| # | Row | Next |
|---|---|---|
| 1 | WI-963 | Held: OI-115 (the owner); recount its module size at the rebase |
| 2 | WI-910 | Held: its Done-when checks CI's macOS and Linux state on the landing tip, which needs a push (coordinator-2026-10-25 D-001) |
| 3 | WI-976 | Held: SN-036's act (the owner, attended, after a re-claim); then P11 and the landing alone, as "Next for WI-976" says |
| 4 | Filings P6, P8 | P6: file its text row from the W3 dry-run record ([plans/2026-10-11-review-churn/w3-dry-run/](plans/2026-10-11-review-churn/w3-dry-run/README.md)): the rubric with the five clarifications it names, the `architecture-decomposition` skill, the `spine-questions.md` pointer, the plan-decomposition question, the pointer from B1's delta anchor and the line in G's single-plan prompt naming the skill. P8 waits on its filing calls. (P4 is filed as WI-977, P5 as WI-978, held by OI-116; its scope critique follows the ruling) |
| 5 | WI-966 | Scope critique and its confirming round, then the claim; it lands before item 10 step 5 |
| 6 | WI-971 | Scope critique at its claim; it touches the hook and slot walk WI-969 added, so it lands alone |
| 7 | WI-977 | Claimable (its critique passed, D-007): claim under one scoped unpause with rows 5 and 6; it changes the dispatcher, the claim and the close, so it lands alone, after WI-976, before the managed loop is unpaused |

**Never claimed by a leg:** WI-684 (waits on OI-98, the owner's re-sync),
WI-795 (OI-105, then WI-820), WI-908 (the owner present), WI-964 (the
owner's Mac), WI-827 (attended only; it never lands from a lane), WI-967
(OI-115's placeholder), WI-978 until OI-116 is ruled, and every row under
`docs/work/deferred/` (D-011, D-016).

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).

## For the owner

- **SN-036's re-attestation act is yours** (WI-976's Done-when, "The
  owner-held step"; wi-976 D-022). Attended in the lane, after a re-claim
  (the lane is headless-marked; SKILL section 7, "The re-claim"), in
  text-then-act order:
  `intake.py snapshot --approves stakeholder-needs=docs/log.d/2026-10-25-wi976-sn036-ruling.md --reattests SN-036`,
  adding `--verdict docs/reviews/wi-976/016-ADJUDICATE-9d6ad4c.md` where the
  route asks for it. Sitting 016 recommends it: the text is your
  2026-09-06 ruling, carried verbatim from `contract_split`.
- **Rule OI-116** (WI-978: does the WI space ride the watermark carrier,
  re-opening revision 33? recommendation (a), spine only; (c) builds for
  (a) now and keeps the question open).
- **Rule OI-115** (WI-963's settlement fix; recommendation (a)).
- **Push `refactor_again`** so WI-910's landing tip can carry CI's state, or
  rule that the WSL POSIX evidence route (wi-931 D-002) stands in for CI on
  that Done-when item (coordinator-2026-10-25 D-001).
- **Hold the FileBackup re-sync (OI-98) until WI-976 lands** (D-003).
- **Confirm or overrule:**
  - wi-976 D-017 to D-022, notably D-017 (the composer split into a new
    module rather than a ratchet entry), D-019 (sitting 015's one-cell
    return applied by the coordinator), D-021 (the gate's four MINORs
    disposed without a fix after the gate);
  - coordinator-2026-10-25 D-006 to D-009, notably D-006 (WI-977's eleven
    drafter calls) and D-008 (WI-978's drafter calls), and D-009 (WI-977
    added to the queue table);
  - wi-976 D-001 to D-016, coordinator-2026-10-25 D-001 to D-005, wi-878
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
