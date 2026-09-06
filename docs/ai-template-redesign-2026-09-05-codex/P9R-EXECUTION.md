# P9R execution: rendering boundary and first text-status extraction

**Basis:** repository state on 2026-09-06, starting from the redesign execution
base `83f2c7aa`. This is a bounded prerequisite and first extraction for
`IMPLEMENTATION.md` P9R. It does not change test cadence, CI selection, or
generated-output freshness. It moves HTML emitters into a physical package and
updates their existing source pointers; it does not change an approval
predicate, an acceptance condition, or an interface's data contract.

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

There is no existing unified typed project-snapshot object to reuse. The two
actual overlapping display reads are the recorded `docs/stage` record and spine
totals. `traj_display.DisplaySnapshot` owns only those immutable facts and is
read once per status or HTML generation. Work-item, interface, source-inventory,
and pending reads stay with their current consumers; no service or intermediate
file was added.

## Test and fixture census

The pre-split inventory collected 303 cases. The current behavioral membership
is broader than a filename prefix and should be treated as follows. The frozen
source collects 306 cases, including the physical renderer-absence and stage-only
compatibility regressions. Moving an existing case between modules does not
add coverage; no execution-speed claim follows from this inventory.
<!-- fig: cmd=".venv/bin/python -m pytest --collect-only -q over the eleven modules below" rev=1e78ada3+OI85-P9R; out/run-logs/oi85-p9r-census.txt -->

| Class | Test modules | Cases | Current smoke tier |
|---|---|---:|---|
| HTML facade/output | `test_gen_trajectory` (20), `test_dashboard_size_budget` (1) | 21 | slow for the facade; size sensor follows its existing classification |
| HTML geometry/rendering | `test_traj_graph` (26), `test_traj_render` (32), `test_traj_render_sweeps` (12) | 70 | slow |
| HTML views/panels | `test_traj_views` (45), `test_traj_panels` (40) | 85 | slow |
| Shared parsing/effects | `test_traj_parse` (7) | 7 | slow, inherited from the pre-split facade |
| Text status | `test_traj_status` (11) | 11 | slow, inherited from the pre-split facade |
| Pending read model | `test_gen_trajectory_pending` (15) | 15 | slow; imports `pending` directly |
| Registry/architecture integrity | `test_trajectory_arch` (97) | 97 | slow; this is `check_trajectory` assurance, not HTML rendering |

The HTML family for eventual affected-capability selection is therefore the
176 cases in the first three rows. The 130 cases in the last four rows are
core/shared assurance or compatibility work and cannot be classified as UI
tests from their names. This is an inventory, not a new selector.

`tests/traj_core_fixtures.py` owns the shared parser/status closure:
`make_repo`, work-spec construction, `write_stage`, and frame construction.
`traj_fixtures.py` re-exports those names for HTML callers while retaining its
HTML/bundle/frame helpers and `gen()` facade command. The pending-state tests
use `pending` directly; the two real HTML as-of cases and the one supported
façade re-export assertion live in the HTML family.

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
respectively. These observations predate the one façade-test move and the new
physical-absence status test, so their 173/130 membership is retained as
historical measurement rather than presented as the current 176/129 census.
They are current-workstation observations while other local work was active,
not quiet-box benchmarks, before/after savings, a selector result, or a changed
tier. No full suite or actual-data `gen_trajectory` timing was run in this
measurement sitting.

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
`gen_trajectory.py` now imports only `traj_status`, whose display facts come
from `traj_display`. The existing `main()` parser, exit values, output splice,
and `--check` behavior are unchanged. A normal HTML invocation imports the
five emitters from `scripts/rendering/`. Importing `gen_trajectory` still loads
the complete compatibility facade and retains its re-exported symbols, because
the narrow route is script-only.

The regression is an execution proof rather than a source-text assertion. It
copies the scripts tree without `rendering/`, then copies and runs the actual
parser, status, and pending test modules under that tree. The child collects and
runs all three suites, including the real public `gen_trajectory.py --status`
command. Any core reader that reintroduces an HTML package edge fails with the
package physically absent.

## Local affected-capability selection

`scripts/check_changed.py --base <recorded-ancestor>` implements the small,
conservative P9R table for local use. It compares the whole proposed change
from that ancestor through committed, index, working-tree, and untracked paths;
rename detection is deliberately disabled, so a rename is a delete/add pair.
An absent, non-ancestor, or otherwise unreadable base selects Full. The default
is a JSON preview; add `--run` to execute the listed commands, or `--full` for
phase-close assurance and known layout stress. The ordinary commit checks still
apply separately.

The only narrow classifications are the three named independent validators
(`check_complexity`, `check_figures`, `check_need_form`) and their named tests,
or an existing declared registry/WI carrier whose parsed TOML/frontmatter shape
is unchanged. New/deleted rows or fields, type changes, malformed carriers,
shared parsers/display data, renderer files/assets, bootstrap/tooling, test
selection, and every unlisted path select Full. This is a whitelist, not a
general test-impact engine.

For a narrow result the script runs every test except the seven physical HTML
family modules, one existing real HTML boundary case, derived-stage freshness,
strict trace/schema integrity, and both current dashboard and status freshness
commands. Declared whole outputs (dashboard, stage, open-items, component view and live
approval brief) may accompany a classified edit. Status, CLI and interface
reference blocks may accompany it only when their authored surrounding prose
remains byte-identical; a missing generated companion broadens. The narrow
commands also run each secondary surface's existing freshness enforcer.
A generated file alone never authorizes narrowing. The companion `--check`
commands require current generated output rather than treating it as evidence.
`tests/test_changed_selection.py` covers the ancestor comparison, index/tree/
untracked inputs, data-shape cases, generated companions, rename/delete,
shared-input/tooling broadening, secondary-output freshness commands and Full
override. The table targets this meta-repo's current profile: enabling currently
disabled OKF requires revisiting its affected outputs. It is not a generic
adopter-profile selector.

OI-85's accepted SN-007 wording now permits the declared green bar before a
change lands; it does not narrow CI or phase-close cadence. `check_changed.py`
is local assistance only: CI and the declared Full bar continue to run the
unfiltered suite, and its result says `core+boundary`, never Full.

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

LLR-035 also owns the shared display snapshot and package initializer under
its existing offline-dashboard responsibility (CMP-009); both source pointers
are included so the real component view has no uncontained new module.

The move preserves the described behavior. LLR `module` fields, the derived
component inventory, and IF-052/083/093/094 requestor paths now name
`scripts/rendering/...`; their acceptance text, code symbols, data fields, and
approval predicates remain unchanged. `check_trajectory`'s critique surface
now watches that package, the façade and the root `traj_*.py` shared inputs
in both primary and scaffold layouts. A shared-input change must also stale
affected rendering evidence. IF-011 remains the façade exit-code seam:
its Drafted `data` field now records the long-public `--status --check` stale
outcome alongside normal HTML, with the same 0/1 verdict. The façade remains
the command owner because callers keep one CLI; `traj_status` remains the source
owner of its splice through IF-164. No Status or new interface row is necessary.

Downstream re-sync needs a dated RESYNC_PACK entry when this slice receives its
commit identity: copy `traj_display.py` and the complete `rendering/` package
with the updated façade and bootstrap mapping. A reviewed operator may then
delete the five former root-level `traj_*.py` emitters only after the adopted
tree's normal dashboard and `--status --check` commands pass. `--force` is not
a recommendation to overwrite adopter-owned files.

## Verification and remaining prerequisites

Focused verification:

```text
.venv/bin/python -m pytest -q tests/test_traj_parse.py \
  tests/test_traj_status.py tests/test_gen_trajectory_pending.py
32 passed in 4.73s
```

`gen_components.py --root . --check` passes after regenerating the derived
component list. The supervising review deliberately re-stamped the module-size
ratchet for the repaired responsibilities: `agent_loop.py` 2678→2685,
`bootstrap.py` 1663→1665 and `check_trajectory.py` 2336→2349 SLOC. Function
complexity ceilings are unchanged; the continuation log records the reasons.
<!-- fig: cmd="check_complexity.module_sloc on the three named scripts" rev=1e78ada3+OI85-P9R -->

The physical package, display snapshot, fixture split, and renderer-absent
collection proof are complete. Completion evidence and rollout limits:

1. Final unfiltered validation passed: `3661 passed, 22 skipped in 744.34s`.
   Its HTML family is 176 passed and its P9R core/shared group is 130 passed.
   Current dashboard/status/component/reference freshness checks pass. These
   are observed results; no matched before/after speedup is claimed.
2. The local selector's classified cases pass 45 tests and an independent
   [closure review](../reviews/2026-09-06-oi85-p9r-selector-closure-structured-opus.md).
   Its new Git-fixture integration tests run at Full/CI under the existing slow
   criterion; no existing smoke test moved. First narrow use on an ordinary
   proposed change remains an operational observation, not a claimed speedup. CI/phase-close narrowing remains a separate cadence
   decision and retains the Full fallback.
3. A dated RESYNC_PACK entry remains contingent on the integration commit
   identity. It must give adopters the reviewed copy/delete procedure already
   stated above; no generic automatic migration is justified.
4. The façade's public re-exports remain supported compatibility surface. Their
   deletion requires an explicit supported-release retirement and replacement
   consumer proof, not a fixture-cleanup assumption.


### Final measurement (2026-09-06)

The final command was `.venv/bin/python -m pytest -q -n auto
--junitxml=out/run-logs/oi85-full-final.xml`, unfiltered. The XML groups the
current behavioral census without treating parallel testcase durations as wall
time:

| Group | Collected cases | Sum of reported testcase seconds | Failures |
|---|---:|---:|---:|
| Seven HTML modules | 176 | 220.77 | 0 |
| Four P9R core/shared modules | 130 | 18.26 | 0 |
| Rest of full suite (including skips) | 3377 | 1844.53 | 0 |

The overall wall time was 744.34 seconds; the row durations overlap across
workers and are not additive wall savings. This complete redesign proposal
selects Full under `check_changed.py --base 1e78ada3`, as expected for package,
shared-input and test-tooling changes. No narrowed execution is represented as
this Full result. A first ordinary-change narrow run remains to be observed.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto --junitxml=out/run-logs/oi85-full-final.xml; XML testcase grouping by the eleven modules in this record" rev=1e78ada3+OI85-final; out/run-logs/oi85-full-final.txt -->
