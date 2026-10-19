# WI-918 implementation plan: an attended re-claim closes a loop lane's trailer window

Spec: `docs/work/active/wi-918/WI-918-reclaim-reader.md`. Its spec of record
is `docs/plans/2026-10-11-review-churn/README.md`, "Owner rulings,
2026-10-11", revision 36's "Headless coordinator legs are marked now" (a lane
claimed headless lands headless, or the attended coordinator re-claims it
before committing in it; how a re-claim clears the loop mark is P9's design),
with the owner's 2026-10-14 split ruling (WI-918 takes the slot's reading of
the re-claim), `docs/decisions/coordinator-2026-10-14.toml` D-015 (the
lane-mode reading: any lane a headless leg marked, by its claim or a
loop-writer commit) and D-017 (design call Q3: an unmarked, empty,
subject-typed commit in the lane, read by the window), and
`docs/decisions/coordinator-2026-10-18.toml` D-005 C4 (the launcher's lane
audit and `check-lane` join the consumers). Rulings 1 (deny by default) and
2 (record at the event, checked against its parent) bind the reader's shape.
Where this plan and a ruling differ, the ruling governs.

Read for this plan: the spec in full; the rulings section of the plan of
record; D-015, D-017 and D-005; `kitlib/provenance.py` (IF-194);
`integrate.py`'s `_loop_claimed`, `_loop_window`, `_held_status_refusal` and
`_loop_trailer_refusal`; `scripts/coordinator/overnight_legs.py`
(`log_records`, `lane_claimed`, `lane_refusal`, `check_lane`); the
`coordinator-cycle` SKILL.md section 7 and `references/recipes.md` section 0
(`$PY`, `$SCRIPTS`); `tests/test_loop_provenance.py`,
`tests/test_overnight_legs.py` (`FakeGit`, `LANE_CASES`),
`tests/test_overnight_legs_git.py` and `tests/overnight_legs_fixtures.py`
(`lane_setup`, `lane_commit`); `tests/conftest.py` `SLOW_MODULES`; SR-209
in `docs/requirements/system-requirements.toml`; LLR-248 in
`docs/requirements/low-level-requirements.toml`; TC-242 and TC-321 in
`docs/test/test-cases.toml`; IF-194 in `docs/requirements/interfaces.toml`;
CMP-008 in `docs/requirements/components.toml`; Flows 4 and 6 of
`docs/runtime-flows.md`; the newest `RESYNC_PACK.md` entries for their shape.

## The architectural-delta answer

Yes, and within scope, as the spec states. No preparatory refactor is
needed and no new boundary is crossed.

- **A new state:** a lane's trailer window can close again, so a lane goes
  from the loop's window back to a person's (P1).
- **A new domain value:** the re-claim subject, `reclaim: <branch>
  (attended)`, in the grammar the window reads, with one composer (P1).
- **A new input:** the slot's trailer window, and the launcher's lane audit
  that calls the same reader, now depend on each lane commit's parents and
  tree and on the trees of the range's boundary parents (P1, P3, P4).
- **An interface amendment, not a new interface:** IF-194's vocabulary gains
  `reclaim_subject`, and `loop_lane_window`'s records gain parents and tree
  (P1 in code, P7 in the row). CMP-008 already owns both the module and the
  slot, so no component row changes. No runtime flow depicts the trailer
  window (Flow 4 shows the slot's merge, Flow 6 the act turn's trailer), so
  `docs/runtime-flows.md` is unchanged; P7 confirms that at the checkpoint.

Rows P1, P3, P4 and P7 carry the change: the reader, its two callers, and the
interface and spine rows that state it.

DELTA: within

## Design decisions this plan fixes

1. **The record shape the reader takes.** `loop_lane_window(commits,
   claimed, branch, boundary)`:
   - `commits` are the lane's records, oldest first, each `(sha, message,
     parents, tree)`, `parents` a tuple of shas;
   - `boundary` maps each parent sha outside the range to its tree;
   - it returns the judged records in the same shape, or None.
   The emptiness check needs a parent's tree, and the lane's first commit,
   the commonest re-claim (an attended coordinator's first commit in a lane
   claimed under the marker), has its parent on trunk, outside the range.
   Both callers get every boundary tree from the one `git log` they already
   run, by adding `--boundary` and the `%m` mark: a record marked `-` is a
   boundary commit, whose tree goes into `boundary` and never into the
   window. No second git read is added, and no new failure path: the range
   read already refuses (slot) or stops (launcher) when git fails.
2. **The re-claim test, deny by default** (ruling 1; the spec's S3). A
   record is a re-claim only when all four hold:
   - exactly one parent;
   - its tree equals that parent's tree, looked up in the range or in
     `boundary`; a parent found in neither fails the test (never assumed
     empty);
   - its subject, as `_subject` reads it, equals `reclaim_subject(branch)`
     exactly;
   - its final trailer block holds no `Loop-Session` key at all
     (`_last_loop_value(message) is None`, so an empty or malformed value is
     a trailer and fails this).
   Anything else is "neither" and is judged like any other commit.
3. **The window walk**, one pass oldest first:
   - the window starts open when `claimed`;
   - a loop-writer commit (`loop_writer_commit`) opens it and is judged;
   - a re-claim met while it is open closes it and is not judged itself;
     one met while it is closed changes nothing;
   - other commits are judged only while it is open;
   - the result is None when the lane was never marked (no claim mark, no
     loop-writer commit), else the judged list, possibly empty, so
     `_held_status_refusal`'s `window is None` test still judges any marked
     lane whole.
   Before a first mark, the result is as today: the commits before it stay
   outside the window.
4. **The composer.** `reclaim_subject(branch)` returns
   `"reclaim: {} (attended)".format(branch)`, byte for byte WI-917's
   literal. It carries no ` -> active/... (bookkeeping)` suffix, so no claim
   reader matches it, and it matches no `LOOP_WRITER_SUBJECTS` pattern. A
   test pins both facts.
5. **Callers change only their read.** `integrate._loop_window` extends its
   format to `%m%x00%H%x00%P%x00%T%x00%B%x1e` with `--boundary`, splits off
   boundary records and hands both to the reader. Its permissive handling of
   a sha-less record stays as is (no further change, the spec's deliverable
   2). The two rungs unpack `sha, message` from the records they iterate.
   The launcher gets a lane-only reader, `lane_records`, with the same
   format and its strict parse (an unparseable record is an `AuditStop`
   naming it, as `log_records` rules today). `log_records` keeps serving
   trunk, the archive and the claim log unchanged. Two parsers of one format
   remain, the slot's and the launcher's, as two do today. Folding them into
   one is a separate finding for the coordinator, not this row's change (see
   "Findings outside scope").
6. **The skill's recipe composes the subject through the kit.** Both recipes
   in section 7 take the subject from `reclaim_subject`:
   - `SUBJ=$("$PY" -c "import sys; sys.path.insert(0, '$SCRIPTS'); from
     kitlib.provenance import reclaim_subject; print(reclaim_subject('<branch>'))")`;
   - then `git commit --allow-empty -m "$SUBJ"`;
   - the missed-re-claim replay passes `-m "$SUBJ"` to `commit-tree`.
   The "until WI-918 lands" sentences in section 7 (the re-claim step and "A
   leg's landing") become the reader's rule: the slot and `check-lane` read
   the re-claim, so a leg may land a lane holding one after `check-lane`
   passes.

## Plan table

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | The re-claim composed once and read once in `kitlib/provenance.py`: `reclaim_subject(branch)`; `loop_lane_window` over `(sha, message, parents, tree)` records and a boundary-tree map, with the four-part re-claim test and the window walk of decisions 2 and 3; the module narrative and the `Contract IF-194:` docstring name both, state the record shape and the one exception to "a forged loop-writer subject only makes a lane MORE governed", and cite revision 36, D-015 and D-017 | D1; SR-209 | IF-194 (the vocabulary gains `reclaim_subject`; `loop_lane_window`'s records gain parents and tree) | |
| P2 | Tests in `tests/test_loop_provenance.py` on real git repositories, one per Done-when clause, each holding a genuine-re-claim control that the pre-change reader refuses; plus the composer's two pins | D2; D3; D4; D5; D6; D7; D8; D9; SR-209; TC-242 | IF-194 (the tests drive the reader through the slot's rungs, IF-194's consumer) | P1 |
| P3 | The merge slot hands the reader what the emptiness check reads: `integrate._loop_window` reads `%m`, `%P` and `%T` with `--boundary` and passes the boundary trees; `_loop_trailer_refusal` unpacks the records; the docstrings of `_loop_window`, `_loop_trailer_refusal` and `_held_status_refusal` state the re-claim (closes the trailer window only; the held-status rung judges a re-claimed lane whole), citing D-017; the size ratchet entry for `integrate.py` re-stamped if the measured count moves | D1; SR-209 | IF-194 (integrate is a requestor of `loop_lane_window`; the call's arguments change, its role does not) | P1 |
| P4 | The launcher reads a re-claim as the slot does: `overnight_legs.lane_records` (the slot's format and `--boundary`, strict parse) feeds `lane_refusal`; the module docstring's audit paragraph and `check-lane` text name the re-claim, citing D-005 C4; `tests/test_overnight_legs_git.py` gains the `check-lane` pair; `tests/test_overnight_legs.py`'s `FakeGit` lane answer and `records` helper carry the new fields, and `LANE_CASES` gains re-claim cases as the smoke-tier pin | D1; D10; SR-209 | IF-194 (the launcher calls `loop_lane_window` and `loop_trailer_refusal`; it is this repo's tooling, outside the kit, so the row names no new requestor) | P1; P3 |
| P5 | The `coordinator-cycle` skill's section 7: the re-claim step composes the subject through `provenance.reclaim_subject` (decision 6), the module now the subject's one home; the two "until WI-918 lands" sentences become the reader's rule; the copies in `.claude/skills/` and `.agents/skills/` synced with `bootstrap.py --dest . --sync` and checked byte-identical | D1; D13; SR-209 | IF-194 (the recipe calls `reclaim_subject`, a new caller outside the kit) | P1; P4 |
| P6 | `RESYNC_PACK.md` entry: "The merge slot reads an attended re-claim in a loop lane", anchored per the pack's convention; kit-owned files to overwrite `scripts/kitlib/provenance.py` and `scripts/integrate.py`; no forced migration, since no adopter lane carries a re-claim and every window reads as before | D12; SR-209 | IF-194 (the entry describes the vocabulary's amendment to adopters) | P1; P3 |
| P7 | The trace rows, authored by Terra's retained session at the lane's checkpoint and sat: SR-209's acceptance, LLR-248 (`code_symbol` gains `reclaim_subject`; `detail` states the re-claim reading and the record shape), TC-242 (`method` and `expected` gain the re-claim cases and the launcher test is named in the method only as evidence of the slot's reading, not as a TC file), and IF-194 (`data` and `rationale`); the act through WI-912's act turn, `coordinator_adjudicate.py act --verdict <path> --wi WI-918`; CMP-008 and the runtime flows confirmed unchanged | D11; SR-209; TC-242 | IF-194 (the row of record is amended) | P2; P3; P4; P5; P6 |
| P8 | The plan gate: this plan, produced after the claim, committed verbatim, passes `plan_coverage.py --item` and the independent critique from another model family before any build | D14 | no interface (a process step; intra-module escape) | |
| P9 | The bar on the landing tip: `run_menu.py smoke` within its 60 s budget; `check_trajectory.py --strict` clean; `trace.py --strict` with no finding beyond LLR-292's; the two slow modules run explicitly; the full suite once at close, which runs TC-242 and TC-321 | D15; D16; D17; D18; SR-209; TC-242; TC-321 | no interface (a verification step; intra-module escape) | P7; P8 |

No clause is excluded: every D# clause is covered by a row above, SR-209 is
cited, and both TCs verifying it are named. TC-242 is amended (P7) and run
(P2, P9). TC-321 verifies SR-209 through the act turn's trailer line,
which this row does not touch; P9 runs it unchanged.

## Build order and commits

Three build stages on one builder, each stopping for the coordinator to
verify and commit before the next is released (recipes section 1):

- stage 1: P1, P2 and P3 together, because the slot tests drive the reader
  through `_loop_window`;
- stage 2: P4;
- stage 3: P5 and P6.

P7 is the checkpoint, after the counted review rounds. P8 precedes the
build, and P9 is the coordinator's check on the landing tip. Every stage
commit passes the commit bar (`run_menu.py smoke`). It also runs
`tests/test_loop_provenance.py` and `tests/test_overnight_legs_git.py`
explicitly, because both are in `SLOW_MODULES` and the smoke tier drops them.

Every new test is written before its code and run red against the lane's
base, in a detached scratch worktree at the base commit with the new tests
copied in, never by stashing. The red output goes in the lane report.

**Lane collision.** WI-946, claimed beside this row, deletes
`integrate._loop_claimed` and `overnight_legs.lane_claimed` and edits
`_loop_window` and `lane_refusal`, the same functions P3 and P4 edit. Its
`needs` carries `~WI-918`, so this row lands first and WI-946 rebases onto
it. This lane does not touch the claim readers.

## Steps in detail

### P1: the composer and the reader (D1)

In `project-trajectory/scripts/kitlib/provenance.py`:

- add `reclaim_subject(branch)` beside `LOOP_WRITER_SUBJECTS`, with an
  `Implements: SR-209, LLR-248` line and a comment stating that it is the
  subject's one home and that the coordinator-cycle recipe calls it;
- add a private `_reclaim(record, branch, trees)` holding decision 2's four
  tests;
- rewrite `loop_lane_window(commits, claimed, branch, boundary)` as
  decision 3's single walk;
- in the narrative's "WHOSE LANE IT IS" paragraph:
  - add the re-claim: the attended coordinator's empty, unmarked commit in
    the lane closes the window for the commits after it;
  - state the exception in place of the sentence it qualifies: a forged
    loop-writer subject still only makes a lane more governed, and the
    re-claim is the one record that makes it less governed, held to one
    rung, to the commits after it, and to a shape checked against its
    parent at every read;
  - cite revision 36, D-015 and D-017;
- rewrite the `Contract IF-194:` docstring's last sentence to the new
  signature and add `reclaim_subject`.

The module stays pure and stdlib-only. It reads no git: the shapes arrive as
data.

### P2: the slot tests (D2 to D9)

New tests in `tests/test_loop_provenance.py`, under the existing "TC-242:
the merge ladder" heading, built on `_closed_lane`'s claim (marked or not),
`_loop_writer_commit`, `_trailered` and `_commit`. A local helper writes a
re-claim the way the recipe does:

- an unmarked porcelain `git commit --allow-empty -m <subject>` on the lane,
  with the marker removed;
- variants for the negative cases: a trailer appended, a file changed, or a
  second parent through `commit-tree -p A -p B`.

Each test asserts through `integ._loop_trailer_refusal` (and
`_held_status_refusal` for D8), so the slot's real git read is exercised.
Each holds a control: a genuine re-claim admitting the unmarked commit after
it. On the base, the old reader never closes the window, so that control is
refused, and `provenance.reclaim_subject` does not exist. That is why each
test fails before the change.

- **D3:** `test_a_reclaim_closes_a_marked_claims_window_for_the_commits_after_it`.
  The lane is claimed under the marker, gets a re-claim, then an unmarked
  file-changing commit: the rung returns None. The same unmarked commit
  placed before the re-claim is refused, naming its subject and sha.
  - Fails before: the after-commit is refused.
- **D4:** `test_a_lane_marked_by_a_sitting_is_judged_from_its_telemetry_and_a_reclaim_clears_it`.
  The lane is claimed attended, then gets a telemetry commit (marked), then
  an unmarked commit, which is refused (judged from the telemetry commit). A
  second lane holds the same commits with a re-claim between the telemetry
  commit and the unmarked one, and passes.
  - Fails before: the second lane is refused.
- **D5:** `test_a_reclaim_carrying_a_trailer_or_naming_another_branch_is_not_one`.
  Three forged re-claims, each followed by an unmarked commit:
  - a well-formed `Loop-Session` trailer: the rung refuses the commit after
    it, so the window stayed open;
  - a malformed trailer (`Loop-Session:` with an empty value, and one
    outside the session grammar): the rung refuses the re-claim itself,
    malformed;
  - `reclaim_subject("wi-999")` in lane `wi-401`: the rung refuses the
    re-claim itself, no trailer.
  - Control: the genuine re-claim passes. Fails before: the control.
- **D6:** `test_a_reclaim_subject_on_a_commit_that_changes_the_tree_or_merges_is_refused_naming_it`.
  The exact subject, no trailer:
  - with a file changed, it is refused, the refusal naming its subject and
    sha prefix;
  - as a two-parent commit whose tree equals its first parent's, it is
    refused the same way;
  - in both, the window stays open for the commit after it.
  - Control as above. Fails before: the control.
- **D7:** `test_a_marked_loop_writer_commit_after_a_reclaim_reopens_the_window`.
  Marked claim, re-claim, a telemetry commit (marked), then an unmarked
  commit: refused, naming it. Without the telemetry commit: passes.
  - Fails before: the second half.
- **D8:** `test_a_lane_never_marked_stays_a_persons_and_the_held_status_rung_judges_a_reclaimed_lane_whole`.
  - A person's lane holding a re-claim and unmarked commits: `_loop_window`
    returns `(None, None)` and both rungs return None.
  - A lane claimed under the marker, re-claimed, then given an attended
    commit that moves a held status (the dial and a registry row written
    with the module's `_write`, `_dial` and `_rows` helpers): the trailer
    rung returns None, and `_held_status_refusal` refuses, naming the
    registry, the row and the held rung.
  - Fails before: the trailer rung refuses the attended commit.
- **D9:** `test_a_reclaim_written_literally_by_wi_917s_recipe_is_read_as_a_composed_one`.
  - `provenance.reclaim_subject("wi-401") == "reclaim: wi-401 (attended)"`.
  - A lane re-claimed with the literal string through `git commit
    --allow-empty -m` and one re-claimed with the composed subject judge the
    same (both None).
  - The missed-re-claim replay, `commit-tree <last>^{tree} -p <last>` then
    `rebase --onto`, also yields a re-claim the rung reads.
  - Fails before: the composer is absent and both lanes are refused.
- **The composer's pins:** in the same file, a pure test. The subject
  matches no `LOOP_WRITER_SUBJECTS` pattern for any branch tried, and
  matches no claim subject: it does not end with ` -> active/<branch>
  (bookkeeping)`. It fails before because the composer is absent.

The module's docstring gains one bullet naming the re-claim among the
pieces pinned.

### P3: the slot's read (D1)

In `project-trajectory/scripts/integrate.py`:

- `_loop_window` gains decision 5's format and `--boundary`;
- records marked `-` fill the `boundary` map, and the rest become `(sha,
  message, tuple(parents.split()), tree)`;
- the reader call passes `boundary`;
- `_loop_trailer_refusal` iterates `for sha, message, *_rest in window`.
  `_held_status_refusal`'s code is unchanged.

The three docstrings are reworded in the module's voice:

- `_loop_window`: the window can close at a re-claim;
- `_loop_trailer_refusal`: a person's commit in a loop lane is refused
  unless it follows the lane's re-claim, and the forged-shape refusal;
- `_held_status_refusal`: a re-claimed lane is still judged whole, until
  WI-851.

The `integrate.py` entry in `tests/test_module_size_ratchet.py` is
re-stamped, with the measured count and a reason naming the record read, if
the count moves. The complexity census is checked for `_loop_window`.

Tests: P2's tests run through this read. No separate case is needed. A
`--boundary` read that loses a boundary tree would make D3's control fail
(its re-claim's parent is the trunk claim commit), so D3 pins the boundary
handling.

### P4: the launcher (D10)

In `scripts/coordinator/overnight_legs.py`:

- `lane_records(repo, trunk_tip, branch)` runs the lane read with decision
  5's format and `--boundary` through the checked `read`, and returns
  `(records, boundary)`. An unparseable record (missing fields, a sha
  outside `SHA_RE`, or a mark other than `-`, `>` or empty) is an
  `AuditStop` naming it;
- `lane_refusal` calls it and hands both to the reader, iterating
  `sha, message, *_rest`;
- the docstring's audit bullet and the `check-lane` paragraph state that a
  re-claim closes the window as at the slot, citing D-005 C4.

Tests:

- **`tests/test_overnight_legs_git.py`:**
  `test_check_lane_reads_a_reclaim_as_the_merge_slot_does`.
  - `lane_setup(repo, WELL_FORMED, [WELL_FORMED])`, then `lane_commit(repo,
    provenance.reclaim_subject("wi-1"))` (an empty commit-tree commit, one
    parent), then `lane_commit(repo, "lane work 2")` (unmarked):
    `check-lane` exits 0.
  - The same with the unmarked commit before the re-claim: exit 3, naming
    `lane work 2`.
  - Both cases also assert that the slot's rung agrees on the same repo
    (`integ._loop_trailer_refusal`), which is what "exactly as the trailer
    rung judges them" asks.
  - Fails before: the first case exits 3, since the launcher reads no
    re-claim.
- **`tests/test_overnight_legs.py`** (the smoke-tier pin):
  - the `records` helper and `FakeGit`'s `lane` answer move to the new
    format;
  - `LANE_CASES` gains "a re-claim closes the window" (marked claim,
    re-claim, unmarked: no refusal, window 0) and "a re-claim that changes
    the tree is refused" (named);
  - a malformed lane record stops the audit.
  - Fails before: the first new case is refused, and the old parser rejects
    the new record shape.

### P5: the skill (D1, D13)

In `project-trajectory/skills/coordinator-cycle/SKILL.md` section 7:

- the re-claim step's opening sentence drops "until WI-918 moves it" and
  names `provenance.reclaim_subject` as the subject's one home;
- both recipe lines take decision 6's `SUBJ=...` form;
- the "Until WI-918 lands, nothing reads that commit" bullet becomes the
  reader's rule: the merge slot's trailer rung and `check-lane` read the
  re-claim; it closes the window for the commits after it, only when it is
  empty and unmarked; a later loop-writer commit re-opens it;
- "A leg's landing" drops its "Until WI-918 lands" sentence.

Then run `bootstrap.py --dest . --sync`, and check the three copies are
byte-identical (diff, and the per-agent skill check). The skill is `scope:
this-repo`, so it gets no RESYNC entry. `test_overnight_legs.py`'s section
cross-reference pins must stay green.

### P6: the RESYNC entry (D12)

Append an entry in the newest entries' shape:

- the heading, with `[since <sha>]` anchored at the preceding commit and its
  italic note;
- **What changed:** the merge slot's loop-lane trailer window now closes at
  an attended re-claim, an empty, unmarked commit with the subject
  `reclaim: <branch> (attended)`, and re-opens at a later loop-writer
  commit; `loop_lane_window` takes records with parents and tree, and a
  boundary-tree map;
- **Kit-owned files — overwrite:** `scripts/kitlib/provenance.py`,
  `scripts/integrate.py`;
- **What to do:** overwrite the two files. Nothing migrates: no adopter lane
  carries a re-claim, so every window reads as before. An adopter's own
  caller of `loop_lane_window`, if any, passes the new record shape.

### P7: the trace rows and the act (D11)

At the checkpoint, after the counted rounds, Terra's retained session
authors the amendments from the settled code, in capability voice (ruling
5: no file or function in SR cells):

- **SR-209 `acceptance_criteria`:** after "a lane that is not the loop's is
  not judged", add one clause. An attended re-claim recorded in the lane (a
  commit that changes nothing against its one parent, names this lane in
  the re-claim form, and carries no trailer) ends the loop's window for the
  commits after it. A commit that fails any of those is judged like any
  other. A later loop-writer commit re-opens the window. The
  `requirement` cell is unchanged: "a lane the loop owns" already reads
  correctly.
- **LLR-248:** `code_symbol` gains `reclaim_subject`. `detail` gains the
  re-claim reading, the record shape with boundary trees, and the
  single-composer rule. `module` is unchanged.
- **TC-242:** `method` gains the re-claim cases of P2. `expected` gains the
  clause SR-209 gained. `evidence` is unchanged.
- **IF-194:** `data` adds `reclaim_subject` and the record shape.
  `rationale`'s "which commits mark a lane as the loop's" gains "and which
  attended record closes it". `requestors` are unchanged.

Then the closure check, the sitting, and the act through WI-912's act turn:
`coordinator_adjudicate.py act --verdict <path> --wi WI-918`. SR-209 sits on
a rung this repo's dial releases (the spec's B4), so the act is the
adjudicator's. At the same point the coordinator confirms that CMP-008 and
Flows 4 and 6 need no change. The generated `docs/interface-reference.md` is
regenerated on trunk at the landing, never committed in the lane.

### P8: the plan gate (D14)

This plan is written after the claim. The coordinator commits it verbatim,
then `plan_coverage.py --item` and the cross-family critique run before any
build.

### P9: the landing bar (D15 to D18)

On the landing tip:

- `run_menu.py smoke`, its smoke tier within the 60 s budget;
- `check_trajectory.py --strict`, clean;
- `trace.py --strict`, with no finding beyond LLR-292's;
- the two slow modules, run explicitly;
- the full unfiltered suite once at close, which runs TC-242's and TC-321's
  modules.

The real output goes in the lane report.

## Findings outside scope

These are surfaced for the coordinator, not fixed here:

- The slot (`integrate._loop_window`) and the launcher
  (`overnight_legs.lane_records`) parse one lane-log format twice, with
  different failure rules: the slot skips a sha-less record, and the
  launcher stops on it. This is the same shape as wi-917 D-003 F3, which
  WI-946 consolidates for the claim reader. One lane-record reader could be
  a follow-up beside it.
- IF-194's `owner` and `requestors` cells name code paths. Ruling 5 retires
  that, and this row leaves it to that program.
