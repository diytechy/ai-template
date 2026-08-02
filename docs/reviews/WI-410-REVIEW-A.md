# WI-410 — REVIEW-A (2026-08-02)

Verdict: APPROVE — the whole value of this row is whether the two absolute-arm
pins BITE, so I did not take the builder's word for it: I re-ran every scratch
mutation myself (reduce the `ImportFrom` test to `if node.level:`, delete the
whole `ast.Import` branch, drop both) and each reds EXACTLY the new fixture —
`1 failed, 60 passed` all three times — with the scratch mirror restored
byte-identical (`cmp` clean against the worktree) and re-green (`61 passed`).
The two-module deviation from the spec's "one fixture: a module" was verified
NECESSARY by my own both-forms probe, not just argued. One finding below: the
first-segment `.split(".")[0]` semantics INSIDE each absolute arm remain
unpinned — a same-class residual one grain finer than the arm list this WI was
minted to close, one dotted-import fixture away.

Reviewed independently against the spec
(`docs/work/complete/WI-410-absolute-import-arm-unpinned.md`: fixtures only,
the absolute-import arms of `_has_internal_import` driven through the full
differential lifecycle, plus the scratch-mutation drive proving either
arm-drop bites and nothing else reds; a divergence, if exposed, fixed in the
mirror) and the WI-406 pattern section of `tests/test_trajectory_arch.py`.
Diff = `34894b48` (work, test file only, +49) + `8c25ea04` (close) on
`wi-410-absolute-import-arm-unpinned`, WI-410 delta measured from `af69a6ff`
(the WI-409 integrate the branch claims from). `docs/log.d/` was not read.
All commands run under `/Users/diytechy/Documents/ai-template/.venv/bin/python`
from the worktree; mutations in a scratch rsync copy, never in the worktree.

## Findings

1. **MINOR — the first-segment split inside BOTH absolute arms is unpinned:
   whole-name membership leaves all 61 green.** Scratch mutation: with both
   arms structurally intact, I dropped the `.split(".")[0]` from each —
   `ImportFrom` reduced to `(node.module or "") in internal_names`,
   `ast.Import` to `a.name in internal_names`
   (`project-trajectory/scripts/check_trajectory.py` `_has_internal_import`)
   — `tests/test_trajectory_arch.py` ran **61 passed in 2.96s**. Both WI-410
   modules survive trivially (their whole names `mod_0` ARE in the names
   universe), so a DOTTED-absolute-import-only module (`import pkg.mod` /
   `from pkg.mod import x`, where `pkg` is a scanned package directory) can
   drift exactly the WI-406-finding-1 way: the generator keeps it
   (`internal_imports` splits the first segment, `gen_arch_map.py:210`), the
   mutated mirror skips it, and the wi-387 station-first topology returns for
   the dotted shape. **The honest bound:** the spec's mutation drive was
   "either absolute arm is DROPPED" — both arm-level drops now bite, so the
   spec was delivered as written; this is the same-class residual its own
   pattern predicts, one `import pkg.mod`-only fixture away. **Does not
   change the verdict** — worth an intake row, not a rework round. -> @owner

## None against — what I tried and could not break

- **Pin 1 bites, and only its fixture.** Scratch mutation reducing the
  `ImportFrom` test to `if node.level:` (names-membership arm dropped) →
  `FAILED tests/test_trajectory_arch.py::test_absolute_import_only_modules_are_inventoried_on_both_sides`
  on `assert "scripts/abs_from" in strict.stderr` — **1 failed, 60 passed in
  2.85s**. No collateral reds.
- **Pin 2 bites, and only its fixture.** Deleting the whole
  `elif isinstance(node, ast.Import):` branch →
  the same test, on `assert "scripts/abs_imp" in strict.stderr` —
  **1 failed, 60 passed in 2.85s**.
- **The review's both-dropped probe now bites.** Both mutations together
  (the exact shape WI-406 REVIEW-A finding 1 ran green across 60 tests) →
  the same test, on `assert strict.returncode == 1` (the mirror keeps
  neither, the delta empties, rc 0) — **1 failed, 60 passed in 2.82s**.
  All three failure modes land exactly where the section comment promises
  (two name asserts, one rc assert). Scratch then restored: `cmp` against
  the worktree's `check_trajectory.py` **byte-identical**, module re-ran
  **61 passed in 2.94s** — the mutations were the only cause.
- **The two-module deviation is NECESSARY, not padding — probed, not just
  argued.** The spec said "one fixture: a module"; the builder shipped one
  test with TWO one-import modules, arguing the arms are disjoint syntactic
  branches. I wrote a scratch probe running the same lifecycle on a SINGLE
  module carrying BOTH forms (`import mod_0` + `from mod_0 import run`):
  under the names-membership-drop mutation it **passed** (1 passed), under
  the `ast.Import`-branch-delete it **passed** (1 passed) — the surviving
  arm keeps the module both times, so a both-forms module pins NEITHER arm
  alone (it fails only under the both-dropped probe). Two separately
  driftable one-form modules are the minimum that makes each single-arm
  mutation red; the Deliverable records the deviation in exactly those
  terms ("One lifecycle, TWO driftable modules, by necessity"). Honest and
  correct.
- **The names-universe claim, verified in code AND empirically.** Generator
  (`gen_arch_map.py` `_module_files`): `names.add(path.stem)` + the rel-path
  directory parts — the scan root's own name is excluded. Mirror
  (`check_trajectory.py` `shipped_modules`): `names.add(path.stem);
  names.update(rel.parts[:-1])` — same universe. Probe: a module whose only
  content is `from scripts import mod_0` + `import scripts.mod_1` on the
  fixture tree — strict rc **0** pre-regen (mirror skips it), regen leaves
  the map unchanged, rc **0** after (generator skips it too): external on
  both sides alike, exactly as the fixture comment states. This also means
  the spec TITLE's literal example shapes (`import scripts.sibling` /
  `from scripts import sibling`) could never have pinned anything — the
  builder's flat-stem substitution was load-bearing, and the fixture
  comment records the why.
- **Differential integrity — real generator, both sides, all four
  stations.** The shipped test asserts: rc==1 + `not yet in the committed
  arch-map` naming BOTH modules + the `2 shipped module(s)` count BEFORE any
  regen; `regen_map` runs the REAL `gen_arch_map.py` (asserts rc==0); after
  regen the ADDED red is gone (a mirror-only keep would be a permanent lane
  red) while `arch-map module(s) are in no CMP-### component` holds the same
  red; tagging all four modules clears to rc==0. Same lifecycle as the
  WI-406 section it extends.
- **The record, re-run rather than read.** In the worktree at `8c25ea04`:
  `python -m pytest -q -n auto tests/test_trajectory_arch.py` → **61 passed
  in 1.63s** — the Deliverable's module fig re-driven with exact agreement
  (this is the spot-checked declared figure). Smoke tier → **629 passed,
  2 skipped in 10.93s** — matches the close commit's 629/2 (the Deliverable
  fig at `34894b48` says 625/6 — same universe of 631, the
  environment-dependent-skip delta this review family has recorded before).
  The full-suite fig (**1892 passed / 10 skipped in 0:05:04** at `34894b48`)
  is the BUILDER'S, attributed not re-run — module + smoke + strict is this
  review's tier. `check_trajectory --root . --strict` rc=0 — WARN set
  diffed line-for-line against trunk: **identical**, none about WI-410;
  `check_doc_refs --strict` rc=0; `check_figures --strict` rc=0, **57
  declared figure(s), every one carrying its command and revision** —
  matching the close claim exactly. `ruff check` All checks passed;
  `ruff format --check` 1 file already formatted.
- **Fixtures-only, proven from the delta.** The whole WI-410 delta vs
  `af69a6ff`: `tests/test_trajectory_arch.py` (+49, the work commit's only
  file), the queued→complete spec move, the unread `docs/log.d/` fragment,
  `PROJECT_STATE.html` (claim-commit dashboard regen), and `docs/gate`
  (claim-commit `as-of` hash bump only — still `G3`, same basis line). Zero
  production `.py` hunks; the `docs/work/` delta is exactly the WI-410
  move and nothing else. Matches the spec's "Scope:
  tests/test_trajectory_arch.py only" and the Deliverable's "no
  production-code change"; budgeted docs untouched, as claimed.
- **R-A / R-F.** The close cleared
  `specref = "docs/reviews/WI-406-REVIEW-A.md"` (present in the active
  spec's frontmatter deleted at `8c25ea04`, absent from the complete spec).
  The Deliverable is dated 2026-08-02, names the work commit, and every
  claim in it either re-ran green here (module fig exact, all three
  mutations re-proven, the disjointness argument probed, the names-universe
  claim probed, no-production-change verified) or is reconciled above
  (smoke env delta, attributed full-suite fig). The `WI-410` token at
  `docs/status.md:173` sits inside the GENERATED STATUS block (ready
  frontier — exempt from forward-only; drops at the merge regen, the same
  shape the WI-406 review recorded).
- **Registration judgment — sound.** No new LLR/TC rows: one fixture inside
  the already-cited `tests/test_trajectory_arch.py` suite, no module added,
  no public surface — the WI-406 REVIEW-A precedent the Deliverable cites.

**THIS IS AN APPROVE:** both absolute-arm pins were re-proven to bite by
reviewer-run mutations, each single-arm drop and the review's both-dropped
probe redding exactly the new fixture and nothing else; the two-module shape
was proven necessary by a both-forms probe that pins neither arm alone; the
differential runs the real generator on both sides; the branch is provably
fixtures-only; and the record re-ran green (builder's full-suite fig
attributed, per this review's tier). The one finding is a finer-grain
residual inside the now-pinned arms — an intake candidate, not a defect in
what shipped.

VERDICT: APPROVE findings=1
