## 2026-08-01 — WI-383: two axes, not one class ladder (and session grouping is removed)

**Summary.** `schedule.py` ran five scheduling classes on ONE ladder —
`spine-serial | protected-serial | single-wi | ordinary | unclassified` — and
used that one ladder for two different jobs: `_GATE_RANK` made the class decide
**who goes first**, `classify()` made the same class decide **what may share the
station**. Split into two independent axes per
[`concurrency-v2.md`](../concurrency-v2.md) §A1, and deleted the packing
plumbing §A6.1 rules out of existence. Net: three constants, one exit code, one
guard and one import gone; nothing added but two lookup tables that replace one.

**Deliverables.**

- **Two tables, one key set.** `_KIND_CONCURRENCY` (`exclusive` = runs alone |
  `parallel`) and `_KIND_RANK` (integer, low first) are keyed by the same
  declared kind and read independently; `classify()` returns
  `(concurrency, rank, reasons)`. §A1's ruled numbers verbatim: `spine` 0,
  `attestation`/`gate` 2, `protected` 3, `high-risk`/`PlanMode=dual` 4 exclusive;
  **`critique` 5 and PARALLEL**, `ordinary` 6.
- **Rank 1 is a written gap**, not an omission — it belongs to the
  `adjudication` kind WI-388 adds. Writing the ladder whole means that row adds
  one mapping instead of renumbering a ruled table, and a test asserts 1 stays
  unoccupied so nobody quietly reuses it.
- **Deleted.** `SCHED_SPINE_SERIAL`, `SCHED_PROTECTED`, `SCHED_SINGLE_WI`
  (collapsed into the one `exclusive` value they always meant — that is the
  whole diagnosis: `protected-serial` and `single-wi` were never different
  things), `_GATE_RANK`, and `is_schedulable_class` → `is_schedulable`.
- **`order_key` takes the RANK, not the classification.** The independence is
  structural on that side rather than merely asserted: no concurrency value can
  reach the sort at all.
- **A quarantine refuses BOTH axes** — `(CONCURRENCY_UNCLASSIFIED,
  RANK_UNCLASSIFIED)` from one `_unclassified()` helper, so no path can fail
  closed on one axis and open on the other.
- **Session grouping removed, not wired** (§A6.1): the §7 continuation re-check,
  the `exit 10 ASSIGNMENT-END` arm, `EXIT_TRAIN_END` itself, the worker's
  `sched` scheduler view, and `agent_loop`'s `schedule` import. The guard's only
  non-refusing case was the homogeneous spine batch, so with packing gone it
  could only ever say yes — and a check that can only say yes is not a
  safeguard. `agent_loop --wi 'WI-201;WI-204'` **survives** with its one
  remaining caller, the dispatcher admitting the spine batch (WI-381).
- **Both ratchets re-stamped DOWNWARD** in the commit that earned it:
  `agent_loop.py` 3026 → 2973 lines, `run_iteration` complexity 23 → 20.

**How the two axes are pinned independently.** A test that reads only one axis
would pass under a re-conflation, so the fixtures attack both directions:

- **Rank does not determine concurrency** — ranks 4 (`high-risk`) and 5
  (`critique`) are ADJACENT and land on opposite concurrency values. Being
  ranked early does not make a WI exclusive.
- **Concurrency does not determine rank** — the five exclusive kinds hold four
  distinct ranks. "Exclusive" says nothing about order.
- **A rank change does not move concurrency** — a `Priority` bump swaps the
  frontier order of two ordinary WIs while every concurrency answer stays
  `parallel`; plus the structural half above (`order_key`'s signature).
- The declared-kind table itself is restated as data the tests read, so §A1's
  ruling and the code disagree loudly rather than silently.

`tests/test_schedule.py` constructs every registry it reads (39 tests, all
in-process).

**Deviation from the spec: the `checkpoint` classifier input was deleted too.**
Not named in the ruled table, and it did not survive the reasoning that keeps
`critique`. Checked before removing: `load_wis` never emitted a `checkpoint`
key, so the arm was reachable only from hand-built dicts in tests — it had no
producer anywhere in the kit. Its entire meaning was *do not pack me*, which is
exactly what `single-wi` meant for a critique; §A6.1 deletes what that was drawn
against. `critique` is kept because §A1's table names it (parallel, rank 5),
and it is honestly documented as a flag the current registry never sets.

**Two things deliberately NOT done here.**

1. **No `adjudication` kind.** The ruled rank table names it, but the kind
   itself — minting, the no-bar rule, the backlog re-scope — is WI-388's scope
   per the §"Revised breakdown". Adding an unowned vocabulary value would be
   this row building another row's surface; the reserved rank is the whole of
   what this row owes it.
2. **No spine amendment.** `SR-093` and `SR-124` describe the five-class ladder
   this row collapses, and `SR-124` names `single-WI` specifically — a class
   that no longer exists. `LLR-059`, `LLR-089`, `LLR-095`, `LLR-131` (`classify`
   / `structural_safety`) and `LLR-058`/`LLR-123` (*"traincar ordering"*,
   *"gate class"*) name the collapsed vocabulary too. That is §A9.1's program
   close (**WI-390**), which is hard-blocked on this row for exactly this
   reason. `TC-091`'s **Evidence** cell was repointed at the renamed test —
   a TRACED cell under §A5.1/WI-380, so it arms no re-attest window and is not
   an amendment.

**Finding (inherited drift, recorded not absorbed — §A9.1 item 2).** `TC-091`'s
Evidence also names `tests/test_agent_loop_dispatch.py::test_unclassified_wi_fails_closed_without_stopping_others`,
a module deleted with the dispatcher at concurrency-restructure Phase 5. Nothing
validates that test node ids resolve, so an Evidence cell can name a file that
has not existed for days and every gate stays green. Worth its own WI — either
a resolver for `Evidence` node ids, or an honest ruling that the cell is prose.

**Bars (real output, this branch).**

```
$ python -m pytest -q -n auto
1 failed, 1755 passed, 8 skipped in 403.80s (0:06:43)
      # the one standing red is tests/test_check_lane.py::test_this_repo_is_not_a_work_branch
      # (this checkout IS a claimed work branch — the guard is asserting about the trunk)
$ python -m pytest -q -n auto -m smoke
1 failed, 567 passed, 4 skipped in 14.59s      # same standing red
$ python -m ruff check .            -> All checks passed!
$ python -m ruff format --check .   -> 146 files already formatted
$ python project-trajectory/scripts/check_trajectory.py --root . --strict
check_trajectory: clean (389 work item(s), 366 done (94%), 16 cancelled, graph acyclic).   [exit 0]
$ python project-trajectory/scripts/check_doc_refs.py --root . --strict
check_doc_refs: OK - no dangling path or sym: references · 870 untraced   [exit 0]
```

No byte-budgeted file was touched. Generated artifacts (`docs/architecture.md`'s
module map loses the `agent_loop → schedule` edge) are deliberately NOT
regenerated here — §5.2, the trunk lane owns them.
