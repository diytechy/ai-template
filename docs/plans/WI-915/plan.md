# WI-915 plan, revision 2: docs/stack.ini is parsed in one place

## Revision 2: the critique's finding, judged

Revision 2 answers `docs/plans/WI-915/critique-1.md` (one finding). Read the
finding as a claim and checked it against the code at the lane tip
`eace6c944`.

- **F1 (MAJOR), CONFIRMED.** `tests/test_module_size_ratchet.py` compares
  each listed module's size to its stamp for exact equality and fails on
  shrink as well as growth. The file says so itself ("A RE-STAMP DOWN, which
  this ratchet requires in the same commit — the assertion fires on shrink
  too"). The module is not in `tests/conftest.py` `SLOW_MODULES`, so the
  commit bar's smoke tier runs it. The refactor commit changes the size of
  all four listed modules (`check.py`, `trace.py`, `integrate.py`,
  `agent_common.py`), so revision 1's allowed order, with P8 after that
  commit, cannot pass its own commit bar. **Fix:** P8's measurements, the
  four re-stamps and their reasons are now part of the P2 to P7 refactor
  commit. The builder applies them before running that commit's bar. P8
  keeps P7 as its predecessor, because it measures the finished edits. The
  `[dupes-census]` re-stamp, if its reading moves, also goes in the same
  commit. The census never fails a gate (`docs/stack.ini` `[dupes-census]`:
  "never fails a gate even under --strict"), so this is for consistency, not
  a forced coupling. P9, the `RESYNC_PACK.md` entry, may still follow as its
  own commit. `tests/test_resync_pack.py` checks entry grammar, anchors and
  order, not that the entry and the kit-file change share a commit. Covered
  by row P8 (and the commit-shape paragraph under Steps).

The rest of revision 1 stands. The delta answer is re-derived below and
stays the same.

Planner: fresh session, 2026-10-17. Inputs read: the spec
`docs/work/active/wi-915/WI-915-one-stack-ini-loader.md` in full; its specref,
`docs/plans/2026-10-11-review-churn/README.md` §10 (the owner ruling and the
program, step 1 of which is this row); the coordinator's ruled calls Q1 to Q7
as the spec quotes them (coordinator-2026-10-14 D-004); the handoff's
mechanism-change rule (`docs/handoff-2026-10-11-attended-coordinator.md`,
"Mechanism changes land one at a time"). Spine read: SR-007 and SR-166
(`docs/requirements/system-requirements.toml`); TC-007, TC-008, TC-176 and
TC-331, the four TCs whose `verifies` names one of them
(`docs/test/test-cases.toml`); IF-022, IF-049 and IF-068, the three rows owned
by `docs/stack.ini` (`docs/requirements/interfaces.toml`); CMP-006 to CMP-009
(`docs/requirements/components.toml`); `docs/runtime-flows.md` ("Declared
config ... read once by the harness", which this row makes literally true and
does not edit). Code read at the lane tip `6533a2331` (equal to trunk
`refactor_again`): the 13 sites, `kitlib/config.py`, `kitlib/evidence.py`'s
other uses of `STACK_FILE`, `tests/test_module_size_ratchet.py`,
`docs/complexity-baseline`, `docs/stack.ini` `[dupes-census]` and
`[generated]`, `tests/conftest.py` `SLOW_MODULES`, `integrate.py`'s
`_HAND_STAMPED_GENERATED_KINDS`, and `RESYNC_PACK.md` §4's latest entry.

## What the code says that the spec does not

- **Line drift since `ff64d366b`.** Two sites moved: `check.py`'s
  `_generated_census` construction is at L1682 (spec L1664), and
  `scripts/check_smoke_budget.py`'s at L65 (spec L61). The other eleven match.
  `git grep -n 'ConfigParser(' -- project-trajectory/scripts scripts` prints
  the 13 lines the spec counts, in 12 files.
- **Every other `configparser` use in those files is the error class at the
  same site** (`configparser.Error` in the `except` beside each construction).
  So D2 is reached by the site edits alone; no other code in those files needs
  `configparser`.
- **`kitlib/evidence.py` uses `STACK_FILE` as a string dict key**
  (`found[STACK_FILE]`, L132, read by `record_test_evidence.py:130`), while
  `check.PROFILE_FILE` and `run_menu.DEFAULT_STACK_INI` are `Path`s and
  `scripts/check_smoke_budget.STACK_INI` is absolute. The one named location is
  therefore the relative POSIX string `"docs/stack.ini"`; each site's constant
  keeps its name AND its type by deriving from it (`Path(...)`, the bare
  string, `ROOT / ...`).
- **`tests/test_stack_profile.py` is in `SLOW_MODULES`** (`tests/conftest.py`,
  "scaffold-profile byte-compare"). The spec puts the characterization test
  there, as TC-007's evidence file, so the commit bar's smoke tier never runs
  it. The plan does not move the module's tier (that would move the smoke
  budget, outside this row); instead every step below runs the module
  explicitly, and the landing bar's full suite runs it. Flagged for the
  critic: if the coordinator wants an in-process smoke pin, a separate small
  smoke module is the shape, and it is not in this plan.
- **None of the 13 site functions is in `docs/complexity-baseline`**, and of
  the touched modules only `check.py`, `trace.py`, `integrate.py` and
  `agent_common.py` are in the module-size ratchet's `BASELINE` (threshold
  1000). `kitlib/config.py` (434 lines) stays far under it.
- **`tests/test_module_size_ratchet.py` is a `[generated]` path of kind
  `linecounts`, the one hand-stamped kind** (`integrate.py`
  `_HAND_STAMPED_GENERATED_KINDS`): a lane re-stamps it by hand with a reason,
  which is what D7 asks.
- **Both build holds are already met at this tip.** The baseline manifest is
  committed on trunk at `fa4bd0c49` ("review-churn plan revision 38: the
  phase-0 baseline manifest (row M)"), and WI-913 landed at `b803dd019`. P0
  re-confirms both at build start and P11 at landing.

## The reader's shape (P2)

In `project-trajectory/scripts/kitlib/config.py`, beside the `process.toml`
readers. Names are the plan's proposal; the builder may rename before the
first commit that imports them, never after.

- `STACK_INI = "docs/stack.ini"`: the one named location.
- `class StackIniError(Exception)`: the one error type. Not a `ValueError`
  subclass, so no site's existing broad `except` catches it by accident; every
  site maps it explicitly.
- `read_stack_ini(path, *, fold_keys=True)`:
  - `Path(path).exists()` false: return `None`.
  - Otherwise construct `configparser.ConfigParser(interpolation=None)` (the
    one construction in the tree), set `optionxform = str` when `fold_keys` is
    false, read `path.read_text(encoding="utf-8-sig", errors="replace")` and
    `read_string(..., source=str(path))`, so every parse error names the file.
  - `configparser.Error` or `OSError` (a directory at the path, a permission
    error): `raise StackIniError(str(exc)) from exc`. `str(OSError)` already
    names the path.
  - Return the `ConfigParser`.
  - Docstring states the parse options once (interpolation off, `=`/`:`,
    whole-line `#`/`;` comments, duplicates refused, `[DEFAULT]` inherited,
    keys folded unless `fold_keys=False`) and carries `Implements: SR-007`
    (Q3). No cache, no defaults, no value checks.
- `__all__` gains the three names.

`kitlib/config.py` imports only `kitlib.ladder` today; adding `configparser`
(stdlib) keeps it import-clean, so `tests/test_import_layers.py` and TC-176's
kitlib-only-imports pin see no cycle.

## The site mapping (P3 to P6)

Each site keeps its function name, key case, defaults and failure rule; only
the cells the spec's "Moves under Q1 and Q2" column names change.

| # | Site | Call | `None` (absent) maps to | `StackIniError` maps to |
|---|---|---|---|---|
| 1 | `check.load_profile` | default fold | `None` | `sys.exit("check: {} is malformed: {}")`, today's text |
| 2 | `check._generated_census` | `fold_keys=False` | `[]` | `[]` |
| 3 | `agent_common._declared_test_command` | default fold | `raise ValueError(...)` naming the file (keeps "absent: ValueError") | `raise ValueError(str(exc)) from exc` |
| 4 | `agent_policy.read_agent_loop_config` | default fold | `{}` | `{}` |
| 5 | `check_doc_refs._scan_profile` | default fold | `("src", "symbols")` | `("src", "symbols")` |
| 6 | `check_dupes_census._load_baseline` | default fold | `None` | uncaught (traceback) |
| 7 | `integrate._generated_table` | `fold_keys=False` | `{}` | `{}` |
| 8 | `kitlib.evidence.source_paths` | default fold | `[]` | `[]` |
| 9 | `run_menu.load_capabilities` | `fold_keys=False` | `[]` | `sys.exit("run_menu: {} is malformed: {}")`, today's text |
| 10 | `trace._cmd_tests_for` (reads `docs / "stack.ini"`, as today) | default fold | test root `tests` | uncaught (traceback) |
| 11 | `trajectory_arch._stack_ini_get` | default fold | `None` | `None` |
| 12 | `trunk_step._profile` | default fold | `None` | `None` |
| 13 | `scripts/check_smoke_budget._profile` | default fold | returned; the caller's subscript still raises (traceback) | uncaught (traceback) |

Path constants: `check.PROFILE_FILE = Path(_kitconfig.STACK_INI)`,
`run_menu.DEFAULT_STACK_INI = Path(...STACK_INI)`,
`kitlib.evidence.STACK_FILE = STACK_INI` (string, from `.config`),
`check_dupes_census.STACK_INI = ...STACK_INI` (string),
`scripts/check_smoke_budget.STACK_INI = ROOT / STACK_INI`. Each import of
`kitlib.config` follows the file's existing import idiom (guarded where the
file guards its `kitlib` imports; `sys.path` insert in
`scripts/check_smoke_budget.py`, as `scripts/check_changed.py` does).

## Architectural delta

The row adds no state (the reader caches nothing; each call reads the file, as
each site does today), no value to any domain (each site maps `None` and
`StackIniError` onto outcomes it already has, per the table above), no new
input to any output (the same file; under Q1 a BOM or stray byte reads as
`check.py` already reads it, and Q2 sends an unreadable path to an outcome the
site already has for a malformed file), and crosses no new boundary
(`kitlib/config.py` is a declared shared-kernel module, `docs/kernel-modules-allow`
L50, already imported across CMP-006 to CMP-009; edges into a declared kernel
are not seams under OI-48; the new edges from `integrate.py`,
`kitlib/evidence.py` and this repo's `scripts/check_smoke_budget.py` point into
it). IF-022, IF-049 and IF-068 keep their owner, consumers, channel and data;
their stale notes wait for item 11 (Q6).

Re-asked for revision 2: F1 changes only which commit the ratchet re-stamps
go in. It adds no state, no domain value, no input and no boundary, so the
answer stands.

DELTA: none

## Steps

Commit shape, as the spec fixes it: P1 is the lane's first code commit, on the
unrefactored code. P2 to P7 are the one refactor commit that removes the
strict-xfail marks; the builder works site by site, removing each site's marks
as it converts it and running the characterization test after each, but
commits once. P8 is part of that same commit, not optional (F1). The exact-size
ratchet runs in the commit bar and fails on any change in a listed module's
size, shrink included. So the builder finishes P3 to P7, measures, applies
P8's re-stamps and reasons, and only then runs the bar and commits. P9 may
share that commit or follow it. P10 and P11 are checks, not edits.

Why clauses repeat across rows (the gate's multi-cover note): D1 to D5 are
properties of all 13 sites together, so each script-family row (P3 to P6, the
spec's S4 split W1 to W4) delivers its share and P7 checks the whole; D9 and
D10 are holds checked at build start (P0) and again at the landing tip (P11).
No scope is duplicated.

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P0 | Build-start holds and base reading: WI-913 landed (`b803dd019`) and the baseline manifest on trunk (`fa4bd0c49`); record the 13-line `ConfigParser(` grep, the dupes-census reading and the four ratchet sizes at the claim base | D9; D10; SR-007 | no interface (reads only) |  |
| P1 | Characterization test on the unrefactored code: 13 sites by 9 input classes, today's outcomes, ruled cells as strict expected failures | D4; SR-007; TC-007; TC-008 | IF-022; IF-049; IF-068 (exercised through their readers, not changed) | P0 |
| P2 | The reader in `kitlib/config.py`: `STACK_INI`, `StackIniError`, `read_stack_ini(path, *, fold_keys=True)`, the parse options stated once, `Implements: SR-007`; its own unit tests | D1; D3; SR-007; TC-007; TC-008 | no interface (a function added to a declared shared-kernel module; OI-48: an edge into the kernel is not a seam) | P1 |
| P3 | W2 sites through the reader: `check.load_profile` and `check._generated_census` (sites 1, 2), `check_doc_refs._scan_profile` (5), `check_dupes_census._load_baseline` (6); `check.PROFILE_FILE` and `check_dupes_census.STACK_INI` from `STACK_INI`; `check.py`'s top-level `import configparser` goes; `tests/test_flag_axis.py:201` imports `configparser` itself | D1; D2; D3; D4; D5; SR-007; TC-007; TC-008 | IF-022 (consumer-side read path only; form and consumers unchanged) | P2 |
| P4 | W1 sites: `trace._cmd_tests_for` (10), `trajectory_arch._stack_ini_get` (11), `kitlib.evidence.source_paths` (8); `kitlib.evidence.STACK_FILE` from `STACK_INI` | D1; D2; D3; D4; D5; SR-007; TC-007 | IF-022 (consumer-side read path only) | P2 |
| P5 | W3 sites: `agent_common._declared_test_command` (3), `agent_policy.read_agent_loop_config` (4), `integrate._generated_table` (7), `trunk_step._profile` (12) | D1; D2; D3; D4; D5; SR-007; TC-007 | IF-022; IF-068 (consumer-side read path only) | P2 |
| P6 | W4 and this repo's tool: `run_menu.load_capabilities` (9), `scripts/check_smoke_budget._profile` (13); `run_menu.DEFAULT_STACK_INI` and `check_smoke_budget.STACK_INI` from `STACK_INI` | D1; D2; D3; D4; D5; SR-007; TC-007 | IF-049; IF-022 (consumer-side read path only) | P2 |
| P7 | One-home sweep: the restating comments at `check.py`, `run_menu.py`, `trunk_step.py`, `check_doc_refs.py`, `agent_common.py` and `scripts/check_smoke_budget.py` (and the `optionxform` notes at `check._generated_census` and `integrate._generated_table`) point at the reader; the one-home pin test; all strict-xfail marks gone | D1; D2; D3; D4; SR-007; TC-007 | no interface (comments and a structural test) | P3; P4; P5; P6 |
| P8 | Ratchets, inside the P2 to P7 refactor commit and done before that commit's bar runs (F1): re-stamp `check.py`, `trace.py`, `integrate.py`, `agent_common.py` in `tests/test_module_size_ratchet.py` to their exact new sizes with reasons; re-measure `[dupes-census]` and re-stamp only if the reading moved; `check_complexity` clean with no baseline row added; each reason in the lane's log fragment | D7; F1; SR-007 | no interface (baseline data) | P7 |
| P9 | `RESYNC_PACK.md` §4 entry: the 11 kit-owned files to overwrite, the Q1 and Q2 read changes named, nothing to migrate | D8; SR-166; TC-176 | IF-022; IF-049; IF-068 (named as unchanged for adopters) | P7 |
| P10 | Unchanged-surface check: no diff from the claim base in the SR/LLR/TC/IF/CMP registries, any `Contract IF-NNN` body, any touched script's `--help`, `docs/cli-reference.md` or `docs/interface-reference.md`; the 13 function names and `check.load_profile`'s `Implements: SR-007, LLR-007, LLR-008` present | D5; D6; SR-007; SR-166 | IF-022; IF-049; IF-068 (verified unchanged) | P8; P9 |
| P11 | Landing-tip bar, landing alone: smoke tier within 60 s, `check_trajectory.py --strict`, `trace.py --strict` with only LLR-292's finding, the full suite (TC-007, TC-008, TC-176, TC-331 among it); holds re-confirmed; no other mechanism change landing in the same slot | D9; D10; D11; D12; D13; D14; SR-007; SR-166; TC-007; TC-008; TC-176; TC-331 | IF-022; IF-049; IF-068 (exercised end to end by the bar, the merge slot and the trunk regen) | P10 |

## Step detail

### P0: holds and base reading

- `git merge-base --is-ancestor b803dd019 HEAD` and
  `git merge-base --is-ancestor fa4bd0c49 HEAD`, both exit 0 (D10; D9's
  manifest half). If the lane is refreshed before building, re-run both.
- Record at the claim base, for P8 and P10 to compare against:
  `git grep -n 'ConfigParser(' -- project-trajectory/scripts scripts` (13
  lines); `python project-trajectory/scripts/check_dupes_census.py --root .`
  (stamped 2/2/32); the ratchet census's sizes of the four listed modules;
  `--help` output of every touched script that has a CLI (`check.py`,
  `check_doc_refs.py`, `check_dupes_census.py`, `integrate.py`, `run_menu.py`,
  `trace.py`, `trunk_step.py`, `agent_loop.py`, `dispatch.py`,
  `scripts/check_smoke_budget.py`) into the scratchpad.

### P1: the characterization test

In `tests/test_stack_profile.py` (TC-007's evidence file), one parametrized
test over the 117 cells (13 sites by 9 classes), named
`test_each_stack_ini_reader_keeps_its_outcome[<site>-<class>]`.

- **Input classes:** absent; empty; a valid file declaring the keys the site
  reads; that file with a UTF-8 BOM; with one stray `\xff` byte inside a value;
  with a parse error (a line with no section header before it, or a key with no
  delimiter); with one upper-case key (`SRC = lib`, or a `[generated]`/`[run]`
  key with capitals); with two keys differing only in case; a directory at the
  path.
- **Drivers, each the site's real function:** `check.load_profile(path)`;
  `check._generated_census(root)`; `agent_common._declared_test_command(ini)`;
  `agent_policy.read_agent_loop_config(docs)`;
  `check_doc_refs._scan_profile(root)`; `check_dupes_census._load_baseline(root)`;
  `integrate._generated_table(root)`; `kitlib.evidence.source_paths(root)`;
  `run_menu.load_capabilities(path)`; `trace._cmd_tests_for(docs, module)` over
  a minimal LLR/TC fixture (reuse `tests/test_evidence_join.py`'s `--tests-for`
  fixture shape), asserting the printed test root; `trajectory_arch._stack_ini_get`
  (through `_arch_scan_profile(root)`); `trunk_step._profile(root)`;
  `scripts/check_smoke_budget._profile()` with `STACK_INI` monkeypatched, then
  `declared_seconds` on its result.
- **Expected outcomes:** the spec's table "today" columns. The cells the table
  does not state (empty, valid, upper-case key, case-twin keys) are measured
  on the base by the builder and pinned as measured: at folded sites a case
  twin is a `DuplicateOptionError`, i.e. the site's parse-error outcome; at the
  three as-written sites both keys survive.
- **Three uncaught sites** (6, 10, 13 on a parse error, and the cells the
  table marks *traceback*): `pytest.raises(Exception)`, so the test pins that
  the call raises, never the type. The two `sys.exit` sites pin `SystemExit`
  with a non-zero code and the "is malformed" text.
- **Ruled cells** (strict `xfail`, expected value written as the NEW outcome,
  reason citing Q1 or Q2): site 1 unreadable; 4 BOM, stray; 5 BOM, unreadable;
  6 BOM, stray, unreadable; 9 BOM, stray, unreadable; 10 stray, unreadable;
  11 BOM, unreadable; 12 unreadable; 13 stray. Nothing else is marked.
- **Cross-platform:** a directory raises `PermissionError` on Windows and
  `IsADirectoryError` on POSIX; both are `OSError`, so the expected outcomes
  are platform-free. Run on Windows here; CI covers Linux and macOS.
- **Fails before the change:** by construction it passes on the base with only
  the ruled cells xfailing; it fails if any site's behaviour drifts in P3 to P6,
  and a ruled cell that starts passing XPASSes, which `strict=True` turns into a
  failure until its mark is removed. Gate for the commit: the module passes on
  the base, the xfail count equals the ruled-cell count (17), and no other
  test changes.

### P2: the reader

Shape as above. Unit tests, in `tests/test_stack_profile.py`:

- `test_the_reader_answers_none_for_an_absent_path`
- `test_the_reader_folds_keys_unless_told_not_to` (`SRC` read as `src`; with
  `fold_keys=False`, `PROJECT_STATE.html` kept)
- `test_the_reader_accepts_a_bom_and_replaces_a_stray_byte` (value read; `�`
  in it)
- `test_the_reader_keeps_percent_and_inline_semicolons_literal`
  (`a = 50% ; note` reads `50% ; note`)
- `test_the_reader_inherits_default_keys` (`[DEFAULT]`)
- `test_a_parse_error_is_the_one_error_and_names_the_file`
- `test_a_directory_at_the_path_is_the_one_error`
- `test_a_duplicate_key_is_the_one_error_only_when_folded`

Each fails before the change with `AttributeError` (`kitlib.config` has no
`read_stack_ini`/`StackIniError`).

### P3 to P6: the sites

Per the site-mapping table. In each step, after converting a site: remove that
site's strict-xfail marks, run `tests/test_stack_profile.py` and the site's
own test modules (`test_check_harness`, `test_step_path_trigger`,
`test_flag_axis`, `test_selection_at_or_above` for check;
`test_check_doc_refs`, `test_check_dupes_census`; `test_evidence_join`,
`test_trace`, `test_trajectory_arch`, `test_test_evidence` for W1;
`test_agent_common_harness`, `test_agent_loop_policy`, `test_prompts`,
`test_integrate_admission`, `test_integrate_station`, `test_generated_freshness_wiring`
for W3; `test_run_menu`, `test_check_smoke_budget`, `test_smoke_budget` for
W4). No test is added beyond P1's and P2's; the characterization cells are
the regression net.

- P3 also edits `tests/test_flag_axis.py:201` to
  `configparser.ConfigParser()` with a module-level `import configparser`
  (D5); that test fails before the change once `check.py` no longer imports
  `configparser` (`AttributeError: module 'check' has no attribute
  'configparser'`).
- P5: `agent_common`'s docstring note "Mirrors check.py's stack schema rather
  than importing it" stays true (it still reads the schema itself); only the
  parse moves to the kernel, which the note's CMP-008 to CMP-007 objection does
  not reach.

### P7: one home

- Comment and docstring edits named in the Steps row; the reader's docstring
  is the only text stating the options.
- `test_the_stack_ini_parse_is_one_home` in `tests/test_stack_profile.py`:
  walks `project-trajectory/scripts/**/*.py` and `scripts/**/*.py`, asserts
  `ConfigParser(` occurs only in `kitlib/config.py` and `import configparser`
  / `from configparser` only there, and that `interpolation=None` and
  `optionxform` occur only there. Fails before the change listing the other
  12 files. (A pin, so a 14th parse fails the full suite rather than waiting
  for the next census.)
- Done-when greps, pasted into the lane report:
  `git grep -n 'ConfigParser(' -- project-trajectory/scripts scripts` → one
  line in `kitlib/config.py`;
  `git grep -nE '^\s*(import|from) configparser' -- project-trajectory/scripts scripts`
  → only `kitlib/config.py`;
  `git grep -nE 'interpolation=None|optionxform' -- project-trajectory/scripts scripts`
  → only `kitlib/config.py`.
- `grep -c xfail tests/test_stack_profile.py` shows no WI-915 marks left; the
  module passes with 0 xfailed.

### P8: ratchets

- Measure with the ratchet's own census and re-stamp the four rows to the
  exact new sizes (all four should fall). The entry reason follows the file's
  convention ("RE-STAMPED DOWN -N (a -> b) <date>, WI-915: ..."). The
  reasons also go in the lane's log fragment
  (`docs/log.d/WI-915-one-stack-ini-loader.md`), one line per module (D7).
- Re-run `check_dupes_census.py --root .`. If it still reads 2/2/32, no
  re-stamp. If it falls, re-stamp down with the reason. If it rises (the site
  adapters scoring as a new duplicate group), do not raise the stamp: reshape
  the adapters so the group is gone, since a rise would mean the refactor
  minted the duplication it exists to remove.
- `check_complexity.py --mode enforce` clean, no new `docs/complexity-baseline`
  row (the reader stays below the threshold).
- The ratchet test runs in the commit bar's smoke tier (it is not in
  `SLOW_MODULES`). It fails before the re-stamp on the exact-equality compare,
  for shrink as well as growth. So these edits ship in the refactor commit,
  never after it (F1). The order inside the commit: P3 to P7 edits, then
  measure, then re-stamp, then `run.cmd smoke`, then commit. The census step
  reports only and never fails. Its re-stamp, if any, rides the same commit.

### P9: RESYNC entry

Appended to `project-trajectory/RESYNC_PACK.md` §4 in the latest entries'
shape: a title ("`docs/stack.ini` is read through one reader"), `[since <the
preceding trunk commit>]` with the anchoring note, **What changed** (one
reader in `scripts/kitlib/config.py`; every kit script reads through it; no
setting, key or format change), **Read changes** naming Q1 (a BOM and a stray
byte now read the same way everywhere: four readers that refused or skipped a
BOM, and four that crashed on a stray byte, now read the declared value) and
Q2 (a path that exists but cannot be read is treated as malformed: `check.py`
and `run_menu.py` exit "is malformed", the lenient readers fall to their
defaults, and the dupes census raises), **Kit-owned files — overwrite:** the
11 files of the spec's deliverable 4, and **What to do** (overwrite; nothing
migrates; nothing in the adopter's `docs/stack.ini` changes). No entry for
`check_dupes_census.py` or `scripts/check_smoke_budget.py`. SR-166 is cited
because this entry is the adopter's manifest for which files must
materialize; TC-176 (the kitlib package ships complete) runs unchanged in P11
because no kitlib module is added.

### P10: unchanged surfaces

- `git diff --stat <claim base>..HEAD -- docs/requirements docs/test` empty
  (D6; D5's "no LLR `code_symbol` cell moves").
- `git diff <claim base>..HEAD -U0 -- project-trajectory/scripts scripts | grep -E '^[-+].*Contract IF-'`
  empty.
- Every P0 `--help` capture re-taken and byte-equal.
- A trunk-style regen into a scratch copy (`trunk_step.py --regen` run against
  a temporary worktree, not the lane) leaves `docs/cli-reference.md` and
  `docs/interface-reference.md` byte-unchanged. Other generated artifacts are
  trunk-only and are not committed in the lane.
- `git grep -n 'def load_profile\|def _generated_census\|def _declared_test_command\|def read_agent_loop_config\|def _scan_profile\|def _load_baseline\|def _generated_table\|def source_paths\|def load_capabilities\|def _cmd_tests_for\|def _stack_ini_get\|def _profile'`
  over the touched files finds all 13 names (two `_profile`), and
  `check.load_profile`'s docstring still carries
  `Implements: SR-007, LLR-007, LLR-008` (D5).

### P11: the landing-tip bar

- Holds: P0's two ancestry checks on the landing tip; the coordinator
  confirms no other mechanism-change lane lands in the same slot and that the
  last one's changed step has run since (D9).
- `run.cmd smoke` within its 60 s budget (D12), pasted with its time.
- `python project-trajectory/scripts/check_trajectory.py --strict` clean
  (D13).
- `python project-trajectory/scripts/trace.py --strict` with no finding other
  than LLR-292's (D14).
- The full suite, `python -m pytest -q -n auto` (batched under the tool's
  10-minute cap if needed), including `tests/test_stack_profile.py` (TC-007,
  TC-008: the characterization, reader and one-home tests), the TC-176 nodes
  in `tests/test_bootstrap.py` and `tests/test_rule_sync.py`, and the TC-331
  nodes in `tests/test_integrate_admission.py` and `tests/test_handback.py`
  (the merge slot reading the bar through `_declared_test_command` and the
  `[generated]` table) (D11).
- After landing, the trunk regen runs through the converted
  `_generated_census`, `_generated_table` and `trunk_step._profile`; the
  coordinator watches that first regen, per the mechanism-change rule.
