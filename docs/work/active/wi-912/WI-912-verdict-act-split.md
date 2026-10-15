+++
id = "WI-912"
title = "An adjudication sitting ends at its committed verdict, and its act is a later adjudicator turn taken from that verdict"
workstream = "process"
sr_refs = ["SR-231", "SR-146", "SR-232", "SR-209"]
specref = "docs/plans/2026-10-11-review-churn/README.md#16-one-mint-across-parallel-lanes"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = ["~WI-911", "~WI-913"]
+++

## Context

Filed on trunk on 2026-10-14 by the attended coordinator as the second half
of the review-churn batch row B1, split from WI-911 at filing under S1
(coordinator-2026-10-14 D-002). The spec of record is the plan's item 16 as
the owner ruled it: verdicts move between lanes while acts keep landing order
(revision 31); the split reaches the shipped sitting briefs (revision 32) and
the coordinator's entry point (revision 36); and, from the revision 36 ruling
on headless legs, the briefs carry the `Loop-Session` line (the handoff's P9
carries the rest of the marking). Where this row and a ruling differ, the
ruling governs.

Today the brief that asks for a judgement also orders the act, in the same
turn. The act is the `Status` flips and the anchoring copy (`intake.py
snapshot --approves` or `--reattests`, with `--verdict` for a held-rung
CLARITY row), committed after the verdict with the text first (WI-806), and
admitted at the merge only when an accepted verdict over the act's own rows
backs it (`integrate._approval_act_refusal`, owner ruling 6, 2026-10-07). The
first-approval brief says "Stop only after that approval commit is recorded";
the amendment and combined briefs take each act after the verdict commit; the
composer's released arm and held-CLARITY arm say the re-attestation is taken
"BY YOU". And `coordinator_adjudicate.py` runs only a fresh judgement. So a
sitting held ahead of landing order that follows its brief takes its act out
of order.

The row hangs from SR-231 (the coordinator's adjudication entry point),
SR-146 (prompts as reviewable files), SR-232 (combined sittings and the one
accepted-verdict reader) and SR-209 (the loop provenance trailer), all
Approved. SR-231 admits only a fresh judgement ("a valid claimed lane
exclusively reserves a new verdict path"), so the lane amends it, with the
rows beneath that it changes (LLR-306 and LLR-167 at least; TC-321 and
TC-161) and IF-283, IF-284 and IF-285.

## Deliverables

One lane, one landing. Each item names its ruling, and the builder writes the
rule in the target's own voice. Q1 to Q4 are answered in Scope answers.

1. **The sitting briefs judge only** (shipped, RESYNC entry):
   `project-trajectory/prompts/adjudicate-first-approval.template.md`,
   `adjudicate-amendment.template.md` and `adjudicate-combined.template.md`,
   and in `project-trajectory/scripts/adjudicate_brief.py` the composer's two
   acting arms (`_RELEASED_AFTERMATH`, and `_HELD_ARMS["reattest"]`, the arm
   `intake.adjudication_action` selects for a held CLARITY verdict). The
   judging turn writes and commits only its verdict, with its `WI:` trailer as
   today, and is told that its act is a later turn taken from that verdict.
   The verdict records what the act needs: each row's ruling and, for a
   MEANING row on a released rung, whether the adjudicator blesses its new
   text (Q2). The act instructions (the flips, the `intake.py snapshot` forms
   and their quoting, stopping on a snapshot refusal, the combined order) move
   to the act brief, their one home, together with the first-approval brief's
   `{registries}` and `{approves_rows}` slots. A held MEANING row and a held
   first draft still stop for the human-or-delegate, as today.
2. **The act brief** (shipped, RESYNC entry): a new template beside the
   sitting briefs, with its prompt key, its bootstrap manifest row and its
   catalogue line, and an assembler (Q1). The assembler reads the named
   verdict and its binding at the lane's HEAD through
   `kitlib.sitting.accepted_at` and lists every act the verdict authorizes
   that HEAD's committed tree does not yet carry in full (Scope answers, S3,
   "Re-runs"): rows ruled APPROVE are flipped, with
   `--approves` naming only their registries; rows ruled CLARITY, and MEANING
   rows the verdict blesses on a released rung, are re-attested, with
   `--verdict` on a held rung. The amendment act comes first, then the
   first-approval act, each in its own commit, text first. It is all or
   nothing, as the module's rule 2 states. `adjudicate_brief.py` stands at
   932 of the size ratchet's 1000 SLOC, so the assembler takes its own
   module unless moving the act text out of the judging assemblers offsets
   it.
3. **The act turn** (shipped, RESYNC entry): in
   `project-trajectory/scripts/coordinator_adjudicate.py`, a command beside
   `adjudicate` that takes the committed verdict's path and the work item
   (Q1). It runs only from a claimed lane, as `adjudicate` does. Before the
   launch it refuses (exit 2), naming why, a verdict that is not accepted at
   HEAD or that owes no act. It reserves no verdict path, writes no binding
   and grades no verdict. It launches the act brief on the retained session
   where the `[adjudicator]` dial retains the verdict's class, and on a fresh
   session otherwise. It exits 0 only when the call succeeded, the
   assembler's derivation finds no listed act still owed, and the call wrote
   nothing under `docs/reviews/`. IF-283, IF-284 and IF-285 state the
   command, its exits and its readings.
4. **The trailer line** (shipped, RESYNC entry): under the loop marker,
   every prompt the entry point launches (both turns, every class) ends with
   the `Loop-Session` instruction the loop's sessions already get,
   `agent_brief.loop_provenance_note` (Q4). Without the marker, nothing is
   added. P9 sets the marker for headless legs and carries the rest.
5. **`project-trajectory/PROCESS_OPTIONS.md`, "Who performs the approval
   act"** (shipped, RESYNC entry): the amendment row's "followed by its own
   re-attestation in the same session" becomes the later act turn, taken
   from the committed verdict. The file is byte-watched: report the delta
   with `byte-budget-guard`.
6. **The `coordinator-cycle` skill** (kit source
   `project-trajectory/skills/coordinator-cycle/`, synced to
   `.claude/skills/`; `scope: this-repo`, so no RESYNC entry). §4 states the
   split. A lane's verdicts may be sat at any time, for any lane. Its acts
   keep landing order: the act turn runs only after the lanes ahead have
   landed and the lane has rebased, and lanes that take acts land one at a
   time. Before the act turn, the coordinator checks that the judged rows are
   unchanged since the verdict judged them (the rows at the verdict's own
   commit before the rebase, against the rebased tip; a renumbered row counts
   as changed), and re-sits any that changed. That is today's §4 rule stated
   as the act's precondition, text only (revision 32). §3's checkpoint
   sitting ends at its verdict. The recipes give the act turn's command and
   the precondition's check, and replace §1's "the adjudicator commits its
   verdict and its act" and §3's stash-and-commit steps for the act.

## Trust

Written before the claim, answering S2 under `project-trajectory/PROCESS.md`
§3, "When a guard is owed". The ruling goes to the owner to confirm or
overrule (coordinator-cycle §1 and §5).

**The carrier.** A judging turn's committed verdict
(`docs/reviews/<lane>/NNN-ADJUDICATE-<sha7>.md`) and the binding beside it
(`<verdict>.requested`: brief class, requested kinds, outcome), read together
at the act turn's HEAD through `kitlib.sitting.accepted_at`, the one reader
every consumer goes through. Today the act rides the judging turn. After this
row the committed verdict is the act turn's whole authority: the session that
wrote it may have been retired, and a fresh act turn takes the same act.

**Producer and write route.** The judging turn, an adjudicator session that
`coordinator_adjudicate.py adjudicate` launches from the lane (or the loop's
`agent_loop.session_body`). Before the launch the entry point reserves the
verdict path exclusively and writes the binding exclusively, with the outcome
`pending`. The session writes the verdict into the reservation and commits it
with `WI: <id>` (and `Loop-Session` under the marker). Then
`adjudicate_brief.record_outcome` validates it against the bound kinds and
rewrites the binding as `accepted` or `failed`, committed through
`agent_common.commit_telemetry`. Failed writes: a failed, timed-out or
error-reporting call is recorded `failed`, and its verdict is not read; an
empty reservation, or a verdict outside its grammar, is recorded `failed`; a
verdict left uncommitted, or a binding commit that is refused, leaves HEAD
without an accepted pair. A committed file cannot be half-written, only
malformed.

**What the authority binds to.** The verdict and its binding as committed in
the lane at the act turn's HEAD, after the rebase. The act covers exactly the
rows each accepted part rules: APPROVE flips; CLARITY re-attests, naming the
verdict on a held rung; MEANING re-attests only on a released rung and only
with the verdict's bless mark. A RETURN row, a held MEANING row, a Done-when
part and every other brief class owe no act. The rung is read from the dial
at the act, and the merge slot re-reads it at trunk. The act turn writes no
verdict and no binding, so nothing it writes can be read as an accepted
verdict: only the route's `record_outcome` writes `accepted`, the act turn
does not call it, and a call that writes under `docs/reviews/` fails. The act
turn checks neither landing order nor whether the judged rows changed since
the verdict: both are the coordinator's precondition (§4), as revision 32
ruled. The binding records no digest of the verdict text, so a later edit to
a committed verdict's row lines is read as the verdict; that is the merge
slot's bound today, unchanged here.

**Consumers and rulings** (grep over `project-trajectory/scripts` for
`accepted_at`, `uncovered_refusal`, `unaccepted_refusal`, `verdict_rulings`,
`read_requested` and the act ledger's `verdict` field):

- **The act turn**, `coordinator_adjudicate.py` (new). A verdict that is
  absent at HEAD, unreadable, unaccepted (no binding, or `pending`, or
  `failed`) or malformed, or one that owes no act, is refused before the
  launch (exit 2), naming why. So is a lane with uncommitted changes (naming
  the paths), and a row whose act evidence at HEAD is inconsistent (S3,
  "Re-runs"; naming the row). Nothing is launched, reserved or written.
- **The act brief's assembler** (new). It uses the same reader, and any of
  those inputs returns `(None, reason)`, never a partial brief.
- **The merge slot**, `integrate._approval_act_refusal` →
  `acceptance_record.merge_approval_refusal` (unchanged). Through
  `kitlib.sitting.uncovered_refusal`, every flipped or re-attested row must
  be judged by an accepted verdict among the branch's bindings. Through
  `kitlib.sitting.unaccepted_refusal`, a verdict that an act names must be
  accepted and must judge the rows the act re-attests. Through
  `acceptance_record.held_reattest_refusal`, a held-rung re-attestation needs
  CLARITY in that verdict. Each refuses the merge on any of these inputs,
  naming the act. The split moves no act out of the branch that carries its
  binding.
- **`intake.py snapshot --verdict`** (`baseline_snapshot._refuse_verdict` and
  `_record_act`; unchanged). It refuses a verdict that names no file in the
  tree, or that comes with no re-attested row, and records the path in
  `docs/archive/last_approved/acts.toml`. Acceptance stays the merge slot's
  question.
- **`gen_open_items.py`** (unchanged): it lists the acts that name a verdict,
  for audit.
- **Readers of verdicts that are not an act's authority** (unchanged):
  `kitlib/done_when.py` (the Done-when holds), `plan_coverage.py` (a
  dispute's binding), `intake.py` (a Done-when section's drafts), and
  `agent_loop.read_verdict` with `adjudication_bookkeeping` (the loop's own
  outcome).

## Done-when

- Every deliverable above is in its target, each citing the ruling it
  carries. No judging brief orders an act. WI-572's pin
  (`test_the_first_approval_brief_cannot_stop_before_its_approved_act`) is
  replaced by its successor: the act turn reports success only when no act
  its brief listed is left untaken.
- Each of these tests fails on the code before the change: a refusal for
  each input the Trust section names; a retained and a fresh act turn taking
  the same act from one verdict; a combined verdict's amendment act committed
  before its first-approval act; a mixed first-approval verdict whose
  `--approves` names only its approved rows' registries; a MEANING row
  without the bless mark left unacted; a call that stops short of a listed
  act, or writes under `docs/reviews/`, not reporting success; an act
  interrupted between its flip and its snapshot refused as a dirty lane, and
  re-run in full once the leftovers are discarded; a combined act
  interrupted between its two commits re-run with only its first-approval
  act listed; a flip committed without its copy refused, naming the row; a
  Drafted row already present unchanged in a whole-registry snapshot listed
  as owed;
  with the loop
  marker set, every prompt the entry point launches ending with the
  `Loop-Session` instruction, and none without it.
- The change's trace rows are authored and sat at the lane's checkpoint,
  SR-231's amendment and its act included. This lane's own checkpoint is sat
  in the new shape from the lane root: its judging turn, then its act turn
  after its rebase. The coordinator records that as a decision.
- The skill copy in `.claude/skills/` matches the kit source (`bootstrap.py
  --dest . --sync`), the prompt catalogue's `--check` passes, and
  `byte-budget-guard` reports `PROCESS_OPTIONS.md`'s delta.
- `RESYNC_PACK.md` carries one entry for the shipped changes (the three
  sitting briefs, the act brief, `adjudicate_brief.py`,
  `coordinator_adjudicate.py`, `PROCESS_OPTIONS.md`), with no forced
  migration. It states that the loop's route has no act turn yet, so its
  sittings end at their verdict (Q3).
- The build starts only after the plan gate (WI-913) has landed. The lane's
  plan is produced after the claim and passes that gate (S4).
- The bar is green on the landing tip: the smoke tier within its budget,
  `check_trajectory.py --strict` clean, and `trace.py --strict` with no
  finding beyond LLR-292's.

## Scope answers

- **S1:** one landable unit. The judge-only briefs cannot land without the
  act turn: a sitting would have no sanctioned way to take its act (revision
  36). The act turn has nothing to take until the briefs stop acting. The
  trailer line could land alone, but it is a few lines in the same launch
  and stays inert until P9 sets the marker, so it is kept here, as D-002
  records. The skill and `PROCESS_OPTIONS.md` text describe the split and
  ride with it.
- **S2:** yes. The committed verdict now authorizes the act turn's act; see
  `## Trust`.
- **S3:** closed by enumeration, with deny by default:
  - **The act turn's input.** An accepted verdict that still owes an act
    launches; every other state is refused before the launch (the Trust
    section's list).
  - **The acts.** Exactly the rows each accepted part rules to authorize
    them. A MEANING row without the bless mark owes none, and neither does
    any class other than amendment, first-approval and combined.
  - **Re-runs.** The assembler judges each authorized act at the lane's
    HEAD, in its committed tree, never the working tree, by the act the
    row's ruling authorizes. A first approval is owed while the row's
    committed status is below Approved, whatever its snapshot copy holds (a
    whole-registry copy carries Drafted rows), and taken when the row is
    Approved and its snapshot copy equals its committed text. A re-attest of
    an Approved row is taken when the copy equals the row's committed text,
    and owed otherwise. Any other state, such as an Approved row without an
    equal copy at a first approval, or a re-attest of a row below Approved,
    is inconsistent: it is refused before the launch, naming the row, and
    never counted as taken. The act turn also refuses a lane with
    uncommitted changes before the launch, naming the paths. So an act
    interrupted between its flip and its snapshot, which leaves the flip
    uncommitted, is refused until the coordinator discards the leftovers
    (recorded as a decision), and the re-run then lists the whole act. A
    combined act interrupted between its amendment commit and its
    first-approval commit is re-run with only the first-approval act
    listed. A re-run after a completed act owes none and is refused as
    such.
  - **The trailer.** One construction covers every prompt the entry point
    launches.
  - **Lanes in flight.** A lane in flight when this lands takes its next act
    through the act turn. A verdict sat before the landing whose act is
    still owed is re-sat, since it carries no bless marks. The coordinator
    records that as a decision.
- **S4:** `single`. The row has a Trust section, two script families (the
  sitting briefs with `adjudicate_brief.py`, and `coordinator_adjudicate.py`)
  and three interface seams (IF-283, IF-284, IF-285).
- **Architectural delta:** yes, carried within scope.
  - **A new state:** a lane holding an accepted verdict whose act is not yet
    taken, where today the judgement and the act share one turn.
  - **New domain values:** the entry point gains a command, the shipped
    briefs gain the act brief, and the amendment verdict gains the bless
    mark.
  - **A new input:** the act now depends on a committed, accepted verdict
    handed across sessions, not on the same turn's judgement.

  The Trust section and the IF amendments carry these, and no preparatory
  refactor is needed.
- **B3 and B4:** the act reads its decision from the verdict, the record
  written at the event, and re-derives nothing from history; the
  precondition's comparison is the coordinator's (§4). No Done-when item
  needs an owner act or credential: SR-231 sits on a rung this repo's dial
  releases.
- **Dependencies:**
  - **`needs` WI-911, soft.** It is claimed with the batch and built after
    WI-911 lands. Both rows edit the `coordinator-cycle` skill's §4
    and its recipes. WI-911 lands first, as the text every later lane runs
    under, and after the baseline manifest
    (`docs/plans/2026-10-11-review-churn/baseline/baseline-manifest.md`).
  - **The plan gate, WI-913,** is a soft edge and a Done-when hold, since
    the handoff lets a `single` row be claimed before the gate lands.
  - **A mechanism change:** this row lands alone, and the next mechanism
    lane waits until a sitting has run through the act turn once.
  - **No third-party dependency.**
  - **Later rows, not edges:** P9 builds on the trailer line. WI-801, which
    deletes `coordinator_adjudicate.py`, must carry the act turn into `ask`.
    WI-809 amends these briefs for the loop's in-lane sitting.
- **Calls answered at filing.** Q1, Q2 and Q4 are the coordinator's
  (coordinator-2026-10-14 D-003); Q3 is the owner's (2026-10-14, in session).
  - **Q1, the act turn's form:** an adjudicator turn with its own act brief,
    composed by the `act` command from the committed verdict (revision 32's
    "a later turn of the retained adjudicator", run fresh where retention
    lapsed; OI-45 (b) keeps scripted approval retired).
  - **Q2, the bless decision:** a typed mark on the verdict's row line, read
    by one reader in `kitlib.verdict`; an absent mark reads as not blessed.
  - **Q3, the loop's route (owner):** the loop's act turn is built in WI-809,
    whose Done-when now carries it. This row's RESYNC entry states the gap,
    and the managed loop stays paused until WI-809 lands.
  - **Q4, the trailer line's home:** the entry point appends
    `agent_brief.loop_provenance_note()` to every prompt it launches.

## Critique dispositions

Round 1 (Codex Sol, medium, 2026-10-14; one finding):

- **S3, MAJOR: adopted, with one change to the remedy.** A partial act is
  reachable in normal use: a turn can stop between its flip and its
  snapshot, or between a combined act's two commits. The Re-runs answer now
  states one completion contract, judged at HEAD: "an APPROVE is taken when
  HEAD carries both the Approved status and a snapshot copy equal to the
  row's committed text, and owed when HEAD carries neither ... Any other
  combination, such as a flip committed without its copy, is inconsistent:
  it is refused before the launch, naming the row, and never counted as
  taken." The critic asked for a flip-only state to be resumed; it is
  refused instead, because a resume path would serve a state the commit
  hook's integrity floor may already exclude, and a refusal fails closed
  either way. The reachable flip-only state is uncommitted, and "the act
  turn also refuses a lane with uncommitted changes". Deliverable 2 reads
  acts from "HEAD's committed tree", the Trust section's act-turn ruling
  carries both refusals, and the Done-when's tests include each recovery
  case (coordinator-2026-10-14 D-008).

Round 2 (Codex Sol, medium, 2026-10-14, the first confirming round; one
finding):

- **S3, MAJOR: adopted.** Round 1's partition refused an ordinary unacted
  row: a whole-registry snapshot carries Drafted rows, so a Drafted row with
  an equal copy is owed, not inconsistent. The Re-runs answer is now
  status-aware: "A first approval is owed while the row's committed status
  is below Approved, whatever its snapshot copy holds ... A re-attest of an
  Approved row is taken when the copy equals the row's committed text, and
  owed otherwise." The Done-when's tests add "a Drafted row already present
  unchanged in a whole-registry snapshot listed as owed".
