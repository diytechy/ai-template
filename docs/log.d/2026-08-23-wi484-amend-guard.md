## 2026-08-23 — WI-484 phase 5: the amend-without-flip guard's Hat-Refs arm

Executed OI-32's phase 5 — OI-33's surviving residue — and nothing else. Spec
items 2 (phase 2's writer), 3 (phase 2's duplication) and 5 (phase 4's blocker)
are untouched and stay owed; item 6 is struck by this slice.

**The rule.** A row whose APPROVED cells moved while its `Hat-Refs` cell did not
is a finding: the substance moved and the perspective record did not, so the
DERIVED component and knowledge views keep answering from the old lenses. That
is the one thing generation cannot do — freshness compares an artifact to its
regeneration and never asks whether the source was right.

**Built as an ARM, not a rule.** `staged_hat_refs_findings(root)` reads the one
amendment set `staged_spine_amendments` already computes, and fires on
`approved` non-empty + `Hat-Refs` absent from `traced`. Ten lines of predicate.
Building it beside `staged_spine_findings` rather than as its own scan is what
keeps the two from ever disagreeing about what an amendment IS — the ruling's own
words were "same shape, same home, warn-first".

**Cell class, never line or file — the whole design.** The defect it is designed
against is measured and lives one module over: `backlog_staleness_findings`
blames the SR registry by LINE, so the phase-2 backfill's 55 informative cells
re-dated their rows and raised seven warns. A `git blame` line time cannot tell
an approved cell from a traced one; `split_changed_cells` can, which is why
`Hat-Refs` was CLASSIFIED `traced` at both tiers rather than left to the
residual. The regression case is driven directly: writing the `Hat-Refs` cell
itself raises nothing.

**The baseline, and what it does not cover.** HEAD versus the index, over rows
reading the same approved-text `Status` on both sides — the amendment guard's own
population, inherited rather than re-litigated. Two vacuities follow and both are
HONEST rather than coverage: a row minted in the same commit has no baseline to
compare, and a row below approval has blessed nothing to amend behind a human's
back. A tier with no `Hat-Refs` column (test cases today) is silent
STRUCTURALLY, through `traced_cells`, not by an allowlist.

**`docs/archive/last_approved` was considered and declined, and the trade is
recorded rather than buried.** That baseline would make the finding STAND until
answered, where this one is a single warn at the commit that earns it. Declined
on OI-33's own timing argument — the party who knows whether the perspectives
moved is the one making the change, at the moment they make it — and on the
ruled home. The standing half of the same question is already carried for
approved cells by snapshot drift. If the warn is measured to be ignored,
promoting it to a drift-tier finding is the next rung, on evidence.

**An empty `Hat-Refs` cell still fires.** A cell never filled and a cell
deliberately left empty (`SR-015`, `SR-040`, both argued) read identically, and
the question is whether the set was RE-EXAMINED — which an unchanged empty cell
cannot answer.

**Initial live finding count.** Zero at HEAD, because nothing is staged; the
figure that means something is the historical rate, driven over real commits:

fig: cmd="python -c \"import sys;sys.path.insert(0,'project-trajectory/scripts');import check_trajectory as ct,subprocess;revs=subprocess.run(['git','rev-list','--reverse','-n','100','HEAD'],capture_output=True,text=True).stdout.split();print([(len(revs))]+[sum(1 for r in revs for x in ct.staged_spine_amendments('.',r+'~1',r) if x['approved'] and (('Hat-Refs' in ct.traced_cells(x['registry'])) == k) and ('Hat-Refs' not in x['traced']))for k in (True,False)])\"" rev=ec0611ed-dirty — over the last **100 commits**: **70** approved-cell amendments, of which the arm would fire on **46**; the other **24** are test-case rows, a tier that carries no such column; **0** were discharged by a `Hat-Refs` that moved with the amendment (expected — the cell only exists since 2026-08-22). Over the 13 commits since the last approval snapshot (`27a30842..HEAD`), 1 amendment and 1 firing: `LLR-147` `Detail`.

**The staleness-granularity disposition: RECORDED, NOT FIXED — and the reason is
a finding, not a shrug.** Confirmed live rather than inherited: of the three
staleness warns at HEAD, exactly one is the backfill's — `WI-508: cites SR-163
amended after…`, whose newest blamed line is `hat_refs = ["MAINTAINER"]`
(2026-08-22), the row's substance untouched since 2026-08-14. Two fixes were
examined and neither is small:

- **Blame only approved-class lines** needs a quote-state parser for multi-line
  TOML values, and — the deciding objection — it would also silence a re-pointed
  `SN-Refs`/`Boundary-Refs`. Those are traced but scope-BEARING (that is exactly
  why they route to adjudication), and a scope re-point is the change a citing WI
  most needs to re-validate against. So "normative lines only" is the WRONG
  filter, not merely an expensive one.
- **Recompute the clock through `split_changed_cells` over a rev range** is exact
  and invents nothing, but replaces the check's bounded cost (≤2 blames) with git
  work per open WI and inherits the amendment scan's approved-only population.

Which traced cells are staleness-bearing is a new classification — a ruling, not
a patch. Taken instead, on the WI-362 precedent (owner ruling 2026-07-29: name
the blind spot, do not build the detection): the limitation is now STATED in
`backlog_staleness_findings`' docstring with its measured instance, so the next
reader does not re-derive it. Left on the lane spec's item 5 as the follow-up.

**Mutation-driven, three ways** (each reverted after; each reds exactly one
test): dropping the tier scoping reds
`…silent_on_a_tier_that_carries_no_such_column`; dropping the `Hat-Refs not in
traced` clause reds `…silent_when_the_cell_moves_with_the_amendment`; widening
the trigger to `approved or traced` reds `…silent_when_only_traced_cells_move`.

**Spine.** `LLR-202` + `TC-198`, both `Drafted` on the standing precedent, parent
`SR-161` (the perspective-record requirement — `LLR-183` makes the record
resolvable, this row asks whether a resolvable record is still true). `LLR-158`
was NOT amended: its cells are Approved and its `code_symbol` already names the
comparison basis this arm reuses.

**Deviations from the brief.** One, and it is a consolidation rather than a
change of subject: `spine_cell_class`'s body was extracted to a public
`traced_cells(csv_path)` because the arm needs the SET, not one column's class —
an absent column classes `approved` under the fail-safe residual, so without it
every amended test case would warn about a cell its registry does not have.
`spine_cell_class` is a one-line caller of it and its behaviour is unchanged.
The test fixture gained a `Hat-Refs` column on the SR and LLR headers rather
than a second fixture family, so both arms of the guard are driven over the same
rows they scan in the code.

## Gates

`python project-trajectory/scripts/check_docs.py --root . --stale` — OK, 1039
doc(s), 1356 intra-repo link(s), 0 broken (1 orphan warning, pre-existing).

`python project-trajectory/scripts/check_trajectory.py --root . --strict` — exit
0; the new findings are warn-only by design and this tree stages nothing, so the
arm prints nothing here. Every WARN it does print is pre-existing and unrelated
(arch-map connectivity, CodeSymbol tag drift, over-long open-WI titles, the two
backlog-staleness warns discussed above).

`python project-trajectory/scripts/check.py --run-steps
component-view,trajectory-map,status-map,open-items,derived-stage` — all five
PASS after regeneration (the two new Drafted rows moved `drafted` 19 -> 21 in
`docs/stage`; the derived stage itself is unchanged at `DevStg-LLReqs`).

**Ratchet re-stamped, reason recorded:** `check_trajectory.py` 4765 -> 4880
(+115) in `tests/test_module_size_ratchet.py`, the entry naming what the bump
buys and why the arm is not decomposable out of the guard it belongs to.

fig: cmd="python -m pytest -q -n auto -m smoke" rev=ec0611ed-dirty — 1301 passed, 5 skipped in 18.84s; `python scripts/check_smoke_budget.py --mode enforce` re-timed it at **19.3s vs the 60s budget -> within**.

fig: cmd="python -m pytest -q -n auto --basetemp=D:\pytest-tmp-w484c2" rev=ec0611ed-dirty — **2960 passed, 14 skipped in 1043.81s (0:17:23)**, run because this is a script change. It is the SECOND full run: the first (`--basetemp=D:\pytest-tmp-w484c`, 2 failed / 2958 passed / 14 skipped in 1172.50s) was started before three edits landed and reds only on them — `test_module_size_ratchet` (baseline 4877 vs the 4880 the `Implements: SR-161, LLR-202` tag made it) and `test_derive_stage::test_this_repo_s_committed_stage_is_current` (`docs/stage` had not yet been regenerated for the two new Drafted rows). Both are stamped/regenerated here, and the re-run above is on the FINAL tree with nothing edited after it but this figure.

Deferred open items: none — the one question this slice could have raised (which
traced cells are staleness-bearing) is recorded on WI-484's own spec as item 5's
follow-up rather than handed to the owner, because it is a checker-design call
inside a lane that is still open.
