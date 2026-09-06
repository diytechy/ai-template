# P9R execution: rendering boundary and first text-status extraction

**Basis:** repository state on 2026-09-06, starting from the redesign execution
base `83f2c7aa`. This is a bounded prerequisite and first extraction for
`IMPLEMENTATION.md` P9R. It does not change test cadence, CI selection,
generated-output freshness, the renderer package layout, or any approved row.

## Actual dependency boundary before this slice

`project-trajectory/scripts/gen_trajectory.py` was one compatibility facade and
one command. At module import it loaded every split sibling before `main()`
could route `--status`:

```text
gen_trajectory
├── check_trajectory
├── traj_status ── traj_parse, pending, kitlib.ladder, kitlib.stage
├── traj_parse ─── gen_arch_map, schedule, spine_carrier
└── HTML family
    ├── traj_context ── traj_render
    ├── traj_views ──── traj_graph, traj_parse, traj_render
    ├── traj_panels ─── traj_graph, traj_parse, traj_render, traj_status
    ├── traj_render ─── traj_graph
    └── traj_graph
```

The status implementation itself has no dependency on `traj_context`,
`traj_graph`, `traj_panels`, `traj_render`, or `traj_views`. Its remaining
upstream imports are source readers and policy/state carriers. `traj_parse`
does import `gen_arch_map`, but that module is the AST source-inventory reader;
it does not import the HTML family. No browser automation module is imported by
the status path.

There is no existing unified typed project-snapshot object to reuse.
`traj_status` already consumes the recorded stage, spine/interface rows, work
registry, and pending read model through the existing parsing functions. This
slice preserves those inputs. Creating a new service or an intermediate file
solely to call those functions would add a second model before a shared snapshot
has a demonstrated consumer contract.

## Test and fixture census

The current behavioral membership is broader than a filename prefix and should
be treated as follows. Counts are static test-function counts on this tree;
`pytest --collect-only` collected the combined 303 cases in 0.12 seconds.

| Class | Test modules | Cases | Current smoke tier |
|---|---|---:|---|
| HTML facade/output | `test_gen_trajectory` (17), `test_dashboard_size_budget` (1) | 18 | slow for the facade; size sensor follows its existing classification |
| HTML geometry/rendering | `test_traj_graph` (26), `test_traj_render` (32), `test_traj_render_sweeps` (12) | 70 | slow |
| HTML views/panels | `test_traj_views` (45), `test_traj_panels` (40) | 85 | slow |
| Shared parsing/effects | `test_traj_parse` (9) | 9 | slow, inherited from the pre-split facade |
| Text status | `test_traj_status` (8 after this slice) | 8 | slow, inherited from the pre-split facade |
| Pending read model and compatibility | `test_gen_trajectory_pending` (16) | 16 | slow; several tests still load the full facade to reach re-exports |
| Registry/architecture integrity | `test_trajectory_arch` (97) | 97 | slow; this is `check_trajectory` assurance, not HTML rendering |

The HTML family for eventual affected-capability selection is therefore the
173 cases in the first three rows. The 130 cases in the last four rows are
core/shared assurance or compatibility work and cannot be classified as UI
tests from their names. This is an inventory, not a new selector.

`tests/traj_fixtures.py` is collected only as a helper. At import it loads
`conftest` and the two `kitlib` stage carriers, not the facade or renderer.
It nevertheless mixes status repository builders with HTML/bundle/frame
builders, and its `gen()` helper invokes the shared facade. That content-level
coupling remains for a later fixture split. `test_gen_trajectory_pending` also
retains intentional facade compatibility checks. Neither is needed to make the
public text command import-independent.

## Existing timing evidence

- The archived WI-281 measurement is the only module-level trajectory cost
  ranking found. Before WI-277 split the test facade, `test_gen_trajectory`
  accounted for 440.8 seconds of summed tier duration on a 24-core Python 3.11.9
  run. WI-277 then assigned all split trajectory modules to the same slow tier;
  the current `tests/conftest.py` comments explicitly say this was inheritance,
  not a fresh cost measurement.
- The latest recorded unfiltered suite before this slice is
  `out/run-logs/redesign-full-final.txt`: 3,556 passed, 20 skipped in 713.82
  seconds. It is a whole-suite baseline and cannot establish an isolated
  renderer saving.
- The latest recorded smoke runs are 1,654 passed, 4 skipped in 60.08 and 60.81
  seconds. The renderer/status/parse modules inventoried above are already in
  `SLOW_MODULES`, so this extraction claims no new smoke-time reduction.

No new full suite, parallel heavy run, or renderer-family timing run was made in
this slice. Current per-family wall time therefore remains unknown. A later
P9R sitting must measure core/shared/rendering groups separately before it
changes any selection or makes a latency claim.

## Current-tree per-family measurement (2026-09-06)

The following is the later P9R measurement sitting, not evidence from the
initial extraction above. It used the repository's active working tree and the
same `.venv/bin/python -m pytest -q -n auto` runner for both commands, run
sequentially on Darwin 25.5.0 arm64, Python 3.13.14, six logical CPUs and 8 GiB
memory:

```text
.venv/bin/python -m pytest -q -n auto \
  tests/test_gen_trajectory.py tests/test_dashboard_size_budget.py \
  tests/test_traj_graph.py tests/test_traj_render.py \
  tests/test_traj_render_sweeps.py tests/test_traj_views.py \
  tests/test_traj_panels.py
173 passed in 124.52s

.venv/bin/python -m pytest -q -n auto \
  tests/test_traj_parse.py tests/test_traj_status.py \
  tests/test_gen_trajectory_pending.py tests/test_trajectory_arch.py
130 passed in 4.84s
```

`/usr/bin/time -lp` measured 124.69 seconds and 5.05 seconds of wall time
respectively. These are current-workstation observations while other local work
was active, not quiet-box benchmarks, before/after savings, a selector result,
or a changed tier. No full suite or actual-data `gen_trajectory` timing was run
in this measurement sitting. The large current difference is useful inventory
evidence, but the shared fixtures and compatibility facade described above still
prevent treating the four-module remainder as a proven renderer-free core.

The supervising final check subsequently timed the public command on the actual
current repository: `/usr/bin/time -lp .venv/bin/python
project-trajectory/scripts/gen_trajectory.py --root .` reported `real 5.64`,
`user 5.53`, `sys 0.08` seconds and “already up to date”. This is the current
generation/freshness path, not a cold-start or before/after saving. The final
unfiltered suite took 734.63 seconds; its scope and later wording-only checks
are recorded in [the execution record](EXECUTION-RECORD.md#continuation-validation-and-remaining-decisions).

## Implemented boundary

The public command remains:

```text
python project-trajectory/scripts/gen_trajectory.py --root <repo> --status [--check]
```

For direct script execution with the exact `--status` flag,
`gen_trajectory.py` now imports only `traj_status` from the split sibling block.
The existing `main()` parser, exit values, output splice, and `--check` behavior
are unchanged. A normal HTML invocation loads every renderer sibling as before.
Importing `gen_trajectory` also loads the complete compatibility facade and
retains its re-exported symbols, because the narrow route is script-only.

The regression is an execution proof rather than a source-text assertion. A
fresh subprocess inserts an import finder that raises if any of
`traj_context`, `traj_graph`, `traj_panels`, `traj_render`, or `traj_views` is
loaded, runs the real public status command, checks its zero exit, and verifies
the generated stage snapshot. Any future import edge into that family fails at
the import boundary.

## Contract accounting

The extraction preserves the approved behavior:

- LLR-035 / TC-038: normal generation still produces the self-contained HTML
  dashboard; the representative full-output case remains green.
- LLR-079 and LLR-130 / TC-079: the normal HTML `--check`, determinism, mobile
  CSS, and Git as-of logic remain on the unchanged full path.
- LLR-124 / TC-060: `trunk_step --regen` can keep invoking the same
  `gen_trajectory.py --status` command and status freshness semantics.
- LLR-198: `traj_status` continues to re-export the pending derivation; no
  pending model or compatibility name moved.
- IF-164 continues to name `traj_status` as writer of the generated status
  block. IF-011 continues to name the facade exit-code seam. Both interface
  rows are currently Drafted, while the LLRs and TCs above are Approved.

No source path or code symbol named by an approved row moved, so no registry
source-reference update is required for this slice. IF-011's terse `data` cell
mentions stale HTML but omits its already-public `--status` outcome; that is a
pre-existing interface-description gap. It should be included if the parent
adjudicates or separates the command interfaces, but it does not justify
changing an interface row during this behavior-preserving extraction.

## Verification and remaining prerequisites

Focused verification:

```text
.venv/bin/pytest -q tests/test_traj_status.py \
  tests/test_gen_trajectory.py::test_generates_self_contained_dashboard
.........                                                                [100%]
9 passed in 1.46s
```

Ruff check and formatting pass for the changed source and test. The source
change is 10 net lines in `gen_trajectory.py`; the import-denial regression is
42 lines. No production module was added, and `traj_status.py` / `traj_parse.py`
did not need modification.

P9R is not complete. The remaining evidence and authorization gates are:

1. The current HTML and shared/status/core families are now measured above.
   Actual-data generation and the final broader-suite costs remain in the
   supervising validation record; a matched before/after saving is not proved.
2. Define the shared snapshot only when both text and HTML consumers can use it
   without duplicating decisions, then drive its meaning at that boundary.
3. Split fixture content so collecting core/status tests remains independent
   after the facade compatibility window, and translate pending compatibility
   cases deliberately.
4. Amend SN-007 and any affected assurance/cadence contracts before enabling a
   narrower ordinary-change test policy. Initial CI and full-close behavior
   remain unchanged meanwhile.
5. Prove rename/delete, schema/shared-input, CSS/JS/assets, renderer removal,
   and unknown-base selection cases before relying on affected-capability
   selection. Retain the broad fallback and generated-output freshness.
