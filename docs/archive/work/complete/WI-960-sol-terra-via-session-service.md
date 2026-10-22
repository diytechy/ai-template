+++
id = "WI-960"
title = "Sol and Terra calls go through the session service: the change check runs between the call and its record, another call's session-log commit is not an edit, and a call outside a claimed lane records its log in the spool and commits nothing"
workstream = "process"
sr_refs = ["SR-222"]
specref = ""
buildtier = "strong"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = ["~WI-957"]
+++

## Deliverable

Landed by headless leg 12 of loop session `20261021T045653Z-213020`, squashed from lane `wi-960`.

- **The route.** `scripts/coordinator/codex_call.py` is the one launch path for a Sol review, a Sol critique (scope or plan) and a Terra turn (roles `REVIEW-A`, `CRITIQUE`, `AUTHOR`). It resolves the role's enabled roster row, launches under its declared template through the session service's `call` (one seam between `act` and `record`), runs the change check between the call and its record, records the log, and exits 0 to 5 (refused before launch, an edit, an uncommitted or unspooled log, a check that could not run). An `AUTHOR` turn names one of the lane's work items; `--resume` continues the thread of the lane's newest committed `AUTHOR` log, chosen by its name's stamp, and refuses a missing, damaged, foreign or newer-uncommitted carrier before launch.
- **The change check.** It compares HEAD, the status with each path's index state and content identity, and the commit range before and after the call. A commit that only adds standard-call logs (another call's record) is discounted, and so is such a log left uncommitted; anything else is an edit for Sol, and uncommitted changes are Terra's output.
- **The spool.** `session_service.record` commits a log only from a claimed lane (a linked worktree whose branch's or trunk's tree holds its claim; an unreadable claim read adds no claim). From any other root it writes the log under the primary checkout's `out/sessions/spool/` and commits nothing, and it reports `committed`, `spooled` or the refusal. The shipped `.gitignore` template ignores `out/sessions/`.
- **Text.** The coordinator-cycle skill and recipes launch every Sol and Terra call through the route (three copies byte-identical), with the headless launch order (REVIEW-B before REVIEW-A); `sol_review.sh`, `terra_author.sh`, `luna_review.sh` and `layout.sh` are retired; Flow 7 in the runtime flows.
- **Spine.** SR-243 (derived), LLR-346, TC-384 and TC-385 approved (act seq 152); LLR-269, LLR-270, TC-265 and TC-268 re-attested (act seq 151); sitting 006 (`docs/reviews/wi-960/006-ADJUDICATE-91aae34.md`). Reviews: counted rounds 1 and 2 and the gate (`docs/reviews/wi-960/001` to `008`); decisions `docs/decisions/wi-960.toml` D-001 to D-016.
- **Live runs.** Sol reviews and Terra's checkpoint and resumed turns ran through the lane's route, their logs committed in the lane; WI-850's scope critique spooled from the detached checkout.

## Context

Review-churn item 8, proposal step 1, with the two settlements revision 36
assigns to this spec (queue row P2, first half). The usage half is WI-961.

**Today.** `session_service.py` says it is "the one path every model call
takes", but in the coordinator cycle only the adjudicator takes it
(`coordinator_adjudicate._call` -> `session_service.call`). Sol (reviews,
scope critiques, plan critiques) and Terra (spine authoring) launch through
`scripts/coordinator/sol_review.sh` and `terra_author.sh` straight to
`codex exec`, so none of their usage is recorded. Each wrapper reads the
worktree's HEAD (and, for Sol, `git status --porcelain`) before and after
the launch and exits 3 on any difference. Terra's resumed turns run by hand
(recipes §1, "Terra, resumed": `codex exec resume <id> ...`), the session id
copied into the lane's decisions.

**Why the check moves inside the call.** `session_service.record` writes the
session log (`agent_common.write_session_log`) and commits it in the call's
root (`agent_common.commit_telemetry`). A recorded call therefore moves the
lane's HEAD itself; checked after `record`, every Sol call would read as the
model's edit (revision 32). The check runs where the model returns: after
`act`, before `record`.

**Settlement 1: a call outside a lane.** A scope critique runs from a
detached scratch checkout at the committed trunk tip (recipes §1, "Run each
critique from a detached scratch checkout"), several at once from one
checkout. Committed there, the log lands on a detached HEAD no branch
reaches; committed from the primary checkout it lands on trunk, which
`coordinator_adjudicate.lane_refusal` refuses the adjudicator for that
reason. **Ruling drafted here:** a call whose root is not a claimed lane
(the primary checkout, a detached HEAD, or a branch with no claim under
`docs/work/active/<branch>/`, the predicate `lane_refusal` already states)
writes its session log into the spool, `out/sessions/spool/` under the
primary checkout (`session_keep.primary_out_dir`), and commits nothing. A linked worktree whose branch has moved its claim out
under close-first while trunk's committed tree still holds it is a lane:
its final verdict round's REVIEW session log is the integrator's gate
evidence, which must commit on the branch. It
is the spool WI-788's design gives WI-800 (ch.2 §6; ch.4 §3, "Keep-warm and
trunk-rooted session logs"). This row builds only its write side; WI-800
keeps the harvest ("spooled logs land exactly once; a spooled entry is
deleted only once trunk's tree holds its log"). Until WI-800 lands, spooled
logs are complete but machine-local.

**Settlement 2: another call's log commit is not an edit.** Two calls on one
lane can overlap (a plan critique beside an adjudication; later, item 7's
second service-routed reviewer). One call's `record` commit moves HEAD under
the other's check. **Ruling drafted here:** of the plan's two options, the
check discounts session-log commits, because "both records after both
checks" cannot be arranged between independent processes. The discount is
narrow: a commit between the before and after HEAD is discounted only when
it adds standard-call session logs and touches nothing else. A standard-call
log is the name `session_service._call_row` gives (`call_<invocation-id>-
<stamp>.log`), which the verdict gate's session-log grammar
(`kitlib.verdict.SESSION_LOG_RE`) does not match. A commit that adds a
gate-grammar log, modifies or deletes any log, or touches any other path is
an edit. Uncommitted state is compared the same way: a standard-call log
present only after the call is not an edit, and neither is a standard-call
log present uncommitted at the call's first snapshot that a discounted
commit in the call's range adds (another call's log committed during this
call).

**Not in scope: the one writer.** `commit_telemetry` serializes nothing; two
`record`s in one worktree contend for git's index lock and the loser's log
is left uncommitted (revision 36). The serializing writer is WI-800's store.
This row makes the loss visible instead (Deliverable 4) and does not build a
writer. In today's workflows the overlap is rare: several critiques at once
run outside a lane (Settlement 1, so no commit), and a lane's REVIEW-B is a
Claude sub-agent that commits nothing.

**Anchor.** SN-026 (approved) through SR-222 (approved, derived): "record
every model session it launches ... in one usage record". Sol and Terra are
model sessions the kit's coordinator tooling launches and does not record.
SR-231's rationale (telemetry landing on trunk instead of the claimed work)
is the lens for Settlement 1. Its text binds only the adjudication entry
point, which this row leaves as it is. If the lane's spine author finds that
SR-222's "delivered loop content" does not reach coordinator-launched calls,
the lane drafts one derived SR under SN-026, labelled with its lens: "every
model session the coordinator's tooling launches is recorded in the usage
record, and a session started outside a claimed unit of work records its log
without committing to the shared line of development". It also drafts
LLR-269's amendment for the spool arm and the change check. All of it is in
capability voice: no file, module or path in a requirement cell (ruling 5).

## Deliverables

1. **A service route for the coordinator's codex calls.** One entry point
   builds a `session_service.Call` for a Sol review, a Sol critique (scope
   or plan) or a Terra turn, runs `session_service.act`, runs the change
   check (Deliverable 3), then `session_service.record`, and writes the
   call's final text to the out path the caller names, as `-o` does today.
   The model, family, tier and route id come from the enabled roster rows
   (`OPENAI-SOL`, `OPENAI-TERRA`), so SR-222's "provider filled from its
   roster row" holds. The launch keeps the wrappers' sandbox (unelevated,
   workspace-write, `--add-dir` on the review scratch root), effort and
   stdin prompt. Where that template lives is the lane's plan, from two
   options: declared rows or a declared template (see the calls below). The
   call's role is one of an enumerated set (`REVIEW-A`, `CRITIQUE`,
   `AUTHOR`). `sol_review.sh` and `terra_author.sh` become thin callers of
   it with their arguments unchanged, or retire with the recipes moved.
   `luna_review.sh` has no caller outside the plan history (grep), so it
   retires.
2. **Terra's resumed turn goes through the same route.** No hand-run
   `codex exec resume` survives in the recipes. The resume id is read from
   a recorded source: the lane's newest Terra (`AUTHOR`) session log's
   `session-id`, as committed at the lane's HEAD (chosen at filing; see
   Trust). It is never re-typed from the decisions record.
   `session_adapters.CodexAdapter.resume` already builds the resume form.
3. **The change check, between `act` and `record`.** It compares the root's
   HEAD and its status before the launch with the same after `act`:
   - **Sol (review, critique):** any change is an edit, except the discount
     (Settlement 2).
   - **Terra:** uncommitted changes are its output; only a HEAD move that
     the discount does not cover is an edit.
   - An edit is exit 3, the changed paths printed. The log is still recorded
     (the call happened); nothing is reverted, as today.
   - HEAD after not a descendant of HEAD before: an edit.
4. **The out-of-lane arm in `record`.** One rule for every caller, derived
   from the root, never selected by the caller: a claimed lane commits the
   log as today; any other root writes it to the spool and commits nothing.
   A `record` whose telemetry commit is refused (index lock, hook veto)
   reports it to its caller (`commit_telemetry` already returns the refusal
   text). The coordinator entry point then exits nonzero, naming the
   uncommitted log, never 0 with the log left dangling. The shipped
   `.gitignore` template ignores the spool directory (`out/sessions/`), as
   it names the loop's other runtime files under `out/`, so a spooled log
   never reads as an uncommitted change on an adopter's primary checkout,
   whose status the dispatcher's claims and keep-warm's records read.
5. **Text.** `coordinator-cycle` recipes §1 (Terra first turn and resumed;
   the review, critique and plan-critique launches; "note the session id
   line") and SKILL Roles, all three copies byte-identical
   (`.claude/`, `.agents/`, `project-trajectory/skills/`). The
   `scripts/coordinator/README.md` launcher list.
6. **Records.** IF-246's contract body (the spool arm of `record`; the
   change-check seam if it is the service's), LLR-269, and the lane's
   derived rows if drafted. One RESYNC entry: `record`'s new out-of-lane
   arm changes where a trunk-rooted call's log goes in an adopter's repo
   (keep-warm pings, which commit to trunk today, per WI-788 ch.4 §3, and
   any other call the loop roots outside a lane; the lane lists them by
   reading each caller's root).

## Trust

The change check is a gate: exit 3 tells the coordinator not to trust the
review or critique until inspected (recipes §1: "Exit 3 means the reviewer
changed the lane; inspect before trusting"). The discount gives a
session-log commit authority to pass that gate. The spool is a new carrier.
It is a gate input only once WI-800's harvest reads it, so WI-800 carries
its Trust. Written under [PROCESS.md §3, "When a guard is owed"](../../../../project-trajectory/PROCESS.md#3-traceability--anti-duplication).

- **Producer** of the discounted commits: `session_service.record` ->
  `agent_common.commit_telemetry`. It writes the subject `telemetry: session
  <id> ...` and commits `--only` the named log, so it never sweeps the
  index. Failed writes: no commit (index lock, hook veto, `held` refusal
  under the loop marker), with the log left uncommitted in the tree; or a
  log written and then the process killed before the commit.
- **Consumers** of session logs, found by grep (`docs/iteration`,
  `glob("*.log")`, `_PHASE_HEADER_RE`, `read_log_meta`):
  - `project-trajectory/scripts/kitlib/verdict.py`: `session_log`,
    `log_history`, `review_logs`, `logged_rounds` (the integrator's verdict
    gate, `integrate._verdict_gate`), keyed on `SESSION_LOG_RE`, which a
    `call_` log never matches;
  - `project-trajectory/scripts/agent_common.py`: `phase_draw_ordinal`
    (skips `call_` logs by name), `next_session_number` (its pattern needs a
    leading ordinal or train, so a `call_` name never matches),
    `draw_iter_dirs`;
  - `project-trajectory/scripts/agent_brief.py`: `last_build_family` (reads
    every log whose `# phase:` is `BUILD` or empty; this row's roles are
    neither);
  - `project-trajectory/scripts/plan_gate.py` (lists `docs/iteration/` as a
    record path);
  - the new change check (this row).
- **Ruling, at the change check:**
  - git cannot answer (HEAD, status or the commit listing unreadable):
    exit nonzero and print that the check could not run. Never 0.
  - A commit in the range that adds a standard-call log and nothing else:
    discounted. Anything else in the range (another path, a modification or
    deletion of a log, a gate-grammar log name, a merge): an edit.
  - Uncommitted: a standard-call log that is new after the call is
    discounted (another call's log written but not yet committed, or left
    after a lost commit). So is a standard-call log uncommitted at the
    first snapshot that is committed during the call, bound to a
    discounted commit in the observed range that adds that same path;
    its modification or deletion stays an edit. Every other change is an
    edit for Sol; for Terra, uncommitted changes are its output.
  - The discount binds to the call's own before and after HEAD and status,
    read in the root; never to a log's content.
- **The bound** (PROCESS.md §6, "Review threat model"): the promise covers
  the commits the kit's own routes make (`record`, the coordinator's
  commits). A model that writes and commits a log under a standard-call
  name hides only a record-path file. Such a log is not gate evidence: no
  consumer above reads a `call_` log as a round or a build. A hand-made
  commit under that name and sub-second races are outside the promise.
- **Ruling, at `record`'s out-of-lane arm:** a root whose lane-ness cannot
  be read (git's worktree records unreadable) is treated as not a lane. A
  claim read that is unreadable (the branch's tree or trunk's) adds no
  claim, so a root that neither readable tree shows claimed is not a lane:
  the log goes to the spool and nothing is committed. That is the direction
  that never writes to trunk, and a lane whose trunk side cannot be read
  (no trunk declared) still commits its gate evidence on its own branch. A spool directory that cannot be created or
  written raises, and the call is reported failed to record. The log is
  never dropped silently and never committed elsewhere.
- **Ruling, at Terra's resume reader** (Deliverable 2). The carrier is
  the lane's newest `AUTHOR` session log, which selects the thread a
  resumed turn continues:
  - **Producer and write route:** `session_service.record`, through
    `agent_common.write_session_log` into the lane's `docs/iteration/`
    and `agent_common.commit_telemetry`'s `--only` commit, at the end of
    each Terra turn this row's entry point runs.
  - **Failed writes:** no log (the call failed before `record`); a log
    written but left uncommitted (the lost-commit arm of Deliverable 4,
    whose nonzero exit names it); a log killed mid-write.
  - **Reader:** this row's coordinator entry point (Deliverable 1), its
    resume arm only, reading the lane's committed logs at HEAD (`git
    show HEAD:<path>`), never the working tree.
  - **Binding:** the log's branch and role (`AUTHOR`) and its route id
    (the enabled Terra row) must equal the resumed call's.
  - **Ruling:** no `AUTHOR` log at HEAD, an unreadable or unparseable
    one, one with no `session-id`, or one bound to another branch or
    route refuses the resumed turn before launch, naming the log and
    the cause; an uncommitted newer log is refused too, naming it, so
    the coordinator commits it first. The reader never starts a fresh
    thread in its place and never reads an id typed into the decisions
    record.

## Done-when

Each named test fails on the code before the change.
- **A recorded Sol call from a claimed lane.** A stand-in codex runner
  through the entry point: one telemetry commit adds a `call_` log carrying
  the codex usage columns and the roster row's provider; the out path holds
  the final text; exit 0.
- **An edit.** The stand-in commits a work file: exit 3, paths printed, log
  still recorded. The stand-in leaves an uncommitted work file: Sol exit 3;
  Terra exit 0 with the file left for the coordinator.
- **Another call's log commit.** During the stand-in's run, a second
  `record` in the same root commits a `call_` log: exit 0. The same with a
  commit that adds a gate-grammar log, modifies an existing log or touches
  a work path: exit 3. A second call's `call_` log already present,
  uncommitted, at the first snapshot and committed by its own `record`
  during the run: exit 0; the same log modified or deleted instead: exit 3.
- **Terra's resume carrier.** Absent, unreadable, malformed, or bound to
  another lane: the resumed turn is refused before launch, the cause
  named, and no fresh thread starts.
- **A rewritten history.** HEAD after is not a descendant of HEAD before:
  exit 3. Git unreadable during the check: nonzero, never 0.
- **Outside a lane.** From the primary checkout, a detached checkout and an
  unclaimed branch, the call writes its log under `out/sessions/spool/` of
  the primary checkout. No commit is made anywhere, HEAD and status of the
  root are unchanged, and the entry point prints the spool path. Several
  calls at once from one detached checkout each spool their own log.
- **A lost commit.** A `record` whose telemetry commit is refused: the entry
  point exits nonzero naming the uncommitted log.
- **Terra resumed.** A second Terra turn in one lane resumes the first
  turn's codex thread through the service, its id read from the recorded
  source, and its log records `session-mode = resumed`.
- **The blackout window** (`agent_common.blackout_at`): a Sol or Terra call
  inside a configured window is refused before launch, as every
  non-adjudication call is (`session_service.launch_refusal`). The
  coordinator recipes say so. (This repo's window is empty today.)
- No recipe or skill text launches `codex exec` for Sol or Terra outside the
  entry point. The three skill copies are byte-identical.
- One live Sol call and one live Terra turn have run through the route,
  their logs committed in a lane. One live scope critique has spooled from
  the detached checkout.
- On the landing tip, the commit bar is green, `check_trajectory.py
  --strict` and `trace.py --strict` are clean, the amended and derived rows
  are judged at the lane's sitting, and the RESYNC entry anchors at the
  landing's parent.

## Calls decided at filing

A headless leg filed this row, so its filing calls are the coordinator's
delegated decisions, for the owner to confirm or overrule
(`docs/decisions/coordinator-2026-10-20.toml#D-005`, high risk). The drafted
text above carries them:

- **C1 (Settlement 1):** a call outside a claimed lane spools its log and
  commits nothing, WI-788's decided design (ch.2 §6; ch.4 §3), not refused
  (critiques could not run from trunk) and not committed on trunk.
- **C2 (Settlement 2):** the check discounts standard-call log commits; the
  records cannot be ordered after both checks between independent
  processes.
- **C3:** `record`'s out-of-lane arm is one rule for every caller, derived
  from the root (WI-788 ch.4 §3), not an arm the coordinator's entry point
  selects.
- **C4 (the lane's plan):** where the coordinator's codex launch template
  lives, declared roster rows or a template the entry point declares. A row
  added to `docs/agents-enabled`, the consent surface, is the owner's, so a
  plan that needs one takes it to the owner before the build.

## Scope answers

- **S1.** Two independently landable deliverables in item 8. This row is the
  first and lands first; WI-961 (sub-agent usage) needs its out-of-lane arm.
  Within this row, the change check, the discount and the spool arm are not
  separable: routing a call through `record` without the check reads every
  call as an edit, and routing a scope critique without the spool arm
  commits on a detached HEAD. Terra's resumed turn rides with its first
  turn so no hand path survives (owner rule: no fallback paths). The spool's
  harvest stays WI-800's.
- **S2.** `## Trust` (the change check and its discount). The spool is a
  carrier whose consumer, the harvest, is WI-800's.
- **S3.** Closed: the role set (`REVIEW-A`, `CRITIQUE`, `AUTHOR`); the root
  is a claimed lane or not, with not readable read as not a lane; the
  commit range is discounted only for an enumerated shape (adds
  standard-call logs only), everything else an edit; deny by default.
- **S4.** `single`: a Trust section, three script families
  (`session_service.py`, the coordinator entry point, the recipes) and a
  promise over the commit-range input space.
- **S5.** A new state for a call (recorded but not committed: spooled), a
  new carrier (the spool, its write side), and a new input to the change
  check (the commit range's shape). It crosses one boundary: the
  coordinator's tooling into the shipped service. No component change.
- **S6.** `~WI-957`: claimed now. It rewrites the same SKILL §3 and recipes
  §1 review steps this row edits, so this row is built after it lands to
  avoid a text conflict; nothing in its construction is needed. WI-800 is
  not needed: this row builds the spool's write side ahead of it, and
  WI-800 gains this row as a hard edge (NOTES). WI-798 (account homes) is
  complete. No new dependency.
- **B3.** The check trusts the commit's own paths and name in the call's
  range, as the commit that made them recorded them. It reads no history
  beyond the call's own range.
- **B4.** No owner act in the Done-when. The live calls run on the box's
  existing codex login, as the wrappers do today.
- **Machinery landing alone** (revision 37). From its landing every Sol
  review, critique and Terra turn runs through the new route, this lane's
  own later rounds included. It lands alone, and the next mechanism change
  lands only after a cycle has run through it. A defect is fixed forward in
  a lane with a regression test. Where the defect blocks the fix's own
  review, that one launch runs by hand, attended and recorded.

## Critique dispositions

Scope critique round 1 (Codex Sol, medium, 2026-10-20; CHANGES-REQUESTED,
findings=2):

- **MAJOR, S3 (another call's log, uncommitted at the first snapshot,
  committed during this call, read as an edit): adopted.** Settlement 2 now
  reads "neither is a standard-call log present uncommitted at the call's
  first snapshot that a discounted commit in the call's range adds", Trust's
  uncommitted ruling reads "So is a standard-call log uncommitted at the
  first snapshot that is committed during the call, bound to a discounted
  commit in the observed range that adds that same path; its modification
  or deletion stays an edit", and Done-when's "Another call's log commit"
  gains that case (exit 0) and its modified or deleted variant (exit 3).
- **MINOR, S2 (Terra's resume carrier is an unlisted consumer): adopted.**
  Trust gains "Ruling, at Terra's resume reader": the plan records the
  chosen carrier's producer, write route, reader by path, lane and route
  binding and failed-write shape before the build, and an absent,
  unreadable, failed, malformed or foreign carrier refuses the resumed turn
  before launch; Done-when gains "Terra's resume carrier".

Confirming round (Codex Sol, medium, convergence stance, 2026-10-20;
CHANGES-REQUESTED, findings=1): the MAJOR's adoption is confirmed. The
MINOR's confirmation failed and keeps its severity (the carrier was still
left to the plan), so it is answered here with no further round (owner,
2026-10-14): the carrier is chosen at filing. Deliverable 2 now reads "the
lane's newest Terra (`AUTHOR`) session log's `session-id`, as committed at
the lane's HEAD", and Trust's "Ruling, at Terra's resume reader" states its
producer and write route, its failed writes, its reader (the entry point's
resume arm, reading committed logs at HEAD), its binding (branch, role and
route id) and the refusal for each bad input.

Plan amendment (the plan's P0, 2026-10-22, before the tests): the plan
critique's F1 is confirmed. Read literally, Settlement 1's "a branch with
no claim under `docs/work/active/<branch>/`" makes every loop lane that
closed first (its claim moved out on the branch while trunk's committed
tree still holds it) a non-lane at its final verdict round, so that
round's REVIEW session log, the integrator's gate evidence, would go to
the spool and every loop lane's merge would be refused. Settlement 1 now
names that worktree a lane, and Trust's out-of-lane ruling adds that any
unreadable claim read decides "not a lane". Done-when is unchanged, and
D7's three spool cases stand as written.

Confirming round of the plan amendment (Codex Sol, medium, convergence
stance, 2026-10-22): APPROVE, findings=0. The build proceeds from P1.

Lane amendment (wi-960 D-006, 2026-10-22, outside the Done-when): P3's
build found that the shipped `.gitignore` template does not ignore the
spool, so a stock scaffold's first spooled log dirties its primary
checkout. Deliverable 4 now states the template line; the lane adds it with
a regression test, and the RESYNC entry tells adopters to add it.

Lane amendment (wi-960 D-009, 2026-10-22, outside the Done-when): round 1
found that Trust's out-of-lane ruling, read literally ("whose claim read is
unreadable"), would spool every claimed lane's gate log where no trunk is
declared, while the plan's decision 3 and the code read an unreadable claim
read as adding no claim. The ruling now states that rule.
