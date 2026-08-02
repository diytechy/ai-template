## 2026-08-02 — WI-410: the absolute-import arms, pinned

**Summary.** WI-406 REVIEW-A finding 1 (minted trunk-side at intake), closed
as specced — fixtures only. The reviewer's probe showed
`_has_internal_import`'s ABSOLUTE arms unpinned: reducing the ImportFrom test
to `if node.level:` and deleting the whole ast.Import branch left all 60
trajectory-arch tests green, so an absolute-import-ONLY module could drift
mirror-side without a red — the wi-387 station-first topology back, for that
shape.

**Deliverables.**

- **One differential fixture** (`tests/test_trajectory_arch.py`, WI-410
  section, work commit 34894b48) through the full lifecycle: lane red on the
  untagged modules BEFORE any regeneration (the mirror keeps them), a REAL
  `gen_arch_map` regen absorbs both and the delta empties — a mirror-only
  keep would be a permanent lane red here — with the station rule holding
  the same red, and the Component tags clearing both. One lifecycle, TWO
  driftable modules, by necessity: the two absolute arms are disjoint
  syntactic branches (one import statement trips exactly one), so no single
  module can pin both — the fixture tree ships both flat-layout shapes
  (`import mod_0` / `from mod_0 import run`), each with no other inventoried
  content, so dropping EITHER arm alone drops exactly its module from the
  delta and reds this one test.
- **No production-code change** — the fixture was GREEN on its first watched
  run: no divergence exposed (the mirror and generator build the same names
  universe — module stems + package directory parts, the scan root's own
  name in neither), so no mirror fix was owed.

**Deviations and judgments.**

1. **The spec's "one fixture: a module"** is delivered as one fixture TEST
   with two one-import modules: a single module cannot red under both
   single-arm mutations (whichever arm survives keeps it inventoried), and a
   both-forms module pins neither alone. The two-module tree is the minimal
   shape under which "either absolute arm dropped ⇒ red" is true; the
   section comment records the why.
2. **The pin was proven to bite** before being trusted: scratch mutations
   (rsync copy, never the worktree) dropping the names-membership arm alone,
   deleting the ast.Import branch alone, and the review's both-dropped probe
   each red exactly the new fixture — 1 failed, 60 passed, all three — with
   the scratch restored byte-identical and re-green (61 passed).
3. **Registration: none owed** — a fixture inside the already-cited
   `tests/test_trajectory_arch.py` suite; no module added, no new LLR/TC
   rows (the WI-406 REVIEW-A precedent).
4. Budgeted docs untouched (no byte deltas).

**Watched, measured on the work commit 34894b48 (clean tree):**
`tests/test_trajectory_arch.py` 61 passed in 1.58s
<!-- fig: cmd="python -m pytest -q -n auto tests/test_trajectory_arch.py" rev=34894b48 -->;
smoke tier 625 passed / 6 skipped in 12.11s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=34894b48 -->;
full suite 1892 passed / 10 skipped in 0:05:04
<!-- fig: cmd="python -m pytest -q -n auto" rev=34894b48 -->.
Green-on-first-run is the correct watched outcome for this WI: the fixture
pins arms the review's probe had already measured consistent; red would have
meant a real divergence, and the mutation drive supplied the red-side
evidence instead.
