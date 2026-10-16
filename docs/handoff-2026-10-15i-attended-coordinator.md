# Handoff 2026-10-15i (attended): the process-text row's gate and fix round; the re-scope walk; seven rows drafted

Overnight: stop

It replaces [handoff-2026-10-15h-attended-coordinator.md](handoff-2026-10-15h-attended-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. The next session runs **attended**,
with the owner. The `Overnight: stop` line above keeps
`scripts/coordinator/overnight_legs.py` from running it headless.

## State (trunk `refactor_again`, nothing pushed)

- **On trunk this session:** the close-out commit only (no code changed on
  trunk): coordinator-2026-10-15 D-012 to D-021, this handoff, status, the
  log fragment and two recipe lessons.
- **Owner rulings this session** (all recorded in
  `docs/decisions/coordinator-2026-10-15.toml`):
  - **The D-010 re-scope walk.** D-012: WI-925 builds no hook; it keeps the
    declared trunk key, the relink fix (reproduced first) and the four
    carried text fixes, and the hand shapes on trunk become stated residue.
    D-013: WI-922 narrows to SR-154's amendment and the unreachable cap
    branch's deletion; its landing shapes and D-008's item 3 become residue.
    D-014: D-008's fail-open row is not filed (items 2 and 4 residue; item 5,
    the hooks exiting 0 without their scripts, goes to WI-926). D-015:
    WI-926's three calls.
  - **The removal rows D-011 ordered**, each drafted after reading the
    original rationale: D-016 (WI-834's grammar forms, with env's split
    string and the chained assignment; no launch-point alternative), D-017
    (WI-852: the shared repeated-field refusal deleted for every consumer,
    and the rollup refusal, two rows), D-018 (WI-881: the late-spawn and
    interrupt guards and D-005's PID-reuse check; the try/finally and the
    `TreeNotEnded` name stay).
  - **WI-926 split** (D-019): the git hooks-on check stays WI-926; the
    Claude Code guard hooks become their own row. The owner **overruled**
    the coordinator on consent: the guard-hook install keeps asking.
    D-021: with no terminal, the lease take refuses rather than asks.
  - D-020 records the coordinator's own calls on the WI-922 and WI-925
    redrafts, for the owner to confirm or overrule.
- **Lanes:**
  - `wi-911` (WI-911, B1 text, `single`). The uncounted gate ran over
    `c0dfd1823..9f35d60ea` in convergence stance: 012 (Sol)
    CHANGES-REQUESTED, 013 (Fable) and 014 (Opus) APPROVE. Its one MAJOR
    was confirmed: the reviewer template's convergence paragraph lacked the
    severity bound the blessed LLR-311 states. Triage is wi-911 D-019, filed
    at `68dbe4136`. Terra's two wording amendments (`31422914d`; LLR-314's
    ruling set, SR-236's rationale) went to sitting 015, which ruled CLARITY
    rows=2, act seq 119 (`95c92c2d2`). The fix round is committed at
    `c074151b7`: the bound in the template, with two assertions that failed
    on the old template first, and the byte-budget rows. The lane tip is
    `c074151b7`. Next: the second uncounted gate, in convergence stance with three
    reviewers, from `c0dfd1823` to the tip; then P5 and the landing.
  - Unchanged: `wi-923`, `wi-914`, `wi-922` (claimed, no worktree),
    `wi-912`, `wi-915`, `wi-916`, WI-798 and WI-902. The `wi-921` and
    `wi-913` branches stay until the open lanes have rebased.
- **Drafted, not filed** (each folds the owner's rulings), in the scratch
  root under `i/drafts/`:
  - `wi-925/row-final.md` replaces the queued WI-925 spec;
  - `wi-922/row-final.md` is the narrowed claim copy, written in its lane;
  - `wi-926/row-final.md` replaces WI-926, and `row-2-final.md` is the
    guard-hooks row (`spec-final.md` is the revised spec of record);
  - `rm-834/row-final.md`, `rm-852/row-final.md`, `rm-852/row-2-final.md`
    and `rm-881/row-final.md` are the removal rows;
  - the notes beside each give its greps and the rationale read.

  The coordinator read the first drafts of WI-925, WI-922 and the WI-834
  removal in full. The others are still unread beyond their drafters'
  summaries.
- **Watermark** on trunk: WI 926; SR 239, LLR 337, IF 295, TC 367, OI 114;
  acts to seq 116 on trunk, 119 in the `wi-911` lane.
- **Strict lints on trunk:** `check_trajectory.py --strict` clean;
  `trace.py --strict` has LLR-292's one finding, which WI-914 fixes.
- **Smoke tier:** the owner's editor and the Codex app loaded the box, with
  the tier at below-normal priority. It read 100.9 to 111.4 s on the lane,
  and 105.5 s on trunk's tip in the same window (40.8 s at that tip's own
  commit), so every bar this session breached the 60 s budget for that
  reason, recorded in each commit message. Re-measure quiet before
  WI-911's landing.
- **Full suite:** not run, since no trunk code changed. The last run is the
  2026-10-15g handoff's, at `cc307bcc5`.
- **No judgement is active**; the lease is handed back at close-out.
  `docs/work/pause` is tracked, unchanged this session.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-15d-coord/`;
  this session is under `i/` (the drafts, the planner brief, sitting 015's
  brief and facts, the bars), and WI-911's gate is under `wi-911/gate/`,
  with the coverage plans `wi-911/cov-g-*.md`.

## How to run reviews now

As the 2026-10-15h handoff says. Once the fix round lands in the lane, the
template carries the convergence severity bound itself, but the interim
addenda stay appended until WI-911 lands on trunk.

## The queue

| # | Row | Next |
|---|---|---|
| 1 | WI-911 | The second uncounted gate (convergence, three reviewers, `c0dfd1823` to the tip). On approval, P5: the rebase (trunk moved by docs only), the RESYNC entry re-anchored at the landing's parent, the close in its own commit, a quiet bar and the full suite; then the landing through WI-921's armed hold |
| 2 | The drafts | Read each draft's Done-when, Trust and Scope answers, then file on trunk with `--bump-ids`: WI-925's and WI-926's specs replaced; the guard-hooks row and the four removal rows new. Then each one's scope critique (Sol from `trunk-tmp`, with `critique-addendum.md`) and dispositions. WI-922's narrowed copy is critiqued fresh; it is claimed, so render it from a detached checkout carrying the copy uncommitted, or after its lane is cut. Its `planmode` mark changes on trunk only if that critique confirms S4 (D-020) |
| 3 | WI-914 | B2: rebase after WI-911 lands; the checkpoint (the LLR-292 amendment sitting and its act); the uncounted gate; the landing |
| 4 | WI-923 | After WI-911 and WI-914 land: the rebase, the checkpoint (`amendment:TC-267;amendment:TC-329;amendment:LLR-270` under SR-227), the gate, the landing |
| 5 onward | as before | WI-912, WI-917, WI-916, WI-915, WI-902 (B4), WI-798, then P1 to P8 with WI-918, then leg 03's rows; the re-scoped hook rows (WI-922, WI-925, WI-926 and the guard-hooks row) and the four removal rows placed with the owner. WI-917 and WI-918 each owe their confirming scope-critique round before a claim |

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Confirm or overrule:**
  - `coordinator-2026-10-15.toml` D-020 (the coordinator's calls on the
    WI-922 and WI-925 redrafts: one home for each residue list, WI-922's
    `none` mark after its critique, `staged_closes` deleted, the relink's
    reach stated as residue);
  - `wi-911.toml` D-019 (the gate's triage: the MAJOR fixed, three MINORs
    adopted, K2's LLR extension and the TC-method question deferred to
    item 5, the plan.md scope MINOR not adopted);
  - still unseen from before: as the 2026-10-15h handoff lists (wi-911
    D-015 and D-018, coordinator-2026-10-15 D-006, and earlier).
- **The three-reviewer trial, the gate:** round-costing Sol 1, Fable 0,
  Opus 0. MINORs: Sol 1, Fable 1, Opus 6, two of them shared. Sol's one
  round-costing finding was real and convergence-class.
- **The convergence tag:** with the severity bound in place, every new
  BLOCKER or MAJOR in a convergence round is convergence-class by
  definition, so `convergence-class: no` cannot occur for a new finding.
  LLR-311 states both rules; whether the tag stays is yours to say.
- **Noted, not filed:** this checkout's `core.hooksPath` is an absolute
  path, so dev-setup's literal `.githooks` comparison reports the hook floor
  as missing here (found by WI-926's drafter). Also carried from the
  2026-10-15h handoff, unchanged: the `wi-880` worktree's uncommitted hook
  edit, the old `coordinator-tools` folder, and OI-98 and OI-105 waiting on
  their conditions.

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
   (medium), Claude Fable (medium) and Claude Opus (high) review in parallel,
   a trial (the handoff's "How to run reviews now"); the independent adjudicator
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
