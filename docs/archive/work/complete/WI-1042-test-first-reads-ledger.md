+++
id = "WI-1042"
title = "The test-first check reads when each row was accepted from the act ledger instead of replaying registry history"
workstream = "process"
sr_refs = ["SR-217"]
needs = ["WI-1022"]
specref = ""
buildtier = "strong"
safety_class = "ordinary"
priority = 3
planmode = "single"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1042`, cut from `refactor_again` at
`6915cde7d`, with the commit hooks on. `planmode = "single"`: the plan,
`docs/plans/WI-1042/plan.md`, was committed before the build. The builder
stopped once before the plan: the spec's first text read the record across
its 2026-11-16 move, where the record is in an earlier spelling that D3 keeps
out of the core tooling. The coordinator ruled (2026-11-22): D3 stands, option
2 with LLR-257's at-or-before reading, and this spec says so. The specref is
cleared at close, as a terminal row's is.

- `c2d6bc52a`: the plan, with the spec amended for the ruling (the cut; the
  completeness check since the cut; the Trust state before the cut; Done-when
  1 and 3). The plan quotes the completeness result and today's verdict, and
  names the test for each Trust state.
- `4f62438e5`: the build. The reader, the tests, the rows, the RESYNC entry,
  the kit README's row and the regenerated views. The plan's table names
  TC-468 to TC-471 there, once the rows exist.
- The close-out commit: this Deliverable, the audit note's site 3 marked
  resolved, the log fragment, and the move to `complete/`.

**What landed.** `check_test_first.record_acceptances(root, rev, line)`
replaces `first_acceptance_commits` and `first_association_commits` (and
their helpers `_touching` and `_carried_at`): the check no longer replays the
registries. It walks the commits that wrote the act ledger or the record's
copies of the requirement, design and test-case registries, through
`baseline_snapshot._ledger_commits`, the one walk, which gains `also` (more of
the record's files) and `rev`, and still reads the current path only. Each
commit's copies are read against every parent's with `acceptance_record`'s row
reader and acceptance-act rule:

- **an act** (its commit added a ledger entry) dates exactly each row it
  carried into acceptance and each pair new in its copies, so a re-pointing
  is accepted at the act that re-accepts it, not at its text commit;
- **the cut** (no parent holds the record at its current path) dates what it
  carries at or before itself, and nothing before it is read; here it is the
  vocabulary move `2bee2b551`;
- **a gap** (a flip or a new pair with no entry), and a commit whose ledger
  or its parent's is malformed, leave what they carry unread, never dated at
  a later act.

A record commit off trunk's first-parent line is placed at the first
first-parent commit containing it, and the report names its own commit. A
requirement or test case reading accepted at the tip that no act accepted is
unread. A tip test case the record holds accepted only while it named
something else is not accepted for the requirement. `history_unreadable`,
`first_implementation_commits`, the report's lines and IF-198's exits are
unchanged; an unread entry now says why. IF-220 names CMP-007 among its
consumers, and its notes name the reading.

**Completeness (Done-when 1).** Measured before any reader change, by a
scratch reader over the 120 commits from seq 1's parent that touch the ledger
or those copies under either directory, reading the current spelling: one
change carries flips or new pairs with no entry, the move `2bee2b551` (852
flips, 694 pairs), which is the cut. Since the cut, none. The shipped reader
agrees: over this repository it reads 9 record commits, one cut
(`2bee2b551d`), and no gap. No row is owed for a gap.
<!-- fig: cmd="python -c 'import check_test_first as c; r = c.record_acceptances(\".\"); print(len(r.places), r.cuts, r.gaps)'" rev="4f62438e5" -->

**Verdict on this repository (Done-when 5).** Unchanged.
`python project-trajectory/scripts/check_test_first.py --root . --src project-trajectory/scripts`
prints, at `6915cde7d` (57 s) and at `4f62438e5` (15 s): "test-first: OK -
no requirement accepted since the declared start f6dd5b87a1 has a test case
accepted after its implementation landed or not accepted"; `--strict` exits
0. The cut reached trunk at `f6dd5b87a`, the declared start, so the 138
requirements it carries are out of scope. SR-247, the one requirement an act
accepted after the cut (seq 183, `9b377be1e` on `maint/vocabulary`), is placed
at that same commit.
<!-- fig: cmd="python project-trajectory/scripts/check_test_first.py --root . --src project-trajectory/scripts" rev="6915cde7d and 4f62438e5" -->

**Trust states and their tests (Done-when 4).** Each act in the tests is
taken with `copy_live`, the producer. An act's commit dates its rows:
`test_a_re_pointing_committed_before_its_act_is_dated_at_the_act` and
`test_an_act_on_a_side_branch_is_ordered_where_it_reached_trunk` (TC-468).
The cut: `test_the_record_before_its_cut_is_never_read` (TC-469), over a
record in the earlier spelling moved on a side branch. No ledger or an empty
one: `test_acceptances_no_act_records_are_unread_never_passing` (TC-470). A
gap and a malformed ledger:
`test_a_record_change_with_no_act_is_unread_never_dated_later` and
`test_an_act_whose_ledger_is_malformed_is_unread` (TC-471). A shallow clone:
the existing `test_a_shallow_clone_is_reported_unreadable_never_passing`. The
TC-250 cases moved onto acts.

**Tests.**

- Red first: `tests/test_check_test_first.py` on `6915cde7d`'s code, `18
  failed, 22 passed in 56.35s`. The text-then-act test failed with `[] ==
  [('SR-001', ..., [('TC-001', <the act>)])]`, the replay dating the pair at
  the text commit; the other failures were the missing reader.
  <!-- fig: cmd="python -m pytest tests/test_check_test_first.py -q -n auto --basetemp D:/rt1042/t" rev="6915cde7d's code under the new tests" -->
- The 35 modules that import or exercise `check_test_first` or
  `baseline_snapshot`, with `test_import_layers`, `test_module_size_ratchet`,
  `test_dogfood_sync` and `test_complexity_ratchet`: `1438 passed, 1 skipped
  in 2998.50s (0:49:58)`.
  <!-- fig: cmd="python -m pytest -q -n auto --basetemp D:/rt1042/t <the 35 modules: every tests/ file naming check_test_first, baseline_snapshot, test-first, _ledger_commits or last_act, with the four whole-tree tests>" rev="4f62438e5 (its tree before the commit)" -->
- Rerun on the final tree, for files edited during that run
  (`test_check_test_first`, `test_resync_pack`, `test_check_resync`,
  `test_dogfood_sync`): `122 passed, 1 skipped in 204.83s (0:03:24)`.
  <!-- fig: cmd="python -m pytest -q -n auto --basetemp D:/rt1042/t tests/test_check_test_first.py tests/test_resync_pack.py tests/test_check_resync.py tests/test_dogfood_sync.py" rev="4f62438e5 (its tree before the commit)" -->
- `run_menu.py smoke`: `3717 passed, 3 skipped, 18 warnings in 270.61s
  (0:04:30)`, the CPU budget WARN only.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="4f62438e5 (its tree before the commit)" -->
- `trace.py --root . --strict` and `check_trajectory.py --root . --strict`:
  exit 0. `plan_coverage.py --item`: OK, 7 clauses. The unfiltered suite was
  not run.

**Sizes.** `baseline_snapshot.py` 964 -> 966 SLOC and `check_test_first.py`
342 -> 410, both under the 1000 threshold. The complexity ratchet is
unchanged (175 rows); every new function is under 15.

**Byte deltas.** `RESYNC_PACK.md` 745,116 -> 747,455 (+2,339, unbudgeted):
"The test-first order reads when each row was accepted from the acceptance
record", anchored `[since 6915cde7d]`. The kit README 94,187 -> 94,539
(+352), its `check_test_first.py` row. `docs/enforcement-audit.md` 55,326 ->
55,360 (+34). No capped or watched file was touched.

**Acts owed.** LLR-257 (Accepted) re-accepted: its text now states the
record reading, the cut, the gap and the side-branch order. TC-250 (Accepted)
re-accepted: two clauses described the replay (a re-pointing "dated at the
re-pointing commit", and a design-row pair dated at or before the design
registry's move to TOML) and now read the act's date and "that move dates
nothing". That is the builder's call: the brief named LLR-257 alone, and
TC-250's accepted text would otherwise describe tests it no longer has. The
first acceptance of TC-468, TC-469, TC-470 and TC-471 (Drafted). IF-220 is
Drafted and owes nothing.

**Rows to file:** none.

## Context

Filed on trunk on 2026-11-21 from WI-1036's history-reader audit, class (c)
site 3 (`docs/reviews/2026-11-history-readers/README.md`). Its two calls
serve one decision, so one row covers both (the coordinator's ruling at
WI-1036's review).

The test-first check needs to know when each requirement was first accepted,
and when each pair of a test case and a requirement it names first read
accepted. Today it replays every first-parent commit touching the
registries and applies the acceptance-act rule to each commit and its
parent. That recomputes a recorded decision (PROCESS.md §3; the review-churn
plan's item 2). The record exists: each act-ledger entry lists the rows it
accepted and re-accepted, its commit is the one that added it, and the
snapshot copy at that commit holds the accepted rows, test cases' `verifies`
cells included. Acceptance happens only in an act, so reading the acts gives
the same order SR-217 asks for, still from the committed history.

**Settled by the scope critique (2026-11-21), and the cut by the
coordinator's ruling, 2026-11-22, on the builder's stop: D3 stands; option 2
with LLR-257's at-or-before reading.**

- **The cut (D3).** The vocabulary move `2bee2b551` (2026-11-16) is the
  record's cut. Entries, copies and keys before it are in an earlier
  spelling (the record's directory `docs/archive/last_approved/`, the
  ledger's keys `approved`/`reattested`, the copies' status `Approved`) and
  are never read: no compatibility readers in the core tooling, and formats
  in git history are cut cleanly (the operator's D3, 2026-11-11; test-tiers
  HANDOFF §5, and §9.9, which declined this reader for this check). Every
  acceptance the move carries, pre-ledger ones included, is read as at or
  before the commit that brought the move onto trunk's first-parent line.
  That is LLR-257's existing rule for a row moved into Accepted from a word
  outside the status vocabulary: it settles the order when it falls at or
  before the landing, and for a requirement's own acceptance at or before
  the declared start; otherwise the requirement is reported unread, never
  as a pass. The declared start `[checks] test_first_since` is that commit
  (`f6dd5b87a`, per §9.9's precedent), so those requirements fall out of
  scope here. An act made on a side branch is ordered by the first trunk
  commit that contains it, as a landing is. WI-1040's finding that
  `baseline_snapshot._ledger_commits` reads the ledger's current path only
  is this cut working as intended, not a defect: the walk keeps reading the
  current path only.
- **Pairs.** A pair reads accepted at the first act whose snapshot copy
  holds the test case accepted while it names the requirement, directly or
  through a design row whose `sr_refs` name the requirement in that same
  copy. A re-pointing is so dated at the act that re-accepted it, as the
  acceptance-act rule dates it today.
- **Completeness.** Before the ledger is trusted, every commit since the cut
  that changes a snapshot copy is checked to add a ledger entry, read in the
  current spelling only: flips to Accepted, and re-acceptances that carry a
  direct or design-row re-pointing. The move commit is the cut, not a gap.
  A snapshot change with no entry is a gap: it is filed, and the check reads
  the rows it touched as unread, never as a pass and never dated at a later
  act.

SR-217 and LLR-257 (both Accepted) state the replay, so this row amends
LLR-257's text, which drifts for automated adjudication.

**The architectural delta.** The test-first check (`check_test_first.py`,
CMP-007) comes to read the act ledger and the snapshot copies, which
`baseline_snapshot.py` (CMP-006) writes through IF-220. IF-220 gains CMP-007
among its consumers. That cell is one WI-1022 (F-2) rewrites into component
ids, so this row builds after it and writes the cell in F-2's form.

## Trust

The act ledger and the snapshot copies gain authority over the test-first
check's dates, which decide its exit under `--strict` (IF-198). The guard is
owed under PROCESS.md §3 "When a guard is owed".

- **Producer:** `intake.py snapshot` (`baseline_snapshot.copy_live`) appends
  one entry per act, in the act's own commit, beside the copies it wrote. An
  act on a malformed ledger is refused before it moves any byte, so a failed
  write leaves the record as it stood. A malformed ledger is refused whole on
  `trace.py`'s integrity floor (IF-220's notes).
- **Consumers:** IF-220's `consumers` cell lists them; this row adds the
  test-first check there, and the cell stays their one list.
- **The ruling, for each state a supported route produces:**
  - an entry and its adding commit both readable: the act's commit dates
    the rows it names;
  - an acceptance before the cut: at or before the cut's trunk commit, as
    above;
  - no ledger, or an empty one, while a registry holds accepted rows: those
    acceptances cannot be dated, so each requirement whose order turns on
    them is reported unread, never as a pass;
  - an entry whose adding commit lies beyond a shallow clone's window, a
    gap the completeness check found, or a malformed ledger on the walk:
    unread, never as a pass, as IF-198 rules for history that cannot show
    the order.

  A hand edit of the ledger or a snapshot copy is outside the ruling.

## Done-when

- [x] The completeness check above is run on this repository and its result
      quoted; any gap is filed, not patched over. Measured before any reader
      change: read in the current spelling from seq 1, one change carries
      flips or new pairs with no entry, the move commit `2bee2b551`, which is
      the cut; since the cut, none.
- [x] Both readings come from the ledger and the snapshot copies under the
      rules above; no first-parent replay of the registries remains.
- [x] The record before the cut is never read; a test shows an acceptance
      the cut carries dated at or before the cut's trunk commit, never at a
      later act and never read from the earlier spelling.
- [x] Each state in the Trust ruling has a test, and one test that fails on
      today's code shows a ledger-read date.
- [x] The check's verdicts on this repository are unchanged, or each change
      is explained in the Deliverable.
- [x] IF-220 names CMP-007 among its consumers; the cross-component rule
      reports nothing uncovered.
- [x] LLR-257's text says so (text only); the Deliverable lists its drift as
      the act owed, and the audit note's site 3 is marked resolved.
