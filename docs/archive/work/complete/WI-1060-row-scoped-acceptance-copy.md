+++
id = "WI-1060"
title = "An acceptance act's copy writes only the rows the act names, so one unblessed row no longer blocks its registry"
workstream = "process"
specref = ""
sr_refs = ["SR-179", "SR-207"]
needs = []
buildtier = "medium"
planmode = "single"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Built on the maintenance branch `maint/wi-1060`, cut from `refactor_again` at
`3db0c6823` and rebased onto it at `121ce2e00` (after WI-1059's merge) before
the build, with the commit hooks on, under the plan `docs/plans/WI-1060/plan.md`.
No status moved, no snapshot was taken on this repository and no id was minted
(every obligation landed in an amended row, so no `--bump-ids` run was owed).
No decisions record: every choice is stated by an amended row or by the plan
the coordinator approved.

**The approval, as the operator required for this row.** The coordinator read
and approved the plan on 2026-11-23, before any build: D1 (the traced-cell
rule C, and the Done-when wording committed with the plan), D2, D3, D5 to D13
as written, with four corrections. (1) D4 changed: an act that would write
nothing stays refused, with today's outcome and exit status, its message now
naming the rows that stay owed; only an act whose scope writes something no
longer refuses for drift, and LLR-245's and TC-240's text say so. (2) Rebase
the plan commit onto `refactor_again` after WI-1059's merge before building.
(3) Measure the hook's integrity step before and after, and stop if it grows by
more than about 10 seconds. (4) Record this approval here.

- `2428a1bf5`: the plan, with the traced-cell rule written into Done-when
  items 1 to 3 (rebased from `3d5967d79`).
- `2ded34460`: the red tests, under the declared expected-failure marker.
- `72f0a63ca`: the build: `record_rows.py`, the writer, the judges, the rows,
  the prose, the RESYNC entry, regenerated evidence and views.
- The commit after it: this close-out (the Deliverable, the move, the log
  fragment).

**`refresh_refusal`, under correction 1 (my choice, as the go-ahead allowed).**
Kept, under its name and signature, shrunk to the one arm that remains: it
answers `""` for any act whose scope writes a copy (a `seed` included) and,
for an act that would write nothing, the refusal listing every drifted row
and cell that stays owed, uncapped. `_unaccepted_rows` stays as its reader of
the owed rows; `_refusal_text` now words only that arm. The three tests that
pin the refusal (`test_a_ACCEPTED_amendment_with_no_flip_and_no_ref_is_REFUSED`,
`test_an_act_that_would_copy_NOTHING_is_REFUSED_rather_than_silent`,
`test_a_DEACCEPTANCE_cannot_authorise_an_unrelated_accepted_amendment`) are
unchanged and pass.

**1. An act writes only the rows it names, and a drifted row beside it no
longer refuses it.** A new module, `scripts/record_rows.py` (CMP-006), is the
one statement of what an act writes, read by the writer and the judge alike and
importing neither (the caller passes the cell comparison in). `row_rule`
classifies each row: a named row (its status moved into acceptance, it arrived
accepted, `--reaccepts` names it; a named row gone from live is retired) takes
live; an unnamed row follows live when its live text claims no acceptance (or,
gone from live, its copy claimed none), or when both sides claim acceptance and
neither its accepted cells nor its routed traced cells (`ROUTED_TRACED_CELLS`,
moved here from `intake.py`, which keeps the name as an alias) differ; every
other unnamed row keeps its recorded text; a template example row (`-000`)
follows live whatever its status. `row_segments` splits a registry
text into a head (every byte before the first row header), rows (each with its
leading blank and comment lines, header and cells) and a tail, refusing a text
that will not split into rows each reading alone as the row the file holds.
`expected_copy` returns the live text unchanged when nothing is kept (so the
seed, the repair and every act that keeps nothing write the live file byte for
byte), and otherwise composes live's head and tail, the rows in live order from
the side the rule names, and a kept row live no longer carries after the row it
followed; a legacy carrier (CSV, or the needs file's markdown) is copied only
whole, refused naming each row and its moved cells when one would be kept.
`baseline_snapshot.copy_live` writes through it: the summary line prints the
kept rows as `LEFT OWED`, the stamp line names them, and the act ledger entry
lists them in a new field, `kept` (`_record_act`; `acts_problems`,
`parse_acts` and `added_acts_problems` carry and judge it as they do `copied`).
A re-seed over a standing record reads its previous copy and is an act over
every registry, row by row.

**2. The writer re-reads its result and writes nothing unless it reads as the
rule.** `copy_live` composes every copy in memory (`_composed_copies`, through
`record_rows.act_copy`), re-reads each with `record_rows.row_problems`, a
parse-level reading independent of the composition, and refuses, writing no
copy, stamp or ledger entry, unless every row reads as the rule gives it; the
directory itself is created only after that.

**3. The checks judge a written record at the row.** `staged_snapshot_findings`
(the hook, through `trace.py --strict-integrity`, and `check_trajectory
--staged`) and `committed_snapshot_findings` (each copy's last writing commit
against its parent, on every integrity run) keep their names; once the record's
act ledger at the parent holds an entry carrying `kept`, or the commit adds
one, they compare each written copy byte for byte with `expected_copy` from the
parent's copy, the live file in the commit and the rows the entries the commit
adds name, a merge's entries brought in over the first parent included
(`record_rows.tree_acts` reads every ledger in one batch;
`record_rows.written_problems` reads the three blobs in one more), and name each
fault by its row (an unnamed row's drift carried in, a named row not equal to
live, a row dropped that no act retired) or name the bytes outside the rows.
Deleting `acts.toml` while the record stands is refused at the hook like
deleting a copy. Tests refuse each of the three attempts at the hook and, with
the hook skipped, on the committed history, plus an entry-less whole-file copy
in a row-by-row record.

**4. The drill's case.** One design registry with a blessed amendment (A,
re-accepted), an unblessed one (B) and a row ruled ACCEPT (C, its status
moved): the act records A and C from live, keeps B's recorded bytes, names B
as `LEFT OWED` and in `kept`, B reads drifted and A and C do not, and both
mirror rules read the act clean.

**5. The seed copies whole files, and existing records read clean.** The seed
writes the live files byte for byte (its entry carries `kept = []`). A record
whose ledger holds no entry carrying `kept` is judged as written,
byte-identical to live; so this repository's record, whose `external.toml`
and `stakeholder-needs.toml` copies were last written by the vocabulary
migrator's entry-less whole-file step, reads clean under `trace.py --strict`
and every hook run on this branch, and a test reads an old writer's record and
a migrator-shaped write clean while refusing the same write after a
row-by-row act.

**6. Rows, `Drafted` rule, RESYNC.** The fifteen accepted rows the plan named
are amended (text only; the code names they inherited scrubbed), listed below
as owed; no row was added, and IF-220 (Drafted) is rewritten. A RESYNC entry,
"An acceptance act records only the rows it names; a drifted row no longer
blocks its registry", tells adopters what changed and that no record needs
migration. The prose the change made false is restated: the shipped record
README template, `PROCESS.md` §4, `PROCESS_OPTIONS.md` ("Who performs the
acceptance act"), the act prompt, the coordinator-cycle and spine-authoring
skill references (and their per-agent copies), the registry machinery
reference, the snapshot command's help, the held-act operator item's
option (a), and the off-spine census note the acceptance brief and the
open-items page print (it said a re-seed "still blesses the whole tree").

**7. The unfiltered suite** is the coordinator's, on this branch before the
merge; left unticked.

**Deviations from the approved plan.**

- D4, as the coordinator corrected it (above), in place of the plan's "an act
  writing nothing exits 0".
- D3, refined: the first row carries no leading lines. Its leading run would
  otherwise swallow a comment-only preamble (the needs file's 100-line
  header), so the head is every byte before the first row header and only
  later rows lead with the blank and comment lines after the row before.
- D6, as built: a re-seed over a standing record reads its previous copy (the
  plan's "row by row like any act" needed the previous copy read whenever the
  prior record reads); only the seed and the repair of an unreadable record
  read none.
- The legacy-carrier refusal names each row and its moved cells (as today's
  refusal did), so TC-297's markdown-needs test passes unchanged.
- `kept`'s shape check is "a list of row ids", folded into the id-list check
  `accepted` and `reaccepted` share; the writer writes it sorted, and no rule
  judges its order. LLR-361 says so.
- Placement, for the size ratchet (both existing modules sit just under 1,000
  SLOC): more of the judge than planned lives in `record_rows`, injected with
  `acceptance_record`'s cell comparison and its reading of the entries a commit
  adds (`act_rows`, `tree_acts`, `written_problems`, `whole_file_faults`,
  `blob_texts`), so `acceptance_record.py` grows from 972 to 987 SLOC and
  `baseline_snapshot.py` from 980 to 994; the two mirror rules keep their names
  and `check_trajectory`'s re-exports, and `test_acceptance_record.py`'s import
  census gains `record_rows`. `intake.py`'s size baseline is re-stamped down
  (1,946 to 1,944).
- `test_intake_held_act.py::test_two_landings_widen_the_act_as_the_item_states`
  pinned today's behaviour too (each landing's own command refused, naming the
  other row); it becomes `test_two_landings_each_take_their_own_act`. The plan's
  table named only its option-text assertion.
- SR-179's acceptance had "on each later check of the committed history"
  flagged as an unbounded absolute by `trace.py`; it reads "again by the check
  of the committed history".
- The merge judgement, found while checking LLR-178's merge clause: at a
  merge the staged rule judges against the first parent alone, so the
  act-ledger entries the merge brings in name their rows and a merge carries
  the other side's act; naming rows only by entries no parent held would have
  read the other side's act as an unnamed row's drift. LLR-178 and TC-173 say
  so, and a test drives it.
- Template example rows (`-000`) follow live whatever their status: found by
  the wide run (below).

**The hook's integrity step, timed (correction 3).** On this repository, back
to back under the same load (other builders were running; one machine, one
reading each), `trace.py --root . --strict-integrity`, the command the hook's
registry-integrity step runs, three runs each:

- before, the scripts at `2ded34460`: 8.86 s, 9.02 s, 8.58 s
- after, the scripts of this branch: 10.65 s, 9.32 s, 9.56 s; again 9.53 s,
  9.33 s, 10.94 s

<!-- fig: cmd="pwsh: Measure-Command { python project-trajectory/scripts/trace.py --root . --strict-integrity } x3, the scripts stashed to 2ded34460 for the before runs" rev="72f0a63ca's tree, uncommitted, 2026-11-23" -->

About half a second to a second more, well inside the 10-second bound. This
repository's record holds no entry carrying `kept` yet, so every copy is still
judged as written, and the added cost is the one batched read of the act
ledgers. Once the first row-by-row act lands, every copy written after it is
judged at the row: forcing that judgement over every copy here, in process,
`committed_snapshot_findings` took 2.35 s and 2.74 s (and 15.30 s once, under
load) against 0.44 s to 0.50 s as written. Forced, it named six faults, all in
the two copies the vocabulary migrator last wrote with no act (`external.toml`
at `675f5b7a4`, `stakeholder-needs.toml` at `db12d3857`), which is why a copy
written before the first row-by-row act is judged as written.

<!-- fig: cmd="python -I <scratch>/time_row_rule.py . (committed_snapshot_findings x3 as written, then x3 with record_rows.act_rows forced to judge every copy row by row)" rev="72f0a63ca's tree, uncommitted, 2026-11-23" -->

**Tests run** (pytest under the worktree's venv, `-p no:cacheprovider`, a
scratch `--basetemp`):

- Red first, the new tests against today's code: `1 passed, 32 xfailed in
  42.65s` (the one pass is the legacy-record test, which holds on both).

<!-- fig: cmd="python -m pytest -q -n auto tests/test_baseline_snapshot.py tests/test_intake_settled.py tests/test_intake_held_act.py -k '<the tests added in 2ded34460>' -rx" rev="2428a1bf5 plus the new tests, before any code change" -->

- Every module importing a changed script (`baseline_snapshot`,
  `acceptance_record`, `intake`, `record_rows`, `check_trajectory`), the
  modules holding the tests tagged TC-147, TC-167, TC-173, TC-240, TC-269,
  TC-400 and TC-403, `test_spine_carrier.py`, `test_migrate_vocabulary.py`,
  `test_coordinator_act.py`, `test_overnight_legs.py`, `test_smoke_budget.py`,
  and the four the brief names (`test_import_layers.py`,
  `test_module_size_ratchet.py`, `test_complexity_ratchet.py`,
  `test_dogfood_sync.py`), 79 modules: `4 failed, 2940 passed, 1 skipped in
  2484.84s (0:41:24)`. The four: the complexity census (the committed mirror
  rule fell under the limit: its entry deleted); a test calling the refusal
  text's old two-argument form (updated); the dispatcher's provenance test,
  which saw the scripts change under it mid-run ("coordinator Python changed
  after this process imported it"; passes alone); and the TC-269 needs test,
  which found a real defect, fixed: a template's example row (`-000`, the
  shipped needs template's `STK-000` reads `Accepted`) was never named, so
  the rule left it out of the copy; example rows now follow live.

<!-- fig: cmd="python -m pytest -q -n auto -p no:cacheprovider --basetemp <scratch> <the 79 modules>" rev="2ded34460 plus the uncommitted build, before the merge-judgement and example-row fixes" -->

- After those fixes and the merge-judgement fix (below), the record-heavy
  modules again (`test_baseline_snapshot`, `test_record_rows`,
  `test_snapshot_readers`, `test_intake_settled`, `test_intake_held_act`,
  `test_acceptance_record`, `test_text_then_act`, `test_accepted_risk`,
  `test_adjudicate_act`, `test_check_test_first`, `test_baseline_drift`,
  `test_trajectory_staged`, `test_import_layers`, `test_module_size_ratchet`,
  `test_complexity_ratchet`, `test_dogfood_sync`, `test_loop_provenance`,
  `test_bootstrap`): `664 passed, 1 skipped in 1760.66s (0:29:20)`.

<!-- fig: cmd="python -m pytest -q -n auto -p no:cacheprovider --basetemp <scratch> <the 18 modules>" rev="72f0a63ca's tree before row_rule's decomposition" -->

- After `row_rule` was split for the cognitive-complexity check (the build
  commit's first hook run refused it at 22): `tests/test_record_rows.py
  tests/test_complexity_ratchet.py`, `9 passed in 1.90s`; the commit hook then
  passed (`RESULT: PASS`).
- `trace.py --root . --strict`: exit 0, `Traceability: SN=31 SR=141 LLR=356
  TC=427 orphans=0 integrity=0 ...`; `check_trajectory.py --root . --strict`:
  exit 0, `check_trajectory: clean (1059 work item(s), 930 done (88%), 37
  cancelled, graph acyclic).`
- `run_menu.py smoke`: `3768 passed, 3 skipped, 18 warnings in 163.92s (0:02:43)`, exit 0, after
  the strict trace and trajectory checks, `check_docs --stale` and
  `check_resync` (`OK, 12 shipped path(s) changed; entry anchored at
  121ce2e002d3...`; its first run refused the RESYNC entry anchored at
  `2ded34460`, re-anchored at the change's base). The budget step reported
  `CPU 671.9 s vs 540 s cpu-seconds; wall 164.8 s vs 600 s` with a WARN, which
  fails nothing (the operator, 2026-10-20): the box carried two other
  builders' runs, and the tier gained `tests/test_record_rows.py`'s eight
  in-process cases.

<!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="72f0a63ca plus the RESYNC anchor fix, uncommitted" -->
- `check_docs.py --root .`: `OK - 3671 doc(s), 3826 intra-repo link(s), 0 broken.`

**Acts owed for automated adjudication** (text only; no status moved):

- Amendments to `Accepted` rows, each owed a re-acceptance at a sitting;
  SR-207's is shown to the operator:
  - SR-140: `requirement`, `rationale`, `acceptance_criteria`
  - SR-179: `requirement`, `rationale`, `acceptance_criteria`
  - SR-207: `title`, `requirement`, `rationale`, `acceptance_criteria`, `coincident`
  - LLR-173: `title`, `detail`, `rationale`
  - LLR-178: `title`, `detail`, `rationale`
  - LLR-245: `title`, `detail`, `rationale` (added; the row had none)
  - LLR-271: `detail`
  - LLR-361: `title`, `detail`, `rationale`
  - LLR-364: `detail`, `rationale`
  - TC-167: `method`
  - TC-173: `method`
  - TC-240: `method`, `expected`
  - TC-269: `method`, `expected`
  - TC-400: `method`, `expected`
  - TC-403: `method`, `expected`
  - The `evidence` cells of TC-167, TC-173, TC-240, TC-269, TC-400 and TC-403
    were regenerated from the tests' tags: a silent trace cell, owing no act.
- Routed traced changes to `Accepted` rows: none.
- New or rewritten `Drafted` rows owed a first acceptance: IF-220
  (`data`, `version`, `notes`: the `kept` field and the ledger-deletion
  refusal), an off-spine interface row, outside the spine's acceptance-act
  rung (OI-30 D3). No new row.

## Context

Filed on trunk on 2026-11-23 by the queue drill's coordinator, on the
operator's ruling given in the coordinator's session ("Yes please file the
row-scoped copy as a work item"). That chose this design over multi-verdict
carry-forward (the specref, §0 step 4).

**The problem.** The acceptance record (`docs/archive/last_accepted/`)
holds a byte-for-byte copy of each registry file, and an act refreshes a
registry by copying the live file over its record. SR-207 refuses that
copy while any row of the file outside the act has drifted from its
recorded text, since the copy would bless text no verdict judged. That
rule is right. But it couples every row of a file: one unblessed amendment
blocks every blessed amendment and every first acceptance in the same
registry. The design registry alone holds 356 rows.

The drill met the coupling at every sitting but the last:
- WI-1047's act was refused outright, and the row was cancelled and
  superseded.
- WI-1049 and WI-1055 each needed an operator ruling to revert the
  unblessed rows on trunk so the rest could be recorded, then a follow-up
  row (WI-1050, WI-1056) to re-land them. Until they re-landed, the
  reverted rows described code that no longer existed.

The operator has given a standing revert ruling to keep sittings moving;
this row removes the need for it.

**Why this design** (the coordinator's recommendation, adopted by the
ruling). PROCESS.md lets a lane land with amendments still owed: its merge
is refused only for an act no verdict backs, and a MEANING row or a first
draft "neither holds a lane". A held rung's acceptance is the operator's,
taken later. So drift from several landings sharing one registry on trunk
is the kit's normal state. Carry-forward (an earlier verdict's blessed
rows, digest unchanged, joined into one later whole-file act) would end the
re-judging but keep the coupling: blessed rows, and new rows waiting to
flip, would still wait on every drifted sibling. Writing only the named
rows ends both. Blessed rows are anchored at once and drop out of the next
sitting, so carry-forward is not needed.

**The rule it keeps.** The record is still written only by copying live
text (SR-179, LLR-178), now at the row: an act copies, byte for byte, the
live text of exactly the rows it names (accepted, re-accepted, retired).
Every other row keeps its recorded text. An act cannot carry an unnamed
row's drift into the record by construction. SR-207's refusal becomes this
construction, and a drifted row outside the act simply stays drifted and
owed. The mirror rules restate the same thing: a record written at a
commit equals the previous record with exactly the act's named rows taken
from live at that commit.

**Trust.** The row adds no authority to any act. An act still writes only
what a verdict or the operator authorizes, and now can write no more than
that. The surface that changes is the record writer and the two checks
that judge what it wrote. A defect there could bless unjudged text, so the
tests must show a laundering attempt refused at each check, and the row
runs the unfiltered suite before it lands.

**The plan settles** (`planmode = "single"`), before any edit:
- **Traced cells of rows the act does not name** (links such as
  `verifies`, which need no acceptance and ride today's whole-file copy):
  refreshed with the act, or left for each row's own act. State the choice
  and why. Today every act's copy refreshes every row's traced cells, the
  ones routed to adjudication included, since only drift in accepted cells
  refuses the copy. The choice weighs that against how a routed traced
  change is found owed. The plan writes its rule into this spec's
  Done-when, in the three items that name it, before any edit, and the
  coordinator approves the plan before the build.
- How a retired row leaves the record, and how a new row enters it.
- The rows' order and every byte between rows, so the record stays
  diffable against live.
- Tiers that share one file.
- The off-spine registries (interfaces, components, external), which today
  no combined sitting shows.
- **The first (seed) snapshot,** which blesses whole files once, stays as
  it is.
- Each accepted row whose text states the whole-file copy: at least SR-179,
  LLR-178, SR-207 and LLR-245 (search for others). Its amendment is text
  only and goes to a sitting; SR-207's is shown to the operator.

**Coverage bound.** The writer's and the checks' promises reach the
records that supported workflows and the kit's own routes produce: acts
taken through the snapshot command, with the registries as committed.
Hand-edited kit-written state (a hand-edited record copy or snapshot stamp)
is outside them (PROCESS.md §6, "Review threat model"), apart from what the
Done-when names inside: the laundering attempts the checks must refuse.

**Ordering.** WI-1045 moves `acceptance_record.py`'s landing rules into a
new module. This row changes the snapshot checks in the same file, so the
two land one after the other, never side by side.

## Done-when

- [x] An act writes into the record only the rows it names, each copied
      byte for byte from live; every other row of the recorded file keeps
      its recorded text, except that a row the act does not name follows
      live (its live text taken whole, or its copy dropped when live no
      longer carries it) when its live text claims no acceptance (or, gone
      from live, its recorded copy claimed none), or when its recorded copy
      and its live text both claim acceptance and neither its accepted
      cells nor its routed traced cells (`SN-Refs`, `Boundary-Refs`,
      `SR-Refs`, `Verifies`: the traced cells whose change routes to
      adjudication) differ, which refreshes its other traced cells. A
      drifted row the act does not name stays drifted, is reported as owed,
      and no longer refuses the act.
- [x] The writer re-reads its result and refuses, writing nothing, unless
      the result reads as the previous record with exactly the named rows
      replaced, plus the unnamed rows that follow live under item 1's rule
      (a row whose live text claims no acceptance, or, gone from live,
      whose recorded copy claimed none; and a row claiming acceptance on
      both sides whose accepted and routed traced cells are unchanged).
- [x] The checks that judge a written record judge it at the row: a record
      written at a commit equals the previous record with exactly that
      act's named rows taken from live at the commit, plus the unnamed rows
      that follow live under item 1's rule (a row whose live text claims no
      acceptance, or, gone from live, whose recorded copy claimed none; and
      a row claiming acceptance on both sides whose accepted and routed
      traced cells are unchanged). Tests show refused, at the commit hook
      and on a committed revision: an unnamed row's drift carried in, a
      named row copied with an edit, and a row dropped that no act retired.
- [x] A test reproduces the drill's case: one registry holding a blessed
      amendment, an unblessed amendment and a row ruled ACCEPT. The act
      records the first and third and leaves the second drifted and owed.
- [x] The seed snapshot still copies whole files, and existing records
      read clean under the new checks with no migration.
- [x] The accepted rows that state the whole-file copy are amended (text
      only, no code names) and listed in the Deliverable as owed to
      adjudication. Any new row is `Drafted`. A RESYNC entry tells adopters
      what changed and that their records need no migration.
- [ ] The unfiltered suite passes on the branch before the merge, and its
      summary line is quoted in the Deliverable.
