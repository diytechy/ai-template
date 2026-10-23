---
name: coordinator-cycle
description: Use when coordinating work in this template repo, from scope critique at filing or minting through lane claims, code iteration, spine checkpoints, independent review, disputes and landing.
stacks: [any]
domains: [any]
phases: [dev, gate]
tags: [coordinator, lane, review, adjudication, dispute, landing, workflow]
scope: this-repo
---

# Coordinator cycle (this template repo)

This skill is the coordinator's **procedure**, its one home; the current
handoff is **state** (what landed, what is open, what the owner owes). Read
`CLAUDE.md` and `docs/status.md` first. Exact commands, landing steps and
environment traps are in [references/recipes.md](references/recipes.md). Read
it before your first claim and when a step below points there.

Read beside it:

- `session-protocol`: standing rules (§2), commit bar (§3), records and
  coordinator close-out (§4), commit style (§5).
- `spine-authoring`: "Three ways a spine grows" and its
  `references/in-lane.md`.

Record procedural corrections in this skill or its recipes at close-out, never
as a handoff section. Why: corrections in handoffs force every successor to
reconstruct the chain.

## Roles

| Role | Who | Session |
|---|---|---|
| Build | the `kit-builder` agent (Claude Opus, medium) | one per round; leaves its change uncommitted |
| Spine author | GPT Terra (`gpt-5.6-terra`, medium) | **one retained session per lane**, resumed each turn |
| Code review, REVIEW-A | Codex 6.1 Sol (`gpt-6.1-sol`, medium) | **fresh per review**, beside REVIEW-B |
| Code review, REVIEW-B | another family or model than REVIEW-A: a Claude Opus (high) stand-in sub-agent until WI-815's Gemini route has one verified launch | **fresh per review**, given only its brief's path |
| Scope and plan critique | Codex 6.1 Sol (`gpt-6.1-sol`, medium) | **fresh per critique**, one critic |
| Adjudication | a retained Claude Opus home, via `coordinator_adjudicate.py` from the lane | the entry point retains it; never a subagent |

Every Sol and Terra call runs through `scripts/coordinator/codex_call.py`
(recipes §1, "A Codex call"), which records it through the session service:

- inside the blackout window, a Sol or Terra call is refused before launch
  (exit 2), as every non-adjudication call is;
- exit 3 is an edit, exit 4 a log left uncommitted or unspooled, exit 5 a
  change check that could not run;
- in a claimed lane the call commits its log; a call outside one (the
  primary checkout, the detached critique checkout) spools its log and
  commits nothing.

Keep judgement independent: Terra authors and Opus judges, Opus builds and
the full-lane reviewers review, none of them the builder's session. The
adjudicator never drafts the text it judges. Its ruling on a dispute is final.

The review shape follows the review-churn plan's owner rulings of 2026-10-11
(`docs/plans/2026-10-11-review-churn/README.md`, "Owner rulings, 2026-10-11"),
cited below by ruling or revision number (rulings 4 and 7, revisions 6 to 8
and 33):

- There are no narrow rounds. Each round runs the two full-lane reviewers in
  parallel, each from its own `review_brief.py review --scope full` render
  with its own `--scratch`, so each has its own verdict path and its own
  `--basetemp`.
- A Claude REVIEW-B is recorded as a substitution in the lane's decisions
  each time it stands in (ruling 7). The owner chose Claude Opus at high for
  the slot when the program's three-reviewer trial ended (revision 37's
  trial; coordinator-2026-10-16 D-008): it caught what Sol missed, while the
  second stand-in's unique catches never changed a round.

## 1. Before the claim: settle scope and trust where the row is born

Settle scope when filing a row or minting a successor, disposition or split;
do not add a lane-size tripwire to an existing row. Before the claim, render
the scope critique with `review_brief.py critique` over the spec and
`docs/rubrics/scope-critique.md` (recipes §1), and send it to a fresh Sol
session. The rubric's anchors carry coverage (S3), the planning need (S4),
the architectural delta (S5) and dependencies (S6); the brief names the
registries they are judged against. Two of its questions shape the spec most:

- **Name each independently landable deliverable, and which lands first.** If
  the owner keeps several together on purpose, record that in the spec so no
  later session argues it again.
- **Does any deliverable give a file authority over a hold, an act or a gate?**
  If yes, the spec gains a `## Trust` section before the claim:
  - **Producer:** who writes the file, by which route, and what a failed write
    looks like (failed call, timeout, structured error, partial file).
  - **Consumers:** every reader, found by grep and listed by path.
  - **Ruling:** what each consumer does with an absent, unreadable, failed or
    malformed input, and what the authority binds to.

  Route the Ruling to the owner for confirmation or overrule (§5). Apply
  `project-trajectory/PROCESS.md` §3, "When a guard is owed".
  Why: an unstated trust boundary produces separate fixes in every consumer.

**The advice binds before the claim** (rulings 1 and 9; owner, 2026-10-14):

- Every critique recommendation gets a disposition in the spec: adopted,
  quoting the spec text that now carries it, or rejected, with the reason.
- A fresh confirming round checks the adopted ones before the claim. It runs
  in convergence stance, which the rubric's verdict section states, so its
  brief needs only one appended line saying it is a confirming round of
  round N. A new finding blocks the claim only if it is fail-open, data loss
  or a Done-when gap, and a supported workflow or the kit's own routes reach
  it; any other new finding gets its disposition in the spec without another
  round.
- A queued row born before S3, S4 and the delta question is re-critiqued when
  it comes up for claim, one row at a time.

Name the change set's **anchor** in the spec: the approved SN or SR it hangs
from. Label any derived SR with its lens (`spine-authoring` §2(c)). File splits
and preparatory rows on trunk before claiming them.

## 2. Claim

Take the coordinator lease at the session's start, before design work; keep a
design session and a claiming session apart. Claim the whole batch under one
scoped unpause: a reviewed deletion of `docs/work/pause`, the claims, and a
byte-identical restore. The steps and the traps are in recipes §2.

## 3. The lane: plan, intent, iterate, checkpoint

### Plan: a `single` row, before its first build

A row whose claim copy declares `planmode = "single"` plans in its lane
first; the plan-gate hook step and the merge slot refuse any build commit
until a pass record under `docs/plans/<WI>/` binds its plan and Done-when.
The commands are in recipes §1, "Single plan".

1. Render the planner's brief and launch a fresh Claude Opus sub-agent given
   only its path. It writes only its plan, under the scratch root; commit it
   verbatim as `docs/plans/<WI>/plan.md`.
2. Gate it with the coverage step; a failing plan is never critiqued.
   `DELTA: beyond` is never critiqued either: close the lane partial, and
   the disposition adjudicator drafts the refactor successor.
3. A fresh Codex Sol critique, another family than the planner, at medium,
   from the lane. File its verdict and commit that record alone.
4. An APPROVE, or a CHANGES-REQUESTED whose findings are all MINOR: write the
   pass record and commit it alone. Any other: one revision, from the
   revision brief; it must pass the coverage step over the first critique's
   findings; then a second, fresh critique in convergence stance, which never
   sees the first. If that one does not approve, its BLOCKER and MAJOR
   findings go to one dispute sitting, and only an accepted DISMISS of each
   lets the pass record be written. A FIX, SUCCESSOR or ESCALATE goes to the
   owner: close the lane partial (OI-70), never to the build.
5. Dispatch the first build only on a committed pass record. The build brief
   names the accepted plan; the builder reports a change of approach rather
   than editing the plan, since an edited plan holds the lane until a new
   critique passes it. An adopted critique recommendation binds the build
   through the plan; one that changes what the row promises is written into
   its Done-when or Trust section in the lane, which the Done-when hold below
   makes a sitting bless before the build. A Done-when edit (not a tick)
   unbinds the pass record, so adopt it before the critique round meant to
   pass, which it then consumes; after the second critique, write it into
   the Trust section or take it to the owner.

Reviewers receive the WI definition (spec, Done-when, Trust, touched rows),
never the builder's rework coverage plan, the Plan-WI table answering a
round file, kept outside the repository (ruling 4). A committed single plan
is lane work under review.

Never write a critique file by hand: the filing step checks its text, not
its author.

Run intent, iterate and checkpoint. Draft the connected spine set once,
iterate code, then reconcile and judge the set against settled code.
Why: alternating code fixes and row re-attestations buys a sitting per fix.

Omit spine authoring and sittings when no new rows, row-text amendments or
Done-when change are owed; traced-only updates owe no sitting.

### Intent: once, at the start

Rows and tests come before the code (`project-trajectory/PROCESS.md` §4,
"DevStg-Impl — Implementation (test-first)").

1. Dispatch Terra once to author the **whole change set**, TC rows included,
   before build round 1 (for a `single` row, after its pass record), from
   the anchor down, plus the arms map (`spine-authoring`,
   `references/in-lane.md`). Keep new spine rows `Drafted` and existing
   statuses unchanged; interface rows have no approval status. Verify and
   commit the set without a sitting yet. These rows give the builder the
   tests to write and reviewers the obligations the code is meant to meet.
2. Build round 1's first deliverable is the tests, committed alone before
   the code, each under one evidence class (plan item 13's typed evidence):
   - **New or corrected executable behaviour:** a strict expected assertion
     failure (Python:
     `@pytest.mark.xfail(strict=True, raises=(AssertionError, pytest.fail.Exception))`).
     Its red reaches the test's own assertion, never an import error; a
     stub is the builder's choice. The code commit removes the marks.
   - **Characterization of already-correct behaviour:** unmarked, with a
     stated adequacy witness, the wrong implementation it would catch,
     written in the test itself (its docstring or a comment).
   - **An Inspection, Analysis or Attest TC:** the independently checkable
     evidence its declared method names, as the TC row states it.

   A test that fits none is named, with its disposition, in the lane's
   decisions record before the code commit.
3. The builder then builds the code. Re-run its claimed results yourself,
   then verify, regenerate and commit through `integrate.py attest`
   (recipes §6).

A lane claimed before this order landed keeps the order it started with;
record that as a decision in its decisions record.

### Iterate: code only, in counted full rounds

Each round:

1. **The tip carries the review bar's attestation** before any review:
   commit lane work through `integrate.py attest` with the round's
   `--tests`, and `review_brief.py review` refuses any other tip. A
   hook-refused commit or a red bar attests nothing, and the render then
   refuses.
2. **Run the lints after the build round** (ruling 6): `trace.py --strict`
   and `check_trajectory.py --strict`, with the commit bar. They run here,
   at the closure check and at the landing check, never in the commit hook.
3. **The full-lane reviewers, in parallel** (the shape under Roles), each
   from its own brief rendered by `review_brief.py review --scope full` from
   the lane's trunk base to its tip; never a hand-written brief (recipes §1).
   Counted rounds 1 and 2 render with no `--stance`, the ordinary default.
   The third counted round renders `--stance convergence` (below). The kit
   reviewer template carries its clauses: name the failure classes the change
   admits and hunt those first, say why a guard-adding remedy cannot instead
   make the defect unrepresentable, tie severity to reachability, and
   classify an out-of-set input. Keep the spec and Drafted intent as the
   code's obligations; row wording is deferred to the checkpoint, and
   proposed wording goes to the spine change list. File each review as the
   lane's round file with `review_brief.py file --phase REVIEW-A` or
   `--phase REVIEW-B`; it refuses a review without exactly one
   `VERDICT: <APPROVE|CHANGES-REQUESTED> findings=<n>` line.
4. **Triage under the review threat model** (`project-trajectory/PROCESS.md`
   §6, "Review threat model"). Dismiss a finding whose reproduction needs a
   compromised or contrived host, or a contrived scenario, in one recorded
   line, in the lane's `docs/decisions/<branch>.toml`, and never answer it
   with code; re-grade a mislabelled BLOCKER or MAJOR there too. Send a
   contested finding to a dispute sitting (step 7). Only a BLOCKER or a MAJOR
   costs a round; a MINOR goes to the spine change list or a successor row,
   and so does a reviewer's coverage-extension note (ruling 1), which carries
   no severity. A fail-closed refusal of an input the cycle's own procedure
   produces, which the earlier route served, is a regression graded by its
   reach, not a coverage-extension note (owner, wi-912 D-008: a retirement
   the checkpoint carries into scope).
5. **A coverage plan before any fix**, one per round file. The builder's
   first answer to a round file is a `Plan-WI` table, one row per finding
   `F#` (F1..Fn in the order written): its class, every site of the class
   with the search that found it, and the one owning boundary that ends the
   class. Run `plan_coverage.py --findings` over it (recipes §1) and dispatch
   the fix only on exit 0: every finding covered by a row, or excluded with a
   reason. The coverage plan is the builder's tool before a fix; it never
   goes to a reviewer (ruling 4). Why: an instance fix leaves sibling sites
   for the next reviewer.
6. **Findings are claims.** The builder confirms or refutes each one on the
   real code path before changing anything. It acts only on verified evidence
   that no setting or OS retry mitigates. Restate a reviewer's direction as a
   construction ("takes the selected row and never reads the registry"); a
   builder has implemented a direction backwards.
7. **A dispute goes to the adjudicator, and you stay neutral.** When the
   builder or you contest a finding, write the findings file and run a
   `dispute` sitting before another build round (recipes §1). Route the
   builder's position verbatim; do not argue the finding. Each finding comes
   back FIX, SUCCESSOR (a row of its own, filed on trunk at the landing),
   DISMISS with a reason class, or ESCALATE to the owner; the ruling is
   final. Record each ruling in the lane's decisions record, never re-raise a
   dismissed finding, and exclude a dismissed or successor finding from the
   next coverage plan by citing the verdict.
8. **A consolidation outside the spec's named surface stops the round.** When
   the fix needs one owner for something several modules outside the spec
   already read, the builder reports it rather than building it. You file a
   preparatory row on trunk, land it as its own lane, and rebase this lane onto
   it. The §1 Consumers list usually predicts this before the build starts.
9. **Trace fields only.** The builder keeps `Implements:`, the LLR module and
   symbols, and the TC evidence current on each commit. Check structural
   integrity and trajectory (recipes §1); append proposed row-text changes to
   the lane's spine change list. Defer spine authoring and sittings to the
   checkpoint, subject to the Done-when hold below.

If the lane changes its Done-when, obtain a verdict bound to that exact text
or an owner ruling before dispatching another build or closing the row.
Use an early checkpoint if necessary; the ordinary cadence does not release
this hold (`project-trajectory/PROCESS.md` §4).

### Rounds, the cap and the convergence round

- **The cap** (ruling 4, revision 7): at most three counted full rounds
  before the checkpoint. Rounds run until one has no BLOCKER or MAJOR code
  finding, and the checkpoint follows it.
- **The red cap** (revisions 17 and 18): a red bar draws no review. Count
  each red `integrate.py attest` as a red round in the lane's decisions
  record; at `[build] red_rounds_max` consecutive red rounds, close the lane
  partial (recipes §8, "Close a lane partial"), never a new stop.
- **Which rounds run in convergence stance.** The third counted round, the
  last the cap allows, renders `review --scope full --stance convergence`
  (ruling 4: the last allowed round runs in convergence mode). The gate over
  the checkpoint tip, and a round over a rebase that changed code or rows,
  always run, uncounted, and render `--stance convergence` too (revision 7),
  as does a review after a fix round the cap's dispute sitting orders. Each
  renders only after the convergence map below is recorded.
- **The convergence map** (revisions 8 and 33): a convergence round never
  sees earlier verdicts, so before it the coordinator maps every accepted
  finding to a regression test that fails on the pre-fix code or, for a fix
  with no executable test, to independently checkable evidence (the
  corrected text at the cited site, or an inspection record). Record the map
  in the lane's decisions, which the reviewers do not read. A round that
  cannot be mapped in full does not start.
- **At the cap, and after a convergence round,** every open BLOCKER or MAJOR
  goes to one dispute sitting, which rules each FIX, SUCCESSOR, DISMISS or
  ESCALATE. Only that sitting moves a finding to a successor row (owner,
  2026-10-14). A convergence-class finding (fail-open, data loss or a
  Done-when gap) is never deferred: the sitting orders one more fix round or
  escalates. A reviewer's `convergence-class` tag is advice to the sitting.
- **Successor rows** are filed on trunk at the landing, one per SUCCESSOR
  ruling of an accepted verdict, from its binding (§4). Without one nothing
  is filed, and the finding holds the landing.
- **A lane in flight when this shape landed** starts its count at zero at
  its next review, recorded as a decision.

### Checkpoint: when a counted round has no BLOCKER or MAJOR

1. **Terra, resumed, reconciles the whole set** against the settled code: the
   accumulated spine change list plus the arms map. Verify, regenerate and
   commit the reconciled text before composing the sitting. When the set
   was reconciled at an earlier checkpoint and since then no round proposed
   row text and no code moved, omit the turn and record why, after checking
   mechanically that each changed approved cell keeps its approved text
   (WI-914, WI-923).
2. **The closure check passes** before the sitting (`spine-authoring`,
   `references/in-lane.md`: parents, the arms, TC-to-LLR-and-SR, interface
   citations, the strict integrity checks).
3. **One combined sitting** (`coordinator_adjudicate.py adjudicate
   --brief-file <composed brief> --brief combined`) judges every amendment,
   first approval and Done-when change together, top-down (recipes §1). The
   sitting ends at its committed verdict; its act is the later act turn (§4).
   Carry retired rows into scope explicitly. A parent's return carries its
   children; have
   the verdict distinguish children returned only for their chain. Route returns:
   - spine text goes to Terra;
   - code goes to the builder;
   - a byte-exact one-assertion fix you may apply yourself, openly and
     recorded.
   A follow-up answered in the lane moves out of `## Dispositions` to another
   heading. Re-sit returned rows and any affected chain or newly changed rows.
4. **The gate over the checkpoint tip:** the full-lane reviewers, uncounted,
   from the lane's trunk base to its tip, in convergence stance after the
   convergence map (`review_brief.py review --scope full --stance
   convergence`), review code and rows together. An open BLOCKER or MAJOR
   goes to the dispute sitting above; a fix round it orders is followed by
   one more checkpoint before landing. A counted round always precedes the
   checkpoint, and the gate follows it.

Before the final gate, restore the trunk-only generated views on the lane
(recipes §3). The module-size stamp is the exception: the lane carries it.

### Sub-agents and tests across lanes

**Sub-agents** (revision 37): planners, builders and reviewers may spawn
them where reasonable, and the spawner's bounds hold for each one:

- a reviewer's sub-agents see only what its brief gives it, never builder
  material or another reviewer's verdict, and write only in its scratch;
- a builder's sub-agents work in its lane, never two writers on one file at
  once, and the builder stays accountable for the change and runs the bar;
- no sub-agent reviews or adjudicates the work of the agent that spawned it;
- each test runner has its own `--basetemp` beside its spawner's, or leaves
  the runs to its spawner.

**Tests across parallel lanes** (owner, 2026-10-14):

- one `--basetemp` per test runner;
- free disk is checked before lanes fan out, and the full suite runs alone
  at phase close;
- a red that passes when re-run quietly is filed as a load-sensitive defect,
  never charged to the lane or re-run until green.

## 4. Land

Parallel lanes are normal; adjudication is a latched event. A lane's verdicts
may be sat at any time; its acts keep landing order (revisions 31 and 32).
Take a lane's act turn only after the lanes ahead of it have landed and it has
rebased, so its acts and the id watermark pull up as each lane lands. A lane
that took acts on an older base gets duplicate act seqs on rebase, and git
applies the later act commits cleanly. Lanes that take acts land one at a time.
Before the act turn, check that the rows the verdict judged are unchanged since
it judged them: the rows at the verdict's own commit, before the rebase,
against the rebased tip. A renumbered row counts as changed; re-sit any changed
row (recipes §3).

Two landing rules for the machinery itself (owner, 2026-10-14; revision 37):

- **A lane that changes the machinery the cycle runs on lands alone.** The
  next such lane lands only after the cycle has run through the last one's
  changed step.
- **A defect in a landed mechanism change is fixed forward,** in a lane with
  a regression test, never by reverting a landing. A step the defect blocks
  runs by hand, attended and recorded, never through a bypass flag or a
  fallback path. A hook that refuses the fix commit is the owner's to decide.

1. Rebase onto current trunk before the final act. Use recipes §3–§4; if the
   rebase changes code or authored rows, repeat the affected checkpoint and
   run an uncounted convergence round over the rebased tip.
2. After the rebase and the unchanged-rows check, take the act turn,
   `coordinator_adjudicate.py act --verdict <path> --wi WI-NNN` (recipes §3).
   Its act is the lane's last **spine** commit: Status flips and the snapshot
   only, with verdicts committed first. Telemetry may follow.
3. Squash, regenerate, run the commit bar on the staged squash, close the
   row, archive the tips, sweep, and close the re-mint citing the act. Every
   step and its trap is in recipes §3.
4. File one successor row on trunk per SUCCESSOR ruling of an accepted
   dispute verdict, from its binding (recipes §3).

## 5. Decisions and the owner

Record calls not already settled by the spec or a ruled item in
`docs/decisions/<branch>.toml` (`coordinator-<date>.toml` for calls on trunk),
with the riskiest in `high_risk`. Ask the owner to **confirm or overrule**,
never to approve. A decision only the owner can make, and that blocks a row,
becomes a pending open item cited by the row's `needs` in the same commit; then
move to the next row. Stop that row for an owner signature on a new need, a
frame external crossing or an explicit owner checkpoint. A high-risk finding
goes to the owner. Leave held signatures and open-item rulings to the owner,
along with push and merge to main.

## 6. Close-out

Follow `session-protocol` §4, "Coordinator close-out", including the lease
handback or relaunch, and its blackout close-down inside an armed window.
Record procedural corrections here or in the recipes.
The handoff links the one it replaces, points here for procedure, and holds
state only: what landed, what is open, what the owner owes, and the session
prompt. It carries no cycle, recipe or "corrections learned" section.

**Record the session's usage** before the handoff is written, from the
primary checkout (`$PY` and `$SCRIPTS` as in the recipes' section 0):

```bash
"$PY" "$SCRIPTS/usage_ingest.py"
"$PY" "$SCRIPTS/usage_ingest.py" --session <the replaced handoff's session id>
```

- The first run records this session and every sub-agent it spawned into
  the spool. The second records what the previous session wrote after its
  own last run (its closing reply, or a sub-agent message that was still
  open then); skip it when the replaced handoff names no session id. A
  repeated run records nothing twice.
- The handoff names this session's id (`$CLAUDE_CODE_SESSION_ID`) under its
  state, so the next close-out can pick up this session's tail. A nonzero
  exit is recorded there too, with the lines it printed; it is never
  hand-patched.

## 7. Headless legs

This section is the headless procedure's one home. It carries the review-churn
plan's revisions 35 ("The coordinator role") and 36 ("Headless coordinator
legs are marked now"), the owner's 2026-10-14 split ruling (WI-918 takes the
merge slot's reading of the re-claim), and
`docs/decisions/coordinator-2026-10-14.toml` D-015 (the lane-mode reading) and
D-016 (the design calls).

**A headless leg is an autonomous run.** The overnight launcher
(`scripts/coordinator/overnight_legs.py`) marks the run once, before its first
leg: one loop session per run, inherited by every leg and every process a leg
starts. Every leg's prompt is the handoff's session prompt, then the
[headless block](../../../scripts/coordinator/headless-leg.md), then the kit's
provenance line naming the session. After each leg the launcher audits every
ref the leg moved and stops the run, naming the commit or the read, when one
fails its rule. It judges every leg against the trunk it bound at run start,
and stops the run when a leg leaves the primary checkout on any other branch:
a leg's work stays in lane worktrees.

**The trailer on every commit:**

- Every commit message ends with the provenance line, inside its final trailer
  block. That includes the landing's message file and an amended message (the
  last trailer wins), and the `archive/lanes` `commit-tree -F` message, the
  one plumbing commit the coordinator writes itself (recipes §3).
- The kit's own writers (claim, mint, handback, telemetry, the merge slot) add
  the trailer themselves, and the adjudicator gets it from its brief's
  provenance line (WI-912).
- A step the marker refuses is never re-run unmarked or past a hook.

**Foreground only:**

- Every command runs in the foreground, with an explicit timeout up to the
  launcher's raised shell cap (recipes §7, "Background or foreground").
- Every Agent call passes `run_in_background: false`.
- Every builder, reviewer and planner is told to run its commands in the
  foreground.

**Owner-held steps.** A leg never takes a step only the owner can take:

- an act the marker refuses (a status move on a held rung);
- an ESCALATE ruling;
- an open item's ruling;
- a Done-when item that needs an owner act or credential;
- a push or a merge to main.

Any other step the session prompt's Never list or §5 reserves to the owner is
treated the same way. For each such step, the leg:

1. brings the lane to a safe committed point;
2. records the step and its evidence (the verdict, the rows, the command) in
   the lane's decisions record and under the new handoff's "For the owner";
3. turns a decision only the owner can make into a pending open item that the
   row's `needs` cites (§5, unchanged);
4. moves to the next row.

When no row can move without the owner, the leg closes out with the
`Overnight: stop` line in the new handoff. A Codex limit is answered with a
`Resume-not-before:` line, as the launcher reads it.

**The lane-mode rule** (D-015). A lane that a headless leg marked lands
headless: by its claim, or by a commit one of the loop's own writers made in
its range under the marker, a sitting's telemetry commit included. Otherwise
the attended coordinator re-claims it before its own first commit there, its
sittings' verdict and act commits included.

**The re-claim.** The subject's one home is the kit's provenance module,
`kitlib.provenance.reclaim_subject`; the recipe composes it there and never
writes it by hand.

- Compose the subject (`$PY` and `$SCRIPTS` as in the recipes' section 0):

  ```bash
  SUBJ=$("$PY" -c "import sys; sys.path.insert(0, '$SCRIPTS'); from kitlib.provenance import reclaim_subject; print(reclaim_subject('<branch>'))")
  ```
- The attended, unmarked coordinator writes an empty commit in the lane with
  that subject and no trailer: `git commit --allow-empty -m "$SUBJ"`.
- A missed re-claim is placed before the first attended commit. Create the
  re-claim on the last headless commit, then replay the attended commits onto
  it: `git commit-tree <last-headless>^{tree} -p <last-headless> -m "$SUBJ"`,
  then `git rebase --onto <reclaim> <last-headless> <branch>`. A replay keeps
  each message and never reaches the commit floor.
- The merge slot's trailer rung and `check-lane` read the re-claim alike
  (D-017): it closes the lane's trailer window for the commits after it, only
  when it is empty (one parent, that parent's tree) and carries no
  `Loop-Session` trailer at all, and a later loop-writer commit re-opens the
  window. A commit under the subject that is not empty or carries a trailer
  is no re-claim: it is judged like any other commit in the open window,
  refused by name when its trailer is absent or malformed, and with a
  well-formed trailer it passes but closes nothing. The commits before a
  re-claim stay judged, and the held-rung lane rule judges every lane commit,
  loop, coordinator or re-claimed, whatever its window.

**A leg's usage.** Before it writes its handoff and ends its reply, a leg
runs the same pair as §6's close-out, from the primary checkout:
`"$PY" "$SCRIPTS/usage_ingest.py"`, then
`"$PY" "$SCRIPTS/usage_ingest.py" --session <the replaced handoff's session id>`.
A headless session's shell carries its own `CLAUDE_CODE_SESSION_ID`, so the
first run needs no `--session`. Neither run launches a model CLI, so the
blackout window does not deny them. As in §6, the leg's handoff names this
session's id (`$CLAUDE_CODE_SESSION_ID`), so the next close-out records the
leg's own tail.

**A leg's landing.** A leg squashes a lane only after
`"$PY" "$TOOLS/overnight_legs.py" check-lane <lane>` exits 0; exit 3 names
the first refused commit or the read that failed, and that lane is not
landed. A lane holding a re-claim may land once `check-lane` passes: the
check reads the re-claim as the merge slot does.

## Never

Owner-reserved acts and standing prohibitions:

- Push or merge to main. Push is the owner's.
- Rule an open item, or sign a held rung or any act reserved to the owner.
- Leave `docs/work/pause` deleted.
- Read `OWNER_SCRATCHPAD.md` or the adjudicator's token file. Keep only the
  token file's path.
- Self-review, or adjudicate through a subagent. If Codex is rate-limited,
  wait for its reset. After Codex has been unavailable for more than two hours,
  fill the REVIEW-A slot with a fresh independent Claude reviewer and record
  the same-family relaxation in the decisions record.
- Skip a hook, or add a fallback, degenerate or legacy path. Fix the single
  point of failure instead.
- Change `~/.claude` settings, or install software the handoff does not name.
