# Handoff 2026-10-11 (attended): the review-churn program is ruled; start its first batch with the owner

Overnight: stop

It replaces [handoff-2026-10-11-leg03-coordinator.md](handoff-2026-10-11-leg03-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes, and this handoff holds state only. The next session runs **attended**,
in an interactive session with the owner. The `Overnight: stop` line above
keeps `coordinator-tools/overnight_legs.py` from running it headless.

This session claimed and built nothing. It stopped the overnight loop after
leg 03 (its last line in `C:/Projects/ai-template.wt/overnight-logs/loop.log`
records why), investigated why legs take 4–6+ hours, and wrote a plan the
owner then ruled item by item:
[plans/2026-10-11-review-churn/](plans/2026-10-11-review-churn/README.md).
Its **"Owner rulings, 2026-10-11"** section governs, and the other sections
are its reasoning. The pointer rules it sets for the spine are drawn in
[plans/2026-10-11-review-churn/pointer-rules.md](plans/2026-10-11-review-churn/pointer-rules.md).
The plan's revision 2 was independently reviewed by Sonnet and Sol, and
revisions 3–5 (the rulings, the pointer rules and this handoff) by GPT-6
Astra, and revision 6 by Claude Fable 5.1. All four reviews are recorded
under `reviews/`; revisions 6 and 7 answer the last two. Revision 11 was
reviewed by GPT-6 Astra at low effort; revision 12 answers it. Item 11 is
open: hold any pointer or schema migration that depends on it until the
owner rules.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk tip:** the newest plan-revision commit (`git log -1`), which also
  edits this handoff. The pre-commit checks passed on every commit this
  session. No full suite ran: no code changed. Leg 03's full suite
  (5811 passed, 22 skipped, 0 failed at `67bf3bf2`) stands.
- **No lease is held, no judgement is active.** `docs/work/pause` is tracked
  and unchanged since leg 03.
- **Lane 1, WI-798:** unchanged from leg 03 and still in flight. Code is
  settled, and sitting 004 returned rows for Terra's rework (Terra session
  `01a12c25-e6ba-7da0-b1ad-72b38ee4741e`). Leg 03's handoff, "Lane 1", has the
  exact next steps; they still apply. Run its remaining reviews in the new
  review shape (below).
- **Lane 2, WI-902:** committed on its lane (tip `d3d30121`). The owner ruled
  to **reshape it before resuming**: record-at-close. The close validates the
  adoption once and records it in the closing commit, a check against the
  parent validates that record, and the sweep trusts it and never replays git
  history. Its Trust ruling (coordinator-2026-10-11 D-005) is re-sat on the
  new shape. This supersedes leg 03's resume instruction (one more build
  round on the history-reading sweep).
- **Watermark** on trunk is unchanged from leg 03: SR 239, LLR 326, IF 293,
  TC 351, WI 908, OI 114; acts to seq 112. The lanes hold more, as leg 03
  lists.

## How to run reviews now (owner ruling, ahead of the code)

The `coordinator-cycle` skill still describes narrow rounds and one Sol
reviewer. Until batch item 1 below lands, follow the ruling by hand:

- **No narrow rounds.** Every review is a full-lane review. Each round runs
  two fresh reviewers **in parallel**, each from its **own render** of
  `review_brief.py review --scope full` with its **own `--scratch`
  directory** (for example `<dated root>/A` and `<dated root>/B`). One shared
  render would give both the same verdict path and pytest `--basetemp`:
  - **A: Codex Sol** (`sol_review.sh`, medium), filed as REVIEW-A;
  - **B: Claude Sonnet**, filed with `review_brief.py file --phase REVIEW-B`.
    Spawn it with `model: sonnet` and give it **only** the path to its
    rendered REVIEW-B brief: no build prompt, no coordinator notes, no builder
    material. It writes nothing except its own `--scratch` directory. This is
    not the forbidden self-review: the builder is a different sub-agent, and
    the reviewer reads only the brief. Sonnet is a **stand-in** for the Gemini
    reviewer and shares the builder's and the adjudicator's model family,
    which is why each lane's decisions record notes the substitution.
- **Add item 1's classification clause to both briefs:** an input outside
  the spec's declared set that the change fails closed on is a
  coverage-extension note; one it fails open on stays a finding. The
  reviewer decides which.
- **At most 3 full rounds before the checkpoint.** Rounds run until one has
  no BLOCKER or MAJOR code finding; the checkpoint follows it. The gate over
  the checkpoint tip, and a round over a rebase that changed code or rows,
  always run, in convergence stance, and are not counted, so the tip that
  lands is always reviewed. Lanes already in flight (WI-798, WI-902) start at
  zero at their next review; record that as a decision.
- **At the cap**, open findings go to one dispute sitting, which rules each
  FIX-as-successor-row, DISMISS, or ESCALATE. A **convergence-class** finding
  (fail-open, data loss, Done-when gap) is never deferred: the sitting orders
  one more fix round or ESCALATEs. Successor rows are filed **on trunk at the
  landing**, from the sitting's binding; a work branch never mints a WI id.
- **Only BLOCKER and MAJOR cost a round.** MINORs go to the spine change list
  or a successor row.
- **The last allowed round and the post-checkpoint gate run in convergence
  mode:** a new finding blocks only if it is fail-open, data loss or a
  Done-when gap. They **never see earlier verdicts** (owner ruling: prior
  conclusions anchor a reviewer). A fix is confirmed by its regression test
  instead: every accepted finding carries a test that fails on the pre-fix
  code. Before the round, check that each accepted finding maps to such a
  test. The reviewer template verifies pre-fix failure only where the diff
  adds a test, so say so in the brief by hand. A wording or inspection
  defect has no test; how its fix is confirmed is an open owner call (plan
  revision 12).
- **Severity is tied to reachability:** BLOCKER or MAJOR needs a scenario
  reachable in normal use, or a fail-open, data-loss or security path.
- **Reviewers get the WI definition** (spec, Done-when, Trust, touched rows),
  **never the builder's coverage plan.**
- **Before a claim**, every scope-critique recommendation gets a disposition:
  adopted, quoting the spec text that carries it, or rejected, with a reason.
  A fresh critique round checks the adopted ones before the claim. Apply S3
  (closed coverage, construction-first) and S4 (planning need) by hand.
- **After each build round**, run `trace.py --strict` and
  `check_trajectory.py --strict` with the commit bar. `trace.py --strict`
  exits 1 on trunk today ("LLR-292 Detail uses 'minimal'"); batch item 2 fixes
  it, and until then compare against that one known finding.

## The queue

The program's first batch comes first. B1–B3 are new rows, and G is minted
on trunk as a split of WI-805: file each on trunk with its scope critique
(under the rules above) before claiming it. B4 is a spec amendment of an
already-claimed row. Rows may be claimed before G lands, but a row S4 marks
`single` builds only after G lands, and its plan is produced after its claim,
in the lane, before its first build. Then WI-798
continues, then leg 03's queue. **Re-order leg 03's queue against the plan once
batch 1 is filed:** several rows now overlap the rulings. WI-817 retires the
SN-028 window, which item 10 folds into one migration. WI-805's plan gate is
pulled forward. WI-800's usage part is pulled forward for item 8. WI-813 keeps
its arbiter.

| # | Row | What |
|---|---|---|
| B1 | *to file* | Process edits that govern every later lane: the review shape and pre-claim dispositions in the `coordinator-cycle` skill; S3, S4 and the B3 bad example in `docs/rubrics/scope-critique.md`; the record-at-event rule in `PROCESS.md` §3; in the shipped reviewer template (RESYNC entry), severity-by-reachability, the convergence round and item 1's fail-open/fail-closed classification clause |
| G | *split from WI-805* | WI-805's per-item plan gate, pulled forward (owner ruling). Once S4 exists, a row it marks `single` waits for this gate, so it comes before B2–B4. Its own row is built without the gate (it cannot plan itself); record that. It launches its planner and critic the way the scope critique is launched by hand today (`review_brief.py critique`, `sol_review.sh`); WI-804 later routes the same calls, so no second launch path is added |
| B2 | *to file* | Item 6: fix LLR-292; add the strict lints to the commit bar, the closure check and the landing check (not the pre-commit hook); build the RESYNC-presence check |
| B3 | *to file* | Item 10 step 1: one shared `stack.ini` loader in place of its 13 separate parsers (13 `ConfigParser` constructions in 12 files; a pure refactor) |
| B4 | WI-902 | The record-at-close spec amendment with its scope critique; D-005 re-sat. The lane's rows approved through acts 113–117 for the history-reading sweep are re-judged or retired under the new shape before the rebuild |
| 0 | WI-798 | In flight: Terra's rework of sitting 004's returns, re-sit, full-lane gate in the new shape, land |
| 1… | leg 03's queue | Its table, rows 1–25, in its order until re-ordered. WI-897 stays last, just before the owner's FileBackup resync test, and the item 10 config consolidation must land before that test |

Held by the owner, skipped: WI-684 (OI-98), WI-795 (OI-105), WI-871
(OI-112), WI-893 (OI-113) and WI-908 (OI-114). WI-827 is the owner's
signature (SN-029).

## For the owner

- **Push** `refactor_again` and `archive/lanes`.
- **Rule OI-113** (holds WI-893) and **OI-114** (holds WI-908; leg 03
  recommends (b), defer). OI-98, OI-105 and OI-112 still wait.
- **Decisions to confirm or overrule:** leg 03's list stands. That is
  `docs/decisions/coordinator-2026-10-11.toml` D-009 and D-010 first, then
  D-008, D-011..D-016, and the open lanes' `wi-798.toml` (D-001 first) and
  `wi-902.toml`. D-015 (WI-902 left committed) is overtaken by the reshape
  ruling.
- **Ruled since the Fable review** (plan revision 8):
  - Test files name their TC; TC rows name no test files or modules, and
    their evidence column becomes generated.
  - The loop refuses an empty route pool. Today it silently falls back to
    the single-model path instead.
  - The convergence round never sees earlier verdicts; regression tests
    confirm fixes.
- **Confirm or overrule** the revision 6–7 clarifications, in the plan's
  rulings section: the cap counts rounds before the checkpoint and the gate
  always runs in convergence stance; convergence-class findings are never
  deferred; lanes in flight restart at zero; IF rows name no files (your IF remark is kept as an
  open question); an explicit `boundary` class in the shipped inventory; the
  plan gate before rows that need it; `agents-enabled`'s TOML shape.
- **Item 11 (what points where) is open:** its open calls, the two owner's
  queries and the decomposition choice (a)/(b) are in the plan's item 11,
  with GPT-6 Astra's views (revision 12) beside them. New with revision 12:
  whether "module" stays the software source file with the wider
  realization units named separately; how generated IF cells declare
  roles and external owners; and whether IF rows' existing approval must
  cover a requirement-bearing allocation.
- **Open after revision 12** (plan rulings section): how a non-executable
  fix is confirmed under the convergence ruling; and which TC evidence
  (CI, inspection records, `::` nodes) stays authored.

## Traps from this session

- When the box is loaded, process queries through WMI (`Get-CimInstance`,
  `tasklist`, `ps -W`) hang. `Get-Process` and its `.Parent` property work.
- Never kill the overnight loop's Python while a leg runs. The venv launcher
  ties its children to it, so killing it takes the leg down. Suspend the loop
  instead, and end it after the leg exits.
- Leg transcripts record one message's usage in several records. Count once
  per message id.

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
   status.md's RESUME HERE names), all of it; the "Owner rulings, 2026-10-11"
   section of docs/plans/2026-10-11-review-churn/README.md and its
   pointer-rules.md, and the plan's item 11 (open; build nothing that
   depends on it until ruled); the coordinator-cycle skill and its references/recipes.md;
   your memory index (review-churn-program-rulings first).
3. Run reviews the way the handoff's "How to run reviews now" says. It
   overrides the skill where they differ, until batch row B1 lands and the
   skill says the same.
4. Work the handoff's queue in order: file and land B1, then the plan gate
   G, then B2–B4 (B4 is WI-902's reshape), each filed on trunk with its scope
   critique and dispositions first; then continue WI-798, then re-order the rest against the plan with the owner. Claim under
   one scoped unpause per batch (a reviewed deletion commit, the claims, a
   byte-identical restore). Cut lanes from trunk's tip and land them one at a
   time. Roles: Claude Opus builds (kit-builder agent, medium); GPT Terra
   (medium) authors spine text in one retained session per lane; Codex Sol and
   the Claude Sonnet stand-in review in parallel; the independent adjudicator
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
