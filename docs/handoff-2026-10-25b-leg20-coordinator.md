# Handoff 2026-10-25b (headless leg 20): WI-976 through its checkpoint and gate; its act turn waits on a composer fix

It replaces [handoff-2026-10-25a-leg19-coordinator.md](handoff-2026-10-25a-leg19-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 20 (loop session
`20261025T055732Z-64b2b6`, coordinator session
`9df582d7-f236-4dc6-b0ce-41448b32825e`) claimed WI-976 (P3) and took it
through its plan, intent set, tests, build, three counted rounds, two dispute
sittings, the checkpoint, a whole-set re-sit and the gate. Its act turn
refused before writing, so the lane holds at a safe committed point. It
carries no `Overnight: stop` line: the next step moves without the owner.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** the unpause for WI-976 (`c4540306a`), its claim (`58d737f5d`)
  and the byte-identical restore (`aa36a5b6e`); then this close-out. Trunk
  has not moved otherwise, so the lane's base is trunk's tip before this
  close-out.
- **Lane `wi-976`** (worktree `C:/Projects/ai-template.wt/wi-976`, tip
  `3e3594937`, base `aa36a5b6e`; headless-marked, so it lands headless):
  - plan passed at critique 2 (`docs/plans/WI-976/`); ruling fragment
    `docs/log.d/2026-10-25-wi976-sn036-ruling.md`; intent set, tests, build
    and two fix rounds committed through `integrate.py attest`;
  - rounds: 1 (`001`/`002`), 2 (`005`/`006`), 3, the cap's convergence round
    (`007`/`008`); dispute sittings `004` (RB1-F1 **SUCCESSOR**: both
    composing routes widen by the authoring work item's tags; file it on
    trunk at the landing from the sitting's binding) and `010` (RB3-F1
    DISMISS);
  - checkpoint sitting `011` (TC-178 returned, the rest blessed) and the
    whole-set re-sit `012-ADJUDICATE-066e66c.md` (every row blessed or
    approved, all eleven SN-036 hats named; SN-036 MEANING on its held rung,
    recommended to the owner). `012` is the act's verdict and TC-211's
    sample, its brief committed beside it; `011` is chain evidence;
  - the gate over `452eec010` (`013`/`014`): both APPROVE, one MINOR
    (SR-165's rationale edit outside the spec's change set; wi-976 D-015,
    a follow-up, not reverted);
  - **the act turn refused before writing** (wi-976 D-016): the composer's
    amendment scope reads only rows present live, so the retired LLR-297
    and TC-312 were dropped from sittings 011 and 012, no verdict names
    their removal, and the snapshot will not copy the two registries
    holding them. Nothing was written.
- **Next for WI-976** (D-016's recommended route): a fix inside the lane's
  own surface, the sitting-brief composer: brief an `Adjudicates` row that
  the recorded copy holds approved and the live registry lacks as a
  removal for the sitting to rule, and refuse by name a scope token naming
  a row in neither; a regression test; then the one more checkpoint a
  post-gate fix owes (a whole-set re-sit, which moves TC-211's sample under
  the plan's P9 step 6, so fix its paths and TC-211's inputs first; then an
  uncounted convergence gate); then the act turn, taking every act except
  SN-036's; then stop for the owner (below). P11 (TC-211's re-judge) waits
  for SN-036's act.
- **Lane `wi-963`:** unchanged, holds for the owner (OI-115). It holds
  LLR-342 and TC-373; recount `acceptance_record.py`'s size at its rebase.
- **Watermark** on trunk: WI 976, SR 246, LLR 359, IF 308, TC 398, OI 115;
  acts to seq 159.
  - Lane-held: wi-963 LLR-342 and TC-373; wi-976 LLR-360 and TC-399.
  - A new lane's Terra floor is SR-247, LLR-361, TC-400 and IF-309.
- **Smoke ceiling:** `max-tests` is 3410 (trunk's tier counts 3289; the
  lane's 3282).
- **Full suite:** at the lane tip `3e3594937`, from a detached worktree: 1 failed, 7348 passed, 33 skipped in 1:07:04. The one red, `test_this_repo_s_committed_stage_is_current`, is the trunk-only `docs/stage` a lane's moved rows leave stale off a claimed branch: re-derived there with `derive_stage.py`, it passed (the recipes' wi-921 D-020 case), so it is not a defect. The run outlasted the 60-minute cap and finished in the background.
- **Usage:** this close-out's ingest recorded this session and its
  sub-agents, and leg 19's tail. The next close-out passes
  `--session 9df582d7-f236-4dc6-b0ce-41448b32825e`.
- **Strict lints:** clean on trunk and on the lane tip. **No judgement is
  active**; `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-25b-leg20/`
  holds the lane's briefs, the arms map (`arms/arms-map.md`), the coverage
  plans and probes; keep it until WI-976 lands. Its `full-wt` detached
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
(the rubric's S7). Each row that changes machinery lands alone, after the
cycle has run through the last landing's changed steps.

**Only the rows in this table are claimed**, in order and under their
`needs`. When no row in it can move without the owner, the leg closes out
with the `Overnight: stop` line.

| # | Row | Next |
|---|---|---|
| 1 | WI-963 | Held: OI-115 (the owner); recount its module size at the rebase |
| 2 | WI-910 | Held: its Done-when checks CI's macOS and Linux state on the landing tip, which needs a push (coordinator-2026-10-25 D-001) |
| 3 | WI-976 | Continue in lane (claimed): the composer fix for retired rows (wi-976 D-016), the post-gate checkpoint and gate, the act turn without SN-036's act; then stop at SN-036's owner-held act, recorded for the owner; it lands alone, after the act, with RB1-F1's successor filed on trunk at the landing |
| 4 | Filings P4 to P6, P8 | P4 and P5 may file (`docs/handoff-2026-10-11-attended-coordinator.md` names them); P5's spec asks D-009's question (does the WI space ride the carrier?) and folds in WI-810's "sequential sittings never collide on an id". P6 starts with the W3 dry run. P8 waits on its filing calls |
| 5 | WI-966 | Scope critique and its confirming round, then the claim; it lands before item 10 step 5 |
| 6 | WI-971 | Scope critique at its claim; it touches the hook and slot walk WI-969 added, so it lands alone |

**Never claimed by a leg:** WI-684 (waits on OI-98, the owner's re-sync),
WI-795 (OI-105, then WI-820), WI-908 (the owner present), WI-964 (the
owner's Mac), WI-827 (attended only; it never lands from a lane), WI-967
(OI-115's placeholder), and every row under `docs/work/deferred/` (D-011,
D-016).

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).

## For the owner

- **SN-036's re-attestation act is yours** (WI-976's Done-when, "The
  owner-held step"), once the next leg has taken the lane's other acts.
  Attended in the lane, after a re-claim (the lane is headless-marked;
  SKILL section 7, "The re-claim"), in text-then-act order:
  `intake.py snapshot --approves stakeholder-needs=docs/log.d/2026-10-25-wi976-sn036-ruling.md --reattests SN-036`,
  adding `--verdict` with the act's verdict where the route asks for it
  (today `docs/reviews/wi-976/012-ADJUDICATE-066e66c.md`; the next leg's
  re-sit may replace it, and its handoff will name it). Sitting 012
  recommends it: the text is your 2026-09-06 ruling, carried verbatim from
  `contract_split`.
- **Rule OI-115** (WI-963's settlement fix; recommendation (a)). It holds
  WI-963 at its gate tip.
- **Push `refactor_again`** so WI-910's landing tip can carry CI's state, or
  rule that the WSL POSIX evidence route (wi-931 D-002) stands in for CI on
  that Done-when item (coordinator-2026-10-25 D-001).
- **Hold the FileBackup re-sync (OI-98) until WI-976 lands** (D-003).
- **Confirm or overrule:**
  - wi-976 D-001 to D-016, notably D-005 and D-006 (the route-dependent
    hat set sent to a dispute and ruled SUCCESSOR), D-007 (round 2's
    REVIEW-A F2 re-graded to the checkpoint), D-013 (the whole-set re-sit
    moving TC-211's sample), D-015 (the gate's SR-165 MINOR kept, not
    reverted) and D-016 (the act blocked; the composer fix route);
  - coordinator-2026-10-25 D-001 to D-005, notably D-003 (the six
    lane-authored sidecars stay as inert records; WI-684 not edited);
  - wi-878 D-001 to D-008 and WI-920's re-judge departures.
- **Still open from the last handoff**, every item it listed:
  - coordinator-2026-10-24 D-001 to D-005 and wi-856 D-001 to D-006;
  - coordinator-2026-10-23 D-001 to D-005 (D-002 and D-004 high risk) and
    wi-851 D-001 to D-014;
  - coordinator-2026-10-22 D-002 to D-004, wi-850 D-001 to D-012 (D-002
    high risk), wi-961 D-010 to D-017 and the earlier items those handoffs
    carried;
  - the `--wi` primary-checkout preflight call (wi-960 D-016);
  - removing the temporary `Bash(codex exec *)` allow rule;
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
