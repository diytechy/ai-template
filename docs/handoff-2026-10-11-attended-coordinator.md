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
reviewed by GPT-6 Astra at low effort (revision 12 answers it), and
revision 12 by Claude Fable 5.1 at medium effort (revision 13 answers it).
All six reviews are under `reviews/`. Item 11 is
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
- **Open after revision 13:** item 11 and **OI-112** are one question
  (OI-112's (b) points SR → IF, item 11 points IF → requirement); rule the
  direction once. Item 11's calls 1 and 4 would amend ruling 5's wording.
- **Revision 14 (item 11 fitness):** two analyses, Astra and Fable at medium
  effort, independently find that item 11 as proposed does not reduce
  rework, and recommend variant E.
  - **What E keeps:** `Implements:` stays, and IF → LLR is authored only on
    interfaces that carry a behaviour.
  - **What E adds:** a delivered-dashboard IF and a reach dial.
  - **Where fitness is judged:** when a row is touched, not as a gate.
  - **New calls,** in `docs/plans/2026-10-11-review-churn/item-11-llr-fitness-report.md`:
    - the authoring guidance (`spine-questions.md:218`) still tells authors
      to name symbols in LLRs; pull the fix into phase 1?
    - 114 IF `data` cells name code: classify the `call` rows first?
    - interactive dashboard evidence?
- **Revision 15 (owner's positions, for confirmation):**
  - **Variant F** refines E (item 11):
    - components are declared on the realization, so LLR → CMP retires;
    - files are created at design time;
    - there is no IF → LLR list: a TC names the IF it drives;
    - interfaces are thin and approved just in time;
    - an id-continuity rule governs amendments;
    - the assumption bridge joins the SR-side derivation.

    Interfaces are required at every architectural boundary at any depth.
    An LLR names the IF it constrains (requirement → IF, OI-112 (b)). An
    interface's value domain is a closed MECE enumeration, and boundaries
    keep dependencies sparse. F-calls 1–7 are open:
    - 5 is recursive components, with W3's lane stages as the first case;
    - 6 is the test for when to descend (a describable state descends; an
      invented number stops);
    - 7 is what to mechanize (checks A–C) and the vocabulary, after the
      research in item-11-value-domain-research.md.
  - **Item 7:** the second reviewer is from a third family when one is
    available, otherwise a different family or model.
  - **Item 5:** the per-module `Implements:` floor is withdrawn; links back
    are encouraged, not mandated.
  - **Item 13 (new, open):** review only a green tip. The order is lint,
    then tests, then review; today nothing refuses a review on a red tip.
    Test cases are reviewed in stages: written before the code with a
    recorded red-before, checked mechanically at the gate, judged for
    adequacy by the reviewers, and judged as text at the sitting. Calls:
    whether the gate sits at the start of review or only at landing,
    TC-first in lanes, and a mutation trial.
  - **Item 12 (new, open):** architectural decomposition at three moments.
    - **One definition:** a rubric and an `architecture-decomposition`
      skill, not a hat (the owner decided: hats serve SN → SR).
    - **Three entry points:** a fresh-vision breakdown; the planner's
      architectural-delta question, with no automatic trigger and a
      handback when the change is beyond the WI's scope; and an on-demand
      `run.cmd arch-audit`.
    - **First step:** a dry run of the drafted rubric on W3 Autonomy, before
      anything is built.
    - **Critique cadence (owner's position):** at depth 0, once over the
      whole tree before the build, and every second level of component
      depth. Confirm the reading of "top level".
    - **Also proposed:** an Architect role owning the CMP and IF rows; the
      planner prompt naming the skill; and code-hygiene tools in the audit
      (stdlib in-kit; jscpd, knip, vulture, lizard, radon, shellcheck and
      PSScriptAnalyzer if the adopter declares them).
  Also: the minimum profile's path from code to LLRs (kept under F, since
  `Implements:` stays). The authored IF list is superseded by F's
  requirement → IF direction; see item 11's status table.
- **Revision 16 (Astra and Fable reviews of revision 15, both REVISE):**
  F is corrected in place, and two new calls are open: F-call 8 (must every
  LLR name an interface?) and F-call 9 (one home for the contract). F-call 1
  now has three positions:
  - an authored component id, which amends OI-67 (a);
  - a generated owner;
  - the module path, which conflicts with ruling 5.

  Item 12's critique gates are named. Item 13's green record becomes one
  tree-bound bar attestation shared with landing, and its red-before is a
  record, with typed evidence for non-executable TCs.
- **Revisions 17–18 (the owner's 2026-10-13 answers, and the Astra-high and
  Fable-medium reviews of revision 17, both REVISE).** These supersede the
  revision 15 and 16 bullets above where they differ; the plan's status
  paragraph and item 11's status table are the current record.
  - **Answered:** F-call 1 (i), so an IF's owner is a component id or an
    `external:` party, with the 35–39 cells that hold placement today
    migrated (decision 1). F-call 2: stubs only where the design needs them;
    the builder mints files and must not duplicate. F-call 8: an LLR need
    not name an IF; placement is derived. F-call 9 with decision 2: an
    interface states its form only, in one line that is the `data` cell
    until the build and the body's first line after; an LLR or SR states
    the behaviour and its dimensional scope; every IF is pointed at by at
    least one. Decision 4: the plan comes after the claim; the scope
    critique asks the questions that reshape the queue.
  - **Item 13 answered:** gate the start of review; about three red rounds,
    then a partial close (OI-70's only stop); TC rows before the build with
    failing test code as its first deliverable; a scoped test set (SR,
    direct and through its LLRs) over the smoke floor; an advisory mutation
    trial. The dashboard's interaction checks run in a browser, off the
    commit bar, each view stamped from its observation record.
  - **Confirmed in revision 19:** decision 3, option (A).
    `dependency_admission = "owner-or-delegate" | "independent"`, with the
    first the default: the lane hands back as an open item, ruled by the
    owner or a delegate. A delegate can do everything the owner can; the
    owner has explicitly permitted an LLM agent to act in their stead. Owed:
    PROCESS.md §4's wording, which today grants delegation only to an
    attended session and only for held-rung approval.
- **Revision 20 (the owner's answers to the revision 19 reviews of Astra-high
  and Fable-medium, both REVISE):**
  - The IF `data` cell holds the whole form, no one-line limit; `call` rows
    are classified, a boundary-crossing one getting a typed form without
    symbol names.
  - An SR gains the optional `constrains` cell; a derived check keeps OI-43's
    executable-test guarantee, and OI-43's check stays until the link exists.
  - Owner and delegate are one role, owner-or-delegate, distinct from an
    autonomous run (what the kit's machinery starts and marks). Enforcers are
    unchanged; a vocabulary rewrite rides item 10's RESYNC entry. **For the
    owner:** is the coordinator role owner-or-delegate (unmarked, as today)
    or an autonomous run when headless?
  - The red-before is proven by strict expected-failure marks, described
    stack-neutrally; contrived scenarios are not designed against.
  - The LLR's dimensions cell is the one home of an input space.
  - **Proposed, for the owner:** a derived component context in the build
    brief.
  - **Next:** one more review pair in a fresh session, from
    `docs/plans/2026-10-11-review-churn/review-handoff-r20.md`.
  - **The owner's acts owed once F is ruled:** overrule ruling 5's "LLRs
    keep naming their component" explicitly, and amend OI-67 (a)'s
    IF-owner header text.
  - **Still open:** F-calls 3 (now per TC and LLR pair) to 7, consumer and
    requestor roles, item 12's reading of "top level", and the dashboard
    check's cadence.
- **Revisions 21–29 (2026-10-13 and 14):** the plan is consolidated (revision
  28): read its Status first, which says what is ruled, open and proposed;
  the revision log and every review's dispositions moved to its
  `history.md`. New since revision 20: item 14 (retire the SN-036
  perspective-record sidecar and wire the hat questions into the SN → SR
  briefs; SAFETY leaves this repo's roster), item 15 (one WI per lane) and
  item 16 (a watermark carrier lane every mint draws from, the keep-or-mint
  rule for ids, and the adjudicator freed from landing order, for a closer
  look). The open owner calls are the plan's phase 0. The `contract_split` divergence report is
  closed (`docs/plans/2026-10-13-contract-split-divergence.md`).
- **Revision 30 (2026-10-14):** the revision 29 review pair (GPT-6 Astra
  and Claude Fable 5.1, medium, both REVISE) is folded in; dispositions in
  `history.md`. Item 16's carrier now re-founds the watermark's hand-raise
  rule on recorded reservations (WI, space, range), checks a lane's new ids
  against them at landing, and orders the act ledger by seq. Item 15's port
  gains LLR-061 and TC-061, and "`contract_split`" means `961f9e47` (the
  local branch stops at the ancestor). F-call 4 is answered by keep-or-mint.
  **For the owner:** the unlatched adjudicator, narrowed to the reviewers'
  option (verdicts move between lanes, acts keep landing order); whether to
  fast-forward the local `contract_split` branch to origin; and confirm or
  overrule the reservation record and F-call 4's closure.

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
