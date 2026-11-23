+++
id = "WI-1059"
title = "A derived act holds back a first-acceptance flip whose parent stays Drafted, instead of listing one the hook refuses"
workstream = "process"
specref = ""
sr_refs = ["SR-231"]
needs = []
buildtier = "medium"
planmode = "single"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Built on the maintenance branch `maint/wi-1059`, cut from `refactor_again`
at `8db60ba58`, with the commit hooks on, under the plan
`docs/plans/WI-1059/plan.md` and the coordinator's go-ahead, which approved
it as written. No status moved and no act was taken. No id was minted (none
was needed: the hold amends LLR-338, and its tests extend TC-368), so no
`--bump-ids` run was owed. No decisions record: every choice is stated by a
spine row or by the plan the coordinator approved. The specref (WI-1057's
spec) is cleared at close, as a terminal row's is.

- `50d4d3fbe`: the plan.
- `42ff50467`: the build: tests, code, rows, Flow 6, the act template's
  notes, the coordinator-cycle recipe, the RESYNC entry, regenerated
  evidence and views.
- `624c2abd0`: a first answer to the writer guard (below), since replaced:
  the flip status as a named constant, and views regenerated.
- `b137199a6`: this close-out.
- The commit after it: the coordinator's correction (below): the literal
  restored, and the guard's one exemption, by name and reviewed.

**The writer guard: an exemption by name, reviewed.** The first smoke run on
this branch failed one test, `tests/test_acceptance_level.py::test_no_shipped_loop_module_WRITES_an_acceptance_cell`
(OI-30 D3's lexical guard that no shipped script assigns an accepted value
to a status key), on `adjudicate_act.py`'s `dict(row, Status="Accepted")`:
the line that reads an in-memory COPY of a flipped row so the parent-first
predicate can be asked about the tree the act would leave. The module writes
no registry. My first answer (`624c2abd0`) named the status as a constant,
`FLIPPED_STATUS`; the coordinator rejected it, because the guard's
`\bstatus` cannot match inside that name (`_` is a word character), so the
constant blinded the guard rather than answering it. On the coordinator's
instruction the literal is back on its one line, the constant and its
comment are gone, and the guard carries one narrow exemption,
`ACCEPTANCE_CELL_WRITER_EXEMPT`, keyed by file name and the exact stripped
line (`("adjudicate_act.py", 'dict(row, Status="Accepted")')`) with its
reason: an in-memory copy, so the parent-first predicate can be asked about
the tree an act would leave; the module writes no registry. The guard's
docstring says a line that assigns the accepted value without writing a
registry is exempt only by name in that table, so any new such line
elsewhere still fails; the rest of the guard is unchanged. Its scan is
factored into one helper over `(name, text)` pairs, which the guard and a new
test, `test_the_writer_guards_exemption_is_its_file_and_line_alone`, both
call: the exempt line in another file, and another accepted-value line in
the exempt file, are still offenders. Neither test carries a test-case tag,
as the guard did not.

**Vocabulary: the spec's "held" is "waits" in everything this row wrote.**
"Held" already names the held rung in LLR-338 ("held MEANING", "held
APPROVE", "on a held rung"), in the act template's notes and in the act
assembler's own per-row flag. So a flip the spec calls held is a **waiting**
flip in every row, brief, refusal and report, and the parent it is held
under is the parent it **waits on**; a "held flip marked held" is a waiting
flip marked `waiting on <parent> (<status>)`; "the all-held refusal" is the
all-waiting refusal. The mapping is one to one.

**1. The derived act holds back a flip whose parent stays unaccepted, and
the hold chains.** The act derivation computes which owed first-acceptance
flips wait in one place, beside the step every consumer already calls, so
the brief, the all-waiting refusal and the later-act report read one
answer. It asks the parent-first rule's own whole-spine predicate (the one
the commit hook and the standing integrity finding ask) over the spine as
the act would leave it, as a fixpoint: start with every owed flip taken,
drop each flip the predicate names as an accepted child under an
unaccepted parent, and repeat until a pass drops none. Each pass that does
not stop shrinks a finite set, so it ends, and it ends on the largest set
whose flips leave the rule nothing to find; a test case under a waiting
design row therefore waits too. The edges are the rule's own (an SR's
needs, a design row's SRs, a test case's SRs and design rows); none is
restated. The rows come from the hook's own tier reader, made public by a
rename and nothing else (`_tree_tiers` to `parent_first_tiers`: its
definition, its two call sites, its comment), so the act lists a flip only
where the hook judges the same rows, and a parent registry that cannot be
read or does not parse refuses the derivation, naming it. The brief's part 2
lists the takeable flips and their one `--accepts` command; each waiting
flip follows under `Not in this act`, one line each,
`<row> (<registry>) waiting on <parent> (<status>)[, ...]`, with every
parent it waits on, and is left out of the command. When every owed flip
waits beside an owed amendment act, part 2 reads "No flip can be taken in
this act." followed by the same block. The act template's instruction text,
slots and catalogue digest are unchanged; only its operator notes say so.

**2. The tests (red first).** In `tests/test_adjudicate_act.py` (TC-368,
smoke tier):

- T1 `test_a_flip_under_a_returned_parent_waits_and_the_listed_flips_pass_the_parent_first_check`:
  ACCEPT LLR-002 and LLR-003, RETURN SR-002. LLR-002 is listed; LLR-003
  waits on SR-002 (Drafted), is named in the brief and is not in its flip
  line or command; the act taken as listed leaves the hook's commit
  judgement with no line.
- T2 `test_a_parent_accepted_in_the_same_act_lets_its_child_be_listed`:
  ACCEPT SR-002 and LLR-003. Both are listed, nothing waits, and the taken
  act passes the parent-first check and leaves nothing owed.
- T3 `test_a_test_case_waits_on_a_waiting_design_row_and_names_every_parent`:
  TC-003 verifies SR-002 and LLR-003. LLR-003 waits on SR-002; TC-003 waits
  on both SR-002 and LLR-003, each named.

**3. The all-waiting refusal, and the later-act derivation.**
- T4 `test_a_verdict_whose_only_remaining_act_waits_is_refused_naming_each_row_and_parent`
  (WI-1057's shape): the derivation and the composed brief both refuse with
  exactly "the verdict <path> owes no act that can be taken at HEAD: every
  flip it still owes waits on a parent that is not accepted, and a later act
  lists each once its parent is accepted: LLR-003
  (docs/requirements/low-level-requirements.toml) waiting on SR-002
  (Drafted)".
- T5 `test_the_later_act_derivation_reports_a_waiting_flip_as_owed_and_marked_never_taken`:
  before the act it reads `flip LLR-002 (...); flip LLR-003 (...) waiting on
  SR-002 (Drafted)`; after the act taken as listed, `flip LLR-003 (...)
  waiting on SR-002 (Drafted)`, never None.
- T9 `tests/test_coordinator_act.py::test_an_act_turn_that_leaves_a_waiting_flip_owes_it_and_does_not_read_complete`
  (TC-368, full tier): the act turn over a stub adjudicator takes the act as
  listed, exits 1 and prints `act: owed after the call: flip LLR-003
  (docs/requirements/low-level-requirements.toml) waiting on SR-002
  (Drafted)`, never `act: complete`; LLR-002 is Accepted at HEAD and LLR-003
  still Drafted. `coordinator_adjudicate.py` is unchanged: its report prints
  the derivation's answer.

**4. Once the parent is accepted, the same verdict's act lists the flip.**
T6 `test_once_its_parent_is_accepted_the_same_verdicts_act_lists_the_waiting_flip`:
the verdict is refused while SR-002 is Drafted; after SR-002's own act
lands, the same verdict's act lists LLR-003.

T7 `test_a_parent_registry_that_does_not_parse_refuses_the_derivation_naming_it`
and T8 `test_the_wait_is_read_from_the_parent_first_rules_one_predicate`
drive LLR-338's failing-registry and one-predicate clauses.

**5. Rows and the runtime flow.** LLR-338's `detail` gains the wait, the
chain, the failing registry, the waiting flip's naming and listing once its
parent is accepted, and the all-waiting refusal; its later-act sentence gains
the marking. TC-368's `method` and `expected` each gain the matching passage.
Flow 6's prose gains the waiting flip, its refusal branch reads "owes only
flips waiting on an unaccepted parent (LLR-338)", its act line notes "a
waiting flip is named, never flipped", and its failing branch "work remains
(a waiting flip included)". No text this row wrote names a code file,
function, symbol or flag. LLR-338 and TC-368 carried no code name before, so
none is left elsewhere in either row.

**Why LLR-338's added refusal stays inside SR-231.** SR-231's pre-launch
list ("an unrecorded verdict, one owing no act, ...") states what the act
turn must refuse, not all it may (LLR-338 already refuses an acceptance with
no acceptance record, which SR-231 does not list), and a verdict whose every
remaining act waits is its "owing no act" case for an act nothing can take
yet; a waiting flip stays owed, so the act turn fails while one is left,
which is SR-231's completion contract ("succeeds only when ... every
authorized act is taken"), and SR-231 is not amended. LLR-306 is not amended
either: its act turn refuses on "act-derivation refusal" and "succeeds only
after a successful call leaves no authorized act owed", which already cover
both outcomes, and it states no wording for the owed-after line.

**Also changed.** IF-296's and IF-308's `data` (both Drafted) name the
waiting part, the all-waiting refusal and the public tier reader; the act
assembler's module docstring and its IF-296 contract say the same. The
coordinator-cycle recipe (`project-trajectory/skills/...`, and its copies
under `.claude/skills/` and `.agents/skills/`) gives the act turn's exit 1
and exit 2 their waiting cases and says a child whose parent was returned
waits until the parent's own act lands. The RESYNC entry is anchored at
`8db60ba58`, the branch's base (the resync check refused `50d4d3fbe`, the
first anchor I gave it). The act template's notes change moves the
retained-session identity (which hashes the template file's bytes, unlike
the catalogue digest, which reads its normalized body and did not move), so
a retained adjudicator holding an actable class drains once, at its next
clear point.

**The live case.** On this branch, the derivation over WI-1057's verdict
(`docs/reviews/wi-1057-adjudicate-fourth-sitting/001-ADJUDICATE-ca5a7d9.md`)
refuses: "the verdict ... owes no act that can be taken at HEAD: every flip
it still owes waits on a parent that is not accepted, and a later act lists
each once its parent is accepted: LLR-406
(docs/requirements/low-level-requirements.toml) waiting on SR-251
(Drafted)"; the later-act derivation reads `flip LLR-406
(docs/requirements/low-level-requirements.toml) waiting on SR-251
(Drafted)`. On `8db60ba58` it listed LLR-406's flip and nothing else.

**Red first.** T1 to T9 were written first and run against the unchanged
code at `50d4d3fbe`: T1, T3, T4, T5, T6, T7, T8 and T9 failed and T2 passed,
`8 failed, 1 passed, 86 deselected in 29.06s`. T1 failed at its `acts`
equality (LLR-003 listed), T3 likewise (TC-003 listed), T4 got an act where
a refusal was owed, T5 read `flip LLR-002, LLR-003 (...)` unmarked, T6 got
an act on its first half, T7 got no refusal, T8 found no call to the rule's
predicate, and T9's act turn exited 0 (`act: complete`).
<!-- fig: cmd="python -m pytest -q -p no:cacheprovider --basetemp <scratch> tests/test_adjudicate_act.py tests/test_coordinator_act.py -k 'waiting or waits or returned_parent or same_act_lets or parent_registry_that or one_predicate'" rev="50d4d3fbe with the new tests added, before any code change" -->

**Mutation proofs** for what passed on the unchanged code (each mutant was
applied as a pytest plugin outside the repository, never committed; the
module passes unmutated, below):

| Test | Mutation | Fails at | Result |
|---|---|---|---|
| T2 (TC-368) | each flip judged with only itself flipped, so a parent the same act accepts is not credited | `tests/test_adjudicate_act.py:1026`, the `acts` equality (LLR-003 reported waiting on SR-002) | `1 failed, 1 passed, 49 deselected in 7.73s` |
| T6, second half (TC-368) | the wait credits only parents the act flips, never one accepted at the revision | `tests/test_adjudicate_act.py:1109`, `assert why is None` (refused after SR-002's act) | `1 failed, 1 passed, 49 deselected in 10.75s` |

T1's last assertion is not vacuous: on its fixture, flipping LLR-002 and
LLR-003 together (as the act listed them before this row) leaves the hook's
commit judgement with `LLR-003 (Accepted) is accepted under SR-002
(Drafted), which is not: accept SR-002 in its own acceptance act, or return
LLR-003 to Drafted`, the line WI-1057's act was refused with.

**Tests.**

- The 55 test modules that import a changed module (`acceptance_record`,
  `adjudicate_act`) or are spine-linked to one (`trace.py --tests-for`), the
  modules holding TC-368's and TC-321's tests, the modules reading the act
  template, the runtime flows, the RESYNC pack or the skills, and
  `test_import_layers`, `test_module_size_ratchet`, `test_dogfood_sync` and
  `test_complexity_ratchet`, at the build tree:
  `2292 passed, 1 skipped in 1792.42s (0:29:52)`.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider -n auto --basetemp <scratch> <the 55 modules>" rev="42ff50467 (its tree before the commit)" -->
- The act derivation's own two modules after the code change:
  `95 passed in 204.53s (0:03:24)`.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider -n 4 --basetemp <scratch> tests/test_adjudicate_act.py tests/test_coordinator_act.py" rev="42ff50467 (its tree before the docstring and template-note edits)" -->
- `trace.py --root . --strict`, exit 0: `orphans=0 integrity=0`.
  <!-- fig: cmd="python project-trajectory/scripts/trace.py --root . --strict" rev="42ff50467 (its tree before the commit)" -->
- `check_trajectory.py --root . --strict`, exit 0:
  `check_trajectory: clean (1057 work item(s), 927 done (88%), 37 cancelled, graph acyclic).`
  <!-- fig: cmd="python project-trajectory/scripts/check_trajectory.py --root . --strict" rev="42ff50467 (its tree before the commit)" -->
- McCabe complexity of the act assembler at the limit of 10: "All checks
  passed!" (`_derive` 9, the highest). `acceptance_record.py` stays at 972
  SLOC; `adjudicate_act.py` grows 287 to 374, under the 1000 threshold.
- The first `run_menu.py smoke`, on the close-out tree over `42ff50467`:
  `1 failed, 3756 passed, 3 skipped, 18 warnings in 141.51s (0:02:21)`, the
  writer guard above. (An earlier attempt stopped at the RESYNC check, which
  refused the entry's first anchor; it is anchored at the base now.)
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="42ff50467 (with the close-out's tree, before the guard fix)" -->
- After the fix, the guard's module and the act tests:
  `147 passed in 78.92s (0:01:18)`; the act's other importers and the
  ratchet and layer modules (`test_coordinator_act`, `test_held_status_git`,
  `test_adjudicate_brief`, `test_coordinator_adjudicate`,
  `test_import_layers`, `test_module_size_ratchet`,
  `test_complexity_ratchet`): `283 passed in 253.66s (0:04:13)`.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider -n 4 --basetemp <scratch> tests/test_acceptance_level.py tests/test_adjudicate_act.py" rev="624c2abd0 (its tree before the commit)" -->
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider -n auto --basetemp <scratch> tests/test_coordinator_act.py tests/test_held_status_git.py tests/test_adjudicate_brief.py tests/test_coordinator_adjudicate.py tests/test_import_layers.py tests/test_module_size_ratchet.py tests/test_complexity_ratchet.py" rev="624c2abd0 (its tree before the commit)" -->
- The commit checks, `run_menu.py smoke`, exit 0, on this close-out's
  staged tree over `624c2abd0` (both strict lints, the docs check and the
  RESYNC check, "OK, 3 shipped path(s) changed; entry anchored at
  8db60ba58967362a448865c72cf0679a51d3014a", then the smoke tier):
  `3757 passed, 3 skipped, 18 warnings in 140.73s (0:02:20)`. Its budget
  line reads CPU 618.0 s against 540, a WARN only, not charged to the lane;
  wall 141.5 s against 600. (One run before it, with the spec's move not
  yet staged, failed `test_disposition_adoption`'s three repository-walk
  cases on the queued path git still listed; staged, they pass.)
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="624c2abd0 (with the close-out's tree staged, before its commit)" -->
- The coordinator's correction (the exemption by name), on its tree over
  `b137199a6`. The guard's two tests under two mutants, never committed: the
  table not honoured fails both, `2 failed, 95 deselected in 0.51s`; the
  exemption keyed by the line alone fails the narrowness test at its
  other-file case, `1 failed, 1 passed, 95 deselected in 0.49s`; restored,
  `2 passed, 95 deselected in 0.46s`. Then the guard's module and both act
  modules: `192 passed in 138.25s (0:02:18)`.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider --basetemp <scratch> tests/test_acceptance_level.py -k 'WRITES_an_acceptance_cell or exemption_is_its_file'" rev="b137199a6 with the correction's tree, each mutant applied then restored" -->
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider -n auto --basetemp <scratch> tests/test_acceptance_level.py tests/test_adjudicate_act.py tests/test_coordinator_act.py" rev="b137199a6 with the correction's tree, before its commit" -->
- The commit checks after the correction, `run_menu.py smoke`, exit 0, on
  its staged tree over `b137199a6` (both strict lints, the docs check, the
  RESYNC check, "OK, 3 shipped path(s) changed; entry anchored at
  8db60ba58967362a448865c72cf0679a51d3014a", then the smoke tier):
  `3758 passed, 3 skipped, 18 warnings in 131.16s (0:02:11)`, one more than
  before (the narrowness test). Budget line: CPU 603.0 s against 540, a WARN
  only; wall 131.9 s against 600.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="b137199a6 (with the correction's tree staged, before its commit)" -->

**Byte deltas** (none budgeted or watched), base `8db60ba58` to `42ff50467`:
`docs/requirements/low-level-requirements.toml` 564,152 -> 564,994 (+842);
`docs/test/test-cases.toml` 703,314 -> 705,563 (+2,249);
`docs/requirements/interfaces.toml` 172,607 -> 172,772 (+165);
`project-trajectory/RESYNC_PACK.md` 758,126 -> 760,313 (+2,187);
`project-trajectory/prompts/adjudicate-act.template.md` 5,687 -> 6,241 (+554).

**Acts owed for automated adjudication.**

- *Amendments to `Accepted` rows (text only, status unchanged):*
  LLR-338 `detail`; TC-368 `method` and `expected`.
- *Routed traced changes to `Accepted` rows:* none. No `Accepted` row's
  `sr_refs`, `verifies`, `sn_refs` or `boundary_refs` moved. TC-368's
  `evidence`, a traced cell no adjudication is routed for, was regenerated
  to name the nine new tests.
- *First acceptance, `Drafted`, rewritten:* IF-296 (`data`) and IF-308
  (`data`). No new row.

## Context

Filed on trunk on 2026-11-23 by the queue drill's coordinator, from the
fourth adjudication sitting's act (WI-1057, the specref).

The sitting ruled LLR-406 ACCEPT and returned its parent SR-251. The act
the kit derives from that verdict listed LLR-406's flip from `Drafted` to
`Accepted`. Taken as listed, the commit was refused by the hook's
parent-first step: "LLR-406 (Accepted) is accepted under SR-251 (Drafted),
which is not: accept SR-251 in its own acceptance act, or return LLR-406
to Drafted". The coordinator took the act without LLR-406.

So the act brief told its taker to do something the kit then refuses. A
taker that follows it to the letter fails at the commit. A taker that
improvises has to choose which listed row to leave out, which the brief
forbids ("take nothing that is not listed" says nothing of taking less).
The derivation and the parent-first rule read the same statuses but
disagree.

The fix belongs in the derivation, which already lists only what is still
owed. A first-acceptance flip whose parent would still not be accepted
after the act is held back and named in the brief: owed under the verdict
until the parent is accepted. The parent can be accepted by the same act
or already, and so is not held. Once the parent is accepted, the same
verdict's act lists the flip again. That is today's behaviour: WI-1057's
act lists LLR-406 and nothing else.

**The outcomes, settled at the scope critique** (coordinator, 2026-11-23):
- **A hold chains.** A flip whose parent is itself held is held too, since
  that parent will not be flipped by the act. A test case whose verified
  design row is held waits on that row.
- **Some flips held, some not.** The brief lists the takeable flips and
  names each held row with the parent it waits on.
- **Every owed flip held, and no other act owed.** There is nothing to take
  now. The derivation refuses, as it refuses a verdict owing no act, and
  its reason names each held row and its parent.
- **Completion is unchanged.** A held flip is work the verdict still owes.
  The later-act derivation keeps reporting it, marked held with its parent,
  so a coordinator act turn that leaves one does not read complete, and the
  verdict is not done until a later act takes it. SR-231's completion
  contract needs no amendment.

**Rows this changes.** LLR-338 (Accepted) states the derivation. Its text
gains the hold, and that amendment is owed to a sitting. Runtime Flow 6's
refusal branch names the all-held case. The plan confirms whether LLR-306's
act-report text needs the held marking too.

**Planning** is `single`: the hold reads parent statuses over the SR, LLR
and TC edges, with chains, and the plan settles where the hold is computed
so the brief and the later-act derivation read one answer.

## Trust

This row adds no authority. The derivation already reads each row's
committed status at the revision to tell an owed act from a taken one, and
the hold reads the parents' committed statuses the same way. Those come from
the registries as committed, written by supported routes. An unreadable or
unparseable registry already refuses the whole derivation. The consumers are
the act brief (`project-trajectory/scripts/adjudicate_act.py`), the
coordinator's act turn and its completion report
(`project-trajectory/scripts/coordinator_adjudicate.py`), and the person or
session that takes the act. The ruling they share: a hold only takes a flip
out of the act and never adds one, so a wrong hold leaves a flip owed and
reported, never lost. The commit hook's parent-first step stays the guard
against a flip listed wrongly. (PROCESS.md §3, "When a guard is owed".)

The promise reaches the states supported workflows and the kit's own routes
produce. Hand-edited kit-written state, such as a hand-edited verdict or
binding, is outside it (PROCESS.md §6, "Review threat model").

## Done-when

- [x] The derived act holds back each first-acceptance flip whose parent
      (a design row's system requirement, a test case's verified rows) is
      neither already accepted nor flipped by the same act. The brief names
      each held row and the parent it waits on, and part 2 lists only rows
      the parent-first rule accepts. A hold chains through a held parent.
- [x] A test derives an act from a verdict that accepts a child and
      returns its parent. The child is held and named, and the brief's
      flips, once taken, pass the parent-first check. A second test accepts
      the parent in the same act and shows the child listed. A third holds
      a test case under a held design row.
- [x] A verdict whose only owed acts are held flips is refused, naming each
      held row and its parent. The later-act derivation reports a held flip
      as owed and marked held, never as taken; a test shows both.
- [x] Once the parent is accepted, the same verdict's act lists the held
      flip; a test shows it.
- [x] LLR-338's amendment (text only) and any other accepted row text this
      changes are listed in the Deliverable as owed to adjudication, and
      Flow 6 names the all-held refusal. No text it writes names a code
      file, function, symbol or flag.
