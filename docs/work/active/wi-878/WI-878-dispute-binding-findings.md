+++
id = "WI-878"
title = "A dispute sitting's binding records the findings file it ruled, and the coverage gate reads exactly that file"
workstream = "process"
sr_refs = ["SR-236"]
specref = "project-trajectory/scripts/plan_coverage.py"
buildtier = "medium"
safety_class = "ordinary"
planmode = "single"
priority = 4
+++

## Context

Filed by the coordinator on 2026-10-09 (overnight leg 02) from WI-853's dispute sitting `docs/reviews/wi-853-findings-gate-in-rework/006-ADJUDICATE-349bb13.md`, which ruled Sol's last-gate finding DISMISS not-worth-cost for WI-853 and named this follow-up (`docs/decisions/wi-853.toml` D-006).

`plan_coverage.py` lets an `F#` exclusion that cites an accepted dispute DISMISS resolve the finding only when the ruled finding is shown to be the excluded one. Nothing records which findings file a dispute verdict ruled: the `.requested` binding beside the verdict holds only the brief class, the requested ids and the outcome. So the gate reads every findings file beside the verdict whose ids match the requested ids, and requires all of them to record the excluded finding's text. That fails closed: when two dispute rounds in one lane reuse finding ids (F1, F2) for different findings, a valid cited dismissal is refused (reproduced by Sol at `9cbf1a59`, exit 1). Until this lands, a lane's dispute findings use ids unique within the lane, or the plan excludes the finding with an uncited reason.

## Done-when

- The sitting's binding (written by the entry point at reservation, out of the adjudicator's reach) records the findings file the dispute brief was composed over, and the coverage gate reads exactly that file to show correspondence; it no longer scans sibling files.
- A binding without that record (every dispute bound before this change) refuses the citation by name; the gate reads no other findings file for it.
- Tests, red first: two dispute rounds in one lane reusing ids, each dismissal cited for its own round's finding, both pass; a citation of round 1's verdict for round 2's same-id finding still refuses; the existing correspondence and refusal cases still hold.
- The rows the change makes untrue are amended in the lane and judged in one combined sitting: SR-232/LLR-310 (the binding), SR-234/LLR-314/LLR-315 (the dispute grammar and brief), LLR-069/TC-069 (the gate), and the contracts of IF-287 (the binding) and IF-290 (the dispute grammar).
- RESYNC_PACK: an entry anchored at a trunk commit (shipped scripts change).

## Trust

The binding beside a dispute verdict gains authority over the coverage gate:
the findings file it records is the one file the gate reads to show that a
cited DISMISS or SUCCESSOR ruled the review finding it excludes. Both
carriers are files on disk, and a person or a model writes the findings file
as well as a kit script, so the guard follows
`project-trajectory/PROCESS.md` §3, "When a guard is owed", and the promise
is bounded as §6, "Review threat model", bounds a spec's promise.

**Producer:**

- *The findings file.* The coordinator writes it by hand before the
  sitting, in the shape `project-trajectory/scripts/kitlib/dispute.py`
  declares (the coordinator-cycle skill's dispute-sitting recipe), or, at
  the plan cap, `project-trajectory/scripts/review_brief.py plan-file
  --dispute-findings` writes it from the committed second critique. The
  coordinator commits it and keeps it after the sitting. On failure: a
  hand-written file that does not read in the declared shape refuses the
  brief's composition (`adjudicate_brief.dispute_values`), so no brief,
  sitting or binding follows; the kit writer reads its body back before
  writing, never writes over an existing file, and writes nothing when it
  refuses; a file left uncommitted is absent from every committed-tree
  reading below.
- *The binding's findings-file record.* The one binding writer
  (`kitlib.sitting.write_binding`, called through
  `adjudicate_brief.bind_pending`) records the repo-relative path the
  dispute row's `Adjudicates` cell names: the file `dispute_values` read
  when it composed the brief. It writes before the call, on two routes: the
  coordinator's entry point
  (`project-trajectory/scripts/coordinator_adjudicate.py adjudicate`,
  `bind_requested`) exclusively at reservation, and the loop
  (`agent_loop.session_body`) at composition; no kit route mints a dispute
  row for the loop today. The entry point is handed only the composed brief
  file, so the record reaches the writer on the brief, as the requested ids
  do; that is the dispute grammar and brief change the Done-when's row list
  names. After the call, `adjudicate_brief.record_outcome` rewrites the
  binding with its outcome through the same writer, carries the record
  through unchanged, as it carries the identity cell, and commits the
  binding in its own telemetry commit. On failure:
  - a reservation write that raises refuses the call before its launch
    (exit 2) and releases the reservation, so no binding exists;
  - a brief that carries no record (one composed before this change) binds
    without one, which every consumer reads as a record absent;
  - a failed or timed-out call is recorded `failed`;
  - an outcome rewrite that raises leaves the binding `pending`, or
    unreadable, which reads as no dispute binding;
  - the telemetry commit is best-effort: a hook's refusal leaves the
    recorded binding in the working tree only, and a committed-tree reading
    then finds no binding.

**Consumers** (found by grep over `project-trajectory/scripts/` and
`scripts/coordinator/` for `requested_path`, `REQUESTED_SUFFIX`,
`read_requested`, `accepted_at` and `read_findings`; `scripts/coordinator/`
reads neither carrier, and its `compose_lane.py` only calls the brief's
assembler):

- `project-trajectory/scripts/plan_coverage.py` `ruling_problem`, the one
  reader the record gives authority to, reads the verdict, its binding and
  the recorded findings file in one reading, on two routes:
  - the coverage gate's command line (`resolution_findings`, from
    `_check_one`), which the coordinator runs before it dispatches a fix:
    the working tree under `--root`. `review_brief.coverage_run` runs the
    same command over plan bytes taken from a commit, but with `--root` the
    lane, so the cited verdict, binding and findings file are still read
    from the working tree;
  - `project-trajectory/scripts/review_brief.py` `_ruled_findings`, inside
    `pass_fields` (`plan-file --pass --dispute`): the committed tree at
    HEAD.
- `project-trajectory/scripts/plan_gate.py` `_dismissals` (the pass-record
  check, run by the pre-commit hook, the landing check in `integrate.py`
  and `pass_fields`) reads the binding's class, ids and outcome at a commit
  and never the findings file: the filing step showed the correspondence
  once. It is unchanged, so a pass record filed before this change still
  passes the landing walk.
- `project-trajectory/scripts/adjudicate_brief.py`: `bound_kinds` and
  `record_outcome` read the binding in the working tree to rewrite it, and
  `dispute_values` reads the findings file in the working tree to compose
  the brief (both producer steps above).
- Unchanged readers, each at a commit or the index: `kitlib/sitting.py`
  `accepted`, `accepted_at`, `accepted_identities`, `branch_verdicts`,
  `uncovered_refusal` and `unaccepted_refusal` (reached from
  `acceptance_record.py` at the merge), `held_status.py`,
  `kitlib/done_when.py` and `adjudicate_act.py`, all under
  `project-trajectory/scripts/`. A dispute binding grants nothing there: its
  class has no sitting grammar, so `accepted` reads it as no blessing, and
  `adjudicate_act` refuses a class that owes no act. `read_requested`
  ignores a cell it does not know, so the record changes none of them.

**Ruling** (one ruling, which `ruling_problem` applies on both its routes;
the plan gate keeps its own check):

- *Binding absent, not a dispute binding, or outcome `pending` or
  `failed`:* refused by name, as today, before any findings file is read.
- *Record present, and the recorded file reads in the declared shape and
  records the ruled id with this review's finding text* (compared as the
  gate compares a hand copy today): the citation resolves when the ruling
  is one its consumer accepts, DISMISS or SUCCESSOR on the rework path and
  DISMISS at the plan cap.
- *Record present, and the file is missing at that reading, unreadable or
  not in the declared shape, does not record the ruled id, or records
  another text under it:* refused by name. No other file is read.
- *Record absent* (every binding written before this change, and one bound
  from a brief that carried none): refused by name. No sibling file is
  read; the remedy is to re-sit the dispute through a route that records
  the file, or to exclude the finding with an uncited reason.

The authority binds to the recorded path, as written at reservation, read
in the same reading as the verdict and its binding: never to the verdict's
directory, and never to another file whose ids match.

*The supported-workflow bound.* The ruling reaches the bindings
`bind_pending` and `record_outcome` write on either route, and the findings
files the coordinator's recipe and `review_brief.py plan-file
--dispute-findings` write, one per sitting, committed as written. Outside
it, with no guard: a hand-edited binding (a file a kit script writes); a
hand-chosen alias for the findings file's path (another case, a `./` or
`..` segment, a trailing dot), which the gate reads as the recorded string
and which the two readings may resolve differently; a findings file
rewritten in place after its sitting, a hand edit of the record the sitting
ruled; and sub-second timing windows, such as a file changed between
composition and reservation.

## Critique dispositions

Scope critique round 1 (Codex Sol, medium, 2026-10-24; CHANGES-REQUESTED,
findings=3):

- **MAJOR, S2/S3 (no Trust section): adopted.** A `## Trust` section now
  follows the Done-when and links `project-trajectory/PROCESS.md` §3, "When
  a guard is owed", and §6, "Review threat model". Its Producer names each
  carrier's writer, route and failed write: the findings file ("The
  coordinator writes it by hand before the sitting", or
  "`project-trajectory/scripts/review_brief.py plan-file
  --dispute-findings` writes it from the committed second critique"), and
  the record ("The one binding writer ... records the
  repo-relative path the dispute row's `Adjudicates` cell names",
  "exclusively at reservation" and "at composition", which `record_outcome`
  "carries ... through unchanged"). Its Consumers list each reader by path
  with its reading, the coverage gate's two routes included ("the working
  tree under `--root`", "the committed tree at HEAD") and the plan gate
  ("at a commit and never the findings file"). Its Ruling is one ruling
  over the pending and failed outcomes, a record present and recording the
  finding, a record present and not recording it, and a record absent; it
  binds the authority to "the recorded path, as written at reservation",
  and states the bound: "a hand-edited binding", "a hand-chosen alias for
  the findings file's path" and "sub-second timing windows" lie outside it,
  "with no guard". It adds no mechanism the Done-when does not already
  promise.
- **MINOR, S4 (planmode unstated): adopted.** The frontmatter now carries
  `planmode = "single"`: the row has a `## Trust` section, crosses script
  families and interface seams (the binding writer in `adjudicate_brief.py`
  and `kitlib/sitting.py`, the dispute grammar's seam IF-290, and the gate
  in `plan_coverage.py`), and promises behaviour over the binding's input
  states. It adds a code path, so the deletion exception does not apply.
- **MINOR, S1 (producer and consumer bundled): adopted, kept together.** The
  binding's record (the producer) and the gate's read of exactly that file
  (the consumer) stay one deliverable set in the Done-when's first bullet,
  and this is the row's recorded keep-together decision: the producer alone
  is read by nothing, since the gate would still scan sibling files; the
  consumer alone refuses every binding, since none would carry the record
  and every cited dismissal would refuse; neither lands a behaviour by
  itself. Inside the lane the red tests land first, then the producer, then
  the consumer, and the lane lands as one change.

Done-when edits at this revision: the second bullet now states the
refusal the Trust ruling gives a binding without the record (it read
"fails closed, as today", while today's sibling scan can pass one); the
row list adds LLR-314 and IF-287, the dispute grammar's request line and
the binding's grammar that the record rides; and the stale "Review bar:
A" line is dropped, since ruling 4 runs two full-lane reviewers per
round.
