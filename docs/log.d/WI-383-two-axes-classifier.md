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
- **`order_key` takes the RANK, not the classification**, so the concurrency
  axis is not in the ordering decision. Round 1 of REVIEW-A showed that is a
  **convention, not a guarantee** — see the retraction below.
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
would pass under a re-conflation, so the fixtures attack both directions — and
after round 1, each pin is mutation-proved rather than merely written:

- **Rank does not determine concurrency** — ranks 4 (`high-risk`) and 5
  (`critique`) are ADJACENT and land on opposite concurrency values. Being
  ranked early does not make a WI exclusive.
- **Concurrency does not determine rank** — the five exclusive kinds hold four
  distinct ranks. Now read off the SHIPPED `_KIND_CONCURRENCY`/`_KIND_RANK`
  rather than off this test file's own copy of §A1; the old form asserted the
  copy was self-consistent and passed unchanged under a `_KIND_RANK` mutation
  that made the property maximally false.
- **A rank change does not move concurrency** — a `Priority` bump swaps the
  frontier order of two ordinary WIs while every concurrency answer stays
  `parallel`.
- **The ordering axis is pinned at its CALL SITE** —
  `test_the_frontier_orders_one_concurrency_group_by_rank` builds a frontier
  whose leading run is four kinds that share one concurrency value and hold
  ranks 0/2/3/4. Anything that orders on the concurrency string ties all four,
  collapses them to id order, and drops the spine WI from first to fourth.
  Nothing hands `order_key` a literal.
- The declared-kind table itself is restated as data the tests read, so §A1's
  ruling and the code disagree loudly rather than silently.

`tests/test_schedule.py` constructs every registry it reads (40 tests, all
in-process).

**RETRACTION (REVIEW-A round 1, MAJOR).** Round 1 of this fragment, the
Deliverable and `order_key`'s docstring all said the same thing in the same
words: *"`order_key` is handed a rank, not a classification, so no concurrency
value can reach the sort at all — the independence is structural on that side
rather than merely tested."* **That was false.** The parameter is an untyped
positional, nothing in the function inspects it, and the single call site in
`evaluate` is the only thing making the sentence true. The reviewer drove the
one-token mutation `order_key(w, rank, …)` → `order_key(w, concurrency, …)`
and the full unfiltered suite returned **byte-identical counts** —
`1 failed, 1755 passed, 8 skipped` — while the frontier genuinely reordered
(`['WI-004','WI-001','WI-002','WI-003','WI-009']` shipped versus
`['WI-001','WI-002','WI-003','WI-004','WI-009']` mutant: every exclusive kind
ties on the string `"exclusive"`, so rank ordering inside the group is
destroyed and the spine WI falls to fourth). It survived because the named test
passed literal ints — it could not see what `evaluate` hands the function — and
because the only cross-boundary ordering test was preserved by the alphabetical
accident `"exclusive" < "parallel"`.

The claim is **retracted in all three places** and replaced by what is now
actually true: a convention held by one call site, with a test that convicts
the edit. Re-driven here — the reviewer's exact mutation applied to a clean
tree now gives `1 failed, 39 passed`, and the single red is the new pin
(`At index 0 diff: 'WI-001' != 'WI-004'`); tree restored and re-verified clean
with `git diff --exit-code`. The `_KIND_RANK` mutation behind the second
finding likewise takes its pin from `1 passed in 0.19s` to a red.

**This is the shape the repo keeps producing** and worth naming: a guarantee
asserted in prose, resting on a convention no mechanism holds, and a test named
after the property that cannot observe the place it breaks. The lesson is not
"write more tests" — it is that a test which constructs its inputs by hand
cannot pin a property of a CALL SITE.

**Considered and declined:** the reviewer's other offered remedy, an
`isinstance(rank, int)` guard in `order_key`. A defensive type check in a pure
library function is the check-instead-of-constraint shape §0 warns against, and
it would not catch a caller passing the wrong *integer* — it converts one
un-pinned property into a narrower un-pinned property. The coordinator endorsed
the divergence; it is recorded here so a successor does not re-propose it as an
oversight.

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
2. **No spine amendment — and here is the whole of what WI-390 inherits.** All
   of these are RATIFIED cells, so amending them is not this row's to do; but
   WI-390 only gets the scope this list writes down, so it is stated in full.
   Round 1 caught the first draft omitting the two `checkpoint` rows — including
   one in a row this branch edited.
   - `SR-093` and `SR-124` describe the five-class ladder this row collapses,
     and `SR-124` names `single-WI` specifically — a class that no longer
     exists.
   - **`SR-094`'s AcceptanceCriteria** — *"Spine, critique, **checkpoint**, and
     dual-plan structure override dishonest declarations"* — names an input this
     row DELETED. Not incidental: SR-094 is the parent SR of the rewritten
     function, cited in `schedule.py`'s own section header and module docstring.
   - **`TC-091`'s Description/Method** — *"Classify missing, unknown,
     structurally contradictory, critique, **checkpoint**, and dual-plan WIs"* —
     the same false clause, in the very row commit `b8c7cc21` edited to repoint
     its `Evidence`. The repoint itself is fine (`Evidence` is TRACED under
     §A5.1/WI-380, so it arms no re-attest window and is not an amendment); the
     Description beside it was left false and is recorded here rather than
     quietly fixed.
   - `LLR-059`, `LLR-089`, `LLR-095`, `LLR-131` (`classify` /
     `structural_safety`) and `LLR-058`/`LLR-123` (*"traincar ordering"*,
     *"gate class"*) name the collapsed vocabulary too.

   That is §A9.1's program close (**WI-390**), hard-blocked on this row for
   exactly this reason.

**Finding (inherited drift, recorded not absorbed — §A9.1 item 2).** `TC-091`'s
Evidence also names `tests/test_agent_loop_dispatch.py::test_unclassified_wi_fails_closed_without_stopping_others`,
a module deleted with the dispatcher at concurrency-restructure Phase 5. Nothing
validates that test node ids resolve, so an Evidence cell can name a file that
has not existed for days and every gate stays green. Worth its own WI — either
a resolver for `Evidence` node ids, or an honest ruling that the cell is prose.
**Confirmed by the reviewer far harder than I stated it:** they replaced the
entry with an entirely invented `tests/this_file_has_never_existed.py::test_entirely_invented`
— a path with no file and no history — and drove
`trace.py --strict --no-placeholders --require-verified --strict-schema`
(rc=0, TC-091 still `Verified`), `check_trajectory --strict` (rc=0),
`check_doc_refs --strict` (rc=0) and the trace/registry test modules (70
passed). Nothing anywhere convicts it. The file half is checkable with
`Path.exists()` today; only the `::node` suffix needs pytest to adjudicate.

**Filed as `WI-394`** (`docs/work/queued/`, spec-of-record
[`docs/specs/WI-394.md`](../specs/WI-394.md)) — with the option NOT picked for
the owner, because the one thing definitely wrong today is that the current
state implies a check nobody performs. Before filing I measured whether the
class is wider than `Evidence`, rather than guessing:

| Cell mutated to something invented | `trace.py --strict …` | `check_trajectory --strict` |
|---|---|---|
| LLR `Module` + `CodeSymbol` (LLR-059) | rc=0 | rc=0 |
| LLR `TestRefs` → `(see TC-999)` | rc=0 | rc=0 |
| TC `Evidence` (the reviewer's run) | rc=0 | rc=0 |
| **CONTROL:** TC `Verifies` → `SR-999;LLR-999` | **rc=1** — `FINDING (orphan): TC TC-091 references unknown SR-999` | — |

113 tests across `test_trace.py`, `test_registry_checks.py`,
`test_check_flows.py`, `test_check_stubs.py`, `test_modules_registry.py` and
`test_components_registry.py` also pass under the `Module`/`CodeSymbol`
mutation. Every tree restored and re-verified with `git diff --exit-code`.

So the boundary is crisp and it is **not** "traced cells are unchecked": a
pointer into ANOTHER REGISTRY is joined and validated (`Verifies`, `SR-Refs`,
`Component`); a pointer OUT of the registries into the code or test tree —
`Evidence`, `Module`, `CodeSymbol`, `TestRefs` — is not checked at all. Those
four are exactly the cells carrying the spine's claim to be grounded in the
code.

One datum found by writing the spec itself: `check_doc_refs --strict` flagged
the invented `.py` path quoted in its evidence table, but passed the
`…::test_entirely_invented` citation silently — its PATH tier needs the token
to END in a known extension, and a `::node` suffix defeats that. The kit
already owns a path-existence checker; it is blind to the registry citation
shape for one tokenising reason (and never reads the CSVs anyway).

The row is `ordinary`, not spine, and the spec says why: `Evidence`, `Module`,
`CodeSymbol` and `TestRefs` are all TRACED under §A5.1, so it arms no re-attest
window. Ids 392/393 were skipped — both are minted on sibling branches in this
wave and invisible from here, which is the id-reservation hazard §B3 describes.

**Naming fix (REVIEW-A round 1, MINOR).** `CONCURRENCY_EXCLUSIVE = "exclusive"`
landed beside the pre-existing `Exclusive` mutex-key column — two unrelated
ideas, both spelled *exclusive*, both about not-running-together — inside the
one module whose stated diagnosis is that an overloaded word caused the defect.
It reached the wire: `evaluate` emitted
`{"concurrency": "parallel", …, "exclusive": ["registry-lock"]}`, which reads as
a self-contradiction to anyone who has not read the source. The emitted record
key is now **`exclusive_keys`** (no live consumer outside `schedule.py`, so a
one-line change), the distinction is stated at the axis header, at
`_exclusive_conflicts` and in the module docstring, and the wire shape is
asserted. `simulate`'s docstring — the one sentence that used both senses — now
says plainly that it DOES apply the mutex keys through `frontier` and does NOT
apply the concurrency axis. The internal `w["exclusive"]` is left alone: it
mirrors the `Exclusive` column name across the three F5-duplicated readers, and
renaming it there would be drift, not clarity.

**Bars (real output, this branch, after the round-1 fixes).**

```
$ python -m pytest -q -n auto
1 failed, 1756 passed, 8 skipped in 400.41s (0:06:40)
      # the one standing red is tests/test_check_lane.py::test_this_repo_is_not_a_work_branch
      # (this checkout IS a claimed work branch — the guard is asserting about the trunk)
$ python -m pytest -q -n auto -m smoke
1 failed, 572 passed in 13.21s                 # same standing red
$ python -m ruff check .            -> All checks passed!
$ python -m ruff format --check .   -> 146 files already formatted
$ python project-trajectory/scripts/check_trajectory.py --root . --strict
check_trajectory: clean (389 work item(s), 366 done (94%), 16 cancelled, graph acyclic).   [exit 0]
$ python project-trajectory/scripts/check_doc_refs.py --root . --strict
check_doc_refs: OK - no dangling path or sym: references · 871 untraced   [exit 0]
```

(Round 1 measured `1 failed, 1755 passed, 8 skipped` / `1 failed, 567 passed,
4 skipped` on the same tree before these fixes; the +1 in each is the new
call-site pin.)

No byte-budgeted file was touched. Generated artifacts (`docs/architecture.md`'s
module map loses the `agent_loop → schedule` edge) are deliberately NOT
regenerated here — §5.2, the trunk lane owns them.
