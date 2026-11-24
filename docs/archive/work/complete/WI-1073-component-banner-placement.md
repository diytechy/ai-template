+++
id = "WI-1073"
title = "The component view's header and its generator's docstring state placement as the placement row does"
workstream = "process"
specref = ""
sr_refs = ["SR-070", "SR-249"]
needs = ["WI-1071"]
buildtier = "light"
safety_class = "ordinary"
priority = 4
planmode = "none"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1073`, cut from `refactor_again`
at `d1571e8fc`, with the commit hooks on and no plan (`planmode = "none"`).
No status moved, no snapshot was taken, no id was minted and no decisions
record was written: the choice is the one LLR-403 already states.

- `541f32d5b`: the build: the header and the docstrings, the test, the
  regenerated view, the RESYNC entry.
- `3263f8d37`: the close-out.
- The commit after it: the two test-module docstrings, at the coordinator's
  request.

**1. The placement sentence.** The component view's header (the
generator's `BANNER`) said "A design row sits at the owner component of
each interface a test case verifying it names; `[unplaced] llr_refs` lists
the rows placed nowhere." It now reads "A design row sits at the owner
component of each interface its `constrains` cell names and of each
interface a test case verifying it names; `[unplaced] llr_refs` lists the
rows placed by neither." That is LLR-403's placement in the view reader's
terms: through `constrains`, through the verifying test cases, unplaced
otherwise. It names no per-pair or external-owner rule: "owner component"
already says an interface owned by an external party places nothing. The
module docstring's "A DESIGN ROW IS PLACED, NEVER TAGGED" passage says the
same, as does the `build` function's docstring, which carried the same stale
sentence (one clause beyond the module docstring the spec names, in the
same file). The committed `docs/requirements/components.derived.toml` is
regenerated with `trunk_step.py --root . --regen`: its header lines alone
change, with the as-of stamps the regeneration moves in `docs/stage` and
`PROJECT_STATE.html`. No code path changed, so where each row is placed is
unchanged.

**2. The rows and the test.** No spine row's text changes. The test that
already pins the header,
`tests/test_gen_components.py::test_the_view_opens_with_the_generated_file_header`
(tagged TC-195), now also asserts the placement sentence, read from the
header's comment lines joined into prose so a rewrap does not break it. Its
name is unchanged, so TC-195's evidence cell is too. Red first, against the
old sentence:
`FAILED tests/test_gen_components.py::test_the_view_opens_with_the_generated_file_header`,
`1 failed, 18 deselected in 8.18s` (the assertion quoting the old "each
interface a test case verifying it names; `[unplaced] llr_refs` lists the
rows placed nowhere").

**3. The RESYNC entry.** "The component view's header states placement
through `constrains` too `[since d1571e8fc]`": overwrite
`scripts/gen_components.py`, then regenerate and commit the view once, since
its `--check` reads the old header as stale. `scripts/check_resync.py`:
`check_resync: OK, 1 shipped path(s) changed; entry anchored at d1571e8fc72d782dcd26529b00df1d78a67a7661`.

**Tests run.** `tests/test_gen_components.py` alone: `19 passed in 1.58s`.
The modules that import the generator, the spine-linked ones
(`trace.py --tests-for`) and the named ratchets, with the RESYNC readers
and the newline check
(`test_gen_components`, `test_constrains`, `test_if_owner_component`,
`test_llr_trace_cells`, `test_requirement_tree`, `test_trace`,
`test_import_layers`, `test_module_size_ratchet`, `test_complexity_ratchet`,
`test_dogfood_sync`, `test_resync_pack`, `test_check_resync`,
`test_generated_newlines`): `309 passed, 2 skipped in 62.41s (0:01:02)`.
`trace.py --root . --strict`: exit 0, `Traceability: SN=31 SR=141 LLR=372
TC=448 orphans=0 integrity=0 ...`. `check_trajectory.py --root . --strict`:
`clean (1071 work item(s), 943 done (88%), 37 cancelled, graph acyclic)`.
`run_menu.py smoke`, on the close-out tree before its commit: exit 0, its
lints passing (`check_trajectory: clean (1071 work item(s), 944 done (88%),
37 cancelled, graph acyclic).`, `check_docs: OK - 3719 doc(s), 3841
intra-repo link(s), 0 broken.`, the RESYNC check as above) and the tier
`3956 passed, 3 skipped, 18 warnings in 254.02s (0:04:14)`. Its budget line
read `CPU 862.7 s vs 540 s cpu-seconds; wall 254.6 s vs 600 s wall-seconds
... -> OVER`, a warning only, judged by the audit and not charged to this
lane.

**Acts owed for automated adjudication: none.** No `Accepted` row is
amended, no traced change is routed, and no `Drafted` row is new or
rewritten.

**Deviations from spec.** The `build` docstring above. Also, at the
coordinator's request after the close-out, two test-module docstrings that
described placement through the verifying test cases alone now describe
it as the header does, through the `constrains` cell and through the
verifying test cases: `tests/test_gen_components.py` (its "the JOIN"
bullet) and `tests/test_llr_trace_cells.py` (its WI-1023 summary).
Docstrings only, no test behaviour; neither file ships. The two modules:
`44 passed in 5.54s`.

## Context

Filed on trunk on 2026-11-24 by the queue drill's coordinator, from
WI-1071's plan (its decision D13, left out of its scope).

LLR-403 (accepted) places a design row through its `constrains` cell and
through the test cases verifying it (WI-1024's slice 1). The generated
component view's header, written by the component view generator, still
says "A design row sits at the owner component of each interface a test
case verifying it names", and the generator's module docstring says the
same: the placement before `constrains` existed. The view itself places
rows as LLR-403 states; only the explanatory text is stale. WI-1071
restates LLR-199's header clause by the header's four elements (generated,
not to be hand-edited, cite the registries, the regeneration command), so
no spine row carries the stale sentence.

Critiqued 2026-11-24 (Sol and Hydrogen;
`docs/reviews/2026-11-24-scope-critiques/WI-1073.md`): `planmode` is `none`.

## Done-when

- [x] The header's placement sentence and the generator's docstring state
      the placement LLR-403 states (through `constrains`, and through the
      verifying test cases), without restating its precedence rules beyond
      what a reader of the view needs; the committed view is regenerated.
- [x] No spine row's text changes; a test pins the header's placement
      sentence if one already pins the header.
- [x] A RESYNC entry for the shipped generator.
