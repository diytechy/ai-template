# WI-406 — REVIEW-A (2026-08-02)

Verdict: APPROVE — the whole value of this row is whether the three pins BITE,
so I did not take the builder's word for it: I re-ran every scratch mutation
myself (drop `node.level`, delete the Contracts block-walk, flip the
SyntaxError arm) and each reds EXACTLY its fixture — `1 failed, 59 passed` all
three times — with the scratch copy diffed back byte-identical to the shipped
tree and re-green afterwards. The `from . import notes` isolation claim also
reproduces exactly as stated. One finding below: the same probe shows the
ABSOLUTE-import arms of the mirror remain unpinned — a same-class residual,
outside the spec's named arm list, one fixture away.

Reviewed independently against the spec
(`docs/work/complete/WI-406-differential-fixtures-cover-all-mirror-arms.md`:
fixtures only, one per unpinned arm — re-exporting `__init__`,
contracts-comment-only, parse-error — each green-or-red identically in the
lane rule and after a REAL `gen_arch_map` regen; a divergence, if exposed,
fixed in the mirror). Diff = `29af0fcb` (work) + `7af16f2f` (close) on
`wi-406-differential-fixtures-cover-all-mirror-arms` vs merge-base
`f85bf39b`. `docs/log.d/` was not read. All commands run under
`/Users/diytechy/Documents/ai-template/.venv/bin/python` from the worktree;
mutations in a scratch rsync copy, never in the worktree.

## Findings

1. **MINOR — the absolute-import arms of `_has_internal_import` are still
   unpinned: dropping BOTH names-universe arms leaves the whole module
   green.** Scratch mutation: with `node.level` intact, I reduced the
   `ImportFrom` test to `if node.level:` and deleted the entire `ast.Import`
   branch (`project-trajectory/scripts/check_trajectory.py` `_has_internal_import`)
   — `tests/test_trajectory_arch.py` ran **60 passed in 1.54s**. So a
   docstring-less module whose only content is an ABSOLUTE internal import
   (`import notes`, or flat-layout `from notes import x`) can drift exactly
   the way WI-399 REVIEW-A finding 4 described: the mirror would skip it, the
   generator keeps it, and the wi-387 stale-map topology returns for that
   shape — the station becomes first-to-know. **The honest bound, stated
   precisely:** the hunted shape `from .notes import x` itself CANNOT drift —
   it is doubly covered (`node.level` AND the names arm; I verified the swap
   survives the node.level mutation, below), and any edit killing both arms
   at once reds the shipped `from . import notes` pin via node.level. The
   genuinely driftable residual is the absolute-import-ONLY module — a fringe
   shape, and OUTSIDE the finding-4 arm list this WI was minted to close
   ("import-only re-exporting `__init__`" — idiomatically relative), so the
   spec was delivered as written. The builder's commit even names the
   "absolute-segment-in-names arm" as the survival route without noting it is
   itself unpinned. **This does not change the verdict**: same-class residual,
   one `import notes`-only fixture away — worth an intake row, not a rework
   round. -> @owner

## None against — what I tried and could not break

- **Pin 1 bites, and only its fixture.** Scratch mutation dropping
  `node.level` from `_has_internal_import` (condition reduced to the
  names-universe membership): full module run →
  `FAILED tests/test_trajectory_arch.py::test_reexporting_init_is_inventoried_on_both_sides_of_the_regen`,
  **1 failed, 59 passed in 1.48s**. No collateral reds — "exactly its
  fixture" holds.
- **Pin 2 bites, and only its fixture.** Deleting the first-8-lines Contracts
  block-walk from `_would_be_inventoried` →
  `FAILED ...::test_contracts_comment_only_module_is_inventoried_on_both_sides`,
  **1 failed, 59 passed in 1.45s**.
- **Pin 3 bites, and only its fixture.** Flipping the SyntaxError arm to
  `return False` →
  `FAILED ...::test_parse_error_module_stays_inventoried_on_both_sides`,
  **1 failed, 59 passed in 1.44s**. Scratch then reverted; both mutated files
  diffed byte-identical to the worktree (`scratch == shipped`) and the module
  re-ran **60 passed in 1.49s** — the mutations were the only cause.
- **The `from . import notes` isolation claim, reproduced exactly.** Under
  the node.level mutation I swapped the fixture body to
  `from .notes import x`: the test **passed** (1 passed in 0.20s) — the shape
  survives via the absolute-segment-in-names arm, exactly as the builder's
  comment and commit message state, so `module=None` is the ONLY shape in
  this tree that isolates the node.level arm. The chosen fixture is honest
  isolation, not papering-over — the residual it leaves is finding 1's
  absolute-only shape, not this one.
- **Differential integrity — real generator, both sides, all four stations.**
  Each fixture: rc==1 + `not yet in the committed arch-map` naming its module
  BEFORE any regen (the mirror keeps it against a stale committed map);
  `regen_map` runs the REAL `gen_arch_map.py` and asserts rc==0 — for the
  parse-error fixture that assert IS the generator-half pin
  (kept-not-crashed, rendered PARSE ERROR); after regen the ADDED red is
  gone (the generator absorbed the key — a mirror-only keep would be a
  permanent red here) while `arch-map module(s) are in no CMP-### component`
  holds the same red; `_tag_three` then clears to rc==0. The `__init__`
  fixture additionally pins the flip side in the same tree: `1 shipped
  module(s)` + `scripts/pkg/notes` absent — the comment-only sibling is
  skipped by BOTH sides inside a package, under the `/__init__`-stripped key
  `scripts/pkg`.
- **The record, re-run rather than read.** In the worktree at `7af16f2f`:
  `python -m pytest -q -n auto tests/test_trajectory_arch.py` → **60 passed
  in 1.52s** — the Deliverable's module fig re-driven with exact agreement
  (this is the spot-checked declared figure). Smoke tier → **625 passed,
  2 skipped in 10.32s** (Deliverable fig at `29af0fcb` says 621/6 — same
  universe of 627, the environment-dependent skips pass on this machine; the
  identical delta WI-405 REVIEW-A recorded). The full-suite fig (**1883
  passed / 10 skipped in 0:04:44** at `29af0fcb`) is the BUILDER'S,
  attributed not re-run — the refresh bar owns the full tier mechanically
  per this review's charter. `check_trajectory --root . --strict` rc=0 —
  WARN set diffed line-for-line against trunk: **identical**, none about
  WI-406; `check_figures --root . --strict` rc=0, **43 declared figure(s),
  every one carrying its command and revision**; `check_doc_refs --root .
  --strict` rc=0; `ruff format --check` 152 files already formatted;
  `ruff check` All checks passed. `check_docs --root . --stale` FAILs (4
  broken links / 404 orphans) — **pre-existing**: the identical run on trunk
  FAILs with the same totals, and the finding-line diff is exactly the
  expected WI-406 spec-move orphan swap (active→complete, the allow-listed
  closed-WI class), nothing else.
- **Fixtures-only, proven from the delta.** The whole branch delta vs
  merge-base is four paths: `tests/test_trajectory_arch.py` (+93, the work
  commit's only file), the active→complete spec move, and the unread
  `docs/log.d/` fragment. Zero production `.py` hunks; the `docs/work/`
  delta is exactly the WI-406 move. Matches the spec's "fixtures only" and
  the Deliverable's "no production-code change".
- **R-A / R-F.** The close cleared
  `specref = "docs/reviews/WI-399-REVIEW-A.md"` (present at `7af16f2f^`,
  absent in the complete spec's frontmatter). The Deliverable is dated
  2026-08-02, names the work commit, and every claim in it either re-ran
  green here (module fig exact, mutations re-proven, isolation reproduced,
  no-production-change verified) or is reconciled above (smoke env delta,
  attributed full-suite fig). The `WI-406` token at `docs/status.md:173`
  sits inside the GENERATED STATUS block (lines 166–177 — exempt from
  forward-only; drops at the merge regen).
- **Registration judgment — sound.** No new LLR/TC rows: three fixtures
  inside the already-cited `tests/test_trajectory_arch.py` suite, no module
  added, no public surface — the same judgment WI-405's review graded
  defensible for the same suite family.
- **Tier placement — by design, worth knowing.** `test_trajectory_arch` is
  in `tests/conftest.py` `SLOW_MODULES` (WI-281 budget: check_trajectory
  run_py subprocesses), so the three pins sit in the full tier — slice
  close, refresh bar, CI — not the per-commit smoke bar; smoke's 625/627
  universe is unchanged by this WI. That is the whole differential family's
  placement, not a WI-406 choice.

**THIS IS AN APPROVE:** all three pins were re-proven to bite by
reviewer-run mutations, each redding exactly its fixture and nothing else;
the deliberate `from . import notes` shape is verified as the only
node.level-isolating shape in the tree; the differential runs the real
generator on both sides of every fixture; the branch is provably
fixtures-only; and the record re-ran green (builder's full-suite fig
attributed, pending the refresh bar). The one finding is a same-class
residual outside the specced arm list — an intake candidate, not a defect in
what shipped.

VERDICT: APPROVE findings=1
