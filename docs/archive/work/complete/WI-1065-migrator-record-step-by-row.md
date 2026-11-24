+++
id = "WI-1065"
title = "The vocabulary migrator's record step works in a record that holds a row-by-row act"
workstream = "process"
specref = ""
sr_refs = ["SR-247", "SR-179"]
needs = ["WI-1060"]
buildtier = "medium"
planmode = "single"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Built on the maintenance branch `maint/wi-1065`, cut from `refactor_again` at
`c7d6bd6f4`, with the commit hooks on, under the plan
`docs/plans/WI-1065/plan.md`. No status moved, no snapshot was taken on this
repository and no id was minted (every obligation landed in the three amended
rows the ruling names). No decisions record: every choice is stated by an
amended row or by the plan the coordinator approved.

**The approval.** The coordinator approved the plan (`f1b3a447e`) on
2026-11-23, before any build: D1, D2, D4, D5, D6, D8, D9, D10, D11 and D12 as
proposed; D3 confirmed (the whole run refuses and writes nothing, the
operator's refined (c) read as refusing the run); D7 adopted here (the link
step skips the operator's scratchpad, both names, at the repository root, and
never opens it). The RESYNC anchor stays `[since c7d6bd6f4]`; trunk has moved
(WI-1067 merged) and was not merged in.

- `f1b3a447e`: the plan.
- `b92a67bfc`: the red tests, under the declared expected-failure marker.
- `47e762418`: the build: the record reading, the refusal, the skip, the link walk,
  the rows, the RESYNC entry, regenerated evidence and views.
- `e425d4173`: the close-out (this Deliverable, the move, the log fragment).
- `809e610f2`: review round 1's three adopted findings (the review record,
  at the end of this Deliverable).
- The commit after it: review round 2's adopted finding (the escaped
  backtick).

**A read of this repository's scratchpad, recorded for the operator.** One
measuring run before the fix, `migrate_vocabulary.py --root . --check` over
this worktree (plan M1), had the migrator's link walk read this repository's
`OPERATOR_SCRATCHPAD.md` in process, to look for a link into the record's
earlier directory. Nothing of it was printed and nothing was written. That
read is the defect D7 fixes; after it, the migrator was not run over this
repository's tree again, and every later probe used a temporary repository
under `D:/review-tmp`.

**1. The skip and the refusal (Done-when 2).** `migrate_vocabulary.py` reads
the acceptance record's act ledger before its first step, at both entry
points (`main` and `spellings_owed`), under either name of the record's
directory, and as the kit's scripts read it (`_ledger_readings`: a ledger that
does not decode or parse as it stands, a byte-order mark included, holds no
entry). The record reads row by row when an `[[act]]` entry carries `kept`, an
empty list included (`_kept_ledger`).
- **Pre-row-by-row records** (no such entry): every step runs as before.
- **Row by row, current vocabulary:** the record step leaves its copies out,
  as it already did for the vocabulary check's report, so it writes no record
  file. A run for other files leaves kept and drifted rows as recorded; check
  mode names no copy as owed and exits 0 when nothing else is owed.
- **Row by row with an earlier spelling** (`record_refusal`): the earlier
  directory present, an act entry keyed `approved` or `reattested`, or a copy,
  under either directory name, that the registry step's own rewrite would
  change or cannot prove (`_earlier_spellings`, `_copy_spelling`). The run
  refuses before its first step, so before the registry step's walk of the
  record, in both modes: nothing runs, no file anywhere is written, exit 1.
  It prints one line per file or directory holding an earlier spelling and one
  naming the ledger with the way back (run the migrator before the record's
  first row-by-row act, pointing to WI-1060's RESYNC entry; restore, run, take
  the act again). `spellings_owed` returns those lines alone, so the
  vocabulary check reports the refusal through IF-312, unamended.
- **Why the whole run** (D3, as the coordinator asked it stated): a run that
  respelled the live registries and left the record would put live and record
  in two vocabularies, a live row reading `Accepted` beside its recorded copy
  reading `Approved`, which the current scripts read as an acceptance the
  record does not hold.
- D3 holds: every earlier spelling the reading looks for is one the migrator
  already held (`RECORD_DIRS`, `LEDGER_KEYS`, the registry carriers); no core
  module changed, and the vocabulary check gets the refusal through the
  existing seam. `kept` is current vocabulary, read here as the kit reads it
  and held to `record_rows.act_rows` by a parity test.
- Tests cover both paths and verify the commit hook and the committed history:
  in a git repository, a record the migrator moved and an act through the
  snapshot writer then kept a drifted row in, a run for a binding rewrites the
  binding and no record file; staged, the hook's registry-integrity step
  (`trace.py --strict-integrity`, run as the hook runs it) reports no
  acceptance-record finding the run added and the staged mirror check is
  empty; committed, the committed-history check is empty.

**2. Coverage bound (Done-when 3).** The skip and the refusal reach records
the kit's own routes produced. The git-backed tests build every record they
judge through those routes: the snapshot writer's seed and acts
(`baseline_snapshot.copy_live`, which the snapshot command runs), and the
migrator's own run over an earlier kit's record (modelled by the fixture the
existing record tests use, since no earlier kit is at hand). The in-process
tests use hand-written ledgers and copies only to drive each signal. A
hand-edited record copy, ledger or stamp is outside the promise (PROCESS.md
§6, "Review threat model").

**3. The scratchpad (D7).** The link walk (`_markdown_files`) skips the
operator's scratchpad at the root under either name, so the run never opens
it; before, it read the file and could rewrite a link in it, on every run and
every vocabulary check. SR-247's "renames it without reading it" is now true
and tested.

**4. Rows (Done-when 4).** SR-247, LLR-369 and TC-427 amended, text only, as
the plan's section 5 wrote them; SR-179 and LLR-178 unchanged. Every code
name the rows inherited is gone (LLR-369's detail rewritten whole, TC-427's
method scrubbed of the check flag, the vocabulary check's file, a folder name
and a section name). The absolute-term rule finds nothing in the new SR-247
acceptance (7 advisories before) or LLR-369 detail (28 before). Inherited
clauses no test drove now have one (D8): the import boundary, a copy whose
live registry is gone, the cache folder, the upper-case status, and the
scratchpad's unread rename.

**5. The RESYNC entry.** "The vocabulary migrator writes no record copy once
the record holds a row-by-row act, and refuses a run while that record keeps
an earlier spelling" `[since c7d6bd6f4]`; `check_resync` OK.

**Deviations from the approved plan.**
- The hook's integrity step is compared before and after the run rather than
  asked for no acceptance-record finding: a two-row tree carries findings of
  its own (the registries its minimal record holds no copy of), and the test
  asserts the run adds none, staged and committed.
- The plan named a repository-level `--check` after the fix as a figure; the
  coordinator ruled the migrator never runs over this repository's tree
  again, so the figure was taken over a copy of this repository's registries
  and record under `D:/review-tmp` (no scratchpad in it): the migrator at
  `c7d6bd6f4` exits 1 with 79 lines (5 copies "written equal", 74 cells
  absorbed: the 67 of plan M1 plus this branch's own amendments to SR-247,
  LLR-369 and TC-427), and the built migrator prints "nothing stored in an
  earlier spelling" and exits 0.

**Tests run** (pytest under the worktree's venv, `-p no:cacheprovider`, a
scratch `--basetemp` under `D:/review-tmp/2026-11-23-wi1065/`):

- Red first, the new tests against the migrator at `c7d6bd6f4`
  (`tests/test_migrate_vocabulary.py tests/test_migrate_vocabulary_record.py`):
  `79 passed, 14 xfailed in 52.72s`. The 79 are the module's 77 and the two
  tests pinning inherited clauses (a copy whose live registry is gone, the
  import boundary), which hold on both trees. Run with `--runxfail`, each of
  the 14 failed on its own assertion (check mode naming the copy, the copy
  written, the refusal absent, the scratchpad's link rewritten).

<!-- fig: cmd="python -m pytest -q -p no:cacheprovider --basetemp <scratch> -rxX tests/test_migrate_vocabulary.py tests/test_migrate_vocabulary_record.py" rev="b92a67bfc (the red tests over the migrator at c7d6bd6f4), 2026-11-23" -->

- After the build, the same two modules: `93 passed in 46.92s`.

<!-- fig: cmd="python -m pytest -q -p no:cacheprovider --basetemp <scratch> tests/test_migrate_vocabulary.py tests/test_migrate_vocabulary_record.py" rev="47e762418's tree, uncommitted, 2026-11-23" -->

- Every module that imports the migrator (`test_acceptance_level`,
  `test_csv_header`) or runs it (`test_old_kit_resync`), `test_stage_ladder`
  (it runs the vocabulary check), the two modules holding TC-427's tests,
  `test_record_rows` (the parity test reads it), `test_smoke_budget` (the slow
  list grew) and the four the brief names (`test_import_layers`,
  `test_module_size_ratchet`, `test_complexity_ratchet`, `test_dogfood_sync`),
  12 modules: `294 passed, 1 skipped in 282.50s (0:04:42)`.
  `trace.py --tests-for` names only `test_migrate_vocabulary.py`.

<!-- fig: cmd="python -m pytest -q -n auto -p no:cacheprovider --basetemp <scratch> <the 12 modules>" rev="47e762418's tree, uncommitted, 2026-11-23" -->

- `check_complexity.py --root . --mode enforce`: `OK - 168 row(s) over 15,
  unchanged from baseline.` The migrator is 882 SLOC against the 1,000
  threshold (814 before), so no size baseline is owed.
- `trace.py --root . --strict`: exit 0, `Traceability: SN=31 SR=141 LLR=368
  TC=444 orphans=0 integrity=0 ...`; its only line on the amended rows is
  SR-247's "declares no Form" advisory, which 131 requirements carry and this
  branch did not touch. `check_trajectory.py --root . --strict`: exit 0,
  `check_trajectory: clean (1066 work item(s), 935 done (88%), 37 cancelled,
  graph acyclic).`
- `scripts/check_resync.py`: `check_resync: OK, 1 shipped path(s) changed;
  entry anchored at c7d6bd6f432883cb242b239cc3809872396c75fa`.
- `check_docs.py --root .` after the move: `OK - 3694 doc(s), 3833 intra-repo
  link(s), 0 broken.`
- `run_menu.py smoke`, once, at the end: exit 0, after the strict trace and
  trajectory checks, `check_docs --stale` and `check_resync`; the tier
  `3887 passed, 3 skipped, 18 warnings in 146.21s (0:02:26)`. The budget step
  reported `CPU 687.9 s vs 540 s cpu-seconds; wall 147.0 s vs 600 s` with a
  WARN, which fails nothing (the box carried other builders' runs). The tier
  now holds 3,890 items against `max-tests = 3890`: this branch added 13
  in-process cases to it, so a sibling landing more smoke cases meets the
  ratchet at its merge.

<!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="47e762418 plus the close-out, uncommitted, 2026-11-23" -->

**Acts owed for automated adjudication** (text only; no status moved):
- Amendments to `Accepted` rows, each owed a re-acceptance at a sitting:
  - SR-247: `acceptance_criteria`, `rationale`
  - LLR-369: `title`, `detail`, `rationale`
  - TC-427: `method`
  - TC-427's `evidence` cell was regenerated from the tests' tags: a silent
    trace cell, owing no act.
- Routed traced changes to `Accepted` rows: none.
- New or rewritten `Drafted` rows owed a first acceptance: none.

**Review record.**

Round 1 (2026-11-23, over `c7d6bd6f4..e425d4173`): Gemini Hydrogen `APPROVE
findings=0`; OpenAI Sol three MINORs. The coordinator's rulings, each fixed on
this branch with the hooks on:

1. **Adopted** (Sol, confirmed by execution): the link step rewrote a link
   written inside an inline code span, against LLR-369's inherited clause
   "the link text, prose and code spans keep their words"; TC-427's fixture
   tested only a bare directory name inside code. Fixed: `relink_markdown`
   leaves a link target alone when it lies inside code, which it reads in two
   forms. An inline code span is a run of one or more backticks up to the
   next run of the same length in its paragraph; a run nothing closes there
   is a literal backtick. A fenced code block is opened by a line of three or
   more backticks (with no backtick after them on the line) or tildes, behind
   up to three spaces, and closed by a line of at least as many of the same
   character, or the end of the file. The walk meets fenced blocks (any
   Markdown page can hold one), so both are handled; an indented code block
   is not recognised, as the docstrings say. The regression is the existing
   links test, which gains a CRLF page holding links in inline spans of one
   and of two backticks, a fenced block of backticks (a link and a reference
   definition), one of tildes, a backtick run with more on its line, a stray
   backtick and one link in prose. Red before the fix:
   `FAILED tests/test_migrate_vocabulary.py::test_links_into_the_record_follow_it_and_every_other_word_stays`,
   on `assert 'docs/reviews/code.md: 1 link(s)' in 'migrate_vocabulary:
   acceptance-record link rewritten: docs/reviews/code.md: 7 link(s) into
   docs/archive/last_accepted ...'`. The test was extended rather than a new
   one added, so no smoke-tier test was added: the tier stays at 3,890 items,
   on its `max-tests` ceiling (`test_smoke_budget.py` passes).
   - LLR-369 `detail`, the link sentence's close, was "the link text, prose
     and code spans keep their words, and a file that is not UTF-8 is left
     untouched and named." It is now "the link text, prose and code keep their
     words, so a link inside an inline code span, a run of backticks up to the
     next run of the same length in its paragraph, or inside a fenced code
     block, opened by a line of three or more backticks or tildes and closed
     by a line of at least as many of the same, is not rewritten; and a file
     that is not UTF-8 is left untouched and named."
   - TC-427 `method` names the new page.
2. **Adopted** (Sol): SR-247 stated the link rewrite in every Markdown file
   outside the skipped folders, while LLR-369 and the code except the
   operator's scratchpad, so the child exceeded its parent. SR-247
   `acceptance_criteria`, its link sentence, was "In a Markdown file outside
   hidden, vendored-package and cache folders it re-bases a link target naming
   the record's earlier directory onto the current one, and changes no link
   text and no prose." It is now "In a Markdown file outside hidden,
   vendored-package and cache folders, the operator's scratchpad at the
   repository root excepted, it re-bases a link target naming the record's
   earlier directory onto the current one, and changes no link text, no prose
   and no text inside an inline code span or a fenced code block." The
   scratchpad exception is driven by D7's test, the code clause by finding
   1's; the code clause makes the parent state what LLR-369 now states.
3. **Adopted in part** (Sol): LLR-369 stated the current-vocabulary skip
   twice. The first statement, in the reading paragraph, was "Finding none,
   the steps run, and the record step writes no registry copy." It is now
   "Finding none, the steps run."; the skip is stated once, in the record
   step's paragraph ("In a record whose ledger lists kept rows, with no
   earlier spelling found, it writes no copy, ..."). LLR-369 still states
   every step of the migrator in one row, as it did before this branch;
   decomposing it is a separate re-cut, which the coordinator notes for the
   stale-text list.

The cells these fixes move were already owed (SR-247 `acceptance_criteria`,
LLR-369 `detail`, TC-427 `method`), so the acts owed above are unchanged.
The absolute-term rule still finds nothing in SR-247's acceptance or
LLR-369's detail.

Tests of the round-1 fixes:
- `tests/test_migrate_vocabulary.py tests/test_migrate_vocabulary_record.py`:
  `93 passed in 16.17s` (the same 93 items as before the round).

<!-- fig: cmd="python -m pytest -q -p no:cacheprovider --basetemp <scratch> tests/test_migrate_vocabulary.py tests/test_migrate_vocabulary_record.py" rev="e425d4173 plus the round-1 fixes, uncommitted, 2026-11-23" -->

- `test_complexity_ratchet`, `test_module_size_ratchet`, `test_import_layers`
  and `test_smoke_budget`: `16 passed in 13.91s`; `check_complexity.py
  --mode enforce`: `OK - 168 row(s) over 15, unchanged from baseline.` The
  migrator is 926 SLOC against the 1,000 threshold.
- `trace.py --root . --strict`: exit 0, `Traceability: SN=31 SR=141 LLR=368
  TC=444 orphans=0 integrity=0 ...`; `check_trajectory.py --root . --strict`:
  exit 0, `check_trajectory: clean (1066 work item(s), 936 done (88%), 37
  cancelled, graph acyclic).`
- No smoke rerun: no smoke-tier test was added.

Round 2 (2026-11-23, narrow, over `e425d4173..809e610f2`): Gemini Hydrogen
`APPROVE findings=0`; OpenAI Sol one new MINOR, confirmed by execution: a
backtick escaped by a backslash was read as a code span's delimiter, so a
link written in prose between two escaped backticks was left unrewritten.
**Adopted** by the coordinator, and fixed on this branch: `_inline_spans`
reads a backtick escaped by an odd run of backslashes, where a span would
open, as a literal (the rest of its run, if any, still opens), while a
span's closing run reads no escape, since code holds none (CommonMark). The
regression is the same links test, whose code page gains three paragraphs:
a link in prose between two escaped backticks (moves), a backtick after an
escaped backslash opening a span around a link (stays), and a span whose
closing backtick follows a backslash with a link after it (moves). Red
before the fix:
`FAILED tests/test_migrate_vocabulary.py::test_links_into_the_record_follow_it_and_every_other_word_stays`,
on `assert 'docs/reviews/code.md: 3 link(s)' in 'migrate_vocabulary:
acceptance-record link rewritten: docs/reviews/code.md: 2 link(s) ...'`.
TC-427's `method` names the three paragraphs (a cell already owed). LLR-369
and SR-247 are unchanged: an escaped backtick is not a run of backticks, so
their "inline code span" already excludes it. After the fix: the two
migrator modules `93 passed in 16.39s`; with the ratchets and
`test_import_layers`, `105 passed in 12.83s`; `check_complexity.py --mode
enforce`: `OK - 168 row(s) over 15, unchanged from baseline.`; `trace.py
--root . --strict` and `check_trajectory.py --root . --strict` exit 0.
<!-- fig: cmd="python -m pytest -q -p no:cacheprovider --basetemp <scratch> tests/test_migrate_vocabulary.py tests/test_migrate_vocabulary_record.py" rev="809e610f2 plus the round-2 fix, uncommitted, 2026-11-23" -->

## Context

Filed on trunk on 2026-11-23 by the queue drill's coordinator, from
WI-1060's review (Sol, round 1, a MAJOR the coordinator recorded as this
follow-up) and its plan's eighth decision.

WI-1060 makes an acceptance act write only the rows it names, and judges
each later write of the record at the row once the record holds an act
carrying kept rows. The vocabulary migrator's record step (SR-247,
LLR-369) writes every record copy equal to live, absorbing drift by design
(the test-tiers plan's D13, operator-ruled). In a record that holds a
row-by-row act with a row still kept, that write carries the kept row's
live text into the record without an act, and the hook refuses the commit.
So after an adopter's first act on the new kit, the migrator's record step
no longer lands while any row is owed. WI-1060's RESYNC entry tells
adopters to run the migrator before that first act.

**The design call is the operator's.** SR-179 says the record is written
only by copying live text. The migrator's absorption was ruled because a
vocabulary move changes spellings, not meaning. The candidates:
- (a) The migrator rewrites the spellings inside each record copy in
  place, leaving every row's own text, so a kept row stays kept in the new
  spelling. This writes the record other than by copying live, so SR-179
  and SR-247 are amended to allow that one kind of write.
- (b) The migrator's record write becomes an act of its own. It names the
  rows whose only difference from live is spelling, keeps every other
  drifted row, and adds a ledger entry, so the row-by-row judge passes it.
- (c) Nothing changes beyond WI-1060's RESYNC guidance: run the migrator
  before the first row-by-row act, and refuse it after with a message
  saying so.

**Operator ruling (2026-11-23): refined (c).** Keep SR-179's mirror
invariant untouched and keep the vocabulary migrator standalone (no
compatibility readers in the mirror judge and no forged acceptance acts).
Once the record's act ledger holds any entry carrying `kept` (even an
empty list, which turns on the row-by-row judge for every later write):
- **Record already in the current vocabulary** (current directory name,
  current ledger keys, no earlier spellings in record copies): skip
  writing record copies from live, so running the migrator (or `--check`)
  for non-record files leaves kept and pending-drift rows untouched,
  exits 0 when nothing else is owed, and lands cleanly past both the
  commit hook and the committed-history check.
- **Record still carrying earlier vocabulary** (earlier directory name,
  earlier ledger keys, or earlier spellings in a record copy): refuse
  before writing any record file — including in the registry step, which
  currently walks the record directories before the record step runs —
  exit 1, and point to WI-1060's RESYNC guidance (run the migrator
  before the first row-by-row act).
- **Pre-row-by-row records** (no ledger entry carrying `kept`): keep
  today's behavior unchanged.

SR-179 and LLR-178 need no amendment; only SR-247, LLR-369 and TC-427
take text-only amendments.

Operator's choice recorded. Critiqued 2026-11-23 (Sol and Hydrogen;
`docs/reviews/2026-11-23-scope-critiques/WI-1065.md`): `planmode` is
`single`, since the row promises behaviour over three record states, and
its promises are bounded below.

## Done-when

- [x] The operator's choice among (a), (b) and (c) is recorded here.
- [x] In a record whose act ledger carries `kept` (including with a kept
      row), the migrator skips record copies when the record is already
      in the current vocabulary (so non-record rewrites pass the commit
      hook and the committed-history check, and `--check` does not flag
      pending drift) and refuses before modifying any record file —
      including in the registry step — when the record still stores
      earlier vocabulary; tests cover both paths and verify the commit
      hook and the committed history.
- [x] Coverage bound: the skip and the refusal reach records the kit's
      own routes produced (acts taken through the snapshot command, the
      migrator's own earlier runs); a hand-edited record copy, ledger or
      stamp is outside them (PROCESS.md §6, "Review threat model").
- [x] Any accepted row this changes is amended (text only, no code names)
      and listed as owed to adjudication.
