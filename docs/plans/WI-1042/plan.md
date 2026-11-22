# WI-1042 plan, revision 1: the test-first order reads when each row was accepted from the acceptance record

Planned in the worktree `D:/ai-template-wt-wi1042`, branch `maint/wi-1042`, head `6915cde7d` (cut from trunk `refactor_again`).

Read in full: the spec `docs/work/queued/WI-1042-test-first-reads-ledger.md`; its specref `docs/reviews/2026-11-history-readers/README.md`, class (c) site 3; its scope critique `docs/reviews/2026-11-21-scope-critiques/WI-1042.md`; `check_test_first.py` and `tests/test_check_test_first.py`. Also read: in `baseline_snapshot.py`, the IF-123 and IF-220 contracts, the `ACTS` comment, `copy_live`, `_accepted_by_act`, `parse_acts`, `_acts_at`, `_ledger_commits`, `risk_acceptance_act` and `last_act`; in `acceptance_record.py`, `rows_at`, `acceptance_acts_between`, `_acceptance_act` and `added_ledger_entries`; `arch_seams._call_cover`; the record step of `migrate_vocabulary.py`; LLR-257, SR-217, TC-250, IF-198 and IF-220; and the test-tiers hand-off (`docs/plans/2026-11-11-test-tiers/HANDOFF.md`) at D3, §5 and §9.9.

## The ruling this plan builds on

The spec's first text read the record across the 2026-11-16 move. Before the move the record is in an earlier spelling: its directory `docs/archive/last_approved/`, the ledger's keys `approved`/`reattested` (in all 110 versions of the ledger there), and the copies' status `Approved` (seq 1's test-case copy holds 224 of them and no `Accepted`). D3 (the operator, 2026-11-11) rules out readers of an earlier spelling in the core tooling, and §9.9 declined this one for this check. The builder stopped and asked. The coordinator's ruling, 2026-11-22: D3 stands; option 2 with LLR-257's at-or-before reading. The move `2bee2b551` is the record's cut. Nothing before it is read. Every acceptance it carries is at or before the commit that brought it onto trunk's first-parent line (`f6dd5b87a`, the declared start). `_ledger_commits` keeps reading the current path only. The spec's Context, Trust ruling and Done-when are amended in this commit to say so.

## Completeness, measured on this repository (Done-when 1)

Measured before any reader change, by a scratch reader that was not committed. It walked the 120 commits from seq 1's parent (`94e82f339^`) to `6915cde7d` that touch the act ledger or the requirement, design or test-case copies under either directory. Each commit's copies were compared with every parent's: a flip is a row claiming acceptance in the commit's copy and in no parent's; a new pair is a test case accepted in the copy while naming a requirement, directly or through a design row's `sr_refs` in the same copy, in no parent's. Entries added are the `seq` numbers no parent's ledger holds.

- **Read in the current spelling only (the ruling):** one change carries flips or new pairs with no ledger entry: the move commit `2bee2b551`, with 852 flips and 694 new pairs. Before it, nothing reads accepted in the current spelling. It is the cut, not a gap. Since the cut, no change carries a flip or a new pair without an entry, and every act's flips and new pairs are named by the entry its commit added (a design-row re-pointing through the design row it names).
- **For the record, with the earlier spelling also read** (which the ruling excludes from the reader): no change since seq 1 is without an entry.

So no gap is filed, and no row is owed for one.

## Today's verdict, measured

`python project-trajectory/scripts/check_test_first.py --root . --src project-trajectory/scripts` at `6915cde7d` (57 s):

> test-first: OK - no requirement accepted since the declared start f6dd5b87a1 has a test case accepted after its implementation landed or not accepted

## The reading

`check_test_first.record_acceptances(root, rev)` replaces `first_acceptance_commits` and `first_association_commits`. It reads the record and never replays the registries.

1. **The record's commits.** `baseline_snapshot._ledger_commits` is the one walk. It gains two optional arguments: `also`, more of the record's files whose commits the walk takes too, and `rev`. The test-first reading passes the record's copies of the requirement, design and test-case registries (both carriers), so one `git log` lists every commit that wrote the ledger or one of those copies, at the record's current path only, with a shallow clone's boundary commits left out. `last_act` and `risk_acceptance_act` call it unchanged.
2. **Each commit against its parents.** The copies are read at the commit and at each parent through `acceptance_record.rows_at`, and judged with `acceptance_acts_between`, the acceptance-act rule, as the replay judged live rows. A row or pair is new at a commit when it is new against every parent, so a merge dates nothing its branch already dated.
3. **What each commit is:**
   - **The cut:** no parent holds the ledger or any of the three copies at the current path. Every acceptance its copies carry is at or before it (inexact). Here that is `2bee2b551`. In a repository whose record began at its first signing it is that commit, since a first copy cannot tell an acceptance it made from one it found.
   - **An act:** the commit added a ledger entry (`_acts_at`). Each row it carried into acceptance and each pair new in its copies is dated at it, exactly. LLR-257's rename rule stays: a move into `Accepted` from a word outside the status vocabulary is at or before the act, not exact.
   - **A gap:** neither, while its copies carry a flip or a new pair. Those rows and pairs are unread at it.
   - **A malformed ledger** at the commit or its parent (`ActLedgerError` from `_acts_at`): read as a gap. Its rows and pairs are unread.

   A row's or pair's first acceptance is kept: a later act never re-dates one the cut, a gap or an earlier act already dated.
4. **Order.** The trunk's first-parent line orders everything, as today. A record commit off that line is placed at the first first-parent commit that contains it (a binary search with `merge-base --is-ancestor`), which is how a landing is dated: a merge lands what it brings. The record commit's own id is the one reported.
5. **Requirements.** Each requirement's first acceptance in the record. A requirement claiming acceptance at the tip that no record commit accepted is unread. With a declared start: an acceptance placed at or before the start is out of scope; an exact one after it is judged; an inexact or unread one after it, or an unread one anywhere, is reported unread. With no start, every requirement is judged.
6. **Test cases.** A requirement's test cases are its chain's members at the tip, as today. A member not accepted at the tip is "not accepted". A member accepted at the tip is dated by its pair in the record. If the record holds it accepted but never while naming this requirement (a re-pointing awaiting its re-acceptance act), it is not accepted for the requirement. If the record never holds it accepted at all (no ledger, or an empty one), it is unread.

Removed: `first_acceptance_commits`, `first_association_commits`, `_touching` and `_carried_at`, the replay. Unchanged: `history_unreadable` (a shallow clone, a start that names no commit or is off the first-parent line, a start before the TOML registries, registries still under an older carrier), `first_implementation_commits`, the report's lines and IF-198's exits. An unread entry's line now says why: at or before a commit, a record change with no act, or no act on record.

## Trust states and the test for each (Done-when 4)

New tests in `tests/test_check_test_first.py` (in `SLOW_MODULES`). Acts are taken with the producer itself, `baseline_snapshot.copy_live`, as `intake.py snapshot` takes them; the fixture's first act seeds the record.

| Trust state | Produced in the test by | Expected |
|---|---|---|
| An entry and its adding commit readable | Acts committed with `copy_live`; a test case re-pointed in a text commit, then re-accepted by an act (text then act); an act made on a side branch and merged | Each row dated at its act's commit. The re-pointed pair is dated at the re-accepting act, not the text commit; that test is run on this head's code first and fails there (the replay dates the text commit). The side-branch act is ordered at its merge and named by its own commit |
| An acceptance before the cut | A record in the earlier spelling under `docs/archive/last_approved/` (keys `approved`/`reattested`, status `Approved`) with acts on it, then a move commit on a side branch respelling it into `docs/archive/last_accepted/`, merged | Every acceptance the move carries is at or before the move, ordered at the merge. A landing before the merge reads unread, one at or after it settles. Never dated at an earlier act in the old directory, never at a later act |
| No ledger, or an empty one, while a registry holds accepted rows | Accepted live rows, code landed, no record; and a record holding only an empty ledger | The requirement and its test cases read unread, never as a pass; `--strict` exits 1 |
| An adding commit beyond a shallow clone's window | A depth-1 clone (the existing test) | Not judged, never a pass |
| A gap | A commit that changes the test-case copy, flipping a row, with no ledger entry; a later act that copies the registry again | The flipped row's pairs read unread at the gap commit, never dated at the later act |
| A malformed ledger on the walk | An act whose committed ledger repeats a `seq` | The rows that act carried read unread |

The existing TC-250 cases move onto acts. Each first act seeds the record. Where a case needs an exact first date, it seeds on a placeholder row first. The CSV cases seed the record at the TOML cutover, the record's first copy there. The rename case takes its acts over copies that hold the retired word.

## Verdict changes (Done-when 5)

On this repository, none expected. Only one requirement was first accepted since the cut: SR-247, by seq 183 at `9b377be1e` on `maint/vocabulary`, which reached trunk at `f6dd5b87a`, the declared start, so it is out of scope. Every other accepted requirement is carried by the cut, which reaches trunk at the same commit, so none is in scope. The run after the build is quoted in the Deliverable, and any change is explained there.

Beyond this repository, three readings change, each a warning and never a pass:

- an acceptance the first signing carries is at or before it, so a landing before the first signing can no longer be ordered against it;
- a repository with no record reads its acceptances as unread;
- a re-pointing is dated at the act that re-accepts it, not at its text commit.

## Rows

- **LLR-257 (Accepted), text only:** the replay is replaced by the record reading above, with the cut, the gap, the unrecorded state and the side-branch order. Its `module` and `code_symbol` cells follow the code (`record_acceptances`; `baseline_snapshot.py`). It drifts; the re-acceptance is the act owed.
- **TC-250 (Accepted), text only:** two clauses describe the replay and no longer hold. "Dated at the re-pointing commit" becomes "dated at the act that re-accepts it". The clause dating a design-row pair at or before the design registry's move to TOML goes: a carrier move dates nothing now (its unreadable-start half stays). It drifts too, and its act is owed. This is the builder's call, recorded here because the brief named LLR-257 alone. A test case whose accepted method text no longer describes its tests would be stale evidence.
- **New, Drafted:** TC-468 (the act's commit dates its rows, the text-then-act re-pointing and the side-branch order), TC-469 (the cut), TC-470 (no record, or an empty ledger), TC-471 (a gap, and a malformed ledger on the walk). Each verifies SR-217 and LLR-257.
- **IF-220 (Drafted):** `consumers` gains `CMP-007`, and its notes name the test-first reading.
- No LLR is minted. The watermark is bumped with `trace.py --root . --bump-ids`.

## Architectural-delta answer

DELTA: within

- **States.** None new. The test-first verdict keeps its three readings (late, unread, not accepted).
- **Value domains.** The unread reading gains its reasons. IF-198's exits and line kinds are unchanged.
- **Output-on-input dependencies.** The check's dates now depend on the act ledger and the record's copies (IF-220), and on ancestry to place a side-branch act. They no longer depend on the live registries' history. The tip's rows still decide membership and standing.
- **Boundaries.** CMP-007 reads CMP-006's record. IF-220 gains CMP-007 among its consumers. The import edge CMP-007 to CMP-006 is already covered by `call` rows (IF-102, IF-308), so the cross-component rule's findings do not change.

## Build

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | Tests first, committed with P2: the Trust-state tests and the TC-250 cases moved onto acts. Run on this head's code first: the text-then-act test must fail there with the text commit's date | D3; D4; SR-217; TC-250 | IF-198; IF-220 | |
| P2 | `record_acceptances` and the judging over it; the replay removed; `_ledger_commits` takes `also` and `rev`; LLR-257 and TC-250 amended, TC-468 to TC-471 drafted, IF-220's consumers; ids bumped; views regenerated | D2; D3; D5; D6; SR-217; TC-250 | IF-220; IF-198 | P1 |
| P3 | Close: the Deliverable with the completeness result, the verdict on this repository, the byte deltas and the acts owed; the audit note's site 3 marked resolved by this row; the log fragment; the spec moved to `docs/archive/work/complete/` | D1; D7 | no interface: records only | P2 |

## Tests and checks

- **Run:** every module importing `check_test_first` or `baseline_snapshot` (grep, and `trace.py --tests-for`), `tests/test_import_layers.py`, `tests/test_module_size_ratchet.py` (`baseline_snapshot.py`, at 964 SLOC, stays at or under 1000), `tests/test_dogfood_sync.py`, `tests/test_complexity_ratchet.py`; then `run_menu.py smoke` before the last build commit. Also `trace.py --root . --strict`, `check_trajectory --strict` and `plan_coverage.py --item` over this plan.
- **On this repository:** the check itself, quoted in the Deliverable.
- **Generated views:** `trunk_step.py --root . --regen` before the build commit.
