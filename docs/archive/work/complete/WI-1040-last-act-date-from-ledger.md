+++
id = "WI-1040"
title = "The re-acceptance brief dates the last acceptance from the act ledger, not from the newest status-line diff"
workstream = "process"
sr_refs = []
needs = []
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 3
planmode = "single"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1040`, cut from `refactor_again` at
`dd8f79e6c`, with the commit hooks on. `planmode = "single"`: the plan,
`docs/plans/WI-1040/plan.md`, was committed alone before the build. The
specref is cleared at close, as a terminal row's is.

- `7379d4a60`: the plan. It names each ledger state the heading handles and
  its outcome, the reading reused, and the limit at the record's move.
- `ea59f2a83`: the build. The code, the tests, the golden brief, the size
  re-stamp, the RESYNC entry, the decisions record and the regenerated views.
- `56b1fc405`: the close-out. This Deliverable, the audit note's site 1
  marked resolved, the log fragment, and the move to `complete/`.
- `8539c3124`: the merge of trunk at `7048e6a6f` (WI-1041, WI-1043,
  WI-1044). `risk_acceptance_act` walks `_ledger_commits` and ends as
  WI-1041 left it, unanchored with no fallback. The tests run with
  `--basetemp D:/rt1040/t` (test_baseline_snapshot, test_accepted_risk,
  test_trace_briefs, test_intake_held_act, test_module_size_ratchet,
  test_import_layers, test_complexity_ratchet): `252 passed in 417.22s
  (0:06:57)`. `run_menu.py smoke` at the merge: `3714 passed, 3 skipped,
  18 warnings in 153.75s (0:02:33)`, CPU budget WARN only.
  <!-- fig: cmd="python -m pytest -q -n auto --basetemp D:/rt1040/t <the 7 modules listed>; python project-trajectory/scripts/run_menu.py smoke" rev="8539c3124 (the pytest run on its tree before the commit, smoke at the commit)" -->
- The records commit after it: these merge lines and the leftover note.

**What landed.** `baseline_snapshot.last_act(root)` returns
`(entry, commit, reason)`. `entry` is the working tree's newest act-ledger
entry, `commit` is the commit that added it, and `reason` is the clause the
brief prints after `_Acceptance provenance: `. `trace.reaccept_lines` prints
it; the line keeps its prefix, so `acceptance_check` still leaves it out of
the comparison. `acceptance_stamp`, the status-line pickaxe, is removed. On
this repository the heading moves from `458724024` (WI-1021's build, which
accepted nothing) to "the last acceptance act is the act ledger's seq 185,
dated 2026-11-20, added by commit 46d518b56c05".

Each ledger state reads one way, and none names a commit that is not the
act's:

- **No ledger, or one with no entry:** "no acceptance act is recorded",
  naming which.
- **The newest entry, its commit read:** its seq, its recorded date and the
  commit.
- **The newest entry, its commit beyond a shallow clone's window:** its seq
  and date; "its commit is not in the available history: this is a shallow
  clone, and the act may lie beyond its window".
- **Two more states supported workflows reach** (D-001 in
  `docs/decisions/maint-wi-1040.toml`): an entry no commit adds yet, as
  when an act's own commit regenerates the views before it lands; and a
  history git cannot read. Each gives the seq and date and says why no
  commit is named.
- **A malformed ledger, outside the promise:** "no acceptance act can be
  read", and the brief never raises.

**The reading reused.** The accepted-risk anchor's walk moves into one
helper, `_ledger_commits`: the ledger's commits, newest first, with a shallow
clone's boundary commits dropped. `risk_acceptance_act` and `last_act` both
call it, and `_acts_at` says which entries each commit added.
`risk_acceptance_act`'s behaviour is unchanged. The new reader stops at the
first commit that added only older entries, since the ledger only grows
(IF-220), so an uncommitted act costs one step instead of a walk over every
ledger commit.

**Finding for the coordinator: the walk does not see across the record's
move.** It follows the ledger at its current path only. `2bee2b551`, the
2026-11-16 move of the record directory, reads as adding all 182 entries it
held (measured at `dd8f79e6c`). The newest entry, seq 185, postdates the
move, so the heading is right here. In a repository whose newest act is
older than its own move of the record, such as one `migrate_vocabulary.py`
moved with no act taken since, the heading would name the move commit.
`risk_acceptance_act` has the same limit for an assumption whose only acts
predate the move. **Left over, by the coordinator's ruling:** not fixed
here. WI-1042 already has to read across the 2026-11-16 move, and the
coordinator will point its spec at `_ledger_commits`, so one change fixes
all three readers.

**Ids and rows.** None minted, and no spine row changed: no LLR names
`acceptance_stamp` or states the heading. `trace.py --root . --bump-ids` was
not needed.

**Tests.** Seven new tests in `tests/test_baseline_snapshot.py`: the draft
after the last act, read through `trace.reaccept_lines`; the newest entry
and its commit; an act not yet committed, then landed; a depth-1 clone; no
ledger and an empty one (two shapes); a ledger off git; and a malformed
ledger. They replace the `acceptance_stamp` test. The CSV-carrier
provenance test in `tests/test_trace_briefs.py` now expects the seed's act
and commit. The golden brief (no git, no record) was regenerated with
`UPDATE_BRIEF_GOLDEN=1`; only its provenance line changed.

- Red first, the new tests against the plan commit's code:
  `7 failed, 148 deselected in 15.45s`. The draft test failed on the heading
  naming the draft's commit (`caa2cb6`, not the act's `fbc9290`); the other
  six on the missing `last_act`.
  <!-- fig: cmd="python -m pytest -q tests/test_baseline_snapshot.py -k '<the 7 new tests>'" rev="7379d4a60 (the new tests over that commit's code)" -->
- The same tests, green: `7 passed, 148 deselected in 25.06s`.
  <!-- fig: cmd="python -m pytest -q tests/test_baseline_snapshot.py -k '<the 7 new tests>'" rev="ea59f2a83 (its tree before the commit)" -->
- Every test module that imports, loads or runs `trace` or
  `baseline_snapshot` (a grep of `tests/`, plus both `trace.py --tests-for`
  lists), the RESYNC pack's readers, `test_import_layers`,
  `test_module_size_ratchet`, `test_dogfood_sync` and
  `test_complexity_ratchet`, 95 modules:
  `80 failed, 3067 passed, 2 skipped, 18 warnings in 1832.37s (0:30:32)`.
  All 80 came from the run's `--basetemp`, a long path under the session
  scratch directory, which pushed record copies at
  `docs/archive/last_accepted/docs/requirements/...` past what Windows
  could read. Those failures say the copy "cannot be read", and the six
  accepted-risk ones read an accepted risk as unproven. The nine modules
  holding all 80 pass whole on a short basetemp:
  <!-- fig: cmd="python -m pytest -q -n auto --basetemp <scratch path> <the 95 modules>" rev="ea59f2a83 (its tree before the commit)" -->
- `test_held_status_git`, `test_intake_held_act`, `test_intake_settled`,
  `test_accepted_risk`, `test_text_then_act`, `test_integrate_admission`,
  `test_snapshot_readers`, `test_done_when_blessing` and
  `test_agent_loop_worker`, with `--basetemp D:/rt1040/b`:
  `414 passed in 2354.43s (0:39:14)`.
  <!-- fig: cmd="python -m pytest -q -n auto --basetemp D:/rt1040/b <the 9 modules listed>" rev="ea59f2a83 (its tree before the commit)" -->
- `run_menu.py smoke`, before the build commit:
  `3714 passed, 3 skipped, 18 warnings in 237.51s (0:03:57)`, with the CPU
  budget WARN only (699.8 s against 540). Its `trace.py --strict`:
  `orphans=0 integrity=0`. `check_trajectory.py --strict` is clean and
  `check_resync.py` is OK.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="ea59f2a83 (its tree before the commit)" -->
- Review round 1 (Sol's MINOR, adopted): a working-tree ledger that is not
  UTF-8 raised `UnicodeDecodeError` out of `last_act`; it now reads as
  malformed. The new test `test_an_undecodable_ledger_reads_malformed_rather_than_raising`
  failed on `d6ccdb587` with that error (`1 failed, 155 deselected in
  1.07s`). After the fix, `test_baseline_snapshot` and `test_trace_briefs`
  with `--basetemp D:/rt1040/r2`: `197 passed in 129.61s (0:02:09)`.
  <!-- fig: cmd="python -m pytest -q -n auto --basetemp D:/rt1040/r2 tests/test_baseline_snapshot.py tests/test_trace_briefs.py" rev="the round-1 answer commit (its tree before the commit)" -->
- The unfiltered suite was not run.

**Sizes.** `trace.py` re-stamped down, 3844 -> 3835 SLOC.
`baseline_snapshot.py` went from 965 to 987 SLOC, under the 1000 threshold,
so it needs no entry. The complexity ratchet is unchanged.

**Byte deltas.** `RESYNC_PACK.md` 737,613 -> 738,955 (unbudgeted). After
the merge it is 739,612 on trunk -> 740,954 here: the same +1,342. The new
entry is "The re-acceptance brief names the last acceptance act from the act
ledger", anchored `[since dd8f79e6c]` at the build and re-anchored
`[since 7048e6a6f]` at the merge, since `check_resync.py` requires the
change's base. Nothing is forced, and the kit-owned files are
`scripts/baseline_snapshot.py` and `scripts/trace.py`. No budgeted file was
touched.

**Acts owed:** none. No spine row changed and no status moved.

**Review** (the coordinator, 2026-11-21; queue-drill HANDOFF §4 step 4).
Round 1 over `7048e6a6f..d6ccdb587` (the branch's net change over trunk,
the WI-1041 merge included), the generated views, the plan and this spec's
copies withheld and the spec at the tip given whole: OpenAI Sol
(`gpt-6.1-sol`, low, via `codex exec`) read the whole diff, and Gemini
Hydrogen (`gemini-4-hydrogen-low`, via the Antigravity CLI) the prose part
by file reference. Both were asked to confirm `risk_acceptance_act` keeps
trunk's behaviour on the shared walk, WI-1041's end included, and to judge
D-001's three states. Hydrogen: `VERDICT: APPROVE findings=0`. Sol:
`VERDICT: CHANGES-REQUESTED findings=1`, a MINOR confirmed by execution
and adopted: invalid UTF-8 in the ledger raised `UnicodeDecodeError`
through `last_act`, against D-001's "never raises". Fixed in
`5dc1c9174`, inside `last_act` only (red first). Round 2, narrow, over
`d6ccdb587..5dc1c9174` with round 1's finding and the ruling prepended:
Sol, `VERDICT: APPROVE findings=0`.

## Context

Filed on trunk on 2026-11-21 from WI-1036's history-reader audit, class (c)
site 1 (`docs/reviews/2026-11-history-readers/README.md`).

The re-acceptance brief's heading names when the last acceptance act
happened. Today the date is recomputed from history: the newest commit
whose diff adds or removes a `status =` line in a snapshotted registry. The
function's own docstring grants that this also matches a row addition or a
new draft, so the heading can name a commit that accepted nothing. The rule
it breaks: a decision is recorded at its event and read from that record,
never recomputed (PROCESS.md §3; the review-churn plan's item 2).

The record already exists. An act made through `intake.py snapshot` appends
an entry to the act ledger (`docs/archive/last_accepted/acts.toml`) with its
date, and the commit that added the entry is the act's own commit, read the
way the accepted-risk reader already reads it (class (b) in the audit). No
LLR names the function, so no accepted row changes.

## Done-when

- [x] The brief's heading reads the newest ledger entry and the commit that
      added it. With no ledger, or an empty one, it says no act is recorded
      instead of guessing. When the newest entry is present but the commit
      that added it is not in the readable history (a shallow clone, the
      limit IF-217 already states), the heading gives the entry's recorded
      date and says its commit is not in the available history; it never
      falls back to another commit. The promise covers supported workflows
      and the ledger as the kit writes it; a hand-edited ledger is outside
      it.
- [x] A test covers each of those states, and one shows that a row addition
      or a new draft after the last act no longer moves the heading's date,
      failing on today's code.
- [x] The audit note's site 1 is marked resolved by this row.
