+++
id = "WI-913"
title = "A row declaring a single plan builds only after its in-lane plan passes the coverage gate and an independent cross-family critique"
workstream = "process"
sr_refs = ["SR-146", "SR-154", "SR-235"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "none"
needs = []
+++

## Deliverable

Landed 2026-10-15. A claimed row whose claim copy declares
`planmode = "single"` now plans in its lane before it builds:
`review_brief.py plan` and `critique --plan` render the single plan's brief
and its critique strictly; `plan-file` files at most two critiques and writes
the pass record, at the cap only behind an accepted dispute DISMISS of every
blocking finding; and a new `plan-gate` check step, in the shipped hook's
floor and on the merge slot's lane-commit walk, refuses build output until a
pass record binds the plan and Done-when digests (`kitlib/plan_pass.py`,
IF-295). Three full-lane rounds in the trial shape, then sittings 010
(combined) and 011 (SR-154's return, answered in the lane) and the uncounted
post-checkpoint gate (012 to 014, APPROVE). Spine: SR-154 amended (the
single-plan hold under its one shall, owner 2026-10-15), LLR-313 and TC-333
amended, LLR-337 and TC-367 new; IF-288 and IF-289 amended, IF-295 new.
Decisions: `docs/decisions/wi-913.toml` D-001 to D-010.

## Context

Filed on trunk on 2026-10-14 by the attended coordinator as the review-churn
program's batch row G, split from WI-805
(`docs/handoff-2026-10-11-attended-coordinator.md`, the queue table). Owner
ruling 9 pulls WI-805's per-item plan gate forward. Decision 4 (revision 18)
puts the plan after the claim, in the lane, before the first build. Plan item
9 step 3 makes it the one planning path: a build starts only after a passing
independent plan verdict, and a capped revision that does not pass goes to a
dispute sitting or to the owner, never to the build. The plan's "Owner
rulings" section through revision 37 governs where this row and a ruling
differ. The gate's shape (plan, coverage gate, one cross-family critique, at
most one revision; the plan at `docs/plans/<WI>/plan.md` in the lane) is
WI-788's approved design, chapter 3 §4.1, §4.5 and §4.7.

Once this row lands, a row S4 marks `single` builds only after its plan
passes; such a row may be claimed earlier (the handoff's queue). This row
cannot plan itself, so it is built without the gate (the revision 6–8
clarification "the planning gate comes before rows that need it", confirmed
in revision 35). It carries no `planmode`, so its own check never holds its
own lane once that check is in the lane's tree, and the coordinator records
this as a decision when it files the row. No interim or hand-run plan stands
in for the gate (item 9 step 3).

WI-805 keeps the loop's planning step, the replan at the family swap and the
build-below-planner dial, with WI-804 and WI-799 in its `needs`. This row
needs neither (revision 36). It launches its planner and its critic the way
the scope critique is launched by hand today, and WI-804 later routes the
same `plan` and `plan-critique` calls, so no second launch path is added.

## Deliverables

One lane, one landing (S1). The `(Qn)` marks are the open calls below; the
text assumes each recommendation.

1. **The planner's brief** (shipped; RESYNC entry).
   - A new `prompts/plan-single.template.md`, registered in `prompts.py`,
     listed in the prompts README table and the generated
     `prompts/CATALOG.md`, and filled strictly by a new `review_brief.py plan`
     render.
   - Its inputs: the work item's spec, and its Done-when items as the
     `D1…Dn` clauses `plan_coverage.py` reads (`kitlib.done_when.items`). It
     points the planner at what the plan must cite and the delta question
     reads: the item's SR rows, the TCs that verify them, the interface and
     component registries, and the runtime flows.
   - It states the plan contract `plan_coverage.py` checks: one `Plan-WI`
     table, and `Excludes:` lines with reasons.
   - It asks the architectural-delta question in plan item 12 entry point 2's
     own words, in the first plan and in the revision, with its two outcomes:
     carry the change within scope, or close partial (item 12, revisions 18
     and 20). The answer is one typed line from a closed set,
     `DELTA: none|within|beyond` (Q8). It names no skill: item 12's text lane
     (P6) adds that one line.
   - Revision mode adds the planner's own plan and the critique's findings,
     labelled claims under judgement.
   - The planner is a fresh Claude Opus sub-agent given only the brief's path
     (plan is an Anthropic kind and plan-critique an OpenAI one: WI-788 README
     A1, this repo's values). It writes only its plan, under the scratch
     root. The coordinator commits it verbatim as `docs/plans/<WI>/plan.md` in
     the lane.
2. **The plan critique** (shipped; RESYNC entry).
   - `review_brief.py critique` gains a plan mode. The artifact is the plan,
     read with its spec and the coverage report `plan_coverage.py --item
     --out` writes over the Done-when alone, so a second critique never meets
     the first one's findings.
   - The rubric is `docs/rubrics/plan-decomposition.md`: item 12 has the plan
     critique judge with it, and P6 gives it the delta question. Its header
     names this second use, a single plan's rows being one work item's steps
     (this repo's rubric; no RESYNC entry).
   - The verdict's first line is `Reviewed: <full sha>` of the lane commit
     holding the plan. It goes to a path of its own per round, never the
     scope critique's.
   - The critic is launched with `scripts/coordinator/sol_review.sh` from the
     lane, as a review is: Codex Sol at medium, fresh per critique, another
     family than the planner.
3. **The filing step, the pass record and the cap** (shipped; RESYNC entry).
   - A `review_brief.py` subcommand files each critique verdict beside the
     plan and, from a later commit, writes the pass record. The Trust section
     is its contract.
   - It checks the critique's commit binding and runs the coverage gate once,
     here. Later readers trust the record and recompute neither (ruling 2).
   - A critique's word is read through `kitlib.verdict.effective_verdict`,
     the one rule the loop and the merge slot share: a CHANGES-REQUESTED
     whose findings are all MINOR reads as an APPROVE (ruling 4: a MINOR
     never costs a round), its findings left in the filed record for the
     build to weigh, and one with no findings stays a refusal.
   - Any other CHANGES-REQUESTED critique allows one revision (item 9 step 3;
     WI-805's "at most one revision"). The revised plan must pass
     `plan_coverage.py --item <spec> --findings <that critique's record>`
     (WI-853's shared step: each finding covered by a row, or excluded with a
     reason). Then a second, fresh critique judges it, in the convergence
     stance and never seeing the first verdict (Q2).
   - If the second critique does not read as an APPROVE, its BLOCKER and
     MAJOR findings go to one `dispute` sitting, through the existing entry
     point and brief. The pass record is written only when the sitting's
     accepted verdict rules each of them DISMISS. A FIX or an ESCALATE goes
     to the owner: the lane closes partial for an owner decision (OI-70),
     never to the build (Q3). A second critique that does not read as an
     APPROVE and has no BLOCKER or MAJOR finding to dispute (a
     CHANGES-REQUESTED with no findings) also closes the lane partial for
     the owner: an empty dispute set never authorizes a pass record.
   - A `beyond` delta is not critiqued and never passes. The lane closes
     partial, and the disposition adjudicator drafts the refactor successor
     (item 12, revision 18).
4. **The gate** (shipped; RESYNC entry).
   - One predicate. The record's grammar, its digests and its one reader live
     in one `kitlib` module, which the filing step writes through.
   - It is asked by the pre-commit hook of the commit being made: a `check.py`
     step beside `done-when-blessed`.
   - It is asked at a landing of each lane commit the landing carries, riding
     the shared lane-commit walk (`text_then_act.lane_commit_walk`, used by
     the hook's squash path and by `integrate.py`'s merge slot) with its own
     judge, as the ruling sync does. So `--no-verify` lands nothing (Q1; the
     owner's 2026-10-03 rule, enforce at the commit; ruling 2's
     record-at-event shape).
   - It judges only the rows the lane itself claimed, under
     `docs/work/active/<its branch>/`, never another lane's claim copy that
     its tree also carries. For each such row whose claim copy declares
     `single`:
     - a commit that changes a path outside the record homes (S3) is refused,
       unless its parent holds a pass record binding the row's current plan
       and Done-when (Q4);
     - a commit that adds or changes a pass record is checked against its
       parent.
   - A merge is judged by what neither parent carried, as text-then-act
     judges one. Bindings are by digest, so a rebase keeps them.
   - Trunk, and a lane with no `single` row, are never held.
   - The managed loop needs nothing here. It is paused, and until WI-805
     gives it a planning step, its build of a `single` row is refused at the
     commit like any other (Q6).
5. **The `coordinator-cycle` skill and its recipes** (this repo's tooling,
   synced to `.claude/skills/`; no RESYNC entry).
   - The plan step for a `single` row, after the claim and before the first
     build: render, launch, commit the plan, gate, critique, file and commit
     the critique, then write and commit the pass record; the one revision,
     the sitting or the owner at the cap, and the `beyond` close. The
     commands go in the recipes.
   - The build brief names the accepted plan. The builder reports a change of
     approach rather than editing the plan, since an edited plan holds the
     lane until a new critique passes it.
   - An adopted critique recommendation binds the build through the plan. One
     that changes what the row promises is written into its Done-when or Trust
     section in the lane, which the WI-841 hold makes a sitting bless before
     the build (decision 4, revision 18). Reviewers still receive the WI
     definition as ruling 4 lists it (Q5).
6. **Shipped text** (RESYNC entry). None of it names a row id of this repo.
   - `work/WI-000.template.md`, with its byte-identical copy
     `docs/work/queued/WI-000-example.md`, documents the `planmode` values the
     gate reads and what `single` holds.
   - `GLOSSARY.md`'s "implementation plan" entry says what exists today (the
     attended plan step) and what is still planned (the loop's).
   - `orphans-allow.template` gains the plan records' glob, with its reason.
     This repo's `docs/orphans-allow` already covers `docs/plans/*`.

## Trust

The pass record releases the gate that holds a `single` row's build. It is a
file on disk, and the plan and the critique it rests on are model output
(`project-trajectory/PROCESS.md` §3, "When a guard is owed").

- **Producer and write route.** One filing step (deliverable 3), run by the
  coordinator from the lane root, in two commits, so the commit that adds a
  pass record has a parent holding everything the record cites:
  1. **File.** It checks that the critique is bound to the lane commit it
     judged, whose tree holds the plan, and carries exactly one `VERDICT:`
     line whose count matches its findings (`kitlib.verdict.filing_refusal`,
     the rule `review_brief.py file` applies to a review). It files every
     critique as a record beside the plan, and the coordinator commits that
     record alone.
  2. **Pass.** From that commit, its pass form checks that HEAD holds the
     filed critique and any dispute verdict it cites, that the tree the
     critique reviewed holds the same work item, the exact plan bytes and the
     same Done-when digest as HEAD (compared by content, so a rebase keeps
     them; a mismatch is refused until a fresh critique judges the changed
     inputs), that the coverage gate
     passes on the plan at HEAD, and that the delta line is `none` or
     `within`. It then writes the pass record, which the coordinator commits
     alone.

  Both commits change only `docs/plans/<WI>/`. The pass form writes a record
  only for a critique that reads as an APPROVE through
  `kitlib.verdict.effective_verdict` (deliverable 3), or, at the cap, for a
  critique whose BLOCKER and MAJOR findings the cited accepted dispute
  verdict all rules DISMISS.
- **Failed-write shapes.** A failed or timed-out critic call leaves no verdict
  file, so nothing is filed. A refused filing exits 2 and writes nothing
  (IF-289's rule). An interrupted write can leave a partial record, which
  every reader treats as malformed. A failed planner call leaves no plan,
  held as Absent. The dispute verdict's producer and failure shapes are the
  adjudication entry point's (`coordinator_adjudicate.py`, IF-283 to
  IF-285): a failed or refused sitting leaves no accepted binding, held as
  Failed. None of these releases anything.
- **Consumers.** Grep finds no reader of `docs/plans/<WI>/` today:
  `plan_artifacts.py` writes only `docs/plans/DP-NNN-<slug>/`, and
  `check_vocab.py` and `check_doc_refs.py` only exempt `docs/plans/` from
  their text checks. The readers this row adds, each through the one `kitlib`
  reader:
  - `project-trajectory/scripts/check.py`, the pre-commit step. It validates
    a commit that adds or changes a pass record against its parent: its
    digests are the parent's plan and Done-when and equal those in the tree
    the cited critique reviewed, and the critique and dispute
    records it cites are in the parent and pass. It holds a build commit
    whose parent has no binding record.
  - `project-trajectory/scripts/text_then_act.py`'s lane-commit walk, as the
    hook's squash path and `project-trajectory/scripts/integrate.py`'s merge
    slot ask it of each lane commit. It re-checks only what a rebase cannot
    change.
  - The coordinator, through the `coordinator-cycle` skill. It dispatches the
    first build only on a committed pass record.
  - Later, not in this row: WI-805's loop planning step and WI-799's
    lane-state provider, through the same reader.

  The `planmode` readers today (`schedule.py`, `intake.py`, `plan_runner.py`,
  `agent_loop.py`) act on `dual` alone, and `single` changes nothing for any
  of them (`tests/test_schedule.py` pins that for the scheduler). The gate is
  the one reader that gives `single` a meaning.
- **Ruling per input.** Each holds; nothing here fails open.
  - **Absent** (no record, no plan, no plan directory): held, naming the row
    and what is missing.
  - **Unreadable** (a git read or a decode fails): held, naming why.
  - **Failed** (only a critique that does not read as an APPROVE, a coverage
    failure, a `beyond` delta, a sitting's FIX or ESCALATE): no pass record
    exists, so
    held. The lane goes to the owner or closes partial, as deliverable 3
    says.
  - **Malformed** (a record outside its grammar, a digest that is not the
    current plan's or Done-when's, a citation its parent does not hold):
    held, saying which. A digest mismatch says the plan or its Done-when
    changed after the verdict, and a new critique must pass the changed plan.
  - **The `planmode` it gates on** is read from the claim copy
    (`kitlib.done_when.claim_copy`), stripped and lowercased. `single` holds
    until a pass record binds. Absent, empty, `none` and `dual` are not held
    by this gate. Any other value holds, naming it.
- **What the authority binds to.** The work item id, the plan's exact bytes,
  and the Done-when the plan was gated against (the digest
  `kitlib.done_when.digest` computes, so a tick or evidence never unbinds
  it), all in the lane's own tree.
  - A plan or Done-when edited after the record unbinds it (Q4).
  - A record copied from another lane names another row or digest and binds
    nothing.
  - A lane that edits its own `planmode` changes nothing, because the claim
    copy is read.
  - The filing validates the critique's text, not its author. Until the
    critic's call is recorded by the session service (the handoff's P2 for
    `sol_review.sh`, WI-804 for the `plan-critique` kind), a hand-written
    critique file is the exposure the attended review files carry today, and
    the skill forbids writing one.

This ruling goes to the owner to confirm or overrule (`coordinator-cycle`
§1).

## Done-when

- A test drives each arm of the gate on a fixture lane, and fails on the code
  before the change:
  - a build commit with no pass record is refused at the hook and at the
    landing walk, and one after a pass record is not;
  - a plan or Done-when edited after its record is refused until a new record
    binds it, and ticking a Done-when item does not unbind it;
  - an absent, unreadable or malformed record holds, and so does one naming
    another row or digest;
  - a pass-record commit whose digests or citations its parent does not
    support is refused;
  - each record home, and a close of the row, passes before any record;
  - a rebased lane's record still binds, and a merge is judged by what
    neither parent carried;
  - a lane that edits its own `planmode` is still held, and a lane whose tree
    carries another lane's `single` claim copy is not held by it;
  - a claim copy whose `planmode` is absent, empty, `none` or `dual` is not
    held, and any other value holds, naming it;
  - trunk commits, and a lane with no `single` row, are not judged.
- `review_brief.py plan` and the plan critique render strictly: an unfilled
  slot, or a missing spec, plan or rubric, refuses and writes nothing.
- The filing step refuses, exiting 2 and writing nothing, each of: a critique
  that is unbound, malformed or count-mismatched; a plan the coverage gate
  fails; a missing or `beyond` delta line; at the cap, a dispute verdict that
  is not an accepted DISMISS of every BLOCKER and MAJOR finding; and a pass
  form run where HEAD lacks a record it cites; and a pass form, or a
  pass-record commit, whose cited critique reviewed other plan bytes or
  another Done-when digest than HEAD's. A test covers each. A
  MINOR-only CHANGES-REQUESTED critique passes and one with no findings does
  not, and the pre-commit check refuses a pass record committed together
  with a critique it cites, while the two-commit order passes.
- `prompts/plan-single.template.md` is in `prompts/CATALOG.md` (the
  `prompt-catalog` check passes), asks the delta question in item 12 entry
  point 2's words in both modes, and names no skill.
- The `coordinator-cycle` skill and recipes carry the plan step. The
  `.claude/skills/` copy matches the kit source (`bootstrap.py --dest .
  --sync`), and `WI-000.template.md` and its copy stay byte-identical
  (`tests/test_dogfood_sync.py`).
- The change's spine rows are authored in the lane and sat at its
  checkpoint. By the WI-788 matrix and LLR-313, they are: the planning half
  of SR-154's acceptance (the dial stays WI-805's); LLR-313 and TC-333 for
  the briefs and the filing; a new LLR and TC for the gate; and IF-288 and
  IF-289 for the new subcommands (Q7).
- `RESYNC_PACK.md` carries one entry for the shipped changes. It forces no
  migration on a repo with no `single` row, and it says that a claimed row
  whose `planmode` is outside the set is now held.
- The bar is green on the landing tip: the smoke tier within its budget,
  `check_trajectory.py --strict` clean, and `trace.py --strict` with no
  finding beyond LLR-292's.

## Scope answers

- **S1:** one landable unit. The briefs and the pass record (deliverables 1–3,
  5 and 6) could land without the gate (4), but the gate has nothing to read
  without the record, and the record without the gate is the procedure-only
  path item 9 step 3 withdrew. If the critique splits them, the record lands
  first, and no `single` row builds until the gate lands.
- **S2:** yes. The pass record releases the build gate; see `## Trust`.
- **S3:** three input spaces, each closed by enumeration with deny by default.
  - **`planmode` values:** absent, empty, `none`, `single` and `dual`. Any
    other value holds.
  - **Paths a `single` lane may change before its pass record:** the record
    homes and a close of the row. The homes are `docs/plans/<WI>/`;
    `docs/reviews/` (a dispute sitting's findings, verdict and binding);
    `docs/decisions/`; the session logs under `docs/iteration/`; the work
    branch's log fragments under `docs/log.d/`; and the row's own spec under
    `docs/work/active/<branch>/`. A close is the spec's move out of
    `active/`, its report under `docs/handbacks/`, and the move's own
    inbound-link edits, as `handback.close_partial` writes them. A merge's
    own changes may also be what the station refresh writes: the compiled
    `docs/log.md` and the views `trunk_step.regen_writes` lists; outside a
    merge, those paths stay build output (round 2's 006 F1, decision D-004).
    Any other path is build output and is refused, so a writer the set
    misses fails closed, by name. The builder confirms the set by grep for
    every writer that commits in a lane before its first build, and a test
    pins it.
  - **Model output:** the critique's verdict grammar, the plan's table
    grammar (`plan_coverage.py` exits 2 on a malformed plan) and the delta
    line's closed set. Anything else is refused with no record.
- **S4:** by the criteria, `single`. The row has a Trust section, touches
  several script families (the attended briefs, the commit check and the
  landing walk, and a new `kitlib` reader), and promises behaviour over
  three input spaces. It is built without the gate because it cannot plan
  itself, so it carries no `planmode`, and that is recorded (Context).
- **Architectural delta:** yes on all four, each carried within scope.
  - **A new state:** a `single` lane is held until its plan passes, derived
    from committed records, with nothing stored.
  - **A new domain value:** `single` gains its meaning in a closed
    `planmode` set.
  - **A new input:** whether a lane commit is accepted now depends on the
    pass record.
  - **A new boundary:** the planner's and the critic's output enter the repo
    as records a commit check reads.

  No preparatory refactor is needed. The gate rides the existing walk and
  hold pattern (WI-806, WI-841), and the briefs reuse `review_brief.py`,
  `prompts.fill` and `plan_coverage.py`.
- **B3 and B4:** the gate trusts the record written at the event, and its
  commit check compares that commit with its parent; nothing re-derives the
  verdict from history. No Done-when item needs an owner act or credential:
  the owner's route at the cap is the existing partial close, and the Trust
  ruling is confirmed or overruled without holding the build.
- **Dependencies:**
  - **`needs = []`.** WI-804 and WI-799 stay WI-805's (revision 36).
    Everything this row reuses has landed: WI-803's gate, WI-852's briefs,
    WI-853's findings step, WI-806's walk and WI-841's hold.
  - **No new third-party package, tool or service.**
  - **WI-911:** a file overlap, not a dependency. Both rows edit
    `review_brief.py` and the `coordinator-cycle` skill, so whichever lands
    second rebases.
  - **Rows that wait on this one:** WI-912, WI-915 and WI-916 carry it as a
    soft edge and a Done-when hold.
  - **A mechanism change:** this row lands alone, and the next mechanism
    lane lands only after a `single` row's plan has run through this gate
    (owner, 2026-10-14).

## Calls ruled at filing

The coordinator ruled the drafter's eight calls as recommended
(coordinator-2026-10-14 D-005), and recorded that this row is built without
the gate it builds: `planmode = "none"`, because it cannot plan itself, and
a `single` mark would let its own new check hold its own lane.

- **Q1:** the commit refuses the build: the pre-commit hook in a `single`
  row's lane, and the same check on every lane commit at landing.
- **Q2:** the one allowed revision is judged by a second fresh critique, in
  convergence stance.
- **Q3:** a dispute sitting's FIX after the one allowed revision goes to the
  owner.
- **Q4:** the pass record binds the plan and the Done-when.
- **Q5:** adopted advice binds the build through the plan; advice that
  changes what the row promises is written into its Done-when or Trust
  section in the lane, so reviewers receive it with the WI definition.
- **Q6:** the loop's dispatch hold is WI-805's remainder.
- **Q7:** the gate's own requirement hangs from SR-154.
- **Q8:** the plan states its architectural-delta answer on a typed `DELTA:`
  line.

## Critique dispositions

Round 1 (Codex Sol, medium, 2026-10-14; two findings):

- **S2, MAJOR: adopted.** The filing step wrote the pass record in the same
  step as the critique it cites, which the pre-commit check, reading cited
  records from the parent, must refuse. The Trust section's write route now
  runs "in two commits, so the commit that adds a pass record has a parent
  holding everything the record cites": "**File.** ... the coordinator
  commits that record alone" and "**Pass.** From that commit, its pass form
  checks that HEAD holds the filed critique and any dispute verdict it cites
  ... which the coordinator commits alone". Deliverables 3 and 5 and the
  Done-when carry the order and its tests.
- **S3, MINOR: adopted, with a different resolution.** The capped
  MINOR-only case is closed through the kit's one severity rule instead of a
  partial close, which would cost the owner a decision over findings ruling
  4 says never cost a round. Deliverable 3 now reads: "A critique's word is
  read through `kitlib.verdict.effective_verdict` ... a CHANGES-REQUESTED
  whose findings are all MINOR reads as an APPROVE", at either critique. The
  remaining case is the critic's: "A second critique that does not read as
  an APPROVE and has no BLOCKER or MAJOR finding to dispute ... also closes
  the lane partial for the owner: an empty dispute set never authorizes a
  pass record" (coordinator-2026-10-14 D-007).

Round 2 (Codex Sol, medium, 2026-10-14, the first confirming round; two
findings):

- **S2, MAJOR: adopted.** A pass record could pair current digests with a
  critique of an older plan. The pass form now checks "that the tree the
  critique reviewed holds the same work item, the exact plan bytes and the
  same Done-when digest as HEAD (compared by content, so a rebase keeps
  them; a mismatch is refused until a fresh critique judges the changed
  inputs)"; the pre-commit check verifies the same, and the Done-when tests
  both.
- **S2, MINOR: adopted.** "Failed-write shapes" now names the planner's and
  the dispute verdict's failures: "A failed planner call leaves no plan,
  held as Absent. The dispute verdict's producer and failure shapes are the
  adjudication entry point's".
