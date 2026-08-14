## 2026-08-14 — WI-453: the boundary hats roster executed (Decision 11, rulings 2026-08-13q/r/s)

**Summary.** The `DevStg-Boundary` hats roster lands, all three owed things
from sitting-2 Decision 11 (accepted 13u): FIRST-RUN-ADOPTER's defective
predicate re-pointed at the deliverable; the UX pair + five aspect hats added
with the owner's row text verbatim; the two kinds of silence (by design vs by
defect) stated in both roster headers. Six hats become thirteen in
[`../requirements/hats.toml`](../requirements/hats.toml) and the shipped
[`../../project-trajectory/registries/hats.template.toml`](../../project-trajectory/registries/hats.template.toml).

**Deliverables.**

- **FIRST-RUN-ADOPTER kept, fixed** (ruling 13s). New predicate
  `'tags contains "scripts" or tags contains "templates" or tags contains
  "process"'`, identical in both copies — the kit's product is its shipped
  scripts, templates and process docs, so those are the deliverable's tags.
  Driven as a census over every real work-item context (docs/work front
  matter → `hats.context_from_work_item`): 453 rows; the old `scope ==`
  clauses fire on 0; the whole old predicate on exactly 1 (WI-131,
  2026-07-13); the new predicate on 224
  <!-- fig: cmd=".venv/bin/python -m pytest -q tests/test_hats.py -k old_first_run_adopter" rev=ceb6d5d0 (the test derives the census and asserts all four figures) -->.
- **Seven hats added, row text verbatim from Decision 11** (13u: "the rows
  below and the FIRST-RUN-ADOPTER predicate fix are the text WI-453
  executes" — no owner-text-pending remainder). UX-DESIGNER / UX-ENGINEER:
  `always` in this repo (the REL-002 reader of PROJECT_STATE.html /
  open-items.html), `render`/`ui`-gated in the shipped template — the
  accepted VALUES-diverge split, with asks/listens_for pinned byte-identical
  across copies. SAFETY / LEGAL / DATA-PROTECTION / ACCESSIBILITY /
  PERFORMANCE: each keyed on its own tag, OFF by the grammar's
  undeclared-field rule — no `enabled` key, no schema change — proven silent
  on all 453 real rows and live under their tags.
- **Header distinction** in both rosters: aspect silence BY DESIGN (awaiting
  a tag) vs the old FIRST-RUN-ADOPTER silence BY DEFECT (keyed on a `scope`
  field no context declares — SN-039's job), so no reader has to guess.
- Tests: three new driven tests in `tests/test_hats.py` (the census
  defect/fix proof, the aspect on/off proof, the UX split pin); the live
  and template thirteen-hat pins updated; refusal paths (missing key,
  unevaluable condition, unknown key, malformed/falsey table) were already
  driven and stand. Prose counts (six → thirteen) updated in the kit README,
  `bootstrap.py` and `test_bootstrap.py` comments.

**Deviations from spec.** One, stated plainly: Decision 11 called the old
predicate "silent"; the census found its `tags contains "templates"` clause
had fired on exactly one historical row (WI-131, a workstream label no later
row uses) — so the honest claim is "the `scope ==` clauses never fire and the
hat was effectively voiceless (1 of 453)", and the test asserts that measured
truth rather than a literal zero. No byte-budgeted file touched.

**Checks.** Full unfiltered suite: `pytest -q -n auto` → 2495 passed, 11
skipped in 402.81s
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto" rev=ceb6d5d0 -->;
commit-bar smoke: 1134 passed, 7 skipped in 33.43s
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto -m smoke" rev=ceb6d5d0 -->;
`check_docs --stale` OK (403 docs, 1183 links, 0 broken);
`check_trajectory --root . --strict` clean after the close (rc=0).
