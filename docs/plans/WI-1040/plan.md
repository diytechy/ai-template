# WI-1040 plan, revision 1: the re-acceptance brief dates the last acceptance from the act ledger

Planned in the worktree `D:/ai-template-wt-wi1040`, branch `maint/wi-1040`, head `dd8f79e6c` (cut from trunk `refactor_again`).

Read in full: the spec `docs/work/queued/WI-1040-last-act-date-from-ledger.md`; its specref `docs/reviews/2026-11-history-readers/README.md`, class (c) site 1; and its scope critique `docs/reviews/2026-11-21-scope-critiques/WI-1040.md`. Also read: in `baseline_snapshot.py`, `stamp`, `acceptance_stamp`, the `ACTS` comment, the IF-217 and IF-220 contracts, `parse_acts`, `read_acts`, `_shallow_commits`, `_acts_at`, `_act_names` and `risk_acceptance_act`; `acceptance_record.added_ledger_entries`; in `trace.py`, `reaccept_lines`, `_DERIVED_STAMP_PREFIXES` and `acceptance_check`; LLR-259, IF-126 and IF-217; and the tests that read the heading or the reader: `tests/test_baseline_snapshot.py` (the `acceptance_stamp` test), `tests/test_trace_briefs.py` (the provenance test and the golden brief) and `tests/test_accepted_risk.py` (the shallow-clone case).

## What the heading reads today, measured

At this head, `docs/ratify/CURRENT.md` line 16 reads: "the last commit to move a `Status` cell in a snapshotted registry is 458724024 (2026-11-21)". `458724024` is WI-1021's build commit. It accepted nothing. The last act is the ledger's seq 185, dated 2026-11-20, which `46d518b56` added. The heading names a commit that is not an act, which is the defect the spec describes.

## The reading reused

The accepted-risk reader finds an act's commit in three steps: it lists the commits that touched the ledger, newest first (`git log --format=%H -- docs/archive/last_accepted/acts.toml`); it drops a shallow clone's boundary commits (`_shallow_commits`), since their diff reads as if they added every entry; and it reads, for each commit left, the entries that commit added (`_acts_at`: those whose `seq` its parent's ledger lacks).

The heading reuses all three. The first two move into one helper that both readers call, so the walk has one home. `risk_acceptance_act` keeps its exact behaviour; only where it gets the list from changes. The new reader, `last_act(root)`, lives in `baseline_snapshot.py` beside it: the module that writes the ledger also reads it back, as IF-217's rationale says. It reads the working tree's ledger (`read_acts`), takes the newest entry (the last one; `parse_acts` refuses a ledger whose `seq` does not increase in file order), and walks the commits for the one that added that `seq`. It returns the entry, the commit or None, and one clause the brief states as its heading. `risk_acceptance_act` uses the same shape.

The walk stops early in one case. It stops at the first readable commit that added entries when every entry it added is older than the newest. The ledger only grows, and each new `seq` is one above the highest (IF-220), so no older commit can have added the newest entry. Without this stop, an act still in the working tree would read the ledger at every commit that ever touched it: about 180 in this repository, two `git show` calls and two parses each.

## The ledger states and the heading's outcome

The heading keeps its prefix, `_Acceptance provenance: `, so `acceptance_check` still sets it aside (`_DERIVED_STAMP_PREFIXES`). A commit reads by its first 12 characters, as the accepted-risk reasons do.

| Ledger state | The heading reads |
|---|---|
| No ledger file | no acceptance act is recorded: there is no act ledger `docs/archive/last_accepted/acts.toml` |
| A ledger with no entry | no acceptance act is recorded: the act ledger `…/acts.toml` holds no entry |
| The newest entry, and the commit that added it is readable | the last acceptance act is the act ledger's seq N, dated D, added by commit `<sha>` |
| The newest entry, and the commit that added it lies beyond a shallow clone's window, or is the window's boundary commit | the last acceptance act is the act ledger's seq N, dated D; its commit is not in the available history: this is a shallow clone, and the act may lie beyond its window |

Two more states are reachable in supported workflows. Each keeps the spec's rule: give the entry's date and never name another commit.

| Ledger state | The heading reads |
|---|---|
| The newest entry is not yet committed: an act made with `intake.py snapshot` whose commit is being made, when the views are regenerated before it lands | …seq N, dated D; its commit is not in the available history: no commit adds it yet, so the act is not committed |
| git cannot read the history: no git, not a checkout, or no commit yet | …seq N, dated D; its commit is not in the available history: git cannot read this repository's history |

Outside the promise: a malformed ledger, which only a hand edit makes (IF-220 and the spec's bound). The heading never raises and never guesses. A malformed working-tree ledger reads "no acceptance act can be read: the act ledger `…/acts.toml` is malformed (…)". A malformed ledger met on the walk reads "…seq N, dated D; its commit cannot be read: the act ledger at commit `<sha>` or its parent is malformed (…)". That wording follows `risk_acceptance_act`'s.

The CSV carrier now gets the same answer as TOML. The ledger is TOML whichever carrier the registries use, so the old reader's CSV case ("or git cannot say") goes away.

## Across the 2026-11-16 move

**The reused reading does not see across the move.** It counts an entry as added by a commit whose parent's ledger, at the current path, lacks its `seq`. At `2bee2b551` the ledger moved from `docs/archive/last_approved/acts.toml` to `docs/archive/last_accepted/acts.toml`. Measured at this head, the walk reads that commit as adding all 182 entries it held (seq 1 to 182), and the commit message says the same. The walk never reaches the old path, since `git log` runs without `--follow`.

This does not change the heading in this repository. The newest entry, seq 185, was added at `46d518b56` after the move, and the walk reaches that commit first. It would matter in a repository whose newest act is older than its own move of the record: one moved by `migrate_vocabulary.py`, with no act taken since. There the heading would name the move commit as the act's commit. `risk_acceptance_act` has the same limit for an assumption whose only acts are older than the move. This row does not fix it; the walk stays shared, so one change would fix both readers. It is reported to the coordinator as a finding, not built here.

## Architectural-delta answer

DELTA: within

- **States.** No new state. The heading is a derived, advisory line, rendered and computed by nothing.
- **Value domains.** The heading's text domain changes to the six outcomes above, plus the malformed one. No machine reads it: `acceptance_check` drops the line by its prefix, which stays the same.
- **Output-on-input dependencies.** The heading's inputs are now the working tree's act ledger, the ledger's git history and the shallow-clone list. The input it drops is the status-line diffs of the snapshotted registries.
- **Boundaries.** None crossed. `trace.py` and `baseline_snapshot.py` are both CMP-006, and `trace.py` already calls `baseline_snapshot`. IF-220 already declares the ledger, and IF-217 the walk.

## Build

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | Tests first, committed with P2. One test per ledger state in the tables above, and one through `trace.reaccept_lines` showing that a new draft committed after the last act leaves the heading on the act's commit. Run against this head's code first: the brief test and the state tests must be red | D1; D2 | no interface: tests only | |
| P2 | `baseline_snapshot.last_act` over the shared ledger walk, with `risk_acceptance_act` moved onto the walk unchanged; the brief's heading reads `last_act`; `acceptance_stamp` and its test removed; the CSV provenance test and the golden brief updated; the `ACTS` comment names the brief as a reader; the views regenerated | D1; D2 | IF-217; IF-220 | P1 |
| P3 | Close: the Deliverable, the audit note's site 1 marked resolved by this row, the log fragment, the spec moved to `docs/archive/work/complete/` | D3 | no interface: records only | P2 |

**Why D1 and D2 each span P1 and P2.** It is one change, split so the tests come first. P1 writes the tests and shows them red on this head's code. P2 writes the code that turns them green, and changes the existing tests that pinned the old heading. Both land in one build commit, so no commit holds a red test.

## Tests and checks

- **New, in `tests/test_baseline_snapshot.py`** (in `SLOW_MODULES`, so the smoke tier's count does not change): no ledger; an empty ledger; a readable adding commit; a depth-1 clone of a repository whose act is older than its newest commit; an uncommitted act; and the draft-after-the-act test through the brief. The old `acceptance_stamp` test goes.
- **Changed:** `tests/test_trace_briefs.py`'s provenance test, a CSV-carrier repository seeded in one act, now expects the seed's act and commit instead of the degrade. The golden brief, a tree with no git and no record, is regenerated with `UPDATE_BRIEF_GOLDEN=1`, and its provenance line becomes the no-ledger outcome.
- **Run:** every test module that imports `baseline_snapshot` or `trace`; `tests/test_import_layers.py`, `tests/test_module_size_ratchet.py` (`trace.py` should shrink and be re-stamped downward; `baseline_snapshot.py`, at 965 SLOC, must stay at or under 1000) and `tests/test_dogfood_sync.py`; then `run_menu.py smoke` before the last build commit. Also `trace.py --root . --strict` and `plan_coverage.py --item` over this plan.
- **Generated views:** `trunk_step.py --root . --regen` before the build commit, since `docs/ratify/CURRENT.md`'s heading changes.

## Ids and records

No id is minted. No LLR names `acceptance_stamp` or states the heading. LLR-259 names `reaccept_lines` for the released-chain split alone, and IF-126's stamp read is `registry_stamps`, which this row leaves alone. So no spine row changes and no act is owed. The two extra states, and the malformed outcome, are design calls no spine row states, so they go in `docs/decisions/maint-wi-1040.toml` as one entry. A RESYNC entry is added if the commit checks ask for one for the two shipped scripts.
