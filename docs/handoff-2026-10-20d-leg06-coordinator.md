# Handoff 2026-10-20d (headless leg 06): WI-957 built and held for the owner; P2 and P7 filed; WI-962 claimed

It replaces [handoff-2026-10-20c-leg05-coordinator.md](handoff-2026-10-20c-leg05-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. This was the sixth headless leg
under WI-946's launcher (loop session `20261019T185432Z-8e4f05`). It built
WI-957 to its first review, where the review bar's budget step holds it for
the owner. It filed queue rows P2 (WI-960, WI-961) and P7 (WI-962), and
took WI-962 through its plan, intent and tests. It carries no
`Overnight: stop` line: WI-962 moves without the owner.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** `7f336b8f5`, `db4f7bb42` and `64b8d686c` are the scoped
  unpause and claim for WI-957. `9cfda90f6` files WI-960 and WI-961;
  `2881f247c` and `17ebbb3d1` hold their scope critiques' dispositions and
  confirming rounds (both cleared for a claim). `e427ecfd1` files WI-962;
  `998cea7cb` and `eea1520b4` hold its dispositions, its confirming round
  (APPROVE 0) and coordinator-2026-10-20 D-007. `5b5bc19e4`, `7f817ca8c`
  and `e79075c46` are the scoped unpause and claim for WI-962. The
  close-out commit follows. Nothing landed this leg, and `archive/lanes`
  is unchanged.
- **Lane `wi-957`** (worktree `C:/Projects/ai-template.wt/wi-957`, base
  `64b8d686c`, tip `804c8011c`): plan `7f3833550`, critique-1 APPROVE 0
  `d0411d424`, pass record `85a68024a`; Terra's intent set `9015acd72`
  (SR-241, LLR-341, TC-371, TC-372, all Drafted; Terra session
  `01a15b92-e996-71b1-98c6-f8a280edc55e`); the tests first, twelve strict
  xfail cases `6fe5e26a9`; the code, the skill text and one RESYNC entry
  (anchored `[since 64b8d686c]`) `804c8011c`. No review has run. The
  review render on the lane now refuses its own tip, as designed: it
  carries no `review` attestation. `integrate.py attest` refused the code
  commit because the smoke tier ran 96.9 s against its 60 s budget, every
  test green (wi-957 D-003). On this box the tier reads 70 to 112 s
  whatever else runs, so the lane holds for the owner (wi-957 D-004; "For
  the owner"). After the ruling: an attest with nothing staged writes the
  empty attestation commit; then counted round 1. If WI-962 lands first,
  rebase WI-957 onto it and re-anchor the RESYNC entry.
- **Lane `wi-962`** (worktree `C:/Projects/ai-template.wt/wi-962`, base
  `e79075c46`, tip `1bd47e778`): plan `96c6e7040`, critique-1
  (CHANGES-REQUESTED, one MINOR, read as an approve) `3581b5726`, pass
  record `a218281e1`; Terra's intent set `899b9b97f` (SR-031, LLR-021,
  TC-021, TC-031 and IF-037 amended, IF-298 new; Terra session
  `01a15c29-40f7-7da2-9b33-22e70f939abf`); the tests first, 72 strict xfail
  cases `1bd47e778`. Claimed by this headless leg, so it lands headless.
  **Next:** the code stage, the plan's P2 to P4, P5's non-registry parts
  (`docs/runtime-flows.md` Flow 3, the prose claims, the contract bodies)
  and P6's RESYNC entry, with the marks removed. Points for that builder's
  brief, from the test builder (wi-962 D-002): the unreadable refusal must
  say `cannot be read or parsed`, and the failed-read refusal must name
  `check_privacy.py` and `--hook-policy`; `test_meta_repo_hook` asserts
  that `KIT_SCRIPTS_DIR` appears in `hooks/pre-commit`, so either a comment
  there survives or the test's subject moves to `kit-python.sh`. Three
  tests tag a TC whose evidence does not list them (the review posture
  test and the no-text-read pin under TC-031, the bootstrap test under
  TC-021): the checkpoint's reconcile. Then counted round 1, both
  reviewers. Its reviews render through trunk's `review_brief.py`, which
  has no attestation gate yet.
- **Watermark** on trunk: WI 962; SR 240, LLR 340, IF 297, TC 370, OI
  114; acts to seq 143. Lane-held ids: wi-957 holds SR-241, LLR-341,
  TC-371 and TC-372; wi-962 holds IF-298. A later lane's Terra takes these
  as its floor.
- **Strict lints:** clean on trunk and both lanes.
- **Tests this leg:** each lane's named modules re-run by the coordinator
  (wi-957: 280 passed; wi-962's tests commit: 224 passed, 72 xfailed). No
  trunk code changed this leg, so no full suite ran. Every bar ran over
  the 60 s budget (67 to 167 s), each code or test commit beside its
  parent's reading in the same window.
- **No judgement is active**; the lease is handed back at close-out.
  `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-20d-leg06/`
  holds this leg's drafts, briefs, verdicts and bar logs, and one
  detached worktree (`parent-wt`; remove with `git worktree remove`).
  **Keep `p8-draft/`** until P8 is filed: it holds the three drafted P8
  specs and their NOTES. The rest may be deleted, as may the leg 05 root.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say: two full-lane
reviewers per round, Codex Sol at medium (REVIEW-A) and Claude Opus at high
(REVIEW-B, launched with the Agent tool's `effort: "high"`), each given
only its rendered brief.

## The queue

The owner's order (coordinator-2026-10-16 D-004, D-006; coordinator-2026-10-17
D-002, D-008), turned toward headless runs (coordinator-2026-10-18 D-004,
D-006). Each row that changes machinery lands alone, after the cycle has
run through the last landing's changed steps.

| # | Row | Next |
|---|---|---|
| 1 | WI-962 | In its lane: the code stage, then the rounds, the checkpoint, the gate and the landing |
| 2 | WI-957 | Held for the owner's ruling on wi-957 D-004; then the empty attestation commit and counted round 1 |
| 3 | WI-958 | After WI-957 lands (hard edge) |
| 4 | WI-960, then WI-961 | Cleared for a claim; built after WI-957 lands (WI-960's soft edge: the same review steps) |
| 5 | WI-953 | WI-902's disposition, after the owner routes the plan cap's FIX |
| 6 onward | As before | P3 to P6 and P8 (P8 waits on its filing calls, below), then leg 03's rows; WI-940 after the batch, unless the owner moves it (wi-957 D-004 (a)) |

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).

## For the owner

- **Rule wi-957 D-004 (high risk; it holds WI-957, and through it WI-958,
  WI-960 and WI-961).** Two rulings meet at WI-957's first review:
  coordinator-2026-10-17 D-005 (a breach close to its parent's reading is
  load and holds nothing, a paired procedure D-007 keeps until WI-940's
  CPU-time budget lands) and WI-956's `attest`, which runs the bar alone and
  refuses any breach. On this box the tier reads over 60 s even idle
  (101.8 s with the box at about 5% CPU), so after WI-957 lands no review
  could render. Options: **(a)** land WI-940 before WI-957 (the
  coordinator's recommendation: your chosen fix, filed, ready and
  single-plan, reviewed before WI-957's gate exists); **(b)** declare
  `[bars] review` without its budget step until WI-940 lands, so the
  review bar judges results and the landing keeps its paired seconds
  reading; **(c)** a re-tier lane that brings the tier under 60 s here;
  **(d)** another route.
- **P8's filing calls** (drafts in the scratch root's `p8-draft/`, split
  three ways: the test-file TC tag and its one reader; the derived review
  test set and its refusals; the strict-mark commit check): the tag
  token (the drafter proposes the existing `Implements:` line); two forced
  downstream migrations (the tags, and a new required `[bars] red_mark`
  key); and refusing a code-touching row that names no SR (8 of 36 open
  rows today).
- **Push** `refactor_again` and `archive/lanes`.
- **Route WI-902's plan-cap FIX** (wi-902 D-011); WI-953 waits on it.
- **Confirm or overrule:** coordinator-2026-10-20 D-004 to D-007 (high
  risk: **D-005**, WI-960's three filing calls, the spool for a call
  outside a lane among them; **D-006**, WI-962's refusal of an unparseable
  policy file at the hooks, a forced change for adopters); wi-957 D-001 to
  D-004; wi-962 D-001 and D-002. Still open from the last handoff:
  coordinator-2026-10-20 D-001 to D-003 (D-002 high risk), wi-955 D-001 to
  D-006, wi-956 D-001 to D-010, and the lists before them.
- **The named-tests `--basetemp`**, **SR-227's wording** and the items
  still open from earlier handoffs: unchanged from the last handoff.

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
