+++
id = "WI-1067"
title = "WI-1066's verdict answered: SR-207 fronts its event and states its retirement rule; TC-560 drives two more faults"
workstream = "process"
specref = ""
sr_refs = ["SR-207", "SR-157"]
needs = []
buildtier = "medium"
planmode = "none"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Built on the maintenance branch `maint/wi-1067`, cut from `refactor_again`
at `d62f3c74b`, with the commit hooks on and planning `none`, as the row
states. No id minted, no status moved, no act taken and no kit file changed
(so no RESYNC entry). No decisions record: every choice made is stated by a
spine row. The specref (WI-1066's verdict) is cleared at close, as a
terminal row's is.

- `5cf590b93`: the build: SR-207's and TC-560's text, the new tests, the
  regenerated evidence and the regenerated views.
- `8b3f62154`: the close-out (the Deliverable, the move to
  `docs/archive/work/complete/`, the log fragment, the views).
- The commit after it: LLR-245's routed-cell list gains the constrains
  cell, on the coordinator's ruling of 2026-11-23 (item 5 below), with this
  record, the log fragment and the views.

**1. SR-207 (text only; still `Accepted`, owed at its recorded copy).**
- `requirement`: "The kit shall leave, in an acceptance act, the recorded
  text of every row ..." now reads "When the kit takes an acceptance act, it
  shall leave the recorded text of every row the act does not accept,
  re-accept or retire whose accepted text, or whose adjudicated links,
  differ from its live text." The event is in front, in the EARS event form;
  one `shall`; nothing else in the sentence moved.
- `acceptance_criteria`: one clause added after "the same act naming that
  row records it from live": "an unnamed recorded accepted row that live no
  longer carries stays in the recorded copy and is named as owed, and an
  act naming that row retires it from the recorded copy". It states the
  retirement the requirement already names.
- `rationale`: the list of adjudicated links now reads "a requirement's
  needs and boundary crossings, a design row's requirements, a
  requirement's or design row's constrains link (the interfaces whose
  behaviour its text states) and a test case's verified rows". Item 2
  below confirms the record already holds that link.
- Unchanged: `title`, `coincident`, `sn_refs`, `boundary_refs`,
  `hat_refs`, `priority`, `verification_method`, `phase`, `aspect`. The
  hook warned that the accepted cells moved while `Hat-Refs` stayed put;
  `SECURITY` is left on purpose, since the row is still about keeping
  unread text out of the record, and its perspective did not change.
- Each acceptance clause and the test that drives it, all named by TC-240
  (`tests/test_baseline_snapshot.py`):

  | Clause | Test |
  |---|---|
  | an unnamed drifted row: the act completes, records the named rows, keeps the row's recorded text, names it owed | `test_a_drifted_row_outside_the_act_is_KEPT_and_named_owed` (every compared tier) |
  | the same act naming that row records it from live | the same test, re-run naming the row |
  | an unnamed recorded accepted row gone from live stays in the copy, named owed; an act naming it retires it | `test_a_REMOVED_accepted_row_is_KEPT_until_an_act_retires_it` |
  | adjudicated links held like accepted text: a needs link; a requirement's and a design row's constrains link | `test_unclaimed_rows_and_silent_trace_cells_follow_live_but_a_routed_link_waits`; `test_a_row_whose_constrains_link_alone_moved_is_KEPT_until_an_act_names_it` (new, both tiers) |
  | an unnamed accepted row with its judged cells unchanged takes its live trace cells; an unnamed row claiming no acceptance takes its live text | `test_unclaimed_rows_and_silent_trace_cells_follow_live_but_a_routed_link_waits` |
  | tiers sharing one file | `test_in_a_SHARED_file_one_tiers_drift_is_kept_by_anothers_acceptance` |

  The retirement rule already had its test, and TC-240's method already
  says "A recorded accepted row gone from live stays until an act names
  it, which retires it", so no test was added for it and TC-240's text is
  unchanged.

**2. The constrains link (confirmed from the code and a test, before the
rationale was amended).** From the code: in `record_rows.py`, `_source`
keeps an unnamed row whose recorded copy and live text both claim
acceptance unless `_settled` holds, and `_settled` fails when the cell
split's traced half (`acceptance_record.split_changed_cells`, which classes
`Constrains` traced for both registries in `SPINE_TRACED_CELLS`) meets
`ROUTED_TRACED_CELLS`, which holds `Constrains` for
`system-requirements.toml` and `low-level-requirements.toml` (WI-1024,
LLR-420). `kept_ids` then lists the row, its recorded bytes differing from
live. From a test: no test pinned it, so
`test_a_row_whose_constrains_link_alone_moved_is_KEPT_until_an_act_names_it`
(TC-240), parameterized over a requirement and a design row, accepts row A
while row B's constrains cell alone moves (`IF-001` to `IF-002`) and runs
the snapshot command: it prints `LEFT OWED: <B>`, the copy keeps B's
recorded bytes, and the act-ledger entry's `kept` is `[B]`; a later act
naming B with `--reaccepts` records B from live, prints no LEFT OWED, and
keeps nothing. The code keeps the row, so the stop rule did not fire.

**3. TC-560 (still `Drafted`).** `method` adds "one naming an example row
(an id ending -000) that the registry carries and that itself names a
system requirement" and "a row below the two-row cycle, not on it, listed
before the cycle". `expected` adds "the row naming an example row is
reported as naming no live design row" and "each row below a broken chain
names the row where its chain breaks, the row naming the missing parent for
the row below it and the cycle's row it hangs from for the row below the
cycle". In `tests/test_requirement_tree.py`, tagged TC-560 as its other
tests are:
- `test_a_row_naming_an_example_row_as_its_parent_is_reported_once`
  (orphan pass, Drafted and Accepted): the example row `LLR-000` names
  SR-001 and the child `LLR-056` names it; the one finding naming LLR-056
  is "LLR LLR-056 names parent LLR-000, which is no live design row".
- `test_a_row_below_a_cycle_names_where_its_chain_breaks` (orphan pass,
  both statuses): `LLR-062` hangs from the cycle `LLR-060`/`LLR-061`,
  listed first so the walk enters the cycle from below; the one finding
  naming it is "LLR LLR-062 reaches no SR: its parent chain breaks at
  LLR-061".
- `test_the_strict_check_fails_on_each_fault` gains both faults as cases,
  each at both statuses, through the registry on disk: the finding is
  reported and the strict check exits 1.

The evidence was regenerated with `trace.py --root . --regen-evidence`
("trace: evidence regenerated for TC-240, TC-560"). The code already did
what LLR-480 says for both branches, so the stop rule did not fire.

**4. The three row rules.** No text written here names a code file,
module, function, symbol, CLI flag or test name, and neither row inherited
one. SR-207 keeps one `shall`. Each clause is driven by a test its test
case names (table above). TC-560 drives LLR-480's stated branches and no
more. SR-207's child LLR-245 now names the constrains link as its parent
does (item 5).

**5. LLR-245 (text only; still `Accepted`), on the coordinator's ruling.**
The first build left LLR-245 alone and reported that its list of routed
trace cells, "`SN-Refs` and `Boundary-Refs` on a requirement, `SR-Refs` on
a design row, `Verifies` on a test case", did not name the constrains
cell, which the code routes and keeps on both tiers and SR-207's amended
rationale now names: read literally, it said a row whose constrains link
alone moved follows live. The gap predates this row: WI-1060 wrote that
list on a branch built beside WI-1024, which routed the cell. The
coordinator ruled on 2026-11-23 that LLR-245 is amended on this branch, so
that a sitting does not judge SR-207's new rationale beside a child that
disagrees with it.
- `detail`: the parenthesis now reads "(`SN-Refs`, `Boundary-Refs` and
  `Constrains` on a requirement, `SR-Refs` and `Constrains` on a design
  row, `Verifies` on a test case)". Nothing else in the row moved. The
  cells it names are registry cell names used as vocabulary, as the row
  already used them; it names no code file, function, symbol or flag, and
  inherited none in the cell touched (its options are "the re-accept
  option" and "the verdict option").
- It stays inside SR-207: it now names the same adjudicated links as
  SR-207's rationale, and states no behaviour SR-207 does not. Its other
  parent, SR-228 (held-rung re-acceptance), is not touched by the list.
- The clause is driven by
  `test_a_row_whose_constrains_link_alone_moved_is_KEPT_until_an_act_names_it`,
  which TC-240 names; TC-240 is LLR-245's one verifying test case
  (`verifies = ["SR-207", "SR-228", "LLR-245"]`), so no tag was added and
  the evidence is unchanged ("trace: every evidence cell is current").

**Red first.** The new tests passed on the code as it stood: the behaviour
existed (`24 passed, 55 deselected in 0.78s` for the TC-560 selection;
both constrains cases passed with the retirement test). Each was shown to
bite under a temporary mutation, applied by a scratch script outside the
repository, run, then reverted by copying the saved file back and checking
it byte-identical. None was committed.

<!-- fig: cmd="python -m pytest -q tests/test_requirement_tree.py -k 'example_row or below_a_cycle or strict_check_fails_on_each_fault'" rev="maint/wi-1067 tests before 5cf590b93, code at d62f3c74b" -->

| Mutation | First red line | Selection |
|---|---|---|
| m1: the walk takes an example row as a live design row | `E       AssertionError: []` | `2 failed, 22 passed, 55 deselected in 0.69s`: the orphan-pass example case at both statuses (the strict check's working set still drops example rows) |
| m2: m1, and the strict check's working set keeps example rows | `E       AssertionError: []` | `4 failed, 20 passed, 55 deselected in 6.39s`: the example case, orphan pass and strict check, both statuses |
| m3: a row below a cycle is taken as a row on it | `E       AssertionError: ['LLR LLR-062 is on a parent cycle (LLR-062 -> LLR-061 -> LLR-060 -> LLR-062)', ...]` | `4 failed, 20 passed, 55 deselected in 0.82s`: the below-cycle case, orphan pass and strict check, both statuses |
| m4: a broken chain is reported at the row itself, not where it breaks | `E       AssertionError: ['LLR LLR-062 reaches no SR: its parent chain breaks at LLR-062', ...]` | `4 failed, 20 passed, 55 deselected in 0.77s`: the same four |
| m5: the constrains cell dropped from the routed cells of both registries | `E       AssertionError: intake: snapshot: 1 registry file(s) copied to docs/archive/last_accepted` (no LEFT OWED line) | `2 failed, 172 deselected in 9.80s`: the constrains case for both tiers |

<!-- fig: cmd="python wi1067_mutate.py (scratch, outside the repository): pytest -q -rf tests/test_requirement_tree.py -k 'example_row or below_a_cycle or strict_check_fails_on_each_fault' under m1-m4; tests/test_baseline_snapshot.py -k constrains_link_alone under m5" rev="maint/wi-1067 tests before 5cf590b93, code at d62f3c74b plus each mutation" -->

**Tests run.**
- The modules holding every touched case's tests, with the four named
  ratchet modules (no kit module changed, so no importer runs):
  `tests/test_requirement_tree.py`, `tests/test_baseline_snapshot.py`,
  `tests/test_record_rows.py`, `tests/test_import_layers.py`,
  `tests/test_module_size_ratchet.py`, `tests/test_complexity_ratchet.py`,
  `tests/test_dogfood_sync.py`: `317 passed, 1 skipped in 79.30s (0:01:19)`.
- `trace.py --root . --strict`: exit 0, "Traceability: SN=31 SR=141
  LLR=368 TC=444 orphans=0 integrity=0 ...".
- `check_trajectory.py --root . --strict`: exit 0, "check_trajectory:
  clean (1066 work item(s), 935 done (88%), 37 cancelled, graph acyclic)."
- `run_menu.py smoke`, once, on the close-out tree before its last
  Deliverable edit: exit 0, `3882 passed, 3 skipped, 18 warnings in
  138.61s (0:02:18)`; "smoke budget: CPU 720.6 s vs 540 s cpu-seconds;
  wall 139.2 s vs 600 s wall-seconds; ... -> OVER" (reported only; no
  checks fail on seconds).

<!-- fig: cmd="python -m pytest -q -n auto <the seven modules above>; python project-trajectory/scripts/trace.py --root . --strict; python project-trajectory/scripts/check_trajectory.py --root . --strict; python project-trajectory/scripts/run_menu.py smoke" rev="maint/wi-1067 at 5cf590b93's tree, and its close-out tree for the smoke run" -->

After LLR-245's amendment (a text-only registry change, no test moved, so
no smoke rerun, as the coordinator ruled):
- `tests/test_requirement_tree.py`, `tests/test_baseline_snapshot.py`,
  `tests/test_record_rows.py`: `261 passed in 83.71s (0:01:23)`.
- `trace.py --root . --strict`: exit 0, "Traceability: SN=31 SR=141
  LLR=368 TC=444 orphans=0 integrity=0 ...".
- `check_trajectory.py --root . --strict`: exit 0, "check_trajectory:
  clean (1066 work item(s), 936 done (88%), 37 cancelled, graph acyclic)."

<!-- fig: cmd="python -m pytest -q -n auto tests/test_requirement_tree.py tests/test_baseline_snapshot.py tests/test_record_rows.py; python project-trajectory/scripts/trace.py --root . --strict; python project-trajectory/scripts/check_trajectory.py --root . --strict" rev="maint/wi-1067 at 8b3f62154 plus LLR-245's amendment" -->

**Acts owed to the next automated adjudication sitting.**
- SR-207: an amendment of an `Accepted` row, cells `Requirement`,
  `AcceptanceCriteria` and `Rationale` here, on top of WI-1060's still
  unblessed amendment; against its recorded copy the row's whole owed
  amendment is `Title`, `Requirement`, `Rationale`, `AcceptanceCriteria`
  and `Coincident`. WI-1060's record says its amendment is shown to the
  operator; this rewrite is shown with it.
- LLR-245: an amendment of an `Accepted` row, cell `Detail` (its list of
  routed trace cells gains the constrains cell on both tiers). It sits in
  SR-207's chain and SR-228's, so the acceptance brief now shows SR-228's
  chain waiting as well.
- TC-560: a `Drafted` row with its `method` and `expected` rewritten, owed a
  first acceptance.
- Routed traced changes to an `Accepted` row: none. TC-240's `evidence`
  gains one test name; it is a silent trace cell, which follows live when an
  act next writes the test-case registry, so it owes nothing.

**Noted, not changed.** TC-240's `expected` summarizes SR-207's acceptance
without the retirement clause; its `method` and tests drive it. The
coordinator ruled on 2026-11-23 that it stays as it is.

**Review.** Round 1 over `d62f3c74b..a14ca8fde`, briefed to judge the rows as
the next sitting will and to judge the mutation evidence: OpenAI Sol (low)
APPROVE, having read the record's row composition, the requirement tree's
walk and both test modules; Gemini Hydrogen (low) APPROVE. Merged by the
coordinator.

## Context

Filed on trunk on 2026-11-23 by the queue drill's coordinator, to answer
the seventh automated adjudication sitting's verdict (WI-1066, Gemini Neon,
the specref). Its two `### Dispositions` drafts name this row's scope; the
two are one row because both are small and text-led, and neither waits on
the other.

**SR-207 (MEANING, not blessed; still `Accepted`, owed at its recorded
text).** WI-1060 rewrote it from "refuse the act while an unnamed row has
drifted" to "leave every unnamed drifted row at its recorded text". The
sitting asks two things:
1. Its requirement fronts its event condition in the EARS event form
   ("When the kit takes an acceptance act, it shall leave ..."), rather
   than burying ", in an acceptance act," after "shall leave".
2. Its acceptance criteria state the retirement rule the requirement
   already names: an unnamed recorded accepted row that live no longer
   carries stays in the recorded copy and is named owed, and an act naming
   that row retires it from the recorded copy.

The coordinator adds one item from reading the row: its rationale's list of
"adjudicated links" (a requirement's needs and boundary crossings, a design
row's requirements, a test case's verified rows) predates WI-1024, which
routes a requirement's or design row's `constrains` link to adjudication
too (LLR-420; `record_rows.ROUTED_TRACED_CELLS`). The list names that link
as well, so the row stays true to the code. The builder confirms from the
code that the record keeps a row whose `constrains` link alone changed, and
says so; if it does not, the builder stops and reports.

SR-207 is the acceptance act's rule, and WI-1060's record says its
amendment is shown to the operator; this row's rewrite is shown with it.

Critiqued 2026-11-23 (`docs/reviews/2026-11-23-scope-critiques/WI-1067.md`):
the `constrains` check is a Done-when item of its own.

**TC-560 (RETURN; still `Drafted`).** It verifies LLR-480 but leaves two
of its fault branches undriven, in its method, expected and tests:
1. A design row whose parent cell names an example row (an id ending
   `-000`, which is not a live design row).
2. A design row whose parent chain reaches a cycle (a row below the cycle,
   not on it), reported naming the row where its chain breaks.
Each runs at both `Drafted` and `Accepted` and through both the orphan
pass and the strict check, as TC-560's other faults do. If a test shows
the code does not do what LLR-480 says for either, the builder stops and
reports; LLR-480 was accepted by this sitting and is not amended here.

## Done-when

- [x] SR-207's requirement opens with its event condition; its acceptance
      criteria state the retirement rule (kept and named owed while
      unnamed, retired when named), each clause driven by a test its test
      cases name; its rationale's adjudicated links include the
      `constrains` link. The amendment is text only; SR-207 stays
      `Accepted`, owed to the next sitting.
- [x] The Deliverable reports, from the code and a test, that an act keeps
      a row whose `constrains` link alone changed (LEFT OWED, in `kept`)
      until an act names it; if it does not, the builder stops and reports
      before amending SR-207's rationale.
- [x] TC-560's method, expected and tests drive both missing faults at
      both statuses, red first where a test is new; TC-560 stays
      `Drafted`, owed to the next sitting.
- [x] Each row it touches keeps the three row rules (no code names,
      inherited ones included; one obligation with every clause tested; a
      child within its parent).
